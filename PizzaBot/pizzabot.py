import discord
from discord.ext import commands
from discord.ext.commands import *
from discord.utils import find
from validate_email import validate_email
from luhn import *
import embeds
import data
import pizzadata

client = commands.Bot(command_prefix = 'P!')
client.remove_command("help")

@client.event
async def on_ready():
    data.create()
    await client.change_presence(activity=discord.Game(name=f"P!help | Serving pizza in {len(client.guilds)} servers"), status=discord.Status.online)
    print("Bot Ready")

@client.command(pass_context=True)
async def help(ctx):
    await embeds.helpscreen(ctx)
    if ctx.message.guild is not None:
        await ctx.send(f"{ctx.author.mention} I sent you a DM!")

@client.command(pass_context=True)
@dm_only()
async def name(ctx, fname="", lname=""):
    if fname.isalpha() and lname.isalpha():
        data.setname(ctx, fname, lname)
        await ctx.send(f'Set name to {fname} {lname}')
    else:
        await ctx.send('Invalid name, remember put your first and last name')

@client.command(pass_context=True)
@dm_only()
async def phone(ctx, phone=""):
    if (len(phone)==10) and (phone.isnumeric()):
        data.setphone(ctx, phone)
        await ctx.send(f'Set phone to {phone}')
    else:
        await ctx.send("Invalid phone number, remember no dashes")

@client.command(pass_context=True)
@dm_only()
async def address(ctx, *, addr=""):
    res = addr.split(', ')
    if len(res)==4 and res[3].isnumeric() and len(res[3])==5:
        data.setaddress(ctx, addr)
        await ctx.send(f"Set address to {addr}")
    else:
        await ctx.send("Invalid address, do P!help to see the exact format and remember to use commas")
@client.command(pass_context=True)
@dm_only()
async def email(ctx, mail=""):
    if validate_email(mail):
        data.setemail(ctx, mail)
        await ctx.send(f'Set email to {mail}')
    else:
        await ctx.send("Invalid email")

@client.command(pass_context=True)
@dm_only()
async def showme(ctx):
    await embeds.vals(ctx, data.showvals(ctx))

@client.command(pass_context=True)
@dm_only()
async def store(ctx):
    st = data.getaddress(ctx)
    if st:
        opn = pizzadata.storedata(ctx, st)
        if not opn:
            await ctx.send("Unfortunately there are no nearby stores open")
        else:
            await ctx.send(opn)
    else:
        await ctx.send("You haven't set your address yet. Do P!help to see how to do that")

@client.command(pass_context=True)
@dm_only()
async def menu(ctx):
    st = data.getaddress(ctx)
    if st:
        menu = pizzadata.menudata(ctx, st)
        if not menu:
            await ctx.send("Unfortunately there are no nearby stores open that I can get a menu from")
        else:
            url = data.pastemenu(menu)
            await ctx.send(f"Here's a link to the menu: {url}")
    else:
        await ctx.send("You haven't set your address yet, so there are no stores I can get a menu from. Do P!help to see how to do that")

@client.command(pass_context=True)
@dm_only()
async def creditcard(ctx, card='', exp='', cvv='', zipc=''):
    if all((exp.isnumeric() and len(exp)==4, cvv.isnumeric() and (len(cvv)==3 or len(cvv)==4), zipc.isnumeric() and len(zipc)==5, verify(card))):
        data.setcredit(ctx, card, exp, cvv, zipc)
        await ctx.send("Set credit card info")
    else:
        await ctx.send("Invalid credit card or unaccepted type, do P!help to see the format")

@client.command(pass_context=True)
@dm_only()
async def clear(ctx):
    data.clear(ctx)
    await ctx.send("Cleared your data")

@client.command(pass_context=True)
@dm_only()
async def additem(ctx, code=''):
    if not code =='':
        x = data.showvals(ctx)
        if data.vcust(x):
            ad = x[5]
            menu = pizzadata.getmenu(ctx, ad)
            if menu:
                valid = menu.verify(code)
                if valid:
                    if data.additem(ctx, code):
                        await ctx.send(f"Added {valid['Name']} for ${valid['Price']}")
                    else:
                        await ctx.send("You've already added that item")
                else:
                    await ctx.send("That item was not found") 
            else:
                await ctx.send("Unfortunately there are no nearby stores open that I can get a menu from, so I can't add an item")
        else:
            await ctx.send("You dont have all the required info to start an order")
    else:
        await ctx.send("You must enter an item code, they're in the brackets on the menu")

@client.command(pass_context=True)
@dm_only()
async def removeitem(ctx, code=''):
    if not code =='':
        x = data.showvals(ctx)
        if data.vcust(x):
            if data.removeitem(ctx, code):
                await ctx.send("Removed that item")
            else:
                await ctx.send("That's not an item on your order")
        else:
            await ctx.send("You dont have all the required info to start an order")
    else:
        await ctx.send("You must enter an item code, they're in the brackets on the menu")

@client.command(pass_context=True)
@dm_only()
async def paytype(ctx, typ=''):
    if typ.lower()=='cash':
        data.setpaytype(ctx, typ)
        await ctx.send("Set pay type to cash")
    elif typ.lower()=='credit':
        if data.checkcredit(ctx):
            data.setpaytype(ctx, typ)
            await ctx.send("Set pay type to credit")
        else:
            await ctx.send("You don't have a credit card on file")
    else:
        await ctx.send("Invalid type, choose either cash or credit")

@client.command(pass_context=True)
@dm_only()
async def orderprice(ctx):
    x = data.showvals(ctx)
    if data.vcust(x):
        if pizzadata.storeopen(ctx, x[5]):
            price = pizzadata.orderprice(ctx, x)
            if not price:
                await ctx.send("Your order is empty")
            else:
                await ctx.send(f'${price}')
        else:
            await ctx.send("Unfortunately there are no nearby stores open, so I can't check the price")
    else:
        await ctx.send("You dont have all the required info to start an order") 

@client.command(pass_context=True)
@dm_only()
async def placeorder(ctx):
    x = data.showvals(ctx)
    if data.vcust(x):
        if pizzadata.storeopen(ctx, x[5]):
            if x[8]=='cash':
                order = pizzadata.placeorder(ctx, x)
                if not order:
                    await ctx.send("Your order is empty, or something else went wrong")
                else:
                    if 'StatusItems' in order['Order']:
                        if {'Code': 'BelowMinimumDeliveryAmount'} in order['Order']['StatusItems']:
                            await ctx.send("Your order was below the minimum delivery amount for your store, this is usually $13-$16 for most stores")
                        elif {'Code': 'CashLimitExceeded'} in order['Order']['StatusItems']:
                            await ctx.send("Your order is above the cash limit for this store")
                    elif order['Status']==-1:
                        await ctx.send('There was an error with your order') 
                    else:
                        await ctx.send("Your order should be placed, to make sure go to this link and put in the phone number you used on the order https://www.dominos.com/en/pages/tracker/?lang=en#!/track/order/")
                        data.clearorder(ctx)
            elif x[8]=='credit':
                card = data.checkcredit(ctx)
                if card:
                    order = pizzadata.placeorder(ctx, x, card)
                    if not order:
                        await ctx.send("Your order is empty, or something elsewent wrong")
                    else:
                        if 'StatusItems' in order['Order']:
                            if {'Code': 'BelowMinimumDeliveryAmount'} in order['Order']['StatusItems']:
                                await ctx.send("Your order was below the minimum delivery amount for your store, this is usually $13-$16 for most stores")
                        elif order['Status']==-1:
                            await ctx.send("There was an error with your order, most likely your credit card wasn't accepted.") 
                        else:
                            await ctx.send("Your order should be placed, to make sure go to this link and put in the phone number you used on the order https://www.dominos.com/en/pages/tracker/?lang=en#!/track/order/")
                            data.clearorder(ctx)
                else:
                    await ctx.send("Your paytype is set to credit, but you don't have a credit card on file")
            else:
                await ctx.send("You haven't set a payment type yet, do P!help to see how to do that.")              
        else:
            await ctx.send("Unfortunately there are no nearby stores open, so I can't place an order")
    else:
        await ctx.send("You dont have all the required info to start an order")  

@client.command(pass_context=True)
@dm_only()
async def showorder(ctx):
    items=data.showorder(ctx)
    if not items:
        await ctx.send("Your order is empty")
    else:
        l=''
        for x in items:
            l+=f'{x}\n'
        l+='Check the menu to see the names and prices of these items'
        await ctx.send(l)

@client.event
async def on_guild_join(guild):
    await client.change_presence(activity=discord.Game(name=f"P!help | Serving pizza in {len(client.guilds)} servers"), status=discord.Status.online)
    general = find(lambda x: x.name == 'general', guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(f"Hello {guild.name}! Do P!help and I'll DM you with info about how to make an order!")

@client.event
async def on_guild_remove(guild):
    await client.change_presence(activity=discord.Game(name=f"P!help | Serving pizza in {len(client.guilds)} servers"), status=discord.Status.online)

client.run(TOKEN)
