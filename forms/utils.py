import os
import secrets
import string
import logging
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)

def save_request_file(request, field_name, storage_dir, random_length=15):
    """
    Save an uploaded file from request.FILES.
    Returns tuple (saved_path, filename, content_bytes)
    - saved_path: path returned by default_storage.save (or None on error)
    - filename: basename used for attachment (randomized)
    - content_bytes: file content bytes (or None)
    """
    if request is None:
        logger.debug("save_request_file: request is None")
        return None, None, None

    files = getattr(request, 'FILES', {}) or {}
    uploaded_file = files.get(field_name)

    if not uploaded_file:
        logger.debug("save_request_file: no uploaded file found for field_name=%s", field_name)
        return None, None, None

    # read bytes
    content = None
    try:
        try:
            uploaded_file.seek(0)
        except Exception:
            pass
        content = uploaded_file.read()
    except Exception:
        # fallback: read from path if FieldFile
        try:
            path = getattr(uploaded_file, 'path', None)
            if path:
                with open(path, 'rb') as f:
                    content = f.read()
        except Exception:
            logger.exception("save_request_file: failed to read uploaded file")

    if content is None:
        logger.warning("save_request_file: could not read content for uploaded file")
        return None, None, None

    # extension and random name
    _, ext = os.path.splitext(getattr(uploaded_file, 'name', '') or '')
    ext = ext.lower() if ext else ''
    alphabet = string.ascii_letters + string.digits
    rand_name = ''.join(secrets.choice(alphabet) for _ in range(random_length))
    filename = f"{rand_name}{ext}"
    storage_path = os.path.join(storage_dir, filename)

    # save to storage
    try:
        saved_path = default_storage.save(storage_path, ContentFile(content))
        logger.debug("save_request_file: saved_path=%s filename=%s size=%d", saved_path, filename)
        return saved_path, filename, content
    except Exception:
        logger.exception("save_request_file: failed to save file to storage %s", storage_path)
        return None, filename, content