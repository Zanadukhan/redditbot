import time
import os
from twilio.rest import Client
import praw
import random
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

random_email = ''
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
password = 'hunter123'
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
phone_number = os.environ['PHONE_NUMBER']


driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

driver.get('https://www.reddit.com/register/')

for i in range(5):
    random_letter = random.choice(letters)
    random_email += random_letter

new_email = random_email + '@gmail.com'

#entering email
driver.find_element(By.CSS_SELECTOR, '#regEmail').send_keys(new_email)
driver.find_element(By.CSS_SELECTOR, '.m-full-width').click()

#entering username and password
time.sleep(1)
username = driver.find_element(By.CSS_SELECTOR, 'a.Onboarding__usernameSuggestion:nth-child(1)')
driver.find_element(By.CSS_SELECTOR, 'a.Onboarding__usernameSuggestion:nth-child(1)').click()
driver.find_element(By.CSS_SELECTOR, '#regPassword').send_keys(password)
driver.find_element(By.CSS_SELECTOR, 'button.AnimatedForm__submitButton:nth-child(3)').click()

#waits for user to defeat CAPTCHA
input("Press ENTER after filling CAPTCHA")
driver.find_element(By.CSS_SELECTOR, 'button.AnimatedForm__submitButton:nth-child(3)').click()

# driver.get('https://www.reddit.com/prefs/apps')

client = Client(account_sid, auth_token)
client.messages.create(body=f'this reddit account username is {username.text}',
                       from_='+15074797617',
                       to=phone_number)
