import asyncio
from bot import Bot
import config as conf

async def main():
    config = conf.read_config()
    
    if config is None:
        print("Please enter the correct values into the empty config file.")
        return
    
    id = config['Client']['ID']
    secret = config['Client']['Secret']
    channel = config['User']['TargetChannel']
    
    bot = Bot(id, secret, channel)
    
    await bot.start()
    
    try:
        input('Press enter at any time to stop.\n')
    finally:
        print('Stopping...')
        await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())