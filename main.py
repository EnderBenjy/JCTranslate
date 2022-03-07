import os
import datetime
import json
import discord
from discord.ext import commands
from keep_alive import keep_alive

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(";"),
    description='EnderTweet ^^',
    case_insensitive=False,
    intents=discord.Intents.all())

bot.remove_command('help')

bot.uptime = datetime.datetime.now()
bot.messages_in = bot.messages_out = 0
bot.region = 'Savoie, FR'


@bot.event
async def on_ready():
    print('Connecté comme {0} ({0.id})'.format(bot.user))

    # Load Modules
    modules = ['Translator']
    try:
        for module in modules:
            bot.load_extension('cogs.' + module)
            print('Loaded: ' + module)
    except Exception as e:
        print(f'Error loading {module}: {e}')

    print('Bot.....Activated')
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Game(name="Personnal test twitter bot"))


@bot.event
async def on_message(message):
    # Sent message
    if message.author.id == bot.user.id:
        if hasattr(bot, 'messages_out'):
            bot.messages_out += 1
    # Received message (Count only commands messages)
    elif message.content.startswith(';'):
        if hasattr(bot, 'messages_in'):
            bot.messages_in += 1

    await bot.process_commands(message)


@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(
                'Hi ! To display the help menu, use ;help !`'
            )
            break

@bot.command(name='help', aliases=['h'])
async def help(ctx, arg: str = ''):
    """Affiches l'aide"""
    embed = discord.Embed(title="EnderBot", colour=discord.Colour(0x7f20a0))

    avatar_url = str(bot.user.avatar_url)
    embed.set_thumbnail(url=avatar_url)
    embed.set_author(
        name="EnderTweet help",
        url=
        "https://discord.com/oauth2/authorize?client_id=945990955314601984&scope=bot&permissions=8",
        icon_url=avatar_url)
    embed.set_footer(text="EnderTweet by EnderBenjy")

    if arg.strip().lower() == '-a':
        # Full version
        embed.description = 'My prefix is `;`'
        with open('help.json', 'r') as help_file:
            data = json.load(help_file)
        data = data['full']
        for key in data:
            value = '\n'.join(x for x in data[key])
            embed.add_field(name=key, value=f"```{value}```", inline=False)
    else:
        # Short version
        embed.description = 'My prefix is `;`, Use ;help -a to get more informations on commands !'
        with open('help.json', 'r') as help_file:
            data = json.load(help_file)
        data = data['short']
        for key in data:
            embed.add_field(name=key, value=data[key])
    try:
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send(
            "I do not have the required permission to send embed here :\'('")


# All good ready to start!
keep_alive()
print('Starting Bot...')
bot.run(os.environ['TOKEN'])
