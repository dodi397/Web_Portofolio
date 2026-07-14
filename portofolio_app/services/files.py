def save_uploaded_image(file_storage, prefix: str) -> str | None:
    if not file_storage or not file_storage.filename:
        return None

    if not allowed_file(file_storage.filename):
        return None

    if not _cloudinary_ready():
        raise RuntimeError(
            "Cloudinary belum dikonfigurasi. "
            "Isi CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, dan CLOUDINARY_API_SECRET."
        )

    _configure_cloudinary()

    try:
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

        return result["secure_url"]

    except Exception as e:
        current_app.logger.exception(e)
        raise