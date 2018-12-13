import requests
import time

home="http://127.0.0.1:5700"#端口号注意要改成对应的

dur=30#发送延时
group=[]

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
        group.append(qun)

num=len(group)
while(1):
    for i in range(num-1,-1,-1):#反向遍历便于删除
        para = {"group_id": str(group[i]), "message": info}
        data=requests.post(home + "/send_group_msg", data=para).json()
        if(data["retcode"]==-34 or data["retcode"]==-39):#被T或被禁言
            print(str(group[i])+"发送失败，已被T或禁言")
            group.pop(i)
            num-=1
        else:
            print(str(group[i])+"发送成功！")
    for i in range(dur, -1, -1):
        mystr = "等待" + str(i) + "秒后再次发送……"
        print(mystr, end="")
        print("\b" * (len(mystr) * 2), end="", flush=True)
        time.sleep(1)