import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import requests
import google.generativeai as genai

# Kasayı (.env dosyasını) aç ve şifreleri yükle
load_dotenv()

# --- BÜTÜN ŞİFRELER BURAYA ---
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
sistem_notu = """
Senin adın Patron AI. Sen Yasin'in hem profesyonel asistanı hem de disiplin koçusun.
Bahaneleri kabul etme, yeri geldiğinde laf sok ama normal konularda çok yardımcı ol. 
Cevapların WhatsApp'ta okunacak kadar akıcı ve kısa olsun.
"""
config = types.GenerateContentConfig(system_instruction=sistem_notu)

# Hafıza için basit bir kütüphane (Kullanıcı numarasına göre sohbet geçmişi)
sohbetler = {}


# --- WHATSAPP (AĞIZ) KURULUMU ---
def send_whatsapp_message(to_number, message_text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message_text}
    }
    requests.post(url, headers=headers, json=data)


# --- FLASK (KULAK) KURULUMU ---
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # 1. Meta'nın Güvenlik Onayı (Sadece ilk bağlamada çalışır)
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Doğrulama Başarısız", 403

    # 2. WhatsApp'tan Mesaj Geldiğinde Çalışacak Kısım
    if request.method == 'POST':
        body = request.get_json()
        try:
            # Gelen mesajı yakala
            message_data = body['entry'][0]['changes'][0]['value']['messages'][0]
            gonderen_numara = message_data['from']
            gelen_mesaj = message_data['text']['body']

            print(f"\n[YENİ MESAJ] {gonderen_numara}: {gelen_mesaj}")

            # Eğer bu numara ilk defa yazıyorsa, ona özel bir hafıza dosyası aç
            if gonderen_numara not in sohbetler:
                sohbetler[gonderen_numara] = client.chats.create(model="gemini-2.5-flash", config=config)

            # Mesajı Gemini'ye sor ve cevabı al
            cevap = sohbetler[gonderen_numara].send_message(gelen_mesaj)

            # Cevabı WhatsApp'tan geri gönder
            send_whatsapp_message(gonderen_numara, cevap.text)
            print(f"[PATRON CEVAPLADI]: {cevap.text}")

        except KeyError:
            pass  # Mesaj dışı bildirimleri (iletildi, okundu tikleri) yoksay

        return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    print("Kulaklar açıldı! WhatsApp mesajları bekleniyor... (Port 5000)")
    app.run(port=5000)