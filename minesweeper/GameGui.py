from StartGui import *
from MineBoard import *
from tkinter import messagebox
from tkinter import *
from nn import *

#雷盘界面GUI
class GameGui():
    def __init__(self, row, col, minenum, master = None):
        self.count = 0#步数
        self.count_list = []#存储步数，便于求平均步数
        self.dis_rate_list = []#存储开采率，便于求平均
        self.file = open('dataset.csv', 'a')
        self.file.writelines('\n')
        self.row = row
        self.col = col
        self.model = create_model()
        self.minenum = minenum
        self.board = array([[10 for i in range(self.col)] for j in range(self.row)])
        self.mineboard = MineBoard(self.row, self.col, self.minenum)
        self.boardlist = self.mineboard.getboard()
        self.root = master
        self.f = None
        #一些操作按钮，重开，退出
        self.opf = Frame(self.root, width = 100, height = 200)
        self.opf.pack(side = LEFT)
        self.restartbutton = Button(self.opf, text = '重开一局', command = self.restart)
        self.restartbutton.pack()
        self.quitbutton = Button(self.opf, text = '退出', command = self.root.quit)
        self.quitbutton.pack()
        self.show()
        self.nn_loop()

    def restart(self):
        self.count = 0
        self.file = open('dataset.csv', 'a')
        self.board = array([[10 for i in range(self.col)] for j in range(self.row)])
        self.mineboard = MineBoard(self.row, self.col, self.minenum)
        self.boardlist = self.mineboard.getboard()
        self.show()
        self.nn_loop()

    def show(self):
        if self.f != None:
            self.f.destroy()
        self.f = Frame(self.root, width=(self.col) * 30+20, height=self.row * 30+20)
        self.f.pack(side = LEFT)
        self.canvas=Canvas(self.f,width=(self.col + 1)*30+10,height=(self.row + 1)*30+10, bg='White')
        for i in range(self.row + 1):
            self.canvas.create_line((10,i*30+10),(30*(self.col)+10,i*30+10),width=2)
        for i in range(self.col + 1):
            self.canvas.create_line((i*30+10,10),(i*30+10,30*(self.row)+10),width=2)
        global maplist
        maplist = []
        for i in range(self.row):
            for j in range(self.col):
##                print(self.board[i][j], end = '\t')
                img = PhotoImage(file=self.getimg(i, j))
                
                maplist.append(img)
                self.canvas.create_image((30*(j+1)-4, 30*(i+1)-4), image = maplist[i * (self.col) + j])
                del img
##            print()
##        for i in range(self.row):
##            for j in range(self.col):
##                print(self.boardlist[i][j], end = '\t')
##            print()
##        self.canvas.bind('<Button-1>', self.left_click)
##        self.canvas.bind('<Button-3>', self.right_click)
        self.canvas.pack()

    def getimg(self, i, j):
        if self.board[i][j] == -1:
            return './image/icons8-地雷-20.png'
        elif self.board[i][j] == 0:
            return './image/0.png'
        elif self.board[i][j] == 1:
            return './image/1.png'
        elif self.board[i][j] == 2:
            return './image/2.png'
        elif self.board[i][j] == 3:
            return './image/3.png'
        elif self.board[i][j] == 4:
            return './image/4.png'
        elif self.board[i][j] == 5:
            return './image/5.png'
        elif self.board[i][j] == 6:
            return './image/6.png'
        elif self.board[i][j] == 7:
            return './image/7.png'
        elif self.board[i][j] == 8:
            return './image/8.png'
        elif self.board[i][j] == 9:
            return './image/flag.png'
        elif self.board[i][j] == 10:
            return './image/unknown.png'
        else:
            print('board error')
            exit(0)

    def nn_loop(self):
        while 1:
            if self.mineboard.getflag() == 0:
                y, x = predict_next(self.model, self.board)
                self.count += 1
                #print(y,x)
                for i in self.board:
                    for j in i:
                        self.file.writelines(str(j) + ' ')
                self.file.writelines(str(y) + ' ' + str(x))
                if self.boardlist[y][x] == -1:#踩到雷
                    self.board[y][x] = self.boardlist[y][x]
                    self.mineboard.setflag(-1)
                elif self.boardlist[y][x] == 0:#踩到安全区域
                    self.board[y][x] = self.boardlist[y][x]
                    dedlist = []#去重列表
                    self.zerosloop(y, x, dedlist)#遍历，将相邻的0全部显示
                else:#踩到数字
                    self.board[y][x] = self.boardlist[y][x]
                self.show()
                self.judge()
            else:
                break   

    def right_click(self, event):
        if self.mineboard.getflag() == 0:
            x = (event.x - 10) // 30
            y = (event.y - 10) // 30
            if self.board[y][x] == 10:#未知地区插旗
                self.board[y][x] = 9
            elif self.board[y][x] == 9:#插旗位置取消旗
                self.board[y][x] = 10
            else:
                pass
            self.show()

    def zerosloop(self, y, x, dedlist):
        ly = y - 1
        ry = y + 1
        lx = x - 1
        rx = x + 1
        if ly < 0:
            ly = 0
        if ry >= self.row:
            ry = self.row - 1
        if lx < 0:
            lx = 0
        if rx >= self.col:
            rx = self.col - 1
        for i in range(ly, ry + 1):
            for j in range(lx, rx + 1):
                if (i, j) not in dedlist:
                    dedlist.append((i, j))
                    if self.board[i][j] == 9:
                        pass
                    else:
                        if self.boardlist[i][j] == 0:
                            self.board[i][j] = self.boardlist[i][j]
                            self.zerosloop(i, j, dedlist)
                        else:
                            self.board[i][j] = self.boardlist[i][j]

    def judge(self):
        count = 0
        if self.mineboard.getflag() == -1:
            self.file.writelines(' 0\n')
            self.file.close()
            self.count_list.append(self.count)
            print(self.count)
            print(sum(self.count_list) // len(self.count_list))
            self.discover_rate()
        else:
            for i in range(self.row):#当全部的非雷都踩出来后，获得胜利
                for j in range(self.col):
                    if self.boardlist[i][j] != -1:
                        if self.board[i][j] == self.boardlist[i][j]:
                            count += 1
            if count == (self.row * self.col - self.minenum):
                self.mineboard.setflag(1)
            if self.mineboard.getflag() == 1:
                self.file.writelines(' 100\n')
                self.file.close()
                self.count_list.append(self.count)
                print(self.count)
                print(sum(self.count_list) // len(self.count_list))
                self.discover_rate()
            else:
                self.file.writelines(' 1\n')

    def discover_rate(self):#在结束的时候显示开采率,平均开采率
        b = []
        for i in self.board:
            for j in i:
                b.append(j)
        cap = self.row * self.col
        rate = (cap - b.count(10)) / cap * 100
        self.dis_rate_list.append(rate)
        rate_avg = sum(self.dis_rate_list) / len(self.dis_rate_list)
        print('%.2f%%' % rate)
        print('%.2f%%' % rate_avg)
