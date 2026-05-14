import asyncio
import traceback
from bot import Bot
from puns import Punner
from configparser import ConfigParser
import config as conf
import gui
import sys
import userdb
import datakeeper


async def main():
    if not conf.config_file_exists():
        conf.write_default_config()
        print('No config file was found. An empty one has been created. Please enter the correct values into it.')
        return

    config: ConfigParser = conf.read_config()

    id = config['Client']['ID']
    secret = config['Client']['Secret']
    channel = config['User']['TargetChannel']

    window = gui.getwindow()

    bot = Bot(id, secret, channel, 'replies.csv', window.chatbox.append)

    punner = Punner(config)

    await bot.start(punner)

    try:
        gui.rungui(window)
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
    finally:
        print('Stopping...')
        await bot.stop()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception:
        print(f'\033[31m{traceback.format_exc()}\033[0m')
        print('An error occurred. Press enter to exit.')
        raise
    finally:
        userdb.save()
        datakeeper.writeAll()
