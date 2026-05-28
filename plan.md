1. AI-Based Quality Prediction for Organic Coconut Sugar Production

Judul keren:

AI-Powered Quality Prediction System for Organic Coconut Sugar Manufacturing

Ide singkat:
Membuat sistem web sederhana untuk memprediksi apakah batch produksi gula kelapa masuk kategori:

Grade A
Grade B
Reject / perlu inspeksi ulang

berdasarkan data produksi seperti:

suhu pemasakan
waktu pemasakan
kadar air
warna produk
pH
tingkat kekeringan
hasil inspeksi visual
asal supplier nira kelapa
tanggal produksi

Kenapa cocok untuk IMC:
Karena perusahaan manufaktur food ingredients sangat peduli dengan quality control, consistency, export standard, dan certification compliance seperti BRC, organic, fairtrade.

Tools:

Flask untuk dashboard/input data
Scikit-Learn untuk model klasifikasi
Pandas untuk preprocessing
Matplotlib/Chart.js untuk grafik
SQLite/MySQL untuk database sederhana

Buzzword yang bisa dipakai:

AI-driven Quality Control
Predictive Quality Analytics
Smart Manufacturing
Food Safety Intelligence
Batch Quality Classification
Data-driven Production Monitoring

Implementasi sebenarnya simple:
Dataset bisa dummy/manual. Model cukup pakai:

Random Forest
Logistic Regression
Decision Tree
XGBoost kalau mau terlihat lebih advanced

Output dashboard:

“Batch #A102 predicted as Grade A with 91% confidence.”

Pakai ini:

Backend: Flask
Machine Learning: Scikit-Learn
Data: Pandas, NumPy
Database: SQLite
Model Saving: Joblib
Frontend: HTML + Bootstrap
Chart: Chart.js



boleh koreksi jika tidak sesuai:

Struktur project yang cocok
cocoq-ai/
  app.py
  train_model.py
  requirements.txt
  database.db

  data/
    coconut_sugar_batches.csv

  models/
    quality_model.pkl

  templates/
    base.html
    dashboard.html
    predict.html
    history.html

  static/
    css/
      style.css

boleh koreksi jika tidak sesuai:

Fitur yang cukup untuk MVP

Buat ini saja dulu:

1. Dashboard ringkasan produksi
2. Form input data batch
3. Prediksi Grade A / Grade B / Reject
4. Confidence score
5. Riwayat prediksi
6. Grafik distribusi grade
7. Grafik reject rate
8. Simulated sensor data generator

Kalau mau terlihat lebih advanced, tambahkan:

9. Feature importance
10. Recommendation message

ontoh output:

Batch B-2026-001 predicted as Grade A with 91% confidence.

Recommendation:
Moisture level is within export-grade range. Batch is suitable for packaging.

Data produksinya bisa dari:

1. Dummy dataset buatan sendiri
2. CSV manual
3. Input form dari dashboard
4. Simulated IoT data, kalau mau terlihat lebih keren


project ini cocok, tidak perlu alat IoT beneran, dan cukup dikerjakan di VSCode.

Paling ideal kamu bungkus sebagai:

AI-Powered Quality Prediction System for Organic Coconut Sugar Manufacturing

Tapi implementasinya:

Flask dashboard + Scikit-Learn model + dummy dataset + SQLite + Chart.js.

Keliatannya profesional, tapi tetap realistis dibuat sendiri.

“Simulated IoT” itu cuma tombol generate data otomatis. Misalnya backend Flask membuat angka random:

Temperature: 118.2°C
Moisture: 2.7%
pH: 5.9
Color Score: 74
Cooking Time: 92 minutes