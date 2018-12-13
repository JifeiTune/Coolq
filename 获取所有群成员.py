import requests
import time

home="http://127.0.0.1:5700"#端口号注意要改成对应的
allGroup=[]#所有要发的群
allMember=set([])#所有已发的人，防止重发

#从文件获取待发送信息
with open("mes.txt", 'r', encoding="utf-8") as f:
    message=f.read()

def getAll(id):
    print("开始解析群"+str(id)+"……")
    para = {"group_id": str(id)}
    GML = requests.post(home + "/get_group_member_list", data=para).json()["data"]
    for i in GML:
        print(str(i["user_id"])+"@qq.com")

id=input()
id=int(id)
getAll(id)