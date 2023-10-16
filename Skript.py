from typing import Generator, Optional
import discord 
import discord.channel as channel
import discord.guild as guild
from discord.guild import Guild
from dotenv import load_dotenv 
import os
import github
import requests
import asyncio



def configure():
    load_dotenv()

def checkUserExist(username):
    r = requests.get('https://api.github.com/users/' + username)
    if r.status_code == 200:
        return True
    else:
        return False

def checkRepoExist(username, repo):
    r = requests.get('https://api.github.com/repos/' + username + '/' + repo)
    if r.status_code == 200:
        return True
    else:
        return False
    
class MyDiscordBot(discord.Client):
    intents = discord.Intents.all()


    user= [] # 3er Tupel: (GitHub Username, Channel) - 4er tupel (GitHub Username, Channel, Anzahl Commits) ?
    repo= str

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        text_channel_list = []
        for guild in self.guilds:
            channels = guild.text_channels
        repo = channels

    async def repeatCheckRepo(self):
        while True:
            await self.write_in_channel(self.user, self.repo)
            await asyncio.sleep(10)

    
   # async def get_all_channels(self) -> Generator[guild.Guild, None, None]:
   #     return super().get_all_channels()
    
    async def send_message(ctx,channel_id: int,*,message):
        target_channel = MyDiscordBot.get_channel(channel_id)
        if target_channel is not None:
            await target_channel.send(message)
        else:
            await ctx.send('Channel not found')

    async def write_in_channel(self,user, repo):
        for user in user:
            target_channel = MyDiscordBot.get_channel(channel)
            repo= g.get_repo(repo)
            commits = repo.get_commits()
            if(commits.totalCount > user[3]):
                await target_channel.send(channel, message='New commit in ' + repo.name + ' from ' + user[0])
                self.user[3] = commits.totalCount
            
    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

        if message.author == self.user:
            return
        
        if message.content.startswith('!setRepo'):
            if message.content == '!setRepo ':
                await message.channel.send('Please enter a valid GitHub repo')
            else:
                arr = message.content.split(' ')[1:]
                if False==checkRepoExist(arr[0],arr[1]):
                    return await message.channel.send('Please enter a valid GitHub repo First type the username and then the repo name')
                else:
                    await message.channel.send('Repo added')
                    self.repo = github.get_repo(arr[0] + '/' + arr[1])


        if message.content.startswith('!hello' or '!Hello' or 'hallo' or 'Hallo' or 'hi' or 'Hi' or 'hey' or 'Hey'):
            await message.channel.send('Hello!')
        
        if message.content.startswith('!addUser '): #addUser
            if message.content == '!addUser ':
                await message.channel.send('Please enter a valid GitHub username')
            else:
                arr = message.content.split(' ')[1:]
                if False==checkUserExist(arr[0]):
                    return await message.channel.send('Please enter a valid GitHub username')
                else:
                    await message.channel.send('User added')
                    self.user.append((arr[0],None,None))
                    if len(arr) > 1:
                        await message.channel.send('Please enter only one GitHub username')
        
        if message.content.startswith('!removeUser '): #removeUser
            if message.content == '!removeUser ':
                await message.channel.send('Please enter a valid number for the user. To see the number, use !listUser')
            else:
                arr = message.content.split(' ')[1:]
                if len(arr) > 1:
                    await message.channel.send('Please enter only one number')
                else:
                    try:
                        self.user.pop(int(arr[0])-1)
                        await message.channel.send('User removed')
                    except:
                        await message.channel.send('Please enter a valid number for the user. To see the number, use !listUser')
        
        if message.content.startswith('!listUser'): #listUser
            await message.channel.send(self.user)
        
        if message.content.startswith('!giveUserChannel'): #giveUserChannel
            if message.content == '!giveUserChannel ' or message.content == '!giveUserChannel':
                await message.channel.send('Please enter a valid GitHub user number and channel name. To see the number, use !listUser')
            else:
                arr = message.content.split(' ')[1:]
                if len(arr) > 2:
                    await message.channel.send('Please enter only one number and channel name')
                else:
                    try:
                        await message.channel.send('User channel added')
                        self.user[int(arr[0])-1][1] = arr[1]
                    except:
                        await message.channel.send('Please enter a valid GitHub user number and channel name. To see the number, use !listUser')

        if message.content.startswith('!help'): #help
            await message.channel.send('\n!hello: Say hello to the bot\n!addUser: Add a GitHub user to the bot\n!removeUser: Remove a GitHub user from the bot\n!listUser: List all the GitHub users\n!giveUserRepo: Give a GitHub user a repo\n!giveUserRepoChannel: Give a GitHub user a channel\n!listChannel: List all the channels\n!help: List all the commands\n')

        if message.content.startswith('!listChannel' or '!listchannel' or '!ListChannel' or '!Listchannel'):
            for guild in self.guilds:
                channels = guild.text_channels
                for channel in channels:
                    await message.channel.send(channel.name)
        
    
            

            
class GitHubBridge(github.Github):
    def __init__(self):
        super().__init__(os.getenv('github_token'))
        self.user = self.get_user()
        self.repo = self.get_repo('DiscordBot')
        self.issue = self.repo.get_issue(1)
        self.issue.create_comment('Hello World')
        self.issue.edit(state='closed')
        self.issue.edit(state='open')
        self.issue.edit(state='closed')
      

def main():
    configure()
    intents = discord.Intents.all()
    client = MyDiscordBot(intents=intents)
    github = GitHubBridge()
    client.run(os.getenv('api_key'))


main()
