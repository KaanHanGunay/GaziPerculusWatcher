import time

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from week import Week


def find_element_by_id(element: WebElement | WebDriver, class_name: str):
    return find_element(element, class_name, By.CLASS_NAME)


def find_element_by_tag_name(element: WebElement | WebDriver, tag_name: str):
    return find_element(element, tag_name, By.TAG_NAME)


def find_element_by_class_name(element: WebElement | WebDriver, class_name: str):
    return find_element(element, class_name, By.CLASS_NAME)


def find_element(element: WebElement | WebDriver, value: str, by: By):
    try:
        return element.find_element(by, value)
    except NoSuchElementException:
        return None


class Course:
    def __init__(self, webdriver: WebDriver, name: str, link: str):
        self.webdriver = webdriver
        self.name = name
        self.link = link
        self.weeks = []

    def find_unwatched_lessons(self):
        self.webdriver.execute_script("window.open('');")
        self.webdriver.switch_to.window(self.webdriver.window_handles[-1])
        self.webdriver.get(self.link)
        time.sleep(3)

        activities_div = self.webdriver.find_element(By.ID, 'activities')
        week_divs = activities_div.find_elements(By.XPATH, './child::*')
        print(f'{self.name} dersi toplam {len(week_divs)} hafta tespit edildi.')
        for week_div in week_divs:
            week = Week(week_div.find_element(By.TAG_NAME, 'span').text)
            activities = week_div.find_elements(By.CLASS_NAME, 'cardItem')
            for activity in activities:
                cardviewtitle = activity.find_element(By.CLASS_NAME, 'cardviewtitle')
                a = cardviewtitle.find_element(By.TAG_NAME, 'a')
                info = find_element_by_id(activity, 'icon-info-sign')
                thumbs_up = find_element_by_id(activity, 'icon-thumbs-up')
                if info is not None and thumbs_up is None:
                    link = a.get_attribute('href')
                    week.links.append(link)
            if len(week.links) > 0:
                self.weeks.append(week)
                print(f'{self.name} dersinin {week.name} zamanında toplam {len(week.links)} izlenmemiştir.')

    def watch_lessons(self):
        for week in self.weeks:
            for lesson in week.links:
                self.webdriver.execute_script("window.open('');")
                self.webdriver.switch_to.window(self.webdriver.window_handles[-1])
                self.webdriver.get(lesson)
                time.sleep(5)

                warning = find_element_by_tag_name(self.webdriver, 'strong')
                if warning is not None:
                    self.webdriver.close()
                    self.webdriver.switch_to.window(self.webdriver.window_handles[0])
                    print('Ders yapılmadığı için geçildi.')
                    break

                button_div = find_element_by_class_name(self.webdriver, 'system-modal-footer-buttons')
                if button_div is not None:
                    button_div.find_element(By.TAG_NAME, 'button').click()

                select_rate = self.webdriver.find_element(By.CLASS_NAME, 'playbackrate')
                select_rate = Select(select_rate)
                select_rate.select_by_value('2')

                current = self.webdriver.find_element(By.ID, 'rec-current').text
                total = self.webdriver.find_element(By.ID, 'rec-total').text

                print(f'{self.name} dersinin {week.name} dersi izlenmeye başlandı.')

                while current != total:
                    time.sleep(5)
                    current = self.webdriver.find_element(By.ID, 'rec-current').text

                self.webdriver.close()
                self.webdriver.switch_to.window(self.webdriver.window_handles[0])
