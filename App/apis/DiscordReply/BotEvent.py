from interactions import Extension, listen, Client

from interactions.api.events import MessageCreate
import boto3
from . import BotSettings

#Get the service resource
#sqs = boto3.resource('sqs', region_name='ap-northeast-2')
#queue = sqs.get_queue_by_name(QueueName='test')

dynamodb = boto3.resource('dynamodb',region_name='ap-northeast-2')
table=dynamodb.Table("lambda_dynamodb")
print("hello dynamodb")

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
        # pk값은 계속해서 traking 해야함
        if message.content.split():
            pk=""
            flag=0
            for i in message.content:
                if i=="#":
                    flag=1
                    continue
                if i==">":
                    break
                if flag:
                    pk+=i
            
        if "First" in message.content:
            print("message_id값: ",str(message.message_reference.message_id))
            print("job-hash값: ",str((message.get_referenced_message().attachments[0].url.split("_")[-1]).split(".")[0]))
            tp_list=message.content.split()
            img_url=None
            for i in tp_list:
                if len(i):
                    if i.startswith("http"):
                        img_url=i
                        break
            # print(tp_list)
            temp_json={}
            temp_json['pk']=pk
            temp_json['message_id']=str(message.message_reference.message_id)
            temp_json['job-hash']=str((message.get_referenced_message().attachments[0].url.split("_")[-1]).split(".")[0])
            temp_json['img_url']=img_url
            
            # 4개의 image로 선택이 되어야 하는 상황.
            temp_json['state']="first"
            #response = queue.send_message(MessageBody=f'{temp_json}')
            # queue 전달 (유저의 선택 혹은 백오피스 작업이 필요한 상태) -before
            try:
                temp=table.put_item(
                    Item={
                        'pk': pk,
                        'message_id':str(message.message_reference.message_id),
                        'job-hash':str((message.get_referenced_message().attachments[0].url.split("_")[-1]).split(".")[0]),
                        'img_url':img_url,
                        'state':'first',
                        }
                )
            except ClientError as err:
                logger.error(
                    "Couldn't")
                raise
            
        if "Upscale_result" in message.content:
            print("message_id값: ",str(message.message_reference.message_id))
            print("job-hash값: ",str((message.get_referenced_message().attachments[0].url.split("_")[-1]).split(".")[0]))
            # queue 전달 (유저의 선택 혹은 백오피스 작업이 끝난 상태) -after
            
        if message.content == "": return
        # reply의 경우 처음 생성된 그림에 대해서만 진행되도록 해야함 >> message_content안에 Image # 번호의 유무로 구분 가능 > 서로 다른 방향으로 진행
        if message.author.bot:
            try:
                # 이미지를 처음 생성할 때 (4가지 중 하나를 선택해야 하는 상태)
                if message.attachments and message.author.username == "Midjourney Bot":
                    # 생성된 사진에 대한 url 얻기
                    imgURL=message.attachments[0].url
                    channel=BotSettings['BotCode']["CHANNEL_ID"]
                    pk="**<#"+pk+">"
                    # job ID를 넣어주어야 향후에 맵핑 가능
                    if "Image" not in message.content:
                        agency="{P} First {I} |{C}".format(I = imgURL, C = channel,P=pk)
                    else:
                        agency="{P} Upscale_result {I} |{C}".format(I = imgURL, C = channel,P=pk)
                    await message.reply(content = agency)
            except IndexError as e:
                pass

        return


def setup(bot):
    print("Init BotEvent.py")
    BotEventCls(bot)