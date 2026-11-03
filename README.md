## Nama Anggota Kelompok
- Muhammad Indra Pratama (2609116083)
- Muhammad Raffy Putra Triadi (2609116091)
- Athallah Rafif (2609116096)
- Rakhmat Nur Alif Abdillah (26091160100)

  
# Sistem Management Bioskop
Program ini adalah sistem pengelolaan bioskop berbasis terminal yang dibuat dengan Python. Ada dua peran akun, yaitu admin dan user. Admin mengelola data film dan memantau seluruh transaksi, sedangkan user membeli tiket memakai saldo e-money miliknya sendiri. Akun admin sudah tersedia dari awal (username `admin`, password `admin123`), sementara user baru bisa mendaftar lewat menu registrasi dan otomatis mendapat peran user dengan saldo awal Rp0. Username minimal 5 karakter dan hanya boleh berisi huruf, angka, dan underscore, sedangkan password minimal 6 karakter tanpa spasi dan harus diketik dua kali untuk konfirmasi. Saat login, pengguna punya **maksimal 3 kali percobaan** sebelum dikembalikan ke menu utama.<br>

Fitur admin meliputi **CRUD film (tambah, lihat, ubah, hapus), riwayat semua transaksi, daftar akun beserta saldonya, dan laporan ringkas berisi total pendapatan, jumlah transaksi, serta film terlaris.** Setiap film menyimpan judul, genre, durasi, jam tayang, harga, dan jumlah kursi, dengan validasi seperti judul tidak boleh kembar, genre dipilih dari daftar yang sudah ditentukan, dan jam harus berformat HH:MM. Saat mengubah film, admin **cukup menekan Enter untuk bagian yang tidak ingin diganti**, dan saat menghapus film, program meminta konfirmasi dulu supaya tidak terhapus tanpa sengaja.<br>

Fitur user meliputi melihat film yang tayang, top up saldo (Rp10.000 sampai Rp10.000.000), beli tiket, dan riwayat transaksi pribadi. Saat membeli tiket (maksimal 10 per transaksi), program mengecek stok kursi dan kecukupan saldo. Kalau saldo kurang, program menampilkan kekurangannya dan meminta user top up dulu. Kalau cukup dan user setuju, saldo dipotong, stok kursi dikurangi, kode transaksi acak dibuat (contoh `TRX929330`), lalu invoice dicetak. Semua input divalidasi supaya data tetap rapi dan program tidak error.<br>

File utamanya `bioskop.py`, dijalankan di terminal, dan butuh dua library luar: `prettytable` untuk menampilkan tabel yang rapi dan `pwinput` untuk menyembunyikan password jadi bintang-bintang. Kodenya dipecah jadi fungsi-fungsi kecil untuk validasi input, login dan registrasi, CRUD film, transaksi, laporan, serta menu admin dan user, yang semuanya dijalankan dari fungsi `main()`. Data akun, film, dan transaksi disimpan otomatis di tiga file JSON (`data_user.json`, `data_film.json`, `data_transaksi.json`), jadi tidak hilang walaupun program ditutup. Kalau file JSON belum ada atau rusak, program otomatis membuatnya ulang dengan data awal.<br>
ini adalah flowchartnya:<br>

<img width="1298" height="1376" alt="WhatsApp Image 2026-11-02 at 22 00 20" src="https://github.com/user-attachments/assets/200dea5b-00a4-4811-9e3f-34ef0695ae91" />
<img width="1592" height="1337" alt="WhatsApp Image 2026-11-02 at 22 00 21 (1)" src="https://github.com/user-attachments/assets/2e040db6-16f4-4f4a-b684-2b16e918443a" />
<img width="1600" height="830" alt="WhatsApp Image 2026-11-02 at 22 00 21" src="https://github.com/user-attachments/assets/ef7ae3cb-1549-483a-929f-3f979d584213" />

Alur dimulai dari start. Program lebih dulu menyambungkan diri ke file .json yang berisi data user, film, dan transaksi. Setelah itu program menampilkan menu utama dengan tiga pilihan: 1. Login, 2. Registrasi, dan 0. Keluar. Pengguna memasukkan pilihannya, lalu program mengecek satu per satu, mulai dari apakah pilihannya 1, kalau bukan lanjut ke 2, kalau bukan lagi lanjut ke 0. Jika angka yang dimasukkan tidak cocok dengan ketiganya, program menampilkan “menu tidak ada” dan kembali ke menu utama lewat konektor A.

Jika pengguna memilih Login, ia diminta mengisi username dan password. Program mengecek kebenarannya. Kalau salah, program menghitung apakah kesalahan sudah mencapai tiga kali. Selama belum tiga kali, pengguna kembali diminta mengisi username dan password. Begitu gagal tiga kali, program menampilkan pesan “gagal login 3x” lalu kembali ke menu utama (A). Kalau username dan password benar, program mengecek role. Role admin diarahkan ke konektor B (menu admin), sedangkan role selain admin diarahkan ke konektor C (menu user).

Jika pengguna memilih Registrasi, ia memasukkan username terlebih dahulu. Program mengecek apakah username valid dan belum dipakai. Kalau tidak, muncul pesan error username dan pengguna mengisi ulang. Kalau valid, pengguna lanjut memasukkan password dan ulangi password. Program mengecek apakah password valid dan keduanya sama. Kalau tidak, muncul pesan error password dan pengguna mengisi lagi. Kalau sudah benar, akun baru disimpan ke file .json, muncul pesan “registrasi berhasil”, dan program kembali ke menu utama (A).

Pilihan 0 (Keluar) adalah satu-satunya jalur menuju akhir program. Program menampilkan “terima kasih” lalu berhenti di end.

Pada menu admin (konektor B), admin memasukkan pilihan 0 sampai 4. Pilihan 1 (Kelola film) membuka submenu pengelolaan film. Di sana admin bisa menambah film dengan mengisi judul, genre, durasi, jam, harga, dan jumlah kursi, lalu data baru ditambahkan ke file .json. Admin juga bisa mengubah film. Program menampilkan seluruh film, admin memasukkan ID film yang ingin diubah, lalu jika ID ditemukan admin mengisi data baru (menekan Enter berarti data tidak diubah) dan perubahan disimpan ke .json. Jika ID tidak ditemukan, muncul pesan “ID film tidak ditemukan”. Untuk menghapus film, alurnya mirip: tampilkan seluruh film, input ID, lalu jika ditemukan program menanyakan “yakin hapus? (y/n)”. Jawaban y menghapus film dari .json, sedangkan n membatalkannya. Semua proses di submenu ini kembali ke konektor K, yaitu submenu kelola film, kecuali pilihan 0 (Kembali) yang membawa admin ke menu admin (B).

Pilihan 2 pada menu admin menampilkan riwayat semua transaksi. Program mengecek data transaksi di .json lalu menampilkannya. Pilihan 3 menampilkan laporan ringkas. Program menghitung pendapatan, jumlah transaksi, dan film terlaris, lalu menampilkan hasilnya. Pilihan 4 menampilkan daftar akun dengan cara mengecek data akun di .json. Ketiga pilihan ini kembali ke menu admin (B) setelah selesai. Pilihan 0 (Logout) membawa admin kembali ke menu utama (A), dan pilihan di luar itu menghasilkan pesan “menu tidak ada” lalu kembali ke B.

Pada menu user (konektor C), user juga memasukkan pilihan 0 sampai 4. Pilihan 1 (Lihat film tayang) mengecek data film di .json lalu menampilkan seluruh film yang tayang. Pilihan 2 (Beli tiket) adalah alur paling panjang. Program menampilkan seluruh film beserta saldo user, lalu user memasukkan ID film. Jika ID tidak ada atau kursi habis, program menampilkan pesan tersebut dan kembali ke C. Jika ID ada dan kursi tersedia, user memasukkan jumlah tiket dan program menghitung total bayar. Kalau saldo kurang dari total, muncul pesan “saldo tidak cukup” dan user kembali ke C. Kalau saldo cukup, program menanyakan “lanjut bayar? (y/n)”. Jawaban n membatalkan dan kembali ke C. Jawaban y membuat program mengurangi saldo dan kursi, menyimpan transaksi ke .json, lalu menampilkan invoice dan sisa saldo sebelum kembali ke C.

Pilihan 3 (Top up saldo) meminta user memasukkan nominal. Jika nominal sekurang-kurangnya 10.000, saldo ditambah dan disimpan ke .json, lalu muncul pesan “top up berhasil”. Jika kurang dari itu, muncul pesan “nominal kurang dari minimal”. Keduanya kembali ke C. Pilihan 4 (Riwayat transaksi saya) mengecek transaksi milik user di .json lalu menampilkannya. Pilihan 0 (Logout) membawa user kembali ke menu utama (A), dan pilihan lain menghasilkan “menu tidak ada” lalu kembali ke C.

#

### Ini Adalah Hasil Hasil Outputnya:
<img width="523" height="224" alt="image" src="https://github.com/user-attachments/assets/be82f0c4-5f2c-45ff-923c-95c82fe10999" /><br>
Menu Output Awal<br>
<img width="540" height="224" alt="image" src="https://github.com/user-attachments/assets/2e3c526d-0b52-4a1e-a709-fecf022eb77b" /><br>
Output menu login<br>
<img width="696" height="381" alt="image" src="https://github.com/user-attachments/assets/8535790f-aa35-4dcc-b928-09e01b4b1488" /><br>
Output menu login user jika salah 3x<br>
<img width="552" height="235" alt="image" src="https://github.com/user-attachments/assets/33567d38-d34f-4d25-832e-3631e6c9c135" /><br>
Output Menu Admin<br>
<img width="798" height="432" alt="image" src="https://github.com/user-attachments/assets/d01581fa-7b3c-475a-a29e-0f680ee29513" /><br>
Output Menu kelola film(admin)<br>
<img width="566" height="148" alt="image" src="https://github.com/user-attachments/assets/383ea039-0438-47a3-a8a8-68f18392c628" /><br>
Output menu tambah film(admin)<br>
<img width="845" height="346" alt="image" src="https://github.com/user-attachments/assets/865553f5-4028-482e-80c0-04220b0b282d" /><br>
Output menu ubah film(admin)<br>
<img width="763" height="353" alt="image" src="https://github.com/user-attachments/assets/028a450b-515d-4e31-8fc1-03573f775a89" /><br>
Output menu hapus film(admin)<br>
<img width="887" height="264" alt="image" src="https://github.com/user-attachments/assets/06799a22-80df-4507-b851-fc4cd0e395ff" /><br>
Output menu riwayat semua transaksi(admin)<br>
<img width="544" height="355" alt="image" src="https://github.com/user-attachments/assets/27d1f62d-3df2-49af-be47-f5887a57ac21" /><br>
Output menu laporan ringkas(admin)<br>
<img width="533" height="267" alt="image" src="https://github.com/user-attachments/assets/1453819f-47c4-4134-916d-4491135cc064" /><br>
Output menu daftar akun(admin)<br>
<img width="517" height="271" alt="image" src="https://github.com/user-attachments/assets/e1c0fcff-c6ac-410a-a939-6d08c49b2108" /><br>
Output menu User<br>
<img width="802" height="344" alt="image" src="https://github.com/user-attachments/assets/14c1216b-9fc0-4268-aeb5-ad2cfa530bd5" /><br>
output menu film tayang<br>
<img width="798" height="380" alt="image" src="https://github.com/user-attachments/assets/ae3b4b81-a10e-4f83-b26b-63e74f0d4aa3" /><br>
Output menu beli tiket<br>
<img width="835" height="477" alt="image" src="https://github.com/user-attachments/assets/87496704-20a3-4030-b61f-0dc1d23d0177" /><br>
Output menu beli tiket jika user tidak mempunyai saldo yang cukup<br>
<img width="595" height="315" alt="image" src="https://github.com/user-attachments/assets/a209a319-48da-4aa0-8726-258311ea3d26" /><br>
Output Top Up saldo<br>
<img width="891" height="863" alt="image" src="https://github.com/user-attachments/assets/90b30d12-5858-4a76-8a09-7fd225196279" /><br>
Output user setelah membeli ticket<br>
<img width="875" height="310" alt="image" src="https://github.com/user-attachments/assets/30f57b07-4878-4b2f-89e3-868f7aeb2074" /><br>
Output riwayat transaksi user<br>
<img width="875" height="310" alt="image" src="https://github.com/user-attachments/assets/7c97acde-9930-4519-a564-4372bc53e4c5" /><br>
Output memilih menu keluar<br>
