import requests
import json

response = requests.get('http://127.0.0.1:5000/cords/1,2')

response1 = requests.get('http://127.0.0.1:5000/board')

response2 = requests.get('http://127.0.0.1:5000/points')

data1 = response1.text
data2 = response2.text

y = json.loads(data1)
z = json.loads(data2)

if __name__ == '__main__':
    print(y['board'])
    print(z['points'])
    requests.get('http://127.0.0.1:5000/cords/4,3')
    response1 = requests.get('http://127.0.0.1:5000/board')
    response2 = requests.get('http://127.0.0.1:5000/points')
    data1 = response1.text
    data2 = response2.text
    y = json.loads(data1)
    z = json.loads(data2)
    print(y['board'])
    print(z['points'])