from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator, UserAuthenticationStorageHelper
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatCommand

from typing import Callable, List, Tuple

import puns

USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

class Bot:
    def __init__(self, id, secret, channel, replyCsv, chatOut: Callable[[str], None]=print):
        global TARGET_CHANNEL
        
        self.id = id
        self.channel = channel
        self.secret = secret
        
        self.chatOut = chatOut
        
        self.replies = {}
        
        if replyCsv is not None:
            with open(replyCsv, 'r', newline='') as replyFile:
                sep = '|'
                replyCommands = { row[:row.index(sep)]:row[row.index(sep) + 1:] for row in replyFile.readlines() }
                
            self.replies = replyCommands

    async def on_ready(self, ready_event: EventData):
        print('Bot is ready.')
        
        await ready_event.chat.join_room(self.channel)
        
        print(f'Connected to {self.channel}.')
        
    async def on_message(self, msg: ChatMessage):
        self.chatOut(f'<b>{msg.user.name}</b>: {msg.text}')
        
        pun = await self.punner.process_message(msg)
        
        if pun:
            self.chatOut(f'<i>^ Replied with pun: {pun}</i>')
        
    async def on_reply_command(self, cmd: ChatCommand):
        reply = self.replies[cmd.name]
        
        await cmd.reply(reply)
        
        self.chatOut(f'<i>v Received command "{cmd.name}" and replied with "{reply[:10] + "..." if len(reply) > 10 else ""}"</i>')
        
    async def start(self, punner: puns.Punner):
        # Log in
        twitch = await Twitch(self.id, self.secret)
        
        self.twitch = twitch
        
        self.punner = punner

        helper = UserAuthenticationStorageHelper(twitch, USER_SCOPE, auth_generator_func=custom_auth_gen)
        
        await helper.bind()
        
        # Set up chat
        chat = await Chat(twitch)
        
        chat.register_event(ChatEvent.READY, self.on_ready)
        chat.register_event(ChatEvent.MESSAGE, self.on_message)
        
        for key in self.replies.keys():
            chat.register_command(key, self.on_reply_command)
        
        chat.start()
        
        self.chat = chat
        
    async def stop(self):
        self.chat.stop()
        await self.twitch.close()

async def custom_auth_gen(twitch: 'Twitch', scopes: List[AuthScope]) -> Tuple[str, str]:
    auth = UserAuthenticator(twitch, scopes, force_verify=True)
    
    # Set custom html
    with open('document.html') as doc:
        auth.document = doc.read()
    
    return await auth.authenticate()