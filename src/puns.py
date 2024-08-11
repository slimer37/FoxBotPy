import random
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
        return self.pun_pattern.sub(lambda match: dict(self.pun_table)[match.group(0)], message)
        
    async def process_message(self, msg: ChatMessage):
        if not self._should_make_pun(): return
        
        await msg.reply(self._form_pun(msg.text))