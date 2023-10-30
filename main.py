import dtlpy as dl

from custom_metrics import CustomMetrics


class ServiceRunner(dl.BaseServiceRunner):
    def __init__(self):
        try:
            self.service = self.service_entity
            self.project = self.service_entity.project
            print("Working on remote mode")
        except:
            self.service = None
            self.project = None
            print("Working on local mode")

    @staticmethod
    def measure_annotations(annotations_set_one: dl.AnnotationCollection,
                            annotations_set_two: dl.AnnotationCollection,
                            ignore_labels: bool = False,
                            ignore_attributes: bool = False,
                            match_threshold: float = 0.1):
        custom_metrics = CustomMetrics()
        results = custom_metrics.measure_annotations(
            annotations_set_one=annotations_set_one,
            annotations_set_two=annotations_set_two,
            ignore_labels=ignore_labels,
            ignore_attributes=ignore_attributes,
            match_threshold=match_threshold
        )
        return results

    ###############################
    # Connections Setup Functions #
    ###############################
    def connect_to_qualification(self):
        try:
            qualification = self.project.services.get(service_name="annotators-qualification")
            qualification.execute(
                function_name="add_custom_metrics",
                execution_input=[
                    dl.FunctionIO(
                        type=dl.PackageInputType.SERVICE,
                        value=self.service.id,
                        name="service",
                    )
                ],
                project_id=qualification.project_id
            )

        except Exception as e:
            raise dl.exceptions.BadRequest(
                status_code="400",
                message=f"Encountered the following error: {e}"
            )

    def disconnect_from_qualification(self):
        try:
            qualification = self.project.services.get(service_name="annotators-qualification")
            qualification.execute(
                function_name="remove_custom_metrics",
                project_id=qualification.project_id
            )

        except Exception as e:
            raise dl.exceptions.BadRequest(
                status_code="400",
                message=f"Encountered the following error: {e}"
            )


def test_measure_annotations():
    test_item = dl.items.get(item_id="64eddcfaccea6ab3b2012364")
    ref_item = dl.items.get(item_id="64ede1df5caa1ae751504095")

    sr = ServiceRunner()
    results = sr.measure_annotations(
        annotations_set_one=test_item.annotations.list(),
        annotations_set_two=ref_item.annotations.list(),
        ignore_labels=False,
        ignore_attributes=False,
        match_threshold=0.1
    )
    print(results)


def main():
    test_measure_annotations()


if __name__ == "__main__":
    main()
