# -*- coding: utf-8 -*-

from linepy import *
from akad import *
import traceback
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, urllib, urllib,pickle
from datetime import datetime
from random import randint

print("""

\033["""+str(randint(0,1))+""";"""+str(randint(31,36))+"""mplay free\nby beach noxtian\033[0m

""")

with open('tval.pkl', 'rb') as f:
    [cltoken,wait] = pickle.load(f,encoding='latin1')

if len(sys.argv) == 2 and sys.argv[1] == "reset":
    cltoken = ""
    with open('tval.pkl', 'wb') as f:
        pickle.dump([cltoken,wait], f)
    os._exit(0)

if cltoken == "":
    cl = LINE()
    cltoken = cl.authToken
else:
    try:
        cl = LINE(cltoken)
    except KeyboardInterrupt as e:
        raise e
    except:
        cl = LINE()
        cltoken = cl.authToken

print("authToken: %s" % (cltoken))


user1 = cl.profile.mid
admin = OEPoll(cl)

start_runtime = datetime.now()

wait = {
    'alwayread':False,
    'autoBlock':False,
    'welcomepic':False,
    'welcomemessage':False,
    'autoadd':False,
    'messageadd':"",
    'autotag':False,
    'tagmessage':"",
}

userhelp = """😎สวัสดีพี่โอ้กับพี่ฟ้าเค้ายัง?😎:
☢☢☢☢☢☢☢☢☢☢☢☢☢☢☢
☞╠☠คำสั่ง
☞╠☠ไอดี
☞╠☠Me
☞╠☠ชื่อ
☞╠☠sp
☞╠☠ชื่อ @
☞╠☠ไปเกิดใหม่ @
☞╠☠ไอดี @
☞╠☠ยกค้าง
☞╠☠ทุกคน
☞╠☠sh *
☞╠☠โทร
☞╠☠เวลา
☞╠☠จำ @
☞╠☠ลืม
☞╠☠ลืมหมด
☞╠☠autodeny off
☞╠☠autodeny [numbers]
☞╠☠เปิด/ปิดอ่าน
☞╠☠เปิด/ปิดบล็อค
☞╠☠เปิด/ปิดข้อความ
☞╠☠เปิด/ปิดรูป
☞╠☠เปิด/ปิดแทค
☞╠☠ตั้งข้อความ:[ใส่ข้อความ]
☞╠☠ตั้งแอด:[ใส่ข้อความ]
☞╠☠ตั้งแทค:[ใส่ข้อความ]
☞╠☠เปิด/ปิดแอด
☞╠☠!resetallmention
☢☢☢☢☢☢☢☢☢☢☢☢☢☢
**😰แค่นี้แหละจะยุกะฟ้าที่รักของกู😰**"""

procLock = 0
mentmedat = {}
respRemember = {}

def user1scipt(op):
    global startruntime
    global user1
    global wait
    global alwayread
    global autoBlock
    global welcomepic
    global welcomemessage
    global autoadd
    global messageadd
    global autotag
    global tagmessage
    global autoDeny
    global procLock
    global mentmedat
    global respRemember
    try:
        if op.type == 0:
            return

        if op.type == 5:
            if wait['autoBlock'] == True:
                cl.blockContact(op.param1)

            if wait['autoadd'] == True:
                cl.findAndAddContactsByMid(op.param1)
                if (wait["messageadd"] in [""," ","\n",None]):
                    pass
                else:
                    cl.sendMessage(op.param1,str(wait["messageadd"]))

        if op.type ==13:
            invitor = op.param2
            gotinvite = []
            if "\x1e" in op.param3:
                gotinvite = op.param3.split("\x1e")
            else:
                gotinvite.append(op.param3)
            if invitor in user1 in gotinvite:
                cl.acceptGroupInvitation(op.param1)
            else:
                group = cl.getGroup(op.param1)
                if len(group.members) <= autoDeny:
                    procLock += 1
                    cl.acceptGroupInvitation(op.param1)
                    cl.leaveGroup(op.param1)

        if op.type == 17:
            if wait['welcomemessage'] and "welcomemessage" in wait:
               cnt = cl.getContact(op.param2)
               cl.sendMessage(op.param1,cnt.displayName + "\n" + str(wait["welcomemessage"]))

            if wait['welcomepic'] and "welcomepic" in wait:
                cnt = cl.getContact(op.param2)
                cl.sendImageWithURL(op.param1,"http://dl.profile.line.naver.jp/" + cnt.pictureStatus)

        if op.type == 26:
             msg = op.message
             msg.from_ = msg._from
             if msg.contentMetadata != {}:
                 try:
                     prov = eval(msg.contentMetadata["MENTION"])["MENTIONEES"]
                     tagme = False
                     alluids = []
                     for i in range(len(prov)):
                         alluids.append(prov[i]["M"])
                         if prov[i]["M"] == mid:
                             tagme = True
                     alluids = list(set(alluids))
                     if tagme:
                        if len(alluids) <= 4:
                            if msg.to not in mentmedat:
                                mentmedat[msg.to] = []
                                tagfrom = msg.from_
                                tagtime = nowS = datetime.strftime(datetime.now(),"%H:%M:%S")
                                tagid = msg.id
                                mentmedat[msg.to].append(
                                    {
                                        "tfrom" : tagfrom,
                                        "ttime" : tagtime,
                                        "tid" : tagid
                                    }
                                )
                 except:
                     pass

             if wait["alwayread"]:
                 cl.sendChatChecked(msg.from_,msg.id)
             else:
                 cl.sendChatChecked(msg.to,msg.id)

             if msg.to in respRemember and msg.text in respRemember[msg.to]:
                 if msg.toType != 0:
                     cl.sendMessage(msg.to,respRemember[msg.to][msg.text])
                 else:
                     cl.sendMessage(msg.from_,respRemember[msg.to][msg.text])

             if wait["tagmessage"] == True:
                 cl.sendMessage(op.param1)
                 if (wait["tagmessage"] in [""," ","\n",None]):
                     pass
                 else:
                     cl.sendMessage(op.param1,str(wait["tagmessage"]))

        if op.type == 25:
            msg = op.message
            if msg.text is None:
               return

            elif msg.text.lower() == "คำสั่ง":
                cl.sendMessage(msg.to,userhelp)

            elif msg.text.lower() == "ไอดี":
                cl.sendMessage(msg.to,user1)

            elif msg.text.lower() == "me":
                beach = user1
                cl.sendContact(msg.to,beach)

            elif msg.text.lower() == "ชื่อ":
                G = cl.getContact(user1)
                cl.sendMessage(msg.to,G.displayName)

            elif msg.text.lower() == "sp":
                start = time.time()
                cl.sendMessage(msg.to,"กำลังทดสอบ(｀・ω・´)")
                cl.sendMessage(msg.to,str(int(round((time.time() - start) * 1000)))+" ms")

            elif "ชื่อ " in msg.text.lower():
                spl = re.split("!name ",msg.text,flags=re.IGNORECASE)
                if spl[0] == "":
                    prof = cl.getProfile()
                    prof.displayName = spl[1]
                    cl.updateProfile(prof)
                    cl.sendMessage(msg.to,"เปลี่ยนชื่อสำเร็จแล้ว(｀・ω・´)")

            elif "ไปเกิดใหม่" in msg.text.lower():
                if msg.contentMetadata is not None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            cl.kickoutFromGroup(msg.to,[target])
                        except:
                            cl.kickoutFromGroup(msg.to,[target])
                    else:
                        pass

            elif "ไอดี " in msg.text.lower():
                if msg.toType == 2:
                    red = re.compile(re.escape('!uid '),re.IGNORECASE)
                    namel = red.sub('',msg.text)
                    namel = namel.lstrip()
                    namel = namel.replace(" @","$spliter$")
                    namel = namel.replace("@","")
                    namel = namel.rstrip()
                    namel = namel.split("$spliter$")
                    gmem = cl.getGroup(msg.to).members
                    for targ in gmem:
                        if targ.displayName in namel:
                            cl.sendMessage(msg.to,targ.displayName+": "+targ.mid)

            elif "ยกค้าง" in msg.text.lower():
                 spl = re.split("!denyall",msg.text,flags=re.IGNORECASE)
                 if spl[0] == "":
                     spl[1] = spl[1].strip()
                     ag = cl.getGroupIdsInvited()
                     txt = "กำลังยกเลิกค้างเชิญจำนวน "+str(len(ag))+"กลุ่ม"
                     if spl[1] != "":
                         txt = txt + " ด้วยข้อความ \""+spl[1]+"\""
                     txt = txt + "\nกรุณารอสักครู่.."
                     cl.sendMessage(msg.to,txt)
                     procLock = len(ag)
                     for gr in ag:
                         try:
                             cl.acceptGroupInvitation(gr)
                             if spl[1] != "":
                                 cl.sendMessage(gr,spl[1])
                             cl.leaveGroup(gr)
                         except:
                             pass
                     cl.sendMessage(msg.to,"สำเร็จแล้ว(｀・ω・´)")

            elif "ตั้งแอด:" in msg.text.lower():
                wait['messageadd'] = msg.text.replace("!setmessageadd:","")
                cl.sendMessage(msg.to,"ตั้งค่าสำเร็จ(｀・ω・´)")

            elif "ตั้งแทค:" in msg.text.lower():
                wait['tagmessage'] = msg.text.replace("!tagmessage:","")
                cl.sendMessage(msg.to,"ตั้งค่าสำเร็จ(｀・ω・´)")

            elif msg.text.lower().startswith("แทค"):
                data = msg.text[len("!mentionall"):].strip()
                if data == "":
                    group = cl.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members if contact.mid != user1]
                    cb = ""
                    cb2 = ""
                    count = 1
                    strt = len(str(count)) + 2
                    akh = int(0)
                    cnt = 0
                    for md in nama:
                        akh = akh + len(str(count)) + 2 + 5
                        cb += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(md)+"},"""
                        strt = strt + len(str(count+1)) + 2 + 6
                        akh = akh + 1
                        cb2 += str(count)+". @name\n"
                        cnt = cnt + 1
                        if cnt == 50:
                            cb = (cb[:int(len(cb)-1)])
                            cb2 = cb2[:-1]
                            msg.contentType = 0
                            msg.text = cb2
                            msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
                            try:
                                cl.sendMessage(msg)
                            except:
                                cl.sendMessage(msg.to,"[[NO MENTION]]")
                            cb = ""
                            cb2 = ""
                            strt = len(str(count)) + 2
                            akh = int(0)
                            cnt = 0
                        count += 1
                    cb = (cb[:int(len(cb)-1)])
                    cb2 = cb2[:-1]
                    msg.contentType = 0
                    msg.text = cb2
                    msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}
                    try:
                       cl.sendMessage(msg.to, text=cb2,contentMetadata={u'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'},contentType=0)
                    except:
                       cl.sendMessage(msg.to,"[[NO MENTION]]")

            elif msg.text.lower() == "ทุกคน":
                if msg.to in mentmedat and mentmedat[msg.to] != []:
                    text = ""
                    for data in mentmedat[msg.to]:
                        print("555")
                        try:
                            conname = cl.getContact(data["tfrom"]).displayName
                        except:
                            conname = "[DELETED]"
                        text += "[%s] %s\nline://nv/chatMsg?chatId=%s&messageId=%s\n\n" % (data["ttime"],conname,msg.to,data["tid"])
                    text = text[:-2]
                    try:
                        cl.sendMessage(msg.to,text)
                    except Exception as e:
                        cl.sendMessage(msg.to,str(e))
                    del mentmedat[msg.to]
                else:
                    cl.sendMessage(msg.to,"ไม่มีการกล่าวถึงก่อนหน้านี้(｀・ω・´)")

            elif msg.text.lower() == "!resetmention":
                dkey = mentmedat.pop(msg.to,None)
                cl.sendMessage(msg.to,"รีเซ็ตข้อมูลการกล่าวถึงเรียบร้อยแล้ว")


            elif msg.text.lower() == "!resetallmention":
                mentmedat = {}
                cl.sendMessage(msg.to,"รีเซ็ตข้อมูลการกล่าวถึงทั้งหมดแล้ว")

            elif "!sh " in msg.text.lower():
                spl = re.split("!sh ",msg.text,flags=re.IGNORECASE)
                if spl[0] == "":
                    try:
                        cl.sendMessage(msg.to,subprocess.getoutput(spl[1]))
                    except:
                        pass

            elif msg.text.lower() == "โทร":
                exc = cl.getGroup(msg.to).members
                zxc = cl.getProfile().mid
                cl.inviteIntoGroupCall(msg.to,[uid.mid for uid in exc if uid.mid != zxc])
                cl.sendMessage(msg.to,"เชิญเข้าร่วมการคอลเรียบร้อย(｀・ω・´)")

            elif msg.text.lower() == "เวลา":
                cl.sendMessage(msg.to,str(datetime.now() - start_runtime)[:-7].split(":")[0]+" hour, "+str(datetime.now() - start_runtime)[:-7].split(":")[1]+" minute, "+str(datetime.now() - start_runtime)[:-7].split(":")[2]+" second,")

            elif msg.text.lower().startswith("จำ "):
                data = msg.text[len("!remember "):]
                keyword = data.split(":",1)[0]
                if keyword.lower().startswith("!remember") or keyword.lower().startswith("!forget") or keyword in ["",None]:
                    raise ValueError
                response = data.split(":",1)[1]
                if response in ["",None]:
                    raise ValueError
                if msg.to not in respRemember:
                    respRemember[msg.to] = {}
                respRemember[msg.to][keyword] = response
                now2 = datetime.now()
                nowT = datetime.strftime(now2,"%H")
                nowM = datetime.strftime(now2,"%M")
                nowS = datetime.strftime(now2,"%S")
                tm = "\n\n"+nowT+":"+nowM+":"+nowS
                if msg.toType != 0:
                    cl.sendMessage(msg.to,"จำแล้ว (｀・ω・´)"+tm)
                else:
                    cl.sendMessage(msg._from,"จำแล้ว (｀・ω・´)"+tm)

            elif msg.text.lower().startswith("ลืม "):
                keyword = msg.text[len("!forget "):]
                if keyword in ["",None]:
                    raise ValueError
                if msg.to in respRemember and keyword in respRemember[msg.to]:
                    dkey = respRemember[msg.to].pop(keyword,None)
                    now2 = datetime.now()
                    nowT = datetime.strftime(now2,"%H")
                    nowM = datetime.strftime(now2,"%M")
                    nowS = datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    if msg.toType != 0:
                        cl.sendMessage(msg.to,"ลืมแล้ว (｀・ω・´)"+tm)
                    else:
                        cl.sendMessage(msg._from,"ลืมแล้ว (｀・ω・´)"+tm)
                else:
                    now2 = datetime.now()
                    nowT = datetime.strftime(now2,"%H")
                    nowM = datetime.strftime(now2,"%M")
                    nowS = datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    if msg.toType != 0:
                        cl.sendMessage(msg.to,"ไม่สามารถลืมได้ (｀・ω・´)"+tm)
                    else:
                        cl.sendMessage(msg._from,"ไม่สามารถลืมได้ (｀・ω・´)"+tm)
            elif msg.text.lower() == "ลืมหมด":
                dkey = respRemember.pop(msg.to,None)
                now2 = datetime.now()
                nowT = datetime.strftime(now2,"%H")
                nowM = datetime.strftime(now2,"%M")
                nowS = datetime.strftime(now2,"%S")
                tm = "\n\n"+nowT+":"+nowM+":"+nowS
                if msg.toType != 0:
                    cl.sendMessage(msg.to,"ลืมทุกอย่างแล้ว (｀・ω・´)"+tm)
                else:
                    cl.sendMessage(msg.from_,"ลืมทุกอย่างแล้ว (｀・ω・´)"+tm)

            elif "ตั้งข้อความ:" in msg.text.lower():
                 c = msg.text.replace("!welcomemessage:","")
                 if c in [""," ","\n",None]:
                     cl.sendMessage(msg.to,"เกิดข้อผิดพลาด!!(｀・ω・´)")
                 else:
                     wait['welcomemessage'] = c
                     cl.sendMessage(msg.to,"ตั้งค่าข้อความสำเร็จแล้ว(｀・ω・´)")

            elif msg.text.lower() == "!autodeny off":
                autoDeny = -1
                cl.sendMessage(msg.to,"ตั้งค่าสำเร็จแล้ว(｀・ω・´)")

            elif msg.text.lower().startswith("!autodeny "):
               try:
                   autoDeny = int(msg.text[len(".autodeny "):])
                   cl.sendMessage(msg.to,"ตั้งค่าสำเร็จแล้ว(｀・ω・´)")
               except:
                   cl.sendMessage(msg.to,"พบข้อผิดพลาด(｀・ω・´)")

            elif msg.text.lower() == "เปิดอ่าน":
                if wait["alwayread"] == True:
                    cl.sendMessage(msg.to,"เปิดอ่านอัตโนมัติแล้ว(｀・ω・´)")
                    wait["alwayread"] = False
                else:
                    if wait["alwayread"] == False:
                        cl.sendMessage(msg.to,"เปิดอ่านอัตโนมัติแล้ว(｀・ω・´)")

            elif msg.text.lower() == "ปิดอ่าน":
                if wait["alwayread"] == False:
                    cl.sendMessage(msg.to,"ปิดอ่านอัตโนมัติแล้ว(｀・ω・´)")
                    wait["alwayread"] = True
                else:
                    if wait["alwayread"] == True:
                        cl.sendMessage(msg.to,"ปิดอ่านอัตโนมัติแล้ว(｀・ω・´)")

            elif msg.text.lower() == "เปิดบล็อค":
                if wait['autoBlock'] == True:
                    cl.sendMessage(msg.to,"เปิดการบล็อคอัตโนมัตื(｀・ω・´)")
                    wait['autoBlock'] = False
                else:
                    if wait['autoBlock'] == False:
                        cl.sendMessage(msg.to,"เปิดการบล็อคอัตโนมัตื(｀・ω・´)")

            elif msg.text.lower() == "ปิดบล็อค":
                if wait['autoBlock'] == False:
                    cl.sendMessage(msg.to,"ปิดการบล็อคอัตโนมัตื(｀・ω・´)")
                    wait['autoBlock'] = True
                else:
                    if wait['autoBlock'] == True:
                        cl.sendMessage(msg.to,"ปิดการบล็อคอัตโนมัตื(｀・ω・´)")

            elif msg.text.lower() == "เปิดรูป":
                if wait['welcomepic'] == False:
                    cl.sendMessage(msg.to,"เปิดต้อนรับรูปเรียบร้อย(｀・ω・´)")
                    wait['welcomepic'] = True
                else:
                    if wait['welcomepic'] == True:
                        cl.sendMessage(msg.to,"เปิดต้อนรับรูปเรียบร้อย(｀・ω・´)")

            elif msg.text.lower() == "ปิดรูป":
                if wait['welcomepic'] == True:
                    cl.sendMessage(msg.to,"ปิดต้อนรับรูปเรียบร้อย(｀・ω・´)")
                    wait['welcomepic'] = False
                else:
                    if wait['welcomepic'] == False:
                        cl.sendMessage(msg.to,"ปิดต้อนรับรูปเรียบร้อย(｀・ω・´)")

            elif msg.text.lower() == "เปิดข้อความ":
                if wait['welcomemessage'] == False:
                    cl.sendMessage(msg.to,"เปิดต้อนรับข้อความเรียบร้อย(｀・ω・´)")
                    wait['welcomemessage'] = True
                else:
                    if wait['welcomemessage'] == True:
                        cl.sendMessage(msg.to,"เปิดต้อนรับข้อความเรียบร้อย(｀・ω・´)")

            elif msg.text.lower() == "ปิดข้อความ":
                if wait['welcomemessage'] == True:
                    cl.sendMessage(msg.to,"ปิดต้อนรับข้อความเรียบร้อย(｀・ω・´)")
                    wait['welcomemessage'] = False
                else:
                    if wait['welcomemessage'] == False:
                        cl.sendMessage(msg.to,"ปิดต้อนรับข้อความเรียบร้อย(｀・ω・´)")

            elif msg.text.lower() == "เปิดแอด":
                if wait['autoadd'] == False:
                    cl.sendMessage(msg.to,"เปิดการรับเพื่อนอัตโนมัติ(｀・ω・´)")
                    wait['autoadd'] = True
                else:
                    if wait['autoadd'] == True:
                        cl.sendMessage(msg.to,"เปิดการรับเพื่อนอัตโนมัติ(｀・ω・´)")

            elif msg.text.lower() == "ปิดแอด":
                if wait['autoadd'] == True:
                    cl.sendMessage(msg.to,"ปิดการรับเพื่อนอัตโนมัติ(｀・ω・´)")
                    wait['auto'] = False
                else:
                    if wait['autoadd'] == False:
                        cl.sendMessage(msg.text,"ปิดการรับเพื่อนอัตโนมัติ(｀・ω・´)")

            elif msg.text.lower() == "เปิดแทค":
                if wait['autotag'] == False:
                    cl.sendMessage(msg.to,"เปิดการแท็กตอบกลับเรียบร้อย(｀・ω・´)")
                    wait['autotag'] = True
                else:
                    if wait['autotag'] == True:
                        cl.sendMessage(msg.to,"เปิดการแท็กตอบกลับเรียบร้อย(｀・ω・´)")

            elif msg.text.lower() == "ปิดแทค":
                if wait['autotag'] == True:
                    cl.sendMessage(msg.to,"ปิดการแท็กตอบกลับเรียบร้อย(｀・ω・´)")
                    wait['autotag'] = False
                else:
                    if wait['autotag'] == False:
                        cl.sendMessage(msg.to,"ปิดการแท็กตอบกลับเรียบร้อย(｀・ω・´)")
    except:
        traceback.print_exc()

try:
    while True:
        ops = admin.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                user1scipt(op)
                admin.setRevision(op.revision)
except:
    traceback.print_exc()
    with open('tval.pkl', 'wb') as f:
        pickle.dump([cltoken,wait], f)
