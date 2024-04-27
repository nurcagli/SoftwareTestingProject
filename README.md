# SoftwareTestingProject
Software Test Project with Python

### 1.İsterler
▪ Django Web projesinde kullanıcıdan github depo linkinin (Repository Url) alınması
▪ Linkteki Git deposunun klonlanması
▪ Klonlanan depo içerisindeki *.java uzantılı tüm dosyaların belirlenmesi
▪ Belirlenen dosyalar içerisinden sadece sınıf olanların ayıklanması ve bu sınıfların
analize tabi tutulması
▪ Analiz sonuçlarının PostgreSql’e kaydedilmesi
▪ Sayfada aynı zamanda daha önceki analizleri veri tabanından çekip sayfada
gösterecek arayüzlerin bulunması
▪ Projenin modüler bir yapıda tasarım prensiplerine uygun bir şekilde yapılması
▪ Projede birim ve entegrasyon testlerinin yapılmış olması
### 2.Yapılan Çalışmalar
#### 2.1 Geliştirme
Web uygulaması başlatıldıktan sonra gelen http isteği bir post isteği ise uygulama,
kullanıcıdan aldığı url’i post isteği olarak işlemekte ve repository_url değişkenine
atamaktadır.
Daha sonra, GitCloning sınıfından bir nesne oluşturulur ve clone_git_repository metodunda
repository_url parametresi kullanılarak GitHub deposu klonlanır.
Eğer clonedRepoPath değişkeni None değilse Analysis sınıfının analyze_files metodu,
klonlanan depodaki dosyalar içerisinden .java uzantılı dosyaları bulur. extract_classes
fonksiyonunu kullanarak analiz eder , analiz sonuçlarını sınıflara ait bir listeye ekler ve tüm
analizler bitince sınıflar listesini döndürür.
analyze_files fonksiyonundan dönen bu sınıflar Database sınıfının save_db metoduna
gönderilir ve burada öncelikle sınıf içerikleri class_analysis fonksiyonu ile analiz edilir.
Analiz sonuçları kullanılarak sınıflara ait model oluşturulur. Bu model instance’ları bir listede
tutulur ve analizler tamamlanınca veritabanına toplu şekilde kaydedilir.
save_db fonksiyonun dönüş değeri ile veritabanına kaydedilen sınıfların kimlik numaraları
(classes_id) alınır. Bu kimlik numaralarıyla Database sınıfının get_batch metodu kullanılır
ve veritabanından analiz sonuçları alınır.
Analiz işlemi tamamlandıktan sonra, GitCloning sınıfının kill_processes_using_directory
metodu çağrılarak klonlanan depoyla ilişkili işlemler sonlandırılır.
Sonuçlar, sonuc.html şablonuna gönderilir ve bu şablon kullanıcıya gösterilir.
Eğer gelen istek bir GET isteği ise, veritabanından mevcut sonuçlar alınır ve bu sonuçlarla
birlikte index.html şablonu kullanıcıya gösterilir.
#### 2.2. Test
Proejenin işlevlerinin test edilebilmesi amacıyla test.py dosyasında iki adet sınıf
kullanılmıştır. Birincisi birim testleri ,ikincisi ise entegrasyon testleri yazmak amacıyla
oluşturulmuştur. Birim testleri altında 10’u parameterized ve 5’i faker kütüphanesi
kullanılarak oluşturulmuş toplam 37 birim testi bulunmaktadır.Entegrasyon testi sınıfı
içerisinde ise projenin veritabanı bağlantısıyla ilgili 5 entegrasyon testi yazılmıştır.
