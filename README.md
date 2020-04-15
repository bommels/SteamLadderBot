### Steam Ladder Discord Bot
This Discord bot is used to retrieve steam(ladder) stats. Active in the <a href='https://steamladder.com/discord/join/'>Steam Ladder Discord</a>.

##### Running the bot
```bash
# Set your tokens and keys in config.py and rename the file
mv bot/config.sample.py bot/config.py

# Option 1: Run with docker-compose
docker-compose up -d --build

# Option 2: Run in python 3.x (easier for debugging and development)
pip install -r requirements.txt
python bot/bot.py
```

<small>You can get a discord bot token <a href='https://discordapp.com/developers/applications'>here</a>. You can get a Steam Ladder API key <a href='https://steamladder.com/user/settings/api/'>here</a>.</small>

<small>*Note: this bot is using an (currently) undocumented v2 of the Steam Ladder API.*</small>