import sys
import discord
import re
from yaml import safe_load, safe_dump

# Settings. Modify these.
token = 'OTQ2NTcxOTMzOTMwMTI3Mzkx.Yhgpzw.jbW1M-Lmphsg-izBiPlTFoqYdlc'
guild_id = 943194908255215716
admin_role_id = 943195430118895637
# role_id = 946573117784985640
anonchan_id = 946573451781619714 # The anonymous board.
logger_id = 946575471636791406 # The GM board that lets you see posters.


client = discord.Client()

@client.event
async def on_ready():
  global guild
  global admin_role
  # global role
  global anonchan
  global logger
  guild = discord.utils.get(client.guilds, id=guild_id)
  admin_role = discord.utils.get(guild.roles, id=admin_role_id)
  # role = discord.utils.get(guild.roles, id=role_id)
  anonchan = discord.utils.get(guild.channels, id=anonchan_id)
  logger = discord.utils.get(guild.channels, id=logger_id)
  if guild == None or anonchan == None or logger == None:
    print("I couldn't find a thing I needed! Aborting.")
    sys.exit()
  print(f'Anonymous Messenger up as {client.user} in guild {guild}')
  # with open("blacklist.yaml", "r", encoding="utf-8") as blacklist:
  #   blacklist = safe_load(blacklist)

@client.event
async def on_message(message):
  if message.author.bot:
    return # Bot should not trigger on bots
  if not isinstance(message.channel, discord.DMChannel):
    return # Only trigger upon DM message
  member = await guild.fetch_member(message.author.id)
  if member == None:
    await message.author.send("You are not in the guild.")
    return # Only trigger if member is in guild
  # if role not in member.roles and admin_role not in member.roles:
  #   await message.author.send("You don't have the right role to send an anonymous message.")
  #   return # Only trigger if they have the right role
  # Ignore attachments
  message.attachments = []
  msg = message.clean_content
  # Strip links
  if re.match(r'http[s:(]\S*', msg) != None:
    await message.author.send("Your message may not contain links.")
    return
  if msg == "":
    await message.author.send("Couldn't send that message.")
    return

  embed = discord.Embed(description=msg, color=0xc0c0c0)
  embed.set_author(name="???", icon_url='https://cdn.discordapp.com/avatars/946571933930127391/492b7fc83d95886aa9f4b687ba9970d0.png')
  # All checks passed, go ahead with posting.
  await anonchan.send(embed=embed)

  # Log the embed
  embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
  await logger.send(embed=embed)
  await message.author.send(f'Message sent to <#{anonchan_id}>!')

client.run(token)
