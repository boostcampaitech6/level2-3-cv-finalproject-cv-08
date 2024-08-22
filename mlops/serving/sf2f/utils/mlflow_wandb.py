import mlflow
import wandb

def mlflow_wandb_logging(log_dict,model,signature,input_sample,sample_image):
    #mlflow Log metric & model
    mlflow.log_metrics(log_dict)
    mlflow.pytorch.log_model(
        pytorch_model=model,
        artifact_path = "sf2f_pytorch",
        signature= signature,
        input_example = input_sample,
        # pip_requirements = "rec.txt"
    )
    log_dict['sample'] = [wandb.Image(sample_image, caption=f"Sample")]
    wandb.log(log_dict)
