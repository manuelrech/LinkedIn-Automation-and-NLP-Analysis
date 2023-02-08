import sys
sys.path.append('/Users/manuel/Desktop/Linkedin')
import os
os.chdir('linkedin_gianluca')
from utils import utils_api, utils_selenium, utils_common
from utils.utils_chrome import utils_chrome
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('loggers/linkedin.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

utils_common.setup_correct_directory('Linkedin_gianluca') # change folder if you are using the script for different people

utils_common.setup_begging_datasets() # the first time the script runs this fixes folders

########################################################################################################################

# utils_common.repeat_times(3, utils_api.send_invitations_note, 40, 60)

# utils_common.repeat_times(3, utils_selenium.get_new_connections, 'ian-allison-438a4aaa')

# utils_chrome.add_manual_interaction(sheet_name = '1569CbCaM_vQ1sxJWHtPNbOHnbK-nfjMSt5KnUEoXKzE')

# utils_common.repeat_times(3, utils_api.send_message_new_1st_connections, 60)

# utils_selenium.send_in_mail_message()

########################################################################################################################

# TODO nuova lista mounir e gianluca