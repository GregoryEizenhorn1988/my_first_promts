import argparse
import string
import sys
from secrets import choice
from typing import List


DEFAULT_LENGTH = 12


def positive_int(value: str) -> int:
    """Parse a positive integer for CLI arguments.

    Raises ArgumentTypeError if the value is not a positive integer.
    """
    try:
        parsed_value = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(f"invalid int value: {value}") from error
    if parsed_value < 1:
        raise argparse.ArgumentTypeError("length must be >= 1")
    return parsed_value


def build_character_pool(include_numbers: bool, include_symbols: bool) -> str:
    """Build the pool of characters to sample from.

    Letters are always included. Numbers/symbols are included if requested.
    """
    pool_parts: List[str] = [string.ascii_letters]
    if include_numbers:
        pool_parts.append(string.digits)
    if include_symbols:
        pool_parts.append(string.punctuation)
    return "".join(pool_parts)


def generate_password(length: int, include_numbers: bool, include_symbols: bool) -> str:
    """Generate a password using a cryptographically secure RNG."""
    character_pool = build_character_pool(include_numbers, include_symbols)
    if not character_pool:
        # Should never happen since letters are always included
        raise ValueError("Character pool is empty")
    return "".join(choice(character_pool) for _ in range(length))


def append_password_to_file(password: str, file_path: str) -> None:
    """Append the generated password to the given file (one per line)."""
    with open(file_path, "a", encoding="utf-8") as file_handle:
        file_handle.write(password + "\n")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple command-line password generator")
    parser.add_argument(
        "-l",
        "--length",
        type=positive_int,
        default=DEFAULT_LENGTH,
        help=f"Length of the password (default: {DEFAULT_LENGTH})",
    )
    parser.add_argument(
        "-n",
        "--numbers",
        action="store_true",
        help="Include numbers (0-9)",
    )
    parser.add_argument(
        "-s",
        "--symbols",
        action="store_true",
        help="Include symbols (punctuation)",
    )
    parser.add_argument(
        "--save",
        metavar="FILE",
        help="Append generated password to FILE",
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    password = generate_password(args.length, args.numbers, args.symbols)
    print(password)
    if args.save:
        try:
            append_password_to_file(password, args.save)
        except OSError as error:
            print(f"Failed to save password to {args.save}: {error}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))