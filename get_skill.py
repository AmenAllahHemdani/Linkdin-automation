import json

def verif(num,list):
    if num > len(list):
        return True
    return False

def get_skill():
    file = "skills.json"
    with open(file, "rb") as file:
        data = json.load(file)
    
    for i,item in enumerate(data.keys()):
            print(i+1,' : ',item)
    num = int(input("\nYour choice : "))
    while verif(num,data.keys()):
        num = int(input("try again Your choice : "))

    key, value = list(data.items())[num-1]

    print('\n\n',key+": \n")
    for i,item in enumerate(value):
            print(i+1,': ',item)

    num = int(input("\nYour choice : "))
    while verif(num,value):
        num = int(input("try again Your choice : "))
    
    return value[num-1]
