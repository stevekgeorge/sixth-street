import requests

if __name__ == '__main__':

    symbol = 'msft'
    date = '2024-02-27'
    n = 10

    lookup = requests.get(f'http://127.0.0.1:5000/lookup?symbol={symbol}&date={date}')
    print(lookup)
    print(lookup.json())

    min = requests.get(f'http://127.0.0.1:5000/min?symbol={symbol}&n={n}')
    print(min.json())

    max = requests.get(f'http://127.0.0.1:5000/max?symbol={symbol}&n={n}')
    print(max.json())