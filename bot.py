#!/usr/sbin/python
import discord
from discord.ext import commands
import os
import requests
import json

tarkov_token = (os.getenv('MARKET'))
tarkov_url = 'https://tarkov-market.com/api/v1/'
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='$', description="bot used to check on items from tarkov marketplace", intents=intents)

def tarkov_item(item):
    response = requests.get(
        f'{tarkov_url}item?q={item}',
        headers={'x-api-key':tarkov_token}        
    )
    return response.json()

def curr_convert(trader_price, curr):
    if curr == '$':
        money = tarkov_item('dollar')['avg24hPrice']
    else:
        money = (tarkov_item('euro'))['avg24hPrice']

    return (trader_price * money)



#### Bot Functions ####

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity = discord.Game('Escape From Tarkov'))

@bot.command()
async def dump(ctx, item):
    response = requests.get(
        f'{tarkov_url}item?q={item}',
        headers={'x-api-key':tarkov_token}        
    )
    print(len(response.json()))
    print(response.json())

@bot.command()
async def item(ctx, item):
    raw = tarkov_item(item)
    for array in raw:
        avg24hrPrice = array['avg24hPrice']
        avg7daysPrice = array['avg7daysPrice']
        currency = array['traderPriceCur']
        if currency == '₽':
            traderPrice = array['traderPrice']
        else:
            traderPrice = curr_convert(array['traderPrice'],currency)


        if avg24hrPrice >= avg7daysPrice:
            trend = 'Trend is up '
        else:
            trend = "Trend is down"
        
        if traderPrice >= avg24hrPrice:
            sellto = 'Sell to Vendor'
            trader = array['traderName']
        else:
            sellto = 'Sell on Flea Market'
            trader = 'market'

        img = array['img']

        output = (f'avg 24hr price: {avg24hrPrice:,}  avg7daysPrice: {avg7daysPrice:,} traderPrice: {traderPrice:,} Trend: {trend} Sellto: {sellto} Trader: {trader} {img}')

        await ctx.send(output)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')



bot.run(os.getenv('TOKEN')) 