from __future__ import annotations

from flask import flash, redirect, render_template, request, url_for

from ..extensions import db
from ..models import Education, Message, Project, Skill
from ..services.seed import get_or_create_profile


def register_public_routes(app):
    @app.route('/')
    def index():
        profile = get_or_create_profile()
        featured_projects = Project.query.order_by(Project.created_at.desc()).limit(3).all()
        skills = Skill.query.filter_by(profile_id=profile.id).order_by(Skill.id.asc()).all()
        return render_template('index.html', profile=profile, skills=skills, featured_projects=featured_projects, dashboard_view=False, active_page='home')

    @app.route('/about')
    def about():
        profile = get_or_create_profile()
        skills = Skill.query.filter_by(profile_id=profile.id).order_by(Skill.id.asc()).all()
        educations = Education.query.filter_by(profile_id=profile.id).order_by(Education.id.asc()).all()
        stats = {'projects': Project.query.count(), 'skills': len(skills), 'messages': Message.query.count()}
        return render_template('about.html', profile=profile, skills=skills, educations=educations, stats=stats, dashboard_view=False, active_page='about')

    @app.route('/portfolio')
    def portfolio():
        projects = Project.query.order_by(Project.created_at.desc()).all()
        return render_template('portfolio.html', projects=projects, dashboard_view=False, active_page='portfolio')

    @app.route('/project/<int:project_id>')
    def project_detail(project_id: int):
        project = Project.query.get_or_404(project_id)
        related_projects = Project.query.filter(Project.id != project.id).order_by(Project.created_at.desc()).limit(3).all()
        return render_template('project_detail.html', project=project, related_projects=related_projects, dashboard_view=False, active_page='portfolio')

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        profile = get_or_create_profile()
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            message_text = request.form.get('message', '').strip()

            if not name or not email or not message_text:
                flash('Semua field kontak wajib diisi.', 'danger')
                return redirect(url_for('contact'))

            message = Message(name=name, email=email, message=message_text)
            db.session.add(message)
            db.session.commit()
            flash('Pesan berhasil dikirim. Terima kasih sudah menghubungi saya.', 'success')
            return redirect(url_for('contact'))

        return render_template('contact.html', profile=profile, dashboard_view=False, active_page='contact')
