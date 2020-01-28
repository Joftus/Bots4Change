import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

email_generator = "https://www.randomlists.com/email-addresses"
location_generator = "https://www.randomlists.com/random-zip-codes"
# Jack's 2K Target
# petition = "https://www.change.org/p/nba-2k-fire-ronnie-for-false-advertising"
petition = "https://www.change.org/p/world-health-organization-change-the-coronavirus-name-to-the-kung-flu"

log = False             # Track Program Progress
users = False   # View Info Generated
timing = True           # Time to Execute Block
progress = True     # Visual
gen = True              # Basic Markers
max_email = 15

start_time = time.time()
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)
emails = []


# Complie email list
if gen:
    print("\ngenerating emails...")
email_start_time = time.time()
driver.get(email_generator)
driver.find_element_by_xpath('//*[@id="rand_options_qty"]').clear()
driver.find_element_by_xpath('//*[@id="rand_options_qty"]').send_keys(max_email)
driver.find_element_by_xpath('/html/body/div/div[1]/main/article/div[3]/aside/p/button').click()
email_lst = driver.find_elements_by_tag_name("li")
count = 0
for email in email_lst:
    if 4 < count < len(email_lst) - 6:
        emails.append(email.text)
    count += 1
if log:
    print(str(len(emails)) + " emails generated\n\n\n")
driver.close()
if timing:
    print("  emails generated in " + str(time.time() - email_start_time) + " seconds!")
    print("  avg: " + str((time.time() - email_start_time) / len(emails)) + " seconds per email.")


# Compile location list and sub-elements
if gen:
    print("generating locations...")
location_start_time = time.time()
location_randomizer = webdriver.Chrome(options=chrome_options)
location_randomizer.get(location_generator)
location_randomizer.find_element_by_xpath('//*[@id="rand_options_qty"]').clear()
location_randomizer.find_element_by_xpath('//*[@id="rand_options_qty"]').send_keys(len(emails))
location_randomizer.find_element_by_xpath('/html/body/div/div[1]/main/article/div[3]/aside/p/button').click()
zip_codes = location_randomizer.find_elements_by_class_name("rand_large")
cities_states = location_randomizer.find_elements_by_class_name("rand_medium")
if timing:
    print("  locations generated in " + str(time.time() - location_start_time) + " seconds!")
    print("  avg: " + str((time.time() - location_start_time) / len(zip_codes)) + " seconds per location.")


# Post generated info to Change.org petition
if gen:
    print("posting to website...")
posting_start_time = time.time()
email_count = 0
for email in emails:
    if progress and (email_count + 1) % 10 == 0:
        print('#')
    elif progress:
        print('#', end="", flush=True)
    if log and email_count == 0:
        print("booting up driver...")
    elif log:
        print("rebooting driver...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(petition)
    if log:
        print("generating signature " + str(email_count + 1) + " out of " + str(len(emails)))
    first_input = driver.find_element_by_id("firstName")
    last_input = driver.find_element_by_id("lastName")
    email_input = driver.find_element_by_id("email")
    name = email.partition("@")[0]
    first_name, last_name = name[:len(name) // 2], name[len(name) // 2:]

    first_input.send_keys(first_name)
    last_input.send_keys(last_name)
    email_input.send_keys(str(email))
    driver.find_element_by_xpath('//*[@id="public"]').click()  # don't show info

    driver.find_element_by_xpath('//*[@id="page"]/div[1]/div[3]/div[2]/div/div/div/div[2]/div[2]/form/button[1]/div/div/div[2]/div/div/div').click()  # open location editor
    Select(driver.find_element_by_xpath('//*[@id="countryCode"]')).select_by_value('US')
    zip_code = zip_codes[email_count].text
    city_state = str(cities_states[email_count].text).partition(', ')
    state = city_state[2]
    city = city_state[0]
    Select(driver.find_element_by_xpath('//*[@id="stateCode"]')).select_by_visible_text(state)
    driver.find_element_by_xpath('//*[@id="city"]').send_keys(city)
    driver.find_element_by_xpath('//*[@id="postalCode"]').send_keys(zip_code)

    driver.find_element_by_xpath('//*[@id="page"]/div[1]/div[3]/div[2]/div/div/div/div[2]/div[2]/form/button').click()  # submit
    if users:
        print("USER " + str(email_count + 1))
        print(" first name: " + str(first_name))
        print(" last name: " + str(last_name))
        print(" email: " + str(email))
        print(" state: " + str(state))
        print(" zip: " + str(zip_code))
        print(" city: " + str(city) + "\n")
    email_count += 1
    driver.close()
location_randomizer.close()
if timing:
    print("", flush=False)
    print("  posting completed in " + str(time.time() - posting_start_time) + " seconds!")
    print("  avg: " + str((time.time() - posting_start_time) / len(emails)) + " seconds per signature.")

if gen:
    if not timing:
        print("", flush=False)
    print(str(len(emails)) + " signatures forged in " + str(time.time() - start_time) + " seconds!")


'''
Runtime
 10 entries
    - 
    - 
    -  
'''
