import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import json

print("Starting...")
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get("http://www.lan-play.com")

print("Loading...")
time.sleep(10)

print("Getting servers ip...")

data = {}
data['server'] = []


print("Writing servers file...")
try:
    for x in range(1, 20):
        ip = driver.find_element_by_xpath(
            "//tbody/tr["+str(x)+"]/td[1]/span").get_attribute("innerHTML")
        flag = driver.find_element_by_xpath(
            "//tbody/tr["+str(x)+"]/td[3]/span").get_attribute("title")
        ping = driver.find_element_by_xpath(
            "//tbody/tr["+str(x)+"]/td[5]/span").get_attribute("innerHTML")
        # servers.append(element)
        data['server'].append({
            'ip': ip,
            'flag': flag,
            'ping': ping,
        })
finally:
    driver.close()


with open('servers.json', 'w') as outfile:
    json.dump(data, outfile)


print("Done")
