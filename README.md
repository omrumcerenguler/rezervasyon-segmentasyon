# 🇹🇷 Turkish Version
## 📊 Rezervasyon Segmentasyon Projesi

Bu proje, SQL Server üzerinde tutulan kurumsal rezervasyon verilerini analiz etmek ve bu verileri anlamlı segmentlere ayırmak amacıyla geliştirilmiştir. Python kullanılarak veri analizi, segmentasyon, görselleştirme ve sınıflandırma adımları profesyonel bir şekilde bir araya getirilmiştir.

---

## 🎯 Projenin Amacı

- **Rezervasyon Süre Analizi:** Rezervasyon başlangıç ve bitiş zamanlarından toplam süre hesaplanarak veriler daha anlamlı hale getirilir.
- **Segmentasyon:** K-means algoritması ile kısa ve uzun süreli rezervasyonlar otomatik olarak gruplandırılır.
- **Zaman Temelli Analiz:** Rezervasyonların saatlik ve günlük dağılımı analiz edilerek yoğunluklar belirlenir.
- **Sınıflandırma:** Random Forest algoritması kullanılarak yeni rezervasyonların hangi segmente ait olacağı tahmin edilir.
- **Görselleştirme:** Matplotlib kütüphanesi ile segmentlere ait grafikler çizilir.
- **Güvenli Bağlantı Yönetimi:** Veritabanı erişim bilgileri `.env` dosyasında saklanarak güvenlik sağlanır.

---

## 🔧 Proje Özellikleri

- **Veritabanı Bağlantısı:** PyODBC ile SQL Server'dan veri çekme.
- **Zaman Hesaplama:** StartDate ve EndDate sütunlarından rezervasyon süresi (dakika) hesaplanması.
- **K-Means Kümeleme:** Rezervasyon verilerini süreye göre segmentlere ayırma.
- **Random Forest Sınıflandırma:** Süre ve mekan bilgilerine dayalı segment tahmini.
- **Saat ve Gün Analizi:** Rezervasyonların hangi saat ve günlerde yoğunlaştığını analiz etme.
- **Görsel Çıktılar:** Segment dağılım grafikleri ve istatistik özetleri.
- **Güvenli Ortam Değişkenleri:** Tüm hassas bilgiler `.env` dosyasında saklanır.

---

## 💾 Kullanılan Kütüphaneler

- pandas – Veri analizi
- pyodbc – SQL Server bağlantısı
- scikit-learn – K-Means ve RandomForest
- matplotlib – Grafik çizimleri
- python-dotenv – `.env` dosyasını yönetmek için

---

## 🚀 Kurulum ve Çalıştırma

### 1. Gerekli Kütüphaneleri Yükleme
```
pip install -r requirements.txt
```

### 2. `.env` Dosyasını Oluşturma
Proje ana dizinine `.env` dosyasını oluşturun ve aşağıdaki formatta doldurun (bilgiler örnek olarak verilmiştir, kendi kurumunuza ait bilgileri kullanın):

```
SERVER=your_server_ip
PORT=your_port
DRIVER=your_driver_name
DATABASE=your_database_name
USERNAME=your_username
PASSWORD=your_password
ENCRYPT=no
TRUST_CERT=yes
```

> 📌 **Not:** Yukarıdaki bilgileri çalıştığınız kurumun sistem yöneticisi, veri tabanı yöneticisi ya da proje sorumlusu sağlamalıdır. Bu bilgiler genellikle herkese açık değildir ve sadece yetkili kişilere özel olarak güvenli bir şekilde paylaşılır. Bağlantının başarıyla sağlanabilmesi için bu bilgilerin eksiksiz ve doğru bir şekilde `.env` dosyasına girilmesi gerekmektedir.

### 3. Python Dosyasını Çalıştırma
```
python rezervasyon_segmentasyon.py
```

---

## 📁 Dosya Yapısı

```
rez. segmantasyon/
├── rezervasyon_segmentasyon.py
├── requirements.txt
├── .env
└── README.md

```

### Veritabanı Tablosu: `Rezervasyonlar`

| Sütun Adı             | Veri Tipi           | Açıklama                                 |
|-----------------------|---------------------|------------------------------------------|
| Id                    | int                 | Rezervasyonun benzersiz kimliği          |
| KullaniciId           | int                 | Rezervasyonu yapan kullanıcı             |
| MekanId               | int                 | Rezervasyon yapılan mekan                |
| StartDate             | datetime            | Rezervasyonun başlangıç zamanı           |
| EndDate               | datetime            | Rezervasyonun bitiş zamanı               |
| Durum                 | int                 | Rezervasyonun durumu (1: Onaylı, 2: Bekliyor vb.) |
| Aciklama              | nvarchar(max)       | Rezervasyonla ilgili açıklama            |
| Subject               | nvarchar(max) / NULL| Konu başlığı (isteğe bağlı)              |
| ReddedildiMi          | bit (0/1)           | Rezervasyon reddedildi mi                |
| ReddetmeAciklamasi    | nvarchar(max) / NULL| Reddetme nedeni (eğer varsa)             |
| OwnerId               | int / NULL          | Rezervasyonun ait olduğu kişi ID'si      |


---

## ⚠️ Güvenlik Notu

- `.env` dosyası **kesinlikle** GitHub gibi herkese açık platformlara yüklenmemelidir.  
- `.gitignore` dosyası, `.env` dosyasını varsayılan olarak göz ardı eder.

---

## 📈 Örnek Çıktılar

- Segment bazlı istatistik tabloları (ortalama, standart sapma vb.)
- Kısa ve uzun rezervasyonların görsel grafikleri
- Random Forest sınıflandırma başarı oranı ve metrikleri

---

## 📬 İletişim

Bu proje, staj süresince yapılan bir veri analizi çalışmasıdır.  
**Geliştirici:** Ömrüm Ceren Güler  
**İletişim:** omrumguler35@gmail.com

---

# 📄 English Version

## 📊 Reservation Segmentation Project

This project is designed to analyze institutional reservation data stored on an SQL Server and segment it into meaningful groups. Using Python, this project brings together data analysis, clustering, visualization, and classification steps in a professional and secure workflow.

---

## 🎯 Project Objectives

- **Reservation Duration Analysis:** Compute total duration from start and end timestamps to derive meaningful features.
- **Segmentation:** Automatically group short and long reservations using the K-Means algorithm.
- **Time-Based Insights:** Analyze distribution by hour and day to identify high-traffic periods.
- **Classification:** Predict reservation segment using the Random Forest algorithm.
- **Visualization:** Generate segment-specific charts using Matplotlib.
- **Secure Credential Handling:** Store database credentials in a `.env` file for security.

---

## 🔧 Features

- **Database Connectivity:** Fetch data from SQL Server via PyODBC.
- **Time Calculation:** Derive duration (in minutes) from `StartDate` and `EndDate`.
- **K-Means Clustering:** Cluster reservations by duration.
- **Random Forest Classification:** Predict segments based on duration and venue ID (`MekanId`).
- **Temporal Analysis:** Examine reservation frequency by hour and day.
- **Visual Outputs:** Generate segment distribution charts and summary statistics.
- **Secure Environment Variables:** All sensitive credentials are managed using a `.env` file.

---

## 💾 Libraries Used

- `pandas` – Data analysis
- `pyodbc` – SQL Server connection
- `scikit-learn` – K-Means and Random Forest algorithms
- `matplotlib` – Visualization
- `python-dotenv` – Environment variable management

---

## 🚀 Installation & Usage

### 1. Install Required Libraries
```
pip install -r requirements.txt
```

### 2. Create `.env` File

Create a `.env` file in the root directory and populate it as shown below. These are placeholders — request the actual connection values from your institution or system administrator.

```
SERVER=your_server_ip
PORT=your_port
DRIVER=your_driver_name
DATABASE=your_database_name
USERNAME=your_username
PASSWORD=your_password
ENCRYPT=no
TRUST_CERT=yes
```

> 📌 **Note:** These credentials must be securely obtained from your organization's system administrator, database admin, or project supervisor. Do not share them publicly. Ensure that all fields are entered accurately to establish a successful connection.

### 3. Run the Python File
```
python rezervasyon_segmentasyon.py
```

---

## 📁 File Structure

```
rez. segmantasyon/
├── rezervasyon_segmentasyon.py
├── requirements.txt
├── .env
└── README.md
```
### Database Table: `Reservations`

| Column Name           | Data Type           | Description                              |
|-----------------------|---------------------|------------------------------------------|
| Id                    | int                 | Unique ID of the reservation             |
| KullaniciId           | int                 | User who made the reservation            |
| MekanId               | int                 | Venue of the reservation                 |
| StartDate             | datetime            | Start time of the reservation            |
| EndDate               | datetime            | End time of the reservation              |
| Durum                 | int                 | Status of reservation (1: Approved, 2: Pending etc.) |
| Aciklama              | nvarchar(max)       | Additional description                   |
| Subject               | nvarchar(max) / NULL| Subject line (optional)                  |
| ReddedildiMi          | bit (0/1)           | Was the reservation rejected?            |
| ReddetmeAciklamasi    | nvarchar(max) / NULL| Reason for rejection (if any)            |
| OwnerId               | int / NULL          | ID of the person who owns the reservation|

---

## ⚠️ Security Note

- The `.env` file **must not** be uploaded to public platforms such as GitHub.
- The `.gitignore` file already includes `.env` to ensure this.

---

## 📈 Sample Outputs

- Segment-specific statistical summaries (mean, std dev, etc.)
- Visual charts showing distribution of short vs. long reservations
- Random Forest classification report and accuracy metrics

---

## 📬 Contact

This project was developed as part of an internship data analysis task.  
**Developer:** Ömrüm Ceren Güler  
**Contact:** omrumguler35@gmail.com
