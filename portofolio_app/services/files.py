from __future__ import annotations

import os
import uuid
from urllib.parse import urlparse

import cloudinary
import cloudinary.uploader
from flask import current_app
from werkzeug.utils import secure_filename


def ensure_upload_folder() -> None:
    """
    Fungsi kompatibilitas untuk kode lama.
    Jika memakai Cloudinary, fungsi ini tidak melakukan apa pun.
    Jika UPLOAD_FOLDER masih dikonfigurasi, folder akan dibuat.
    """
    upload_folder = current_app.config.get("UPLOAD_FOLDER")

    if upload_folder:
        os.makedirs(upload_folder, exist_ok=True)


def _cloudinary_ready() -> bool:
    return all([
        current_app.config.get("CLOUDINARY_CLOUD_NAME"),
        current_app.config.get("CLOUDINARY_API_KEY"),
        current_app.config.get("CLOUDINARY_API_SECRET"),
    ])


def _configure_cloudinary() -> None:
    if _cloudinary_ready():
        cloudinary.config(
            cloud_name=current_app.config["CLOUDINARY_CLOUD_NAME"],
            api_key=current_app.config["CLOUDINARY_API_KEY"],
            api_secret=current_app.config["CLOUDINARY_API_SECRET"],
            secure=True,
        )


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def save_uploaded_image(file_storage, prefix: str) -> str | None:
    if not file_storage or not file_storage.filename:
        return None

    if not allowed_file(file_storage.filename):
        return None

    _configure_cloudinary()

    if not _cloudinary_ready():
        return None

    original = secure_filename(file_storage.filename)
    ext = original.rsplit(".", 1)[1].lower()

    public_id = f"{prefix}_{uuid.uuid4().hex[:12]}"

    result = cloudinary.uploader.upload(
        file_storage,
        folder="portofolio",
        public_id=public_id,
        overwrite=True,
        resource_type="image",
        format=ext,
    )

    return result.get("secure_url")


def delete_uploaded_image(image_value: str | None) -> None:
    if not image_value:
        return

    if "res.cloudinary.com" not in image_value:
        return

    _configure_cloudinary()

    if not _cloudinary_ready():
        return

    try:
        path = urlparse(image_value).path

        if "/upload/" not in path:
            return

        public_part = path.split("/upload/", 1)[1]

        if public_part.startswith("v") and "/" in public_part:
            public_part = public_part.split("/", 1)[1]

        public_id = os.path.splitext(public_part.lstrip("/"))[0]

        cloudinary.uploader.destroy(
            public_id,
            resource_type="image",
        )
    except Exception:
        pass