import asyncio
from bot import Bot
from puns import Punner
import config as conf

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
    
    bot = Bot(id, secret, channel, 'replies.csv')
    
    punner = Punner(punPercentage, punFileCsv)
    
    await bot.start(punner)
    
    try:
        input('Press enter at any time to stop.\n')
    finally:
        print('Stopping...')
        await bot.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f'\033[31m{e}\033[0m')
        print("An error occurred. Press enter to exit.")
        input()