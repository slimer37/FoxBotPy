from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator, UserAuthenticationStorageHelper
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage

from typing import List, Tuple

USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
TARGET_CHANNEL = None

async def on_ready(ready_event: EventData):
    print('Bot is ready.')
    
    await ready_event.chat.join_room(TARGET_CHANNEL)
    
    print(f'Connected to {TARGET_CHANNEL}.')
    
async def on_message(msg: ChatMessage):
    print(f'{msg.user.name}: {msg.text}')

async def startup(id, secret, channel):
    
    global TARGET_CHANNEL
    
    TARGET_CHANNEL = channel

    # Log in
    twitch = await Twitch(id, secret)

    helper = UserAuthenticationStorageHelper(twitch, USER_SCOPE, auth_generator_func=custom_auth_gen)
    
    await helper.bind()
    
    # Set up chat
    chat = await Chat(twitch)
    
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    
    chat.start()
    
    try:
        input('Press ENTER any time to stop\n')
    finally:
        chat.stop()
        await twitch.close()

async def custom_auth_gen(twitch: 'Twitch', scopes: List[AuthScope]) -> Tuple[str, str]:
    auth = UserAuthenticator(twitch, scopes, force_verify=True)
    
    # Set custom html
    with open('document.html') as doc:
        auth.document = doc.read()
    
    return await auth.authenticate()