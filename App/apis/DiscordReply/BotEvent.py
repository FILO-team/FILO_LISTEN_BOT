from interactions import Extension, listen, Client

from interactions.api.events import MessageCreate
import boto3
import json
import time
from . import BotSettings

# Get the service resource
# sqs = boto3.resource('sqs', region_name='ap-northeast-2')
# queue = sqs.get_queue_by_name(QueueName='SQS_midjourney_output_prod')
print("hello sqs")
"""
Event Listen Class
"""


class BotEventCls(Extension):
    def __init__(self, client: Client) -> None:
        self.client = client
        self.queue = boto3.resource(
            "sqs", region_name="ap-northeast-2"
        ).get_queue_by_name(QueueName="SQS_midjourney_output_prod")

    @listen()
    async def on_ready(self):
        print("Bot Ready!")

    @listen()
    async def on_MessageCreate(self, event: MessageCreate, **kwargs):
        message = event.message
        # pk값은 계속해서 traking 해야함 -> user_id, time_stamp 식별
        if message.content.split():
            pk = ""
            flag = 0
            for i in message.content:
                if i == "#":
                    flag = 1
                    continue
                if i == ">":
                    break
                if flag:
                    pk += i

        if "First" in message.content:
            # print("message_id값: ",str(message.message_reference.message_id))
            # print("job-hash값: ",str((message.get_referenced_message().attachments[0].url.split("_")[-1]).split(".")[0]))
            tp_list = message.content.split()
            img_url = None
            for i in tp_list:
                if len(i):
                    if i.startswith("http"):
                        img_url = i
                        break
            temp_json = {}
            temp_json["object_key"] = pk
            temp_json["message_id"] = str(message.message_reference.message_id)
            temp_json["job_hash"] = str(
                (
                    message.get_referenced_message().attachments[0].url.split("_")[-1]
                ).split(".")[0]
            )
            temp_json["img_url"] = img_url
            # upscale 전 이미지
            temp_json["state"] = "before"
            message_body = json.dumps(temp_json)
            try:
                response = self.queue.send_message(
                    MessageBody=message_body,
                )
            except ClientError as error:
                logger.exception("Send message failed: %s", message_body)
                raise error

        if "Upscale_result" in message.content:
            # print("message_id값: ",str(message.message_reference.message_id))
            # print("job-hash값: ",str((message.get_referenced_message().attachments[0].url.split("_")[-1]).split(".")[0]))
            # print(pk)
            tp_list = message.content.split()
            img_url = None
            for i in tp_list:
                if len(i):
                    if i.startswith("http"):
                        img_url = i
                        break
            # index
            index = tp_list[2]
            # print(tp_list)
            temp_json = {}
            temp_json["object_key"] = pk
            temp_json["message_id"] = str(message.message_reference.message_id)
            temp_json["job_hash"] = str(
                (
                    message.get_referenced_message().attachments[0].url.split("_")[-1]
                ).split(".")[0]
            )
            temp_json["img_url"] = img_url
            temp_json["in_dex"] = index
            # 4개의 image로 선택이 되어야 하는 상황.
            temp_json["state"] = "after"

            # queue 전달 (유저의 선택 혹은 백오피스 작업이 끝난 상태) -after
            message_body = json.dumps(temp_json)
            try:
                response = self.queue.send_message(
                    MessageBody=message_body,
                )
            except ClientError as error:
                logger.exception("Send Upscale message failed: %s", message_body)
                raise error

        if message.content == "":
            return
        # reply의 경우 처음 생성된 그림에 대해서만 진행되도록 해야함 >> message_content안에 Image # 번호의 유무로 구분 가능 > 서로 다른 방향으로 진행
        if message.author.bot:
            try:
                # 이미지를 처음 생성할 때 (4가지 중 하나를 선택해야 하는 상태)
                if message.attachments and message.author.username == "Midjourney Bot":
                    # 생성된 사진에 대한 url 얻기
                    imgURL = message.attachments[0].url
                    channel = BotSettings["BotCode"]["CHANNEL_ID"]
                    pk = "**<#" + pk + ">"
                    # job ID를 넣어주어야 향후에 맵핑 가능
                    if "Image" not in message.content:
                        agency = "{P} First {I} |{C}".format(I=imgURL, C=channel, P=pk)
                    else:
                        # print(message.content.split())
                        temp = message.content.split()[-2][1]

                        agency = "{P} Upscale_result {index} {I} |{C}".format(
                            I=imgURL, C=channel, P=pk, index=temp
                        )
                    await message.reply(content=agency)
            except IndexError as e:
                pass

        return


def setup(bot):
    print("Init BotEvent.py")
    BotEventCls(bot)
