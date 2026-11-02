# ProjectAkhir_DDP_AzzamLevis<br>

## Nama Anggota Kelompok ##
- Muhammad Indra Pratama (2609116083)
- Muhammad Raffy Putra Triadi (2609116091)
- Athallah Rafif (2609116096)
- Rakhmat Nur Alif Abdillah (26091160100)
  
**Sistem Management Bioskop**<br>
Program ini adalah sistem pengelolaan bioskop berbasis terminal yang dibuat dengan Python. Ada dua peran akun, yaitu admin dan user. Admin mengelola data film dan memantau seluruh transaksi, sedangkan user membeli tiket memakai saldo e-money miliknya sendiri. Akun admin sudah tersedia dari awal (username `admin`, password `admin123`), sementara user baru bisa mendaftar lewat menu registrasi dan otomatis mendapat peran user dengan saldo awal Rp0. Username minimal 5 karakter dan hanya boleh berisi huruf, angka, dan underscore, sedangkan password minimal 6 karakter tanpa spasi dan harus diketik dua kali untuk konfirmasi. Saat login, pengguna punya maksimal 3 kali percobaan sebelum dikembalikan ke menu utama.<br>
Fitur admin meliputi CRUD film (tambah, lihat, ubah, hapus), riwayat semua transaksi, daftar akun beserta saldonya, dan laporan ringkas berisi total pendapatan, jumlah transaksi, serta film terlaris. Setiap film menyimpan judul, genre, durasi, jam tayang, harga, dan jumlah kursi, dengan validasi seperti judul tidak boleh kembar, genre dipilih dari daftar yang sudah ditentukan, dan jam harus berformat HH:MM. Saat mengubah film, admin cukup menekan Enter untuk bagian yang tidak ingin diganti, dan saat menghapus film, program meminta konfirmasi dulu supaya tidak terhapus tanpa sengaja.<br>
Fitur user meliputi melihat film yang tayang, top up saldo (Rp10.000 sampai Rp10.000.000), beli tiket, dan riwayat transaksi pribadi. Saat membeli tiket (maksimal 10 per transaksi), program mengecek stok kursi dan kecukupan saldo. Kalau saldo kurang, program menampilkan kekurangannya dan meminta user top up dulu. Kalau cukup dan user setuju, saldo dipotong, stok kursi dikurangi, kode transaksi acak dibuat (contoh `TRX929330`), lalu invoice dicetak. Semua input divalidasi supaya data tetap rapi dan program tidak error.<br>
File utamanya `bioskop.py`, dijalankan di terminal, dan butuh dua library luar: `prettytable` untuk menampilkan tabel yang rapi dan `pwinput` untuk menyembunyikan password jadi bintang-bintang. Kodenya dipecah jadi fungsi-fungsi kecil untuk validasi input, login dan registrasi, CRUD film, transaksi, laporan, serta menu admin dan user, yang semuanya dijalankan dari fungsi `main()`. Data akun, film, dan transaksi disimpan otomatis di tiga file JSON (`data_user.json`, `data_film.json`, `data_transaksi.json`), jadi tidak hilang walaupun program ditutup. Kalau file JSON belum ada atau rusak, program otomatis membuatnya ulang dengan data awal.<br>
ini adalah flowchartnya:<br>
