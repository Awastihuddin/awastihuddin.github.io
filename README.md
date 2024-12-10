# Koperasi Fawwaz

**Koperasi Fawwaz** adalah sebuah aplikasi berbasis web yang dirancang untuk mengelola keanggotaan koperasi, termasuk fitur pendaftaran, login, pengelolaan pinjaman, dan penghapusan akun. Program ini dibangun menggunakan **Flask** sebagai framework backend dan terhubung ke database **MySQL**.

---

## Fitur Utama

1. **Login Anggota**
   - Anggota dapat masuk dengan menggunakan nama dan password.
   - Validasi terhadap kredensial anggota dilakukan melalui database.

2. **Pendaftaran Anggota**
   - Anggota baru dapat mendaftar dengan mengisi nama dan password.
   - Setelah mendaftar, anggota akan memiliki saldo awal sebesar Rp 15.000.000.

3. **Dashboard Anggota**
   - Menampilkan informasi saldo dan status pinjaman anggota.
   - Status pinjaman menunjukkan apakah anggota memiliki pinjaman aktif.

4. **Pengambilan Pinjaman**
   - Anggota dapat mengambil pinjaman sesuai saldo koperasi dengan bunga tetap sebesar Rp 50.000.
   - Sistem akan mengurangi saldo koperasi sesuai dengan jumlah pinjaman yang diambil.

5. **Pelunasan Pinjaman**
   - Anggota dapat melunasi pinjaman mereka jika memiliki saldo yang cukup.
   - Setelah dilunasi, pinjaman anggota akan dihapus dari catatan.

6. **Penghapusan Akun**
   - Anggota dapat menghapus akun mereka jika tidak memiliki pinjaman yang aktif.

---

## Teknologi yang Digunakan

- **Python**: Bahasa pemrograman utama.
- **Flask**: Framework backend untuk pengelolaan rute dan logika aplikasi.
- **MySQL**: Database untuk menyimpan data anggota dan transaksi.
- **HTML**: Template untuk antarmuka pengguna.

---

## Struktur Program

- **Fungsi Login (`login`)**: Mengelola login anggota dan validasi akun.
- **Fungsi Pendaftaran (`daftar_keanggotaan`)**: Memungkinkan anggota baru mendaftar ke koperasi.
- **Fungsi Dashboard (`dashboard`)**: Menampilkan informasi keuangan anggota.
- **Fungsi Ambil Pinjaman (`ambil`)**: Mengelola pengajuan pinjaman anggota.
- **Fungsi Lunasi Pinjaman (`lunasi`)**: Mengelola pelunasan pinjaman anggota.
- **Fungsi Hapus Akun (`hapus_akun`)**: Menghapus akun anggota yang tidak memiliki pinjaman aktif.

---

## Cara Menjalankan Program

1. **Persiapan Database**:
   - Pastikan MySQL terinstal dan aktif di perangkat Anda.
   - Buat database dengan nama `koperasi`.
   - Buat tabel `anggota` dengan struktur berikut:
     ```sql
     CREATE TABLE anggota (
         id INT AUTO_INCREMENT PRIMARY KEY,
         nama VARCHAR(100),
         password VARCHAR(100),
         saldo FLOAT DEFAULT 0.0,
         pinjaman FLOAT DEFAULT 0.0
     );
     ```

2. **Menjalankan Aplikasi**:
   - Pastikan Anda memiliki Python dan pustaka Flask terinstal.
   - Jalankan aplikasi dengan perintah berikut:
     ```bash
     python nama_file_program.py
     ```
   - Akses aplikasi melalui browser di alamat `http://127.0.0.1:5000`.

---

## Catatan

- Pastikan database MySQL aktif sebelum menjalankan aplikasi.
- Program menggunakan mode debug (`debug=True`) untuk mempermudah pengembangan.
- Ganti nilai `app.secret_key` untuk meningkatkan keamanan aplikasi.

---

## Kontributor

- **Nama**: Fawwaz
- **Kelas**: XI TKJ 1/23
