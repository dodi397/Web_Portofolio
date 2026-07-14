from __future__ import annotations

import os
import uuid
from datetime import datetime

from flask import current_app
from werkzeug.utils import secure_filename


def ensure_upload_folder() -> None:
    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename: str) -> bool:
    if '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in current_app.config['ALLOWED_EXTENSIONS']


def save_uploaded_image(file_storage, prefix: str) -> str | None:
    if not file_storage or not file_storage.filename:
        return None

    if not allowed_file(file_storage.filename):
        return None

    ensure_upload_folder()
    original = secure_filename(file_storage.filename)
    extension = original.rsplit('.', 1)[1].lower()
    unique_name = f"{prefix}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:10]}.{extension}"
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
    file_storage.save(file_path)
    return unique_name


def delete_uploaded_image(filename: str | None) -> None:
    if not filename:
        return
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except OSError:
            pass
