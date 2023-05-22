import requests


def get_collections(parms: dict) -> bool:
    """
    Fetches the collections from sunnah.com
    """
    url = "https://sunnah.com"
    response = requests.get(url + "/search?", params=parms)
    if response.status_code == 200:
        with open('search.html', 'w') as f:
            f.write(response.content.decode('utf-8'))
        return True
    print("Error: ", response.status_code)
    return False
