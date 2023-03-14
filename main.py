import selenium.common.exceptions
from webbot import Browser
import time
from lxml import etree
from botcity.web import WebBot
from botcity.web.browsers.chrome import default_options
from botcity.web import By


class Browser(WebBot):
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


def func(url: str):
    global bot
    bot = Browser()
    bot.browse(url)
    time.sleep(1)
    bot.kb_type("GOSSHO")
    bot.enter()
    time.sleep(1)
    bot.add_image(label="join", path='./images/join.png')
    if bot.find(label="join", matching=0.97, waiting_time=10000):
        print("This element was found!")
        bot.click_on(label="join")

    iframe = bot.find_element('/html/body/div[2]/div[4]/div[1]/iframe', By.XPATH)
    bot.enter_iframe(iframe)
    time.sleep(1)

    print(bot.find_element('/html/body/div[2]/div[2]/div[2]/div[2]/div', By.XPATH).text)

if __name__ == '__main__':
    func('https://jklm.fun/UAKW')