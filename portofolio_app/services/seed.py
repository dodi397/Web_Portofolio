from __future__ import annotations

from .files import ensure_upload_folder
from ..extensions import db
from ..models import Education, Profile, Project, Skill


def normalize_technologies(raw_text: str) -> str:
    items = [item.strip() for item in (raw_text or '').split(',') if item.strip()]
    return ', '.join(items)


def seed_educations_if_empty(profile: Profile) -> None:
    if Education.query.filter_by(profile_id=profile.id).count() > 0:
        return

    legacy_items = [
        (
            getattr(profile, 'education_title_1', '') or 'Pengantar Pemrograman',
            getattr(profile, 'education_desc_1', '') or 'Belajar Python, Flask, SQLite, Jinja2, routing, form handling, dan deployment dasar.',
        ),
        (
            getattr(profile, 'education_title_2', '') or 'Pengembangan Web',
            getattr(profile, 'education_desc_2', '') or 'Belajar UI modern, komponen responsif, dan struktur project yang rapi untuk presentasi akademik.',
        ),
    ]

    for title, description in legacy_items:
        db.session.add(Education(profile_id=profile.id, title=title, description=description))
    db.session.commit()


def get_or_create_profile() -> Profile:
    profile = Profile.query.first()
    if profile:
        seed_educations_if_empty(profile)
        return profile

    profile = Profile(
        full_name='Nama Mahasiswa',
        headline='Web Developer & Problem Solver',
        about=(
            'Saya membangun aplikasi web modern yang rapi, responsif, dan mudah dikembangkan. '
            'Saya menekankan desain antarmuka yang nyaman, logika backend yang stabil, '
            'dan pengalaman pengguna yang terasa premium.'
        ),
        email='email@example.com',
        github_link='https://github.com/',
        linkedin_link='https://linkedin.com/',
        location='Indonesia',
    )
    db.session.add(profile)
    db.session.commit()

    default_skills = [('HTML', 92), ('CSS', 88), ('JavaScript', 85), ('Python', 90), ('Flask', 87), ('SQLite', 80)]
    for skill_name, level in default_skills:
        db.session.add(Skill(profile_id=profile.id, name=skill_name, level=level))
    db.session.commit()

    seed_educations_if_empty(profile)
    return profile


def seed_projects_if_empty() -> None:
    if Project.query.count() > 0:
        return

    demo_projects = [
        {
            'title': 'Sistem Informasi Sekolah',
            'description': 'Aplikasi administrasi sekolah untuk data siswa, guru, kelas, dan laporan akademik dengan tampilan dashboard modern.',
            'technologies': 'Python, Flask, SQLite, Bootstrap',
            'github_link': 'https://github.com/',
            'live_link': 'https://example.com/',
        },
        {
            'title': 'E-Commerce Modern',
            'description': 'Website toko online dengan katalog produk, keranjang belanja, dan halaman checkout yang dirancang responsif.',
            'technologies': 'HTML, CSS, JavaScript, Flask',
            'github_link': 'https://github.com/',
            'live_link': 'https://example.com/',
        },
        {
            'title': 'Task Management App',
            'description': 'Aplikasi manajemen tugas berbasis web untuk memantau progress kerja tim secara cepat dan terstruktur.',
            'technologies': 'Flask, SQLite, Jinja2',
            'github_link': 'https://github.com/',
            'live_link': 'https://example.com/',
        },
        {
            'title': 'Dashboard Analytics',
            'description': 'Dashboard ringkas untuk menampilkan statistik proyek dan aktivitas secara visual dengan komponen modern.',
            'technologies': 'Python, Flask, CSS Grid, JavaScript',
            'github_link': 'https://github.com/',
            'live_link': 'https://example.com/',
        },
    ]

    for item in demo_projects:
        db.session.add(Project(**item))
    db.session.commit()


def init_database() -> None:
    ensure_upload_folder()
    db.create_all()
    get_or_create_profile()
    seed_projects_if_empty()
