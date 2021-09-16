
"""
In the parent directory you should have a file `config.json` which is
structured as follows. Please fill in the student_number
and time_slot fields with your prefered values.

{
    "url" : "https://hub.ucd.ie/usis/W_HU_MENU.P_PUBLISH?p_tag=GYMBOOK",
    "student_number" : "STUDENT_NUMBER",
    "time_slot" : "9:30"
}
"""
import json
import time
from selenium import webdriver


def check_gym_times(time_slot, driver):
    for i in range(1, 8):
        if check_timeslot(i, time_slot, driver):
            if check_gym(i, driver):
                check_available(i, driver)


def check_timeslot(i, time_slot, driver):
    row_time = driver.find_element_by_xpath(f"//table/tbody/tr[{i}]/td[1]")
    if row_time == time_slot:
        return True


def check_gym(i, driver):
    gym = driver.find_element_by_xpath(f"//table/tbody/tr[{i}]/td[2]")
    if gym == 'Poolside':
        return True


def check_available(i, driver):
    avail = driver.find_element_by_xpath(f"//table/tbody/tr[{i}]/td[6]")
    if avail == 'Book':
        avail.click()
        print("Timeslot is available.\n")


def book_gym(user, driver):
    student_number_box = driver.find_element_by_xpath("")
    student_number_box.send_keys(user)
    student_number_box.submit()


if __name__ == "__main__":

    with open("config.json", 'r') as file:
        config = json.load(file)

    url = config['url']
    user = config['student_number']
    time_slot = config['time_slot']

    # No display
    firefox_options = webdriver.firefox.webdriver.Options()
    firefox_options.set_headless()

    driver = webdriver.Firefox(options=firefox_options)
    time.sleep(5)
    driver.get(url)

    # Check for prefered time and gym
    if check_gym_times(time_slot, driver):
        book_gym(user)
