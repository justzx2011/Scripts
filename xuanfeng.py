#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import hashlib
try:
    import urllib as parse
    import urllib2 as request
    import cookielib as cookiejar
except:
    from urllib import parse,request
    from http import cookiejar
import random,time
import threading as thread
import json,os,sys,re
try:
    raw_input
except:
    raw_input=input
def _(string):
    try:
        return string.decode("u8")
    except:
        return string

class XF:
    """
     Login QQ
    """
    __headers ={
                'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:11.0) Gecko/20100101 Firefox/11.0',\
    }
    __downpath = '%s/Downloads/xuanfeng.down'%os.path.expanduser("~")
    __cookiepath = '/tmp/cookie.xf'
    __verifycode = None
    __http = {}
    __RE=re.compile("\d+")
    def __preprocess(self,password,verifycode):
        """
            QQ密码加密部份
        """

        return hashlib.md5( (self.__md5_3((password).encode('utf-8')) + (verifycode).upper()).encode('utf-8')).hexdigest().upper()

        pass

    def __md5_3(self,str):
        """
            QQ密码md5_3部份
        """
        return hashlib.md5(hashlib.md5(hashlib.md5(str).digest()).digest()).hexdigest().upper()
        pass
    def __init__(self):
        """
            初始化模拟进程
        """
        self.__http['cj'] = cookiejar.LWPCookieJar(self.__cookiepath)
        if os.path.isfile(self.__cookiepath):
            self.__http['cj'].load(ignore_discard=True, ignore_expires=True)

        self.__http['opener'] = request.build_opener(request.HTTPCookieProcessor(self.__http['cj']))
        if os.path.isfile(self.__cookiepath):
            self.main()
        else:
            self.__Login()
    def __request(self,url,method='GET',data={},savecookie=False):
        """
            请求url
        """
        if (method).upper() == 'POST':
            data = parse.urlencode(data).encode('utf-8')
            self.__http['req'] = request.Request(url,data,headers=self.__headers)
        else:
            self.__http['req'] = request.Request(url=url,headers=self.__headers)
        fp = self.__http['opener'].open(self.__http['req'])
        try:
            str = fp.read().decode('utf-8')
        except UnicodeDecodeError:
            str = fp.read()
        if savecookie == True:
            self.__http['cj'].save(ignore_discard=True, ignore_expires=True)
        fp.close()
        return str
        pass
    def __getcookies(self,name):
        fp = open(self.__cookiepath)
        fp.seek(130)
        for read in fp.readlines():
            str = read.split(name)
            if len(str) == 2:
                fp.close()
                return str[1].strip()
        fp.close()
        return None
        pass
    def __getverifycode(self):
        """
            @url:http://ptlogin2.qq.com/check?uin=644826377&appid=1003903&r=0.56373973749578
        """
        urlv = 'http://ptlogin2.qq.com/check?uin='+ ('%s' % self.__qq)+'&appid=1003903&r='+ ('%s' % random.Random().random())
        str = self.__request(url = urlv, savecookie=False)
        str = re.findall(r'\d|(?<=\')[a-zA-Z0-9\!]{4}',str)
        return str
        pass
    def __request_login(self):
        """
            @url:http://ptlogin2.qq.com/login
            @params:{u:644826377
                    p:73DA5C1145E0F82247F60B3A17B89E6A   verifycode:!S10   webqq_type:10
                    remember_uin:1  login2qq:1  aid:1003903  u1:http://webqq.qq.com/loginproxy.html?login2qq=1&webqq_type=10
                    h:1  ptredirect:0   ptlang:2052  from_ui:1   pttype:1  dumy:
                    fp:loginerroralert   action:1-24-62651  mibao_css:m_webqq}
        """
        urlv = 'http://ptlogin2.qq.com/login?u='+('%s' %  self.__qq) +'&' +  'p=' + ('%s' % self.__pswd) +  '&verifycode='+ ('%s' % self.__verifycode[1]) +'&aid=567008010' +  "&u1=http%3A%2F%2Flixian.qq.com%2Fmain.html" +  '&h=1&ptredirect=1&ptlang=2052&from_ui=1&dumy=&fp=loginerroralert'
        str = self.__request(url = urlv,savecookie=True)
        if str.find(_('登录成功')) != -1:
            #执行二次登录
            self.__getlogin()
            self.main()
        elif str.find(_('不正确')) != -1:
            print('你输入的帐号或者密码不正确，请重新输入。')
        else:
            print('登录失败')
        pass

    def main(self):
        self.__getlist()
        self.__gethttp()
        self.__chosetask()
        self.__download()

    def getfilename_url(self,url):
        url=url.strip()
        filename=""
        if url.startswith("ed2k"):
            arr=url.split("|")
            if len(arr)>=4:
                filename=parse.unquote(arr[2])
        else:
            filename=url.split("/")[-1]
        return filename.split("?")[0]
    def __getlogin(self):
        urlv = 'http://lixian.qq.com/handler/lixian/do_lixian_login.php'
        str = self.__request(url =urlv,method = 'POST',savecookie=True)
            #登陆旋风，可从str中得到用户信息

    def __getlist(self):
            """
            得到任务名与hash值
            """
            urlv = 'http://lixian.qq.com/handler/lixian/get_lixian_list.php'
            res = self.__request(urlv,'POST',savecookie=False)
            res = json.JSONDecoder().decode(res)
            if res["msg"]==_('未登录!'):
                self.__getlogin()
                self.main()
            elif not res["data"]:
                print (_('无离线任务!'))
                self.__addtask()
                self.main()
            else:
                self.filename = []
                self.filehash = []
                self.filemid = []
                print ("\n===================离线任务列表====================")
                print ("序号\t大小\t进度\t文件名")
                for num in range(len(res['data'])):
                    index=res['data'][num]
                    self.filename.append(index['file_name'].encode("u8"))
                    self.filehash.append(index['hash'])
                    size=index['file_size']
                    self.filemid.append(index['mid'])
                    if size==0:
                        percent="-0"

                    else:
                        percent=str(index['comp_size']/size*100).split(".")[0]

                    dw=["B","K","M","G"]
                    for i in range(3):
                        _dw=dw[i]
                        if size>=1024:
                            size=size/1024
                        else:
                            break
                    size="%d%s"%(size,_dw)
                    print ("%d\t%s\t%s%%\t%s"%(num+1,size,percent,_(self.filename[num])))
                print ("=======================END=========================\n")

    def __gethttp(self):
            """
            获取任务下载连接以及FTN5K值
            """
            urlv = 'http://lixian.qq.com/handler/lixian/get_http_url.php'
            self.filehttp = []
            self.filecom = []
            print("请求杂七杂八的玩意ing")
            for num in range(len(self.filename)):
                    data = {'hash':self.filehash[num],'filename':self.filename[num],'browser':'other'}
                    str = self.__request(urlv,'POST',data)
                    self.filehttp.append(re.search(r'\"com_url\":\"(.+?)\"\,\"',str).group(1))
                    self.filecom.append(re.search(r'\"com_cookie":\"(.+?)\"\,\"',str).group(1))
           
    def __chosetask(self):
        print ("请选择操作,输入回车(Enter)下载任务\nA添加任务,D删除任务,O在线播放任务,R刷新离线任务列表")
        inputs=raw_input()
        if inputs=="":
            self.__creatfile()
        elif inputs.upper()=="A":
            self.__addtask()
            self.main()
        elif inputs.upper()=="D":
            self.__deltask()
            self.main()
        elif inputs.upper()=="R":
            self.main()
        elif inputs.upper()=="O":
            self.__online()
            self.main()

    def __creatfile(self):
            """
            建立aria2下载文件
            """
            print ("请输入要下载的任务序号,数字之间用空格,逗号或其他非数字字符号分割.\n输入A下载所有任务:")
            target=raw_input().strip()
            if target.upper()=="A":
                lists=range(1,len(self.filehttp)+1)
            else:
                lists=self.__RE.findall(target)
            if lists==[]:
                print ("选择为空.")
                self.__chosetask()
                return
            f = open(self.__downpath,'w')
            for num in lists:
                try:
                    num=int(num)-1
                    f.write(self.filehttp[num] + '\n  header=Cookie: FTN5K=' + self.filecom[num] +
                    '\n  continue=true\n  max-conection-per-server=5\n  split=10\n   parameterized-uri=true\n\n')
                except:
                    print (num+1 ,_(" 任务建立失败!"))
            f.close
            print("aria2输入文件建立")

    def __deltask(self):
        print ("请输入要删除的任务序号,数字之间用空格,逗号或其他非数字字符号分割.\n输入A删除所有任务:")
        target=raw_input().strip()
        if target.upper()=="A":
            lists=range(1,len(self.filehttp)+1)
        else:
            lists=self.__RE.findall(target)
        if lists==[]:
            print ("选择为空.")
            self.__chosetask()
        urlv = 'http://lixian.qq.com/handler/lixian/del_lixian_task.php'
        for num in lists:
                num=int(num)-1
                data = {'mids':self.filemid[num]}
                str = self.__request(urlv,'POST',data)
        print("任务删除完成")
                    
    def __addtask(self):
        print ("请输入下载地址:")
        url=raw_input()
        filename=self.getfilename_url(url)
        data={"down_link":url,\
                "filename":filename,\
                "filesize":0,\
                }
        urlv="http://lixian.qq.com/handler/lixian/add_to_lixian.php"
        str = self.__request(urlv,'POST',data)
    def __download(self):
        os.system("aria2c -i %s" % self.__downpath)

    def __online(self):
        print("输入需要在线观看的任务序号")
        num = int(raw_input())
        print("正在缓冲，马上开始播放")
        os.system(r"cd ~/videos/online;wget -c -O %s --header 'Cookie:FTN5K=%s' '%s'&sleep\
                        5;mplayer %s >/dev/null" %
                        (self.filename[num],self.filecom[num],self.filehttp[num],self.filename[num]))
        
    def __Login(self):
        """
        登录
        """
        if not hasattr(self,"__qq"):
            self.__qq = raw_input('QQ号：')
            self.__pswd = raw_input('QQ密码：')
        self.__qq = self.__qq.strip()
        self.__pswd = self.__pswd.strip()
        self.__verifycode = self.__getverifycode()
        self.__pswd = self.__preprocess(
            self.__pswd,#密码 \
            '%s' % self.__verifycode[1]  #验证码 \
        )
        print ("登录中...")
        self.__request_login()
        pass

try:
    s = XF()
except KeyboardInterrupt:
    print (" exit now.")
    os.system(r'killall wget')
    sys.exit()

