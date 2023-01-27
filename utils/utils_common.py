from datetime  import datetime
from time import sleep
import pandas as pd
import logging
import random
import os

if not 'loggers' in os.listdir():
            os.mkdir('loggers')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('loggers/utils_common.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.info('-'*80)

def setup_correct_directory(directory_name = 'Linkedin'):
    try:
        home_directory = os.path.expanduser("~")
        desktop_directory = os.path.join(home_directory, "Desktop")
        os.makedirs(desktop_directory + f'/{directory_name}' + '/loggers', exist_ok=True)
        os.makedirs(desktop_directory + f'/{directory_name}' + '/datasets', exist_ok=True)
        os.chdir(desktop_directory + f'/{directory_name}')

        logger.info(f"Set directory to {desktop_directory}/{directory_name}")

    except Exception as e:
        logger.error(f"There's been an error, {e} while reading file, check that you are in the right folder")

def repeat_times(max_attempts, function, *args):    
    counter = 0
    while counter < max_attempts:
        try:
            function(*args)
        except Exception as e:
            logger.error(f'Error {e} in {function}, attempt {counter}')
            counter += 1
            sleep(180)
            continue
        sleep(180)
        break
    else:
        logger.error(f'Error: Max attempts reached in {function}')
        raise Exception("Error: Max attempts reached")


def setup_begging_datasets():

    if not 'datasets' in os.listdir():
            os.mkdir('datasets')

    if not 'family_offices_UK.csv' in os.listdir():
        family_offices = pd.read_csv('family_offices.csv')
        family_offices_UK = family_offices.loc[family_offices.Stato.isin(['England', 'Scotland', 'Ireland'])]
        family_offices_UK.to_csv('family_offices_UK.csv', index=0)
        logger.info('family offices has been created')
    else:
        family_offices_UK = pd.read_csv('family_offices_UK.csv')
        logger.info('family offices UK has been read')

    try: 
        network_info = pd.read_csv('datasets/network_info.csv')
    except FileNotFoundError:
        network_info = pd.DataFrame(columns=['timestamp', 'date_time',  'profile_id', 'connection_level'])
        network_info.to_csv('datasets/network_info.csv', index=0)
        logger.info('network info file has been created from 0')

    try:
        submitted_invitation =  pd.read_csv('datasets/submitted_invitation.csv')
    except FileNotFoundError:
        submitted_invitation = pd.DataFrame(columns=[ 'timestamp', 'datetime', 'profile_id', 'message_code', 'accepted_invitation', 'replied'])
        submitted_invitation.to_csv('datasets/submitted_invitation.csv', index=0)
        logger.info('submitted invitation file has been created from 0')
    
    try:
        submitted_inmail =  pd.read_csv('datasets/submitted_inmail.csv')
    except FileNotFoundError:
        submitted_inmail = pd.DataFrame(columns=['timestamp', 'datetime', 'profile_id', 'message_code'])
        submitted_inmail.to_csv('datasets/submitted_inmail.csv', index=0)
        logger.info('submitted inmail file has been created from 0')

    try:    
        message = pd.read_csv('datasets/message.csv')
    except FileNotFoundError: 
        message = pd.DataFrame(columns=['type', 'text', 'code'])
        message.to_csv('datasets/message.csv', index=0)
        logger.info('message file has been created from 0')

    try:    
        submitted_call_to_action = pd.read_csv('datasets/submitted_call_to_action.csv')
    except FileNotFoundError: 
        submitted_call_to_action = pd.DataFrame(columns=['timestamp', 'date_time', 'profile_id', 'message_code', 'replied'])
        submitted_call_to_action.to_csv('datasets/submitted_call_to_action.csv', index=0)
        logger.info('submitted_call_to_action file has been created from 0')

    logger.info('read in all files')

def create_message(type, text, code):
    message_begin = pd.read_csv('datasets/message.csv')
    new_message = [type, text, code]
    message = pd.DataFrame([new_message], columns=['type', 'text', 'code'])
    message = pd.concat([message_begin, message])
    message.to_csv('datasets/message.csv', index=0)
    logger.info(f'added new message to dataframe {code}')

def create_row_network_info(public_identifier, connection_level):
    current_datetime = datetime.now()
    human_readable_date = current_datetime.strftime("%Y-%m-%d %H:%M")
    timestamp = int(current_datetime.timestamp())
    row_network_info = [timestamp,human_readable_date, public_identifier, connection_level]
    # logger.info(f'Created row in network info for {public_identifier}')
    
    return row_network_info

def create_row_submitted_invitation(public_identifier, message_code):
    current_datetime = datetime.now()
    human_readable_date = current_datetime.strftime("%Y-%m-%d %H:%M")
    timestamp = int(current_datetime.timestamp())
    accepted_invitation = False
    replied = False
    submitted_invitation_row = [timestamp, human_readable_date,  public_identifier, message_code, accepted_invitation, replied]
    logger.info(f'Created row in submitted_invitation for  {public_identifier}')
    return submitted_invitation_row

def create_row_subitted_cta(profile_id, message_code):

    current_datetime = datetime.now()
    human_readable_date = current_datetime.strftime("%Y-%m-%d %H:%M")
    timestamp = int(current_datetime.timestamp())
    replied = False
    row_submitted_invitation = [timestamp, human_readable_date, profile_id, message_code, replied]

    return row_submitted_invitation

def create_row_submitted_inmail(profile_id, message_code):
    current_datetime = datetime.now()
    human_readable_date = current_datetime.strftime("%Y-%m-%d %H:%M")
    timestamp = int(current_datetime.timestamp())
    row_inmail = [timestamp, human_readable_date, profile_id, message_code]

    return row_inmail

def randomly_get_message(message_begin, type):
    if type == 'note':
        first_letter = 'n'
    elif type == 'cta':
        first_letter = 'c'
    df = message_begin[message_begin.code.str.contains(first_letter)]
    random_number = random.choice([*range(len(df))])
    message = df.iloc[random_number].text
    code = df.iloc[random_number].code
    return message, code

