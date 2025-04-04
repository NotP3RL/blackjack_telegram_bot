import requests


_DECK_ID = 0


def get_new_deck(deck_count):
    response = requests.get(
        'https://deckofcardsapi.com/api/deck/new/shuffle/',
        params={'deck_count': deck_count}
    )
    return response.json()


def draw_card(count):
    global _DECK_ID
    response = requests.get(
        f'https://deckofcardsapi.com/api/deck/{_DECK_ID}/draw/',
        params={'count': count}
    )
    return response.json()


def count_score(cards):
    ace_count = 0
    sum = 0
    for card in cards:
        if card['value'] in ['KING', 'QUEEN', 'JACK']:
            sum += 10
        elif card['value'] == 'ACE':
            ace_count += 1
            sum += 11
        else:
            sum += int(card['value'])
        if sum > 21 and ace_count > 0:
            for ace in range(ace_count):
                sum -= 10
                ace_count -= 1
                if sum <= 21:
                    break
    return sum


# def parse_card(cards):
#     card_codes = ''
#     for card in cards:
#         card_codes += f'{card["code"]} '
#     return card_codes


def get_card_images(cards):
    card_images = []
    for card in cards:
        card_images.append(card['image'])
    return card_images


def check_winner(player_score, dealer_score):
    if player_score > 21:
        return 'Вы проиграли'
    elif dealer_score > 21:
        return f'Счёт диллера: {dealer_score}, Вы выиграли!'
    elif player_score > dealer_score:
        return f'Счёт диллера: {dealer_score}, Вы выиграли!'
    elif player_score < dealer_score:
        return f'Счёт диллера: {dealer_score}, Вы проиграли'
    elif player_score == dealer_score:
        return f'Счёт диллера: {dealer_score}, Ничья'


def start_game():
    global _DECK_ID
    deck = get_new_deck(6)
    _DECK_ID = deck['deck_id']
    start_cards = draw_card(4)
    dealer_cards = start_cards['cards'][:2]
    player_cards = start_cards['cards'][2:]
    return dealer_cards, player_cards


def add_card(cards):
    new_card = draw_card(1)
    cards.extend(new_card['cards'])
    return cards


def get_dealer_hand(cards):
    dealer_score = count_score(cards)
    while True:
        if dealer_score >= 17:
            break
        else:
            new_card = draw_card(1)
            cards.extend(new_card['cards'])
            dealer_score = count_score(cards)
    return cards


def main():
    pass
    # deck = get_new_deck(6)
    # deck_id = deck['deck_id']
    # start_cards = draw_card(deck_id, 4)
    # dealer_cards = start_cards['cards'][:2]
    # player_cards = start_cards['cards'][2:]
    # print(f'Карты диллера: {dealer_cards[0]["code"]}')
    # print(f'Ваши карты: {parse_card(player_cards)}')
    # player_score = count_score(player_cards)
    # dealer_score = count_score(dealer_cards)
    # print(f'Ваш счёт: {player_score}')
    # while True:
    #     if player_score == 21:
    #         print('Ваш счёт достиг максимума!')
    #         break
    #     elif player_score > 21:
    #         break
    #     response = input('Взять карту? (Да/Нет): ')
    #     if response == 'Да':
    #         new_card = draw_card(deck_id, 1)
    #         player_cards.extend(new_card['cards'])
    #         print(f'Ваши карты: {parse_card(player_cards)}')
    #         player_score = count_score(player_cards)
    #         print(f'Ваш счёт: {player_score}')
    #     elif response == 'Нет':
    #         break
    # if player_score > 21:
    #     while True:
    #         if dealer_score >= 17:
    #             break
    #         else:
    #             new_card = draw_card(deck_id, 1)
    #             dealer_cards.extend(new_card['cards'])
    #             dealer_score = count_score(dealer_cards)
    # print(check_winner(player_score, dealer_score))


if __name__ == '__main__':
    main()
