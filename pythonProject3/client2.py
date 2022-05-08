import requests
import json
import time

turn = 2

def createGame():
    response = requests.get('http://127.0.0.1:5000/create')
    data = response.text
    return json.loads(data)['gameId']


def joinGame():
    response = requests.get('http://127.0.0.1:5000/join')
    data = response.text
    return json.loads(data)['gameId']


def mainMenu():
    while True:
        choice = int(input("1.Make new game\n2.doloncz do gry\n3.Exit\n"))
        if choice == 1:
            gameID = createGame()
            inGameMenu(gameID, 2)

        elif choice == 2:
            gameID = joinGame()
            inGameMenu(gameID, 1)

        elif choice == 3:
            break


def inGameMenu(gameID, color):
    while True:
        response = requests.get('http://127.0.0.1:5000/checkT/' + str(gameID))
        data = response.text
        if not int(json.loads(data)['onGoing']):
            requests.get('http://127.0.0.1:5000/leave/' + str(gameID))
        response = requests.get('http://127.0.0.1:5000/checkT/' + str(gameID))
        data = response.text
        if int(json.loads(data)['turn']) == color:
            response = requests.get('http://127.0.0.1:5000/board/' + str(gameID))
            data = response.text
            print(json.loads(data)['board'])
            choice = int(input("1.Wstaw\n2.wycofaj sie\n"))
            if choice == 1:
                x = input("x:\n")
                y = input("y:\n")
                requests.get('http://127.0.0.1:5000/cords/' + x + ',' + y + ',' + str(gameID))
        else:
            choice = int(input("1.Odswierz stan gry\n2.wycofaj sie\n"))
            if choice == 1:
                print("Checking...")
            elif choice == 2:
                response = requests.get('http://127.0.0.1:5000/leave/' + str(gameID))
                data = response.text
                break


if __name__ == '__main__':
    mainMenu()
