import discord
import asyncio
import datetime
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True

client = discord.Client(intents=intents)

DAYS = [
    ("🇹", "Tuesday", 1),
    ("🇼", "Wednesday", 2),
    ("🇷", "Thursday", 3),
    ("🇫", "Friday", 4),
    ("🇸", "Saturday", 5),
    ("🇺", "Sunday", 6),
    ("🇲", "Monday", 0),
]

def get_upcoming_dates(start_date):
    dates = []
    for _, _, weekday in DAYS:
        days_ahead = (weekday - start_date.weekday()) % 7
        target_date = start_date + datetime.timedelta(days=days_ahead)
        dates.append(target_date)
    return dates

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print("Channel not found.")
        await client.close()
        return

    start_date = datetime.datetime.now()
    week_of = (start_date + datetime.timedelta(days=(1 - start_date.weekday()) % 7)).strftime("%m/%d/%y")
    upcoming_dates = get_upcoming_dates(start_date)

    lines = []
    for (emoji, day_name, _), date in zip(DAYS, upcoming_dates):
        lines.append(f"{emoji} - {day_name} ({date.strftime('%m/%d')})")

    description = f"**@Everyone What days are you available to run content** (Week of {week_of}):\n" + "\n".join(lines)

    msg = await channel.send(description)

    for emoji, _, _ in DAYS:
        await msg.add_reaction(emoji)

    await client.close()

client.run(TOKEN)
