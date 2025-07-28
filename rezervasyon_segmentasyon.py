import pyodbc  # SQL Server bağlantısı için gerekli kütüphane
import pandas as pd  # Veri analizi için pandas kütüphanesi
from sklearn.cluster import KMeans  # K-means algoritması için gerekli kütüphane
import matplotlib.pyplot as plt  # Görselleştirme için matplotlib kütüphanesi
# Random Forest algoritması için gerekli kütüphane
from sklearn.ensemble import RandomForestClassifier
# Veri setini eğitim ve test olarak ayırmak için gerekli kütüphane
from sklearn.model_selection import train_test_split
# Model başarısını değerlendirmek için gerekli kütüphane
from sklearn.metrics import classification_report, accuracy_score
from dotenv import load_dotenv # Çevresel değişkenleri yüklemek için gerekli kütüphane
import os # Çevresel değişkenleri kullanmak için gerekli kütüphane

# Çevresel değişkenleri yükle
load_dotenv()

# SQL Server bağlantı bilgilerini al
server = os.getenv("SERVER")
database = os.getenv("DATABASE")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
port = os.getenv("PORT")
driver = os.getenv("DRIVER")
encrypt = os.getenv("ENCRYPT")
trust_cert = os.getenv("TRUST_CERT")

# SQL Server'a bağlan
conn_str = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server},{port};"
    f"DATABASE={database};"
    f"UID={username};PWD={password};"
    f"Encrypt={encrypt};TrustServerCertificate={trust_cert}"
)
conn = pyodbc.connect(conn_str)


# SQL sorgusu, veriyi çekmek için
query = "SELECT * FROM Rezervasyonlar"

# DataFrame’e oku
df = pd.read_sql(query, conn)

# Tarih sütununu datetime formatına çevir
df["StartDate"] = pd.to_datetime(df["StartDate"])
# Tarih sütununu datetime formatına çevir
df["EndDate"] = pd.to_datetime(df["EndDate"])

df["Süre(dk)"] = (df["EndDate"] - df["StartDate"]
                  ).dt.total_seconds() / 60  # Süreyi dakika cinsine çevir

# Özellik matrisini oluştur # K-means algoritması için özellik matrisini seçiyoruz. Burada sadece "Süre(dk)" sütununu kullanıyoruz. neye göre segmentleyeceğimizi belirliyoruz.
X1 = df[["Süre(dk)"]]
# MekanId ile birlikte özellik matrisini oluştur # K-means algoritması için özellik matrisini seçiyoruz. Burada "Süre(dk)" ve "MekanId" sütunlarını kullanıyoruz. MekanId ile birlikte segmentleme yapıyoruz.
X2 = df[["Süre(dk)", "MekanId"]]

model1 = KMeans(n_clusters=2, random_state=42) #n_clusters=2, burada segment sayısını belirliyoruz. 2 segment oluşturacağız. random_state=42, modelin tekrarlanabilirliğini sağlamak için kullanılır.
df["Segment_sadece_süre"] = model1.fit_predict(X1) # K-means algoritması ile sadece süreye göre segmentleme yapıyoruz.

model2 = KMeans(n_clusters=2, random_state=42)
df["Segment_süre_ve_mekan"] = model2.fit_predict(X2) # K-means algoritması ile süre ve mekanId'ye göre segmentleme yapıyoruz.
# Sonuçları yazdır
print(df[["StartDate", "EndDate", "Süre(dk)", "Segment_sadece_süre"]])

plt.figure(figsize=(8, 5)) 
plt.scatter(df["Süre(dk)"], df["Segment_sadece_süre"], # Rezervasyon sürelerine göre segmentleri görselleştiriyoruz.
            c=df["Segment_sadece_süre"], cmap="viridis") 
plt.xlabel("Süre (dk)")  # rezervasyon süresi
plt.ylabel("Segment")  # ait olduğu segment
plt.title("Rezervasyon Süresine Göre Segmentler")
plt.grid(True) # Izgarayı açar
for i in range(len(df)):
    plt.text(df["Süre(dk)"][i], df["Segment_sadece_süre"][i]+0.05,
             f"{df['Süre(dk)'][i]:.1f}", fontsize=8)  # Rezervasyon süresini göster
plt.show()

# Veritabanındaki rezervasyon sürelerini analiz ederek, K-means algoritmasıyla 2 segment oluşturdum.
# Kısa süreli ve uzun süreli rezervasyonları otomatik olarak grupladım.
# Bu grupları matplotlib ile görselleştirerek her rezervasyonun hangi segmentte olduğunu etiketledim.

print("\n" + "="*40 + "\n")
print("Segment Dağılımı:")  # Segmentlerin sayısını göster
# Segmentlerin sayısını gösterir
print(df["Segment_sadece_süre"].value_counts())

print("\n" + "="*40 + "\n")
# Segmentlere göre süre istatistiklerini gösterir
print("\nSegmentlere Göre Süre İstatistikleri:")
# Segmentlere göre süre istatistiklerini gösterir
print(df.groupby("Segment_sadece_süre")["Süre(dk)"].describe()) #groupby ile segmentlere göre süre istatistiklerini gösteriyoruz.

print("\n" + "="*40 + "\n")
df["SegmentLabel"] = df["Segment_sadece_süre"].map(
    {0: "Kısa", 1: "Uzun"})  # Segment etiketlerini ekle
# Segment etiketlerinin sayısını gösterir
print(df["SegmentLabel"].value_counts())


print("\n" + "="*40 + "\n")
# Segment etiketlerine göre süre istatistiklerini gösterir
print(df.groupby("SegmentLabel")["Süre(dk)"].describe()) #describe ile ortalamaları, standart sapmaları ve diğer istatistikleri gösteriyoruz.

# Başlangıç saatini ekle dt.hour ile saat bilgisini alıyoruz
df["Saat"] = df["StartDate"].dt.hour
# Başlangıç gününü ekle dt.day_name() ile gün bilgisini alıyoruz haftanın gününü alır (pazar, pazartesi, salı vb.)
df["Gün"] = df["StartDate"].dt.day_name()

# "Süre" ve "MekanId" verilerinden yola çıkarak segment tahmini yapılır
X = df[["Süre(dk)", "MekanId"]]
y = df["Segment_sadece_süre"]

# RANDOM FOREST MODELİ
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42) # Veriyi eğitim ve test setlerine ayırıyoruz. test_size=0.3, verinin %30'unu test seti olarak ayırıyoruz. random_state=42, modelin tekrarlanabilirliğini sağlamak için kullanılır.

model_rf = RandomForestClassifier(random_state=42) # Random Forest modelini oluşturuyoruz. random forest, karar ağaçlarının bir araya gelmesiyle oluşan bir modeldir.
model_rf.fit(X_train, y_train) # Modeli eğitim verileri ile eğitiyoruz.

y_pred = model_rf.predict(X_test) # x_test verileri ile tahmin yapıyoruz.

print("\n" + "="*40 + "\n")
print("Random Forest Başarı Skoru:", accuracy_score(y_test, y_pred)) # Modelin doğruluk oranını gösterir
print("\nSınıflandırma Raporu:\n", classification_report(y_test, y_pred)) # Sınıflandırma raporu, modelin her sınıf için doğruluk, hatırlama ve F1 skorunu gösterir.

#Bu bölümde, elimizdeki rezervasyon verilerine bakarak yeni gelen bir rezervasyonun hangi segmente ait olacağını tahmin etmeyi amaçlıyoruz.
#“Süre ve mekan bilgisine göre rezervasyonun kısa mı uzun mu olacağını tahmin et.”
#Kullanılan Algoritma: RandomForestClassifier
#	•	Bu, bir denetimli öğrenme (supervised learning) algoritmasıdır.
#	•	İçerisinde birden fazla karar ağacı vardır.
#	•	Her ağaç kendi tahminini yapar ve en çok oylanan sonuç alınır.