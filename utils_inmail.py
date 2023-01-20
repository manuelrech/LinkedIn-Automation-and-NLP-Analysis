from selenium import webdriver
from datetime import datetime
import pandas as  pd
import utils
import logging
from time import sleep
from selenium import  webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('loggers/utils_inmail.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.info('-'*80)

def linkedin_login(username, password):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    ##### LOGIN SESSION #####
    driver.get("https://www.linkedin.com")
    username_space = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'session_key')))
    password_space = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'session_password')))
    username_space.send_keys(username)
    password_space.send_keys(password)
    accedi_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'sign-in-form__submit-button')))
    accedi_button.click()
    sleep(10)
    logger.info('successfully logged into linkedin with selenium')
    return driver

def send_in_mail_message():
    submitted_invitation = pd.read_csv('datasets/submitted_invitation.csv')
    submitted_inmail = pd.read_csv('datasets/submitted_inmail.csv')
    family_offices_UK = pd.read_csv('family_offices_UK.csv')
    message = pd.read_csv('datasets/message.csv')

    si_not_accepted = submitted_invitation[submitted_invitation.accepted_invitation == False]

    seven_days_timestamp = 604800
    current_timestamp = int(datetime.now().timestamp())
    si_to_be_inmailed = si_not_accepted[si_not_accepted.timestamp + seven_days_timestamp < current_timestamp]

    if si_to_be_inmailed.empty:
        logger.info('no people to target with inmail yet')
        return
    
    driver = linkedin_login(username = 'gianluca@vaiuk.finance', password = '2023.VaiLondon$')

    si_to_be_inmailed_fo = pd.merge(si_to_be_inmailed, family_offices_UK, how='left', left_on='profile_id', right_on='LinkedIn')
    for name, profile_id in zip(si_to_be_inmailed_fo.profile_id, si_to_be_inmailed_fo.Nome):

        if submitted_inmail.profile_id.isin([profile_id]).any():
            logger.info(f'inmail has already been sent to person {profile_id}')
            continue
        
        driver.get(f"https://www.linkedin.com/in/{profile_id}")
        
        more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/button')))
        more_button.click() 

        view_in_sales_navigator_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/div/div/ul/li[1]/div')))
        view_in_sales_navigator_button.click() 

        sleep(10) 
        driver.switch_to.window(driver.window_handles[-1])

        message_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[1]/div[3]/div/div[1]/div/div/section[1]/section[1]/div[2]/section/div[1]/div[2]/button')))
        message_button.click()

        object_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/section/div[2]/section/div[2]/form[1]/input')))
        object_field.send_keys('Partnership Proposal by VAI UK Ltd')

        cta, code = utils.randomly_get_message(message, type='cta')
        core_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'textarea')))
        core_field.send_keys(cta.format(name))

        row_submitted_inmail = utils.create_row_submitted_inmail(profile_id=profile_id, message_code=code)
        submitted_inmail.loc[len(submitted_inmail)] = row_submitted_inmail
        submitted_inmail.to_csv('datasets/submitted_inmail.csv', index=0)
        logger.info(f"added row for {profile_id} in submitted in mail")

        send_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/section/div[2]/section/div[2]/form[1]/section[2]/span[2]/button')))
        # send_button.click()
        logger.info(f'send inmail to {profile_id}')
        driver.switch_to.window(driver.window_handles[0])


