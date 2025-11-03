from enum import Enum
from typing import List

from colorama import Fore

from address_book import AddressBook, Record
from exceptions import AddressBookError, InvalidInputError, RecordNotFoundError
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
def add_birthday(args: list[str], address_book: AddressBook) -> str:
    name, birthday = args
    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    message = "Birthday updated." if record.birthday is not None else "Birthday added."
    record.add_birthday(birthday)
    return message


@input_error
def show_birthday(args: list[str], address_book: AddressBook) -> str:
    name = args[0]
    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    return f"{Fore.LIGHTYELLOW_EX}{record.birthday}"


@input_error
def change_contact(args: list[str], address_book: AddressBook) -> str:
    name, old_number, new_number = args
    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    record.edit_phone(old_number, new_number)
    return "Contact changed."


@input_error
def show_phone(args: list[str], address_book: AddressBook) -> str:
    name = args[0]
    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    return f"{Fore.LIGHTYELLOW_EX}{[x.value for x in record.phones]}"


@input_error
def show_all(_: list[str], address_book: AddressBook) -> str:
    if address_book.is_empty:
        raise AddressBookError("Address Book is empty...")

    output = f"{Fore.YELLOW}CONTACTS:\n"
    for _, record in address_book.records.items():
        output += f"{Fore.LIGHTYELLOW_EX}{record.name}: {Fore.LIGHTYELLOW_EX}{[x.value for x in record.phones]}\n"
    return output.rstrip()


@input_error
def birthdays(_: list[str], address_book: AddressBook) -> str:
    output = f"{Fore.YELLOW}UPCOMING BIRTHDAYS:\n"
    for _, record in address_book.records.items():
        output += f"{Fore.LIGHTYELLOW_EX}{record.name}: {Fore.LIGHTYELLOW_EX}{record.birthday}\n"
    return output.rstrip()


class Command(Enum):
    ADD = 0, add_contact
    CHANGE = 1, change_contact
    CLOSE = 2, None
    EXIT = 3, None
    HELLO = 4, None
    PHONE = 5, show_phone
    ALL = 6, show_all
    ADD_BIRTHDAY = 7, add_birthday
    SHOW_BIRTHDAY = 8, show_birthday
    BIRTHDAYS = 9, birthdays

    def __init__(self, order, func):
        self.order = order
        self.func = func

    @classmethod
    def available_commands(cls) -> List[str]:
        return [x.name.replace("_", "-") for x in cls]


@input_error
def parse_input(user_input: str):
    command, *args = user_input.strip().split()
    command = command.upper()

    if command not in Command.available_commands():
        raise InvalidInputError(
            f"Invalid command. Use one of commands: {', '.join(Command.available_commands())}"
        )

    command = Command[command.replace("-", "_")]

    if command in (Command.ADD, Command.ADD_BIRTHDAY) and len(args) != 2:
        use_params = (
            f"Use: {command.name} <name> <phone>"
            if command.ADD
            else f"Use: {command.name} <name> <birthday>"
        )
        raise InvalidInputError(
            f"Your input is incorrect. You forgot additional parameters. {use_params}"
        )
    elif command == Command.CHANGE and len(args) != 3:
        raise InvalidInputError(
            f"Your input is incorrect. You forgot additional parameters. Use: {command.name} "
            f"<name> <old_phone_number> <new_phone_number>"
        )
    elif command in (Command.PHONE, Command.SHOW_BIRTHDAY) and len(args) != 1:
        use_params = (
            f"Use: {command.name} <name>"
            if command.PHONE
            else f"Use: {command.name} <name>"
        )
        raise InvalidInputError(
            f"Your input is incorrect. You forgot additional parameters. {use_params}"
        )
    elif command in (Command.ALL, Command.BIRTHDAYS) and len(args) != 0:
        raise InvalidInputError(
            f"Your input is incorrect. Commands '{Command.ALL}' and '{Command.BIRTHDAYS}' doesn't need additional parameters."
        )

    return command, args


def main():
    print(f"{Fore.GREEN}Welcome to the assistant bot!")
    address_book = AddressBook()
    while True:
        input_command = input(f"{Fore.BLUE}Enter a command: ")
        if not input_command:
            print(
                f"{Fore.RED}Use one of commands: {', '.join(Command.available_commands())}"
            )
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
            result = command.func(args, address_book=address_book)
            if result is not None:
                print(f"{Fore.GREEN}{result}")


if __name__ == "__main__":
    main()
