import logging
import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

from course import Course

if __name__ == '__main__':
    load_dotenv()
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    if username is None or password is None:
        logging.error('Lütfen .env dosyasına kullanıcı adı ve şifrenizi giriniz.')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--mute-audio")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://lms.gazi.edu.tr/")

    username_field = driver.find_element(By.ID, "UserName")
    login_button = driver.find_element(By.ID, "btnLoginName")
    username_field.send_keys(username)
    login_button.click()
    time.sleep(1)
    password_field = driver.find_element(By.ID, "Password")
    login_button = driver.find_element(By.ID, "btnLoginPass")
    password_field.send_keys(password)
    login_button.click()
    time.sleep(3)

    elements = driver.find_elements(By.NAME, "dontShowAgain")
    if len(elements) > 0:
        for element in elements:
            if 'Devam et' in element.accessible_name:
                element.click()
                time.sleep(3)
                break
    original_window = driver.current_window_handle
    courses = driver.find_elements(By.CLASS_NAME, 'coursename')

    if courses is None or len(courses) == 0:
        print('No courses found')
        exit(1)

    course_list: list[Course] = []
    for course_item in courses:
        course_name = course_item.accessible_name
        print(f'{course_name} dersi bulundu.')
        course = Course(driver, course_name, course_item.get_attribute('href'))
        course_list.append(course)

    for course in course_list:
        course.find_unwatched_lessons()
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    for course in course_list:
        course.watch_lessons()
