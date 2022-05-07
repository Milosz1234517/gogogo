# import requests
import json


class Menu:
    def __init__(self):

        self.playerNick = input("Podaj swój nick:\n")
        # można tu sprawdzić czy nick zajęty

    def menu0(self):
        while True:
            choice = int(input("1.Make new game\n2.doloncz do gry\n3.Exit\n"))
            if (choice == 1):
                print("xd")
                # request z stworzeniem gry
            elif (choice == 2):
                print("xd")
                self.menu2()


            elif (choice == 3):
                break

    def menu2(self):
        gamenumber = 22  # tu sprawdzamy liste gier
        choice=-1
        if (gamenumber < 1):
            print("Brak Dostępnych gier")
        else:
            while True:
                for i in range(gamenumber):
                    print(i)  # printowanie gier
                choice = int(input("Wybierz numer gry\n"))
                if (choice < gamenumber and choice >= 0):
                    break
                else:
                    print("Błąd")
            #request z dołączeniem do gry
            odp=True
            if (odp):
                print("dołączam")
            else:
                print("Gra Zajęta")





# response = requests.get('http://127.0.0.1:5000/cords/1,2')
#
# response1 = requests.get('http://127.0.0.1:5000/board')
#
# response2 = requests.get('http://127.0.0.1:5000/points')
#
# data1 = response1.text
# data2 = response2.text
#
# y = json.loads(data1)
# z = json.loads(data2)

if __name__ == '__main__':
    # print(y['board'])
    # print(z['points'])
    # requests.get('http://127.0.0.1:5000/cords/4,3')
    # response1 = requests.get('http://127.0.0.1:5000/board')
    # response2 = requests.get('http://127.0.0.1:5000/points')
    # data1 = response1.text
    # data2 = response2.text
    # y = json.loads(data1)
    # z = json.loads(data2)
    # print(y['board'])
    # print(z['points'])

    m = Menu()
    print(m.playerNick)
    m.menu0()
