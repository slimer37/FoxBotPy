from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

APP_ID = config['Client']['ID']
APP_SECRET = config['Client']['SECRET']
TARGET_CHANNEL = config['User']['TargetChannel']

USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

async def startup():
    twitch = await Twitch(APP_ID, APP_SECRET)

    auth = UserAuthenticator(twitch, USER_SCOPE, force_verify=False)
    
    with open('document.html') as doc:
        auth.document = doc.read()
        
    # this will open your default browser and prompt you with the twitch verification website
    token, refresh_token = await auth.authenticate()
    # add User authentication
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)