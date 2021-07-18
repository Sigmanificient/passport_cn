from typing import List

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select

from app import config
from app.mailing import send_mail
from app.utils import sleep_after

Driver = webdriver.Remote


def get_driver() -> Driver:
    return webdriver.Remote(
        desired_capabilities=(
            DesiredCapabilities.FIREFOX if config.browser == "firefox" else DesiredCapabilities.CHROME
        )
    )


@sleep_after(2)
def load_website(driver: Driver) -> None:
    driver.get(config.url)


@sleep_after(1)
def get_folder_page(driver: Driver) -> None:
    l_path = "/html/body/div[9]/div[3]/div/button"
    l_elem = driver.find_element_by_xpath(l_path)
    l_elem.click()

    # link 继续未完成的申请预约
    l_path = "/html/body/div[2]/div[1]/ul/li[2]/p[2]/span/a"
    l_elem = driver.find_element_by_xpath(l_path)
    l_elem.click()


@sleep_after(1)
def answer_pop_up(driver: Driver) -> None:
    l_path = "/html/body/div[5]/div[2]/div[2]/table/tbody/tr[1]/td[2]/input"
    record_number_huifu = driver.find_element_by_xpath(l_path)
    record_number_huifu.send_keys(config.record_number_huifu)

    # select 验证问题
    l_path = "/html/body/div[5]/div[2]/div[2]/table/tbody/tr[2]/td[2]/select"
    l_elem = Select(driver.find_element_by_xpath(l_path))
    l_elem.select_by_visible_text(config.question_huifu)

    # input 答 案
    l_path = "/html/body/div[5]/div[2]/div[2]/table/tbody/tr[3]/td[2]/input"
    answer_huifu = driver.find_element_by_xpath(l_path)
    answer_huifu.send_keys(config.answer_huifu)

    # button 提交
    l_path = "/html/body/div[5]/div[3]/div/button[1]"
    l_elem = driver.find_element_by_xpath(l_path)
    l_elem.click()


@sleep_after(5)
def go_to_appointments(driver: Driver) -> None:
    l_path = "/html/body/div[3]/div[1]/div[2]/form/p[2]/input[2]"
    l_elem = driver.find_element_by_xpath(l_path)
    l_elem.click()


@sleep_after(2)
def attempt(driver: Driver) -> bool:
    confirm(driver)
    select(driver)
    return loop_calendar(driver)


@sleep_after(2)
def confirm(driver: Driver) -> None:
    l_path = "/html/body/div[6]/div[3]/div/button"
    l_elem = driver.find_element_by_xpath(l_path)
    l_elem.click()


@sleep_after(1)
def select(driver: Driver) -> None:
    l_path = "/html/body/div[3]/div[1]/div[2]/table/tbody/tr[1]/td/div[2]/select"
    l_elem = Select(driver.find_element_by_xpath(l_path))
    l_elem.select_by_visible_text(config.address)


@sleep_after(2)
def loop_calendar(driver: Driver) -> bool:
    for j in range(4):
        found: bool = loop_calendar_inner(driver, j)
        if found:
            return True


def loop_calendar_inner(driver: Driver, j: int) -> bool:
    if not j % 2:
        driver.find_elements_by_css_selector(".ui-icon-circle-triangle-e")[0].click()
        return False

    driver.find_elements_by_css_selector(".ui-icon-circle-triangle-w")[0].click()
    for span in driver.find_elements_by_css_selector('.fc-event-title'):
        space: List[str] = span.text.split('/')

        if space[0] == space[1]:
            continue

        print(config.console_message)

        if config.mail == 1:
            send_mail(config.mail_recipient, config.mail_title, config.mail_message)

        return True
    return False


def main() -> None:
    driver: Driver = get_driver()
    driver.maximize_window()
    load_website(driver)

    if config.browser == "firefox":
        driver.switch_to.alert.accept()
        driver.switch_to.default_content()

    get_folder_page(driver)
    answer_pop_up(driver)
    go_to_appointments(driver)

    attempt_number: int = 0
    found: bool = False

    while not found:
        if attempt_number:
            driver.refresh()

        attempt_number += 1
        print(f"Trail number: {attempt_number}")
        found: bool = attempt(driver)
