# =====================================================================
# app.py  ->  "Otak" website (backend). Dijalankan dengan: python app.py
# Flask = framework Python untuk membuat website.
# =====================================================================
import json                      # untuk menyimpan data ke file .json
import os                        # untuk urusan folder / path file
import random                    # untuk memilih kenangan secara acak
from datetime import datetime    # untuk membaca jam & tanggal

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename   # membersihkan nama file upload

app = Flask(__name__)            # membuat aplikasi web
app.secret_key = os.environ.get("SECRET_KEY", "lokal saja")   # dipakai untuk session login

# ---------------------------------------------------------------------
# 1) VARIABEL & TIPE DATA  (syarat dosen)
# ---------------------------------------------------------------------
NAMA_ADMIN = os.environ.get("NAMA_user", "admin")             # str     (teks)
PASSWORD_ADMIN = os.environ.get("PASSWORD_user", "pasword lokal")        # str     -> GANTI sebelum dikumpulkan!
MAKS_UKURAN_MB = 8              # int     (bilangan bulat)
VERSI_WEB = 1.0                 # float   (bilangan desimal)
MODE_DEBUG = True               # bool    (True / False)
EKSTENSI_BOLEH = ("png", "jpg", "jpeg", "gif", "webp")   # tuple (isi tidak bisa diubah)
KATEGORI = ["Masa SMA", "Masa Kuliah", "Keluarga", "Lainnya"]   # list (array)

app.config["MAX_CONTENT_LENGTH"] = MAKS_UKURAN_MB * 1024 * 1024  # batas upload

# Lokasi folder & file
FOLDER_DASAR = os.path.dirname(os.path.abspath(__file__))
FOLDER_UPLOAD = os.path.join(FOLDER_DASAR, "static", "uploads")
FILE_DATA = os.path.join(FOLDER_DASAR, "data", "kenangan.json")
os.makedirs(FOLDER_UPLOAD, exist_ok=True)                       # buat folder bila belum ada
os.makedirs(os.path.dirname(FILE_DATA), exist_ok=True)

# ---------------------------------------------------------------------
# 2) DATA PORTOFOLIO  (dictionary = pasangan kunci:nilai, list = daftar)
#    >>> EDIT bagian ini dengan data dirimu <<<
# ---------------------------------------------------------------------
PROFIL = {
    "nama": "Satrya Iqbal H",
    "julukan": ["Mahasiswa Teknologi Rekayasa Otomasai", "Algoritma Pemrograman", "Pencerita Kenangan"],  # list
    "tentang": "Halo! Saya mahasiswa yang sedang belajar pemrograman Python. "
               "Saya membuat website ini untuk menyimpan perjalanan dan kenangan saya.",
    "email": "satryaiqbal22@gmail.com",
    "instagram": "@shi_qbal",
    "lokasi": "solo, Indonesia",
}

SKILL = [                                   # list berisi dictionary
    {"nama": "Python", "level": 60},
    {"nama": "HTML & CSS", "level": 55},
    {"nama": "Microsoft Office", "level": 80},
    {"nama": "Komunikasi", "level": 85},
]

PENDIDIKAN = [
    {"tahun": "2022 - 2025", "judul": "SMA Negreri 2 Sukoharjo", "ket": "IPA 1B."},
    {"tahun": "2025 - sekarang", "judul": "Diponegoro University", "ket": "D4 Teknologi Rekaya Otomasi."},
]

PROYEK = [
    {"judul": "Website Portofolio & Kenangan", "ket": "Kenangan yang indah harus diabadikan bukan dihapus."},
    {"judul": "Proyek Kedua", "ket": "Tulis deskripsi singkat proyekmu di sini."},
]

# ---------------------------------------------------------------------
# 3) FUNGSI  (def = membuat fungsi, return = mengembalikan hasil)
# ---------------------------------------------------------------------
def muat_kenangan():
    """Membaca semua kenangan dari file JSON, hasilnya sebuah LIST."""
    if not os.path.exists(FILE_DATA):          # IF: kalau file belum ada
        return []                              # kembalikan list kosong
    with open(FILE_DATA, "r", encoding="utf-8") as f:
        return json.load(f)


def simpan_kenangan(daftar):
    """Menyimpan list kenangan ke file JSON."""
    with open(FILE_DATA, "w", encoding="utf-8") as f:
        json.dump(daftar, f, ensure_ascii=False, indent=2)


def ucapan_waktu():
    """Ucapan sesuai jam (contoh penggunaan IF - ELIF - ELSE)."""
    jam = datetime.now().hour                  # int: 0 - 23
    if jam < 11:
        return "Selamat pagi"
    elif jam < 15:
        return "Selamat siang"
    elif jam < 18:
        return "Selamat sore"
    else:
        return "Selamat malam"


def foto_diizinkan(nama_file):
    """True kalau ekstensi file termasuk yang diperbolehkan."""
    if "." not in nama_file:
        return False
    ekstensi = nama_file.rsplit(".", 1)[1].lower()
    return ekstensi in EKSTENSI_BOLEH


def buat_id_baru(daftar):
    """Mencari nomor id yang belum dipakai (contoh LOOPING for & while)."""
    id_terpakai = []
    for kenangan in daftar:                    # FOR: ulangi untuk tiap kenangan
        id_terpakai.append(kenangan["id"])
    id_baru = 1
    while id_baru in id_terpakai:              # WHILE: ulangi selama id sudah dipakai
        id_baru += 1
    return id_baru


def simpan_foto(daftar_file):
    """Menyimpan banyak foto sekaligus, mengembalikan list nama file."""
    nama_tersimpan = []
    for file in daftar_file:                   # FOR: proses satu per satu foto
        if file and file.filename != "" and foto_diizinkan(file.filename):
            stempel = datetime.now().strftime("%Y%m%d%H%M%S%f")   # supaya nama unik
            nama_baru = stempel + "_" + secure_filename(file.filename)
            file.save(os.path.join(FOLDER_UPLOAD, nama_baru))
            nama_tersimpan.append(nama_baru)
    return nama_tersimpan


def hitung_statistik(daftar):
    """Menghitung jumlah kenangan, total foto, dan rata-rata foto."""
    total_foto = 0
    per_kategori = {}                          # dictionary kosong
    for k in KATEGORI:
        per_kategori[k] = 0
    for item in daftar:
        total_foto += len(item["foto"])
        per_kategori[item["kategori"]] = per_kategori.get(item["kategori"], 0) + 1
    if len(daftar) > 0:
        rata_rata = round(total_foto / len(daftar), 1)   # float
    else:
        rata_rata = 0.0
    return {"jumlah": len(daftar), "foto": total_foto,
            "rata": rata_rata, "kategori": per_kategori}


@app.context_processor
def data_global():
    """Data yang otomatis tersedia di SEMUA halaman HTML."""
    return {"profil": PROFIL, "versi": VERSI_WEB, "kategori_list": KATEGORI}

# ---------------------------------------------------------------------
# 4) ROUTE = alamat halaman. @app.route("/") artinya halaman utama.
# ---------------------------------------------------------------------
@app.route("/")
def beranda():
    daftar = muat_kenangan()
    acak = random.choice(daftar) if daftar else None     # kenangan acak (kalau ada)
    return render_template("beranda.html", ucapan=ucapan_waktu(),
                           stat=hitung_statistik(daftar), acak=acak)


@app.route("/portofolio")
def portofolio():
    return render_template("portofolio.html", skill=SKILL,
                           pendidikan=PENDIDIKAN, proyek=PROYEK)


@app.route("/kenangan")
def kenangan():
    daftar = muat_kenangan()
    pilihan = request.args.get("kategori", "Semua")      # ambil ?kategori=... dari URL
    if pilihan != "Semua":
        tersaring = []
        for item in daftar:
            if item["kategori"] == pilihan:
                tersaring.append(item)
        daftar = tersaring
    daftar.reverse()                                     # terbaru tampil di atas
    return render_template("kenangan.html", daftar=daftar, pilihan=pilihan)


@app.route("/kenangan/tambah", methods=["GET", "POST"])
def tambah_kenangan():
    if not session.get("login"):                         # hanya yang login boleh tambah
        flash("Silakan login dulu untuk menambah kenangan.")
        return redirect(url_for("login"))

    if request.method == "POST":                         # form dikirim
        judul = request.form.get("judul", "").strip()
        keterangan = request.form.get("keterangan", "").strip()
        if judul == "":
            flash("Judul tidak boleh kosong.")
            return render_template("tambah.html")

        daftar = muat_kenangan()
        daftar.append({
            "id": buat_id_baru(daftar),
            "judul": judul,
            "keterangan": keterangan,
            "kategori": request.form.get("kategori", "Masa SMA"),
            "tanggal": request.form.get("tanggal") or datetime.now().strftime("%Y-%m-%d"),
            "foto": simpan_foto(request.files.getlist("foto")),
        })
        simpan_kenangan(daftar)
        flash("Kenangan berhasil disimpan.")
        return redirect(url_for("kenangan"))

    return render_template("tambah.html")


@app.route("/kenangan/hapus/<int:id_kenangan>", methods=["POST"])
def hapus_kenangan(id_kenangan):
    if not session.get("login"):
        return redirect(url_for("login"))
    daftar = muat_kenangan()
    sisa = []
    for item in daftar:
        if item["id"] == id_kenangan:
            for nama_foto in item["foto"]:               # hapus juga file fotonya
                lokasi = os.path.join(FOLDER_UPLOAD, nama_foto)
                if os.path.exists(lokasi):
                    os.remove(lokasi)
        else:
            sisa.append(item)
    simpan_kenangan(sisa)
    flash("Kenangan dihapus.")
    return redirect(url_for("kenangan"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username", "").strip()
        sandi = request.form.get("password", "")
        if user == NAMA_ADMIN and sandi == PASSWORD_ADMIN:
            session["login"] = True                      # tandai sudah login
            flash("Berhasil masuk. Selamat datang kembali!")
            return redirect(url_for("beranda"))
        flash("Username atau password salah.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Kamu sudah keluar.")
    return redirect(url_for("beranda"))


# Baris ini berarti: jalankan server hanya jika file ini dieksekusi langsung
if __name__ == "__main__":
    app.run(debug=MODE_DEBUG)
