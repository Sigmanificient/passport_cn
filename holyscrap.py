import time
import smtplib, ssl

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config

############################################################

def send_mail(to_address, subject, body):
    smtp_user = config.smtp_user
    smtp_password = config.smtp_password
    server = config.smtp_server
    port = 587

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_address
    msg["Cc"] = smtp_user
    msg.attach(MIMEText(body, "html"))
    s = smtplib.SMTP(server, port)
    #s.connect(server, port)
    s.ehlo()
    s.starttls()
    #s.ehlo()
    s.login(smtp_user, smtp_password)
    s.sendmail(smtp_user, to_address, msg.as_string())
    s.quit()

############################################################

driver = webdriver.Remote(
   command_executor='http://127.0.0.1:4444/wd/hub',
   desired_capabilities=DesiredCapabilities.CHROME)

driver.maximize_window()

found = 0
for t in range(100000):

    #open URI
    driver.get(config.url)

    time.sleep(2)

    #button 我已知晓
    lpath="/html/body/div[9]/div[3]/div/button"
    lelem=driver.find_element_by_xpath(lpath)
    lelem.click()

    #link 继续未完成的申请预约
    lpath="/html/body/div[2]/div[1]/ul/li[2]/p[2]/span/a"
    lelem=driver.find_element_by_xpath(lpath)
    lelem.click()

    time.sleep(1)

    #POPUP
    #input 档 案 号
    lpath="/html/body/div[5]/div[2]/div[2]/table/tbody/tr[1]/td[2]/input"
    recordNumberHuifu=driver.find_element_by_xpath(lpath)
    recordNumberHuifu.send_keys(config.recordnumberhuifu)

    #select 验证问题
    lpath="/html/body/div[5]/div[2]/div[2]/table/tbody/tr[2]/td[2]/select"
    lelem=Select(driver.find_element_by_xpath(lpath))
    lelem.select_by_visible_text(config.questionhuifu)

    #input 答 案
    lpath="/html/body/div[5]/div[2]/div[2]/table/tbody/tr[3]/td[2]/input"
    answerHuifu=driver.find_element_by_xpath(lpath)
    answerHuifu.send_keys(config.answerhuifu)

    #button 提交
    lpath="/html/body/div[5]/div[3]/div/button[1]"
    lelem=driver.find_element_by_xpath(lpath)
    lelem.click()

    time.sleep(1)

    #button 进入预约
    lpath="/html/body/div[3]/div[1]/div[2]/form/p[2]/input[2]"
    lelem=driver.find_element_by_xpath(lpath)
    lelem.click()

    time.sleep(3)

    #button 确认
    lpath="/html/body/div[6]/div[3]/div/button"
    lelem=driver.find_element_by_xpath(lpath)
    lelem.click()

    #select
    lpath="/html/body/div[3]/div[1]/div[2]/table/tbody/tr[1]/td/div[2]/select"
    lelem=Select(driver.find_element_by_xpath(lpath))
    lelem.select_by_visible_text(config.address)

    #loop on the calendar page
    for j in range(2):
        if j % 2 == 0:
            driver.find_elements_by_css_selector(".ui-icon-circle-triangle-e")[0].click()
        else:
            driver.find_elements_by_css_selector(".ui-icon-circle-triangle-w")[0].click()
            for span in driver.find_elements_by_css_selector('.fc-event-title'):
                #print(span.text)
                space = span.text.split('/')
                if space[0] != space[1]:
                    print(config.console_message)
                    found = 1
                    if config.mail == 1:
                        send_mail(config.mail_recipient, config.mail_title, config.mail_message)
                    break
        time.sleep(1)

    if (found == 1):
        break

driver.close()
