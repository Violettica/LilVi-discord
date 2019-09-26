import discord

client = discord.Client()


def main():
    token_file = open("token")
    token = token_file.read()
    client.run(token)


@client.event
async def on_ready(self):
    print(f"Lil' Vi has logged in as {self.client.user}")


@client.event
async def on_message(self, message):
    if message.author == self.client.user:
        return  # No self responding

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")


if __name__ == '__main__':
    main()
