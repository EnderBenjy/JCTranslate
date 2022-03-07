import json
import re
import googletrans
import discord
from discord.ext import commands


class Translator(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.translator = googletrans.Translator()

    def get_language(self, flag):
        with open("utils/languages.json", "r") as datafile:
            jsondata = json.loads(datafile.read())
            return jsondata.get(flag)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.count > 1:
            return
        language = self.get_language(reaction.emoji)
        if language:
            text = re.sub(
                "<@[0-9]{18}>",
                "@@@@",
                re.sub("<@![0-9]{18}>", "@@@@", reaction.message.content),
            )
            if (language not in googletrans.LANGUAGES
                    and language not in googletrans.LANGCODES):
                await reaction.message.channel.send(embed=discord.Embed(
                    title="Translation failed!", colour=0xFF0000))
            else:
                dest = str(language)
                text = str(text)
                print(dest)
                translated_text = self.translator.translate(text, dest).text
                for user_mention in reaction.message.mentions:
                    translated_text = re.sub("@@@@", user_mention.mention,
                                             translated_text, 1)
                embed = discord.Embed(
                    title=f"Translation to {language}  {reaction.emoji}",
                    description=translated_text,
                    colour=discord.Colour(0xA6A67A),
                )
                embed.set_footer(
                    text=f"Requested by @{user.name}#{user.discriminator}",
                    icon_url=user.avatar_url,
                )
                await reaction.message.channel.send(embed=embed)

    @commands.command()
    async def translate(self, ctx, language, *text):
        language = language.lower()
        if (language not in googletrans.LANGUAGES
                and language not in googletrans.LANGCODES):
            await ctx.send(embed=discord.Embed(title="Translation failed!",
                                               colour=0xFF0000))
        else:
            dest = str(language)
            text = str(text)
            print(dest)
            translated_text = self.translator.translate(text, dest).text[2:-2]
            embed = discord.Embed(
                title=f"Translation to {language}",
                description=translated_text,
                colour=discord.Colour(0xA6A67A),
            )
            embed.set_footer(
                text=
                f"Requested by @{ctx.author.name}#{ctx.author.discriminator}",
                icon_url=ctx.author.avatar_url,
            )
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Translator(client))
