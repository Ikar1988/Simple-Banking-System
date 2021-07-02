import sqlite3
from random import randint

class BankingSystem:

    def __init__(self):
        self.cards = []
        self.card_number = None
        self.balance = 0
        self.conn = sqlite3.connect('card.s3db')

        cur = self.conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS card(
                id INTEGER,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def menu(self, level = '1'):
        if level == '1':
            print('1. Create an account')
            print('2. Log into account')
            print('0. Exit')
        elif level == '2.1':
            print('1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')

        key = int(input())
        print()
        return key

    def create_card(self):
        iin = '400000'
        can = str(randint(0, 999999999))
        number = iin + '0' * (9 - len(can)) + can
        checksum = self.get_checksum(number)
        number += str(checksum)
        pin = str(randint(1111, 9999))
        card = {'number': number, 'pin': pin}
        self.card_number = number

        cur = self.conn.cursor()
        cur.execute(f'INSERT into card (number, pin, balance) VALUES ({number}, {pin}, 0)')
        self.conn.commit()

        self.cards.append(card)
        return card

    def get_checksum(self, card_number):
        total = 0
        for i in range(1, 16):
            val = int(card_number[i - 1])
            if i % 2 == 1:
                val *= 2
                if val > 9:
                    val -= 9
            total += val

        checksum = 10 - total % 10
        if checksum == 10:
            checksum = 0
        return checksum

    def add_income(self, sum):
        self.balance += sum
        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE card SET balance = balance + {sum} WHERE number = {self.card_number}")
        self.conn.commit()

    def do_transfer(self, card_number):
        card_number = str(card_number)
        if card_number == self.card_number:
            print("You can't transfer money to the same account!")
            return False
        elif card_number[15] != str(self.get_checksum(card_number)):
            print('Probably you made a mistake in the card number. Please try again!')
            return False

        cursor = self.conn.cursor()
        card_for_transfer = cursor.execute(f"SELECT * FROM card WHERE number = {card_number}")
        if len(card_for_transfer.fetchall()) == 0:
            print('Such a card does not exist.')
            return False
        else:
            print('Enter how much money you want to transfer:')
            sum = int(input())
            if sum > self.balance:
                print('Not enough money!')
                return False
            cursor.execute(f"UPDATE card SET balance = balance + {sum} WHERE number = {card_number}")
            cursor.execute(f"UPDATE card SET balance = balance - {sum} WHERE number = {self.card_number}")
            self.balance -= sum

        self.conn.commit()
        print('Success!')

    def close_account(self):
        cursor = self.conn.cursor()
        cursor.execute(f"DELETE FROM card WHERE number = {card_number}")
        self.conn.commit()

    def login(self, number, pin):
        if {'number': number, 'pin': pin} in self.cards:
            self.card_number = number
            return True
        else:
            return False

    def logout(self):
        self.card_number = None


banking_system = BankingSystem()

is_exit = False

while not is_exit:
    key = banking_system.menu()
    if key == 1:
        card = banking_system.create_card()
        print('Your card has been created')
        print('Your card number:')
        print(card['number'])
        print('Your card PIN:')
        print(card['pin'])
    elif key == 2:
        print('Enter your card number:')
        card_number = input()
        print('Enter your PIN:')
        pin = input()
        print()
        if banking_system.login(card_number, pin):
            print('You have successfully logged in!', '\n')
            is_exit_submenu = False
            while not is_exit_submenu:
                key = banking_system.menu('2.1')
                if key == 1:
                    print('Balance:', banking_system.balance, '\n')
                if key == 2:
                    print('Enter income:')
                    banking_system.add_income(int(input()))
                if key == 3:
                    print('Enter card number:')
                    banking_system.do_transfer(int(input()))
                elif key == 4:
                    banking_system.close_account()
                    print('The account has been closed!')
                    is_exit_submenu = True
                elif key == 5:
                    banking_system.logout()
                    is_exit_submenu = True
                elif key == 0:
                    print('Bye!')
                    is_exit_submenu = True
                    is_exit = True
                    break

                print()

        else:
            print('Wrong card number or PIN!')
    elif key == 0:
        print('Bye!')
        is_exit = True

    print()




