from StartGui import *
from MineBoard import *
from tkinter import messagebox
from tkinter import *
from nn import *
import random
from keras.models import load_model


#雷盘界面GUI
class GameGui():
    def __init__(self, row, col, minenum, master = None):
        self.count = 0#步数
        self.count_list = []#存储步数，便于求平均步数
        self.dis_rate_list = []#存储开采率，便于求平均
        self.discovered = []#集合A，已探明（旗，数字（包括0））
        self.peripheral = []#集合B，所有已探明的格子外围8格的总和-已探明部分（即，已知区域外围的总和）
        self.flags = []#集合C，存储所有的旗子

        self.row = row
        self.col = col
        self.minenum = minenum
        self.model = load_model('minemodel.h5')
        self.board = array([[10 for i in range(self.col)] for j in range(self.row)])#play时显示的表
        self.mineboard = MineBoard(self.row, self.col, self.minenum)#mineboard类型
        self.boardlist = self.mineboard.getboard()#list类型，存储实际的分布表

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
        self.discovered = []
        self.peripheral = []
        self.flags = []
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
        if self.board[i][j] == -1:#雷
            return './image/icons8-地雷-20.png'
        elif self.board[i][j] == 0:#数字0
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
        elif self.board[i][j] == 8:#数字8
            return './image/8.png'
        elif self.board[i][j] == 11:#旗子
            return './image/flag.png'
        elif self.board[i][j] == 10:#未知区域
            return './image/unknown.png'
        else:#除了以上，还有一种，在棋盘外，赋值为9
            print('board error')
            exit(0)

    def nn_loop(self):
        self.file = open('dataset.csv', 'a')
        flags_cache = []
        while 1:
            if self.mineboard.getflag() == 0:
                if self.discovered == (self.row * self.col):#防止旗子数量超过雷数量
                    if len(flags_cache) == 0:#重复循环遍历flags
                        flags_cache = self.flags
                    for c in flags_cache:
                        x, y = c
                        plist, _ = self.traverse_per(x, y)  # 存储每一个点的外围区8个坐标的值
                        pred = predict_next(self.model, plist)  # 得到预测值，范围在0~1
                        if pred < 0.5:  # 预测值亲近0，则右键行动
                            click_flag = 1
                        else:  # 亲近1，左键行动
                            click_flag = 0
                    flags_cache.remove((x,y))
                else:
                    x, y, click_flag = self.get_best_point()

                self.count += 1

                plist, p_point_list = self.traverse_per(x, y)
                for i in range(len(plist)):
                    if plist[i] != 11:#碰到旗子的时候按实际情况存储
                        self.file.writelines(str(plist[i]) + ' ')
                    else:
                        xi, yi = p_point_list[i]
                        self.file.writelines(str(self.boardlist[xi][yi]) + ' ')
                # print('click', x+1,y+1, click_flag)
                if self.boardlist[x][y] == -1:
                    self.file.writelines('0\n')
                else:
                    self.file.writelines('1\n')
                if click_flag == 1:
                    self.board[x][y] = 11
                    self.flags.append((x, y))
                    #更新集合A，B
                    self.update_set(x, y)
                else:
                    if self.boardlist[x][y] == -1:  # 踩到雷
                        self.board[x][y] = self.boardlist[x][y]
                        self.mineboard.setflag(-1)
                    elif self.boardlist[x][y] == 0:  # 踩到安全区域，更新集合A B
                        self.board[x][y] = self.boardlist[x][y]
                        dedlist = []  # 去重列表
                        self.zerosloop(x, y, dedlist)  # 遍历，将相邻的0全部显示
                        self.update_set(x, y)
                    else:  # 踩到数字，更新集合A B
                        self.board[x][y] = self.boardlist[x][y]
                        self.update_set(x, y)
                # self.print_board()
                self.show()
                self.judge()
            else:
                break
        self.file.close()

    def update_set(self, x, y):
        if (x,y) not in self.discovered:
            self.discovered.append((x, y))
        if (x, y) in self.peripheral:
            self.peripheral.remove((x, y))
        _, p_point_list = self.traverse_per(x, y)
        for pp in p_point_list:
            if pp not in self.peripheral:
                if pp not in self.discovered:
                    if pp != None:
                        self.peripheral.append(pp)

    def get_best_point(self):
        click_flag = 0#表明时左键行动或右键行动，默认左键
        if len(self.peripheral) == 0:#刚开局数组B为空，随机踩个位置
            return random.randint(0, self.row - 1), random.randint(0, self.col - 1), click_flag
        else:
            max_pred = -1
            x_cache = 0
            y_cache = 0
            for p in self.peripheral:#遍历集合B，集合B中的每一个点对应一个预测值
                x, y = p
                plist, _ = self.traverse_per(x, y)#存储每一个点的外围区8个坐标的值
                pred = predict_next(self.model, plist)#得到预测值，范围在0~1
                abs_pred = abs(0.5 - pred)
                if max_pred < abs_pred:
                    max_pred = abs_pred
                    x_cache = x
                    y_cache = y
                    if abs_pred == (0.5-pred):#预测值亲近0，则右键行动
                        click_flag = 1
                    else:#亲近1，左键行动
                        click_flag = 0
            return x_cache, y_cache, click_flag


    def traverse_per(self, x, y):#获取外围坐标的值存入plist
        plist = [0 for i in range(8)]
        p_point_list = [(0, 0) for i in range(8)]#存储外围点的坐标
        if x - 1 < 0:
            plist[0] = 9
            plist[1] = 9
            plist[2] = 9
            plist[6] = self.board[x + 1][y]
            if y - 1 < 0:#该点位于左上
                plist[3] = 9
                plist[4] = self.board[x][y+1]
                plist[5] = 9
                plist[7] = self.board[x+1][y+1]
            elif y - 1 >= 0 and y + 1 < self.col:  # 最上列
                plist[3] = self.board[x][y-1]
                plist[4] = self.board[x][y+1]
                plist[5] = self.board[x+1][y-1]
                plist[7] = self.board[x+1][y+1]
            else:  # 右上角
                plist[3] = self.board[x][y - 1]
                plist[4] = 9
                plist[5] = self.board[x + 1][y - 1]
                plist[7] = 9
        elif x - 1 >= 0 and x + 1 < self.row:
            plist[1] = self.board[x - 1][y]
            plist[6] = self.board[x + 1][y]
            if y - 1 < 0:  # 最左列
                plist[0] = 9
                plist[2] = self.board[x-1][y+1]
                plist[3] = 9
                plist[4] = self.board[x][y + 1]
                plist[5] = 9
                plist[7] = self.board[x + 1][y + 1]
            elif y - 1 >= 0 and y + 1 < self.col:  # 内层
                plist[0] = self.board[x-1][y-1]
                plist[2] = self.board[x - 1][y + 1]
                plist[3] = self.board[x][y-1]
                plist[4] = self.board[x][y + 1]
                plist[5] = self.board[x+1][y-1]
                plist[7] = self.board[x + 1][y + 1]
            else:  # 最右列
                plist[0] = self.board[x-1][y-1]
                plist[2] = 9
                plist[3] = self.board[x][y-1]
                plist[4] = 9
                plist[5] = self.board[x+1][y-1]
                plist[7] = 9
        else:
            plist[1] = self.board[x - 1][y]
            plist[5] = 9
            plist[6] = 9
            plist[7] = 9
            if y - 1 < 0:  # 左下角
                plist[0] = 9
                plist[2] = self.board[x-1][y+1]
                plist[3] = 9
                plist[4] = self.board[x][y+1]
            elif y - 1 >= 0 and y + 1 < self.col:  # 最下列
                plist[0] = self.board[x-1][y-1]
                plist[2] = self.board[x - 1][y + 1]
                plist[3] = self.board[x][y-1]
                plist[4] = self.board[x][y + 1]
            else:  # 右下角
                plist[0] = self.board[x-1][y-1]
                plist[2] = 9
                plist[3] = self.board[x][y-1]
                plist[4] = 9
        for i in range(8):
            if plist[i] == 9:
                p_point_list[i] = None
            else:
                if i == 0:
                    p_point_list[i] = (x-1,y-1)
                elif i == 1:
                    p_point_list[i] = (x-1,y)
                elif i == 2:
                    p_point_list[i] = (x-1, y+1)
                elif i == 3:
                    p_point_list[i] = (x, y-1)
                elif i == 4:
                    p_point_list[i] = (x,y+1)
                elif i == 5:
                    p_point_list[i] = (x+1,y-1)
                elif i == 6:
                    p_point_list[i] = (x+1,y)
                elif i == 7:
                    p_point_list[i] = (x+1,y+1)
                else:
                    print('p_point_list error')
        return plist, p_point_list

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
                if (i, j) not in dedlist:#去重，防止重复遍历
                    dedlist.append((i, j))
                    if self.board[i][j] == 11:#遇到标旗的区域，直接跳过
                        pass
                    else:
                        if self.boardlist[i][j] == 0:#如果为数字0，则继续循环遍历
                            self.board[i][j] = self.boardlist[i][j]
                            self.update_set(i, j)
                            self.zerosloop(i, j, dedlist)
                        else:#数字1~8，则停止遍历
                            self.board[i][j] = self.boardlist[i][j]
                            self.update_set(i, j)

    def judge(self):
        count = 0
        if self.mineboard.getflag() == -1:
            self.count_list.append(self.count)
            print('步数:%d' % self.count)
            print('平均步数:%d' % (sum(self.count_list) // len(self.count_list)))
            self.discover_rate()
        else:
            for i in range(self.row):#当全部的非雷都踩出来后，获得胜利
                for j in range(self.col):
                    if self.boardlist[i][j] != -1:#对于每一个非雷的区块
                        if self.board[i][j] == self.boardlist[i][j]:
                            count += 1
            if count == (self.row * self.col - self.minenum):
                self.mineboard.setflag(1)
            if self.mineboard.getflag() == 1:#获得胜利，游戏结束
                self.count_list.append(self.count)
                print('步数:%d' % self.count)
                print('平均步数:%d' % (sum(self.count_list) // len(self.count_list)))
                self.discover_rate()
            else:
                pass

    def discover_rate(self):#在结束的时候显示开采率,平均开采率
        if self.count == 1:#不统计一步就踩雷的情况
            pass
        else:
            b = []
            for i in self.board:
                for j in i:
                    b.append(j)
            cap = self.row * self.col
            rate = (cap - b.count(10) - b.count(11)) / cap * 100
            self.dis_rate_list.append(rate)
            rate_avg = sum(self.dis_rate_list) / len(self.dis_rate_list)
            max_rate = (cap - self.minenum) / cap
            rate = rate / max_rate
            rate_avg = rate_avg / max_rate
            print('开采率：%.2f%%' % rate)
            print('平均开采率：%.2f%%' % rate_avg)

    def print_boardlist(self):
        for i in self.boardlist:
            for j in i:
                print(j, end='\t')
            print()

    def print_board(self):
        for i in self.board:
            for j in i:
                print(j, end='\t')
            print()