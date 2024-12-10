from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'fawwaz'
print("Koperasi Simpan Pinjam 'Fawwaz'")
print("XI TKJ 1/23")
print("\nDebug Info:")

# Menghubungkan Database MySql
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="koperasi",
        buffered=True 
    )
    cursor = db.cursor()
except Error as e: #Opsi yang ditampilkan jika database belum aktif
    print("Database belum aktif...")
    exit()

# Halaman login dan Halaman masuk
@app.route('/', methods=['GET', 'POST']) #Halaman login
def login():
    if request.method == 'POST': # Jika menggunakan metode POST maka akan melakukan login
        nama = request.form.get('nama') # Mengambil inputan nama
        password = request.form.get('password')# Mengambil inputan password

        if 'daftar' in request.form: # Jika tombol daftar diklik maka akan melakukan registrasi
            return redirect(url_for('daftar_keanggotaan')) # Membawa ke halaman daftar keanggotaan

        query = "SELECT id FROM anggota WHERE nama = %s AND password = %s" # Query untuk memilih id anggota
        cursor.execute(query, (nama, password)) # Menggunakan cursor untuk menjalankan query
        user = cursor.fetchone() # Mengambil hasil query

        if user:
            user_id = user[0] # Mengambil id anggota
            return redirect(url_for('dashboard', user_id=user_id)) # Membawa ke halaman dashboard
        else:
            #flash("Nama atau password salah.") # Membuat pesan error
            return redirect(url_for('login')) # Membawa ke halaman login

    return render_template('login.html') # Membawa ke halaman login

# Halaman daftar keanggotaan-------------------------------------------------------------------------------------------------------------------------
@app.route('/daftar_keanggotaan', methods=['GET', 'POST'])
def daftar_keanggotaan():
    if request.method == 'POST': # Jika menggunakan metode POST maka akan melakukan registrasi
        nama = request.form.get('nama') # Mengambil inputan nama
        password = request.form.get('password') # Mengambil inputan password

        if not nama or not password: # Jika inputan nama atau password kosong maka akan membuat pesan error
            #flash("Nama dan password harus diisi.") # Membuat pesan error
            return redirect(url_for('daftar_keanggotaan')) # Membawa ke halaman daftar keanggotaan

        try:
            query = "INSERT INTO anggota (nama, password, saldo, pinjaman) VALUES (%s, %s, %s, %s)" # Query untuk memasukkan data ke database
            cursor.execute(query, (nama, password, 15000000.0, 0.0)) # Menggunakan cursor untuk menjalankan query
            db.commit() # Menggunakan cursor untuk menjalankan query
            #flash("Pendaftaran berhasil! Silakan login.") # Membuat pesan sukses
            return redirect(url_for('login')) # Membawa ke halaman login
        except mysql.connector.Error as err: # Opsi yang ditampilkan jika terjadi kesalahan
            #flash(f"Terjadi kesalahan: {err}")
            return redirect(url_for('daftar_keanggotaan')) # Membawa ke halaman daftar keanggotaan

    return render_template('daftar.html') # Membawa ke halaman daftar keanggotaan

# Halaman dashboard----------------------------------------------------------------------------------------------------------------------------------
@app.route("/dashboard/<int:user_id>") 
def dashboard(user_id):
    query = "SELECT saldo, pinjaman FROM anggota WHERE id = %s" # Query untuk memilih saldo dan pinjaman
    cursor.execute(query, (user_id,)) # Menggunakan cursor untuk menjalankan query
    user = cursor.fetchone() # Mengambil hasil query

    if not user:
        return render_template("error.html", error="User tidak ditemukan.") # Membawa ke halaman error

    saldo, pinjaman = user # Mengambil saldo dan pinjaman
    status = "Masih Meminjam" if pinjaman > 0 else "Tidak Meminjam" # Mengatur status
    return render_template("dashboard.html", saldo=saldo, pinjaman=pinjaman, status=status, user_id=user_id) # Membawa ke halaman dashboard

# Halaman ambil pinjaman------------------------------------------------------------------------------------------------------------------------------
@app.route("/ambil/<int:user_id>", methods=["GET", "POST"]) # Membuat route untuk halaman ambil pinjaman
def ambil(user_id):
    if request.method == "POST":
        try:
            jumlah = float(request.form.get("jumlah")) # Mengambil inputan jumlah pinjaman
        except (ValueError, TypeError): # Jika inputan jumlah pinjaman tidak valid maka akan membuat pesan error
            #flash("Masukkan jumlah pinjaman yang valid (tipe desimal).", "error") # Membuat pesan error
            return redirect(url_for("ambil", user_id=user_id)) # Membawa ke halaman ambil pinjaman

        bunga = 50000.0 # Bunga pinjaman

        query = "SELECT saldo, pinjaman FROM anggota WHERE id = %s" # Query untuk memilih saldo dan pinjaman
        cursor.execute(query, (user_id,)) # Menggunakan cursor untuk menjalankan query
        saldo, pinjaman = cursor.fetchone() # Mengambil hasil query

        if jumlah > saldo: 
            #flash("Saldo koperasi tidak mencukupi.", "error") # Membuat pesan error
            return redirect(url_for("ambil", user_id=user_id)) # Membawa ke halaman ambil pinjaman

        baru_pinjaman = pinjaman + jumlah + bunga # Menghitung pinjaman baru
        baru_saldo = saldo - jumlah # Menghitung saldo baru
        update_query = "UPDATE anggota SET saldo = %s, pinjaman = %s WHERE id = %s" # Query untuk memperbarui saldo dan pinjaman
        cursor.execute(update_query, (baru_saldo, baru_pinjaman, user_id)) # Menggunakan cursor untuk menjalankan query
        db.commit() # Menggunakan cursor untuk menjalankan query
        #flash("Pinjaman berhasil diambil.", "success") # Membuat pesan sukses
        return redirect(url_for("dashboard", user_id=user_id)) # Membawa ke halaman dashboard

    return render_template("ambil.html", user_id=user_id) # Membawa ke halaman ambil pinjaman

# Halaman lunasi pinjaman----------------------------------------------------------------------------------------------------------------------------
@app.route("/lunasi/<int:user_id>", methods=["GET", "POST"]) # Membuat route untuk halaman lunasi pinjaman
def lunasi(user_id): 
    if request.method == "POST":
        try:
            jumlah = float(request.form.get("jumlah")) # Mengambil inputan jumlah lunasi
        except (ValueError, TypeError): # Jika inputan jumlah lunasi tidak valid maka akan membuat pesan error
            flash("Masukkan jumlah pembayaran yang valid (tipe desimal).", "error") 
            return redirect(url_for("lunasi", user_id=user_id)) # Membawa ke halaman lunasi pinjaman

        query = "SELECT saldo, pinjaman FROM anggota WHERE id = %s" # Query untuk memilih saldo dan pinjaman
        cursor.execute(query, (user_id,)) # Menggunakan cursor untuk menjalankan query
        saldo, pinjaman = cursor.fetchone() # Mengambil hasil query

        if jumlah < pinjaman: 
            #flash("Jumlah pembayaran kurang dari total pinjaman.", "error")
            return redirect(url_for("lunasi", user_id=user_id)) # Membawa ke halaman lunasi pinjaman

        if jumlah > saldo: 
            #flash("Saldo Anda tidak mencukupi.", "error")
            return redirect(url_for("lunasi", user_id=user_id)) # Membawa ke halaman lunasi pinjaman

        new_saldo = saldo - jumlah 
        update_query = "UPDATE anggota SET saldo = %s, pinjaman = 0 WHERE id = %s" # Query untuk memperbarui saldo dan pinjaman
        cursor.execute(update_query, (new_saldo, user_id)) # Menggunakan cursor untuk menjalankan query
        db.commit()
        #flash("Pinjaman berhasil dilunasi.", "success") # Membuat pesan sukses
        return redirect(url_for("dashboard", user_id=user_id)) # Membawa ke halaman dashboard

    return render_template("lunasi.html", user_id=user_id) # Membawa ke halaman lunasi pinjaman

# Halaman hapus akun-------------------------------------------------------------------------------------------------------------------------------
@app.route("/hapus_akun/<int:user_id>", methods=["POST"]) # Membuat route untuk halaman hapus akun
def hapus_akun(user_id):
    try:
        # Periksa apakah pengguna masih memiliki pinjaman
        query = "SELECT pinjaman FROM anggota WHERE id = %s" # Query untuk memilih pinjaman
        cursor.execute(query, (user_id,)) # Menggunakan cursor untuk menjalankan query
        hasil = cursor.fetchone() # Mengambil hasil query

        if hasil is None: 
            #flash("Akun tidak ditemukan.", "error") # Membuat pesan error
            return redirect(url_for("dashboard", user_id=user_id)) # Membawa ke halaman dashboard

        pinjaman = hasil[0] # Mengambil pinjaman dari hasil query

        if pinjaman > 0: 
            #flash("Tidak dapat menghapus akun karena Anda masih memiliki pinjaman yang harus dilunasi.", "error")
            return redirect(url_for("dashboard", user_id=user_id))

        # Jika tidak ada pinjaman, hapus akun
        query = "DELETE FROM anggota WHERE id = %s" # Query untuk menghapus akun
        cursor.execute(query, (user_id,)) # Menggunakan cursor untuk menjalankan query
        db.commit() # Mengkomit perubahan database
        #flash("Akun berhasil dihapus.", "success") # Membuat pesan sukses
        return redirect(url_for("login")) # Membawa ke halaman login

    except mysql.connector.Error as err:
        #flash(f"Terjadi kesalahan: {err}", "error")
        return redirect(url_for("dashboard", user_id=user_id))

# Jalankan aplikasi------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__": # Jika aplikasi dijalankan secara langsung
    app.run(debug=True) # Jalankan aplikasi dengan mode debug   
