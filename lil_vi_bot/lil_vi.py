import discord
import shlex
import re


class LilVi(discord.Client):  # TODO: Change global bollocks to class
    prefix = "vi$"

    def __init__(self, **options):
        super().__init__(**options)


client = discord.Client()
prefix = "vi$"


def main():
    token_file = open("token")
    token = token_file.read()
    new_activity = discord.Game(f"Prefix is {prefix}")
    global client
    client.activity = new_activity
    client.run(token)


def split_command(s):
    parts = shlex.split(s)
    return parts[1:]  # cut the prefix


@client.event
async def on_ready():
    print(f"Lil' Vi has logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return  # No self responding

    if message.content.startswith(prefix):
        print(f"Received command: {message.content}")
    else:
        return

    # TODO: Change this to a dictionary switch
    selector = {
        f"{prefix}hello": lambda m: send_reply(m, "Hello!")

    }
    if message.content.startswith(f"{prefix}hello"):
        print(f"Hello World command from {message.channel}")
        await send_reply(message, "Hello!")
    elif message.content.startswith(f"{prefix}echo"):
        echo_msg = "Under construction! >m<"
        await send_reply(message, echo_msg)


async def send_reply(message, reply):
    print(f"Replying in {message.channel} with \"{reply}\"")
    await message.channel.send(reply)


async def invalid_command(command):
    pass


if __name__ == '__main__':
    main()
