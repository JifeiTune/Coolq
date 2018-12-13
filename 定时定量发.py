import requests
from cqhttp import CQHttp,Error
import random
import time

#统一配置参数
sendP=5700#发送端口号
revP=4080#监听端口号
dur=20#每个群发消息的时间间隔
MIN=3#发消息前最少等待条数
MAX=5#发消息前最大等待条数

home="http://127.0.0.1:"+str(sendP)#端口号注意要改成对应的

group=set([])#要发送的群
mNum={}#每个群继上一次别人已发信息条数
lastTime={}#每个群继上一次我的发言时间

#读取要发送的文本
with open("mes.txt", 'r', encoding="utf-8") as f:
    info=f.read()

#首先获取并确认要发的群号
data=requests.get(home+"/get_group_list").json()["data"]
num=len(data)
for i in range(0,num):
    print(str(data[i]["group_id"])+"\t\t"+data[i]["group_name"])
print("输入要发送的群号，以0结束：")
while(1):
    qun=int(input())
    if(qun==0):
        break
    else:
        group.add(qun)#添加群
        mNum[qun]=99#开始信息为0
        lastTime[qun]=0#时间设为极远，这样一开始就能发

bot = CQHttp(api_root=home)
@bot.on_message("group")#此处参数为上报数据的message_type，若不填将接受所有信息
def handle_msg(con):
    #bot.send(context, '你好呀，下面一条是你刚刚发的：')
    #bot.send_private_msg(user_id=con["user_id"],message="[CQ:at,qq="+str(con["user_id"])+"]")
    #@人的CQ码
    #bot.send_group_msg(group_id=con["group_id"],message="[CQ:at,qq="+str(con["user_id"])+"] 我好帮你点了，@你一直不回，麻烦回一下")
    if(con["group_id"] in group):#在要发送的群内
        if(
            mNum[con["group_id"]] > random.randint(MIN,MAX)#需要隔几条信息
            and
            time.time()-lastTime[con["group_id"]]>dur#需要间隔一定秒数
            ):
            #先更新信息条数和时间，减少多线程问题
            mNum[con["group_id"]] = 0
            lastTime[con["group_id"]] = time.time()
            try:
                bot.send_group_msg(group_id=con["group_id"],
                               message=info+"[CQ:face,id="+str(random.randint(0,170))+"]")
            except Error as e:
                if(e.retcode==-34):
                    print("群"+str(con["group_id"])+"发送失败，已被T或被禁言")
                    group.remove(con["group_id"])#除去已经不能发言的群
            else:
                print("已向群"+str(con["group_id"])+"推送")
        else:
            mNum[con["group_id"]]+=1#接收到的信息加一
bot.run(host='127.0.0.1', port=revP)#监听端口要改