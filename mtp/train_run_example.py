import sys
import os
import time
from datetime import datetime

# Add the project root to Python path so we can import from src
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.model_training_pipeline.utils import load_config, get_logger
from src.model_training_pipeline.data import load_data, check_for_new_dataset, update_last_training_date
from src.model_training_pipeline.preprocessing import balance_data, stratified_train_test_split
from src.model_training_pipeline.training import train_model
from src.model_training_pipeline.evaluation import evaluate_model
from src.model_training_pipeline.persistence import save_model_to_gcs
from src.model_training_pipeline.model_registry import ModelRegistry
import pandas as pd

# Set config path relative to project root
CONFIG_PATH = os.environ.get('PIPELINE_CONFIG', os.path.join(project_root, 'config.yaml'))

def main():
    start_time = time.time()
    config = load_config(CONFIG_PATH)
    logger = get_logger('train_pipeline')
    logger.info('Starting model training pipeline...')
    logger.info('Pipeline config loaded: %s', config)

    # Check for new training dataset
    data_dir = os.path.join(project_root, 'src', 'data')
    naming_pattern = config['data']['naming_pattern']
    
    logger.info('Checking for new training dataset...')
    has_new_data, dataset_path, dataset_date = check_for_new_dataset(data_dir, naming_pattern)
    
    if not has_new_data:
        logger.info('No new training dataset found. Exiting pipeline.')
        print("No new training dataset")
        sys.exit(0)
    
    logger.info('New training dataset found: %s (date: %s)', dataset_path, dataset_date)
    
    # Initialize model registry
    registry = ModelRegistry()
    
    try:
        # Load and validate training data from the discovered dataset
        logger.info('Loading training data from: %s', dataset_path)
        df = load_data(dataset_path)
        logger.info('Final training data shape: %s', df.shape)
        if df.empty:
            logger.error('No valid training data found. Exiting pipeline.')
            sys.exit(1)

        # Preprocessing: Balance data if enabled
        if config['preprocessing']['balance']:
            logger.info('Balancing dataset...')
            df = balance_data(
                df, 
                label_col='intent', 
                method=config['preprocessing']['balance_method'],
                random_state=config['data']['random_state']
            )
            logger.info('Balanced dataset shape: %s', df.shape)

        # Split data into train/test sets
        logger.info('Splitting data into train/test sets...')
        X_train, X_test, y_train, y_test = stratified_train_test_split(
            df,
            label_col='intent',
            test_size=config['data']['test_size'],
            random_state=config['data']['random_state']
        )
        logger.info('Train set: %s, Test set: %s', X_train.shape, X_test.shape)

        # Train model
        logger.info('Training model...')
        model, metadata = train_model(X_train, y_train, config['model'])
        logger.info('Model training completed. Version: %s', metadata['model_version'])

        # Save model to GCS
        logger.info('Saving model to GCS...')
        gcs_info = save_model_to_gcs(
            model, 
            metadata, 
            bucket_name='pcc-datasets',
            model_prefix='pcc-models'
        )
        logger.info('Model saved to GCS: %s', gcs_info["model_gcs_path"])

        # Evaluate model
        logger.info('Evaluating model...')
        # Generate case IDs for test set
        case_ids = [f'case_{i}' for i in range(len(y_test))]
        
        metrics = evaluate_model(
            model=model,
            X_test=X_test,
            y_test=y_test,
            case_ids=case_ids,
            model_version=metadata['model_version'],
            embedding_model=config['preprocessing']['embedding_model']
        )
        
        logger.info('Model evaluation completed. Accuracy: %.4f', metrics["accuracy"])
        logger.info('F1 (weighted): %.4f', metrics["f1_weighted"])
        
        # Update last training date record
        update_last_training_date(dataset_date)
        
        # Log run to registry
        run_data = {
            'run_id': f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'model_version': metadata['model_version'],
            'training_timestamp': metadata['training_timestamp'],
            'dataset_date': dataset_date.isoformat(),
            'data_info': {
                'total_samples': len(df),
                'train_samples': len(X_train),
                'test_samples': len(X_test),
                'feature_dimensions': metadata['feature_dimensions'],
                'classes': metadata['classes'],
                'class_distribution': metadata['class_distribution']
            },
            'hyperparameters': metadata['hyperparameters'],
            'search_method': metadata['search_method'],
            'search_info': metadata['search_info'],
            'metrics': metrics,
            'gcs_paths': gcs_info,
            'status': 'success',
            'duration_seconds': time.time() - start_time,
            'notes': f"Pipeline run with {config['model']['search_method']} search on dataset {dataset_date}"
        }
        
        run_id = registry.log_run(run_data)
        logger.info('Logged run %s to registry', run_id)
        
        # Export registry to CSV for analysis
        registry.export_registry_to_csv()
        
        # Print performance summary
        summary = registry.get_performance_summary()
        logger.info('Performance summary: %s', summary)
        
        logger.info('Pipeline completed successfully!')
        
    except Exception as e:
        logger.error('Pipeline failed: %s', e)
        
        # Log failed run to registry
        run_data = {
            'run_id': f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'model_version': None,
            'training_timestamp': datetime.now().isoformat(),
            'dataset_date': dataset_date.isoformat() if dataset_date else None,
            'data_info': {},
            'hyperparameters': {},
            'search_method': None,
            'search_info': {},
            'metrics': {},
            'gcs_paths': {},
            'status': 'failed',
            'duration_seconds': time.time() - start_time,
            'notes': f"Pipeline failed: {str(e)}"
        }
        
        registry.log_run(run_data)
        raise

if __name__ == '__main__':
    main() 