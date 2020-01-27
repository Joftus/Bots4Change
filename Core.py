import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

email_generator = "https://generator.email/"
# petition = "https://www.change.org/p/nba-2k-fire-ronnie-for-false-advertising"
# started at 31
petition = "https://www.change.org/p/alsa-long-term-care-and-vent-placement-in-west-virginia"

log = True
log_user_info = True
stats = False       # currently broken
max_batch = 2
max_email = 10
sleep_time = 1

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

driver.get(email_generator)
emails = []
batch = 0
while True:
    email_count = 0
    try:
        if log:
            print("\nbatch: " + str(batch + 1))
            print("generating emails...")
        while email_count < max_email:
            driver.find_element_by_xpath("/html/body/div[3]/div/div/p/a[1]/button").click()
            email = driver.find_element_by_id('userName').get_attribute('value')
            emails.append(str(email))
            if log:
                print('#', end="", flush=True)
            email_count += 1
            if email_count == max_email and log:
                print("", flush=False)
        if batch == max_batch:
            if log:
                print("\nSUCCESSFULLY GENERATED: " + str(len(emails)) + " EMAILS!\n\n\n")
            break
        batch += 1
    except Exception as e:
        if log:
            print("\nHANDELING EXCEPTION [BLOCK 1]")
            print(e)
            time.sleep(sleep_time * 5)
        email_count += 1

starting_amount = 0
if stats:
    driver.get(petition)
    starting_amount = str(driver.find_element_by_xpath(
        '//*[@id="page"]/div[1]/div[3]/div[2]/div/div/div/div[2]/div[1]/p/span').text)
email_count = 1
for email in emails:
    if log:
        print("generating signature " + str(email_count) + " out of " + str(len(emails)))
    driver.get(petition)
    if log:
        print("\nsleeping for " + str(sleep_time) + " seconds...")
    time.sleep(sleep_time)
    try:
        driver.switch_to.alert.dismiss()
        if log:
            print("alert removed...")
            print("page is now ready...")
    except Exception:
        print("page ready...")

    try:
        first_input = driver.find_element_by_id("firstName")
        last_input = driver.find_element_by_id("lastName")
        email_input = driver.find_element_by_id("email")

        first_name, last_name = email[:len(email) // 2], email[len(email) // 2:]

        first_input.send_keys(first_name)
        last_input.send_keys(last_name)
        email_input.send_keys(str(email) + "@gmail.com")
        driver.find_element_by_xpath(
            '//*[@id="page"]/div[1]/div[3]/div[2]/div/div/div/div[2]/div[2]/form/button[2]').click()
        if log and log_user_info:
            print("user info")
            print(" first name: " + str(first_name))
            print(" last name: " + str(last_name))
            print(" email: " + str(email) + "@gmail.com")
    except Exception as e:
        if log:
            print("failed to forge user signature!")
            # print("\nHANDELING EXCEPTION [BLOCK 2]")
            # print(e)
    email_count += 1

if stats:
    try:
        driver.get(petition)
        ending_amount = str(driver.find_element_by_xpath(
            '//*[@id="page"]/div[1]/div[3]/div[2]/div/div/div/div[2]/div[1]/p/span').text)
        if stats:
            print("\n\noriginal signature count: " + str(starting_amount).partition(" ")[0])
            print("final signature count: " + str(ending_amount).partition(" ")[0])
    except Exception as e:
        if log:
            print("\nHANDELING EXCEPTION [BLOCK 3]")
            print(e)
            time.sleep(sleep_time * 5)

driver.quit()
