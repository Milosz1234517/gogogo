import requests
import json
import time

turn = 2


def createGame(nick):
    response = requests.get('http://127.0.0.1:5000/create/' + nick)
    data = response.text
    return json.loads(data)['gameId']


def joinGame(nick):
    response = requests.get('http://127.0.0.1:5000/join/' + nick)
    data = response.text
    return json.loads(data)['gameId']


def mainMenu():
    nick = input("Insert nick\n")
    while True:
        choice = int(input("1.Make new game\n2.doloncz do gry\n3.Exit\n"))
        if choice == 1:
            gameID = createGame(nick)
            inGameMenu(gameID, 2)

        elif choice == 2:
            gameID = joinGame(nick)
            inGameMenu(gameID, 1)

        elif choice == 3:
            break


def inGameMenu(gameID, color):
    while True:
        response = requests.get('http://127.0.0.1:5000/onGoing/' + str(gameID))
        data = response.text
        if not json.loads(data)['onGoing']:
            response = requests.get('http://127.0.0.1:5000/leave/' + str(gameID))
            data = response.text
            print(json.loads(data)['remove'])
            break

        response = requests.get('http://127.0.0.1:5000/checkT/' + str(gameID))
        data = response.text

        if int(json.loads(data)['turn']) == 1:
            print("White player turn")
        else:
            print("Black player turn")

        if int(json.loads(data)['turn']) == color:
            response = requests.get('http://127.0.0.1:5000/board/' + str(gameID))
            data = response.text
            print(json.loads(data)['board'])

            choice = int(input("1.Wstaw\n2.Pass\n3.Wycofaj\n"))
            if choice == 1:
                x = input("x:\n")
                y = input("y:\n")
                response = requests.get('http://127.0.0.1:5000/cords/' + x + ',' + y + ',' + str(gameID))
                data = response.text
                print(json.loads(data)['response'])
            elif choice == 2:
                response = requests.get('http://127.0.0.1:5000/pass/' + str(gameID))
                data = response.text
                if int(json.loads(data)['passCounter']) == 2:
                    break
            elif choice == 3:
                response = requests.get('http://127.0.0.1:5000/leave/' + str(gameID))
                data = response.text
                print(json.loads(data)['remove'])
                break

            response = requests.get('http://127.0.0.1:5000/board/' + str(gameID))
            data = response.text
            print(json.loads(data)['board'])

        else:
            choice = int(input("1.Odswierz stan gry\n2.wycofaj sie\n"))
            if choice == 1:
                print("Checking...")
            elif choice == 2:
                response = requests.get('http://127.0.0.1:5000/leave/' + str(gameID))
                data = response.text
                print(json.loads(data)['remove'])
                break


if __name__ == '__main__':
    mainMenu()
