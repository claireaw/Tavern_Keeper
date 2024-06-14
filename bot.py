import discord
from discord import app_commands, Interaction
from pymongo import MongoClient
from pandas import DataFrame

intents = discord.Intents.default()
intents.message_content = True

cluster = MongoClient("")
db2 = cluster['']
collectionUsers = db2['']
collectionItems = db2['']
client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=))
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='you'))


@tree.command(name='setup', description='Setup with the bot', guild=discord.Object(id=))
async def setup(interaction):
    myquery = {"_id": interaction.user.id}
    if collectionUsers.count_documents(myquery) == 0:
        post = {"_id": interaction.user.id, "score": 0, "items": []}
        collectionUsers.insert_one(post)
        await interaction.response.send_message('User added', ephemeral=True)
    else:
        await interaction.response.send_message('User already exists', ephemeral=True)


# still trying to search for user in table
@tree.command(name='addpoint', description='Add a point to a user (staff)',
              guild=discord.Object(id=))
async def addPoint(interaction, user: str):
    myquery = {"_id": user}
    if collectionUsers.count_documents(myquery) == 1:
        collectionUsers.update_one(
            {'_id': user},
            {'$inc': {'score': 1}})
    else:
        await interaction.response.send_message("User does not exist", ephemeral=True)


@tree.command(name='additem', description='Add an item to the store (staff)',
              guild=discord.Object(id=))
async def additem(interaction, name: str, stats: str, price: int, count: int):
    myquery = {"name": name}
    if collectionItems.count_documents(myquery) == 0:
        post = {"name": name, "stats": stats, 'price': price, 'count': count}
        collectionItems.insert_one(post)
        await interaction.response.send_message("Item added", ephemeral=True)
    else:
        await interaction.response.send_message("Item already exists", ephemeral=True)


@tree.command(name='removeitem', description='Remove an item from the store (staff)',
              guild=discord.Object(id=))
async def removeitem(interaction, name: str):
    myquery = {"name": name}
    if collectionItems.count_documents(myquery) == 1:
        collectionItems.delete_one({'name': name})
        await interaction.response.send_message('Item removed', ephemeral=True)
    else:
        await interaction.response.send_message("Item did not exist, cannot remove", ephemeral=True)


@tree.command(name='seeitem', description='View an item in the store',
              guild=discord.Object(id=))
async def viewitem(interaction, name: str):
    myquery = {"name": name}
    if collectionItems.count_documents(myquery) == 1:
        result = collectionItems.find_one(myquery, {'_id': 0, 'name': 1, 'stats': 1, 'price': 1, 'count': 1})
        await interaction.response.send_message(str(result), ephemeral=True)
    else:
        await interaction.response.send_message("Item does not exist, cannot view", ephemeral=True)


@tree.command(name='seestore', description='View the items in the store',
              guild=discord.Object(id=))
async def seestore(interaction):
    z = []
    for x in collectionItems.find({}, {'_id': 0, 'name': 1, 'price': 1, 'count': 1}):
        z.append(x)
    await interaction.response.send_message(z, ephemeral=True)


@tree.command(name='myitems', description='View the items that you own',
              guild=discord.Object(id=))
async def myitems(interaction):
    x = collectionUsers.find_one({"_id": interaction.user.id}, {'items': 1})
    print(x['items'][0])
    await interaction.response.send_message(x['items'], ephemeral=True)


# if user has < amount needed to buy
@tree.command(name='buyitem', description='Purchse an item',
              guild=discord.Object(id=))
async def buyitem(interaction, name: str):
    myquery1 = {"name": name}
    myquery2 = {"name": name, 'count': 0}
    if collectionItems.count_documents(myquery1) == 1:
        if collectionItems.count_documents(myquery2) == 1:
            await interaction.response.send_message("No more copies of this item exist", ephemeral=True)
        elif collectionItems.count_documents(myquery2) != 1:
            myquery3 = {"_id": interaction.user.id}
            #price
            x = collectionItems.find_one(myquery1)
            y = collectionUsers.find_one(myquery3)
            comp1 = x['price']
            comp2 = y['score']
            if comp1 <= comp2:
                xname = x['name']
                xstats = x['stats']
                # take point value of item, inc by negative of that, not just 1
                collectionUsers.update_one({'_id': interaction.user.id},
                                           {'$push': {'items': {'name': xname, 'stats': xstats}}})
                collectionItems.update_one({'name': name},
                                           {'$inc': {'count': -1}})
                collectionUsers.update_one({'_id': interaction.user.id},
                                           {'$inc': {'score': -1}})
                await interaction.response.send_message("Item bought", ephemeral=True)
            else:
                await interaction.response.send_message("Invalid point amount", ephemeral=True)
    else:
        await interaction.response.send_message("Item does not exist", ephemeral=True)


intents = discord.Intents.default()
intents.message_content = True

token = open("./botToken", "r").read()

client.run(token)
