import random
from typing import Callable
from twitchAPI.chat import ChatMessage
import csv
import re

class Punner:
    def __init__(self, punChancePercentage, punFileCsv):
        
        with open(punFileCsv, 'r', newline='') as csvFile:
            self.pun_table: dict[str, str] = { row[0]:row[1] for row in csv.reader(csvFile) }
            self.pun_pattern = re.compile('|'.join(re.escape(key) for key in self.pun_table.keys()))
            
        self.chance = punChancePercentage / 100
        
    def _should_make_pun(self) -> bool:
        return random.random() < self.chance
    
    def _form_pun(self, message: str) -> str:
        if re.search(self.pun_pattern, message):
            return self.pun_pattern.sub(lambda match: self.pun_table[match.group(0)], message)
        else:
            return None
        
    async def process_message(self, msg: ChatMessage):
        if msg.text.startswith('!') or not self._should_make_pun(): return
        
        pun = self._form_pun(msg.text)
        
        if pun:
            await msg.reply(pun)
            
        return pun