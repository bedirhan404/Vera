🚀 Proje: Yapay Zeka Destekli Kişisel Sesli Asistan
Ne İşe Yarıyor? Bu proje, bilgisayarınızı tamamen sesli komutlarla yönetmenizi ve tıpkı bir insanla sohbet eder gibi iletişim kurmanızı sağlayan yapay zeka destekli bir masaüstü asistanıdır. Kendi özel arayüzü sayesinde her türlü sorunuza cevap verebilir, sohbet edebilir, bilgisayarınızda müzik açabilir, donanım durumunuzu kontrol edebilir ve sistemi (uykuya alma, yeniden başlatma, ekran görüntüsü çekme) yönetebilir.

💻 Kullanılan Teknolojiler
Bu asistanı hayata geçirirken gücünü Python'dan alan modern ve gelişmiş kütüphaneler kullandık:

Python: Projemizin temel kodlama dili. Tüm sistemin ve mantığın üzerine kurulduğu ana iskelet.
Google Gemini AI (google-genai): Asistanın beyni. Sadece belli komutları değil, sorulan karmaşık soruları anlamlandırmasını, mantıklı cevaplar üretmesini ve sizinle doğal bir dilde sohbet etmesini sağlayan yapay zeka modeli.
Konuşma Tanıma (SpeechRecognition): Sizin sesinizi mikrofondan anlık olarak dinleyip, bunu kodun anlayabileceği metin (yazı) formatına çeviren teknoloji (Speech-to-Text).
Doğal Ses Sentezi (edge-tts ve pygame): Asistanın robotik değil, gerçekçi ve akıcı bir insan sesiyle konuşmasını sağlayan (Text-to-Speech) teknoloji. PyGame ise bu ses dosyasının sorunsuz bir şekilde bilgisayarda oynatılması için kullanıldı.
Görsel Arayüz (customtkinter): Uygulamanın modern, karanlık temalı (Dark Mode) ve kullanıcı dostu arayüzünü (penceresini) tasarladığımız grafik kütüphanesi.
Sistem Yönetimi (psutil, pyautogui, os): Bilgisayarın işlemci (CPU) ve pil durumunu okumak, ekran görüntüsü (screenshot) almak, uygulamaları başlatmak ve bilgisayarı uyku moduna geçirmek için kullanılan sistem seviyesindeki teknolojiler.
Çoklu İş Parçacığı (threading): Asistanın arkada sizi dinlerken ve konuşurken uygulamanın arayüzünün donmamasını, her iki işlemin aynı anda (paralel olarak) gerçekleşmesini sağlayan mimari yapı.
Paketleme (PyInstaller): Yazdığımız tüm bu kodları ve kütüphaneleri, kurulum gerektirmeyen tek bir masaüstü uygulaması (.exe) haline getiren derleme teknolojisi.
🏗️ Nasıl Yaptık?
Projeyi adım adım şu mantıkla inşa ettik:

Dinleme ve Konuşma Modüllerinin Kurulumu: İlk olarak mikrofondan gelen sesi algılayıp yazıya döken dinle() fonksiyonunu ve oluşturduğumuz metinleri gerçekçi bir sesle dışarı aktaran konus() fonksiyonunu inşa ettik.
Yapay Zeka (Beyin) Entegrasyonu: Sisteme Google Gemini API'sini bağladık. Asistana "Sen çok zeki ve kibar bir asistansın, kullanıcıya efendim diye hitap edersin" şeklinde özel bir karakter yükleyerek cevaplarını şekillendirdik.
Komut-Tepki Mekanizması: Alınan sesli komutları analiz eden bir kontrol merkezi (döngü) kurduk. "Ekran görüntüsü al", "Spotify aç" veya "Uyku moduna geç" gibi belirli anahtar kelimeler duyulduğunda sistemin (işletim sisteminin) ilgili komutları çalıştırmasını sağladık.
Görsel Arayüz (GUI) Tasarımı: Asistanın sadece arka planda çalışmasını engellemek için, konuşmaların yazıya döküldüğü ve asistanın o anki durumunun ("Dinliyor...", "Düşünüyor...") anlık olarak takip edilebildiği bir pencere tasarladık.
Entegrasyon ve Derleme: Yazdığımız görsel arayüzü ve yapay zeka arka plan kodlarını "Threading" ile birbirine bağlayıp kusursuz çalışmalarını sağladık. Son aşamada ise projeyi paketleyerek kullanıma hazır, taşınabilir bir .exe dosyasına dönüştürdük.
