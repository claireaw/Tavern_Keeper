import discord
from discord import app_commands, Interaction
from pymongo import MongoClient
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

cluster = MongoClient("")
db2 = cluster['']
collectionUsers = db2['']
collectionItems = db2['']
client = discord.Client(intents=intents)
is_client_running = False

tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    global is_client_running

    if not is_client_running:
        await tree.sync(guild=discord.Object(id=))
        print(f'{client.user} has connected to Discord!')
        await client.change_presence(activity=discord.Game(name="Poker Night at the Inventory"))


@commands.cooldown(rate=1, per=5, type=commands.BucketType.guild)
@tree.command(name='setup', description='Setup with the bot', guild=discord.Object(id=))
async def setup(interaction, name: str):
    myquery = {"_id": interaction.user.id}
    myquery2 = {"name": name}
    # if there's not a user with the same user id or same username, create a new user in the table
    if collectionUsers.count_documents(myquery) == 0:
        if collectionUsers.count_documents(myquery2) == 0:
            post = {"_id": interaction.user.id, "score": 0, 'username': name, "items": []}
            collectionUsers.insert_one(post)
            await interaction.response.send_message('User added', ephemeral=True)
        else:
            await interaction.response.send_message('Username already exists, please try again', ephemeral=True)
    else:
        await interaction.response.send_message('User already exists', ephemeral=True)


@tree.command(name='addpoint', description='Add a point to a user (staff)',
              guild=discord.Object(id=))
@app_commands.checks.has_role('staff')
async def addPoint(interaction, name: str):
    myquery = {"name": name}
    if collectionUsers.count_documents(myquery) == 1:
        collectionUsers.update_one(myquery, {'$inc': {'score': 1}})
        await interaction.response.send_message("Point added", ephemeral=True)
    else:
        await interaction.response.send_message("User does not exist", ephemeral=True)


@tree.command(name='seeitem', description='Inspect an item in the store',
              guild=discord.Object(id=))
async def viewitem(interaction, name: str):
    myquery = {"name": name}
    z = []
    if collectionItems.count_documents(myquery) == 1:
        for x in collectionItems.find(myquery, {'_id': 0, 'name': 1, 'rarity': 1, 'url': 1, 'price': 1}):
            z.append(
                'Name: ' + x['name'] + '. Rarity: ' + str(x['rarity']) + '. Price: ' + str(
                    x['price']) + ' point(s)' + '. URL: ' + str(x['url']))
        await interaction.response.send_message(z[0], ephemeral=True)
    else:
        await interaction.response.send_message("Item does not exist, cannot view", ephemeral=True)


@tree.command(name='seestore', description='View the items in the store',
              guild=discord.Object(id=))
async def seestore(interaction):
    z = []
    await interaction.response.defer()
    for x in collectionItems.find({'count': {'$gt': 0}}, {'_id': 0, 'name': 1, 'rarity': 1, 'price': 1}):
        z.append('Name: ' + x['name'] + '. Rarity: ' + str(x['rarity']) + '. Price: ' + str(x['price']) + ' point(s).')

    count = collectionItems.count_documents({'count': {'$gt': 0}})
    for i in range(count):
        await interaction.channel.send(z[i])
    await interaction.followup.send('ASTRAL MERCHANT:')


@tree.command(name='myitems', description='View the items that you own',
              guild=discord.Object(id=))
async def myitems(interaction):
    myquery = {"_id": interaction.user.id}
    z = []
    for x in collectionUsers.find(myquery, {'_id': 0, 'items.name': 1, 'items.rarity': 1}):
        z.append(str(x['items']))
    await interaction.response.send_message(z.pop(0), ephemeral=True)


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
            x = collectionItems.find_one(myquery1)
            y = collectionUsers.find_one(myquery3)
            comp1 = x['price']
            comp2 = y['score']
            if comp1 <= comp2:
                xname = x['name']
                xrarity = x['rarity']
                collectionUsers.update_one({'_id': interaction.user.id},
                                           {'$push': {'items': {'name': xname, 'rarity': xrarity}}})
                collectionItems.update_one({'name': name},
                                           {'$inc': {'count': -1}})
                collectionUsers.update_one({'_id': interaction.user.id},
                                           {'$inc': {'score': -1 * comp1}})
                await interaction.response.send_message("Item bought", ephemeral=True)
            else:
                await interaction.response.send_message("Invalid point amount", ephemeral=True)
    else:
        await interaction.response.send_message("Item does not exist", ephemeral=True)


@tree.command(name='whoami', description='View details about your market data',
              guild=discord.Object(id=))
async def whoami(interaction):
    myquery = {"_id": interaction.user.id}
    z = []
    # if there's a user with this id
    if collectionUsers.count_documents(myquery) == 1:
        for x in collectionUsers.find(myquery, {'_id': 0, 'name': 1, 'score': 1}):
            z.append('Username: ' + str(x['name']) + '. Points: ' + str(x['score']) + ' point(s).')
        await interaction.response.send_message(z, ephemeral=True)
    else:
        await interaction.response.send_message('User does not exist, please run /setup to join the market',
                                                ephemeral=True)


@tree.command(name='announce', description='Announce changes to the store (staff)',
              guild=discord.Object(id=))
@app_commands.checks.has_role('staff')
async def announce(interaction):
    await interaction.response.send_message("The Astral Merchant has been updated!")


@tree.command(name='helpme', description='View commands',
              guild=discord.Object(id=))
async def helpme(interaction):
    await interaction.response.defer()
    await interaction.channel.send('/setup: Join the Astral Merchant system')
    await interaction.channel.send('/seestore: See the items currently available for sale')
    await interaction.channel.send('/seeitem: See information about a specifc item')
    await interaction.channel.send('/buyitem: Purchase a specifc item from the shop')
    await interaction.channel.send('/myitems: See your purchased items')
    await interaction.channel.send('/whoami: See details about your Astral Merchant setup')
    await interaction.followup.send('COMMANDS:')

intents = discord.Intents.default()
intents.message_content = True

token = open("./botToken", "r").read()

client.run('')
