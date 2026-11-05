"""Entry point for the PY-Bloomberg Terminal prototype."""

import command


def main() -> None:
    print("Welcome to the PY-Bloomberg Terminal prototype!")
    print("Type HELP for commands or EXIT to quit.")
    active = True
    while active:
        try:
            cmd = input("PY-B Ter: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        active = command.parseCommand(cmd)


if __name__ == "__main__":
    main()
