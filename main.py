import tkinter
import tkinter.messagebox
import message
import draw

class Lottery():
    def __init__(self):
        title = '抽奖机'
        try:
            with open('./title.txt', 'r') as fin:
                title = fin.readline()
        except Exception:
            pass
        self.root = tkinter.Tk()
        self.root.title(title)
        self.root.geometry('1280x720')
        self.frame = tkinter.Frame(self.root)
        self.frame.pack()
        self.title = tkinter.Label(self.frame, text=title, font=('幼圆',24))
        self.title.pack()
        self.messageArea = tkinter.Frame(self.frame)
        self.messageArea.pack()
        self.message = message.Message(self.messageArea)

        self.drawArea = tkinter.Frame(self.frame)
        self.draw = draw.Draw(self.drawArea)
        self.enterDraw = tkinter.Button(self.frame, text='进入抽奖', command=self.GoDraw)
        self.enterDraw.pack(anchor='e')
        self.enterMessage = tkinter.Button(self.frame, text='返回', command=self.GoMessage)
        self.root.mainloop()

    def __unpackAll(self):
        self.title.pack_forget()
        self.messageArea.pack_forget()
        self.drawArea.pack_forget()
        self.enterDraw.pack_forget()
        self.enterMessage.pack_forget()

    def GoDraw(self):
        self.__unpackAll()
        self.title.pack()
        self.enterMessage.pack(anchor='w')
        self.drawArea.pack()
        self.draw.SetPartAndMsg(self.message.GetParticipants(), self.message.GetMsgs())

    def GoMessage(self):
        self.__unpackAll()
        self.title.pack()
        self.messageArea.pack()
        self.enterDraw.pack(anchor='e')

if __name__ == '__main__':
    lottery = Lottery()