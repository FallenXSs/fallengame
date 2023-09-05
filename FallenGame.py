import telebot
import random

# Telegram bot tokenınızı buraya ekleyin
TOKEN = '6514609660:AAH0hFPPgYVS4am21LQ5uRapVmbPdRJA5ns'

print("Fallen Game Is Only ❌⭕")

# Botunuzun instance'ını oluşturun
bot = telebot.TeleBot("6514609660:AAH0hFPPgYVS4am21LQ5uRapVmbPdRJA5ns")

# Etiketlenen kullanıcının hamlesini bekleyen oyun
games = {}

# /start komutunu işleyen fonksiyon
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hoş geldiniz! Oyunu başlatmak için /oyun komutunu kullanın. Bir sorunla karşılaşırsanız @BenYakup lütfen bildiriniz.")

# /oyun komutunu işleyen fonksiyon
@bot.message_handler(commands=['oyun'])
def start_game(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # Oyunu zaten başlatan kullanıcı varsa
    if chat_id in games:
        bot.send_message(chat_id, "Zaten bir oyun başlatılmış!")
        return

    # Oyunu başlatan kullanıcıya hoş geldin mesajı gönder
    games[chat_id] = {
        'turn': user_id,
        'board': [[' ' for _ in range(3)] for _ in range(3)]
    }
    bot.send_message(chat_id, f"{user_name} oyunu başlattı! İlk hamle sizden.")

# Oyun tahtasını çizmek için yardımcı fonksiyon
def draw_board(board):
    lines = []
    for row in board:
        line = ' | '.join(row)
        lines.append(line)
    sep = '-' * (len(line) + 2)
    return f"\n{sep}\n".join(lines)

# Oyun hamlesini işleyen fonksiyon
@bot.message_handler(func=lambda message: True)
def make_move(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    text = message.text

    if chat_id not in games:
        return

    game = games[chat_id]

    # Sadece oyun sırası olan kullanıcının hamlesini işle
    if user_id != game['turn']:
        bot.send_message(chat_id, "Şu anda sizin sıranız değil!")
        return

    # Geçerli hamle için doğru formatı kontrol et
    if not text.startswith('/') or len(text) != 4 or not text[1:].isdigit():
        bot.send_message(chat_id, "Geçersiz hamle formatı!")
        return

    # Oyuncunun hamlesini al ve tahtayı güncelle
    move = int(text[1:]) - 1
    row = move // 3
    col = move % 3

    if game['board'][row][col] != ' ':
        bot.send_message(chat_id, "Geçersiz hamle!")
        return

    game['board'][row][col] = '❌' if user_id == game['turn'] else '⭕️'
    game['turn'] = random.choice([user_id for user_id in game.keys() if user_id != 'turn'])

    # Oyun tahtasını gönder
    board = draw_board(game['board'])
    bot.send_message(chat_id, board)

    # Kazananı kontrol et
    if check_winner(game['board']):
        bot.send_message(chat_id, f"{user_name} oyunu kazandı! Oyun bitti.")
        del games[chat_id]

    # Tahta dolu ise oyunu berabere bitir
    elif ' ' not in [cell for row in game['board'] for cell in row]:
        bot.send_message(chat_id, "Oyun berabere bitti. Oyun bitti.")
        del games[chat_id]


# Kazananı kontrol eden yardımcı fonksiyon
def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return True
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return True
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return True
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return True
    return False


# Botu çalıştır
bot.polling()
