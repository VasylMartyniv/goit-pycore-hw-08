from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number format. Must have 10 digits.")
        super().__init__(value)

    def __str__(self):
        return str(self.value)

    @staticmethod
    def is_valid_phone(value):
        return len(value) == 10 and value.isdigit()


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return f"{self.value.strftime('%d.%m.%Y')}"


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone):
        if Phone.is_valid_phone(phone):
            self.phones.append(Phone(phone))
        else:
            raise ValueError("Invalid phone number format.")

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError("Phone number not found.")

    def edit_phone(self, old_phone, new_phone):
        if not Phone.is_valid_phone(new_phone):
            raise ValueError("Invalid phone number format.")
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError("Phone number not found.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.data = {}

    def __str__(self):
        return '\n'.join([str(record) for record in self.data.values()])

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def get_upcoming_birthdays(self, days=7):
        today = datetime.today().date()
        prefix = f"Upcoming birthdays in {days} days:\n"
        future_birthdays = ''
        for name, record in self.data.items():
            if record.birthday is None:
                continue
            birthday = record.birthday.value.replace(year=today.year).date()
            birthday_this_year = birthday.replace(year=today.year)

            days_until_birthday = (birthday_this_year - today).days

            if 0 <= days_until_birthday <= 7:
                future_birthdays += f"{name}: {birthday_this_year.strftime('%d.%m.%Y')}\n"

        return prefix + future_birthdays if future_birthdays else "No upcoming birthdays."

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise None
