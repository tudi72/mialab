"""The pre-processing module contains classes for image pre-processing.

Image pre-processing aims to improve the image quality (image intensities) for subsequent pipeline steps.
"""
import warnings

import pymia.filtering.filter as pymia_fltr
import matplotlib.pyplot as plt 
import SimpleITK as sitk

from datetime import datetime


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
    plt.imshow(image_array[image_array.shape[0] // 2], cmap=cmap)  # Show the middle slice of the 3D image
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

        print(f"Mean intensity: {img_mean:.2f}, Standard deviation: {img_std:.2f}")
        voxel_size = image.GetSpacing()  # Returns a tuple (x, y, z)
        print("Voxel size:", voxel_size,'\n')
        plot_histogram(img_arr)

        if img_max > img_min:
            normalized_arr = (img_arr - img_min) / (img_max - img_min)
        else:
            warnings.warn("Image has no intensity range (max == min). Returning unprocessed image.")
            normalized_arr = img_arr    

        img_out = sitk.GetImageFromArray(normalized_arr)
        img_out.CopyInformation(image)

        show_image(img_out, title='Image after normalization')
        
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

        show_image(skull_stripped_image, title='Image after skull stripping')
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

        registered_image = image
        try:
            registered_image = sitk.Resample(image, atlas, transform, sitk.sitkLinear, 0.0)
        except Exception as e:
            print("[ImageRegistration]: ",e)

        # note: if you are interested in registration, and want to test it, have a look at
        # pymia.filtering.registration.MultiModalRegistration. Think about the type of registration, i.e.
        # do you want to register to an atlas or inter-subject? Or just ask us, we can guide you ;-)

        show_image(registered_image, title='Image after registration')

        return registered_image

    def __str__(self):
        """Gets a printable string representation.

        Returns:
            str: String representation.
        """
        return 'ImageRegistration:\n' \
            .format(self=self)
