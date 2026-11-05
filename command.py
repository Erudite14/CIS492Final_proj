"""Parse and execute user commands for the terminal prototype."""

import display


def parseCommand(command: str) -> bool:
    """Process a command; return False when the user wants to exit."""
    cmd = command.strip().upper()
    if cmd in ("EXIT", "QUIT"):
        print("Goodbye!")
        return False
    executeCommand(cmd)
    return True


def executeCommand(cmd: str) -> None:
    """Run the requested terminal feature, or explain what is still planned."""
    if cmd == "HELP":
        print("Commands: HELP, STOCKS, BOND, CASH, COMMODITIES, STATE, EXIT")
    elif cmd == "STOCKS":
        display.displayInfo()
    elif cmd in ("BOND", "CASH", "COMMODITIES", "STATE"):
        print(f"{cmd} is planned but is not implemented in this prototype.")
    elif cmd == "":
        return
    else:
        print("Unknown command. Type HELP to see available commands.")
