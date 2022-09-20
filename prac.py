
def remove_space(command):
    if command == "":
        return command
    if command[0]==" " or command[0]=="\t":
        return remove_space(command[1:])
    elif command[-1]==" " or command[-1]=="\t":
        return remove_space(command[:-1])
    else:
        return command

def user_command(pwd):
    valid = True
    temp = input(pwd)
    temp = temp.strip("\t")
    valid_list = [",","-","_","\""," ", "+","=",".","/","\t","\n","\r","\v"]
    quote = False
    i = 0
    start = 0
    command = []
    while i < len(temp):
        if not(temp[i].isalpha()) and not(temp[i].isnumeric()) and not(temp[i] in valid_list):
            valid = False
        elif quote:
            if temp[i] == "\"":
                quote = False
                command.append(temp[start:i])
                start = i + 2
        else:
            if temp[i] == "\"":
                quote = True
                start = i + 1
            elif temp[i].isspace():
                command.append(temp[start:i])
                start = i + 1
        i += 1
    command.append(temp[start:])

    j = 0
    while j < len(command):
        if command[j] == "":
            command.pop(j)
        else:
            command[j] = remove_space(command[j])
            j+=1

    if not valid:
        return command[0], valid
    return command, valid

a = user_command(":")
print(a)
print(len(a[0]))