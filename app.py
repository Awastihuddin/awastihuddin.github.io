from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="koperasi",
        buffered=True
    )
    cursor = db.cursor()
except Error as e:
    print("Database belum aktif...")
    exit()

# Halaman login & daftar keanggotaan
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nama = request.form.get('nama')
        password = request.form.get('password')

        if 'daftar' in request.form:
            return redirect(url_for('daftar_keanggotaan'))

        query = "SELECT id FROM anggota WHERE nama = %s AND password = %s"
        cursor.execute(query, (nama, password))
        user = cursor.fetchone()

        if user:
            user_id = user[0]
            return redirect(url_for('dashboard', user_id=user_id))
        else:
            flash("Nama atau password salah.")
            return redirect(url_for('login'))

    return render_template('login.html')

# Halaman daftar keanggotaan
@app.route('/daftar_keanggotaan', methods=['GET', 'POST'])
def daftar_keanggotaan():
    if request.method == 'POST':
        nama = request.form.get('nama')
        password = request.form.get('password')

        if not nama or not password:
            flash("Nama dan password harus diisi.")
            return redirect(url_for('daftar_keanggotaan'))

        try:
            query = "INSERT INTO anggota (nama, password, saldo, pinjaman) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nama, password, 15000000.0, 0.0))
            db.commit()
            flash("Pendaftaran berhasil! Silakan login.")
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f"Terjadi kesalahan: {err}")
            return redirect(url_for('daftar_keanggotaan'))

    return render_template('daftar.html')

# Halaman dashboard
@app.route("/dashboard/<int:user_id>")
def dashboard(user_id):
    query = "SELECT saldo, pinjaman FROM anggota WHERE id = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    if not user:
        return render_template("error.html", error="User tidak ditemukan.")

    saldo, pinjaman = user
    status = "Masih Meminjam" if pinjaman > 0 else "Tidak Meminjam"
    return render_template("dashboard.html", saldo=saldo, pinjaman=pinjaman, status=status, user_id=user_id)

# Halaman ambil pinjaman
@app.route("/ambil/<int:user_id>", methods=["GET", "POST"])
def ambil(user_id):
    if request.method == "POST":
        try:
            jumlah = float(request.form.get("jumlah"))
        except (ValueError, TypeError):
            flash("Masukkan jumlah pinjaman yang valid (tipe desimal).", "error")
            return redirect(url_for("ambil", user_id=user_id))

        bunga = 50000.0

        query = "SELECT saldo, pinjaman FROM anggota WHERE id = %s"
        cursor.execute(query, (user_id,))
        saldo, pinjaman = cursor.fetchone()

        if jumlah > saldo:
            flash("Saldo koperasi tidak mencukupi.", "error")
            return redirect(url_for("ambil", user_id=user_id))

        new_pinjaman = pinjaman + jumlah + bunga
        new_saldo = saldo - jumlah
        update_query = "UPDATE anggota SET saldo = %s, pinjaman = %s WHERE id = %s"
        cursor.execute(update_query, (new_saldo, new_pinjaman, user_id))
        db.commit()
        flash("Pinjaman berhasil diambil.", "success")
        return redirect(url_for("dashboard", user_id=user_id))

    return render_template("ambil.html", user_id=user_id)

# Halaman lunasi pinjaman
@app.route("/lunasi/<int:user_id>", methods=["GET", "POST"])
def lunasi(user_id):
    if request.method == "POST":
        try:
            jumlah = float(request.form.get("jumlah"))
        except (ValueError, TypeError):
            flash("Masukkan jumlah pembayaran yang valid (tipe desimal).", "error")
            return redirect(url_for("lunasi", user_id=user_id))

        query = "SELECT saldo, pinjaman FROM anggota WHERE id = %s"
        cursor.execute(query, (user_id,))
        saldo, pinjaman = cursor.fetchone()

        if jumlah < pinjaman:
            flash("Jumlah pembayaran kurang dari total pinjaman.", "error")
            return redirect(url_for("lunasi", user_id=user_id))

        if jumlah > saldo:
            flash("Saldo Anda tidak mencukupi.", "error")
            return redirect(url_for("lunasi", user_id=user_id))

        new_saldo = saldo - jumlah
        update_query = "UPDATE anggota SET saldo = %s, pinjaman = 0 WHERE id = %s"
        cursor.execute(update_query, (new_saldo, user_id))
        db.commit()
        flash("Pinjaman berhasil dilunasi.", "success")
        return redirect(url_for("dashboard", user_id=user_id))

    return render_template("lunasi.html", user_id=user_id)

# Halaman hapus akun
@app.route("/hapus_akun/<int:user_id>", methods=["POST"])
def hapus_akun(user_id):
    try:
        # Periksa apakah pengguna masih memiliki pinjaman
        query = "SELECT pinjaman FROM anggota WHERE id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result is None:
            flash("Akun tidak ditemukan.", "error")
            return redirect(url_for("dashboard", user_id=user_id))

        pinjaman = result[0]

        if pinjaman > 0:
            flash("Tidak dapat menghapus akun karena Anda masih memiliki pinjaman yang harus dilunasi.", "error")
            return redirect(url_for("dashboard", user_id=user_id))

        # Jika tidak ada pinjaman, hapus akun
        query = "DELETE FROM anggota WHERE id = %s"
        cursor.execute(query, (user_id,))
        db.commit()
        flash("Akun berhasil dihapus.", "success")
        return redirect(url_for("login"))

    except mysql.connector.Error as err:
        flash(f"Terjadi kesalahan: {err}", "error")
        return redirect(url_for("dashboard", user_id=user_id))

# Jalankan aplikasi
if __name__ == "__main__":
    app.run(debug=True)
