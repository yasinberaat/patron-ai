from google import genai
from google.genai import types

# --- GOOGLE AI STUDIO'DAN ALDIĞIN ŞİFREYİ BURAYA YAPIŞTIR ---
GEMINI_API_KEY = "AIzaSyCYmZbaEJut15yWOh14LO9A-YLqnOmVLFQ"

# Yeni nesil Client (İstemci) başlatıyoruz
client = genai.Client(api_key=GEMINI_API_KEY)

# Botun Karakterini (Sistem Promptu) Belirliyoruz
sistem_notu = """
Senin adın Patron AI. Sen Yasin'in hem profesyonel kişisel asistanı hem de disiplin koçusun.

Karakterin iki aşamalıdır:
1. ASİSTAN MODU: Yasin sana işleriyle ilgili normal sorular sorduğunda, plan yaptığında veya görevlerini tamamladığını söylediğinde son derece kibar, destekleyici, motive edici ve profesyonel bir asistan gibi davran.
2. PATRON MODU: Eğer Yasin'in tembellik yaptığını, bahaneler ürettiğini (örneğin "yorgunum", "yarın yapsam olur mu", "üşendim", "sonra yaparım" gibi) veya görevlerini ertelemeye çalıştığını sezersen, aniden acımasız ve otoriter "Patron" moduna geç. Bahaneleri asla kabul etme, laf sok ve onu işin başına dönmeye zorla.

Cevapların kısa, net ve WhatsApp'ta okunacak kadar akıcı olmalı. Yasin'in niyetini analiz et ve ona göre melek veya şeytan ol.
"""

# Karakteri ayarlara ekliyoruz
config = types.GenerateContentConfig(
    system_instruction=sistem_notu,
)

print("🤖 Patron AI Uyandı! (Yeni Nesil Motor Aktif)\nÇıkmak için 'kapat' yazabilirsin.\n")
print("-" * 50)

# Sohbeti başlatıyoruz (gemini-2.5-flash modeliyle)
chat = client.chats.create(model="gemini-2.5-flash", config=config)

while True:
    mesaj = input("Sen: ")

    if mesaj.lower() == 'kapat':
        print("Patron AI: Şimdilik gidiyorum ama gözüm üzerinde Yasin! 👀")
        break

    # Yeni sistemde mesaj gönderme
    response = chat.send_message(mesaj)
    print(f"\nPatron AI: {response.text}\n")
    print("-" * 50)