import discord
import shlex
import re


async def send_reply(message, reply):
    print(f"Replying in {message.channel} with \"{reply}\"")
    await message.channel.send(reply)


class LilVi(discord.Client):  # TODO: Change global bollocks to class
    prefix = "vi$"

    def __init__(self, **options):
        super().__init__(**options)
        self.activity = discord.Game(f"Prefix is {self.prefix}")

    async def on_ready(self):
        print(f"Lil' Vi has logged in as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return  # No self responding

        if message.content.startswith(self.prefix):
            print(f"Received command: {message.content}")
        else:
            return

        # TODO: Change this to a dictionary switch
        selector = {
            f"{self.prefix}hello": lambda m: send_reply(m, "Hello!")

        }
        if message.content.startswith(f"{self.prefix}hello"):
            print(f"Hello World command from {message.channel}")
            await send_reply(message, "Hello!")
        elif message.content.startswith(f"{self.prefix}echo"):
            echo_msg = "Under construction! >m<"
            await send_reply(message, echo_msg)





def split_command(s):
    parts = shlex.split(s)
    return parts[1:]  # cut the prefix


async def send_reply(message, reply):
    print(f"Replying in {message.channel} with \"{reply}\"")
    await message.channel.send(reply)


def main():
    token_file = open("token")
    token = token_file.read()
    lil_vi = LilVi()
    lil_vi.run(token)


if __name__ == '__main__':
    main()
