from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope

USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

async def startup(id, secret):
    twitch = await Twitch(id, secret)

    auth = UserAuthenticator(twitch, USER_SCOPE, force_verify=False)
    
    with open('document.html') as doc:
        auth.document = doc.read()
        
    # this will open your default browser and prompt you with the twitch verification website
    token, refresh_token = await auth.authenticate()
    # add User authentication
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)