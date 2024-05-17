import pickle

from classes import *


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the argument for the command."

    return inner


def parse_input(user_input):
    parts = user_input.split()
    command = parts[0].casefold()
    args = parts[1:]
    return command, args


@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    message = ''
    if record is not None:
        record.add_phone(phone)
        message = "Phone added to record."
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        message = "Contact added."
    return message


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    if name in book:
        record = book[name]
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        return "Contact not found."


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        return 'Contact not found.'
    return record


@input_error
def show_all(book):
    output = ''
    for name, phone in book.items():
        output += f"{name}: {phone}\n"
    return output


@input_error
def add_birthday(args, book):
    name, date = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(date)
    return "Birthday added to record."


def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return record.birthday


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def main():
    book = load_data()
    print("Welcome to the bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good-bye!")
            break
        if command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(book.get_upcoming_birthdays())
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(book)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
