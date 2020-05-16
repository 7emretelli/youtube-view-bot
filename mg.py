#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import os
import zipfile
import codecs


print("""
Youtube izlenme aracına hoşgeldiniz...

YT Viewer v2

""")


def get_chromedriver(use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(
        os.path.join(path, 'chromedriver'),
        chrome_options=chrome_options)
    return driver


def creator(terim, link, sure):
    browser = get_chromedriver(use_proxy=True)
    try:

        print(terim)

        browser.get("https://youtube.com/")
        time.sleep(5)

        search = browser.find_element_by_xpath(
            "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input")
        search.send_keys(terim)
        time.sleep(3)

        ara = browser.find_element_by_xpath("//*[@id='search-icon-legacy']")

        ara.click()

        time.sleep(3)

        vid = browser.find_element_by_xpath("//a[@href='/watch?v="+link+"']")

        time.sleep(3)

        vid.click()

        browser.set_window_position(-10000, 0)

        time.sleep(sure)

        browser.close()

        print("cooldown vakti")

        time.sleep(10)
    except Exception as e:
        browser.close()
        print(e)
        print("Hata alındı tekrar deneniyor")
        creator(terim, link, sure)


# with codecs.open("./Data/terim.txt", "r", encoding='utf-8', errors='ignore') as f:
#    terim = f.readlines()
#terim = terim[0]
# print(terim)

# with codecs.open("./Data/link.txt", "r", encoding='utf-8', errors='ignore') as f:
#    link = f.readlines()
# link = link[0]
# print(link)


with open("./Data/proxies.txt", 'r') as f:
    c_proxies = f.readlines()
    line = len(c_proxies)

terim = raw_input("Arama terimi:")
terim = terim.decode('utf-8')
link = raw_input("link:")
tekrar = int(raw_input("Kaç tekrar olsun?"))
sure = int(raw_input("İzleme süresi(Videodan kısa olmalı)(saniye):"))


a = 0

for i in range(0, tekrar):

    if a == line:
        a = 0
    if a < line:
        pieces = c_proxies[a].split(":")
        host = pieces[0]
        port = pieces[1]
        kadi = pieces[2]
        passw = pieces[3]

        a += 1

    PROXY_HOST = host  # rotating proxy or host
    PROXY_PORT = port  # port
    PROXY_USER = kadi  # username
    PROXY_PASS = passw.replace("\n", "")  # password

    print(PROXY_HOST+"-"+PROXY_PORT+"-"+PROXY_USER +
          "-"+PROXY_PASS+"tekrar: "+str(i))

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    creator(terim, link, sure)
