from selenium import webdriver
from datetime import datetime
import pandas as  pd
import utils_api, utils_common
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
file_handler = logging.FileHandler('loggers/utils_selenium.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.info('-'*80)

def linkedin_login(profile = None):

    if profile == None:
        profile = input('what profile do you want to use gialuca/manuel/cappero? ')

    if profile == 'gianluca':
        username = 'gianluca@vaiuk.finance'
        password = '2023.VaiLondon$'

    elif profile == 'manuel':
        username = 'rech.manuel.27@gmail.com'
        password = 'micael21'

    elif profile == 'cappero':
        username = 'capperobello111@gmail.com'
        password = 'micael21'

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

def send_in_mail_message(sleeps=60):

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
    
    driver = linkedin_login('gianluca')

    si_to_be_inmailed_fo = pd.merge(si_to_be_inmailed, family_offices_UK, how='left', left_on='profile_id', right_on='LinkedIn')
    for name, profile_id, profile_urn in zip(si_to_be_inmailed_fo.Nome, si_to_be_inmailed_fo.profile_id, si_to_be_inmailed_fo.profile_urn):

        if submitted_inmail.profile_id.isin([profile_id]).any():
            logger.info(f'inmail has already been sent to person {profile_id}')
            continue
        
        driver.get(f"https://www.linkedin.com/in/{profile_id}")
        
        sleep(10)

        driver.get(f"https://www.linkedin.com/sales/lead/{profile_urn},name")

        try:
            message_button = WebDriverWait(driver, sleeps).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[1]/div[3]/div/div[1]/div/div/section[1]/section[1]/div[2]/section/div[1]/div[2]/button')))
        except:
            message_button = WebDriverWait(driver, sleeps).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[1]/div[3]/div/div/div/div/section[1]/section[1]/div[2]/section/div[1]/div/button')))
                                                                                                    
        message_button.click()

        try:
            messages_not_possible = WebDriverWait(driver, sleeps).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/section/div[2]/section/div[2]/span')))
            assert messages_not_possible.text == "Sorry, you can’t send a reply because the recipient has disabled all communications"
            continue

        except:
            pass

        object_field = WebDriverWait(driver, sleeps).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/section/div[2]/section/div[2]/form[1]/input')))
        object_field.send_keys('Partnership Proposal by VAI UK Ltd')

        cta, code = utils_common.randomly_get_message(message, type='cta')
        core_field = WebDriverWait(driver, sleeps).until(EC.element_to_be_clickable((By.TAG_NAME, 'textarea')))
        core_field.send_keys(cta.format(name))

        row_submitted_inmail = utils_common.create_row_submitted_inmail(profile_id=profile_id, message_code=code)
        submitted_inmail.loc[len(submitted_inmail)] = row_submitted_inmail
        submitted_inmail.to_csv('datasets/submitted_inmail.csv', index=0)
        logger.info(f"added row for {profile_id} in submitted in mail")
        sleep(10)

        send_button = WebDriverWait(driver, sleeps).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/section/div[2]/section/div[2]/form[1]/section[2]/span[2]/button')))
        send_button.click()

        logger.info(f'send inmail to {profile_id}')
        sleep(10)

def get_new_connections(stopping_id):
    # stopping id is created just before the campaing starts, creating a cutoff for which we do not need to look more back in time for connections
    # in simple works, the last connection before the campaign starst. 

    submitted_invitation = pd.read_csv('datasets/submitted_invitation.csv')    
    network_information = pd.read_csv('datasets/network_info.csv')
    family_offices_UK = pd.read_csv('family_offices_UK.csv')

    driver = linkedin_login('gianluca')
    driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections")

    recently_added_button = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div/div[2]/div/div/main/div/section/div[1]/div[1]/div/button/span')))
    assert recently_added_button.text == 'Recently added'

    table_connections = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div/div[2]/div/div/main/div/section/div[2]/div[1]')))

    lis = table_connections.find_elements(By.TAG_NAME, 'li')

    found=False
    while found == False:

        for li in lis:

            nome = li.find_element(By.TAG_NAME, 'a')
            profile_id = nome.get_attribute('href')
            profile_id = profile_id.split('/')[-2]

            if profile_id == stopping_id:
                found = True
                break

            if not submitted_invitation.profile_id.isin([profile_id]).any():
                continue

            if submitted_invitation.loc[submitted_invitation.profile_id == profile_id, 'accepted_invitation'].iloc[0] == True:
                continue
                
            print(profile_id)
            submitted_invitation.loc[submitted_invitation.profile_id == profile_id, 'accepted_invitation'] = True
            logger.info(f'{profile_id} has accepted invitation, updated column on submitted invitation')
            submitted_invitation.to_csv('datasets/submitted_invitation.csv', index=0)

            network_information.loc[network_information.profile_id == profile_id] = utils_common.create_row_network_info(public_identifier=profile_id, connection_level='DISTANCE_1')
            logger.info(f'network info has been updated to 1 for {profile_id}')
            network_information.to_csv('datasets/network_info.csv', index=0)

            if pd.isna(family_offices_UK.loc[family_offices_UK.LinkedIn == profile_id, 'conversation_urn'].iloc[0]):
                family_offices_UK = utils_api.get_conversation_urn(sleeping_time=60)

        driver.execute_script("arguments[0].scrollIntoView();", nome)

    driver.close()


# send_in_mail_message()