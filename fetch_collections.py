import requests


def get_collections(search_query: str) -> bool:
    """
    Fetches the collections from sunnah.com based on a search query
    """
    query = {
        "q": f"{search_query}"
    }
    url = "https://sunnah.com"
    response = requests.get(url + "/search?", params=query)
    if response.status_code == 200:
        with open('./pages/search.html', 'w', encoding='utf-8') as f:
            f.write(response.content.decode('utf-8'))
        return True
    print("Error: ", response.status_code)
    return False


def fetch_page(url: str, filename: str) -> bool:
    """
    Fetches the pages from sunnah.com based on a url
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"./pages/{filename}", 'w', encoding='utf-8') as f:
            f.write(response.content.decode('utf-8'))
        return True
    print("Error: ", response.status_code)
    return False


if __name__ == "__main__":
    get_collections("abu")
