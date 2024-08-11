import random
from twitchAPI.chat import ChatMessage
import re

class Punner:
    def __init__(self, punChancePercentage, punFileCsv):
        
        with open(punFileCsv, 'r', newline='') as csvFile:
            sep = '|'
            self.pun_table: dict[str, str] = { row[:row.index(sep)].lower():row[row.index(sep) + 1:] for row in csvFile.readlines() }
            self.pun_pattern = re.compile('|'.join(re.escape(key) for key in self.pun_table.keys()), re.IGNORECASE)
            
        self.chance = punChancePercentage / 100
        
    def _should_make_pun(self) -> bool:
        return random.random() < self.chance
    
    def replace_match(self, match):
        original_text = match.group(0)
        replacement_text = self.pun_table.get(original_text.lower(), original_text)

        # Match the case
        if original_text.isupper():
            return replacement_text.upper()
        elif original_text.islower():
            return replacement_text.lower()
        elif original_text.istitle():
            return replacement_text.capitalize()
        else:
            return replacement_text
    
    def _form_pun(self, message: str) -> str:
        if re.search(self.pun_pattern, message):
            return self.pun_pattern.sub(self.replace_match, message)
        else:
            return None
        
    async def process_message(self, msg: ChatMessage):
        if msg.text.startswith('!') or not self._should_make_pun(): return
        
        pun = self._form_pun(msg.text)
        
        if pun:
            await msg.reply(pun)
            
        return pun