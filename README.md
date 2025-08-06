# goit-pycore-hw-08

# 📒 GOIT-PyCore Homework 08 — Address Book Bot

Цей проєкт — консольний помічник для роботи з контактами: іменами, телефонами та днями народження.  
Підтримує збереження даних між сесіями за допомогою `pickle`.

---

## Як запустити проєкт

### 1. Клонувати репозиторій
git clone https://github.com/LidiiaChernysh/goit-pycore-hw-08.git
cd goit-pycore-hw-08

### 2. Створити віртуальне середовище (опціонально)
python3 -m venv .venv
source .venv/bin/activate  # (або .venv\Scripts\activate на Windows)

### 3. Запустити програму
python main.py (або python3 main.py)


## Команди, які підтримує бот
add [name] [phone] — додати контакт
change [name] [old phone] [new phone] — змінити номер телефону
phone [name] — показати телефони контакту
all — показати всі записи
add-birthday [name] [DD.MM.YYYY] — додати день народження
show-birthday [name] — показати день народження
birthdays — показати дні народження на поточному тижні
close, exit — завершити роботу


### Структура проєкту
goit-pycore-hw-08/
├── main.py                # Точка входу
├── bot_oop.py             # Реалізація класів AddressBook, Record тощо
├── command_parser.py      # Обробка команд користувача
├── README.md              # Цей файл