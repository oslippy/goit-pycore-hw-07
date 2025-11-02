from enum import Enum

from colorama import Fore

from address_book import AddressBook, Record
from exceptions import AddressBookError, InvalidInputError, RecordNotFoundError, PhoneNotFoundError
from utils import input_error


@input_error
def add_contact(args: list[str], address_book: AddressBook) -> str:
    name, phone_number = args
    record = address_book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        address_book.add_record(record)
        message = "Contact added."
    if phone_number:
        record.add_phone(phone_number)
    return message


@input_error
def change_contact(args: list[str], address_book: AddressBook) -> str:
    name, phone_number = args
    record = address_book.find(name)
    if record is None:
            raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    old_phone_number = record.find_phone(phone_number)
    record.edit_phone(old_phone_number.value, phone_number)
    return "Contact changed."


@input_error
def show_phone(args: list[str], address_book: AddressBook) -> str:
    name = args[0]
    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    if phone := record.find_phone(name):
        return f"{Fore.LIGHTYELLOW_EX}{phone.value}"
    raise PhoneNotFoundError("Contact not found.")


@input_error
def show_all(_: list[str], address_book: AddressBook) -> str:
    if address_book.is_empty:
        raise AddressBookError("Address Book is empty...")

    output = f"{Fore.YELLOW}CONTACTS:\n"
    for record in address_book.records:
        output += f"{Fore.LIGHTYELLOW_EX}{record.name}: {Fore.LIGHTYELLOW_EX}{record.phones}\n"
    return output.rstrip()


class Command(Enum):
    ADD = add_contact
    CHANGE = change_contact
    CLOSE = None
    EXIT = None
    HELLO = None
    PHONE = show_phone
    ALL = show_all


@input_error
def parse_input(user_input: str):
    command, *args = user_input.strip().split()
    command = command.upper()

    if command not in Command:
        raise InvalidInputError(
            f"Invalid command. Use one of commands: {', '.join([x.name.lower() for x in Command])}"
            )

    command = Command[command]

    if command in (Command.ADD, Command.CHANGE) and len(args) != 2:
        raise InvalidInputError(
            f"Your input is incorrect. You forgot additional parameters. Use: {command} <name> <phone>"
        )
    elif command == Command.PHONE and len(args) != 1:
        raise InvalidInputError(
            "Your input is incorrect. You forgot additional parameters. Use: phone <name>"
        )
    elif command == Command.ALL and len(args) != 0:
        raise InvalidInputError(
            "Your input is incorrect. Command 'all' doesn't need additional parameters."
        )

    return command, args


def main():
    print(f"{Fore.GREEN}Welcome to the assistant bot!")
    address_book = AddressBook()
    while True:
        input_command = input(f"{Fore.BLUE}Enter a command: ")
        if not input_command:
            print(f"{Fore.RED}Use one of commands: {', '.join([x.name.lower() for x in Command])}")
            continue

        parsed_input = parse_input(input_command)
        if parsed_input is None:
            continue

        command, args = parsed_input
        if command in (Command.EXIT, Command.CLOSE):
            print(f"{Fore.GREEN}Good bye!")
            break
        elif command == Command.HELLO:
            print(f"{Fore.GREEN}Hello! How can I help you?")
        else:
            result = command.value(args, address_book=address_book)
            if result is not None:
                print(f"{Fore.GREEN}{result}")


if __name__ == "__main__":
    main()