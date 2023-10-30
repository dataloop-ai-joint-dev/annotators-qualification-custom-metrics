import dtlpy as dl

from deployment_parameters import project_name


def execute_connect_to_qualification(project: dl.Project, custom_metrics: dl.Service = None):
    if custom_metrics is None:
        custom_metrics = project.services.get(service_name="custom-metrics")
    custom_metrics.execute(
        function_name="connect_to_qualification",
        project_id=custom_metrics.project_id
    )


def execute_disconnect_to_qualification(project: dl.Project, custom_metrics: dl.Service = None):
    if custom_metrics is None:
        custom_metrics = project.services.get(service_name="custom-metrics")
    custom_metrics.execute(
        function_name="disconnect_from_qualification",
        project_id=custom_metrics.project_id
    )


def main():
    project = dl.projects.get(project_name=project_name)
    execute_connect_to_qualification(project=project)
    # execute_disconnect_to_qualification(project=project)


if __name__ == "__main__":
    main()
