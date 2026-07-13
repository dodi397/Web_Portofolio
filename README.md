# Portofolio Flask

Web portofolio dinamis berbasis **Flask** dengan tampilan modern, responsif, dan dashboard admin untuk mengelola profil, proyek, skill, pendidikan, serta pesan masuk.

## Fitur Utama

### Halaman Publik
- Beranda dengan hero section dan profil utama
- Halaman About
- Halaman Portfolio untuk daftar proyek
- Halaman detail proyek
- Halaman Contact untuk mengirim pesan

### Dashboard Admin
- Login admin
- Ringkasan statistik dashboard
- Kelola proyek: tambah, edit, hapus
- Kelola profil: nama, headline, about, email, lokasi, foto profil, link GitHub, link LinkedIn
- Kelola skill: tambah dan hapus
- Kelola pendidikan: tambah, edit, hapus
- Kelola pesan masuk: lihat, tandai dibaca/belum dibaca, hapus

### Fitur Teknis
- Flask blueprint / routing modular
- SQLite database otomatis
- Upload gambar untuk profil dan proyek
- Validasi file gambar
- Tampilan responsif dengan Bootstrap 5
- Animasi dan komponen UI modern
- Session login untuk admin

## Teknologi yang Digunakan
- Python 3.13
- Flask 3.1
- SQLite
- Jinja2
- Bootstrap 5
- Bootstrap Icons
- HTML, CSS, JavaScript

## Struktur Folder

```bash
Web_Portofolio_Dinamis_dengan_Python_Flask/
├── app.py
├── requirements.txt
├── README.md
├── portofolio_app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   ├── routes/
│   │   ├── public.py
│   │   └── dashboard.py
│   └── services/
│       ├── auth.py
│       ├── files.py
│       └── seed.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── portfolio.html
│   ├── project_detail.html
│   ├── contact.html
│   └── dashboard/
│       ├── login.html
│       ├── index.html
│       ├── profile.html
│       ├── projects.html
│       ├── add_project.html
│       ├── edit_project.html
│       └── messages.html
└── static/
    ├── css/
    ├── js/
    ├── images/
    └── uploads/
```

## Instalasi

### 1. Ekstrak file ZIP
Ekstrak proyek ke folder kerja, lalu buka folder proyeknya.

### 2. Buat virtual environment
```bash
python -m venv .venv
```

### 3. Aktifkan virtual environment

**Windows**
```bash
.venv\Scripts\activate
```

**Mac / Linux**
```bash
source .venv/bin/activate
```

### 4. Install dependency
```bash
pip install -r requirements.txt
```

## Menjalankan Aplikasi

Jalankan perintah berikut:

```bash
python app.py
```

Setelah itu buka di browser:

```bash
http://127.0.0.1:5000
```

## Login Dashboard Admin

Gunakan akun bawaan berikut:

- **Username:** `admin`
- **Password:** `admin123`

## Konfigurasi Penting

Beberapa pengaturan bisa diubah lewat environment variable di `portofolio_app/config.py`, seperti:
- `SECRET_KEY`
- `DATABASE_URL`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`

## Upload Gambar

Aplikasi mendukung upload gambar dengan batas maksimum **5 MB** dan format:
- PNG
- JPG
- JPEG
- GIF
- WEBP

File upload disimpan di folder:

```bash
static/uploads/
```

## Database

Aplikasi menggunakan **SQLite** dan database akan dibuat otomatis saat aplikasi dijalankan pertama kali.

## Catatan Pengembangan

- Proyek ini memakai struktur modular agar mudah dikembangkan.
- Data profil dan pendidikan awal akan dibuat otomatis jika belum ada.
- Tampilan dashboard dan halaman publik menggunakan sistem template Jinja2.

## License
Proyek ini dibuat untuk pembelajaran dan pengembangan portofolio.
