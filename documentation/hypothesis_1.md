# HYPOTHESIS 1

**_We investigate the effects of background removal through skull stripping on the final accuracy of brain tissue segmentation, and hypothesize that applying skull stripping significantly improves segmentation performance compared to using non-skull-stripped images._**

_Pre-processing Category: Background Removal_

## Aim:
- To evaluate the effect of skull stripping (background removal) on the performance of brain tissue segmentation.
- Skull stripping removes non-brain tissues such as the skull and scalp, potentially reducing irrelevant information and focusing the model on regions of interest.

## Things we could Explore:
1. **Effectiveness of Skull Stripping:** Assess how skull stripping influences segmentation accuracy by comparing results from skull-stripped and non-skull-stripped images.
2. **Implementation Methods:** Use established skull stripping algorithms (e.g., BET from FSL) to ensure consistent and reliable background removal.
3. **Impact on Different Structures:** Investigate whether the improvement is uniform across all brain structures (e.g., hippocampus, amygdala) or more significant for certain areas.

## Experimental Design:
1. **Data Processing:** Create two versions of the dataset—one with skull stripping applied and one without. Ensure that other pre-processing steps like normalization are applied equally to both datasets.
2. **Model Training:** Train identical segmentation models on both datasets, maintaining the same hyperparameters and training protocols.
3. **Evaluation:** Compare the segmentation performance using the same evaluation metrics and test data, focusing on the differences attributed to skull stripping.
4. **Analysis:** Examine segmentation errors to understand how background removal affects model predictions, possibly using qualitative assessments alongside quantitative metrics.