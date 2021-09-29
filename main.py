"""
Script to automatically book a gym slot based on the config in `config.json`.
Booking opens 3 hours before entry.

In the parent directory you should have a file `config.json` which is
structured as follows. Please fill in the student_number
and time_slot fields with your prefered values.

{
    "url" : "https://hub.ucd.ie/usis/W_HU_MENU.P_PUBLISH?p_tag=GYMBOOK",
    "student_number" : "STUDENT_NUMBER",
    "time_slot" : "09:30"
}
"""

# TODO: Clean up main script to functions
#       Write general sleep_time function
#       Main function
#       Test runtime and speedup


import os
import json
import time
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def check_gym_times(time_slot, driver, override=False):
    for i in range(1, 6):
        if check_timeslot(i, time_slot, driver):
            if check_gym(i, driver, override):
                if check_available(i, driver):
                    return True


def check_timeslot(i, time_slot, driver):
    row_time = driver.find_element_by_xpath(
        f"//table/tbody/tr/td/table/tbody/tr[{i}]/td[1]")
    print(f"Checking time\t {row_time.text}", flush=True)
    if row_time.text == time_slot:
        return True


def check_gym(i, driver, override):
    gym = driver.find_element_by_xpath(
        f"//table/tbody/tr/td/table/tbody/tr[{i}]/td[2]")
    if gym.text == 'Poolside Gym':  # Prefer to book poolside
        return True
    return override


def check_available(i, driver):
    not_booked = True
    while not_booked:  # continually check if able to book
        avail = driver.find_element_by_xpath(
            f"//table/tbody/tr/td/table/tbody/tr[{i}]/td[6]")
        if avail.text == 'Book':
            avail.click()
            return True
        elif avail.text == 'Full':
            print("Fully booked", flush=True)
            not_booked = False


def book_gym(user, driver):
    # find the field for student number
    student_number_box = driver.find_element_by_xpath(
        "/html/body/main/div/div/div/div[2]/div/form/input[4]")
    # send student number and submit
    student_number_box.send_keys(user)
    student_number_box.submit()
    # click confirm
    confirm_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Confirm Booking')))
    try:
        confirm_button.click()
        print("Success, timeslot is booked\n", flush=True)
    except Exception:
        cookies_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handle')))
        cookies_button.click()

        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Confirm Booking')))
        confirm_button.click()
        all_cookies = driver.get_cookies()
        with open('cookies.json', 'w') as cookies_file:
            json.dump(all_cookies, cookies_file)
        print("Cookies saved\nSuccess, timeslot is booked\n", flush=True)


if __name__ == "__main__":
    now = datetime.datetime.now().replace(microsecond=0)
    print(f"Entering Python script at {now}\n", flush=True)

    with open("config.json", 'r') as file:
        config = json.load(file)

    url = config['url']
    user = config['student_number']
    time_slot = config['time_slot']
    print("Configuration loaded\n" +
          f"\tuser:\t{user}\n" +
          f"\tslot:\t{time_slot}", flush=True)

    # No display
    firefox_options = Options()
    firefox_options.set_headless()
    firefox_options.binary_location = '/usr/lib/firefox/firefox'

    # def func to read config time and set sleep time
    # sleep_hour =
    # sleep_mins =
    # sleep_secs =

    sleep_until = datetime.datetime.today().replace(hour=6,
                                                    minute=30,
                                                    second=0,
                                                    microsecond=0)

    sleep_time = (sleep_until - datetime.datetime.today())

    driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver',
                               options=firefox_options)

    print(f"Entering sleep for {sleep_time.seconds}", flush=True)
    time.sleep(sleep_time.seconds)

    driver.get(url)

    # Add cookies if available
    if os.path.isfile('cookies.json'):
        with open('cookies.json', 'r') as cookies_file:
            cookies = json.load(cookies_file)

    print("Awake \nURL recieved\nChecking times...\n", flush=True)
    # Check for prefered time at Poolside gym
    if check_gym_times(time_slot, driver):
        book_gym(user, driver)
    else:
        print("\n\nPoolside Not Available, Checking Performance\n", flush=True)
        if check_gym_times(time_slot, driver, override=True):
            book_gym(user, driver)

    now = datetime.datetime.now().replace(microsecond=0)
    print(f"Exiting Python script at {now}\n", flush=True)
