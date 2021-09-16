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
import json
import time
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def check_gym_times(time_slot, driver, override=False):
    for i in range(1, 8):
        if check_timeslot(i, time_slot, driver):
            if check_gym(i, driver, override):
                check_available(i, driver)


def check_timeslot(i, time_slot, driver):
    row_time = driver.find_element_by_xpath(f"//table/tbody/tr[{i}]/td[1]")
    if row_time == time_slot:
        return True


def check_gym(i, driver, override):
    gym = driver.find_element_by_xpath(f"//table/tbody/tr[{i}]/td[2]")
    if gym == 'Poolside':
        return True
    return override


def check_available(i, driver):
    avail = driver.find_element_by_xpath(f"//table/tbody/tr[{i}]/td[6]")
    if avail.text == 'Book':
        avail.click()


def book_gym(user, driver):
    # find the field for student number
    student_number_box = driver.find_element_by_xpath(
        "/html/body/main/div/div/div/div[2]/div/form/input[4]")
    # send student number and submit
    student_number_box.send_keys(user)
    student_number_box.submit()
    # click confirm
    confirm = driver.find_element_by_xpath(
        '/html/body/main/div/div/div/div[2]/div/a[1]')
    confirm.click()


if __name__ == "__main__":
    now = datetime.datetime.now().replace(microsecond=0)
    print(f"Entering Python script at {now}\n")

    with open("config.json", 'r') as file:
        config = json.load(file)

    url = config['url']
    user = config['student_number']
    time_slot = config['time_slot']
    print("Configuration loaded\n" +
          f"\tuser:\t{user}\n" +
          f"\tslot:\t{time_slot}")

    # No display
    firefox_options = Options()
    firefox_options.set_headless()
    firefox_options.binary_location = '/usr/lib/firefox/firefox'

    sleep_until = datetime.datetime.today().replace(hour=6,
                                                    minute=30,
                                                    second=0,
                                                    microsecond=0)

    sleep_time = (sleep_until - datetime.datetime.today()).seconds

    driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver',
                               options=firefox_options)
    now = datetime.datetime.now().replace(microsecond=0)

    print(f"Entering sleep at {now}")
    time.sleep(sleep_time)
    driver.get(url)

    print("Awake \nURL recieved\nChecking times...\n")
    # Check for prefered time at Poolside gym
    if check_gym_times(time_slot, driver):
        book_gym(user)
    # Check for prefered time at Performance gym
    elif check_gym_times(time_slot, driver, override=True):
        book_gym(user)

    now = datetime.datetime.now().replace(microsecond=0)
    print(f"Exiting Python script at {now}\n")