import asyncio
import traceback
from bot import Bot
from puns import Punner
import config as conf
import gui
import sys

async def main():
    config = conf.read_config()
    
    if config is None:
        print("Please enter the correct values into the empty config file.")
        input()
        return
    
    id = config['Client']['ID']
    secret = config['Client']['Secret']
    channel = config['User']['TargetChannel']
    
    punPercentage = int(config['User']['PunChancePercentage'])
    punFileCsv = 'puns.csv'
    
    window = gui.getwindow()
    
    bot = Bot(id, secret, channel, 'replies.csv', window.chatbox.append)
    
    punner = Punner(punPercentage, punFileCsv)
    
    await bot.start(punner)
    
    try:
        gui.rungui(window)
    finally:
        if not getattr(sys, 'frozen', False):
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            
        print('Stopping...')
        await bot.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        print(f'\033[31m{traceback.format_exc()}\033[0m')
        print("An error occurred. Press enter to exit.")
        input()