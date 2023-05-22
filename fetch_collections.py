import requests


url = "https://sunnah.com"

params = {
    'q': 'Ibn Majah',
}
response = requests.get(url + "/search?", params=params)

with open('search.html', 'w') as f:
    f.write(response.content.decode('utf-8'))


def get_collections(parms: dict) -> bool:
    response = requests.get(url + "/search?", params=params)
    if response.status_code == 200:
        with open('search.html', 'w') as f:
            f.write(response.content.decode('utf-8'))
        return True
    print("Error: ", response.status_code)
    return False
