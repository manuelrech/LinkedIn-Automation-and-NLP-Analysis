## This project automates the interaction with people on linkedin and help grow network

All what is needed is a database of people to target that can be:
- imported from external csvs
- scraped using linkedin api (in next version)

In this version the csv files with people's linked need to have these mandatory columns: `['Name', 'LinkedIn_url']`. The second to interact using api and the first to send a personalized message with the right name (in next version also name will be automatically retrieved). 

The project is divided into 3 parts

### Sending connection invite + note
We send people a connection invite and a note to make the connection meaningful

This is done using the call in `main.py`
    
    utils_common.repeat_times(3, utils_api.send_invitations_note, api, 30, 60)

the first parameter is how many times the code is repeated (there are connection errow when you let the code run), the second is the function, the other are `*args` of the second function. 

### Fetching for 1st connections
Some of the people to which we have sent the invitation may accept it and therefore we want to update our database so that we keep track of accpeted invitations. 

The second call in `main.py` is 

    utils_common.repeat_times(3, utils_selenium.get_new_connections, 'ian-allison-438a4aaa', api)

the first parameter is how many times the code is repeated (there are connection errow when you let the code run), the second is the function, the other are `*args` of the second function. 

### Sending messages to 1st connections
People who accept invitation are targeted with a message 

The third call in `main.py` is 

    utils_common.repeat_times(3, utils_api.send_message_new_1st_connections, api, 60)

the first parameter is how many times the code is repeated (there are connection errow when you let the code run), the second is the function, the other are `*args` of the second function. 

### Sending inmail to those who do not accept invitation