from interactions import Extension, listen, Client

from interactions.api.events import MessageCreate

from . import BotSettings

'''
Event Listen Class
'''
class BotEventCls(Extension):
    def __init__(self, client: Client) -> None:
        self.cliendt = client        

    @listen()
    async def on_ready(self):
        print("Bot Ready!")


    @listen()
    async def on_MessageCreate(self, event: MessageCreate, **kwargs):
        message = event.message
        print("message_content: ", message.content)
        
        test=message.content.split()
        print(test)
        if len(test)>1:
            ck=test[0][4:-1]
            if ck=="123":
                cond=test[4][2:-1]
                print(ck,cond)
    
        if hasattr(message,'attachments'):
            print("message_Hash: ", (message.attachments))
        if "Get Bot Message for" in message.content:
            print("",str(message.message_reference.message_id))
            print("job-hash값: ",str((message.get_referenced_message().attachments[0].url.split("_")[-1]).split(".")[0]))
            
        if message.content == "": return
        if message.author.bot:
            try:
                if ck=="123":
                    if message.attachments and message.author.username == "Midjourney Bot":
                        print("hello!")
                        # 생성된 사진에 대한 url 얻기
                        imgURL=message.attachments[0].url
                        channel="1120192393329770547"
                        #msgID = Queue_msg[1][1].queue_name
                        jobId='123'
                        agency="Get Bot Message for |UV|<@{U}>|{I} |{C}|{J}".format(U = cond, I = imgURL, 
                                                                    C = channel, J = jobId)
                        await message.reply(content = agency)
                        
            except IndexError as e:
                pass

        return


def setup(bot):
    print("Init BotEvent.py")
    BotEventCls(bot)