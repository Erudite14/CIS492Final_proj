from . import command


print("Welcome to the PY-Bloomberg Terminal !")
active = True
while active == True:
    cmd = input("PY-B Ter: ")
    command.parseCommand(cmd)
    if cmd == "exit":
        active = False
    print(f"Hello {name}")