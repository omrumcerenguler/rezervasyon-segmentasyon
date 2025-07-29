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

def veri_cek():
    """
    Veritabanından rezervasyon verilerini çek ve gerekli dönüşümleri yap.
    Tarih sütunlarını datetime formatına çevirir ve süreyi dakika cinsine hesaplar.
    """
    query = "SELECT * FROM Rezervasyonlar"
    df = pd.read_sql(query, conn)
    # YENİ EKLENDİ: StartDate sütununu datetime formatına çeviriyoruz
    df["StartDate"] = pd.to_datetime(df["StartDate"])
    # YENİ EKLENDİ: EndDate sütununu datetime formatına çeviriyoruz
    df["EndDate"] = pd.to_datetime(df["EndDate"])
    # YENİ EKLENDİ: Rezervasyon süresini dakika cinsinden hesaplıyoruz
    df["Süre(dk)"] = (df["EndDate"] - df["StartDate"]).dt.total_seconds() / 60
    return df

def segment_et(df):
    """
    K-means algoritması ile rezervasyon sürelerine göre segmentler oluşturur.
    'Süre(dk)' sütununa göre segmentleme yapar ve segment etiketlerini ekler.
    """
    X1 = df[["Süre(dk)"]]
    # YENİ EKLENDİ: Mekan bilgisini de dahil ederek segmentleme için ikinci bir model
    X2 = df[["Süre(dk)", "MekanId"]]

    model1 = KMeans(n_clusters=2, random_state=42)
    df["Segment_sadece_süre"] = model1.fit_predict(X1)

    # YENİ EKLENDİ: Mekan ve süre bilgilerini kullanarak ikinci segment modeli oluşturuluyor
    model2 = KMeans(n_clusters=2, random_state=42)
    df["Segment_süre_ve_mekan"] = model2.fit_predict(X2)

    print(df[["StartDate", "EndDate", "Süre(dk)", "Segment_sadece_süre"]])

    print("\n" + "="*40 + "\n")
    print("Segment Dağılımı:")
    print(df["Segment_sadece_süre"].value_counts())

    print("\n" + "="*40 + "\n")
    print("\nSegmentlere Göre Süre İstatistikleri:")
    print(df.groupby("Segment_sadece_süre")["Süre(dk)"].describe())

    print("\n" + "="*40 + "\n")
    df["SegmentLabel"] = df["Segment_sadece_süre"].map({0: "Kısa", 1: "Uzun"})
    print(df["SegmentLabel"].value_counts())

    print("\n" + "="*40 + "\n")
    print(df.groupby("SegmentLabel")["Süre(dk)"].describe())

    # YENİ EKLENDİ: Zaman bazlı analiz için saat ve gün bilgisi
    df["Saat"] = df["StartDate"].dt.hour
    # YENİ EKLENDİ: Zaman bazlı analiz için saat ve gün bilgisi
    df["Gün"] = df["StartDate"].dt.day_name()

    return df

def grafik_ciz(df):
    # YENİ EKLENDİ: Segmentleri görselleştirmek için scatter plot fonksiyonu
    """
    Rezervasyon sürelerine göre oluşturulan segmentleri görselleştirir.
    Her rezervasyonun süresini ve segmentini gösterir.
    """
    plt.figure(figsize=(8, 5)) 
    plt.scatter(df["Süre(dk)"], df["Segment_sadece_süre"],
                c=df["Segment_sadece_süre"], cmap="viridis") 
    plt.xlabel("Süre (dk)")
    plt.ylabel("Segment")
    plt.title("Rezervasyon Süresine Göre Segmentler")
    plt.grid(True)
    for i in range(len(df)):
        plt.text(df["Süre(dk)"][i], df["Segment_sadece_süre"][i]+0.05,
                 f"{df['Süre(dk)'][i]:.1f}", fontsize=8)
    plt.show()

def model_egit(df):
    # YENİ EKLENDİ: Random Forest ile segment tahmini yapılır
    """
    Random Forest algoritması ile süre ve mekan bilgisine göre segment tahmini yapar.
    Modeli eğitim ve test verileri ile eğitir ve başarı skorunu, sınıflandırma raporunu yazdırır.
    """
    X = df[["Süre(dk)", "MekanId"]]
    y = df["Segment_sadece_süre"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)

    model_rf = RandomForestClassifier(random_state=42)
    model_rf.fit(X_train, y_train)

    y_pred = model_rf.predict(X_test)

    print("\n" + "="*40 + "\n")
    print("Random Forest Başarı Skoru:", accuracy_score(y_test, y_pred))
    print("\nSınıflandırma Raporu:\n", classification_report(y_test, y_pred))

def main():
    # YENİ EKLENDİ: Ana kontrol akışı burada başlar
    """
    Programın ana fonksiyonu. Veriyi çeker, segmentler, grafik çizer ve modeli eğitir.
    """
    df = veri_cek()
    df = segment_et(df)
    grafik_ciz(df)
    model_egit(df)

if __name__ == "__main__": # Programın ana fonksiyonu çalıştırılır
    print("Rezervasyon Segmentasyon Programı Başlatılıyor...")
    print("\n" + "="*40 + "\n")
    print("Veritabanından veri çekiliyor...")
    print("\n" + "="*40 + "\n")
    print("Veri Çekildi. Segmentleme ve Analiz Başlatılıyor...")
    print("\n" + "="*40 + "\n")
    # Ana fonksiyonu çağır 
    main()
    