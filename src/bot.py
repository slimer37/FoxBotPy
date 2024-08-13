from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator, UserAuthenticationStorageHelper
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatCommand

from typing import Callable, List, Tuple

import userdb

import puns

USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

class Bot:
    def __init__(self, id, secret, channel, replyCsv, chatOut: Callable[[str], None]=print):
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
        print(f'Bot is ready. Attempting to connect to {self.channel}...')
        
        nojoin = await ready_event.chat.join_room(self.channel)
        
        if len(nojoin) == 0: print(f'Connected to {self.channel}.')
        else: print('Timed out.')
        
    async def on_message(self, msg: ChatMessage):
        ignored = userdb.user_exists(msg.user.id)
        
        self.chatOut(('(ignored) ' if ignored else '') + f'<b>{msg.user.name}</b>: {msg.text}')
        
        # ignore stored users
        if ignored: return
        
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
            
        chat.register_command('ignore', self.add_to_ignore_list)
        chat.register_command('unignore', self.remove_from_ignore_list)
        
        chat.start()
        
        self.chat = chat
        
    async def stop(self):
        self.chat.stop()
        await self.twitch.close()
        
    async def add_to_ignore_list(self, cmd: ChatCommand):
        if userdb.add_user(cmd.user.id):
            self.chatOut(f'<i>Ignored {cmd.user.name}</i>')
            await cmd.reply('Ignored.')
        else:
            self.chatOut(f'<i>{cmd.user.name} is already ignored.</i>')
        
    async def remove_from_ignore_list(self, cmd: ChatCommand):
        if userdb.remove_user(cmd.user.id):
            await cmd.reply('Unignored.')
            self.chatOut(f'<i>Unignored {cmd.user.name}</i>')
        else:
            self.chatOut(f'<i>{cmd.user.name} is already not ignored.</i>')
            
        

import sys
import os

async def custom_auth_gen(twitch: 'Twitch', scopes: List[AuthScope]) -> Tuple[str, str]:
    auth = UserAuthenticator(twitch, scopes, force_verify=True)
    
    if getattr(sys, 'frozen', False):
        path = os.path.join(sys._MEIPASS, "document.html")
    else:
        path = "document.html"
    
    # Set custom html
    with open(path) as doc:
        auth.document = doc.read()
    
    return await auth.authenticate()