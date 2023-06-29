import interactions

from .. import BotSettings
BotAgent = interactions.Client(
                token=BotSettings["BotCode"]["BOT_TOKEN"],
                default_scope=BotSettings["BotCode"]["SERVER_ID"],
                intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MESSAGES | interactions.Intents.MESSAGE_CONTENT ,
                proxy_url=BotSettings["BotOpt"]["PROXY_URL"],
                proxy_auth=BotSettings["BotOpt"]["PROXY_AUTH"],
            )

BotAgent.load_extension("App.apis.DiscordReply.BotEvent")