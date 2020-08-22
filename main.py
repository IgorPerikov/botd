from renderer import render
from scraper import scrape

if __name__ == '__main__':
    render(scrape('botdata - history.csv', True))
