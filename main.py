import time
import requests
import string
import random
from botcity.web import WebBot, Browser
from botcity.web.browsers.chrome import default_options
from botcity.web import By

USER = "GOSHO"
WORDS_CACHE = dict()
USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
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

        def_options.add_argument("--incognito")
        self.options = def_options


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


def func(url: str):
    global bot
    bot = MyBrowser()
    bot.browse(url)
    time.sleep(1)
    global USER
    USER += id_generator(size=3)
    bot.kb_type(USER)
    bot.enter()
    time.sleep(1)
    bot.add_image(label="join", path='./images/join.png')
    if bot.find(label="join", matching=0.97, waiting_time=10000):
        print("This element was found!")
        bot.click_on(label="join")

    iframe = bot.find_element('/html/body/div[2]/div[4]/div[1]/iframe', By.XPATH)
    bot.enter_iframe(iframe)
    time.sleep(3)

    while True:
        turn = bot.find_element('/html/body/div[2]/div[3]/div[2]/div[1]/span[1]', By.XPATH).text
        if turn == "":
            syllable = bot.find_element('/html/body/div[2]/div[2]/div[2]/div[2]/div', By.XPATH).text
            word = get_word(syllable)
            print(word)
            bot.kb_type(word)
            bot.enter()
        winner = bot.find_element('/html/body/div[2]/div[2]/div[2]/div[3]/div/div[2]', By.XPATH).text
        if winner != '':
            break
        time.sleep(1)


if __name__ == '__main__':
    url = input()
    func(url)
