# Sistem Management Bioskop

## Nama Anggota Kelompok

| Nama | NIM |
|------|-----|
| Muhammad Indra Pratama | 2609116083 |
| Muhammad Raffy Putra Triadi | 2609116091 |
| Athallah Rafif | 2609116096 |
| Rakhmat Nur Alif Abdillah | 26091160100 |

---

## 1. Deskripsi Singkat Program

Ini program pengelolaan bioskop yang dijalankan lewat terminal, dibuat pakai Python. Ada dua role dengan hak akses yang beda:

- **Admin** ngurus data film dan mantau semua transaksi.
- **User** beli tiket pakai saldo e-money miliknya sendiri.

Akun admin sudah tersedia dari awal. User baru bisa daftar lewat menu registrasi, lalu otomatis dapat role user dengan saldo awal Rp0. Waktu login, pengguna punya **maksimal 3 kali percobaan** sebelum dikembalikan ke menu utama. Password yang diketik nggak kelihatan di layar (jadi bintang-bintang) karena pakai library `pwinput`.

**Akun bawaan:**

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |

**Aturan registrasi:**

- Username minimal 5 karakter dan hanya boleh huruf, angka, dan underscore.
- Password minimal 6 karakter tanpa spasi, dan harus diketik dua kali untuk konfirmasi.

### Fitur Admin

- **CRUD film**: tambah, lihat, ubah, dan hapus film.
- **Riwayat semua transaksi**.
- **Daftar akun** beserta saldonya.
- **Laporan ringkas**: total pendapatan, jumlah transaksi, dan film terlaris.

Setiap film menyimpan judul, genre, durasi, jam tayang, harga, dan jumlah kursi. Ada beberapa validasi: judul nggak boleh kembar, genre dipilih dari daftar yang sudah ditentukan, dan jam harus berformat `HH:MM`. Saat mengubah film, admin **cukup menekan Enter untuk bagian yang nggak ingin diganti**. Saat menghapus film, program minta konfirmasi dulu supaya nggak terhapus tanpa sengaja.

### Fitur User

- Lihat film yang tayang.
- Top up saldo (Rp10.000 sampai Rp10.000.000).
- Beli tiket (maksimal 10 tiket per transaksi).
- Riwayat transaksi pribadi.

Saat beli tiket, program ngecek stok kursi dan kecukupan saldo. Kalau saldo kurang, program nampilin kekurangannya dan minta user top up dulu. Kalau cukup dan user setuju, saldo dipotong, stok kursi dikurangi, kode transaksi acak dibuat (contoh `TRX929330`), lalu invoice dicetak. Semua input divalidasi supaya data tetap rapi dan program nggak error.

### Struktur Program dan Penyimpanan Data

File utamanya `bioskop.py`. Kodenya dipecah jadi fungsi-fungsi kecil untuk validasi input, login dan registrasi, CRUD film, transaksi, laporan, serta menu admin dan user, yang semuanya dijalankan dari fungsi `main()`.

Data disimpan otomatis di tiga file JSON, jadi nggak hilang walaupun program ditutup:

| File | Isi |
|------|-----|
| `data_user.json` | Data akun |
| `data_film.json` | Data film |
| `data_transaksi.json` | Data transaksi |

Kalau file JSON belum ada atau rusak, program otomatis membuatnya ulang dengan data awal.

**Library yang dibutuhkan:**

- `prettytable` untuk menampilkan tabel yang rapi.
- `pwinput` untuk menyembunyikan password.

```bash
pip install prettytable pwinput
```

Pastikan `bioskop.py` dijalankan lewat terminal.

---

## 2. Flowchart

### 2.1 Alur Utama (Menu Utama, Login, dan Registrasi)

<br>
<img width="1298" height="1376" alt="Flowchart bagian 1" src="https://github.com/user-attachments/assets/200dea5b-00a4-4811-9e3f-34ef0695ae91" />

**Penjelasan alur:**

Begitu program jalan, program menyambungkan diri ke file JSON yang berisi data user, film, dan transaksi. Setelah itu muncul menu utama dengan tiga pilihan: **1. Login**, **2. Registrasi**, dan **0. Keluar**. Pilihan dicek satu per satu. Kalau angkanya nggak cocok dengan ketiganya, muncul "menu tidak ada" lalu balik ke menu utama lewat konektor **A**.

**Login**

1. Pengguna mengisi username dan password.
2. Kalau salah, program ngecek apakah sudah salah tiga kali. Selama belum, pengguna diminta mengisi ulang.
3. Kalau sudah gagal tiga kali, muncul pesan "gagal login 3x" lalu balik ke menu utama (A).
4. Kalau benar, program ngecek role. Admin diarahkan ke konektor **B** (menu admin), selain itu ke konektor **C** (menu user).

**Registrasi**

1. Pengguna mengisi username. Program ngecek apakah username valid dan belum dipakai. Kalau nggak, muncul pesan error dan diminta mengisi ulang.
2. Kalau valid, pengguna mengisi password dan mengulanginya. Program ngecek apakah password valid dan keduanya sama. Kalau nggak, muncul pesan error dan diminta mengisi lagi.
3. Kalau sudah benar, akun baru disimpan ke file JSON, muncul "registrasi berhasil", lalu balik ke menu utama (A).

**Keluar**

Pilihan 0 adalah satu-satunya jalur menuju akhir program. Program menampilkan "terima kasih" lalu berhenti di end.

### 2.2 Menu Admin

<br>
<img width="1592" height="1337" alt="Flowchart bagian 2" src="https://github.com/user-attachments/assets/2e040db6-16f4-4f4a-b684-2b16e918443a" />

**Penjelasan alur:**

Di menu admin (konektor **B**), admin memasukkan pilihan 0 sampai 4:

- **1. Kelola film**: membuka submenu pengelolaan film.
  - **Tambah film**: isi judul, genre, durasi, jam, harga, dan jumlah kursi, lalu data ditambahkan ke JSON.
  - **Ubah film**: program menampilkan semua film, admin memasukkan ID film. Kalau ID ketemu, admin mengisi data baru (Enter berarti data nggak diubah) lalu disimpan ke JSON. Kalau nggak ketemu, muncul "ID film tidak ditemukan".
  - **Hapus film**: tampilkan semua film, input ID, lalu program menanyakan "yakin hapus? (y/n)". Jawaban `y` menghapus film dari JSON, `n` membatalkan.
  - Semua proses di submenu ini balik ke konektor **K** (submenu kelola film), kecuali pilihan 0 (Kembali) yang membawa admin ke menu admin (B).
- **2. Riwayat semua transaksi**: program ngecek data transaksi di JSON lalu menampilkannya.
- **3. Laporan ringkas**: program menghitung pendapatan, jumlah transaksi, dan film terlaris, lalu menampilkan hasilnya.
- **4. Daftar akun**: program ngecek data akun di JSON lalu menampilkannya.
- **0. Logout**: balik ke menu utama (A).

Pilihan 2, 3, dan 4 balik ke menu admin (B) setelah selesai. Pilihan di luar itu menghasilkan "menu tidak ada" lalu balik ke B.

### 2.3 Menu User

<br>
<img width="1600" height="830" alt="Flowchart bagian 3" src="https://github.com/user-attachments/assets/ef7ae3cb-1549-483a-929f-3f979d584213" />

**Penjelasan alur:**

Di menu user (konektor **C**), user memasukkan pilihan 0 sampai 4:

- **1. Lihat film tayang**: program ngecek data film di JSON lalu menampilkan semua film yang tayang.
- **2. Beli tiket**: ini alur paling panjang.
  1. Program menampilkan semua film beserta saldo user, lalu user memasukkan ID film.
  2. Kalau ID nggak ada atau kursi habis, muncul pesan tersebut lalu balik ke C.
  3. Kalau ID ada dan kursi tersedia, user memasukkan jumlah tiket dan program menghitung total bayar.
  4. Kalau saldo kurang dari total, muncul "saldo tidak cukup" lalu balik ke C.
  5. Kalau saldo cukup, program menanyakan "lanjut bayar? (y/n)". Jawaban `n` membatalkan dan balik ke C.
  6. Jawaban `y` membuat program mengurangi saldo dan kursi, menyimpan transaksi ke JSON, lalu menampilkan invoice dan sisa saldo sebelum balik ke C.
- **3. Top up saldo**: user memasukkan nominal. Kalau nominalnya minimal 10.000, saldo ditambah dan disimpan ke JSON, lalu muncul "top up berhasil". Kalau kurang, muncul "nominal kurang dari minimal". Keduanya balik ke C.
- **4. Riwayat transaksi saya**: program ngecek transaksi milik user di JSON lalu menampilkannya.
- **0. Logout**: balik ke menu utama (A).

Pilihan lain menghasilkan "menu tidak ada" lalu balik ke C.

---

## 3. Dokumentasi Program dan Output

### 3.1 Menu Awal dan Login

**Tampilan menu awal**

<br>
<img width="523" height="224" alt="Menu awal" src="https://github.com/user-attachments/assets/be82f0c4-5f2c-45ff-923c-95c82fe10999" />

**Tampilan menu login**

<br>
<img width="540" height="224" alt="Menu login" src="https://github.com/user-attachments/assets/2e3c526d-0b52-4a1e-a709-fecf022eb77b" />

**Login salah 3 kali**

Setelah tiga kali salah, pengguna dikembalikan ke menu utama.

<br>
<img width="696" height="381" alt="Login salah 3 kali" src="https://github.com/user-attachments/assets/8535790f-aa35-4dcc-b928-09e01b4b1488" />

### 3.2 Menu Admin

**Tampilan menu admin**

<br>
<img width="552" height="235" alt="Menu admin" src="https://github.com/user-attachments/assets/33567d38-d34f-4d25-832e-3631e6c9c135" />

**1. Kelola film**

Submenu untuk mengelola data film.

<br>
<img width="798" height="432" alt="Menu kelola film" src="https://github.com/user-attachments/assets/d01581fa-7b3c-475a-a29e-0f680ee29513" />

**Tambah film**

Admin mengisi judul, genre, durasi, jam tayang, harga, dan jumlah kursi.

<br>
<img width="566" height="148" alt="Tambah film" src="https://github.com/user-attachments/assets/383ea039-0438-47a3-a8a8-68f18392c628" />

**Ubah film**

Admin memilih ID film, lalu mengisi data baru. Tekan Enter kalau nggak mau mengubah bagian tertentu.

<br>
<img width="845" height="346" alt="Ubah film" src="https://github.com/user-attachments/assets/865553f5-4028-482e-80c0-04220b0b282d" />

**Hapus film**

Sebelum dihapus, program minta konfirmasi (y/n).

<br>
<img width="763" height="353" alt="Hapus film" src="https://github.com/user-attachments/assets/028a450b-515d-4e31-8fc1-03573f775a89" />

**2. Riwayat semua transaksi**

<br>
<img width="887" height="264" alt="Riwayat semua transaksi" src="https://github.com/user-attachments/assets/06799a22-80df-4507-b851-fc4cd0e395ff" />

**3. Laporan ringkas**

Menampilkan total pendapatan, jumlah transaksi, dan film terlaris.

<br>
<img width="544" height="355" alt="Laporan ringkas" src="https://github.com/user-attachments/assets/27d1f62d-3df2-49af-be47-f5887a57ac21" />

**4. Daftar akun**

<br>
<img width="533" height="267" alt="Daftar akun" src="https://github.com/user-attachments/assets/1453819f-47c4-4134-916d-4491135cc064" />

### 3.3 Menu User

**Tampilan menu user**

<br>
<img width="517" height="271" alt="Menu user" src="https://github.com/user-attachments/assets/e1c0fcff-c6ac-410a-a939-6d08c49b2108" />

**1. Lihat film tayang**

<br>
<img width="802" height="344" alt="Film tayang" src="https://github.com/user-attachments/assets/14c1216b-9fc0-4268-aeb5-ad2cfa530bd5" />

**2. Beli tiket**

<br>
<img width="798" height="380" alt="Beli tiket" src="https://github.com/user-attachments/assets/ae3b4b81-a10e-4f83-b26b-63e74f0d4aa3" />

**Beli tiket saat saldo nggak cukup**

Program nampilin kekurangan saldonya dan minta user top up dulu.

<br>
<img width="835" height="477" alt="Saldo tidak cukup" src="https://github.com/user-attachments/assets/87496704-20a3-4030-b61f-0dc1d23d0177" />

**3. Top up saldo**

<br>
<img width="595" height="315" alt="Top up saldo" src="https://github.com/user-attachments/assets/a209a319-48da-4aa0-8726-258311ea3d26" />

**Tampilan setelah berhasil membeli tiket**

Invoice dicetak beserta kode transaksi dan sisa saldo.

<br>
<img width="891" height="863" alt="Setelah membeli tiket" src="https://github.com/user-attachments/assets/90b30d12-5858-4a76-8a09-7fd225196279" />

**4. Riwayat transaksi saya**

<br>
<img width="875" height="310" alt="Riwayat transaksi user" src="https://github.com/user-attachments/assets/30f57b07-4878-4b2f-89e3-868f7aeb2074" />

### 3.4 Keluar

Program menampilkan ucapan terima kasih lalu berhenti.

<br>
<img width="875" height="310" alt="Menu keluar" src="https://github.com/user-attachments/assets/7c97acde-9930-4519-a564-4372bc53e4c5" />

---
