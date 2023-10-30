# Annotators Qualification Custom Metrics

Custom Metrics service to provide custom calculations of annotation scores for 
**Dataloop Annotators Qualification App**.

In order to install the **Dataloop Annotators Qualification App** please contact your Customer Success Manager. 

## How to Customize:

The only function that needs to be updated is `measure_annotations` in the script: [custom_metrics.py](custom_metrics.py). \
The function should return a `dict` in the following structure:
```
{
    "scores": {
        "<annotation-type>": {  \\ Per annotation type
            "annotation_score: number,  \\ (Must) final score for the annotation-type
            "label_score": number,  \\ (Optional) label comparison scroe for the annotation-type
            "attributes_score": number,  \\ (Optional) attributes comparison scroe for the annotation-type
            "ref_number": number,  \\ (Optional) number of annotations in the ground truth
            "test_number": number,  \\ (Optional) number of annotations from the annotator exam
            "match_number": number,  \\ (Optional) number of matched annotations
            "<metric-name>_score": number,  \\ (Optional) Per requestet metric
            "<metric-name>_number": number,  \\ (Optional) Per requested metric
        }
    }
    "total_score": number  \\ (Optional) If not provided, the mean of all the annotation_score fields will be taken.
} 
```

## How to deploy:

1. Make sure that the `project_name` is correct in [deployment_parameters.py](deployment_parameters.py).
2. Run the script [service_deployment.py](service_deployment.py).

## How to connect to Qualification App:
1. Make sure that the `project_name` is correct in [deployment_parameters.py](deployment_parameters.py).
2. Run the function `execute_connect_to_qualification` in the script: [add_service_to_app.py](add_service_to_app.py).

## How to disconnect from Qualification App:
1. Make sure that the `project_name` is correct in [deployment_parameters.py](deployment_parameters.py).
2. Run the function `execute_disconnect_to_qualification` in the script: [add_service_to_app.py](add_service_to_app.py).

## Requirements

`dtlpy`

If you use specific libraries for calculations, don't forget to add them to a `requirement.txt` file
