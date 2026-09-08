# Analitik Dropout Mahasiswa — Jaya Jaya Institut

Proyek ini menganalisis riwayat hasil studi mahasiswa, mengidentifikasi faktor dropout yang dapat ditindaklanjuti, membangun model *machine learning* tiga kelas yang telah divalidasi, menyediakan prototipe sistem peringatan dini berbasis Streamlit, serta menyertakan dashboard pemantauan Metabase yang persisten.

## Identitas submission

- Nama: Regina Maria Samantha George
- Email: reginageo22@gmail.com
- Username Dicoding: reregin

## Permasalahan bisnis

Jaya Jaya Institut menghadapi jumlah mahasiswa dropout yang tinggi. Institusi perlu mengidentifikasi sedini mungkin mahasiswa yang berpotensi tidak menyelesaikan studi agar dukungan akademik, administratif, dan finansial yang sesuai dapat diberikan. Proyek ini menggabungkan analisis deskriptif, dashboard pemantauan, dan model penyaringan yang mengutamakan *recall*. Besaran masalah dan pola pada data dibahas setelah tahap data understanding dan analisis dilakukan.

Skor yang dihasilkan merupakan pendukung keputusan untuk intervensi yang bermanfaat. Skor tidak boleh digunakan untuk pemberian sanksi, proses penerimaan, pembatasan akses pembayaran kuliah, penentuan kelayakan akademik, ataupun keputusan berdampak tinggi lainnya secara otomatis.

## Isi proyek

```text
submission/
├── .streamlit/config.toml
├── dashboard/student_dropout.db
├── data/
│   ├── data.csv
│   ├── student_prepared.csv
│   ├── modeling_students.csv
│   ├── enrolled_students_future_scoring.csv
│   ├── enrolled_student_predictions.csv
│   ├── dashboard_student_data.csv
│   └── berkas CSV ringkasan analisis
├── model/
│   ├── student_status_model.joblib
│   └── berkas evaluasi CSV/JSON
├── app.py
├── metabase.db.mv.db
├── notebook.ipynb
├── README.md
├── reregin-dashboard.png
└── requirements.txt
```

`reregin-dashboard.png` berisi tangkapan layar dashboard yang telah dibuat. Video bersifat opsional dan sengaja tidak disertakan dalam paket ini.

## Menjalankan ulang analisis

Gunakan Python 3.10 dan jalankan perintah berikut dari direktori `submission`:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
jupyter notebook notebook.ipynb
```

Notebook yang disertakan telah dijalankan dari awal hingga akhir. Isinya mendokumentasikan pemahaman bisnis, pemahaman data, persiapan data, analisis eksploratif, perbandingan model, kalibrasi, pemilihan ambang batas, evaluasi pada data *holdout* yang belum pernah digunakan, diagnostik subkelompok, ekspor artefak, kesimpulan, dan rekomendasi tindakan.

## Solusi machine learning

Solusi yang diimplementasikan adalah model klasifikasi biner terkalibrasi untuk memprediksi **Dropout (`1`) atau Graduate (`0`)** pada titik pemantauan semester pertama dengan 17 input operasional. Data training hanya mencakup 3.630 mahasiswa dengan outcome akhir: 1.421 Dropout dan 2.209 Graduate. Sebanyak 794 mahasiswa berstatus Enrolled dipisahkan sebelum pembagian data dan hanya digunakan untuk prediksi masa mendatang.

Validasi silang terstratifikasi lima lipatan memilih *class-weighted logistic regression* dengan membandingkan kandidat berbasis data pendaftaran dan semester pertama. Proses pemilihan model dan threshold tidak melihat data *holdout*.

Kinerja pada 20% data *holdout* yang belum pernah digunakan:

| Metrik | Hasil |
|---|---:|
| Akurasi pada threshold screening | 0,825 |
| Precision Dropout | 0,712 |
| Recall Dropout | 0,930 |
| F1 Dropout | 0,806 |
| Balanced accuracy | 0,844 |
| ROC-AUC | 0,949 |
| F2 penyaringan Dropout | 0,876 |

Ambang batas penyaringan (`0,217`) ditentukan hanya menggunakan prediksi *out-of-fold* dari data latih untuk mengutamakan *recall* dropout. Setiap peringatan tetap memerlukan peninjauan manusia. Atribut identitas yang dilindungi atau sensitif, latar belakang keluarga, indikator makroekonomi, dan hasil semester kedua tidak digunakan dalam fitur model yang diimplementasikan.

### Menjalankan prototipe Streamlit secara lokal

```bash
streamlit run app.py
```

Buka alamat lokal yang ditampilkan Streamlit, lengkapi 17 input, lalu pilih **Assess student status**. Aplikasi akan menampilkan probabilitas Dropout dan Graduate, keputusan penyaringan dropout, dan saran dukungan yang sesuai dengan konteks.

### Streamlit Community Cloud

URL prototipe: **https://student-dropout-analysis-dicoding.streamlit.app/**

Langkah deployment manual:

1. Buat sebuah repositori GitHub dan letakkan **isi** folder `submission` ini pada direktori utama repositori. Pertahankan posisi relatif `app.py`, `requirements.txt`, dan folder `model` seperti saat ini.
2. Masuk ke <https://share.streamlit.io>, pilih **Create app**, kemudian tentukan repositori, branch, dan `app.py` sebagai *entrypoint*.
3. Pada **Advanced settings**, pilih Python 3.10 apabila tersedia, lalu jalankan proses deployment.
4. Uji satu prediksi melalui URL publik dan ganti placeholder di atas dengan URL tersebut sebelum membuat ZIP submission.

Struktur relatif repositori perlu dipertahankan karena Streamlit Community Cloud menjalankan aplikasi dari direktori utama repositori. Deklarasi dependensi dapat disimpan di direktori utama repositori atau di direktori yang sama dengan *entrypoint*. Referensi: [struktur berkas Streamlit](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization), [dependensi aplikasi](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies), dan [proses deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).

## Dashboard Metabase

Dashboard: **Jaya Jaya Institut — Student Dropout Monitor**

- Email: `root@mail.com`
- Password: `root123`
- URL lokal: <http://localhost:3030>
- Sumber data analitik: `dashboard/student_dropout.db`
- State Metabase persisten: `metabase.db.mv.db`

Dashboard berisi 16 kartu visual yang mencakup KPI dan distribusi hasil studi, tingkat dropout berdasarkan status pembayaran kuliah, persetujuan mata kuliah semester pertama, program studi, status debitur, beasiswa, dan waktu perkuliahan, segmen prioritas dukungan, perbandingan model dengan validasi silang, metrik kualitas pada data *holdout*, serta *permutation importance*. Jumlah mahasiswa ditampilkan bersama tingkat dropout agar kelompok kecil tidak keliru dianggap sebagai bukti yang kuat untuk keseluruhan populasi.

### Menjalankan dashboard yang tersimpan

1. Instal Java 21 dan unduh `metabase.jar` versi **0.58.7** dari halaman rilis resmi Metabase.
2. Letakkan berkas JAR tersebut di dalam folder `submission`, lalu jalankan perintah berikut melalui PowerShell:

```powershell
$env:MB_DB_TYPE = "h2"
$env:MB_DB_FILE = (Join-Path (Get-Location) "metabase.db")
$env:MB_JETTY_PORT = "3030"
java --add-opens=java.base/java.nio=ALL-UNNAMED -jar metabase.jar
```

3. Tunggu hingga <http://localhost:3030> dapat dibuka, lalu masuk menggunakan kredensial di atas.
4. Buka dashboard yang telah tersimpan. Jika Metabase melaporkan bahwa sumber SQLite berpindah lokasi, buka **Admin settings → Databases → Student Dropout Analytics**, kemudian ubah nama berkas menjadi `dashboard/student_dropout.db`.

## Temuan dan kesimpulan

Tingkat dropout historis mencapai 32,1%. Indikator deskriptif terkuat yang dapat ditindaklanjuti adalah:

- biaya kuliah tidak dibayar tepat waktu: 457 dari 528 mahasiswa mengalami dropout (86,6%);
- tingkat kelulusan mata kuliah semester pertama di bawah 50%: 719 dari 848 mahasiswa mengalami dropout (84,8%);
- tidak ada mata kuliah semester pertama yang lulus: 570 dari 718 mahasiswa mengalami dropout (79,4%);
- berstatus debitur: 312 dari 503 mahasiswa mengalami dropout (62,0%);
- tingkat dropout yang lebih tinggi pada program studi tertentu, terutama Equinculture dan Informatics Engineering dalam dataset ini.

Temuan tersebut menunjukkan hubungan atau asosiasi, bukan estimasi sebab-akibat. Prediktor operasional terkuat pada model—jumlah mata kuliah semester pertama yang lulus, status pembayaran kuliah, nilai semester pertama, jumlah mata kuliah yang diambil, dan jumlah evaluasi—selaras dengan hasil analisis deskriptif. Hal ini mendukung pelaksanaan intervensi segera setelah hasil semester pertama tersedia.

## Rekomendasi tindakan

1. Bentuk antrean penjangkauan yang ditinjau oleh petugas setelah hasil semester pertama tersedia. Hubungi mahasiswa dengan pendekatan suportif dan dokumentasikan alasan setiap penjangkauan.
2. Tawarkan konsultasi rencana pembayaran, konseling keuangan, dan pemeriksaan kelayakan beasiswa secara rahasia ketika terdapat indikator masalah pembayaran kuliah atau status debitur.
3. Tawarkan bimbingan belajar dan konsultasi akademik kepada mahasiswa yang belum meluluskan mata kuliah atau memiliki tingkat kelulusan di bawah 50%, dengan berkoordinasi bersama program studi terkait.
4. Minta tim program studi dengan tingkat dropout tinggi untuk meninjau hambatan kurikulum dan kapasitas dukungan mahasiswa tanpa memberikan stigma kepada mahasiswa tertentu.
5. Pantau proses penjangkauan, penggunaan layanan, status mahasiswa berikutnya, dan umpan balik mahasiswa. Evaluasi kembali kalibrasi, *recall*, tingkat positif palsu, dan kesenjangan antarsubkelompok sebelum setiap siklus pelatihan ulang.
6. Pertahankan mekanisme keputusan manual dan kanal pengajuan keberatan. Jangan pernah mengubah estimasi risiko menjadi keputusan merugikan yang dilakukan secara otomatis.
