from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

songs = 28
skipId = []

title = []
artist = []
youtubeList = {}
youtubeLinks = ['https://www.youtube.com/watch?v=5e1aqKrZSWQ', 'https://www.youtube.com/watch?v=otKCxvx3wik', 'https://www.youtube.com/watch?v=NTn1q6YEAPY', 'https://www.youtube.com/watch?v=iXtyqKC6W88']

options = Options()
options.add_argument("user-data-dir=C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data\\")
options.add_argument("profile-directory= Profile 1")
driver = webdriver.Chrome(executable_path=r'../drivers/chromedriver.exe', options=options)

def ShazamSongScraping():

    num = 0

    driver.get("https://www.shazam.com/myshazam?key=XAV1UHKJ88LK93W5KGNQGQQ0G")

    last_height = driver.execute_script("return document.body.scrollHeight")

    driver.execute_script("window.scrollTo(0, window.scrollY + 230)")

    time.sleep(1)



    while num < songs:
        driver.execute_script("window.scrollTo(0, window.scrollY + 143)")

        num += 1

        if num not in skipId:
            title_text = driver.find_element_by_xpath("/html/body/div[4]/div/main/div/div[2]/div/div/article/ul/li[" + str(num) + "]/article/div/div[2]/div[1]")
            artist_text = driver.find_element_by_xpath("/html/body/div[4]/div/main/div/div[2]/div/div/article/ul/li[" + str(num) + "]/article/div/div[2]/div[2]")

            title.append(title_text.text)
            artist.append(artist_text.text)

        if num == 18:
            time.sleep(1)

def SpotifyService():

    for index in range(len(title)):


        driver.get("https://open.spotify.com/search")

        time.sleep(2)

        searchboxSpotify = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/header/div[3]/div/div/input')


        searchboxSpotify.send_keys(title[index] + " " + str.split(artist[index])[0])

        time.sleep(2)

        try:
            SpotifyPlaylistCheck = driver.find_element_by_xpath('//*[@id="searchPage"]/div/div/section[1]/div/div[2]/div/div/div/div[2]/div[2]')

            if "SONG" in SpotifyPlaylistCheck.text:

                TopResult = driver.find_element_by_xpath(
                    '//*[@id="searchPage"]/div/div/section[2]/div/div[2]/div[1]/div/div/div[3]/a')

                RightClick = ActionChains(driver)
                RightClick.context_click(TopResult).perform()

                time.sleep(1)

                SaveCheck = driver.find_element_by_xpath('//*[@id="main"]/div/nav[1]/div[2]')

                if "Save" in SaveCheck.text:
                    RightClick.context_click(TopResult).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

                time.sleep(.5)

            else:
                youtubeList[title[index]] = artist[index]

        except NoSuchElementException:
            youtubeList[title[index]] = artist[index]

def YoutubeService():

    for key, value in youtubeList.items():

        driver.get("https://www.youtube.com")

        time.sleep(1)

        searchboxYoutube = driver.find_element_by_xpath(
            '//html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input')
        enter = driver.find_element_by_xpath('//*[@id="search-icon-legacy"]')


        time.sleep(1)

        searchboxYoutube.send_keys(Keys.CONTROL + "a")
        searchboxYoutube.send_keys(Keys.DELETE)

        searchboxYoutube.send_keys(key + " " + value)
        enter.click()

        time.sleep(1)

        topVid = driver.find_element_by_xpath('//*[@id="video-title"]/yt-formatted-string')

        topVid.click()

        time.sleep(1)

        youtubeLinks.append(driver.current_url)


    time.sleep(1)
    print(youtubeLinks)

def YoutubeDownload(links):

    for index in range(len(youtubeLinks)):

        driver.get('https://www.ytmp3.cc')

        time.sleep(1)

        searchboxYTMP3 = driver.find_element_by_xpath('//*[@id="input"]')
        convertBtn = driver.find_element_by_xpath('//*[@id="submit"]')


        searchboxYTMP3.send_keys(Keys.CONTROL + "a")
        searchboxYTMP3.send_keys(Keys.DELETE)

        searchboxYTMP3.send_keys(youtubeLinks[index])

        convertBtn.click()

        time.sleep(1)

        WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.LINK_TEXT, 'Download')))

        downloadBtn = driver.find_element_by_link_text('Download')

        RightClick = ActionChains(driver)
        RightClick.context_click(downloadBtn).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

        Esc = ActionChains(driver)
        Esc.send_keys(Keys.ESCAPE)

        time.sleep(1)

ShazamSongScraping()
SpotifyService()
YoutubeService()
YoutubeDownload(youtubeLinks)

driver.get('chrome://downloads/')