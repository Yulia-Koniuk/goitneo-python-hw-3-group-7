from datetime import datetime
from collections import UserDict, defaultdict

# base class for fields record
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# class for storing a contact name
class Name(Field):
    pass

# class for storing a phone number (10 digits)
class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number should contain 10 letters")
        super().__init__(value)

# class for B-day
class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid birthday format (DD.MM.YYYY)")
        super().__init__(value)

# class for storing info about a contact, incld name and phone list
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None # adding B-day

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def remove_phone(self, phone):
        phone_obj = Phone(phone)
        if phone_obj in self.phones:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        old_phone_obj = Phone(old_phone)
        for i, phone_obj in enumerate(self.phones):
            if phone_obj.value == old_phone_obj.value:
                self.phones[i] = Phone(new_phone)
                break

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj.value

    # adding B-day       
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    # string update with B-day
    def __str__(self):
        contact_info = f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"
        if self.birthday:
            contact_info += f", birthday: {self.birthday.value}"
        return contact_info

# class for storing and managing records
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find(self, name):
        if name in self.data:
            return self.data[name]
        
    def get_birthdays_per_week(self):
        today = datetime.today().date()
        upcoming_birthdays = defaultdict(list)

        for name, record in self.items():
            if record.birthday:
                b_date = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
                b_date_this_year = b_date.replace(year=today.year)

                if b_date_this_year < today:
                   b_date_this_year = b_date_this_year.replace(year=today.year + 1)

                day_difference = (b_date_this_year - today).days
                birthday_weekday = b_date_this_year.strftime("%A")

                if 0 <= day_difference <= 7:
                    if birthday_weekday in ["Saturday", "Sunday"]:
                        day_of_week = "Monday"
                    else:
                        day_of_week = birthday_weekday

                    upcoming_birthdays[day_of_week].append(name)

        return upcoming_birthdays