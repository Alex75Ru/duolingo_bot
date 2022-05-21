import requests
from bs4 import BeautifulSoup

url = 'https://www.duolingo.com/profile/'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}

def parser(url, user_list):
    for name in user_list:
        full_url = f'{url}{name}'
        response = requests.get(url=full_url, headers=headers, timeout=(50000, 50000), read)
        soup = BeautifulSoup(response.text, "lxml")
        items = soup.find_all('div', class_='3gX7q')
        print(response.text)


