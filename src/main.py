import asyncio
import bot
import config as conf

def main():
    config = conf.read_config()
    
    if config is None:
        print("Please enter the correct values into the empty config file.")
        return
    
    id = config['Client']['ID']
    secret = config['Client']['Secret']
    channel = config['User']['TargetChannel']
    
    asyncio.run(bot.startup(id, secret, channel))

if __name__ == "__main__":
    main()