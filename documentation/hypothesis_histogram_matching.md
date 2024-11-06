
A histogram matching method was proposed for correcting the variations in scanner
sensitivity due to differences in scanner performance [1]. It was shown that this method
can reduce the variations in white matter (WM) intensities from 7.5 to 2.5%.  


In addition, some histogram matching algorithms were designed to
match the histogram of the **input image*** with the histogram of the **reference image** by
minimizing some information-centric criteria, such as through a **joint histogram** [2]. But this method suffers from unreliable processing results.
Because, in order for the existing histogram matching based on a joint histogram to achieve a more reliable implementation, it required a better prior knowledge based of the neighborhoods used to split up the image into K sub-images, which are corrected separately.

Global Histogram Normalization with low computation complexity and no parameter tuning. Implements intensity normalization to achieve homogeneous intensities or similar image quality for two brain MR images acquired from two
different field strength scanners with different acquisition parameters

CONCLUSION: histogram matching is not feasible because our Human Connectome Dataset is has the same acquisition parameters and same imaging devices across all patients. To verify, we did a sanity check for printing the mean, standard and histogram of each patient. All of them are uniform with the following values: 
```
----- Training...
---------- Processing 100307
Mean intensity: 25.07, Standard deviation: 60.34
Mean intensity: 25.06, Standard deviation: 60.33
---------- Processing 100408
Mean intensity: 24.28, Standard deviation: 59.56
Mean intensity: 24.28, Standard deviation: 59.55
---------- Processing 101107
Mean intensity: 25.23, Standard deviation: 60.51
Mean intensity: 25.22, Standard deviation: 60.49
```

CONCLUSION 2: NORMALIZATION (E.G. standardization) would not work since the patients are already normalized, the sanity check confirms this (mean, std) values.


*1. Collewet G, Strzelecki M, Marriette F. Influence of MRI acquisition protocols and image intensity normalization
methods on texture classification. Magn Reson Imag. 2004;22(1):81–91.*

*2. Jager F, Hornegger J. Nonrigid registration of joint histograms for intensity standardization in magnetic resonance
imaging. IEEE Trans Med Imag. 2009;28(1):137–50*