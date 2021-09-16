
# In the parent directory you should have a file `config.json` which is
# structured as follows. Please fill in the student_number
# and time_slot fields with your prefered values.
"""
{
    "url" : "https://hub.ucd.ie/usis/W_HU_MENU.P_PUBLISH?p_tag=GYMBOOK",
    "student_number" : "15311336",
    "time_slot" : "9:30"
}
"""
import json
import selenium as sel
from selenium import webdriver as web

if __name__ == "__main__":

    with open("secrets/config.json", 'r') as file:
        config = json.load(file)

    url = config['url']
    user = config['student_number']
    time = config['time_slot']

    driver = web.Firefox()
    driver.get(url)