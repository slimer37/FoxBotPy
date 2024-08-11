import asyncio
import bot
import config

def main():
    id, secret, channel = config.read_config()
    asyncio.run(bot.startup(id, secret))

if __name__ == "__main__":
    main()