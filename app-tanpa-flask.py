import mysql.connector
from mysql.connector import Error
#from datetime import datetime

# Coba sambungkan ke database
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="koperasi",
        buffered=True  # Gunakan buffered cursor
    )
    cursor = db.cursor()
except Error as e:
    print("Database belum aktif...")
    exit()

# Fungsi untuk mendaftar keanggotaan
def daftar_keanggotaan():
    nama = input("Masukkan Nama: ")
    password = input("Masukkan Password: ")
    saldo_awal = 15000000.0  # Default saldo koperasi untuk anggota baru
    
    query = "INSERT INTO anggota (nama, password, saldo, pinjaman) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (nama, password, saldo_awal, 0.0))
    db.commit()
    print("Pendaftaran berhasil! Saldo awal koperasi Anda adalah Rp15.000.000,00.")

# Fungsi untuk menampilkan informasi koperasi
def tampilkan_informasi():
    cursor.execute("SELECT SUM(saldo) FROM anggota")
    total_saldo = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(pinjaman) FROM anggota")
    total_pinjaman = cursor.fetchone()[0]
    
    total_saldo = total_saldo if total_saldo else 0.0
    total_pinjaman = total_pinjaman if total_pinjaman else 0.0
    
    print("\n=== Informasi Koperasi ===")
    print(f"Saldo koperasi yang tersedia: {total_saldo:.2f}")
    print(f"Total pinjaman yang sudah dipinjam: {total_pinjaman:.2f}")
    print("=========================\n")

# Fungsi untuk masuk ke akun
def masuk():
    nama = input("Masukkan Nama: ")
    password = input("Masukkan Password: ")
    
    query = "SELECT * FROM anggota WHERE nama = %s AND password = %s"
    cursor.execute(query, (nama, password))
    user = cursor.fetchone()
    
    if user:
        print(f"Selamat datang, {nama}!")
        tampilkan_informasi()
        menu_user(user[0])
    else:
        print("Nama atau Password salah.")

# Menu untuk user yang sudah login
def menu_user(user_id):
    while True:
        print("\n1. Tarik Pinjaman\n2. Melunasi Pinjaman\n3. Hapus Pengguna\n4. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tarik_pinjaman(user_id)
        elif pilihan == "2":
            melunasi_pinjaman(user_id)
        elif pilihan == "3":
            hapus_pengguna(user_id)
        elif pilihan == "4":
            break
        else:
            print("Opsi tidak ditemukan.")

# Fungsi tarik pinjaman
def tarik_pinjaman(user_id):
    try:
        jumlah = float(input("Masukkan jumlah pinjaman: "))
    except ValueError:
        print("Input tidak valid. Harap masukkan angka.")
        return

    bunga = 50000.0  # Tambahan bunga Rp50.000 pada setiap pengambilan pinjaman
    
    cursor.execute("SELECT saldo, pinjaman FROM anggota WHERE id = %s", (user_id,))
    saldo, pinjaman = cursor.fetchone()
    
    if jumlah <= saldo:
        new_pinjaman = pinjaman + jumlah + bunga
        new_saldo = saldo - jumlah
        tanggal_pinjam = datetime.now().date()
        
        query = "UPDATE anggota SET saldo = %s, pinjaman = %s, tanggal_pinjam = %s WHERE id = %s"
        cursor.execute(query, (new_saldo, new_pinjaman, tanggal_pinjam, user_id))
        db.commit()
        print(f"Pinjaman berhasil dicairkan sebesar Rp{jumlah:.2f}.")
        print(f"Tambahan bunga sebesar Rp50.000 telah ditambahkan ke total pinjaman Anda.")
    else:
        print("Saldo koperasi tidak mencukupi untuk pinjaman ini.")

# Fungsi melunasi pinjaman
def melunasi_pinjaman(user_id):
    cursor.execute("SELECT pinjaman FROM anggota WHERE id = %s", (user_id,))
    pinjaman = cursor.fetchone()[0]
    
    if pinjaman > 0:
        try:
            jumlah = float(input(f"Jumlah yang harus dilunasi: {pinjaman:.2f}\nMasukkan jumlah pembayaran: "))
        except ValueError:
            print("Input tidak valid. Harap masukkan angka.")
            return
        
        if jumlah >= pinjaman:
            cursor.execute("SELECT saldo FROM anggota WHERE id = %s", (user_id,))
            saldo = cursor.fetchone()[0]
            
            if saldo >= jumlah:
                new_saldo = saldo - jumlah
                query = "UPDATE anggota SET saldo = %s, pinjaman = 0, tanggal_pinjam = NULL WHERE id = %s"
                cursor.execute(query, (new_saldo, user_id))
                db.commit()
                print("Pinjaman berhasil dilunasi.")
            else:
                print("Saldo tidak mencukupi untuk melunasi pinjaman.")
        else:
            print("Jumlah pembayaran kurang dari pinjaman.")
    else:
        print("Tidak ada pinjaman yang perlu dilunasi.")

# Fungsi hapus pengguna
def hapus_pengguna(user_id):
    cursor.execute("SELECT pinjaman FROM anggota WHERE id = %s", (user_id,))
    pinjaman = cursor.fetchone()[0]
    
    if pinjaman > 0:
        print("Anda masih memiliki tanggungan pinjaman. Lunasi pinjaman terlebih dahulu sebelum menghapus akun.")
        return

    konfirmasi = input("Apakah Anda yakin ingin menghapus akun ini? (y/n): ").lower()
    if konfirmasi == "y":
        query = "DELETE FROM anggota WHERE id = %s"
        cursor.execute(query, (user_id,))
        db.commit()
        print("Akun berhasil dihapus.")
    else:
        print("Penghapusan akun dibatalkan.")

# Menu utama
def menu():
    while True:
        print("\nKOPERASI SIMPAN PINJAM")
        print("1. Daftar Keanggotaan\n2. Masuk\n3. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            daftar_keanggotaan()
        elif pilihan == "2":
            masuk()
        elif pilihan == "3":
            print("Terima kasih telah menggunakan Koperasi Simpan Pinjam.")
            break
        else:
            print("Opsi tidak ditemukan.")

# Jalankan program
menu()

# Tutup koneksi
cursor.close()
db.close()
