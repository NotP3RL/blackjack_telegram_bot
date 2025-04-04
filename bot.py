import os
import telebot
from telebot import types
from dotenv import load_dotenv
import blackjack


_PLAYER_CARDS, _DEALER_CARDS = [], []

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
token = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(token)


# Начало взаимодействия с ботом
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    start_game_button = types.InlineKeyboardButton(
        'Начать игру',
        callback_data='start_game'
    )
    markup.add(start_game_button)
    bot.send_message(message.chat.id, 'Привет', reply_markup=markup)


# Начало игры(получаем 2 карты дилера и игрока)
def start_game(message):
    global _DEALER_CARDS, _PLAYER_CARDS
    _DEALER_CARDS, _PLAYER_CARDS = blackjack.start_game()
    dealer_cards_img = [
        types.InputMediaPhoto(media=_DEALER_CARDS[0]['image']),
        types.InputMediaPhoto(media='https://deckofcardsapi.com/static/img/back.png')
    ]
    bot.send_message(message.chat.id, 'Карты диллера:')
    bot.send_media_group(message.chat.id, media=dealer_cards_img)
    player_cards_img = [
        types.InputMediaPhoto(media=_PLAYER_CARDS[0]['image']),
        types.InputMediaPhoto(media=_PLAYER_CARDS[1]['image'])
    ]
    bot.send_message(message.chat.id, 'Ваши карты:')
    bot.send_media_group(message.chat.id, media=player_cards_img)
    game(message)


# Выборы игрока(взять или нет карту)
def game(message):
    global _DEALER_CARDS, _PLAYER_CARDS
    if blackjack.count_score(_PLAYER_CARDS) >= 21:
        bot.send_message(
            message.chat.id,
            f'Ваш счёт: {blackjack.count_score(_PLAYER_CARDS)}'
        )
        game_results(message)
    else:
        markup = types.InlineKeyboardMarkup()
        draw_card_button = types.InlineKeyboardButton(
            'Да',
            callback_data='draw_card'
        )
        dont_draw_card_button = types.InlineKeyboardButton(
            'Нет',
            callback_data='dont_draw_card'
        )
        markup.add(draw_card_button, dont_draw_card_button)
        bot.send_message(
            message.chat.id,
            f'Ваш счёт: {blackjack.count_score(_PLAYER_CARDS)}. Хотите ли вы взять карту?',
            reply_markup=markup
        )


# Результаты игры(кто победил, какие очки)
def game_results(message):
    global _DEALER_CARDS, _PLAYER_CARDS
    if blackjack.count_score(_PLAYER_CARDS) <= 21:
        _DEALER_CARDS = blackjack.get_dealer_hand(_DEALER_CARDS)
    dealer_cards_img = []
    for img in blackjack.get_card_images(_DEALER_CARDS):
        dealer_cards_img.append(types.InputMediaPhoto(media=img))
    bot.send_message(message.chat.id, 'Карты диллера:')
    bot.send_media_group(message.chat.id, media=dealer_cards_img)
    markup = types.InlineKeyboardMarkup()
    start_game_button = types.InlineKeyboardButton(
        'Начать игру снова',
        callback_data='start_game'
    )
    markup.add(start_game_button)
    bot.send_message(
        message.chat.id,
        blackjack.check_winner(
            blackjack.count_score(_PLAYER_CARDS),
            blackjack.count_score(_DEALER_CARDS)
            ),
        reply_markup=markup
        )


def draw_player_card(message):
    global _PLAYER_CARDS
    _PLAYER_CARDS = blackjack.add_card(_PLAYER_CARDS)
    player_cards_img = []
    for img in blackjack.get_card_images(_PLAYER_CARDS):
        player_cards_img.append(types.InputMediaPhoto(media=img))
    bot.send_message(message.chat.id, 'Ваши карты:')
    bot.send_media_group(message.chat.id, media=player_cards_img)
    game(message)


# Обработчик всех ответов от пользователя
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'start_game':
        start_game(call.message)
    elif call.data == 'draw_card':
        draw_player_card(call.message)
    elif call.data == 'dont_draw_card':
        game_results(call.message)


bot.infinity_polling()
