# Discord-Pizza-Ordering-Bot

This is a Python Discord Bot that can order pizza and other stuff from Dominos that uses the Pizzapi Python libraray.
It's my submissions for the Discord Hack Week.
I wrote this in a few days and I kind of just learned Python so the code is probably pretty inefficient, and it crashes if you send too many requests which I'll try to fix later.

It uses these librarys:
- My slightly modified version of Jarvis Johnson's fork of gamagoris pizzapi python library: https://github.com/Isaac100/pizzapi
- luhn for credit card validation https://pypi.org/project/luhn/
- validate_email for email validation https://pypi.org/project/validate_email/
- discordpy of course https://pypi.org/project/discord.py/
- sqlite for storing user info
- pbwrap for posting the menu to pastebin https://pypi.org/project/pbwrap/

Theres also some things I'll add later like Canada support, adding multiple of the same item, and other stuff. If you have any suggestions please leave them in an issue here.

If you want to invite the bot heres the link: https://discordapp.com/oauth2/authorize?client_id=592764368261873819&scope=bot&permissions=117760

Just keep in mind it crashes often and probably wont be online much.
