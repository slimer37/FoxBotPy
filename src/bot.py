from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator, UserAuthenticationStorageHelper
from twitchAPI.type import AuthScope

from typing import List, Tuple

USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

async def custom_auth_gen(twitch: 'Twitch', scopes: List[AuthScope]) -> Tuple[str, str]:
    auth = UserAuthenticator(twitch, scopes, force_verify=True)
    
    # Set custom html
    with open('document.html') as doc:
        auth.document = doc.read()
    
    return await auth.authenticate()

async def startup(id, secret):
    twitch = await Twitch(id, secret)

    helper = UserAuthenticationStorageHelper(twitch, USER_SCOPE, auth_generator_func=custom_auth_gen)
    
    await helper.bind()