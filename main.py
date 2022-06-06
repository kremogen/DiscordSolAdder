import discord
from discord.ext import commands
from config import settings
import csv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)
channelId = 749953407350997125


@bot.event
async def on_ready():
    print('Я запущен!')


async def write_to_csv(discord_id, solana_address):
    exist = False
    with open('Wallet_binding.csv', 'r+', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if discord_id in row or solana_address in row:
                exist = True
                return False
        if not exist:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow((discord_id, solana_address))
            return True
        csvfile.close()


@bot.event
async def on_message(message):
    if len(message.content) == 44 and message.channel.id == channelId and message.author != bot.user:
        if await write_to_csv(str(message.author.id), message.content):
            await message.channel.send(f'Успешно добавлен!')
        else:
            await message.channel.send(f'Ты уже добавил свой кошелёк!')


bot.run(settings['token'])
