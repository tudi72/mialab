"""The pre-processing module contains classes for image pre-processing.

Image pre-processing aims to improve the image quality (image intensities) for subsequent pipeline steps.
"""

import pymia.filtering.filter as pymia_fltr
import matplotlib.pyplot as plt
from scipy.signal import wiener
from scipy.ndimage import gaussian_filter
from datetime import datetime
import SimpleITK as sitk
import numpy as np
import warnings



def estimate_snr_histogram(noisy_image):
    # Mask out zero background
    non_zero_mask = noisy_image > 0
    non_zero_pixels = noisy_image[non_zero_mask]
    
    # Use histogram for non-zero pixels
    hist, bin_edges = np.histogram(non_zero_pixels, bins=50, range=(1, 255))
    
    # Find the lowest non-zero intensity bin (likely noise)
    noise_bin_index = np.argmin(hist)
    noise_threshold = bin_edges[noise_bin_index]
    
    # Separate signal and noise
    noise_region = non_zero_pixels[non_zero_pixels <= noise_threshold]
    signal_region = non_zero_pixels[non_zero_pixels > noise_threshold]
    
    # Calculate SNR
    signal_mean = np.mean(signal_region)
    noise_std = np.std(noise_region)
    
    if noise_std == 0:
        return float('inf'), hist, bin_edges
    
    snr = 20 * np.log10(signal_mean / noise_std)
    
    return snr, hist, bin_edges


def plot_histogram(img_arr, bins=20):
    plt.hist(img_arr.flatten(), bins=bins, alpha=0.5, label="Image Histogram")
    plt.xlabel('Intensity')
    plt.ylabel('Frequency')
    plt.title('Histogram of Image Intensities')

    # Generate a timestamp for the filename
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Create the filename with the timestamp
    filename = f'mia-result/plots/histogram_plot_{timestamp}.png'

    # Save the plot to a PNG file with timestamp
    plt.savefig(filename, format='png', dpi=300)

class WienerDenoisingFilter(pymia_fltr.Filter):
    """Represents a Wiener denoising filter for MRI image preprocessing."""
    
    def __init__(self, kernel_size: int = 3):
        """
        Initializes a new instance of the WienerDenoisingFilter class.
        
        Args:
            kernel_size (int): Size of the local neighborhood window for the Wiener filter.
        """
        self.kernel_size = kernel_size
    

    def execute(self, image: sitk.Image, params: pymia_fltr.FilterParams = None) -> sitk.Image:
        """
        Executes the Wiener denoising filter on the given image.
        
        Args:
            image (sitk.Image): Input image.
            params (pymia_fltr.FilterParams): Optional parameters for filtering.
        
        Returns:
            sitk.Image: Denoised image.
        """
        # print("[WienerDenoising]: Applying Wiener filter with kernel size", self.kernel_size)
        
        # Convert SimpleITK image to numpy array
        image_array = sitk.GetArrayFromImage(image)

        # Apply Wiener filter
        denoised_array = wiener(image_array,mysize=self.kernel_size,noise=0.1)


        denoised_image = sitk.GetImageFromArray(denoised_array)
        denoised_image.CopyInformation(image)  # Preserve image metadata

        ############### DENOISING PLOT #######################################################        
        # f, (plot1, plot2) = plt.subplots(1, 2)
        # plot1.imshow(image_array[image_array.shape[0] // 2],cmap='gray')
        # plot1.set_title("Original Image")
        # plot2.imshow(denoised_array[denoised_array.shape[0] // 2],cmap='gray') 
        # plot2.set_title("Wiener Denoised Image")
        # plt.show()
        ########################################################################################
        # plt.figure(figsize=(8, 8))
        # plt.imshow(denoised_array[denoised_array.shape[0] // 2],cmap='gray') 
        # plt.title("Wiener Denoising")
        # plt.axis('off')  
        # plt.show()
        ############### DENOISING HISTOGRAM #####################################################        
        # noisy_image = denoised_array
        # snr_value, hist, bin_edges = estimate_snr_histogram(noisy_image[noisy_image.shape[0] // 2])
        # plt.figure(figsize=(10, 6))
        # plt.bar(bin_edges[:-1], hist, width=np.diff(bin_edges), edgecolor='black', alpha=0.7)
        # plt.title(f'Histogram after denoising (SNR: {snr_value:.2f} dB)')
        # plt.xlabel('Pixel Intensity')
        # plt.ylabel('Frequency')
        # noise_bin_index = np.argmin(hist)
        # plt.axvline(x=bin_edges[noise_bin_index], color='r', linestyle='--', label='Noise Threshold')
        # plt.legend()
        # plt.tight_layout()
        # plt.show()
        # print(f"Estimated SNR: {snr_value:.2f} dB")
        ########################################################################################



        return denoised_image

class Resampling(pymia_fltr.Filter):
    """Represents various resampling methods for MRI image preprocessing."""

    def __init__(self, new_spacing = (1, 1 , 1),method = 'NN'):
        """Initializes a new instance of the Resampling class."""
        self.new_spacing = new_spacing
        self.method = method

    def execute(self, image: sitk.Image, params: pymia_fltr.FilterParams = None) -> sitk.Image: 

        # new_spacing = self.new_spacing
        new_spacing = (0.6, 0.6, 0.6)
 
        # print("[Resampling]: original space ", image.GetSpacing()," ---Upsampling---> ",new_spacing)

        original_spacing = image.GetSpacing()
        original_size = image.GetSize()
        
        new_size = [
            int(np.round(original_size[0] * (original_spacing[0] / new_spacing[0]))),
            int(np.round(original_size[1] * (original_spacing[1] / new_spacing[1]))),
            int(np.round(original_size[2] * (original_spacing[2] / new_spacing[2])))]
            

        resampler = sitk.ResampleImageFilter()
        resampler.SetOutputDirection(image.GetDirection())      # direction from input
        resampler.SetOutputOrigin(image.GetOrigin())            # origin from input
        resampler.SetOutputSpacing(new_spacing)                 # new spacing
        resampler.SetSize(new_size)                             # new size

        resampler.SetTransform(sitk.Transform())                # transform ?  
        resampler.SetDefaultPixelValue(image.GetPixelIDValue()) # origin pixel value 

        match self.method: 
            case 'NN':
                resampler.SetInterpolator(sitk.sitkNearestNeighbor)
            case 'linear':
                resampler.SetInterpolator(sitk.sitkLinear)
            case 'Bspline':
                resampler.SetInterpolator(sitk.sitkBSpline)
            case _: 
                resampler.SetInterpolator(sitk.sitkNearestNeighbor)

        resampled_image = resampler.Execute(image)
        
        ############### DENOISING PLOT #######################################################        
        # image_array = sitk.GetArrayFromImage(image)
        # resampled_array = sitk.GetArrayFromImage(resampled_image)
        # f, (plot1, plot2) = plt.subplots(1, 2)
        # plot1.imshow(image_array[image_array.shape[0] // 2],cmap='gray')
        # plot1.set_title("Original Image")
        # # plot1.set_aspect('auto')
        # plot2.imshow(resampled_array[resampled_array.shape[0] // 2],cmap='gray') 
        # # plot2.set_aspect('auto')  # Set aspect ratio to auto to stretch the axes
        # plot2.set_title("Resampled Image")
        # plt.show()        
        ########################################################################################
        # resampled_array = sitk.GetArrayFromImage(resampled_image)
        # plt.figure(figsize=(8, 8))
        # plt.imshow(resampled_array[resampled_array.shape[0] // 2],cmap='gray') 
        # plt.title("Resampling")
        # plt.axis('off')  
        # plt.show()
        ########################################################################################



        return resampled_image


    def __str__(self):
        """Gets a printable string representation of the Resampling class."""
        return 'Resampling Methods: Nearest Neighbor, Bilinear, Cubic, Spline'

class ImageNormalization(pymia_fltr.Filter):
    """Represents a normalization filter."""

    def __init__(self):
        """Initializes a new instance of the ImageNormalization class."""
        super().__init__()

    def execute(self, image: sitk.Image, params: pymia_fltr.FilterParams = None) -> sitk.Image:
        """Executes a normalization on an image.

        Args:
            image (sitk.Image): The image.
            params (FilterParams): The parameters (unused).

        Returns:
            sitk.Image: The normalized image.
        """

        img_arr = sitk.GetArrayFromImage(image)


        img_min = img_arr.min()
        img_max = img_arr.max()

        # SANITY CHECK: image intensity evaluation
        img_mean = img_arr.mean()
        img_std = img_arr.std()

        # print(f"Mean intensity: {img_mean:.2f}, Standard deviation: {img_std:.2f}")
        voxel_size = image.GetSpacing()  # Returns a tuple (x, y, z)
        # print("Voxel size:", voxel_size,'\n')

        if img_max > img_min:
            normalized_array = (img_arr - img_min) / (img_max - img_min)
        else:
            warnings.warn(f"Image has no intensity range (max == min). Returning unprocessed image. mean:{img_mean}, std:img_std")
            normalized_array = img_arr    



        ##################NORMALIZATION PLOT###################################################
        # plt.figure(figsize=(8, 8))
        # plt.imshow(normalized_array[normalized_array.shape[0] // 2], cmap='gray')
        # plt.title("Normalization")
        # plt.axis('off')  
        # plt.show()
        ########################################################################################

        img_out = sitk.GetImageFromArray(normalized_array)
        img_out.CopyInformation(image)

        # show_image(img_out, title='Image after normalization')
        
        return img_out

    def __str__(self):
        """Gets a printable string representation.

        Returns:
            str: String representation.
        """
        return 'ImageNormalization:\n' \
            .format(self=self)

class SkullStrippingParameters(pymia_fltr.FilterParams):
    """Skull-stripping parameters."""

    def __init__(self, img_mask: sitk.Image):
        """Initializes a new instance of the SkullStrippingParameters

        Args:
            img_mask (sitk.Image): The brain mask image.
        """
        self.img_mask = img_mask

class SkullStripping(pymia_fltr.Filter):
    """Represents a skull-stripping filter."""

    def __init__(self):
        """Initializes a new instance of the SkullStripping class."""
        super().__init__()

    def execute(self, image: sitk.Image, params: SkullStrippingParameters = None) -> sitk.Image:
        """Executes a skull stripping on an image.

        Args:
            image (sitk.Image): The image.
            params (SkullStrippingParameters): The parameters with the brain mask.

        Returns:
            sitk.Image: The normalized image.
        """
        mask = params.img_mask  # the brain mask


        skull_stripped_image = image
        try:
            if mask.GetSize() != image.GetSize():
                raise ValueError("The mask and image must have the same dimensions.")

            skull_stripped_image = sitk.Mask(image, mask)

        except Exception as e:
            print("[SkullStripping]: ",e)

        ##################SKULL STRIPPING PLOT##################################################
        # skull_stripped_array = sitk.GetArrayFromImage(skull_stripped_image)
        # plt.figure(figsize=(8, 8))
        # plt.imshow(skull_stripped_array[skull_stripped_array.shape[0] // 2], cmap='gray')
        # plt.title("Skull Stripping")
        # plt.axis('off')  
        # plt.show()
        ########################################################################################

        return skull_stripped_image

    def __str__(self):
        """Gets a printable string representation.

        Returns:
            str: String representation.
        """
        return 'SkullStripping:\n' \
            .format(self=self)

class ImageRegistrationParameters(pymia_fltr.FilterParams):
    """Image registration parameters."""

    def __init__(self, atlas: sitk.Image, transformation: sitk.Transform, is_ground_truth: bool = False):
        """Initializes a new instance of the ImageRegistrationParameters

        Args:
            atlas (sitk.Image): The atlas image.
            transformation (sitk.Transform): The transformation for registration.
            is_ground_truth (bool): Indicates weather the registration is performed on the ground truth or not.
        """
        self.atlas = atlas
        self.transformation = transformation
        self.is_ground_truth = is_ground_truth

class ImageRegistration(pymia_fltr.Filter):
    """Represents a registration filter."""

    def __init__(self):
        """Initializes a new instance of the ImageRegistration class."""
        super().__init__()

    def execute(self, image: sitk.Image, params: ImageRegistrationParameters = None) -> sitk.Image:
        """Registers an image.

        Args:
            image (sitk.Image): The image.
            params (ImageRegistrationParameters): The registration parameters.

        Returns:
            sitk.Image: The registered image.
        """

        # todo: replace this filter by a registration. Registration can be costly, therefore, we provide you the
        # transformation, which you only need to apply to the image!

        atlas = params.atlas
        transform = params.transformation
        is_ground_truth = params.is_ground_truth  # the ground truth will be handled slightly different

        interpolator = sitk.sitkNearestNeighbor if is_ground_truth else sitk.sitkLinear

        registered_image = image
        try:
           registered_image = sitk.Resample(
                image,                   # Input image
                atlas,                   # Reference atlas for output grid
                transform,               # Precomputed transformation
                interpolator,            # Interpolation method
                0.0,                     # Default pixel value for out-of-bounds areas
                image.GetPixelID()       # Maintain the pixel type of the input image
            )

        except Exception as e:
            print("[ImageRegistration]: ",e)

        # note: if you are interested in registration, and want to test it, have a look at
        # pymia.filtering.registration.MultiModalRegistration. Think about the type of registration, i.e.
        # do you want to register to an atlas or inter-subject? Or just ask us, we can guide you ;-)

        # show_image(registered_image, title='Image after registration')

        ##################REGISTRATION PLOT###################################################
        # registered_array = sitk.GetArrayFromImage(registered_image)
        # plt.figure(figsize=(8, 8))
        # plt.imshow(registered_array[registered_array.shape[0] // 2], cmap='gray')
        # plt.title("Registration")
        # plt.axis('off')  
        # plt.show()
        ########################################################################################

        return registered_image

    def __str__(self):
        """Gets a printable string representation.

        Returns:
            str: String representation.
        """
        return 'ImageRegistration:\n' \
            .format(self=self)

