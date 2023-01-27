# Overview
This project automates the process of sending connection invites and notes, fetching 1st level connections, sending messages to new connections and sending inmails to those who do not accept the invitation. The automation is done using selenium and linkedin-api. The responses data is then analyzed with NLP using pre-trained RoBERTa in the transformers library of Huggingface to understand which messages were more effective


## Getting started
The project requires a database of people to target, which can be imported from external csvs or scraped using linkedin api (in next version). The current version requires csv files with people's linkedin urls and names, which are mandatory columns. The LinkedIn url is used to interact using the API, and the name is used to send a personalized message.

Project Structure
The project is divided into 3 parts:

- Sending connection invite + note
- Fetching 1st level connections
- Sending messages to new connections
- Sending inmails to those who do not accept the invitation

The automation process is done using the calls in main.py. Each call is made using the utils_common.repeat_times() function, which repeats the process multiple times to handle connection errors. The specific functions and arguments for each call are detailed in the comments of main.py.riteria when we fetch among the most recent connections


## Note
For privacy reasons i cannot disclose the beginning datasets, but you can create an example one by picking ten of your friends profile_id and create a csv, the folders should create as magic
