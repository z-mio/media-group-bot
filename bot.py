import asyncio

from pyrogram import Client
from config.config import cfg
from log import logger, setup_logging
from utils.optimized_event_loop import setup_optimized_event_loop

setup_logging(debug=cfg.debug)
setup_optimized_event_loop()
loop = asyncio.new_event_loop()


class Bot(Client):
    def __init__(self):
        self.cfg = cfg

        super().__init__(
            f"{self.cfg.bot_token.split(':')[0]}_bot",
            api_id=self.cfg.api_id,
            api_hash=self.cfg.api_hash,
            bot_token=self.cfg.bot_token,
            plugins=dict(root="plugins"),
            proxy=self.cfg.proxy.dict_format,
            loop=loop,
        )

    async def start(self, **kwargs):
        logger.info("Bot开始运行...")
        await super().start()

    async def stop(self, *args):
        await super().stop()


if __name__ == "__main__":
    bot = Bot()
    bot.run()
