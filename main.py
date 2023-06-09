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
password = 'hunter123.'
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
phone_number = os.environ['PHONE_NUMBER']
redirect_url = 'http://www.example.com/unused/redirect/uri'
subreddit_list = ['vancouver',
                  'canada',
                  'Games',
                  'CK3AGOT',
                  'news',
                  'worldnews',
                  'AnimalsBeingDerps',
                  'AnimalsBeingJerks',
                  'cats',
                  'britishcolumbia']



driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

driver.get('https://www.reddit.com/register/')

for i in range(8):
    random_letter = random.choice(letters)
    random_email += random_letter

new_email = random_email + '@gmail.com'

#entering email
driver.find_element(By.CSS_SELECTOR, '#regEmail').send_keys(new_email)
driver.find_element(By.CSS_SELECTOR, '.m-full-width').click()

#entering username and password
time.sleep(1)
username = str(driver.find_element(By.CSS_SELECTOR, 'a.Onboarding__usernameSuggestion:nth-child(1)').text)
driver.find_element(By.CSS_SELECTOR, 'a.Onboarding__usernameSuggestion:nth-child(1)').click()
driver.find_element(By.CSS_SELECTOR, '#regPassword').send_keys(password)
driver.find_element(By.CSS_SELECTOR, 'button.AnimatedForm__submitButton:nth-child(3)').click()



#waits for user to defeat CAPTCHA
input("Press ENTER after filling CAPTCHA")
driver.find_element(By.CSS_SELECTOR, 'button.AnimatedForm__submitButton:nth-child(3)').click()
time.sleep(2)
driver.refresh()

# opens apps and retrieves app id and secret id
driver.get('https://www.reddit.com/prefs/apps')

WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#create-app-button"))).click()
driver.find_element(By.CSS_SELECTOR, 'table.content > tbody:nth-child(1) >'
                                     ' tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)').send_keys(new_email)
driver.find_element(By.CSS_SELECTOR, '#app_type_script').click()
driver.find_element(By.CSS_SELECTOR, 'table.content > tbody:nth-child(1) > tr:nth-child(7) >'
                                     ' td:nth-child(2) > input:nth-child(1)').send_keys(redirect_url)
driver.find_element(By.CSS_SELECTOR, '#create-app > button:nth-child(6)').click()

secret_id = str(driver.find_element(By.CSS_SELECTOR, 'table.preftable:nth-child(4) > tbody:nth-child(1)'
                                                 ' > tr:nth-child(1) > td:nth-child(2)').text)

app_id = str(driver.find_element(By.CSS_SELECTOR, 'div.app-details:nth-child(3) > h3:nth-child(3)').text)

# uses PRAW to subscribe to subreddits

user_agent = f'subreddit suscriber 1.0 by /u/{username}'
reddit = praw.Reddit(
    client_id=app_id,
    client_secret=secret_id,
    user_agent=user_agent,
    password=password,
    username=username,

)

for subreddit in subreddit_list:
    reddit.subreddit(f'{subreddit}').subscribe()

print('Finished Subscribing to Subreddits')


client = Client(account_sid, auth_token)
client.messages.create(body=f'this reddit account username is {username}',
                       from_='+15074797617',
                       to=phone_number)

driver.get('https://mail.google.com')
driver.find_element(By.CSS_SELECTOR, 'div.feature__chapter__button:nth-child(1) > a:nth-child(1)').click()
driver.find_element(By.CSS_SELECTOR, '#firstName').send_keys('rand')
driver.find_element(By.CSS_SELECTOR, '#lastName').send_keys('dom')
driver.find_element(By.CSS_SELECTOR, '#username').send_keys(random_email)
driver.find_element\
    (By.CSS_SELECTOR,
     '#passwd > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)').send_keys(password)
driver.find_element(By.CSS_SELECTOR,
                    '#confirm-passwd > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)')\
    .send_keys(password)
driver.find_element(By.CSS_SELECTOR, '.VfPpkd-LgbsSe-OWXEXe-k8QpJ > div:nth-child(3)').click()