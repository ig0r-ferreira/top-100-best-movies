import time
from pathlib import Path
from typing import Iterable

import dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

ENV_VARS: dict[str, str | None] = dotenv.dotenv_values()


def save_movies_in_file(file_path: str, movies_names: Iterable[str]) -> None:
    with open(file_path, mode='w', encoding='utf-8') as file:
        file.writelines(movies_names)


def main() -> None:
    movies_page_url = ENV_VARS.get('MOVIES_PAGE_URL', '')
    if not movies_page_url:
        return

    options = webdriver.ChromeOptions()
    # Disable GUI
    options.headless = True
    # Disable logs
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    browser = webdriver.Chrome(options=options)
    browser.get(movies_page_url)

    # Waits 3 seconds just to make sure the page will load
    time.sleep(3)

    elements = browser.find_elements(By.CSS_SELECTOR, '.listicle-item h3')
    movie_names = [f'{element.text}\n' for element in elements[::-1]]

    browser.quit()

    folder_path = ENV_VARS.get('FOLDER_PATH') or ''
    file_path = Path(folder_path) / '100-movies-to-watch.txt'
    save_movies_in_file(str(file_path), movie_names)


if __name__ == '__main__':
    main()
