import discord
import shlex
import re
import logging
import logging.config
import logging.handlers

logger = logging.getLogger(__name__)
logger.addHandler(logging.handlers.RotatingFileHandler("bot.log", mode='a', backupCount=2))


class LilVi(discord.Client):
    prefix = "v!"
    re_channel = re.compile(r"^<#(\d+)>$")

    def __init__(self, **options):
        super().__init__(**options)
        self.activity = discord.Game(f"Prefix is {self.prefix}")
        self.selector_user = {
            "ping": self.hello,
            "echo": self.echo
        }

    async def on_ready(self):
        logging.info(f"Lil' Vi has logged in as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return  # No self responding

        if message.content.startswith(self.prefix):
            parts = shlex.split(message.content)
            command_str = self.extract_command(parts[0])
            command = self.selector_user.get(command_str, self.default)
            self.print_command(message, command_str)
            await command(message)
        else:
            return

    async def hello(self, msg):
        await send_reply(msg, f"Hello! Latency: {int(seconds_to_ns(self.latency))} ns")

    async def echo(self, msg):
        parts = split_command(msg.content)
        if len(parts) == 1:
            await send_reply(msg, parts[0])
        else:
            await self.send_to_channel(parts[0], parts[1])

    async def default(self, msg):
        logging.warning(f"Invalid command: {msg.content}")

    def print_command(self, msg, command):
        logging.info(f"Received {command} in channel {msg.channel.name} ({msg.channel.id}) from guild {msg.guild.name} "
                     f"({msg.guild.id})")
        logging.info(f"Command: {msg.content}")

    async def send_to_channel(self, channel_raw, msg):
        match = self.re_channel.match(channel_raw)
        try:
            channel_id = int(match.group(1))
            await self.send_to_channel_id(channel_id, msg)
        except discord.NotFound:
            logging.error(f"{channel_raw} is not a valid channel")
            return
        except IndexError:
            logging.error(f"{channel_raw} matching incorrectly")
            return

    async def send_to_channel_id(self, channel_id, msg):
        channel = await self.fetch_channel(channel_id)
        await channel.send(msg)

    def extract_command(self, prefixed_command):
        return prefixed_command.replace(self.prefix, "", 1)  # Only replace first occurrence of the prefix.


def split_command(s):
    parts = shlex.split(s)
    return parts[1:]  # cut the prefix


def seconds_to_ns(seconds):
    return seconds * 10 ** -9


async def send_reply(origin_msg, reply):
    logger.info(f"Replying in {origin_msg.channel} with \"{reply}\"")
    await origin_msg.channel.send(reply)


def main():
    token_file = open("token")
    token = token_file.read()
    lil_vi = LilVi()
    lil_vi.run(token)


if __name__ == '__main__':
    main()
