import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

email_generator = "https://generator.email/"
location_generator = "https://www.randomlists.com/random-zip-codes"
# petition = "https://www.change.org/p/nba-2k-fire-ronnie-for-false-advertising"
# started at 31
petition = "https://www.change.org/p/alsa-long-term-care-and-vent-placement-in-west-virginia"

log = True
log_user_info = True
max_batch = 5
max_email = 20

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

driver.get(email_generator)
emails = []
batch = 0

while True:
    email_count = 0
    if log:
        print("\nbatch: " + str(batch + 1))
        print("generating emails...")
    while email_count < max_email:
        driver.find_element_by_xpath("/html/body/div[3]/div/div/p/a[1]/button").click()
        email_1 = driver.find_element_by_id('userName').get_attribute('value')
        email_2 = driver.find_element_by_xpath('//*[@id="domainName2"]').get_attribute('value')
        email = str(email_1) + '@' + str(email_2)
        emails.append(email)
        if log:
            print('#', end="", flush=True)
        email_count += 1
        if email_count == max_email and log:
            print("", flush=False)
    if batch + 1 == max_batch:
        if log:
            print("\ngenerated " + str(len(emails)) + " emails\n\n\n")
        break
    batch += 1
    email_count += 1

driver.quit()
email_count = 1
for email in emails:
    driver = webdriver.Chrome(options=chrome_options)
    location_randomizer = webdriver.Chrome(options=chrome_options)
    driver.get(petition)
    location_randomizer.get(location_generator)

    if log:
        print("generating signature " + str(email_count) + " out of " + str(len(emails)))
    first_input = driver.find_element_by_id("firstName")
    last_input = driver.find_element_by_id("lastName")
    email_input = driver.find_element_by_id("email")
    name = email.partition('@')[0]
    first_name, last_name = email[:len(name) // 2], email[len(name) // 2:]

    first_input.send_keys(first_name)
    last_input.send_keys(last_name)
    email_input.send_keys(str(email))
    driver.find_element_by_xpath('//*[@id="public"]').click()  # don't show info

    driver.find_element_by_xpath('//*[@id="page"]/div[1]/div[3]/div[2]/div/div/div/div[2]/div[2]/form/button[1]/div/div/div[2]/div/div/div').click()  # open location editor
    Select(driver.find_element_by_xpath('//*[@id="countryCode"]')).select_by_value('US')
    zip_code = location_randomizer.find_element_by_xpath('/html/body/div/div[1]/main/article/div[2]/ol/li[1]/span[1]').text
    city_state = str(location_randomizer.find_element_by_xpath('/html/body/div/div[1]/main/article/div[2]/ol/li[1]/span[2]').text).partition(', ')
    state = city_state[2]
    city = city_state[0]
    Select(driver.find_element_by_xpath('//*[@id="stateCode"]')).select_by_visible_text(state)
    driver.find_element_by_xpath('//*[@id="city"]').send_keys(city)
    driver.find_element_by_xpath('//*[@id="postalCode"]').send_keys(zip_code)
    driver.find_element_by_xpath('//*[@id="page"]/div[1]/div[3]/div[2]/div/div/div/div[2]/div[2]/form/button').click()  # submit
    if log or log_user_info:
        print("user info")
        print(" first name: " + str(first_name))
        print(" last name: " + str(last_name))
        print(" email: " + str(email))
        print(" state: " + str(state))
        print(" zip: " + str(zip_code))
        print(" city: " + str(city) + "\n")
    email_count += 1

    time.sleep(random.randrange(10) + 3)
    driver.quit()
    location_randomizer.quit()
    print("rebooting driver...")
