# реализация мастей и достоинств карт

import random

# масти
suits = ('Черви', 'Буби', 'Пики', 'Крести')
# значения карт
ranks = ('Двойка', 'Тройка', 'Четвёрка', 'Пятёрка', 'Шестёрка', 'Семёрка', 'Восьмёрка',
         'Девятка', 'Десятка', 'Валет', 'Дама', 'Король', 'Туз')
# достоинства карт, где ключи - достоинства карт, значения - очки
values = {'Двойка': 2, 'Тройка': 3, 'Четвёрка': 4, 'Пятёрка': 5, 'Шестёрка': 6, 'Семёрка': 7, 'Восьмёрка': 8,
          'Девятка': 9, 'Десятка': 10, 'Валет': 10, 'Дама': 10, 'Король': 10, 'Туз': 11}

# переменная для while
playing = True


# класс Card содержит 2 атрибута - масть и достоинство
class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' ' + self.suit


# Создание колоды карт
class Deck:

    def __init__(self):
        self.deck = [] # начинаем с пустого списка
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    # покажем в строковом виде всю колоду карт
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'В колоде находятся карты:' + deck_comp

    # перемешиваем колоду
    def shuffle(self):
        random.shuffle(self.deck)

    # сдать карты
    def deal(self):
        single_card = self.deck.pop()
        return single_card


# создание руки, тут хранятся очки игрока и его карты
class Hand:
    def __init__(self):
        self.cards = []  # пустой список для начала
        self.value = 0   # начинаем счёт со значения 0
        self.aces = 0    # атрибут, чтобы учитывать тузов

    def add_card(self, card):
        # card - это из объекта Deck, поэтому это объект Card из Deal.deck() -> Card(suit,rank)
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Туз':
            self.aces += 1

    def adjust_for_ace(self):
        # если сумма больше 21 и всё ещё есть тузы, то считаем тузы не как 11, а как 1
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1


# создание фишек (начальные фишки игрока, его ставки, текущие выигрыши)
class Chips:

    def __init__(self, total=100):
        self.total = total  # установить по умолчанию/у пользователя запрашивать. Здесь храним общие кол-во фишек игрока
        self.bet = 0       # здесь храним ставку

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


# функция, в которой игрок делает ставки
def take_bet(chips):

    while True:

        try:
            chips.bet = int(input('Сколько фишек Вы хотите поставить? '))

        except:
            print('Извините, пожалуйста, введите число')

        else:

            if chips.bet > chips.total:
                print('У Вас недостаточно фишек. Доступное количество фишек: {}'.format(chips.total))
            else:
                break


# функция, где игрок берёт доп карты
def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()


# функция предлагает взять игроку доп карту или остаться при текущих
def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input('Взять дополнительную карту - введите h или остаться при текущих картах введите - s: ')

        if x[0].lower() == 'h':
            hit(deck, hand)

        elif x[0].lower() == 's':
            print('Игрок остаётся при текущих картах. Ход дилера.')
            playing = False

        else:
            print('Извините, ответ непонятен. Пожалуйста, введите s млм h: ')
            continue
        break


# функции для отображения карт
def show_some(player, dealer):
    print('\nКарты Дилера:')
    print(' <карта скрыта>')
    print('', dealer.cards[1])
    print('\nКарты игрока:', *player.cards, sep='\n ')


def show_all(player, dealer):
    print('\nКарты Дилера:', *dealer.cards, sep='\n')
    print('Карты Дилера =', dealer.value)
    print('\nКарты игрока:', *player.cards, sep='\n ')
    print('Карты игрока =', player.value)


# функция для обработки сценариев завершения игры
def player_busts(player, dealer, chips):
    print('Превышение суммы 21 для Игрока.')
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print('Игрок выиграл.')
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print('Дилер выиграл.')
    chips.lose_bet()


def dealer_busts(player, dealer, chips):
    print('Игрок выиграл. Дилер превысил 21')
    chips.win_bet()


def push(player, dealer):
    print('Ничья!')


while True:
    print('Добро пожаловать в игру Блэкджек!')

    # создать и перемешать колоду карт, выдайте каждому Игроку по две карты
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # установить кол-во фишек у игрока
    player_chips = Chips()

    # спросите у Игрока его ставку
    take_bet(player_chips)

    # Покажите карты (но одна карта Дилера скрыта)
    show_some(player_hand, dealer_hand)

    while playing:
        # спросить игрока, хочет ли он взять карты
        hit_or_stand(deck, player_hand)

        # покажите карты (но у дилера 1 скрыта)
        show_some(player_hand, dealer_hand)

        # если карты игрока превысили 21
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
        # показываем все карты
        show_all(player_hand, dealer_hand)

        # выполняем различные варианты завершения игры
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
    # сообщить игроку сумму его фишек
    print('\n Количество фишек игрока: {}'.format(player_chips.total))

    # спросить его, хочет он играть снова
    new_game = input('Хотите сыграть снова? y или n ')

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('Спасибо за игру!')
        break
