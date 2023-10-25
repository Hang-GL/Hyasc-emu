'''
Hubei Youth Automatically Study Evolution

code:
-1 undefined
0 OK
1 Can not save picture
2 Only login
30 Request error
31 OpenID generating failed
32 Wrong OpenID
33 Can not save record
50 Arguement missing
51 Data missing
52 Invalid arguements
53 Invalid data
'''
import getopt
import sys
import requests
from bs4 import BeautifulSoup
login_agent={
        "Host": "cp.fjg360.cn",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "X-Requested-With": "com.tencent.mm",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
stage1_agent = {
        "Host": "h5.cyol.com",
        "Connection": "keep-alive",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Origin": "http://h5.cyol.com",
        "X-Requested-With": "com.tencent.mm",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
stage2_agent = {
        "Host": "api.fjg360.cn",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Accept": "*/*",
        "X-Requested-With": "com.tencent.mm",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "script",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
stage3_agent = {
        "Host": "h5.cyol.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/tpg,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "X-Requested-With": "com.tencent.mm",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
stage4_agent = {
        "Host": "cp.fjg360.cn",
        "Connection": "keep-alive",
        "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
Rresult={
    "code":-1,
    "message":"undefined",
    "OpenID":"",
    "course":"",
    "name":"",
    "section1":"",
    "section2":"",
    "section3":"",
    "picUrl":"",
    "EmuUrl":"",
    "id":""
}
version=(1,0,0,0)
savePicture=False
onlyLogin=False
urlWithCode=""
openid=""

rtFlag=True
def onExit():
    global rtFlag
    if(rtFlag):
        print(Rresult)
        rtFlag=False
    sys.exit(0)

def getOpidByUrl():
    ssLogin=requests.session()
    replaced=urlWithCode.replace("rood","door.php")
    replaced=replaced+"#wechat_redirect"
    resp=ssLogin.get(replaced,headers=login_agent)
    sstr=resp.content.decode("utf8")
    ssLogin.close()
    opidPosi=sstr.find("pre_loc='sessionId=&imgTextId=&ip=&username='+username+'&phone='+phone+'&city='+city+'&danwei2='+danwei2+'&danwei='+danwei+'&openid=")+132
    buildstr=""
    while(sstr[opidPosi]!="'"):
        buildstr+=sstr[opidPosi]
        opidPosi+=1
    if(buildstr!=""):
        global openid
        openid=buildstr
    else:
        Rresult["code"]=31
        Rresult["message"]="OpenID generating failed"
        onExit()

#1
def get_code():
    ssTask=requests.session()
    url = "https://h5.cyol.com/special/weixin/sign.json"
    resp = ssTask.get(url,headers=stage1_agent).json()
    ssTask.close()
    return list(resp)[-1]

#2
def get_user():
    ssTask=requests.session()
    url = "https://api.fjg360.cn/index.php?m=vote&c=index&a=get_members&openid="+ openid
    resp = ssTask.get(url, headers=stage2_agent).json()
    ssTask.close()
    if resp.get("code") == 1:
        Rresult["OpenID"]=openid
        return resp.get("h5_ask_member")
    else:
        Rresult["code"]=32
        Rresult["message"]="Wrong OpenID"
        onExit()

#3
def get_course(code):
    Rresult["id"]=code
    ssTask=requests.session()
    url = 'https://h5.cyol.com/special/daxuexi/'+ code +'/m.html'
    resp = ssTask.get(url,headers=stage3_agent)
    ssTask.close()
    soup = BeautifulSoup(resp.content.decode("utf8"),"lxml")
    course = soup.title.string[7:]
    return course

def save_rec(user, course):
    ssTask=requests.session()
    Rresult["name"]=user["name"]
    Rresult["section1"]=user["danwei1"]
    Rresult["section2"]=user["danwei2"]
    Rresult["section3"]=user["danwei3"]
    Rresult["course"]=course
    url = "https://cp.fjg360.cn/index.php?m=vote&c=index&a=save_door&sessionId=&imgTextId=&ip="
    url += "&username=" + user["name"]
    url += "&phone=" + "未知"
    url += "&city=" + user["danwei1"]
    url += "&danwei2=" + user["danwei3"]
    url += "&danwei=" + user["danwei2"]
    url += "&openid=" + openid
    url += "&num=10"
    url += "&lesson_name=" + course
    resp = ssTask.get(url,headers=stage4_agent).json()
    ssTask.close()
    if resp.get("code") == 1:
        Rresult["code"]=0
        Rresult["message"]="OK"
        return True
    else:
        return False

def save_pic(code,extra):
    Rresult["picUrl"]="https://h5.cyol.com/special/daxuexi/"+code+"/images/end.jpg"
    Rresult["EmuUrl"]="https://hang-gl.github.io/Hyase/web/door.html?id="+code
    if(savePicture):
        resupic=requests.get(Rresult["picUrl"])
        open("./"+extra+".jpg","wb").write(resupic.content)

def main():
    global onlyLogin
    try:
        if(openid==""):getOpidByUrl()
        code=get_code()
        user=get_user()
        if(onlyLogin):
            Rresult["code"]=2
            Rresult["message"]="Only login"
            onExit()
        course=get_course(code)
        if(openid!="" and code!="" and user!="" and course!="" and onlyLogin==False):
            if(save_rec(user, course)):
                try:
                    save_pic(code,course)
                except:
                    Rresult["code"]=1
                    Rresult["message"]="Can not save picture"
            else:
                Rresult["code"]=33
                Rresult["message"]="Can not save record"
                onExit()
        else:
            Rresult["code"]=30
            Rresult["message"]="Request error"
            onExit()
    except:
        Rresult["code"]=39
        Rresult["message"]="Request error"
        onExit()
    onExit()

def onLoad():
    argc=len(sys.argv)
    if(argc==1):
        Rresult["code"]=50
        Rresult["message"]="Arguement missing"
        onExit()
    try:
        opts,args=getopt.getopt(sys.argv[1:],'ahvsd:',["help","version","auth"])
    except:
        Rresult["code"]=52
        Rresult["message"]="Invalid arguements"
        onExit()
    global openid,urlWithCode,savePicture
    for name,val in opts:
        if name in ("-h","--help"):
            print("[-h] [--help] [-v] [--version] [-a] [--auth] only get OpenID [-s] save picture [-d <data>] Wechat url or OpenID")
            print("https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx26a2a915deb3df1c&redirect_uri=https%3A%2F%2Fcp.fjg360.cn%2Fwenda%2F18da%2Frood%3FsessionId%3D%26secret%3D60e9768b2c0ea4b99265237587416905%26tset%3D1&response_type=code&scope=snsapi_userinfo&state=STATE&connect_redirect=0#wechat_redirect")
            sys.exit()
        if name in ("-v","--version"):
            print(version[0],":",version[1],":",version[2],":",version[3])
            sys.exit()
        if name in ("-d"):
            if(val.find("://")==-1):
                openid=val
            else:
                urlWithCode=val
        if name in ("-s"):
            savePicture=True
        if name in ("-a","--auth"):
            global onlyLogin
            onlyLogin=True
    if(openid==""and urlWithCode==""):
        Rresult["code"]=51
        Rresult["message"]="Data missing"
        onExit()
    if(urlWithCode==""and onlyLogin==True):
        Rresult["code"]=53
        Rresult["message"]="Invalid data"
        onExit()
    main()
            

if __name__ == '__main__':
    onLoad()