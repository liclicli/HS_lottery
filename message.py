import tkinter
import tkinter.messagebox

class MessageDisplay():
    def __init__(self, frame):
        self.root = frame
        self.partArea = tkinter.Frame(self.root)
        self.partArea.pack(side=tkinter.LEFT)
        self.partLabel = tkinter.Label(self.partArea, text='候选名单')
        self.partLabel.pack(side=tkinter.TOP, anchor='w')
        self.partText = tkinter.Text(self.partArea, width=8)
        self.partText.pack()

        self.msgArea = tkinter.Frame(self.root)
        self.msgArea.pack(side=tkinter.RIGHT)
        self.msgLabel = tkinter.Label(self.msgArea, text='祝福语')
        self.msgLabel.pack(side=tkinter.TOP, anchor='w')
        self.msgText = tkinter.Text(self.msgArea)
        self.msgText.pack()
    
    def Append(self, info):
        self.partText.insert(tkinter.END, info[0] + '\n')
        self.partText.yview(tkinter.END)
        self.msgText.insert(tkinter.END, info[1] + '\n')
        self.msgText.yview(tkinter.END)
    
    def GetParticipants(self):
        return self.partText.get('0.0', tkinter.END)

    def GetMsgs(self):
        return self.msgText.get('0.0', tkinter.END)

class MessageInput():
    def __init__(self, frame):
        self.root = frame
        self.userLabel = tkinter.Label(self.root, text='参与者')
        self.userLabel.pack(side=tkinter.LEFT)
        self.userVar = tkinter.StringVar()
        self.userInput = tkinter.Entry(self.root, width=8, textvariable=self.userVar)
        self.userInput.pack(side=tkinter.LEFT)

        self.msgLabel = tkinter.Label(self.root, text='想说的话')
        self.msgLabel.pack(side=tkinter.LEFT)
        self.msgVar = tkinter.StringVar()
        self.msgInput = tkinter.Entry(self.root, width=40, textvariable=self.msgVar)
        self.msgInput.pack(side=tkinter.LEFT)
    
    def GetInput(self):
        return (self.userVar.get(), self.msgVar.get())
    
    def Clear(self):
        self.userVar.set('')
        self.msgVar.set('')
    
    def ResetFocus(self):
        self.userInput.focus()

class Message():
    def __init__(self, frame):
        self.root = tkinter.Frame(frame)
        self.root.pack()
        self.displayArea = tkinter.Frame(self.root, pady=10)
        self.displayArea.pack(side=tkinter.TOP)
        self.inputArea = tkinter.Frame(self.root)
        self.inputArea.pack(side=tkinter.BOTTOM)
        self.display = MessageDisplay(self.displayArea)
        self.input = MessageInput(self.inputArea)
        self.submit = tkinter.Button(self.inputArea, text='提交', command=self.__submit)
        self.submit.pack(side=tkinter.LEFT)

    def __submit(self):
        info = self.input.GetInput()
        if info[0] == '' or info[1] == '':
            tkinter.messagebox.showinfo('温馨提示','参与者或想说的话不能为空哦～')
        else:
            self.display.Append(info = info)
            self.input.Clear()
            self.input.ResetFocus()
    
    def GetParticipants(self):
        return self.display.GetParticipants()
    
    def GetMsgs(self):
        return self.display.GetMsgs()
