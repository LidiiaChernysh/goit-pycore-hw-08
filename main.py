# import needed functions
from command_parser import parse_input
from bot_oop import AddressBook, load_data, save_data, add_birthday, show_birthday, show_all, show_phone, add_contact, change_contact, birthdays


def main():

    """
    add [ім'я] [телефон]: Додати або новий контакт з іменем та телефонним номером, або телефонний номер до контакту який вже існує.
    change [ім'я] [старий телефон] [новий телефон]: Змінити телефонний номер для вказаного контакту.
    phone [ім'я]: Показати телефонні номери для вказаного контакту.
    all: Показати всі контакти в адресній книзі.
    add-birthday [ім'я] [дата народження]: Додати дату народження для вказаного контакту.
    show-birthday [ім'я]: Показати дату народження для вказаного контакту.
    birthdays: Показати дні народження на найближчі 7 днів з датами, коли їх треба привітати.
    hello: Отримати вітання від бота.
    close або exit: Закрити програму.

    """
    
    book = load_data()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book) 

            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()