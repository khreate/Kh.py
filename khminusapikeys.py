#valid_users = [" "]: can add to if statement str(message.author) in valid_users
import discord
import requests
import json
import random
import ibm_watson
import ibm_cloud_sdk_core

#Oxford Dictionary API requirements
app_id = '********'
app_key = '********'
language = 'en-us'
fields = 'definitions'

#OpenWeatherMap API requirements
a_key = '********'

#IBM Language Translator requirements
api_key = '********'
url_ibm = 'https://api.us-south.language-translator.watson.cloud.ibm.com/instances/********'
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('********')
language_translator = LanguageTranslatorV3(
    version='2020-05-01',
    authenticator=authenticator
)
language_translator.set_service_url(url_ibm)
language_translator.set_disable_ssl_verification(True)


def read_token():
    with open('token.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()
client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Game('>help for commands'))
    print('online')

@client.event
async def on_member_update(before, after):
    end = after.nick
    if end:
        if end.lower().count('khreator') > 0 or end.lower().count('kh.py') > 0:
            start = before.nick
            if start:
                await after.edit(nick = start)
            else:
                await after.edit(nick = 'There can only be one')

@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "welcome":
            await channel.send(f"""Welcome to the server, {member.mention}!""")

@client.event
async def on_message(message):
    id = client.get_guild(********)
    channels = ["bot-allowed", "current-kh-commands", "general", "bot-dump"]
    if str(message.channel) in channels:

        if message.content.find(">hi") != -1:
            await message.channel.send("I want to kill myself")

        elif message.content == ">users":
            await message.channel.send(f'''There are {id.member_count} members on this server.''')
        
        elif message.content.find('>delete') != -1:
            s = str(message.content)
            split = s.split()
            n = int(split[1])
            await message.channel.purge(limit = n + 1)
        
        elif message.content.find('>r') != -1:
            s = str(message.content)
            split = s.split()
            mi = int(split[1])
            ma = int(split[2])
            fin = random.randint(mi,ma)
            await message.channel.send(f'''Result of {mi}-{ma} random number: {fin}''')
        
        elif message.content.find('>help') != -1:
            embed = discord.Embed(colour = 16777215, title = 'Kh.py Commands', description = 'Work in progress bot by Khreator')
            embed.add_field(name = '>help', value = 'Displays all working commands and information about their usage')
            embed.add_field(name ='>hi', value = 'Kh.py will tell you it wants to die.')
            embed.add_field(name = '>users', value = 'Lists the number of users on the server.')
            embed.add_field(name = '>delete #', value = 'Deletes # number of messages in channel command was sent in')
            embed.add_field(name = '>r #', value = 'Creates a random number in range specified eg. `>r 1 15`')
            embed.add_field(name = '>define <string>', value = 'Defines a specified word using Oxford Dictionary, eg. `>define cow`')
            embed.add_field(name = '>weather <city,state>', value = 'Displays some temperature information about specified location eg. `>weather dallas,texas` or `>weather ontario,canada`')
            await message.channel.send(content = None, embed = embed)
        
        elif message.content.find('>define') != -1:
            s = str(message.content)
            word = s[8:]
            print(word)
            url = "https://od-api.oxforddictionaries.com/api/v2/entries/" + language + "/" + word.lower() + "?fields=" + fields
            r = requests.get(url, headers={"app_id": app_id, "app_key": app_key}) 
            print('code {}\n'.format(r.status_code))
            print('defining ' + word)
            t = json.dumps(r.json())
            l = json.loads(json.dumps(r.json()))
            f = l["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
            embed = discord.Embed(colour = discord.Colour.from_rgb(107, 230, 255), title = 'Oxford Dictionary - ' + word, description = str(f))
            await message.channel.send(content = None, embed = embed)

        elif message.content.find('>weather') != -1:
            s = str(message.content)
            inter = s[9:]
            t = inter.split(',')
            city = t[0]
            state = t[1]
            try:
                url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + ',' + state + '&units=imperial'
                r = requests.get(url + '&appid=' + a_key)
                print('code {}\n'.format(r.status_code))
                print(f'''Weather of {city}, {state}''')
                l = json.dumps(r.json())
                v = json.loads(l)
                print(v)
                currenttemp = v['main']['temp']
                low = v['main']['temp_min']
                high = v['main']['temp_max']
                weacon = v['weather'][0]['description']
                embed = discord.Embed(colour = discord.Colour.from_rgb(200, 0, 0), title = 'OpenWeatherMap - ' + city + ', ' + state, description = 'Weather Information')
                embed.add_field(name = 'Condition', value = str(weacon))
                embed.add_field(name = 'Current Temperature', value = str(currenttemp) + " degrees Fahrenheit")
                embed.add_field(name = "Today's low", value = str(low) + " degrees Fahrenheit")
                embed.add_field(name = "Today's high", value = str(high) + " degrees Fahrenheit")
                await message.channel.send(content = None, embed = embed)
            except:
                print('error')
                embed = discord.Embed(colour = discord.Colour.from_rgb(200, 0, 0), title = 'OpenWeatherMap', description = 'Failed with HTTP ' + ' code{}\n'.format(r.status_code))
                await message.channel.send(content = None, embed = embed)


    else:
        if message.content.find('>') != -1:
            print(f'''User: {message.author} tried to use command {message.content} in {str(message.channel)}, failed''')



client.run(token)
