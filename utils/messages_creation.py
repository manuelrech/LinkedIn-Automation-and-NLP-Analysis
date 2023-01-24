import utils_common
import logging
import os


if not 'loggers' in os.listdir():
            os.mkdir('loggers')


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('loggers/message_creation.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


utils_common.create_message(type='note', text='Hi {}, I\'m Gianluca, CEO of https://vaiuk.finance/, we work within the alternative and disruptive investments space. Judging from your profile, you have quite the experience in this field, as such I\'d like to join your network to exchange ideas and opportunities. Kind regards, Gianluca', code='n0')
utils_common.create_message(type='call_to_action', text='Dear {},\nLately it seems the world is jumping from one crisis to the next. From pandemic, to natural disasters, war and economic downturn. Market uncertainty has become the norm, and making resilient investments has become a pertinent challenge for our partners and the wider investment community.\nHowever, we at Virgil Alternative Investments ltd. have dedicated the past few years to study and specialise in uncertain markets and assets, supporting and advising a network of Investors with over $3.5 billion AUM in Alternative Investments.\nWe see opportunity where others see uncertainty, and we’d like you to join our community to share our investment opportunities and services with you.\nPlease feel free to book a call https://calendly.com/vaiuk with us so that we can discuss your suitability and so that you learn more about VAI UK.\nKind regards,\nGianluca', code='c0')
utils_common.create_message(type='call_to_action', text='Dear {},\nI\’m Gianluca the CEO & CIO of Virgil Alternative Investments Ltd. We specialise in Alternative Investments Advisory Services, supporting and advising a network of Investors with over $3.5 billion AUM.\nAfter reviewing your profile we would love to add your company to our growing network of Investors to access our investment opportunities and advisory services. We are working on a few great projects which you may be interested in, all of which are tailored for resilience during this market climiate.\nPlease feel free to book a call https://calendly.com/vaiuk with us so that we can discuss your suitability and so that you learn more about VAI UK.\nKind regards,\nGianluca', code='c1')
utils_common.create_message(type='call_to_action', text='Hi {},\nI am reaching out because I looked into your profile and see that your company is focused on investing in financial assets. My company, Virgil Alternative Investments specialises in advising investors within this space, with over $3.5 billion AUA.\nWe have shortlisted a list of opportunities which may be of interest to you, all of which are focused on resilience during this period of uncertainty.\nPlease feel free to book a call https://calendly.com/vaiuk with us so that we can discuss your suitability and so that you learn more about VAI UK.\nKind regards,\nGianluca', code='c2')
utils_common.create_message(type='call_to_action', text='Hi{},\nI am the CEO of Virgil Alternative Investments (VAI) ltd.\nOur company is dedicated to supporting forward thinking investors like yourself in making sound investment decisions in the most alternative of investments. To date, we have advised professional and institutional investors with over $3.5 billion in AUA on disruptive opportunities, and on how to navigate market uncertainty through diversification.\nWe have shortlisted a list of opportunities which may be of interest to you, all of which are focused on resilience during this period of uncertainty.\nI\’d love to schedule a quick call to discuss these opportunities or any synergies with yourself and VAI. Please feel free to book a call https://calendly.com/vaiuk with us so that we can discuss your suitability and so that you learn more about VAI UK.\nKind regards,\nGianluca', code='c3')

