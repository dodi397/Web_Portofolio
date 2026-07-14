@app.context_processor
def inject_globals():
    profile = Profile.query.first()

    if profile:
        seed_educations_if_empty(profile)

    unread_messages = (
        Message.query.filter_by(is_read=False).count()
        if Message.query.count() > 0
        else 0
    )

    def resolve_image_url(image_value):
        if not image_value:
            return None

        if image_value.startswith(("http://", "https://", "data:")):
            return image_value

        return url_for(
            "static",
            filename=f"uploads/{image_value}",
        )

    return {
        "profile": profile,
        "site_profile": profile,
        "unread_messages": unread_messages,
        "current_year": datetime.utcnow().year,
        "resolve_image_url": resolve_image_url,
    }