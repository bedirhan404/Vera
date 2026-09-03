import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import psutil
import pywhatkit
import pyautogui
import threading
import customtkinter as ctk
from dotenv import load_dotenv
from google import genai
from google.genai import types

import pygame
import edge_tts
import asyncio

# .env dosyasındaki değişkenleri yükle
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# pygame mixer ayarları (Sesi çalmak için)
pygame.mixer.init()

class PerseveraApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PERSEVERA - Sistem Arayüzü")
        self.geometry("700x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Ana çerçeve
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Sohbet Ekranı
        self.textbox = ctk.CTkTextbox(self.main_frame, font=("Helvetica", 15), wrap="word")
        self.textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.textbox.insert("0.0", "PERSEVERA Sistemleri Başlatılıyor...\n\n")
        self.textbox.configure(state="disabled")
        
        # Durum Çubuğu
        self.status_label = ctk.CTkLabel(self.main_frame, text="Hazırlanıyor...", font=("Helvetica", 16, "bold"), text_color="#00ffcc")
        self.status_label.grid(row=1, column=0, padx=10, pady=(0, 10))
        
        # Arka plan işlemlerini kontrol etmek için bayrak
        self.running = True
        self.chat_session = None
        
        # Yapay zeka motorunu hazırlama
        if API_KEY and API_KEY != "buraya_api_anahtarınızı_yapisitirin":
            try:
                client = genai.Client(api_key=API_KEY)
                self.chat_session = client.chats.create(
                    model="gemini-2.5-flash",
                    config=types.GenerateContentConfig(
                        system_instruction="Senin adın PERSEVERA. Sen çok zeki, kibar ve yetenekli bir yapay zeka asistanısın. Kullanıcıya 'Efendim' diye hitap edersin. Cevapların çok uzun olmasın, sesli olarak okunacağı için kısa, net ve konuşma diline uygun cevaplar vermelisin.",
                    )
                )
            except Exception as e:
                self.log(f"Gemini Başlatma Hatası: {e}")

        # Thread başlat
        self.thread = threading.Thread(target=self.asistan_dongusu)
        self.thread.daemon = True
        self.thread.start()
        
        # Kapatma olayını yakala
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.running = False
        self.destroy()

    def log(self, metin, kaynak="sistem"):
        self.textbox.configure(state="normal")
        if kaynak == "kullanici":
            self.textbox.insert("end", f"Siz: {metin}\n\n")
        elif kaynak == "asistan":
            self.textbox.insert("end", f"PERSEVERA: {metin}\n\n")
        else:
            self.textbox.insert("end", f"{metin}\n\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def set_status(self, durum):
        # GUI güncellemelerini ana thread'de yapmak daha güvenlidir
        self.after(0, lambda: self.status_label.configure(text=durum))

    def konus(self, metin):
        """Verilen metni akıcı sesle okur."""
        self.log(metin, "asistan")
        self.set_status("Konuşuyor...")
        ses_dosyasi = "cevap.mp3"
        
        if os.path.exists(ses_dosyasi):
            try:
                os.remove(ses_dosyasi)
            except:
                pass
                
        async def _olustur():
            communicate = edge_tts.Communicate(metin, "tr-TR-AhmetNeural")
            await communicate.save(ses_dosyasi)
            
        try:
            asyncio.run(_olustur())
            pygame.mixer.music.load(ses_dosyasi)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() and self.running:
                pygame.time.Clock().tick(10)
            pygame.mixer.music.unload()
        except Exception as e:
            self.log(f"Ses çalınırken hata: {e}")

    def selam_ver(self):
        saat = int(datetime.datetime.now().hour)
        if saat >= 0 and saat < 12:
            self.konus("Günaydın Efendim!")
        elif saat >= 12 and saat < 18:
            self.konus("Tünaydın Efendim!")
        else:
            self.konus("İyi Akşamlar Efendim!")
        
        if not API_KEY or API_KEY == "buraya_api_anahtarınızı_yapisitirin":
            self.konus("Sistemlerim tam kapasite çalışmıyor. Lütfen .env dosyasına Gemini API anahtarını girin.")
        else:
            self.konus("Sistemler devrede. Ben PERSEVERA. Sizin için ne yapabilirim?")

    def dinle(self):
        r = sr.Recognizer()
        with sr.Microphone() as kaynak:
            self.set_status("Dinliyor...")
            r.pause_threshold = 1
            try:
                audio = r.listen(kaynak, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                return "None"

        try:
            self.set_status("Anlaşılıyor...")
            komut = r.recognize_google(audio, language='tr-TR')
            self.log(komut, "kullanici")
            return komut.lower()
        except:
            return "None"

    def asistan_dongusu(self):
        self.selam_ver()
        
        while self.running:
            self.set_status("Bekliyor...")
            komut = self.dinle()

            if komut == "None" or not self.running:
                continue

            # 1. Çıkış
            if 'kendini kapat' in komut or 'görüşürüz' in komut or 'sistemleri kapat' in komut:
                self.konus("Sistemleri kapatıyorum. İyi günler dilerim efendim.")
                self.on_closing()
                break

            # 2. Müzik
            elif 'çal' in komut or 'oynat' in komut:
                sarki = komut.replace('çal', '').replace('oynat', '').replace('persevera', '').strip()
                self.konus(f"{sarki} çalınıyor...")
                pywhatkit.playonyt(sarki)

            # 3. Saat
            elif 'saat kaç' in komut:
                strTime = datetime.datetime.now().strftime("%H:%M")
                self.konus(f"Efendim, saat şu an {strTime}")

            # 4. Sistem Durumu
            elif 'sistem durumu' in komut or 'şarjım' in komut:
                pil = psutil.sensors_battery()
                cpu = psutil.cpu_percent()
                durum = f"İşlemci kullanımınız yüzde {cpu}. "
                if pil:
                    durum += f"Pil seviyeniz yüzde {pil.percent}."
                self.konus(durum)

            # 5. Ekran Görüntüsü Alma
            elif 'ekran görüntüsü' in komut or 'fotoğraf çek' in komut:
                self.konus("Ekran görüntüsü alınıyor ve masaüstüne kaydediliyor efendim.")
                masaustu = os.path.join(os.path.expanduser("~"), "Desktop")
                dosya_adi = f"Ekran_Goruntusu_{datetime.datetime.now().strftime('%H%M%S')}.png"
                tam_yol = os.path.join(masaustu, dosya_adi)
                try:
                    pyautogui.screenshot(tam_yol)
                    self.log(f"Ekran görüntüsü kaydedildi: {tam_yol}")
                except Exception as e:
                    self.konus("Ekran görüntüsü alınırken bir hata oluştu.")
                    self.log(str(e))

            # 6. Bilgisayarı Yeniden Başlatma
            elif 'bilgisayarı yeniden başlat' in komut or 'sistemi yeniden başlat' in komut:
                self.konus("Sistem yeniden başlatılıyor. Lütfen bekleyin...")
                os.system("shutdown /r /t 5")

            # 7. Bilgisayarı Uyku Moduna Alma
            elif 'uyku moduna al' in komut or 'bilgisayarı uyut' in komut:
                self.konus("Bilgisayar uyku moduna alınıyor efendim. Görüşmek üzere.")
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            # 8. İnternet ve Uygulamalar
            elif 'youtube' in komut and 'aç' in komut:
                self.konus("Youtube açılıyor...")
                webbrowser.open("youtube.com")
            elif 'google' in komut and 'aç' in komut:
                self.konus("Google açılıyor...")
                webbrowser.open("google.com")
            elif 'spotify' in komut and 'aç' in komut:
                self.konus("Spotify açılıyor...")
                os.system("start spotify:")
            elif 'discord' in komut and 'aç' in komut:
                self.konus("Discord açılıyor...")
                os.system("start discord")

            # 9. Vikipedi
            elif 'vikipedi' in komut or 'kimdir' in komut:
                aranacak = komut.replace("vikipedi", "").replace("kimdir", "").replace("persevera", "").strip()
                self.konus("Kayıtlarda arıyorum...")
                try:
                    wikipedia.set_lang("tr")
                    self.konus(wikipedia.summary(aranacak, sentences=2))
                except:
                    self.konus("Buna dair bir bilgi bulamadım.")

            # 10. Gemini AI
            else:
                if not API_KEY or API_KEY == "buraya_api_anahtarınızı_yapisitirin":
                    self.konus("API anahtarı eksik olduğu için size cevap veremiyorum.")
                    continue
                    
                try:
                    self.set_status("Düşünüyor...")
                    response = self.chat_session.send_message(komut)
                    cevap = response.text
                    if len(cevap) > 300:
                        cevap = cevap[:300] + "... efendim, geri kalanını ekrandan okuyabilirsiniz."
                    self.konus(cevap)
                except Exception as e:
                    self.log(f"Gemini Hatası: {e}")
                    self.konus("Bağlantımda bir sorun var.")

if __name__ == "__main__":
    app = PerseveraApp()
    app.mainloop()
