from __future__ import annotations

from flask import flash, redirect, render_template, request, session, url_for

from ..extensions import db
from ..models import Education, Message, Project, Skill
from ..services.auth import dashboard_required
from ..services.files import delete_uploaded_image, save_uploaded_image
from ..services.seed import get_or_create_profile, normalize_technologies


def register_dashboard_routes(app):
    @app.route('/dashboard/login', methods=['GET', 'POST'])
    def dashboard_login():
        if session.get('admin_logged_in'):
            return redirect(url_for('dashboard_index'))

        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()

            if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
                session.permanent = True
                session['admin_logged_in'] = True
                session['admin_username'] = username
                flash('Login berhasil. Selamat datang di dashboard.', 'success')
                next_url = session.pop('next_url', None)
                return redirect(next_url or url_for('dashboard_index'))

            flash('Username atau password salah.', 'danger')

        return render_template('dashboard/login.html', dashboard_view=True)

    @app.route('/dashboard/logout')
    def dashboard_logout():
        session.clear()
        flash('Anda telah logout.', 'info')
        return redirect(url_for('index'))

    @app.route('/dashboard')
    @dashboard_required
    def dashboard_index():
        total_projects = Project.query.count()
        total_messages = Message.query.count()
        unread_total = Message.query.filter_by(is_read=False).count()
        total_skills = Skill.query.count()
        latest_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
        latest_messages = Message.query.order_by(Message.created_at.desc()).limit(5).all()
        profile = get_or_create_profile()

        return render_template('dashboard/index.html', total_projects=total_projects, total_messages=total_messages, unread_total=unread_total, total_skills=total_skills, latest_projects=latest_projects, latest_messages=latest_messages, profile=profile, dashboard_view=True, active_dashboard='overview')

    @app.route('/dashboard/projects')
    @dashboard_required
    def dashboard_projects():
        projects = Project.query.order_by(Project.created_at.desc()).all()
        return render_template('dashboard/projects.html', projects=projects, dashboard_view=True, active_dashboard='projects')

    @app.route('/dashboard/projects/add', methods=['GET', 'POST'])
    @dashboard_required
    def dashboard_add_project():
        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            technologies = normalize_technologies(request.form.get('technologies', ''))
            github_link = request.form.get('github_link', '').strip()
            live_link = request.form.get('live_link', '').strip()
            image_file = request.files.get('image_file')

            if not title or not description or not technologies:
                flash('Judul, deskripsi, dan teknologi wajib diisi.', 'danger')
                return redirect(url_for('dashboard_add_project'))

            filename = save_uploaded_image(image_file, 'project')
            if image_file and image_file.filename and not filename:
                flash('Format gambar tidak valid. Gunakan PNG, JPG, JPEG, GIF, atau WEBP.', 'danger')
                return redirect(url_for('dashboard_add_project'))

            project = Project(title=title, description=description, technologies=technologies, image_file=filename, github_link=github_link, live_link=live_link)
            db.session.add(project)
            db.session.commit()
            flash('Proyek berhasil ditambahkan.', 'success')
            return redirect(url_for('dashboard_projects'))

        return render_template('dashboard/add_project.html', project=None, dashboard_view=True, active_dashboard='projects')

    @app.route('/dashboard/projects/edit/<int:project_id>', methods=['GET', 'POST'])
    @dashboard_required
    def dashboard_edit_project(project_id: int):
        project = Project.query.get_or_404(project_id)

        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            technologies = normalize_technologies(request.form.get('technologies', ''))
            github_link = request.form.get('github_link', '').strip()
            live_link = request.form.get('live_link', '').strip()
            image_file = request.files.get('image_file')
            remove_image = request.form.get('remove_image') == 'on'

            if not title or not description or not technologies:
                flash('Judul, deskripsi, dan teknologi wajib diisi.', 'danger')
                return redirect(url_for('dashboard_edit_project', project_id=project.id))

            new_filename = None
            if image_file and image_file.filename:
                new_filename = save_uploaded_image(image_file, 'project')
                if not new_filename:
                    flash('Format gambar tidak valid. Gunakan PNG, JPG, JPEG, GIF, atau WEBP.', 'danger')
                    return redirect(url_for('dashboard_edit_project', project_id=project.id))
            elif remove_image:
                new_filename = ''

            old_filename = project.image_file
            project.title = title
            project.description = description
            project.technologies = technologies
            project.github_link = github_link
            project.live_link = live_link

            if new_filename is not None:
                project.image_file = new_filename or None

            db.session.commit()

            if new_filename is not None and old_filename and old_filename != new_filename:
                delete_uploaded_image(old_filename)

            flash('Proyek berhasil diperbarui.', 'success')
            return redirect(url_for('dashboard_projects'))

        return render_template('dashboard/edit_project.html', project=project, dashboard_view=True, active_dashboard='projects')

    @app.route('/dashboard/projects/delete/<int:project_id>', methods=['POST'])
    @dashboard_required
    def dashboard_delete_project(project_id: int):
        project = Project.query.get_or_404(project_id)
        old_filename = project.image_file
        db.session.delete(project)
        db.session.commit()
        delete_uploaded_image(old_filename)
        flash('Proyek berhasil dihapus.', 'info')
        return redirect(url_for('dashboard_projects'))

    @app.route('/dashboard/profile', methods=['GET', 'POST'])
    @dashboard_required
    def dashboard_profile():
        profile = get_or_create_profile()

        if request.method == 'POST':
            profile.full_name = request.form.get('full_name', '').strip() or profile.full_name
            profile.headline = request.form.get('headline', '').strip() or profile.headline
            profile.about = request.form.get('about', '').strip() or profile.about
            profile.email = request.form.get('email', '').strip() or profile.email
            profile.github_link = request.form.get('github_link', '').strip()
            profile.linkedin_link = request.form.get('linkedin_link', '').strip()
            profile.location = request.form.get('location', '').strip()

            photo_file = request.files.get('photo_file')
            if photo_file and photo_file.filename:
                new_photo = save_uploaded_image(photo_file, 'profile')
                if not new_photo:
                    flash('Format foto profil tidak valid.', 'danger')
                    return redirect(url_for('dashboard_profile'))
                old_photo = profile.photo_file
                profile.photo_file = new_photo
                db.session.commit()
                delete_uploaded_image(old_photo)
            else:
                db.session.commit()

            flash('Profil berhasil diperbarui.', 'success')
            return redirect(url_for('dashboard_profile'))

        skills = Skill.query.filter_by(profile_id=profile.id).order_by(Skill.id.asc()).all()
        educations = Education.query.filter_by(profile_id=profile.id).order_by(Education.id.asc()).all()
        return render_template('dashboard/profile.html', profile=profile, skills=skills, educations=educations, dashboard_view=True, active_dashboard='profile')

    @app.route('/dashboard/profile/skill/add', methods=['POST'])
    @dashboard_required
    def dashboard_add_skill():
        profile = get_or_create_profile()
        name = request.form.get('skill_name', '').strip()
        level_raw = request.form.get('skill_level', '80').strip()

        if not name:
            flash('Nama skill wajib diisi.', 'danger')
            return redirect(url_for('dashboard_profile'))

        try:
            level = max(0, min(100, int(level_raw)))
        except ValueError:
            level = 80

        db.session.add(Skill(profile_id=profile.id, name=name, level=level))
        db.session.commit()
        flash('Skill berhasil ditambahkan.', 'success')
        return redirect(url_for('dashboard_profile'))

    @app.route('/dashboard/profile/skill/delete/<int:skill_id>', methods=['POST'])
    @dashboard_required
    def dashboard_delete_skill(skill_id: int):
        skill = Skill.query.get_or_404(skill_id)
        db.session.delete(skill)
        db.session.commit()
        flash('Skill berhasil dihapus.', 'info')
        return redirect(url_for('dashboard_profile'))

    @app.route('/dashboard/profile/education/add', methods=['POST'])
    @dashboard_required
    def dashboard_add_education():
        profile = get_or_create_profile()
        title = request.form.get('education_title', '').strip()
        description = request.form.get('education_description', '').strip()

        if not title or not description:
            flash('Judul dan deskripsi pendidikan wajib diisi.', 'danger')
            return redirect(url_for('dashboard_profile'))

        db.session.add(Education(profile_id=profile.id, title=title, description=description))
        db.session.commit()
        flash('Pendidikan berhasil ditambahkan.', 'success')
        return redirect(url_for('dashboard_profile'))

    @app.route('/dashboard/profile/education/edit/<int:education_id>', methods=['POST'])
    @dashboard_required
    def dashboard_edit_education(education_id: int):
        education = Education.query.get_or_404(education_id)
        title = request.form.get('education_title', '').strip()
        description = request.form.get('education_description', '').strip()

        if not title or not description:
            flash('Judul dan deskripsi pendidikan wajib diisi.', 'danger')
            return redirect(url_for('dashboard_profile'))

        education.title = title
        education.description = description
        db.session.commit()
        flash('Pendidikan berhasil diperbarui.', 'success')
        return redirect(url_for('dashboard_profile'))

    @app.route('/dashboard/profile/education/delete/<int:education_id>', methods=['POST'])
    @dashboard_required
    def dashboard_delete_education(education_id: int):
        education = Education.query.get_or_404(education_id)
        db.session.delete(education)
        db.session.commit()
        flash('Pendidikan berhasil dihapus.', 'info')
        return redirect(url_for('dashboard_profile'))

    @app.route('/dashboard/messages')
    @dashboard_required
    def dashboard_messages():
        messages = Message.query.order_by(Message.created_at.desc()).all()
        return render_template('dashboard/messages.html', messages=messages, dashboard_view=True, active_dashboard='messages')

    @app.route('/dashboard/messages/toggle/<int:message_id>', methods=['POST'])
    @dashboard_required
    def dashboard_toggle_message(message_id: int):
        message = Message.query.get_or_404(message_id)
        message.is_read = not message.is_read
        db.session.commit()
        flash('Status pesan diperbarui.', 'success')
        return redirect(url_for('dashboard_messages'))

    @app.route('/dashboard/messages/delete/<int:message_id>', methods=['POST'])
    @dashboard_required
    def dashboard_delete_message(message_id: int):
        message = Message.query.get_or_404(message_id)
        db.session.delete(message)
        db.session.commit()
        flash('Pesan berhasil dihapus.', 'info')
        return redirect(url_for('dashboard_messages'))
