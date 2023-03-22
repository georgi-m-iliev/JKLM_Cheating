import time
import requests
import string
import random
import json

import selenium.common.exceptions
from botcity.web import WebBot, Browser
from botcity.web.browsers.chrome import default_options
from botcity.web import By

USER = "GOSHO"
WORDS_CACHE = dict()
USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/111.0.0.0 Safari/537.36'
}


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class MyBrowser(WebBot):
    def action(self, execution=None):
        self.headless = False
        self.browser = Browser.CHROME

        def_options = default_options(
            headless=self.headless,
            download_folder_path=self.download_folder_path,
            user_data_dir=None
        )

        self.options = def_options


# Function for reading words from file
def load_words(words: dict, path: str = 'dict.json'):
    try:
        file = open(file=path, encoding='utf-8')
        words = json.load(file)
        file.close()
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        pass


# # Function for saving words from file
def save_words(words: dict, path: str = 'dict.json'):
    file = open(file=path, encoding='utf-8', mode='w')
    file.write(json.dumps(words))
    file.close()


# Function that returns unused word containing a syllable
def get_word(syllable: str) -> str:
    if syllable not in WORDS_CACHE.keys():
        data = requests.get(
            url='https://api.datamuse.com/words?sp=*{0}*'.format(syllable),
            headers=USER_AGENT
        ).json()

        words = list()
        for item in data:
            words.append(item['word'])

        WORDS_CACHE[syllable] = dict()
        WORDS_CACHE[syllable]["words"] = words
        WORDS_CACHE[syllable]["last"] = 0
    else:
        WORDS_CACHE[syllable]["last"] += 1

    return WORDS_CACHE[syllable]["words"][WORDS_CACHE[syllable]["last"]]


def spawn_browser(url: str):
    global bot
    bot = MyBrowser()
    bot.browse(url)
    time.sleep(1)
    global USER
    # USER += id_generator(size=3)
    bot.kb_type(USER)
    bot.enter()
    time.sleep(1)

    iframe = bot.find_element('/html/body/div[2]/div[4]/div[1]/iframe', By.XPATH)
    bot.enter_iframe(iframe)
    time.sleep(3)

    clicked_join = False
    winner_showed = False
    while True:
        status = bot.find_element('/html/body/div[2]/div[1]/div/header', By.XPATH)
        if status.location['x'] != 0 and status.location['y'] != 0 and clicked_join is False:
            print("Status found!")
            join = bot.find_element('/html/body/div[2]/div[3]/div[1]/div[1]/button', By.XPATH)
            if join:
                print("Join button found!!!!!")
                try:
                    join.click()
                    clicked_join = True
                    winner_showed = False
                except selenium.common.exceptions.ElementNotInteractableException:
                    pass
        if winner_showed is False:
            winner = bot.find_element('/html/body/div[2]/div[2]/div[2]/div[3]/div/div[2]', By.XPATH)
            if winner.location['x'] != 0 and winner.location['y'] != 0:
                print("The winner is: " + winner.text)
                winner_showed = True
                continue
        print("Waiting for turn")
        turn = bot.find_element('/html/body/div[2]/div[3]/div[2]/div[1]/span[1]', By.XPATH)
        if turn.location['x'] == 0 and turn.location['y'] == 0 and status.location['x'] == status.location['y'] == 0:
            syllable = bot.find_element('/html/body/div[2]/div[2]/div[2]/div[2]/div', By.XPATH).text
            word = get_word(syllable)
            print(word, sep=' ')
            bot.kb_type(word, interval=random.randint(0, 10))
            bot.enter()
            clicked_join = False
        time.sleep(1)


def main():
    load_words(WORDS_CACHE)
    try:
        spawn_browser(input())
    finally:
        save_words(WORDS_CACHE)


if __name__ == '__main__':
    main()
