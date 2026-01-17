'''
用户校验
'''
import json
import threading
lock = threading.Lock()

def check_user(username,password):
    with lock:
        with open("userconfig.json",encoding="utf-8") as f:
            datajson = json.loads(f.read())
        if username in datajson:
            if password == datajson.get(username).get("password"):
                return True
        return False

def check_quota(username):
    with lock:
        with open("userconfig.json",encoding="utf-8") as f:
            datajson = json.loads(f.read())
        if username in datajson:
            visited = datajson[username]["visited"]
            quota = datajson[username]["quota"]
            if visited >= quota:
                raise Exception(f"你当前配额已用完,用了{visited},总次数是{quota}")
            datajson[username]["visited"] +=1
            with open("userconfig.json","w",encoding="utf-8") as f:
                f.write(json.dumps(datajson,ensure_ascii=False,indent=4))


def get_quotas(username):
    with lock:
        with open("userconfig.json",encoding="utf-8") as f:
            datajson = json.loads(f.read())
        if username in datajson:
            visited = datajson[username]["visited"]
            quota = datajson[username]["quota"]
            return f"你当前总配额是 {quota} ,已经用了 {visited} ,还剩 {quota - visited} 数量"
    return ""