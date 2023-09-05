import telebot

TOKEN = "6514609660:AAH0hFPPgYVS4am21LQ5uRapVmbPdRJA5ns"

print("Fallen Game Is Only")

bot = telebot.TeleBot("6514609660:AAH0hFPPgYVS4am21LQ5uRapVmbPdRJA5ns")

oyuncu1 = "❌"
oyuncu2 = "⭕"
hane_durum = ["", "", "", "", "", "", "", "", ""]  # 9 adet hane durumu

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "FAllen game bot'a hoşgeldiniz bu bot Yakup Karahan tarafından ❌⭕ oyunu olarak tasarlanmıştır! destek ve yardım için @BenYakup")

@bot.message_handler(func=lambda message: True)
def hamle_yap(message):
    # Hamle yapılacak hane sayısını alın
    hane_sayisi = int(message.text)

    # Hane numarasını (1-9 arası) hane indeksine dönüştürün
    hane_indeks = hane_sayisi - 1

    # Belirtilen hanenin durumunu kontrol edin
    if hane_durum[hane_indeks] == '':
        # Oyuna göre hanenin durumunu belirleyin
        if message.from_user.id == 123456789:  # İlk oyuncunun ID'si
            hane_durum[hane_indeks] = oyuncu1
        elif message.from_user.id == 987654321:  # İkinci oyuncunun ID'si
            hane_durum[hane_indeks] = oyuncu2
        else:
            bot.reply_to(message, "Bu oyuncu oynamaya yetkili değil!")
            return
        
        # Güncellenmiş hane durumunu gönderin
        bot.reply_to(message, f"{message.from_user.first_name} tarafından {hane_durum[hane_indeks]} hamlesi yapıldı!\nHamle sonrası durum: {hane_durum}")
    else:
        bot.reply_to(message, "Bu hane zaten dolu!")

bot.polling()
            
