from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile

from PIL import Image
import io
import os

from .api_ml import send_to_ml
from .settings import MEDIA_ROOT, MEDIA_URL

import hashlib


def upload(file: UploadedFile) -> str:
    """
    Upload an image, if it does not exist.
    """
    buffer = io.BytesIO()
    for chunk in file.chunks():
        buffer.write(chunk)
    
    result_id = hashlib.blake2s(buffer.getbuffer()).hexdigest()
    result_path = os.path.join(MEDIA_ROOT, result_id + '.png')

    if os.path.isfile(result_path):
        return result_id

    try:
        image = Image.open(buffer)
    except OSError:  # This is not an image
        raise

    with open(result_path, 'wb') as result_file:
        image.save(result_file, 'PNG')

    send_to_ml(result_path)

    return result_id


def result(id: str) -> dict or None:
    """
    Get the result of image processing, forming a dictionary that can be passed
    to page template.
    """

    source_path = os.path.join(MEDIA_ROOT, id + '.png')
    if not os.path.isfile(source_path):
        return None

    result_path = source_path + '.proc' + os.path.splitext(source_path)[1]

    return {
        'source': MEDIA_URL + os.path.basename(source_path),
        'result': MEDIA_URL + os.path.basename(result_path) \
            if os.path.isfile(result_path) \
            else '/static/img/await.jpg',
    }
