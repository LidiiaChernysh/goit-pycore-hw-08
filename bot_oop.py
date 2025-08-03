from collections import UserDict
from datetime import datetime, date, timedelta
import re
from functools import wraps
import pickle


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            if func.__name__ == "add_birthday":
                return f"Invalid value: {str(e)}"
                #return "Enter a valid date in the format DD.MM.YYYY."
            return f"Invalid value: {str(e)}"
        
        except KeyError:
            return "Such name does not exists in the contacts."
        except IndexError:
            return "Enter the argument (user name)."
        except AttributeError as e:
            if func.__name__ == "change_contact":
                return "Invalid value: check your phone"
            return f"Attribute error: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    return inner

class Field:
    # Base class for record fields.

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    

class Name(Field):
    # Class for storing contact name. Required field.
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    # Class for storing phone numbers. Has format validation (10 digits).

    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

    def __eq__(self, other):
        """Compare phone numbers by value, not object reference."""
        if isinstance(other, Phone):
            return self.value == other.value
        return False
    
class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
        super().__init__(value)


class Record:
    # A class for storing contact information, including name and phone list.

    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_birthday(self, birthday):
        if isinstance(birthday, datetime):
            birthday_str = Birthday(birthday.strftime("%d.%m.%Y"))
            birthday = Birthday(birthday_str)
        elif isinstance(birthday, str):
            birthday = Birthday(birthday)
        elif not isinstance(birthday, Birthday):
            raise ValueError("Birthday must be an instance of Birthday class.")
        self.birthday = birthday    


    def add_phone(self, phone):
        if isinstance(phone, str):  # If the passed phone number is a string, we create a Phone object
            phone = Phone(phone)
        if not isinstance(phone, Phone):
            raise ValueError("Phone must be an instance of Phone class.")
        self.phones.append(phone)
    

    def find_phone(self, phone):
        if isinstance(phone, str):
            phone = Phone(phone)
        for p in self.phones:
            if p == phone:
                return p
        return None


    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)  
        if phone_obj:
            self.phones.remove(phone_obj)
        else:
            raise ValueError("The phone number not found.")
    

    def edit_phone(self, old_phone, new_phone):
        try:
            new_phone_obj = Phone(new_phone)
        except ValueError:
            raise ValueError(f"The phone number {new_phone} is not valid.")

        phone_obj = self.find_phone(old_phone) 
        if phone_obj:
            self.remove_phone(old_phone)  
            self.add_phone(new_phone_obj)
        else:
            raise ValueError(f"The phone number {old_phone} not found.")

    def __str__(self):
        phones_str = ', '.join(str(p) for p in self.phones)
        birthday_str = self.birthday.value if self.birthday else "N/A"
        return f'Contact name: {self.name.value}; phones: {phones_str}; birthday: {birthday_str}'
    

class AddressBook(UserDict):
    # A class for storing and managing records.

    def add_record(self, record):
        if not isinstance(record, Record):
            raise ValueError("Record must be an instance of Record class.")
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Record not found.")
        
    def date_to_string(self, data):
        return data.strftime("%d.%m.%Y")

    def find_next_weekday(self, start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    def adjust_for_weekend(self, birthday):
        if birthday.weekday() >= 5:
            return self.find_next_weekday(birthday, 0)
        return birthday

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()
        next_year = today.year + 1


        for user in self.data.values():
            if not user.birthday:
                continue
            
            birthday_date = datetime.strptime(user.birthday.value, "%d.%m.%Y").date()
            birthday_this_year = birthday_date.replace(year=today.year)

            """
            Перевірка, чи не буде 
            припадати день народження вже наступного року.
            """
        

            if birthday_this_year < today:
                try:
                    next_year_birthday = birthday_this_year.replace(year=next_year)
                except ValueError:  # Handle February 29 to non-leap year
                    next_year_birthday = birthday_this_year + timedelta(days=365)

                if next_year_birthday <= (today + timedelta(7)):
                    birthday_this_year = next_year_birthday
            
                

            if today <= birthday_this_year < (today + timedelta(7)):
                
                
                """
                Додайте перенесення дати привітання на наступний робочий день,
                якщо день народження припадає на вихідний. 
                """
                congratulation_date = self.adjust_for_weekend(birthday_this_year)
                congratulation_date_str = self.date_to_string(congratulation_date)
                upcoming_birthdays.append({"name": user.name.value, "birthday":user.birthday.value, "congratulation_date": congratulation_date_str})
            else:
                pass
            
        return upcoming_birthdays

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())



@input_error
def add_birthday(args, book:AddressBook):
    name, birthday, *_ = args
    record = book.find(name)

    if record is None:
        return f"No contact found with the name {name}."
    
    if record.birthday is not None:
        return f"Birthday already exists for {name}."
    
    try:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    except ValueError as e:
        return f"Invalid date format: {e}"
    
        
@input_error
def show_birthday(args, book:AddressBook):
    name, *_ = args
    record = book.find(name)
    
    if record is None:
        return f"No contact found with the name {name}."

    birthday = record.birthday
    if not birthday:
        return f"Birthday is not set for {name}."

    return birthday.value

@input_error
def birthdays(book:AddressBook): 
    birthdays = book.get_upcoming_birthdays()

    if not birthdays:
        return "No contacts with upcoming birthdays this week."
    
    lines = []
    for b in birthdays:
        line = f"Contact name: {b['name']}; birthday: {b['birthday']}; congratulation date: {b['congratulation_date']}"
        lines.append(line)

    return "\n".join(lines)


@input_error
def add_contact(args, book:AddressBook):
    name, phone, *_ = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"Contact {name} added."
    else:
        message = f"Contact {name} updated."

    try:
        if phone:
            record.add_phone(phone)
    except ValueError as e:
        return f"Invalid phone number: {e}"
    
    return message
   
@input_error
def change_contact(args, book:AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)

    if record is not None:
        record.edit_phone(old_phone, new_phone)
        return f"Contact {name} updated with phone {new_phone}"
    else:
        add_contact(name, new_phone)
        return f"Contact {name} added."
    
@input_error
def show_phone(args, book:AddressBook):
    name, *_ = args
    record = book.find(name)

    if record is not None:
        phones_str = ', '.join(str(phone) for phone in record.phones)
        return f"{phones_str if phones_str else 'No phones'}"
    else: 
        return "No such contact"

@input_error
def show_all(book:AddressBook):
    if len(book) != 0:
        return f'All contacts: {book}'
    else:
        return 'There is no saved contacts.'

@input_error
def delete_contact(args, book:AddressBook):
    name, *_ = args
    record = book.find(name)
    if record:
        return book.delete(record)


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено