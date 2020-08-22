from pathlib import Path

from renderer import render
from scraper import scrape

if __name__ == '__main__':
    render(scrape(Path('botdata - history.csv'), True))
