import requests
from help import CQHttp
import random
import time

home="http://127.0.0.1:5702"#端口号注意要改成对应的

usr=set([])#已经私聊的用户列表
last=time.time()#上一次私聊时间

#读取要发送的文本
with open("mes.txt", 'r', encoding="utf-8") as f:
    info=f.read()

data=requests.get(home+"/get_group_list").json()["data"]
num=len(data)
for i in range(0,num):
    print(str(data[i]["group_id"])+"\t\t"+data[i]["group_name"])
    id=str(data[i]["group_id"])
    qun=requests.post(home+"/_get_group_info?group_id="+id).json()["data"]["admins"]
    for j in qun:
        usr.add(j["user_id"])
        print(j["user_id"])



bot = CQHttp(api_root=home)
@bot.on_message("group")#此处参数为上报数据的message_type，若不填将接受所有信息
def handle_msg(con):
    global last
    print((con["user_id"] not in usr))
    print(time.time()-last)
    if((con["user_id"] not in usr) and time.time()-last>20):
        print("正在向"+str(con["user_id"])+"发送信息……")
        bot.send_private_msg(user_id=con["user_id"],message=info+str(time.time()))
        last=time.time()
        usr.add(con["user_id"])
    #@人的CQ码
    #bot.send_group_msg(group_id=con["group_id"],message="[CQ:at,qq="+str(con["user_id"])+"] 我好帮你点了，@你一直不回，麻烦回一下")

bot.run(host='127.0.0.1', port=8082)#监听端口要改