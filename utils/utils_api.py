from linkedin_api import Linkedin
import utils_common
from time import sleep
import pandas as pd
import logging
import os


if not 'loggers' in os.listdir():
            os.mkdir('loggers')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('loggers/utils_api.log')
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

def send_invitations_note(how_many, sleeping_time=60):
    
    api = autenticate_linkedin_API('gianluca')

    family_offices_UK = pd.read_csv('family_offices_UK.csv')
    network_info = pd.read_csv('datasets/network_info.csv')
    submitted_invitation = pd.read_csv('datasets/submitted_invitation.csv')
    message = pd.read_csv('datasets/message.csv')

    counter = 0
    for profile_id, nome in zip(family_offices_UK.LinkedIn, family_offices_UK.Nome):

        if counter >= how_many:
            break

        if submitted_invitation.profile_id.isin([profile_id]).any():
            continue #ignores the rest of the code and goes to next iteration
            
        if family_offices_UK[family_offices_UK.LinkedIn == profile_id].troubling_profile.any():
            continue

        if family_offices_UK[family_offices_UK.LinkedIn == profile_id].already_1st.any():
            continue
        
        network_information = api.get_profile_network_info(profile_id)
        sleep(sleeping_time)

        if network_information == {}:

            logger.warning(f"Proile {profile_id} has not been found")
            family_offices_UK.loc[family_offices_UK.LinkedIn == profile_id, 'troubling_profile'] = True
            family_offices_UK.to_csv('family_offices_UK.csv', index=0)
            logger.info(f"{profile_id} has been added flag troubling profile")
            
            continue
        
        connection_level = network_information['distance']['value']

        assert connection_level in ('SELF', 'DISTANCE_1', 'DISTANCE_2', 'DISTANCE_3', 'OUT_OF_NETWORK')
        
        if connection_level == 'SELF':
            logger.warning('you are verifying your same profile! dumbass!')
            continue
        
        if connection_level == 'DISTANCE_1':

            logger.warning(f"{profile_id} for you is aready a connection of level {connection_level}")
            family_offices_UK.loc[family_offices_UK.LinkedIn == profile_id, 'already_1st'] = True
            family_offices_UK.to_csv('family_offices_UK.csv', index=0)
            logger.info(f"{profile_id} has been added flag already 1st")

            continue

        assert connection_level in ('DISTANCE_2', 'DISTANCE_3', 'OUT_OF_NETWORK')
        
        # logger.info(f"{profile_id} for you is a connection of level {connection_level}")
        network_info.loc[len(network_info)] = utils_common.create_row_network_info(profile_id, connection_level)
        network_info.to_csv('datasets/network_info.csv', index=0)
        logger.info(f"{profile_id} has been updated on network information with connection level {connection_level}")


        note, code = utils_common.randomly_get_message(message_begin=message, type='note')
        note = note.format(nome)
        if len(note) > 300:
            logger.error('message with name was longer than 300 char')
            family_offices_UK.loc[family_offices_UK.LinkedIn == profile_id, 'troubling_profile'] = True
            family_offices_UK.to_csv('family_offices_UK.csv', index=0)
            logger.info(f"{profile_id} has been added flag troubling profile")
            continue

        result, profile_urn = api.add_connection(profile_public_id = profile_id, message=note.format(nome))
        sleep(sleeping_time)

        if result == False:

            logger.info(f"Sent invitation + note to {profile_id}")
            family_offices_UK.loc[family_offices_UK.LinkedIn == profile_id, 'profile_urn'] = profile_urn
            family_offices_UK.to_csv('family_offices_UK.csv', index=0)
            logger.debug(f'new profile urn for user {profile_id} has been added')

            submitted_invitation.loc[len(submitted_invitation)] = utils_common.create_row_submitted_invitation(profile_id, message_code=code)
            submitted_invitation.to_csv('datasets/submitted_invitation.csv', index=0)
            counter += 1
        
        elif result == True:

            logger.error(f"there's been an error while sending a message to {profile_id}")
            family_offices_UK.loc[family_offices_UK.LinkedIn == profile_id, 'troubling_profile'] = True
            family_offices_UK.to_csv('family_offices_UK.csv', index=0)
            logger.info(f"{profile_id} has been added flag troubling profile")
        
        else:

            logger.error(f"Result has value: {result}")

def get_conversation_urn(sleeping_time=60):
    api = autenticate_linkedin_API('gianluca')

    family_offices_UK = pd.read_csv('family_offices_UK.csv')
    submitted_invitation = pd.read_csv('datasets/submitted_invitation.csv')

    fo_si_merged = pd.merge(submitted_invitation, family_offices_UK, how='left', left_on='profile_id', right_on='LinkedIn')

    conversations = api.get_conversations()
    sleep(sleeping_time)

    for i in range(len(conversations['elements'])):

        pi = conversations['elements'][i]['participants'][0]['com.linkedin.voyager.messaging.MessagingMember']['miniProfile']['publicIdentifier']
        if not fo_si_merged.LinkedIn.isin([pi]).any():
            continue

        if pd.isna(family_offices_UK[family_offices_UK.LinkedIn.str.contains(pi)].conversation_urn).any():

            conversation_urn = conversations['elements'][i]['dashEntityUrn'].split(':')[-1]
            family_offices_UK.loc[family_offices_UK.LinkedIn == pi, 'conversation_urn'] = conversation_urn
            logger.debug(f"added conversation urn for user {pi}")
            family_offices_UK.to_csv('family_offices_UK.csv', index=0)
            fo_si_merged = pd.merge(submitted_invitation, family_offices_UK, how='left', left_on='profile_id', right_on='LinkedIn')

    while len(conversations['elements']) > 0:

        if fo_si_merged[fo_si_merged.accepted_invitation].conversation_urn.isna().sum() == 0:
            break

        if len(conversations['elements']) < 20:
            break

        conversations = api.get_conversations(conversations['elements'][19]['events'][0]['createdAt'])
        sleep(sleeping_time)
        
        for i in range(len(conversations['elements'])):
        
            pi = conversations['elements'][i]['participants'][0]['com.linkedin.voyager.messaging.MessagingMember']['miniProfile']['publicIdentifier']
            if not fo_si_merged.LinkedIn.isin([pi]).any():
                continue    

            if pd.isna(family_offices_UK[family_offices_UK.LinkedIn.str.contains(pi)].conversation_urn).any():

                conversation_urn = conversations['elements'][i]['dashEntityUrn'].split(':')[-1]
                family_offices_UK.loc[family_offices_UK.LinkedIn == pi, 'conversation_urn'] = conversation_urn
                logger.debug(f"updated conversation urn for user {pi}")
                family_offices_UK.to_csv('family_offices_UK.csv', index=0)
                fo_si_merged = pd.merge(submitted_invitation, family_offices_UK, how='left', left_on='profile_id', right_on='LinkedIn')
    
    return family_offices_UK
                
# def scan_for_1st_connections(api, sleeping_time=60):
#     family_offices_UK = pd.read_csv('family_offices_UK.csv')
#     network_info = pd.read_csv('datasets/network_info.csv')
#     submitted_invitation = pd.read_csv('datasets/submitted_invitation.csv')
#     troubling_profiles = pd.read_csv('datasets/troubling_profiles.csv')

#     for public_identifier in network_info.profile_id:
        
#         ni_for_person = network_info[network_info.profile_id ==  public_identifier]
#         if ni_for_person.connection_level.isin(['DISTANCE_1']).any():
#             logger.info(f"{public_identifier} is already a level 1 connection")
#             continue
        
#         current_timestamp = int(datetime.now().timestamp())
#         if ni_for_person.timestamp.iloc[0] > current_timestamp - 3600*5:
#             logger.info(f'{public_identifier} has already been scraped in the last 5 hours')
#             continue

#         network_information = api.get_profile_network_info(public_identifier)
#         sleep(sleeping_time)

#         if network_information == {}:
#             logger.error(f"Proile {public_identifier} has either changed profile url or api issue, re-authenticating")
#             df_with_troubling_person = family_offices_UK.query(f"LinkedIn == '{public_identifier}'")
#             troubling_profiles = pd.concat([df_with_troubling_person, troubling_profiles])
#             api = autenticate_linkedin_API('gianluca')
#             continue

#         connection_level = network_information['distance']['value']

#         if connection_level == 'SELF':
#             logger.warning('you are verifying your same profile! dumbass!')
#             continue

#         connection_levels_for_public_id = network_info[network_info.profile_id ==  public_identifier].connection_level
#         if connection_level == connection_levels_for_public_id.iloc[len(connection_levels_for_public_id)-1]: #last one
#             logger.info(f"connection level for profile {public_identifier} has not changed")

#         else:
#             logger.info(f"new connection level with {public_identifier}, now it is {connection_level}")

#         network_info.loc[network_info['profile_id'] == public_identifier] = utils_common.create_row_network_info(public_identifier, connection_level)
#         network_info.to_csv('datasets/network_info.csv', index=0)
#         logger.info(f'updated row in network information for user {public_identifier}')

#         if "1" in connection_level:
            
#             logger.info(f"{public_identifier} is a first_level_connection")
#             submitted_invitation.loc[submitted_invitation.profile_id == public_identifier, "accepted_invitation"] = True
#             logger.info(f'updated to True column accpeted invitation on table submitted invitation for user {public_identifier}')
#             submitted_invitation.to_csv('datasets/submitted_invitation.csv', index=0)

#             if pd.isna(family_offices_UK.loc[family_offices_UK.LinkedIn == public_identifier, 'conversation_urn'].iloc[0]):
#                 family_offices_UK = get_conversation_urn(api=api, sleeping_time=60)
    
def send_message_new_1st_connections(sleeping_time=60):

    api = autenticate_linkedin_API('gianluca')

    submitted_invitation = pd.read_csv('datasets/submitted_invitation.csv')
    family_offices_UK = pd.read_csv('family_offices_UK.csv')
    message = pd.read_csv('datasets/message.csv')
    submitted_call_to_action = pd.read_csv('datasets/submitted_call_to_action.csv')

    si_fo = pd.merge(submitted_invitation, family_offices_UK, how='left', left_on='profile_id', right_on='LinkedIn')
    si_fo_accepted_invitation = si_fo[si_fo.accepted_invitation == True]

    for nome, profile_urn, conversation_urn, profile_id in zip(si_fo_accepted_invitation.Nome, si_fo_accepted_invitation.profile_urn, si_fo_accepted_invitation.conversation_urn, si_fo_accepted_invitation.profile_id):
        
        if submitted_call_to_action.profile_id.isin([profile_id]).any():

            logger.info(f'already sent 1 message to {profile_id}')
            continue

        cta, code = utils_common.randomly_get_message(message_begin=message, type='cta')
        
        try:
            result = api.send_message(message_body=cta.format(nome), conversation_urn_id=conversation_urn)
            sleep(sleeping_time)
            if result == False:
                tool = 'conversation_urn'
            elif result  == True:
                logger.error(f"not sent message to {profile_id}")
                raise Exception
    
        except:
            result = api.send_message(message_body=cta.format(nome), recipients=[profile_urn])
            sleep(sleeping_time)
            if result == False:
                tool = 'profile_urn'
                
            elif result  == True:
                logger.error(f"not sent message to {profile_id}")
                raise Exception

        finally:

            submitted_call_to_action.loc[len(submitted_call_to_action)] = utils_common.create_row_subitted_cta(profile_id, message_code=code)
            submitted_call_to_action.to_csv('datasets/submitted_call_to_action.csv', index=0)
            logger.info(f'sent cta message {code} to {profile_id} using {tool}')



        










