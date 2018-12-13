import requests
import time

home="http://127.0.0.1:5700"#端口号注意要改成对应的
allGroup=[]#所有要发的群
allMember=set([])#所有已发的人，防止重发

#从文件获取待发送信息
with open("mes.txt", 'r', encoding="utf-8") as f:
    message=f.read()

def send(QQ,group):
    """向群里某个QQ号发送信息"""
    para = {"message_type": "group","user_id": QQ,"group_id": group, "message": message}
    data = requests.post(home + "/send_msg", data=para).json()
    print(data)


def getAllGroup():
    """获取所有要发的群"""
    data = requests.get(home + "/get_group_list").json()["data"]
    num = len(data)
    for i in range(0, num):
        print(str(data[i]["group_id"]) + "\t\t" + data[i]["group_name"])
    print("输入要发送的群号，以0结束：")
    while (1):
        qun = int(input())
        if (qun == 0):
            break
        else:
            allGroup.append(qun)

def begin():
    """开始发"""
    #取得所有群内所有除管理员和群主外的成员
    for i in allGroup:
        print("开始解析群"+str(i)+"……")
        #所有群成员
        para = {"group_id": str(i)}
        GML = requests.post(home + "/get_group_member_list", data=para).json()["data"]
        gInfo = requests.post(home + "/_get_group_info", data=para).json()["data"]
        print("解析成功，除管理和群主共"+str(len(GML))+"人")
        for i in gInfo:
            print()