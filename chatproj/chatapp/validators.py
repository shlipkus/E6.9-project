from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


def validate_size(width=None, height=None):
    def validator(image):
        width_i, height_i = get_image_dimensions(image)
        error = False
        if width is not None and width_i != width:
            error = True
        if height is not None and height_i != height:
            error = True
        if error:
            raise ValidationError(
                [f'Размер изображения должен быть {width} x {height} px.']
            )

    return validator