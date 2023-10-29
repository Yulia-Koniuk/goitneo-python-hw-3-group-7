from datetime import datetime, timedelta
from HW_3_astnt_bot_internal_logic import AddressBook, Record

# parser
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

# decorator for managing mistakes
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            if str(ve) == "Phone number should contain 10 letters":
                return "Phone number should contain 10 letters."
            elif str(ve) == "Invalid birthday format (DD.MM.YYYY)":
                return "Invalid birthday format (DD.MM.YYYY)."
            elif func.__name__ in 'add_contact':
                return "Give me name and phone please."
            return str(ve)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid command."
        except Exception as e:
            return str(e)

    return inner

# adding new contact
@input_error
def add_contact(args, contacts):
    if len(args) != 2:  
        raise ValueError 
    name, phone = args
    name = name.lower()
    if name in contacts:
        contacts[name].add_phone(phone)  
    else:
        record = Record(name)
        record.add_phone(phone)
        contacts[name] = record
    return "Contact added."

# rewriting new phone
@input_error
def change_contact(args, contacts):
    if len(args) != 2: 
        raise ValueError("Give me name and phone please.")
    name, new_phone = args
    name = name.lower()
    if name in contacts:
        if not new_phone.isdigit() or len(new_phone) != 10:
            raise ValueError("Phone number should contain 10 letters.")
        contacts[name].phones = [new_phone]
        return "Contact updated."
    else:
        raise KeyError

# show phone number
@input_error
def show_phone(args, contacts):
    if len(args) != 1:
        raise ValueError 
    name = args[0].lower()
    if name in contacts:
        return contacts[name]
    else:
        raise KeyError 

# get all contacts
@input_error
def show_all(contacts):
    if not contacts:
        return "No contacts found."
    else:
        contacts_list = "\n".join(f"{name}: {phone}" for name, phone in contacts.items())
        return contacts_list
    
# adding birthday
@input_error
def add_birthday(args, contacts):
    if len(args) != 2:
        raise ValueError("Give me name and birthday please.")
    name, birthday = args
    name = name.lower()
    if name in contacts:
        contacts[name].add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError
    
# showing birthday
@input_error
def show_birthday(args, contacts):
    if len(args) != 1:
        raise ValueError
    name = args[0].lower()
    if name in contacts:
        birthday = contacts[name].birthday
        if birthday:
            return f"{name}'s birthday: {birthday.value}"
        else:
            return f"{name} doesn't have a birthday set."
    else:
        raise KeyError

# taking all birthdays that will happen next week
@input_error
def birthdays(contacts):
    upcoming_birthdays = contacts.get_birthdays_per_week()
    today = datetime.today().date()

    if not upcoming_birthdays:
        return "No upcoming birthdays in the next week."
    
    birthday_message = "Upcoming birthdays in the next week:\n"
    for day_of_week, names in sorted(upcoming_birthdays.items()):
        if day_of_week in ["Saturday", "Sunday"]:
            day_of_week = "Monday"  
        birthday_date = today
        while birthday_date.strftime('%A') != day_of_week:
            birthday_date += timedelta(days=1) 
        formatted_date = birthday_date.strftime('%A, %B %d')
        birthday_message += f"{formatted_date}: {', '.join(names)}\n"
    
    return birthday_message

# request-response cycle
def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all" and not args:
            print(show_all(contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(birthdays(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()


    