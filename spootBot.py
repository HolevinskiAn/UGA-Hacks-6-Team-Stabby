# bot.py
import sys
import os
import random
import discord
import pandas as pd
import numpy as np
from dotenv import load_dotenv

from discord.ext import commands
from discord.utils import get

load_dotenv()
TOKEN = 'NzMxNjAzNjgyNjUwNjIwMDI0.XwodBg.TbnmD_YmjoDFuNfy4oy8Hlv0w50'
GUILD = 'ugaSpootBotTester'

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user.name} has connected to the following guild:\n'
        f'{guild.name}(id:{guild.id})'
    )

@bot.event
async def on_member_join(member):
    await member.create.dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to our glorious game of spooting!'
    )

@bot.command(brief="Use this command to sign up for the spooting game", name='register')
async def register(ctx):
    user = ctx.message.author.id
    newUser = True
    #checks if user is already in game
    spootFile = pd.read_csv('spootGame.csv')

    s = spootFile.columns.values.tolist()
    for value in s:
        if str(user) == value:
            await ctx.send(f'{ctx.message.author.mention}'+", you are already a player!")
            newUser = False
        #if
    #for
    if newUser:
        noob = pd.DataFrame({str(user):[0, 0]})
        spootFile = spootFile.join(noob)
        spootFile.to_csv('spootGame.csv', index=False)
        spoot_welcomes = ['Ready,set, SPOOT!', 'May the odds be in your favor',
            ('Dont get caught!'),
        ]

        user = ctx.message.author
        role = get(user.guild.roles, name = "TargetSpooter")
        await user.add_roles(role)

        response = random.choice(spoot_welcomes)
        await ctx.send(f'{ctx.message.author.mention}'+' '+response)
    #if

@bot.command(brief="Use this command to spoot people", name='spoot')
async def spoot(ctx,*args):
    user = ctx.message.author.id
    existingUser=False
    spootFile = pd.read_csv('spootGame.csv')
    s = spootFile.columns.values.tolist()
    for value in s:
        if str(user) == value:
            existingUser = True
        #if
    #for
    validTarget=False
    target = str(args[0])
    target = target[3:len(target)-1]

    for value in s:
        if target == value:
            validTarget = True
        #if
    #for
    if not existingUser:
        await ctx.send(f'{ctx.message.author.mention}'+", you are NOT a player!")
    elif len(args) != 1:
        await ctx.send(f'{ctx.message.author.mention}'+", please use format [!spoot] [@player]")
    elif not validTarget:
        await ctx.send(f'{ctx.message.author.mention}'+", the person you've spooted is not a player. Please try again.")
    else:
        await ctx.send(f'{ctx.message.author.mention}'+", congradulations! You've spooted someone!")
        #increment spooters score
        data = spootFile.pop(str(user))
        data[0] = int(data[0]) + 1

        player1 = pd.DataFrame({str(user): data})
        spootFile = spootFile.join(player1)

        #increment person spooted hit score
        data = spootFile.pop(target)
        data[1] = int(data[1]) + 1
        player2 = pd.DataFrame({target: data})
        spootFile = spootFile.join(player2)
        spootFile.to_csv('spootGame.csv', index=False)

@bot.command(brief="Use this command to leave the spooting game", name='leave')
async def leave(ctx):
    user = str(ctx.message.author.id)
    spootFile = pd.read_csv('spootGame.csv')

    bye = spootFile.pop(user)
    spootFile.to_csv('spootGame.csv', index=False)

    remove = ctx.message.author
    role = get(remove.guild.roles, name = "TargetSpooter")
    await remove.remove_roles(role)

    await ctx.send(f'{ctx.message.author.mention}'+", you have been removed from game. Come again soon!")

@bot.command(brief="Use this command to see your score in the spooting game", name='stats')
async def stats(ctx):
    user = str(ctx.message.author.id)
    spootFile = pd.read_csv('spootGame.csv')

    view = spootFile.pop(user)
    await ctx.send(f'{ctx.message.author.mention}'+", you have spooted " + str(view[0]) + " time(s) "
         + "and have been spooted " + str(view[1]) + " time(s)!")

@bot.command(brief="Use this command to modify the form links",name="forms")
async def forms(ctx, *args):
    correctSyn = True;

    try:
        formsLibr = pd.read_csv('formsLib.csv')
        fileExist = False
        f = formsLibr.columns.values.tolist()
        if args[0] == 'list':
            await ctx.send(f'{ctx.message.author.mention} Here is the list you requested: ' + str(f))
        else:
            for value in f:
                if str(args[1]) == value:
                    fileExist = True;
                #if
            #for
            if str(args[0]) == "get" and len(args) == 2 and fileExist:
                form = formsLibr.pop(str(args[1]))
                await ctx.send(f'{ctx.message.author.mention} Your form: ' +
                    str(form[0]))
            elif str(args[0]) == "set" and len(args) == 3 and not fileExist:
                newForm = pd.DataFrame({str(args[1]):[str(args[2])]})
                formsLibr = formsLibr.join(newForm)
                formsLibr.to_csv('formsLib.csv', index=False)
                await ctx.send(f'{ctx.message.author.mention}, you have set a new form!')
            elif str(args[0]) == "drop" and len(args) == 2 and fileExist:
                form = formsLibr.pop(str(args[1]))
                formsLibr.to_csv('formsLib.csv', index=False)
                await ctx.send(f'{ctx.message.author.mention}, you have dropped a form!')
            elif str(args[0]) == "replace" and len(args) == 3 and fileExist:
                form = formsLibr.pop(str(args[1]))
                form[0] = str(args[2])
                update = pd.DataFrame({str(args[1]):form})
                formsLibr = formsLibr.join(update)
                formsLibr.to_csv('formsLib.csv', index=False)
                await ctx.send(f'{ctx.message.author.mention}, you have replaced a form!')
            else:
                correctSyn = False
                print(correctSyn)
        #else
    except:
        correctSyn = False
    else:
        if not correctSyn:
            await ctx.send(f'{ctx.message.author.mention}, invalid format. Please use one of following formats: \n' +
                '[!forms] [list] \n' +
                '[!forms] [get/drop] \n' +
                '[!forms [set/replace] [formName] [URL] \n'
                )


@bot.command(brief="Use this command to kill me :(", name='off')
async def off(ctx):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.send('You have successfully killed me. Well played.')
        sys.exit()
    else:
        await ctx.send(f'{ctx.message.author.mention} is the imposter!')


bot.run(TOKEN)
