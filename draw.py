import tkinter
import tkinter.messagebox
import re
import hashlib
import random

defaultDrawSetting = [
    ('特等奖', 1),
    ('一等奖', 2),
    ('二等奖', 4),
    ('三等奖', 6),
]

class DrawSetting():
    def __init__(self, frame):
        self.root = frame
        self.setting = defaultDrawSetting
        self.curSetting = []
        for draw in self.setting:
            labelVar = tkinter.StringVar()
            labelVar.set(draw[0])
            label = tkinter.Label(self.root, textvariable=labelVar)
            label.pack(side=tkinter.LEFT)
            entryVar = tkinter.StringVar()
            entryVar.set("%d" % draw[1])
            vcmd = (lambda text: re.match(r"\d*", text) == text, "%P")
            entry = tkinter.Entry(self.root, textvariable=entryVar, validate='key', validatecommand=vcmd)
            entry.pack(side=tkinter.LEFT)
            ph = tkinter.Label(self.root, width=1)
            ph.pack(side=tkinter.LEFT)
            self.curSetting.append((labelVar, entryVar, entry))
    
    def GetCurDrawSetting(self):
        curSetting = []
        for setting in self.curSetting:
            if int(setting[1].get()) > 0:
                curSetting.append((setting[0].get(), int(setting[1].get())))
        return curSetting
    
    def GetLuckyNum(self):
        total = 0
        for setting in self.curSetting:
            n = int(setting[1].get())
            if n > 0:
                total = total + n
        return total

    def Enable(self, flag):
        for setting in self.curSetting:
            if flag:
                setting[2].config(state=tkinter.NORMAL)
            else:
                setting[2].config(state=tkinter.DISABLED)

class DrawCore():
    def __init__(self):
        self.seed = 0
        self.setting = []
        self.partList = []

        self.remainList = []
        self.records = []
        self.curLevel = ''
        self.curList = []
        self.nextLevel = ''
        self.index = -1
    
    def GetRemainList(self):
        remainStr = ''
        for remain in self.remainList:
            remainStr = remainStr + remain + '\n'
        return remainStr
    
    def GetRecord(self):
        recordStr = ''
        for record in self.records:
            recordStr = recordStr + ('--%s--\n' % record[0])
            for part in record[1]:
                recordStr = recordStr + ('%s\n' % part)
        return recordStr
    
    def GetCurLevel(self):
        return self.curLevel
    
    def GetNextLevel(self):
        return self.nextLevel
    
    def GetCurList(self):
        curListStr = ''
        for part in self.curList:
            curListStr = curListStr + part + ', '
        return curListStr
    
    def Reset(self):
        random.seed(self.seed)
        self.remainList = self.partList[:]
        self.records = []
        self.curLevel = ''
        self.curList = []
        self.nextLevel = ''
        self.index = -1

    def Start(self, seed, setting, partList):
        self.seed = seed
        self.setting = setting[:]
        self.partList = partList[:]
        self.Reset()
        if len(self.setting) > 0:
            self.nextLevel = self.setting[-1][0]

        print('--after start--')
        print(self.seed)
        print(self.partList)
        print(self.setting)
    
    def Next(self):
        if self.index + 1 >= len(self.setting):
            return False
        self.index = self.index + 1
        self.curLevel = self.setting[-(self.index + 1)][0]
        if self.index + 1 < len(self.setting):
            self.nextLevel = self.setting[-(self.index + 2)][0]
        num = self.setting[-(self.index + 1)][1]
        for i in range(num):
            x = random.randint(0,len(self.remainList) - 1 - i)
            t = self.remainList[i]
            self.remainList[i] = self.remainList[i + x]
            self.remainList[i + x] = t
        self.curList = self.remainList[:num]
        self.remainList = self.remainList[num:]
        self.records.append((self.curLevel, self.curList[:]))

class DrawDisplay():
    def __init__(self, frame):
        self.root = frame
        self.recordArea = tkinter.Frame(self.root)
        self.recordArea.pack()
        # reaminArea
        self.remainArea = tkinter.Frame(self.recordArea)
        self.remainArea.pack(side=tkinter.LEFT)
        self.remainLabel = tkinter.Label(self.remainArea, text='剩余候选人')
        self.remainLabel.pack(anchor='w')
        self.remainText = tkinter.Text(self.remainArea, state=tkinter.DISABLED)
        self.remainText.pack()

        self.luckyRecordArea = tkinter.Frame(self.recordArea)
        self.luckyRecordArea.pack(side=tkinter.LEFT)
        self.luckyLabel = tkinter.Label(self.luckyRecordArea, text='中奖记录')
        self.luckyLabel.pack(anchor='w')
        self.luckyText = tkinter.Text(self.luckyRecordArea, state=tkinter.DISABLED)
        self.luckyText.pack()

        # curArea
        self.curLevelArea = tkinter.Frame(self.root)
        self.curLevelArea.pack(fill=tkinter.X)
        self.curLevelLabel = tkinter.Label(self.curLevelArea, text='当前奖项', font=('幼圆',16))
        self.curLevelLabel.pack(side=tkinter.LEFT)
        self.curLevelVar = tkinter.StringVar()
        self.curLevelEntry = tkinter.Entry(self.curLevelArea, textvariable=self.curLevelVar, state=tkinter.DISABLED, font=('幼圆',16))
        self.curLevelEntry.pack(side=tkinter.LEFT, fill=tkinter.X, expand=1)

        # curListArea
        self.curLevelListArea = tkinter.Frame(self.root)
        self.curLevelListArea.pack(fill=tkinter.X)
        self.curLevelListLabel = tkinter.Label(self.curLevelListArea, text='中奖名单', font=('幼圆',18))
        self.curLevelListLabel.pack(side=tkinter.LEFT)
        self.curLevelListVar = tkinter.StringVar()
        self.curLevelListEntry = tkinter.Entry(self.curLevelListArea, textvariable=self.curLevelListVar, state=tkinter.DISABLED, font=('幼圆',18))
        self.curLevelListEntry.pack(side=tkinter.LEFT, fill=tkinter.X, expand=1)

    def Update(self, core: DrawCore):
        self.curLevelVar.set(core.GetCurLevel())
        self.curLevelListVar.set(core.GetCurList())
        self.remainText.config(state=tkinter.NORMAL)
        self.remainText.delete('0.0', tkinter.END)
        self.remainText.insert(tkinter.END, core.GetRemainList())
        self.remainText.config(state=tkinter.DISABLED)
        self.luckyText.config(state=tkinter.NORMAL)
        self.luckyText.delete('0.0', tkinter.END)
        self.luckyText.insert(tkinter.END, core.GetRecord())
        self.luckyText.config(state=tkinter.DISABLED)
        print('--lucky--')
        print(core.GetRecord())

class Draw():
    def __init__(self, frame):
        self.root = frame
        self.participants = []
        self.seed = 0

        self.settingArea = tkinter.Frame(self.root)
        self.settingArea.pack()
        self.setting = DrawSetting(self.settingArea)
        self.settingConfirm = tkinter.Button(self.settingArea, text='确认抽奖方案', command=self.ConfirmScheme)
        self.settingConfirm.pack(anchor='w')

        self.drawArea = tkinter.Frame(self.root)

        self.stateArea = tkinter.Frame(self.drawArea)
        self.stateArea.pack()
        self.core = DrawCore()
        self.display = DrawDisplay(self.stateArea)

        self.drawVar = tkinter.StringVar()
        self.drawVar.set('开奖')
        self.drawButton = tkinter.Button(self.drawArea, textvariable=self.drawVar, command=self.Draw, font=('幼圆',18))
        self.drawButton.pack()

        self.resetButton = tkinter.Button(self.drawArea, text='重置开奖结果', command=self.Reset)
        self.resetButton.pack()
    
    def SetPartAndMsg(self, partStr: str, msg: str):
        print("-----partStr escape-----")
        print(partStr.encode('unicode_escape'))
        parts = partStr.split('\n')
        self.participants = []
        for part in parts:
            if part != '':
                self.participants.append(part)
        print("-----participants insight-----")
        print(self.participants)

        if len(msg) > 1:
            msg = msg[:-1]
        print("-----msg escape-----")
        print(msg.encode('unicode_escape'))
        
        hash = hashlib.sha512()
        hash.update(msg.encode())
        key = hash.hexdigest()[:16]
        self.seed = int('0x' + key, 16)
        print("-----hash key-----")
        print(hash.hexdigest())
        print(key)
        print("-----seed-----")
        print(self.seed)
    
    def Reset(self):
        self.setting.Enable(True)
        self.settingConfirm.config(state=tkinter.NORMAL)
        self.core.Reset()
        self.display.Update(self.core)
        self.settingArea.pack_forget()
        self.drawArea.pack_forget()
        self.settingArea.pack()

    def Update(self):
        self.display.Update(self.core)
        nextLevel = self.core.GetNextLevel()
        if nextLevel != '':
            self.drawVar.set("开%s" % nextLevel)
            self.drawButton.config(state=tkinter.NORMAL)
        else:
            self.drawButton.config(state=tkinter.DISABLED)

    def ConfirmScheme(self):
        if len(self.participants) < self.setting.GetLuckyNum():
            tkinter.messagebox.showinfo('温馨提示','中奖人数超过候选人数')
            return
        if self.setting.GetLuckyNum() <= 0:
            tkinter.messagebox.showinfo('温馨提示','至少要有1人中奖')
            return
        self.setting.Enable(False)
        self.settingConfirm.config(state=tkinter.DISABLED)

        self.core.Start(self.seed, self.setting.GetCurDrawSetting(), self.participants)
        self.Update()

        self.settingArea.pack_forget()
        self.drawArea.pack_forget()

        self.settingArea.pack()
        self.drawArea.pack()

    def Draw(self):
        self.core.Next()
        self.Update()