import dtlpy as dl
import pandas as pd
import statistics
from collections import defaultdict


class CustomMetrics:
    def __init__(self):
        self.supported_annotations = [
            dl.AnnotationType.CLASSIFICATION,
            dl.AnnotationType.POINT,
            dl.AnnotationType.BOX,
            dl.AnnotationType.CUBE,
            dl.AnnotationType.SEGMENTATION,
            dl.AnnotationType.POLYGON,
            dl.AnnotationType.POLYLINE,
            dl.AnnotationType.ELLIPSE,
        ]

    # TODO: Implement your own scores calculations
    def measure_annotations(self,
                            annotations_set_one: dl.AnnotationCollection,
                            annotations_set_two: dl.AnnotationCollection,
                            ignore_labels: bool,
                            ignore_attributes: bool,
                            match_threshold: float):
        """
        Compare annotations sets between two items
        :param annotations_set_one: Annotations of the ref_item
        :param annotations_set_two: Annotations of the test_item
        :param ignore_labels: Flag to ignore label scores in annotation score
        :param ignore_attributes: Flag to ignore attributes scores in annotation score
        :param match_threshold: Threshold of annotation score for a match
        :return: results
        """
        # In the following script example, the annotation score is calculated only by the mean of the
        # label_score and attributes_score
        scores_dict = dict()

        for annotation_type in self.supported_annotations:
            subset_one = [a1 for a1 in annotations_set_one if a1.type == annotation_type]
            subset_two = [a2 for a2 in annotations_set_two if a2.type == annotation_type]

            if len(subset_one) >= 1 and len(subset_two) >= 1:
                match_list = list()
                label_scores_dict = defaultdict(dict)
                attributes_scores_dict = defaultdict(dict)
                annotation_scores_dict = defaultdict(dict)

                scores_df = pd.DataFrame(
                    data=[[0.0 for _ in range(len(subset_one))] for _ in range(len(subset_two))],
                    columns=[a1.id for a1 in subset_one],
                    index=[a2.id for a2 in subset_two]
                )
                for a1 in subset_one:
                    for a2 in subset_two:
                        annotation_score = list()

                        # Label Score
                        label_score = 1.0 if a1.label == a2.label else 0.0
                        label_scores_dict[a1.id][a2.id] = label_score
                        if ignore_labels is False:
                            annotation_score.append(label_score)

                        # Attributes Score
                        attributes_score = 1.0 if a1.attributes == a2.attributes else 0.0
                        attributes_scores_dict[a1.id][a2.id] = attributes_score
                        if ignore_attributes is False:
                            annotation_score.append(attributes_score)

                        # Annotation Score
                        annotation_score = statistics.mean(annotation_score) if annotation_score else 0.0
                        annotation_scores_dict[a1.id][a2.id] = annotation_score
                        scores_df[a1.id][a2.id] = annotation_score

                print(f"Scores Matrix ({annotation_type}):\n{scores_df}")
                for a1_id in scores_df.columns:
                    a2_id = scores_df[a1_id].idxmax()
                    # print(f"Match: {a1_id} - {a2_id}")

                    if scores_df[a1_id][a2_id] > match_threshold:
                        match_list.append([a1_id, a2_id])
                        scores_df = scores_df.drop(index=[a2_id])

                # Calculate statistics
                final_annotation_scores_list = list()
                final_label_scores_list = list()
                final_attributes_scores_list = list()
                for match in match_list:
                    a1_id, a2_id = match
                    final_annotation_scores_list.append(annotation_scores_dict[a1_id][a2_id])
                    final_label_scores_list.append(label_scores_dict[a1_id][a2_id])
                    final_attributes_scores_list.append(attributes_scores_dict[a1_id][a2_id])

                mean_annotation_score = (
                    statistics.mean(final_annotation_scores_list) if final_annotation_scores_list else 0.0
                )
                mean_label_score = (
                    statistics.mean(final_label_scores_list) if final_label_scores_list else 0.0
                )
                mean_attributes_score = (
                    statistics.mean(final_attributes_scores_list) if final_attributes_scores_list else 0.0
                )
                ref_number = len(subset_one)
                test_number = len(subset_two)
                match_number = len(match_list)

                scores_dict[annotation_type] = {
                    "annotation_score": mean_annotation_score,
                    "label_score": mean_label_score,
                    "attributes_score": mean_attributes_score,
                    "ref_number": ref_number,
                    "test_number": test_number,
                    "match_number": match_number
                }
            elif len(subset_one) >= 1 or len(subset_two) >= 1:
                ref_number = len(subset_one)
                test_number = len(subset_two)

                scores_dict[annotation_type] = {
                    "annotation_score": 0.0,
                    "label_score": 0.0,
                    "attributes_score": 0.0,
                    "ref_number": ref_number,
                    "test_number": test_number,
                    "match_number": 0
                }

        total_scores_list = list()
        for _, measure in scores_dict.items():
            total_scores_list.append(measure["annotation_score"])

        results = dict()
        results["scores"] = scores_dict

        # Adding total_score is optional. If not provided, the qualification app will calculate it by taking the mean
        # of all the annotation_score per annotation_type field.
        results["total_score"] = statistics.mean(total_scores_list) if total_scores_list else 0.0

        return results
