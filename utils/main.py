import utils_api, utils_selenium, utils_common
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('loggers/linkedin.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

utils_common.setup_correct_directory('Linkedin') # change folder if you are using the script for different people

utils_common.setup_begging_datasets() # the first time the script runs this fixes folders

########################################################################################################################

# utils_common.repeat_times(3, utils_api.send_invitations_note, 40, 60)

# utils_common.repeat_times(3, utils_selenium.get_new_connections, 'ian-allison-438a4aaa')

# utils_common.repeat_times(3, utils_api.send_message_new_1st_connections, 60)

utils_selenium.send_in_mail_message()

########################################################################################################################

# TODO finish campaing gianluca
# TODO nuova lista mounir e gianluca