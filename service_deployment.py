import dtlpy as dl
from typing import List

from deployment_parameters import project_name, package_name
from add_service_to_app import execute_connect_to_qualification


def create_modules(package_name: str) -> List[dl.PackageModule]:
    modules = [
        dl.PackageModule(
            name=package_name,
            class_name='ServiceRunner',
            entry_point='main.py',
            functions=[
                dl.PackageFunction(
                    name='measure_annotations',
                    inputs=[
                        dl.FunctionIO(type=dl.PackageInputType.ANNOTATIONS, name='annotations_set_one'),
                        dl.FunctionIO(type=dl.PackageInputType.ANNOTATIONS, name='annotations_set_two'),
                        dl.FunctionIO(type=dl.PackageInputType.BOOLEAN, name='ignore_labels'),
                        dl.FunctionIO(type=dl.PackageInputType.BOOLEAN, name='ignore_attributes'),
                        dl.FunctionIO(type=dl.PackageInputType.FLOAT, name='match_threshold')
                    ],
                    outputs=[
                        dl.FunctionIO(
                            type=dl.PackageInputType.JSON,
                            name='results'
                        )
                    ]
                ),
                dl.PackageFunction(
                    name='connect_to_qualification',
                    inputs=[],
                    outputs=[]
                ),
                dl.PackageFunction(
                    name='disconnect_from_qualification',
                    inputs=[],
                    outputs=[]
                ),
            ]
        )
    ]
    return modules


def create_package(project: dl.Project, package_name: str, modules: List[dl.PackageModule],
                   slots: List[dl.PackageSlot] | None, upload_package: bool) -> dl.Package:
    if upload_package:
        package = project.packages.push(
            package_name=package_name,
            modules=modules,
            slots=slots,
            service_config={
                'runtime': dl.KubernetesRuntime(
                    concurrency=1,
                    autoscaler=dl.KubernetesRabbitmqAutoscaler(
                        min_replicas=0,
                        max_replicas=10,
                        queue_length=100
                    )
                ).to_json()
            },
            src_path='.'
        )
        print("package has been deployed: ", package.name)
    else:
        package = project.packages.get(package_name=package_name)
        print("package has been gotten: ", package.name)

    return package


def create_service(project: dl.Project, package: dl.Package, slots: List[dl.PackageSlot] | None) -> dl.Service:
    try:
        service = package.services.get(service_name=package.name)
        print("service has been gotten: ", service.name)
    except dl.exceptions.NotFound:
        service = package.services.deploy(
            service_name=package.name,
            module_name=package.name,
        )
        print("service has been deployed: ", service.name)

    print("package.version: ", package.version)
    print("service.package_revision: ", service.package_revision)
    print("service.runtime.concurrency: ", service.runtime.concurrency)
    service.runtime.autoscaler.print()

    if package.version != service.package_revision:
        service.package_revision = package.version
        service.update(force=True)
        print("service.package_revision has been updated: ", service.package_revision)

    if slots and len(slots):
        try:
            service.activate_slots(project_id=project.id)
            print("Slot has been activated")
        except:
            print("Slot is already existing")

    return service


def deploy(project: dl.Project, package_name: str, upload_package: bool, connect_to_application: bool):
    ##################
    # create modules #
    ##################
    modules = create_modules(package_name)
    ################
    # create slots #
    ################
    slots = None
    ##################
    # create package #
    ##################
    package = create_package(project=project, package_name=package_name, modules=modules, slots=slots,
                             upload_package=upload_package)
    ##################
    # create service #
    ##################
    service = create_service(project=project, package=package, slots=slots)

    if connect_to_application:
        execute_connect_to_qualification(project=project, custom_metrics=service)


def main():
    upload_package = True
    connect_to_application = True

    project = dl.projects.get(project_name=project_name)
    deploy(project=project, package_name=package_name, upload_package=upload_package)


if __name__ == '__main__':
    main()
