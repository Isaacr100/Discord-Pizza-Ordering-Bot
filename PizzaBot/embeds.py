import discord

helpembed = discord.Embed(
    title = 'Commands (* = Required for order)',
    colour = 24465
)    
helpembed.add_field(
    name = 'P!name (First+Last Name) *', 
    value = "Sets the name for your profile. ex: 'John Doe'", 
    inline = False
)
helpembed.add_field(
    name = 'P!phone (Phone) *', 
    value = "Sets the phone for your profile. ex: '1234567890'", 
    inline = False
)
helpembed.add_field(
    name = 'P!email (E-mail) *', 
    value = "Sets the E-mail for your profile. ex: 'johndoe@gmail.com'", 
    inline = False
)
helpembed.add_field(
    name = 'P!address (Address) *', 
    value = "Sets the address for your profile. Use this exact format: **Street**, **City**, **State**, **ZIP Code** ex: '123 Main Street, Atlanta, Georgia, 30349' (Include commas)", 
    inline = False
)
helpembed.add_field(
    name = 'P!creditcard (Credit card, Expiration date, CVV, Zip code)', 
    value = "Sets the credit card for your account(Not required, you can pay with cash) ex: '4100123422343234 0115 777 90210' (**DONT** use commas)", 
    inline = False
)
helpembed.add_field(
    name = 'P!paytype (Cash/Credit)', 
    value = "Sets the payment type for your account, either cash or credit", 
    inline = False
)
helpembed.add_field(
    name = 'P!showme', 
        value = "Shows the current information about you that the bot has", 
        inline = False
)
helpembed.add_field(
    name = 'P!store', 
    value = "Displays the closest Domino's to you. I'll automatically use this one when you make an order", 
    inline = False
)
helpembed.add_field(
    name = 'P!menu', 
    value = "Displays the menu of your closest Domino's", 
    inline = False
)
helpembed.add_field(
    name = 'P!additem (Item Code)', 
    value = "Adds an item to your order. The code is the string of letters and numbers in brackets before each item on the menu", 
    inline = False
)
helpembed2 = discord.Embed(
    title = 'Commands P. 2',
    colour = 24465
)    
helpembed2.add_field(
    name = 'P!removeitem (Item Code)', 
    value = "Removes an item from your order. The code is the string of letters and numbers in brackets before each item on the menu", 
    inline = False
)
helpembed2.add_field(
    name = 'P!showorder', 
    value = "Shows the items in your order", 
    inline = False
)
helpembed2.add_field(
    name = 'P!placeorder', 
    value = "Places you order", 
    inline = False
)
helpembed2.add_field(
    name = 'P!orderprice', 
    value = "Shows the price of your order", 
    inline = False
)
helpembed2.add_field(
    name = 'P!clear', 
    value = "Clears your information", 
    inline = False
)

async def helpscreen(ctx):
    await ctx.author.send("Here's how I work. Commands like P!name and P!phone will add those details to your 'profile' which is stored with the bot.  Once you've added all the requred info to your profile, you can make an order. Here's a full list of my commands and what they do. (They're also all DM only so no one is snoopin' on your personal info)", embed=helpembed)    
    await ctx.author.send(embed=helpembed2)    

async def vals(ctx, tup):
    fix = list(tup)
    for i in range(len(fix)):
        if fix[i] is None or fix[i] == '':
            fix[i] = "Not set"

    embed = discord.Embed(
        title = 'Your info',
        colour = 24465
    )
    embed.add_field(
        name = 'First and Last Name', 
        value = f"{fix[1]}, {fix[2]}", 
        inline = False
    )
    embed.add_field(
        name = 'Phone', 
        value = fix[3], 
        inline = False
    )
    embed.add_field(
        name = 'E-mail', 
        value = fix[4], 
        inline = False
    )
    embed.add_field(
        name = 'Address', 
        value = fix[5], 
        inline = False
    )
    embed.add_field(
        name = 'Credit card info', 
        value = fix[6], 
        inline = False
    )
    await ctx.send(embed=embed)