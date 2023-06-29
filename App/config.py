from dotenv import load_dotenv
import os
load_dotenv("/Users/yoonhp/Desktop/FILO_LISTEN_BOT/APP/key.env")

VenvValue = os.environ

# 삽입할 환경 변수:
VenvNeed = ["BOT_TOKEN", "SERVER_ID", "VIP_TOKEN", "CHANNEL_ID", "CHANNEL_SIGN", "PROXY_CHANNEL", "MID_JOURNEY_ID"]

#strings 형식

BOT_TOKEN = VenvValue.get('BOT_TOKEN') if "BOT_TOKEN" in VenvValue else "_Add your BOT_TOKEN HERE_"
BOT_NAME = VenvValue.get('BOT_NAME') if "BOT_NAME" in VenvValue else "_Add your BOT_NAME HERE_"

SERVER_ID = VenvValue.get('SERVER_ID') if "SERVER_ID" in VenvValue else "_Add your SERVER_ID HERE_"
VIP_TOKEN = VenvValue.get('VIP_TOKEN') if "VIP_TOKEN" in VenvValue else "_Add your VIP_TOKEN HERE_"
CHANNEL_ID = VenvValue.get('CHANNEL_ID') if "CHANNEL_ID" in VenvValue else "_Add your CHANNEL_ID HERE_" 

# 是否启用代理频道 此频道用于MJ보내기消息 若启用flask필수 입력 항목입니다.
AGENT_CHANNEL = VenvValue.get('AGENT_CHANNEL') if "AGENT_CHANNEL" in VenvValue else None

# 상담원 서비스가 활성화되어 있습니다 URL로컬 프록시 링크 AUTH인증된 계정 및 비밀번호입니다.:Tuple(user, pwd)
PROXY_URL = VenvValue.get('PROXY_URL') if "PROXY_URL" in VenvValue else None

#tuple 형식
PROXY_AUTH = VenvValue.get('PROXY_AUTH') if "PROXY_AUTH" in VenvValue else None

#boolean 형식
# 这个已经彻底没用了 需要설정의话请在discord위 설정
USE_MESSAGED_CHANNEL = True if "CHANNEL_SIGN" in VenvValue and VenvValue.get('CHANNEL_SIGN') == "True" else False 

#list 형식

AUTHORITY_LIST = []

# 初始化属性 不需要改动

HAS_RUN = False
MID_JOURNEY_ID = VenvValue.get('MID_JOURNEY_ID') if "MID_JOURNEY_ID" in VenvValue else "936929561302675456"  #midjourney bot id
