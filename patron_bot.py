import urllib.request
import json

# --- META PANELİNDEN ALDIĞIN BİLGİLERİ BURAYA YAPIŞTIR ---

# 1. Sayfanın en üstündeki upuzun şifre
ACCESS_TOKEN = "EAANJH1gPGBMBRMvM6gaJ7j0EmYBv3BiAyRktZAtTLbpo7WCwrVwq0JITZBUk62g73Dlkx8C3SNpGzGnOqopeqFJHd7ZBNEWLAdZBQjygGDIFvIb7m1xBiB4mCxkrogdPJZAktZCY22Wf9JUZCNYhnJFxMJHDY9FEJjw3ufqlLfefjOBnNECwIBkYMUufteaSe6UJwZDZD"

# 2. "Gönderen Telefon Numarası Kimliği" (Test numarasının altındaki kısa ID)
PHONE_NUMBER_ID = "990174144189106"

# 3. Kendi telefon numaran (Kayıt ettiğin numara, başında + olmadan, ülke koduyla)
RECIPIENT_PHONE = "905352021619" # Örn: 905321234567

# --------------------------------------------------------

url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "messaging_product": "whatsapp",
    "to": RECIPIENT_PHONE,
    "type": "text",
    "text": {
        "body": "Selam Yasin! Ben yeni patronun. Kurulumsuz, saf Python ile bu işi çözdük. Şimdi gönül rahatlığıyla işe gidebilirsin! 😎"
    }
}

print("Mesaj gönderiliyor...")

# Kurulum gerektirmeyen yöntem (urllib)
req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
        print("✅ BAŞARILI! Telefonuna bak, mesaj gelmiş olmalı.")
except Exception as e:
    print("❌ HATA OLUŞTU:", e)