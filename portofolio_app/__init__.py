from __future__ import annotations

import os
from datetime import datetime

from flask import Flask, url_for

from .config import Config
from .extensions import db
from .models import Message, Profile
from .routes.dashboard import register_dashboard_routes
from .routes.public import register_public_routes
from .services.seed import init_database, seed_educations_if_empty


def create_app() -> Flask:
    template_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "templates")
    )
    static_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "static")
    )

    app = Flask(
        __name__,
        template_folder=template_folder,
        static_folder=static_folder,
    )

    app.config.from_object(Config)

    db.init_app(app)

    register_public_routes(app)
    register_dashboard_routes(app)

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

    @app.context_processor
    def inject_auth_state():
        from flask import session

        return {
            "admin_username": session.get("admin_username"),
            "is_admin_logged_in": session.get("admin_logged_in", False),
        }

    @app.errorhandler(413)
    def file_too_large(_error):
        from flask import flash, redirect, request, url_for

        flash("Ukuran file terlalu besar. Maksimal 5 MB.", "danger")
        return redirect(request.referrer or url_for("dashboard_projects"))

    with app.app_context():
        init_database()

    return app