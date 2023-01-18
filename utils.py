from linkedin_api import Linkedin
import logging
from datetime import datetime
import pandas as pd
import os
import random


if not 'loggers' in os.listdir():
            os.mkdir('loggers')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('loggers/utils.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.info('-'*80)


def autenticate_linkedin_API(profile = None):
    ##### LINKEDIN AUTHENTICATION API #####
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
    api = Linkedin(username, password)
    logger.info(f"Logged into API using {profile}'s profile")
    return api

def setup_correct_directory():
    try:
        home_directory = os.path.expanduser("~")
        desktop_directory = os.path.join(home_directory, "Desktop")
        linkedin_directory = os.path.join(desktop_directory, "Linkedin")
        os.chdir(linkedin_directory)
        if not 'loggers' in os.listdir():
            os.mkdir('loggers')
        if not 'datasets' in os.listdir():
            os.mkdir('datasets')
        logger.info(f"Set directory to {linkedin_directory}")

    except Exception as e:
        logger.error(f"There's been an error, {e} while reading file, check that you are in the right folder")

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
        network_info = pd.DataFrame(columns=['timestamp', 'date_time',  'profile_id', 'connection_level','connections', 'followers'])
        network_info.to_csv('datasets/network_info.csv', index=0)
        logger.info('network info file has been created from 0')

    try:
        submitted_invitation =  pd.read_csv('datasets/submitted_invitation.csv')
    except FileNotFoundError:
        submitted_invitation = pd.DataFrame(columns=[ 'date_time', 'timestamp', 'profile_id', 'message_code', 'accepted_invitation', 'replied'])
        submitted_invitation.to_csv('datasets/submitted_invitation.csv', index=0)
        logger.info('submitted invitation file has been created from 0')

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
    
    try:    
        troubling_profiles = pd.read_csv('datasets/troubling_profiles.csv')
    except FileNotFoundError: 
        troubling_profiles = pd.DataFrame(columns=['Nome', 'Cognome', 'Email', 'LinkedIn', 'Posizione', 'Azienda', 'Città',
    'Stato', 'Continente', 'profile_urn', 'conversation_urn'])
        troubling_profiles.to_csv('datasets/troubling_profiles.csv', index=0)
        logger.info('troubling_profiles file has been created from 0')
    

    logger.info('read in all files')
    return family_offices_UK, network_info, submitted_invitation, message, submitted_call_to_action, troubling_profiles

def create_message(type, text, code):
    message_begin = pd.read_csv('datasets/message.csv')
    new_message = [type, text, code]
    message = pd.DataFrame([new_message], columns=['type', 'text', 'code'])
    message = pd.concat([message_begin, message])
    message.to_csv('datasets/message.csv', index=0)
    logger.info(f'added new message to dataframe {code}')

def create_row_network_info(public_identifier, network_information):
    current_datetime = datetime.now()
    human_readable_date = current_datetime.strftime("%Y-%m-%d %H:%M")
    timestamp = int(current_datetime.timestamp())
    connection_level = network_information['distance']['value']
    connections_number = network_information['connectionsCount']
    followers_number = network_information['followersCount']

    row_network_info = [timestamp,human_readable_date, public_identifier, connection_level, connections_number, followers_number]
    logger.info(f'Created row in network info for {public_identifier}')
    
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

def send_invitations_note(api, how_many):
    family_offices_UK = pd.read_csv('family_offices_UK.csv')
    network_info = pd.read_csv('datasets/network_info.csv')
    submitted_invitation = pd.read_csv('datasets/submitted_invitation.csv')
    message = pd.read_csv('datasets/message.csv')
    troubling_profiles = pd.read_csv('datasets/troubling_profiles.csv')

    linkedin_pi = family_offices_UK.LinkedIn

    counter = 0
    for public_identifier in linkedin_pi:
        if public_identifier in submitted_invitation.profile_id:
            continue

        if counter >= how_many:
            break

        if submitted_invitation.profile_id.str.contains(public_identifier).any():
            continue #ignores the rest of the code and goes to next iteration
            
        if troubling_profiles.LinkedIn.str.contains(public_identifier).any():
            continue

        network_information = api.get_profile_network_info(public_identifier)
        
        if network_information == {}:
            logger.error(f"Proile {public_identifier} has not been found")
            df_with_troubling_person = family_offices_UK.query(f"LinkedIn == '{public_identifier}'")
            troubling_profiles = pd.concat([df_with_troubling_person, troubling_profiles])
            troubling_profiles.to_csv('datasets/troubling_profiles.csv', index=0)
            logger.info(f"{public_identifier} has been added to dataframe of troubling profiles")
            continue
        
        connection_level = network_information['distance']['value']

        if connection_level == 'SELF':
            logger.warning('you are verifying your same profile! dumbass!')
            continue

        assert connection_level in ('DISTANCE_1', 'DISTANCE_2', 'DISTANCE_3', 'OUT_OF_NETWORK')
        if connection_level == 'DISTANCE_1':
            logger.info(f"{public_identifier} for you is a connection of level {connection_level}")
            continue

        assert connection_level in ('DISTANCE_2', 'DISTANCE_3', 'OUT_OF_NETWORK')
        row_network_info = create_row_network_info(public_identifier, network_information)
        network_info.loc[len(network_info)] = row_network_info
        network_info.to_csv('datasets/network_info.csv', index=0)
        logger.info(f"{public_identifier} for you is a connection of level {connection_level}")

        note, code = randomly_get_message(message_begin=message, type='n')
        result, profile_urn = api.add_connection(profile_public_id = public_identifier, message=note)

        if result == False:
            logger.info(f"Sent invitation + note to {public_identifier}")
            family_offices_UK.loc[family_offices_UK.LinkedIn == public_identifier, 'profile_urn'] = profile_urn
            family_offices_UK.to_csv('family_offices_UK.csv', index=0)
            logger.info(f'new profile urn for user {public_identifier} has been added')

            submitted_invitation_row = create_row_submitted_invitation(public_identifier, message_code=code)
            submitted_invitation.loc[len(submitted_invitation)] = submitted_invitation_row
            submitted_invitation.to_csv('datasets/submitted_invitation.csv', index=0)
            counter += 1

def get_conversation_urn(api):
    family_offices_UK = pd.read_csv('family_offices_UK.csv')
    submitted_invitation = pd.read_csv('datasets/submitted_invitation.csv')

    fo_si_merged = pd.merge(submitted_invitation, family_offices_UK, how='left', left_on='profile_id', right_on='LinkedIn')

    conversations = api.get_conversations()

    for i in range(len(conversations['elements'])):

        pi = conversations['elements'][i]['participants'][0]['com.linkedin.voyager.messaging.MessagingMember']['miniProfile']['publicIdentifier']
        if not fo_si_merged.LinkedIn.isin([pi]).any():
            continue

        if pd.isna(family_offices_UK[family_offices_UK.LinkedIn.str.contains(pi)].conversation_urn).any():

            conversation_urn = conversations['elements'][i]['dashEntityUrn'].split(':')[-1]
            family_offices_UK.loc[family_offices_UK.LinkedIn == pi, 'conversation_urn'] = conversation_urn
            logger.info(f"added conversation urn for user {pi}")
            family_offices_UK.to_csv('family_offices_UK.csv', index=0)
            fo_si_merged = pd.merge(submitted_invitation, family_offices_UK, how='left', left_on='profile_id', right_on='LinkedIn')

    while len(conversations['elements']) > 0:

        if fo_si_merged[fo_si_merged.accepted_invitation].conversation_urn.isna().sum() == 0:
            break

        if len(conversations['elements']) < 20:
            break

        conversations = api.get_conversations(conversations['elements'][19]['events'][0]['createdAt'])
        
        for i in range(len(conversations['elements'])):
        
            pi = conversations['elements'][i]['participants'][0]['com.linkedin.voyager.messaging.MessagingMember']['miniProfile']['publicIdentifier']
            if not fo_si_merged.LinkedIn.isin([pi]).any():
                continue    

            if pd.isna(family_offices_UK[family_offices_UK.LinkedIn.str.contains(pi)].conversation_urn).any():

                conversation_urn = conversations['elements'][i]['dashEntityUrn'].split(':')[-1]
                family_offices_UK.loc[family_offices_UK.LinkedIn == pi, 'conversation_urn'] = conversation_urn
                logger.info(f"updated conversation urn for user {pi}")
                family_offices_UK.to_csv('family_offices_UK.csv', index=0)
                fo_si_merged = pd.merge(submitted_invitation, family_offices_UK, how='left', left_on='profile_id', right_on='LinkedIn')
    
    return family_offices_UK
                
def scan_for_1st_connections(api):
    family_offices_UK = pd.read_csv('family_offices_UK.csv')
    network_info = pd.read_csv('datasets/network_info.csv')
    submitted_invitation = pd.read_csv('datasets/submitted_invitation.csv')

    for public_identifier in network_info.profile_id:
        if '1' in network_info[network_info.profile_id ==  public_identifier].connection_level:
            logger.info(f"{public_identifier} is already a level 1 connection")
            continue

        network_information = api.get_profile_network_info(public_identifier)

        if network_information == {}:
            df_with_troubling_person = family_offices_UK.query(f"LinkedIn == '{public_identifier}'")
            troubling_profiles = pd.concat([df_with_troubling_person, troubling_profiles])
            logger.error(f"Proile {public_identifier} has not been found")
            continue

        connection_level = network_information['distance']['value']

        if connection_level == 'SELF':
            logger.warning('you are verifying your same profile! dumbass!')
            continue

        connection_levels_for_public_id = network_info[network_info.profile_id ==  public_identifier].connection_level
        if connection_level == connection_levels_for_public_id.iloc[len(connection_levels_for_public_id)-1]: #last one
            logger.info(f"connection level for profile {public_identifier} has not changed")
            continue

        logger.info(f"new connection level with {public_identifier}, now it is {connection_level}")
        row_network_info = create_row_network_info(public_identifier, network_information)
        network_info.loc[len(network_info)] = row_network_info
        network_info.to_csv('datasets/network_info.csv', index=0)

        if "1" in connection_level:
            
            logger.info(f"{public_identifier} is a first_level_connection")
            submitted_invitation.loc[submitted_invitation.profile_id == public_identifier, "accepted_invitation"] = True
            logger.info(f'updated to True column accpeted invitation on table submitted invitation for user {public_identifier}')
            submitted_invitation.to_csv('datasets/submitted_invitation.csv', index=0)

            if pd.isna(family_offices_UK.loc[family_offices_UK.LinkedIn == public_identifier, 'conversation_urn'].iloc[0]):
                family_offices_UK = get_conversation_urn(api)
    
def send_message_new_1st_connections(api):
    submitted_invitation = pd.read_csv('datasets/submitted_invitation.csv')
    family_offices_UK = pd.read_csv('family_offices_UK.csv')
    message = pd.read_csv('datasets/message.csv')
    submitted_call_to_action = pd.read_csv('datasets/submitted_call_to_action.csv')

    si_fo = pd.merge(submitted_invitation,  family_offices_UK, how='left', left_on='profile_id', right_on='LinkedIn')
    si_fo_accepted_invitation = si_fo[si_fo.accepted_invitation == True]

    for profile_urn, conversation_urn, profile_id in zip(si_fo_accepted_invitation.profile_urn, si_fo_accepted_invitation.conversation_urn, si_fo_accepted_invitation.profile_id):
        if submitted_call_to_action.profile_id.isin([profile_id]).any():
            logger.info(f'already sent 1 message to this person {profile_id}')
            continue

        message = pd.read_csv('datasets/message.csv')
        cta, code = randomly_get_message(message_begin=message, type='cta')
        try:
            result = api.send_message(message_body=cta, conversation_urn_id=conversation_urn)
            if result == False:
                tool = 'conversation_urn'
            

        except:
            result = api.send_message(message_body=cta, recipients=[profile_urn])
            if result == False:
                tool = 'profile_urn'

        finally:
            row_submitted_cta = create_row_subitted_cta(profile_id, message_code=code)
            submitted_call_to_action.loc[len(submitted_call_to_action)] = row_submitted_cta
            submitted_call_to_action.to_csv('datasets/submitted_call_to_action.csv', index=0)
            logger.info(f'sent cta message {code} to {profile_id} using {tool}')



        










