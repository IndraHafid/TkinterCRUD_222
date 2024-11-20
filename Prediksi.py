# Import library yang dibutuhkan
import sqlite3  # Untuk pengelolaan database SQLite
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk  # Untuk GUI

# Membuat database dan tabel jika belum ada
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')  # Menghubungkan ke database SQLite
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID auto-increment
            nama_siswa TEXT,                       -- Nama siswa (teks)
            biologi INTEGER,                       -- Nilai Biologi
            fisika INTEGER,                        -- Nilai Fisika
            inggris INTEGER,                       -- Nilai Inggris
            prediksi_fakultas TEXT                 -- Prediksi Fakultas
        )
    ''')
    conn.commit()  # Menyimpan perubahan
    conn.close()   # Menutup koneksi

# Mengambil semua data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")  # Query untuk mengambil semua data
    rows = cursor.fetchall()  # Mengambil hasil query
    conn.close()
    return rows  # Mengembalikan data sebagai list

# Menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))  # Menyisipkan data
    conn.commit()
    conn.close()

# Memperbarui data di database berdasarkan ID
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))  # Update data berdasarkan ID
    conn.commit()
    conn.close()

# Menghapus data di database berdasarkan ID
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  # Hapus data
    conn.commit()
    conn.close()

# Menentukan prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"  # Biologi tertinggi
    elif fisika > biologi and fisika > inggris:
        return "Teknik"  # Fisika tertinggi
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"  # Inggris tertinggi
    else:
        return "Tidak Diketahui"  # Jika ada nilai yang sama

# Fungsi untuk men-submit data
def submit():
    try:
        nama = nama_var.get()  # Ambil input nama
        biologi = int(biologi_var.get())  # Ambil nilai Biologi
        fisika = int(fisika_var.get())  # Ambil nilai Fisika
        inggris = int(inggris_var.get())  # Ambil nilai Inggris

        if not nama:
            raise Exception("Nama siswa tidak boleh kosong.")  # Validasi nama

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Simpan ke database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()  # Bersihkan input
        populate_table()  # Perbarui tabel
    except ValueError:
        messagebox.showerror("Error", "Masukkan nilai yang valid!")

# Fungsi untuk memperbarui data
def update():
    try:
        record_id = selected_record_id.get()  # Ambil ID data yang dipilih
        if not record_id:
            raise Exception("Pilih data dari tabel untuk di-update!")  # Validasi ID

        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Prediksi fakultas
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)  # Update data

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()
        populate_table()
    except ValueError:
        messagebox.showerror("Error", "Masukkan nilai yang valid!")

# Fungsi untuk menghapus data
def delete():
    try:
        record_id = selected_record_id.get()
        if not record_id:
            raise Exception("Pilih data dari tabel untuk dihapus!")  # Validasi ID

        delete_database(record_id)  # Hapus data
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()
        populate_table()
    except ValueError:
        messagebox.showerror("Error", "Pilih data yang valid!")

# Fungsi untuk membersihkan input
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children():  # Hapus semua data di tabel
        tree.delete(row)
    for row in fetch_data():  # Tambahkan data dari database
        tree.insert('', 'end', values=row)

# Fungsi untuk mengisi input dari data yang dipilih di tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]  # Ambil item yang dipilih
        selected_row = tree.item(selected_item)['values']  # Ambil nilai dari item
        selected_record_id.set(selected_row[0])  # Isi ID
        nama_var.set(selected_row[1])  # Isi nama
        biologi_var.set(selected_row[2])  # Isi Biologi
        fisika_var.set(selected_row[3])  # Isi Fisika
        inggris_var.set(selected_row[4])  # Isi Inggris
    except IndexError:
        pass

# INISIALISASI DATABASE DAN GUI
create_database()  # Membuat database jika belum ada

# Inisialisasi GUI
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel untuk input
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()

# Label dan input untuk Nama Siswa
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

# Label dan input untuk Nilai Biologi
Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

# Label dan input untuk Nilai Fisika
Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

# Label dan input untuk Nilai Inggris
Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Tombol untuk Submit, Update, dan Delete
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Membuat tabel untuk menampilkan data siswa
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")

# Membuat widget Treeview untuk menampilkan data dalam bentuk tabel
tree = ttk.Treeview(root, columns=columns, show='headings')

# Menambahkan kolom dan mengatur judul kolom untuk tabel
for col in columns:
    tree.heading(col, text=col.capitalize())  # Menampilkan nama kolom
    tree.column(col, anchor='center')  # Mengatur agar kolom rata tengah

# Menempatkan tabel di GUI
tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Menghubungkan event klik pada baris tabel dengan fungsi untuk mengisi form input
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

# Memperbarui tabel dengan data yang sudah ada dalam database
populate_table()

# Menjalankan aplikasi GUI
root.mainloop()
