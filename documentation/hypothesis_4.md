# HYPOTHESIS 4

**_We investigate the effects of histogram matching for intensity normalization across subjects on the final accuracy of brain tissue segmentation, and hypothesize that histogram matching improves segmentation performance compared to standard normalization methods like z-score normalization._**

_Pre-processing Category: Normalization_

## Aim:
- To investigate whether histogram matching can better standardize intensity distributions across subjects, leading to improved segmentation performance.

## Things we could Explore:
1. **Standardization Across Subjects:** Evaluate if histogram matching reduces inter-subject variability more effectively than methods like z-score normalization.
2. **Selection of Reference Histogram:** Determine the optimal reference histogram (e.g., from an atlas or average of training images) for matching.
3. **Effect on Model Generalization:** Assess whether improved intensity consistency translates to better model performance on unseen data.

## Experimental Design:
1. **Histogram Matching Application:** Apply histogram matching to all MR images using a chosen reference histogram.
2. **Comparison with Other Methods:** Create datasets normalized with z-score normalization and min-max scaling for comparative analysis.
3. **Model Training:** Train the segmentation model on each normalized dataset under identical conditions.
4. **Evaluation and Analysis:** Compare segmentation performances, focusing on whether histogram matching offers a significant advantage.

_Note: Not sure about this one since intensity normalization likely doesn’t significantly impact segmentation performance when using datasets where intensity values are already standardized, such as the Human Connectome Project dataset._