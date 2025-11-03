from colorama import Fore


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (TypeError, ValueError) as e:
            error_message = str(e)
            if "_contact" in error_message:
                error_message = error_message.replace("_contact", "")
            if "show_" in error_message:
                error_message = error_message.replace("show_", "")
            if "()" in error_message:
                error_message = error_message.replace("()", "")
            print(f"{Fore.RED}{error_message}")
            return None

    return inner
