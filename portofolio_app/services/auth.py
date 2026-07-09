from __future__ import annotations

from functools import wraps

from flask import flash, redirect, request, session, url_for


def dashboard_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get('admin_logged_in'):
            session['next_url'] = request.path
            flash('Silakan login terlebih dahulu.', 'warning')
            return redirect(url_for('dashboard_login'))
        return view(*args, **kwargs)

    return wrapped_view
