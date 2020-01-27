from selenium import webdriver
from selenium.webdriver.chrome.options import Options

email_generator = "https://generator.email/"
# petition = "https://www.change.org/p/nba-2k-fire-ronnie-for-false-advertising"
# started at 31
petition = "https://www.change.org/p/alsa-long-term-care-and-vent-placement-in-west-virginia"

log = True
log_user_info = True
max_batch = 1
max_email = 2

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
        email = driver.find_element_by_id('userName').get_attribute('value')
        emails.append(str(email))
        if log:
            print('#', end="", flush=True)
        email_count += 1
        if email_count == max_email and log:
            print("", flush=False)
    if batch + 1 == max_batch:
        if log:
            print("\nSUCCESSFULLY GENERATED: " + str(len(emails)) + " EMAILS!\n\n\n")
        break
    batch += 1
    email_count += 1


email_count = 1
for email in emails:
    if email_count % 3 == 1:
        driver.quit()
        print("rebooting driver...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(petition)
    if log:
        print("generating signature " + str(email_count) + " out of " + str(len(emails)))
    first_input = driver.find_element_by_id("firstName")
    last_input = driver.find_element_by_id("lastName")
    email_input = driver.find_element_by_id("email")

    first_name, last_name = email[:len(email) // 2], email[len(email) // 2:]

    first_input.send_keys(first_name)
    last_input.send_keys(last_name)
    email_input.send_keys(str(email) + "@gmail.com")
    driver.find_element_by_xpath(
        '//*[@id="page"]/div[1]/div[3]/div[2]/div/div/div/div[2]/div[2]/form/button[2]').click()
    if log or log_user_info:
        print("user info")
        print(" first name: " + str(first_name))
        print(" last name: " + str(last_name))
        print(" email: " + str(email) + "@gmail.com\n")
    email_count += 1


driver.quit()
