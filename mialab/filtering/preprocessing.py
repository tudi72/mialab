"""The pre-processing module contains classes for image pre-processing.

Image pre-processing aims to improve the image quality (image intensities) for subsequent pipeline steps.
"""

import pymia.filtering.filter as pymia_fltr
import matplotlib.pyplot as plt 
from scipy.signal import wiener
from datetime import datetime
import SimpleITK as sitk
import numpy as np
import warnings

def show_image(image, title='Image', cmap='gray'):
    """
    Function to display an MRI image using Matplotlib.
    Args:
        image (SimpleITK.Image): The image to display.
        title (str): Title of the plot.
        cmap (str): Color map to use for the image display.
    """
    # Convert the SimpleITK image to a numpy array for visualization
    image_array = sitk.GetArrayFromImage(image)
    
    # Display the image (assumes 3D or 2D image)
    plt.figure(figsize=(6, 6))
    # plt.imshow(image_array[image_array.shape[0] // 2], cmap=cmap)  # Show the middle slice of the 3D image
    plt.title(title)
    plt.axis('off')
    plt.show()

# SANITY CHECK - histogram plot
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

#TODO bilinear interpolation, wiener filter 
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
        print("[WienerDenoising]: Applying Wiener filter with kernel size", self.kernel_size)
        
        # Convert SimpleITK image to numpy array
        image_array = sitk.GetArrayFromImage(image)
        
        # Apply Wiener filter
        denoised_array = wiener(image_array, mysize=self.kernel_size)
        
        # Convert denoised numpy array back to SimpleITK image
        denoised_image = sitk.GetImageFromArray(denoised_array)
        denoised_image.CopyInformation(image)  # Preserve image metadata
        
        return denoised_image

class NNResampling(pymia_fltr.Filter):
    """Represents various resampling methods for MRI image preprocessing."""

    def __init__(self):
        """Initializes a new instance of the Resampling class."""
        pass

    def execute(self, image: sitk.Image, params: pymia_fltr.FilterParams = None) -> sitk.Image: 

        new_spacing = (0.5, 0.5, 0.5)

        # print("[Resampling]: original space ", image.GetSpacing()," ---Upsampling---> ",new_spacing)


        if isinstance(image, sitk.Image):
            # obj is a SimpleITK Image
            pass
            # print("Object is of type sitk.Image")
        elif isinstance(image, list) and isinstance(image[0], sitk.Image):
            # obj is a list with one element
            image = image[0]
            # print("Object is a list with one element, now obj is:", image)
        else:
            print("Object is neither sitk.Image nor a list with one element")


        original_spacing = image.GetSpacing()
        original_size = image.GetSize()
        new_size = tuple(
            int(np.round(original_size[i] * original_spacing[i] / new_spacing[i]))
            for i in range(3)
        )

        # print("[Resampling]: new SIZE",new_size, " <---- old size ", original_size)
        
        original_spacing = image.GetSpacing()
        original_size = image.GetSize()

        # Compute new size to maintain the same physical dimensions
        new_size = [
            int(round(original_size[i] * (original_spacing[i] / new_spacing[i])))
            for i in range(3)
        ]

        # Set up the resampler
        resampler = sitk.ResampleImageFilter()
        resampler.SetInterpolator(sitk.sitkNearestNeighbor)  # Nearest neighbor interpolation
        resampler.SetOutputSpacing(new_spacing)             # Desired spacing
        resampler.SetSize(new_size)                         # Computed new size
        resampler.SetOutputDirection(image.GetDirection())  # Copy direction from input
        resampler.SetOutputOrigin(image.GetOrigin())        # Copy origin from input

        # Perform resampling
        resampled_image = resampler.Execute(image)
        return resampled_image

class BilinearResampling(pymia_fltr.Filter):
    """Represents various resampling methods for MRI image preprocessing."""

    def __init__(self):
        """Initializes a new instance of the Resampling class."""
        pass

    def execute(self, image: sitk.Image, params: pymia_fltr.FilterParams = None) -> sitk.Image: 

        new_spacing = (0.5, 0.5, 0.5)

        # print("[Resampling]: original space ", image.GetSpacing()," ---Upsampling---> ",new_spacing)

        if isinstance(image, sitk.Image):
            # obj is a SimpleITK Image
            pass
            # print("Object is of type sitk.Image")
        elif isinstance(image, list) and isinstance(image[0], sitk.Image):
            # obj is a list with one element
            image = image[0]
            # print("Object is a list with one element, now obj is:", image)
        else:
            print("Object is neither sitk.Image nor a list with one element")
        
        original_spacing = image.GetSpacing()
        original_size = image.GetSize()
        new_size = tuple(
            int(np.round(original_size[i] * original_spacing[i] / new_spacing[i]))
            for i in range(3)
        )

        resampler = sitk.ResampleImageFilter()
        resampler.SetSize(new_size)
        resampler.SetOutputSpacing(new_spacing)
        resampler.SetSize(new_size)
        resampler.SetTransform(sitk.Transform())
        resampler.SetInterpolator(sitk.sitkLinear)
        resampled_image = resampler.Execute(image)
        
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
        # plot_histogram(img_arr)

        if img_max > img_min:
            normalized_arr = (img_arr - img_min) / (img_max - img_min)
        else:
            warnings.warn("Image has no intensity range (max == min). Returning unprocessed image.")
            normalized_arr = img_arr    

        img_out = sitk.GetImageFromArray(normalized_arr)
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

        # todo: remove the skull from the image by using the brain mask

        skull_stripped_image = image
        try:
            if mask.GetSize() != image.GetSize():
                raise ValueError("The mask and image must have the same dimensions.")

            image = sitk.Cast(image, sitk.sitkUInt8)
            mask = sitk.Cast(mask, sitk.sitkUInt8)

            skull_stripped_image = sitk.Mask(image, mask)

        except Exception as e:
            print("[SkullStripping]: ",e)

        # show_image(skull_stripped_image, title='Image after skull stripping')
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

        return registered_image

    def __str__(self):
        """Gets a printable string representation.

        Returns:
            str: String representation.
        """
        return 'ImageRegistration:\n' \
            .format(self=self)

