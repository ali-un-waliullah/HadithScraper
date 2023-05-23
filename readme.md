# Hadith Scraper

## About

This is a simple scraper that scrapes hadith from [Sunnah.com](https://sunnah.com/). It is written in Python and uses the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library to scrape the hadith. The hadith are then stored in a JSON file.

## Usage

To use this scraper, you must have Python 3 installed. You can download it [here](https://www.python.org/downloads/).

- You must also have the BeautifulSoup library installed.
- You can install it by running the following command in your terminal:

```bash
pip install pipenv
pipenv install
```

To run the scraper, run the following command in your terminal:

```bash
python3 main.py "search query" -o
```

All the hadith collections will be stored in json files in the `collections` folder.

## Contributing

To contribute to this project, fork this repository and make a pull request. Make sure to describe your changes in the pull request.
