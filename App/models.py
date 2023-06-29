import re

from .config import BOT_TOKEN, SERVER_ID, VIP_TOKEN, CHANNEL_ID, \
                    USE_MESSAGED_CHANNEL, MID_JOURNEY_ID, AGENT_CHANNEL, \
                    HAS_RUN, BOT_NAME, PROXY_URL, PROXY_AUTH

def ConfigCheck(Config):
    if bool(re.findall("^_Add.*HERE_$", Config)):
        raise ValueError("초기 변수{}정의되지 않음".format(Config))
    return Config


BotSettings = {
    "BotCode" : {
        "BOT_TOKEN": ConfigCheck(BOT_TOKEN),
        "SERVER_ID": ConfigCheck(SERVER_ID),
        "VIP_TOKEN": ConfigCheck(VIP_TOKEN),
        "CHANNEL_ID": ConfigCheck(CHANNEL_ID),
        "MID_JOURNEY_ID": MID_JOURNEY_ID,
    },
    "BotOpt" : {
        "USE_CHANNEL": USE_MESSAGED_CHANNEL,
        "AGENT_SIGN": bool(AGENT_CHANNEL),
        "AGENT_CHANNEL": AGENT_CHANNEL,
        "PROXY_URL": PROXY_URL,
        "PROXY_AUTH": PROXY_AUTH,
        "HAS_RUN": HAS_RUN
    },
    "BotInfo" : {
        "Name": BOT_NAME,
        "version": "v1.0",
    },
    "BotInit" : {
        "Speed": "Fast",
    },
}

