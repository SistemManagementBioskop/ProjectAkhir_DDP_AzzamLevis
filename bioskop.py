#              SISTEM MANAGEMENT BIOSKOP
# Akun admin awal -> username: admin | password: admin123

import json
import os
import random
import time

import pwinput
from prettytable import PrettyTable

# ---------- PATH FILE JSON ----------
# FOLDER = folder tempat bioskop.py berada.
# Jadi file JSON selalu disimpan di folder yang sama dengan program,
# walaupun program dijalankan dari folder lain.
FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_USER = os.path.join(FOLDER, "data_user.json")
PATH_FILM = os.path.join(FOLDER, "data_film.json")
PATH_TRANSAKSI = os.path.join(FOLDER, "data_transaksi.json")

# ---------- DATA TETAP (TUPLE) ----------
GENRE = ("Aksi", "Drama", "Horor", "Komedi", "Animasi", "Romantis", "Sci-Fi")
MAKS_LOGIN = 3
MAKS_TIKET = 10
MIN_TOPUP = 10000
MAKS_TOPUP = 10000000


# =====================================================
# FUNGSI BANTUAN
# =====================================================
def bersihkan_layar():
    # cek sistem operasi: Windows = "nt", selain itu (Linux/Mac) pakai clear
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def tekan_enter():
    input("\nTekan Enter untuk lanjut...")


def rupiah(angka):
    teks = f"{angka:,}"          # 1000000 -> 1,000,000
    teks = teks.replace(",", ".")  # 1,000,000 -> 1.000.000
    return "Rp" + teks


def waktu_sekarang():
    return time.ctime()  # contoh: Mon Oct 19 14:30:05 2026


def tampil_judul(teks):
    print("=" * 50)
    print(teks.center(50))
    print("=" * 50)


def minta_angka(pertanyaan, minimum, maksimum):
    """Minta angka bulat sampai user mengisi dengan benar."""
    while True:
        print(pertanyaan, end="")
        try:
            angka = int(input())
        except ValueError:
            print("Input harus berupa angka bulat ya!")
            continue

        if angka < minimum:
            print("Angka terlalu kecil, minimal", minimum)
        elif angka > maksimum:
            print("Angka terlalu besar, maksimal", maksimum)
        else:
            return angka


def minta_ya_tidak(pertanyaan):
    """Return True kalau user jawab y, False kalau n."""
    while True:
        print(pertanyaan + " (y/n) : ", end="")
        jawaban = input().strip().lower()
        if jawaban == "y":
            return True
        elif jawaban == "n":
            return False
        else:
            print("Jawab dengan y atau n saja ya!")


def jam_valid(teks):
    """Cek format jam HH:MM, contoh 19:30"""
    if len(teks) != 5:
        return False
    if teks[2] != ":":
        return False
    jam = teks[0:2]
    menit = teks[3:5]
    if not jam.isdigit() or not menit.isdigit():
        return False
    if int(jam) > 23 or int(menit) > 59:
        return False
    return True


def minta_jam(pertanyaan):
    while True:
        print(pertanyaan, end="")
        jam = input().strip()
        if jam_valid(jam):
            return jam
        print("Format jam salah. Contoh yang benar: 19:30")


def pilih_genre():
    nomor = 1
    for g in GENRE:
        print(f"  {nomor}. {g}")
        nomor += 1
    pilihan = minta_angka("Pilih genre (nomor) : ", 1, len(GENRE))
    return GENRE[pilihan - 1]


# =====================================================
# BACA & SIMPAN FILE JSON
# =====================================================
def simpan_data(path, data):
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except OSError:
        print("Gagal menyimpan ke file", os.path.basename(path))


def baca_data(path, data_awal):
    """Baca file JSON. Kalau file belum ada / rusak, pakai data awal."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        # file belum ada, buat baru berisi data awal
        simpan_data(path, data_awal)
        return data_awal
    except ValueError:
        # isi file rusak (bukan JSON yang benar)
        print("File", os.path.basename(path), "rusak, dipakai data awal.")
        simpan_data(path, data_awal)
        return data_awal


def data_awal_user():
    return {
        "admin": {"password": "admin123", "role": "admin", "saldo": 0}
    }


def data_awal_film():
    return [
        {"id": 1, "judul": "Galaksi Terakhir", "genre": "Sci-Fi",
        "durasi": 130, "jam": "19:00", "harga": 50000, "stok": 40},
        {"id": 2, "judul": "Dapur Mama", "genre": "Drama",
        "durasi": 105, "jam": "16:30", "harga": 40000, "stok": 35},
        {"id": 3, "judul": "Rumah di Ujung Jalan", "genre": "Horor",
        "durasi": 98, "jam": "21:00", "harga": 45000, "stok": 30},
        {"id": 4, "judul": "Petualangan Si Kancil", "genre": "Animasi",
        "durasi": 90, "jam": "13:00", "harga": 35000, "stok": 50},
        {"id": 5, "judul": "Kejar Sampai Jakarta", "genre": "Aksi",
        "durasi": 120, "jam": "20:15", "harga": 50000, "stok": 45},
    ]


# =====================================================
# REGISTRASI & LOGIN
# =====================================================
def username_sudah_ada(users, username):
    for nama in users:
        if nama.lower() == username.lower():
            return True
    return False


def cek_username(username):
    """Return pesan error. Kalau username benar, return teks kosong."""
    if len(username) < 5:
        return "Username minimal 5 karakter."
    if not username.replace("_", "").isalnum():
        return "Username hanya boleh huruf, angka, dan underscore (_)."
    return ""


def cek_password(password):
    """Return pesan error. Kalau password benar, return teks kosong."""
    if len(password) < 6:
        return "Password minimal 6 karakter."
    if " " in password:
        return "Password tidak boleh ada spasi."
    return ""


def registrasi(users):
    bersihkan_layar()
    tampil_judul("REGISTRASI")
    print("(ketik 0 di username untuk batal)\n")

    while True:
        username = input("Username : ").strip()
        if username == "0":
            return
        pesan = cek_username(username)
        if pesan != "":
            print(pesan)
        elif username_sudah_ada(users, username):
            print("Username sudah dipakai, coba yang lain.")
        else:
            break

    while True:
        password = pwinput.pwinput(prompt="Password : ", mask="*")
        pesan = cek_password(password)
        if pesan != "":
            print(pesan)
            continue
        ulang = pwinput.pwinput(prompt="Ulangi password : ", mask="*")
        if ulang != password:
            print("Password tidak sama, ulangi lagi.")
        else:
            break

    users[username] = {"password": password, "role": "user", "saldo": 0}
    simpan_data(PATH_USER, users)
    print("\nRegistrasi berhasil! Silakan login.")
    tekan_enter()


def login(users):
    """Return username kalau berhasil, return None kalau gagal 3x."""
    bersihkan_layar()
    tampil_judul("LOGIN")

    percobaan = 0
    while percobaan < MAKS_LOGIN:
        username = input("Username : ").strip()
        password = pwinput.pwinput(prompt="Password : ", mask="*")

        if username in users and users[username]["password"] == password:
            print("\nLogin berhasil, selamat datang", username)
            time.sleep(1)
            return username

        percobaan += 1
        sisa = MAKS_LOGIN - percobaan
        if sisa > 0:
            print("Username atau password salah. Sisa percobaan:", sisa, "\n")

    print("Gagal login 3 kali. Kembali ke menu utama.")
    time.sleep(2)
    return None


# =====================================================
# FILM (CRUD)
# =====================================================
def cari_film(films, id_film):
    for film in films:
        if film["id"] == id_film:
            return film
    return None


def buat_id_film(films):
    id_terbesar = 0
    for film in films:
        if film["id"] > id_terbesar:
            id_terbesar = film["id"]
    return id_terbesar + 1


def tampil_film(films):
    if len(films) == 0:
        print("Belum ada film yang tayang.")
        return

    tabel = PrettyTable()
    tabel.field_names = ["ID", "Judul", "Genre", "Durasi", "Jam", "Harga", "Kursi"]
    tabel.align["Judul"] = "l"
    for film in films:
        tabel.add_row([
            film["id"],
            film["judul"],
            film["genre"],
            str(film["durasi"]) + " mnt",
            film["jam"],
            rupiah(film["harga"]),
            film["stok"],
        ])
    print(tabel)


def tambah_film(films):
    bersihkan_layar()
    tampil_judul("TAMBAH FILM")

    # judul tidak boleh kosong dan tidak boleh sama dengan film lain
    while True:
        judul = input("Judul film : ").strip()
        kembar = False
        for film in films:
            if film["judul"].lower() == judul.lower():
                kembar = True
        if judul == "":
            print("Judul tidak boleh kosong.")
        elif kembar:
            print("Film dengan judul itu sudah ada.")
        else:
            break

    genre = pilih_genre()
    durasi = minta_angka("Durasi (menit) : ", 1, 500)
    jam = minta_jam("Jam tayang (HH:MM) : ")
    harga = minta_angka("Harga tiket : ", 1000, 1000000)
    stok = minta_angka("Jumlah kursi : ", 0, 1000)

    film_baru = {
        "id": buat_id_film(films),
        "judul": judul,
        "genre": genre,
        "durasi": durasi,
        "jam": jam,
        "harga": harga,
        "stok": stok,
    }
    films.append(film_baru)
    simpan_data(PATH_FILM, films)
    print("\nFilm berhasil ditambahkan!")
    tekan_enter()


def ubah_angka(pertanyaan, nilai_lama, minimum):
    """Kosongkan (Enter) kalau gamau mengubah nilai."""
    while True:
        print(f"{pertanyaan} [{nilai_lama}] : ", end="")
        teks = input().strip()
        if teks == "":
            return nilai_lama
        try:
            angka = int(teks)
        except ValueError:
            print("Input harus berupa angka bulat ya!")
            continue
        if angka < minimum:
            print("Angka minimal", minimum)
        else:
            return angka


def ubah_film(films):
    bersihkan_layar()
    tampil_judul("UBAH FILM")
    tampil_film(films)
    if len(films) == 0:
        tekan_enter()
        return

    id_film = minta_angka("\nID film yang diubah (0 = batal) : ", 0, 100000)
    if id_film == 0:
        return
    film = cari_film(films, id_film)
    if film is None:
        print("ID film tidak ditemukan.")
        tekan_enter()
        return

    print("\n(Tekan Enter kalau tidak ingin mengubah)")

    judul_baru = input("Judul [" + film["judul"] + "] : ").strip()
    if judul_baru != "":
        film["judul"] = judul_baru

    if minta_ya_tidak("Ubah genre? (sekarang " + film["genre"] + ")"):
        film["genre"] = pilih_genre()

    film["durasi"] = ubah_angka("Durasi", film["durasi"], 1)

    while True:
        jam_baru = input("Jam tayang [" + film["jam"] + "] : ").strip()
        if jam_baru == "":
            break
        if jam_valid(jam_baru):
            film["jam"] = jam_baru
            break
        print("Format jam salah. Contoh yang benar: 19:30")

    film["harga"] = ubah_angka("Harga", film["harga"], 1000)
    film["stok"] = ubah_angka("Kursi", film["stok"], 0)

    simpan_data(PATH_FILM, films)
    print("\nFilm berhasil diubah!")
    tekan_enter()


def hapus_film(films):
    bersihkan_layar()
    tampil_judul("HAPUS FILM")
    tampil_film(films)
    if len(films) == 0:
        tekan_enter()
        return

    id_film = minta_angka("\nID film yang dihapus (0 = batal) : ", 0, 100000)
    if id_film == 0:
        return
    film = cari_film(films, id_film)
    if film is None:
        print("ID film tidak ditemukan.")
        tekan_enter()
        return

    if minta_ya_tidak("Yakin ingin menghapus film " + film["judul"] + "?"):
        films.remove(film)
        simpan_data(PATH_FILM, films)
        print("Film berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")
    tekan_enter()


def menu_kelola_film(films):
    while True:
        bersihkan_layar()
        tampil_judul("KELOLA FILM")
        tampil_film(films)
        print("\n1. Tambah film")
        print("2. Ubah film")
        print("3. Hapus film")
        print("0. Kembali")
        pilihan = input("Pilih menu : ").strip()

        if pilihan == "1":
            tambah_film(films)
        elif pilihan == "2":
            ubah_film(films)
        elif pilihan == "3":
            hapus_film(films)
        elif pilihan == "0":
            break
        else:
            print("Menu tidak ada.")
            time.sleep(1)


# =====================================================
# E-MONEY & TRANSAKSI
# =====================================================
def top_up(username, users):
    bersihkan_layar()
    tampil_judul("TOP UP SALDO")
    print("Saldo sekarang :", rupiah(users[username]["saldo"]))
    print("Minimal top up :", rupiah(MIN_TOPUP))
    print("Maksimal top up:", rupiah(MAKS_TOPUP))

    nominal = minta_angka("\nNominal top up (0 = batal) : ", 0, MAKS_TOPUP)
    if nominal == 0:
        return
    if nominal < MIN_TOPUP:
        print("Nominal kurang dari minimal top up.")
        tekan_enter()
        return

    users[username]["saldo"] += nominal
    simpan_data(PATH_USER, users)
    print("\nTop up berhasil! Saldo sekarang:", rupiah(users[username]["saldo"]))
    tekan_enter()


def buat_kode_transaksi(transaksi):
    """Bikin kode acak, contoh TRX483920. Dicek supaya tidak kembar."""
    while True:
        kode = "TRX" + str(random.randint(100000, 999999))
        sudah_ada = False
        for t in transaksi:
            if t["kode"] == kode:
                sudah_ada = True
        if not sudah_ada:
            return kode


def cetak_invoice(trx):
    print("\n" + "=" * 44)
    print("INVOICE BIOSKOP".center(44))
    print("=" * 44)
    print("Kode       :", trx["kode"])
    print("Waktu      :", trx["waktu"])
    print("Pembeli    :", trx["username"])
    print("-" * 44)
    print("Film       :", trx["film"])
    print("Jam tayang :", trx["jam"])
    print("Harga      :", rupiah(trx["harga"]), "x", trx["jumlah"], "tiket")
    print("-" * 44)
    print("TOTAL      :", rupiah(trx["total"]))
    print("=" * 44)
    print("Terima kasih, selamat menonton!".center(44))


def beli_tiket(username, users, films, transaksi):
    bersihkan_layar()
    tampil_judul("BELI TIKET")
    tampil_film(films)
    if len(films) == 0:
        tekan_enter()
        return

    print("\nSaldo kamu :", rupiah(users[username]["saldo"]))
    id_film = minta_angka("ID film yang dipilih (0 = batal) : ", 0, 100000)
    if id_film == 0:
        return
    film = cari_film(films, id_film)
    if film is None:
        print("ID film tidak ditemukan.")
        tekan_enter()
        return
    if film["stok"] <= 0:
        print("Maaf, kursi film ini sudah habis.")
        tekan_enter()
        return

    # batas tiket = sisa kursi, tapi maksimal 10 per transaksi
    batas = film["stok"]
    if batas > MAKS_TIKET:
        batas = MAKS_TIKET
    jumlah = minta_angka("Jumlah tiket (1-" + str(batas) + ") : ", 1, batas)

    total = film["harga"] * jumlah
    print("Total bayar :", rupiah(total))

    if users[username]["saldo"] < total:
        kurang = total - users[username]["saldo"]
        print("Saldo tidak cukup, kurang", rupiah(kurang), "- silakan top up dulu.")
        tekan_enter()
        return

    if not minta_ya_tidak("Lanjut bayar?"):
        print("Pembayaran dibatalkan.")
        tekan_enter()
        return

    # saldo dan stok dikurangi (sudah dicek di atas, jadi tidak akan minus)
    users[username]["saldo"] -= total
    film["stok"] -= jumlah

    trx = {
        "kode": buat_kode_transaksi(transaksi),
        "waktu": waktu_sekarang(),
        "username": username,
        "film": film["judul"],
        "jam": film["jam"],
        "harga": film["harga"],
        "jumlah": jumlah,
        "total": total,
    }
    transaksi.append(trx)

    simpan_data(PATH_USER, users)
    simpan_data(PATH_FILM, films)
    simpan_data(PATH_TRANSAKSI, transaksi)

    print("\nPembayaran berhasil!")
    cetak_invoice(trx)
    print("Sisa saldo :", rupiah(users[username]["saldo"]))
    tekan_enter()


# =====================================================
# RIWAYAT & LAPORAN
# =====================================================
def tampil_riwayat_user(transaksi, username):
    bersihkan_layar()
    tampil_judul("RIWAYAT TRANSAKSI SAYA")

    tabel = PrettyTable()
    tabel.field_names = ["Kode", "Waktu", "Film", "Tiket", "Total"]
    for t in transaksi:
        if t["username"] == username:
            tabel.add_row([t["kode"], t["waktu"], t["film"], t["jumlah"], rupiah(t["total"])])

    if len(tabel.rows) == 0:
        print("Kamu belum punya transaksi.")
    else:
        print(tabel)
    tekan_enter()


def tampil_riwayat_admin(transaksi):
    bersihkan_layar()
    tampil_judul("RIWAYAT SEMUA TRANSAKSI")

    if len(transaksi) == 0:
        print("Belum ada transaksi.")
        tekan_enter()
        return

    tabel = PrettyTable()
    tabel.field_names = ["Kode", "Waktu", "Pembeli", "Film", "Tiket", "Total"]
    for t in transaksi:
        tabel.add_row([t["kode"], t["waktu"], t["username"], t["film"],
                    t["jumlah"], rupiah(t["total"])])
    print(tabel)
    tekan_enter()


def hitung_laporan(transaksi):
    """Return total pendapatan, jumlah transaksi, dan dictionary tiket per film."""
    total_pendapatan = 0
    tiket_per_film = {}
    for t in transaksi:
        total_pendapatan += t["total"]
        nama = t["film"]
        if nama in tiket_per_film:
            tiket_per_film[nama] += t["jumlah"]
        else:
            tiket_per_film[nama] = t["jumlah"]
    return total_pendapatan, len(transaksi), tiket_per_film


def tampil_laporan(transaksi):
    bersihkan_layar()
    tampil_judul("LAPORAN RINGKAS")

    pendapatan, jumlah, tiket_per_film = hitung_laporan(transaksi)
    print("Total pendapatan :", rupiah(pendapatan))
    print("Jumlah transaksi :", jumlah)

    if len(tiket_per_film) == 0:
        print("Film terlaris    : -")
        tekan_enter()
        return

    # ubah dictionary jadi list [tiket, nama] lalu urutkan dari terbanyak
    daftar = []
    for nama in tiket_per_film:
        daftar.append([tiket_per_film[nama], nama])
    daftar.sort(reverse=True)

    print("Film terlaris    :", daftar[0][1], "(" + str(daftar[0][0]) + " tiket)\n")

    tabel = PrettyTable()
    tabel.field_names = ["No", "Film", "Tiket Terjual"]
    tabel.align["Film"] = "l"
    nomor = 1
    for item in daftar:
        tabel.add_row([nomor, item[1], item[0]])
        nomor += 1
    print(tabel)
    tekan_enter()


def tampil_semua_akun(users):
    bersihkan_layar()
    tampil_judul("DAFTAR AKUN")
    tabel = PrettyTable()
    tabel.field_names = ["Username", "Role", "Saldo"]
    for nama in users:
        tabel.add_row([nama, users[nama]["role"], rupiah(users[nama]["saldo"])])
    print(tabel)
    tekan_enter()


# =====================================================
# MENU ADMIN & USER
# =====================================================
def menu_admin(username, users, films, transaksi):
    while True:
        bersihkan_layar()
        tampil_judul("MENU ADMIN - " + username)
        print("1. Kelola film (tambah / ubah / hapus)")
        print("2. Riwayat semua transaksi")
        print("3. Laporan ringkas")
        print("4. Daftar akun")
        print("0. Logout")
        pilihan = input("Pilih menu : ").strip()

        if pilihan == "1":
            menu_kelola_film(films)
        elif pilihan == "2":
            tampil_riwayat_admin(transaksi)
        elif pilihan == "3":
            tampil_laporan(transaksi)
        elif pilihan == "4":
            tampil_semua_akun(users)
        elif pilihan == "0":
            break
        else:
            print("Menu tidak ada.")
            time.sleep(1)


def menu_user(username, users, films, transaksi):
    while True:
        bersihkan_layar()
        tampil_judul("MENU USER - " + username)
        print("Saldo kamu :", rupiah(users[username]["saldo"]), "\n")
        print("1. Lihat film tayang")
        print("2. Beli tiket")
        print("3. Top up saldo")
        print("4. Riwayat transaksi saya")
        print("0. Logout")
        pilihan = input("Pilih menu : ").strip()

        if pilihan == "1":
            bersihkan_layar()
            tampil_judul("FILM TAYANG")
            tampil_film(films)
            tekan_enter()
        elif pilihan == "2":
            beli_tiket(username, users, films, transaksi)
        elif pilihan == "3":
            top_up(username, users)
        elif pilihan == "4":
            tampil_riwayat_user(transaksi, username)
        elif pilihan == "0":
            break
        else:
            print("Menu tidak ada.")
            time.sleep(1)


# =====================================================
# PROGRAM UTAMA
# =====================================================
def main():
    # ambil data dari file JSON (kalau belum ada, otomatis dibuat)
    users = baca_data(PATH_USER, data_awal_user())
    films = baca_data(PATH_FILM, data_awal_film())
    transaksi = baca_data(PATH_TRANSAKSI, [])

    while True:
        bersihkan_layar()
        tampil_judul("SISTEM MANAGEMENT BIOSKOP")
        print("1. Login")
        print("2. Registrasi")
        print("0. Keluar")
        pilihan = input("Pilih menu : ").strip()

        if pilihan == "1":
            username = login(users)
            if username is not None:
                if users[username]["role"] == "admin":
                    menu_admin(username, users, films, transaksi)
                else:
                    menu_user(username, users, films, transaksi)
        elif pilihan == "2":
            registrasi(users)
        elif pilihan == "0":
            print("\nTerima kasih sudah memakai Sistem Management Bioskop!")
            break
        else:
            print("Menu tidak ada.")
            time.sleep(1)


try:
    main()
except (KeyboardInterrupt, EOFError):
    print("\n\nProgram dihentikan. Data sudah tersimpan otomatis.")