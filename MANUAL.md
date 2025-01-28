# Panduan Pengguna Schema Designer

## Daftar Isi
1. [Pendahuluan](#pendahuluan)
2. [Instalasi](#instalasi)
3. [Autentikasi](#autentikasi)
4. [Dasbor](#dasbor)
5. [Membuat Diagram Skema](#membuat-diagram-skema)
6. [Mengelola Tabel](#mengelola-tabel)
7. [Ekspor Diagram](#ekspor-diagram)
8. [Berbagi Diagram](#berbagi-diagram)
9. [Pemecahan Masalah](#pemecahan-masalah)

## Pendahuluan

Schema Designer adalah alat canggih untuk merancang dan memvisualisasikan skema basis data. Aplikasi ini memungkinkan Anda:
- Membuat diagram skema basis data secara visual
- Menambah, mengedit, dan menghapus tabel
- Mengekspor skema ke berbagai format
- Berkolaborasi dengan tim

## Instalasi

### Prasyarat
- Docker
- Docker Compose
- Node.js (v16+)
- Python (v3.9+)

### Langkah Instalasi
1. Kloning repositori:
   ```bash
   git clone https://github.com/idiarso/DrawDatabase.git
   cd DrawDatabase
   ```

2. Jalankan aplikasi dengan Docker:
   ```bash
   docker-compose up --build
   ```

3. Akses aplikasi di `http://localhost:3000`

## Autentikasi

### Registrasi
1. Buka halaman registrasi
2. Masukkan username, email, dan password
3. Klik tombol "Daftar"

### Login
1. Masukkan username dan password
2. Klik tombol "Masuk"

### Logout
- Klik tombol "Logout" di sudut kanan atas dasbor

## Dasbor

Setelah login, Anda akan melihat dasbor dengan:
- Daftar diagram yang sudah dibuat
- Tombol untuk membuat diagram baru
- Opsi untuk mengedit atau mengekspor diagram

### Membuat Diagram Baru
1. Klik tombol "Buat Diagram Baru"
2. Beri nama diagram
3. Mulai menambahkan tabel

## Membuat Diagram Skema

### Menambah Tabel
1. Klik tombol "Tambah Tabel"
2. Masukkan nama tabel
3. Tambahkan kolom:
   - Nama kolom
   - Tipe data
   - Pilih apakah primary key
   - Tentukan nullable/not null

### Mengatur Tata Letak
- Drag-and-drop tabel untuk mengatur posisi
- Gunakan zoom dan pan untuk navigasi

## Mengelola Tabel

### Menambah Kolom
1. Pilih tabel
2. Klik "Tambah Kolom"
3. Isi detail kolom

### Menghapus Kolom
1. Pilih kolom
2. Klik ikon hapus

### Mengubah Tipe Data
- Klik pada kolom
- Ubah tipe data di panel properti

## Ekspor Diagram

### Ekspor SQL
1. Pilih diagram di dasbor
2. Klik "Ekspor"
3. Pilih format SQL

### Ekspor JSON
1. Pilih diagram di dasbor
2. Klik "Ekspor"
3. Pilih format JSON

## Berbagi Diagram

### Mengatur Visibilitas
- Pilih "Publik" untuk berbagi
- Pilih "Privat" untuk akses terbatas

### Berbagi Tautan
1. Aktifkan berbagi publik
2. Salin tautan
3. Bagikan ke rekan tim

## Pemecahan Masalah

### Tidak Bisa Login
- Periksa username dan password
- Pastikan akun sudah terdaftar
- Cek koneksi internet

### Diagram Tidak Tersimpan
- Pastikan sudah login
- Periksa koneksi internet
- Coba refresh halaman

### Masalah Ekspor
- Pastikan diagram memiliki setidaknya satu tabel
- Periksa format yang dipilih
- Hubungi dukungan jika masalah berlanjut

## Dukungan

Untuk pertanyaan atau masalah:
- Email: support@schemadesigner.com
- GitHub Issues: https://github.com/idiarso/DrawDatabase/issues

## Lisensi

Dilisensikan di bawah Lisensi MIT. Lihat file LICENSE untuk detail lebih lanjut.
