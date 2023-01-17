import utils
import os
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('loggers/linkedin.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

utils.setup_correct_directory()

api = utils.autenticate_linkedin_API()

family_offices_UK, network_info, submitted_invitation, message, submitted_call_to_action, troubling_profiles = utils.setup_begging_datasets()

utils.create_message(type='note', text='hi there i am new to linkedin!', code='n0')
utils.create_message(type='note', text='hi i just signed up and trying to make connections!', code='n1')
utils.create_message(type='call_to_action', text='this is the first message', code='c0')
utils.create_message(type='call_to_action', text='i would like make a few works', code='c1')
utils.create_message(type='call_to_action', text='may i disturb you?', code='c2')


utils.send_invitations_note(api,
                            5, 
                            family_offices_UK)


utils.scan_for_1st_connections(api, 
                                family_offices_UK)

utils.send_message_new_1st_connections(api)