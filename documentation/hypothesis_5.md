# HYPOTHESIS 5

**_We investigate the effects of various normalization methods on the final accuracy of brain tissue segmentation, and hypothesize that z-score normalization performs better than other normalization techniques and significantly influences segmentation performance._**

_Pre-processing Category: Normalization_

## Aim:
- To investigate how different image intensity normalization methods affect the performance of brain tissue segmentation using MR images.
- The goal is to determine whether advanced normalization techniques lead to better segmentation results compared to the standard z-score normalization currently implemented in the pipeline.

## Things we could Explore:
1. **Comparison of Normalization Methods:** Implement various normalization techniques such as min-max scaling, histogram matching, z-score normalization with and without 95% range clipping, and assess their impact on segmentation performance.
2. **Necessity of Normalization:** Evaluate if normalization is essential by including a control group where no normalization is applied. This will help determine the baseline performance without any intensity scaling.
3. **Data Inspection:** Analyze the provided dataset to check if it is already normalized in some way, which could influence the effectiveness of additional normalization steps.
4. **Negative Control:** Intentionally unnormalize data (e.g., by introducing intensity variability) to observe any negative effects on segmentation performance, reinforcing the importance of proper normalization.

## Experimental Design:
1. **Dataset Preparation:** Use the same MR images, applying different normalization methods to create multiple datasets while keeping all other variables constant.
2. **Model Training:** Train the segmentation model separately on each normalized dataset, ensuring that training parameters and random seeds are consistent to control for confounders.
3. **Performance Evaluation:** Use metrics like Dice coefficient, sensitivity, and specificity to evaluate segmentation performance on a consistent test set across all normalization methods.
4. **Statistical Analysis:** Perform statistical tests to determine if observed improvements are significant, providing robust conclusions about the effectiveness of additional normalization steps.
