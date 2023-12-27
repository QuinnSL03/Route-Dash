from operator import itemgetter

def get_balance(id):
    line = None
    balance = None
    with open("data.text") as file:
        while True:
            line = file.readline()
            if str(id) in line:
                break
            if not(line):
                print("ID not found, try again.")
                return -1
                exit()
        balance = line[line.index(":")+1:line.index("-")]
    return balance

def write_balance(id, bal):
    line = None
    lines = None

    data = str(id) + ";" + str(bal) + "-"
    
    #Find line that contains this account
    with open("data.text", "r") as file:
        lines = file.readlines()
        counter = 0
        while True:
            line = lines[counter][:lines[counter].index(":")]
            if id in line:
                break
            counter += 1
        lines[counter] = data + "\n"
    
    #Write data
    with open("data.text", "w") as file:
        for line in lines:
            file.write(line)

def write_new_users(users):
    with open("data.text", "w") as file:
        file.write(users)

def sort_bals():
    sorted_data = []
    data = ""
    with open("data.text", "r") as file:
        while True:
            line = file.readline()
            if not(line):
                print("End")
                break
            sorted_data.append([line[:line.index(":")],int(line[line.index(":")+1:line.index("-")])])
        sorted_data = sorted(sorted_data, reverse=True, key=itemgetter(1))
        for d in sorted_data:
            data += str(d[0]) + ":" + str(d[1]) + "-\n"
    with open("data.text", "w") as file:
        file.write(data)
        
def return_board():
    with open("data.text", "r") as file:
        data += file.readlines()


