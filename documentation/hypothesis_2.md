# HYPOTHESIS 2

**_We investigate the combined effects of multiple pre-processing steps on the final accuracy of brain tissue segmentation, and hypothesize that combining normalization and denoising leads to additive improvements in segmentation performance over using each method individually._**

_Pre-processing Category: Combination [Background Removal, Noise Reduction, Normalization]_

## Aim:
- To explore whether the sequential application of pre-processing techniques such as normalization and denoising results in cumulative benefits for segmentation performance.

## Things we could Explore:
1. **Additive Effects:** Determine if the improvements from individual pre-processing steps are additive when combined.
2. **Optimal Pre-processing Pipeline:** Identify the most effective sequence of pre-processing steps that maximize segmentation accuracy.
3. **Interaction Between Steps:** Understand how different pre-processing methods interact and whether some combinations are more beneficial than others.

## Experimental Design:
1. **Pre-processing Combinations:** Create datasets with various combinations of pre-processing steps:
   - No pre-processing (baseline)
   - Normalization only
   - Denoising only
   - Both normalization and denoising
2. **Model Training:** Train the segmentation model on each dataset separately, ensuring consistency in training conditions.
3. **Performance Comparison:** Evaluate the segmentation results to see if the combination of normalization and denoising leads to better performance than each method alone.
4. **Statistical Validation:** Use statistical methods to assess whether observed improvements are significant.

_Note: Could be extended to include skull stripping._
