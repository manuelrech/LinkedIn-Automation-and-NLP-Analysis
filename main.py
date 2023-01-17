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

family_offices_UK, network_info, submitted_invitation, message, submitted_call_to_action, replies_note, replies_call_to_action, troubling_profiles = utils.setup_begging_datasets()

utils.create_message(type='note', text='hi there i am new to linkedin!', code='n0')
utils.create_message(type='note', text='hi i just signed up and trying to make connections!', code='n1')

family_offices_UK, network_info, submitted_invitation, message, troubling_profiles = utils.send_ifnvitations_note(
                                                                                                    api,
                                                                                                    10, 
                                                                                                    family_offices_UK, 
                                                                                                    network_info, 
                                                                                                    submitted_invitation, 
                                                                                                    message, 
                                                                                                    troubling_profiles)


family_offices_UK, network_info, submitted_invitation = utils.scan_for_1st_connections(api, 
                                                                            family_offices_UK, 
                                                                            network_info, 
                                                                            submitted_invitation)