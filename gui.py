from tkinter import *
from tkinter.filedialog import askdirectory
import tkinter.messagebox
from tkinter import ttk
import requests
import os
import threading
import inspect
import ctypes
import time

x_1=-1
th=[]
def selectPath():
    path_ = askdirectory()
    path.set(path_)

root = Tk()
root.title('抓取百度图片数据')
path = StringVar()
p = ttk.Progressbar(root, orient="horizontal", length=300, mode='determinate').grid(row=4, column=0,columnspan=3)
ll=Label(root, text="00/00张",font=("Monaco", 16)).grid(row=4,column=2,sticky=E)


def getManyPages(keyword,pages):
    params=[]
    for i in range(30,30*pages+30,30):
        params.append({
                      'tn': 'resultjson_com',
                      'ipn': 'rj',
                      'ct': 201326592,
                      'is': '',
                      'fp': 'result',
                      'queryWord': keyword,
                      'cl': 2,
                      'lm': -1,
                      'ie': 'utf-8',
                      'oe': 'utf-8',
                      'adpicid': '',
                      'st': -1,
                      'z': '',
                      'ic': 0,
                      'word': keyword,
                      's': '',
                      'se': '',
                      'tab': '',
                      'width': '',
                      'height': '',
                      'face': 0,
                      'istype': 2,
                      'qc': '',
                      'nc': 1,
                      'fr': '',
                      'pn': i,
                      'rn': 30,
                      'gsm': '1e',
                      '1488942260214': ''
                  })
    url = 'https://image.baidu.com/search/acjson'
    urls = []
    for i in params:
        urls.append(requests.get(url,params=i).json().get('data'))

    return urls


def getImg(dataList, localPath):
    global x_1
    global p
    global ll
    global b1
    global b2
    if not os.path.exists(localPath):  # 新建文件夹
        os.mkdir(localPath)
    x = 0
    print( 'nun:'+str(int(w.get()) * 30))
    for list in dataList:
        for i in list:
            if i.get('thumbURL') != None:
                print('正在下载第'+str(x+1)+'：%s' % i.get('thumbURL'))
                ir = requests.get(i.get('thumbURL'))
                open(localPath + '/'+str(entry2.get())+'%d.jpg' % x, 'wb').write(ir.content)
                x += 1
                x_1=x
                if x<10:
                    ll=Label(root, text='0'+str(x) + "/"+str(int(w.get()) * 30)+"张", font=("Monaco", 16)).grid(row=4, column=2, sticky=E)
                else:
                    ll= Label(root, text=str(x) + "/" + str(int(w.get()) * 30) + "张", font=("Monaco", 16)).grid(row=4,column=2,sticky=E)
            else:
                pass
            print("x:" + str(x + 1) + "  num:" + str(int(w.get()) * 30))
            p = ttk.Progressbar(root, orient="horizontal", length=300, mode='determinate',value=x,maximum=int(w.get()) * 30).grid(row=4, column=0,columnspan=3)
            root.update()
            time.sleep(0.1)

def execute_asyn():
    global p
    global th
    global b1
    global b2
    def sp():
        b1 = Button(root, text='运行', font=("Monaco", 16), width=10, command=execute_asyn,state='disabled').grid(row=6, column=1,sticky=E)
        b2 = Button(root, text='停止', font=("Monaco", 16), width=10, command=pause,state='normal').grid(row=6, column=2)
        userPath = str(path.get())
        keyWord = str(entry2.get())
        num = int(w.get())
        if keyWord=='':
            tkinter.messagebox.showinfo('错误', '搜索内容不能为空')
            b1 = Button(root, text='运行', font=("Monaco", 16), width=10, command=execute_asyn, state='normal').grid(
                row=6, column=1, sticky=E)
            b2 = Button(root, text='停止', font=("Monaco", 16), width=10, command=pause, state='disabled').grid(row=6,
                                                                                                              column=2)
            return
        if userPath=='':
            tkinter.messagebox.showinfo('错误', '保存路径不能为空')
            b1 = Button(root, text='运行', font=("Monaco", 16), width=10, command=execute_asyn, state='normal').grid(row=6, column=1, sticky=E)
            b2 = Button(root, text='停止', font=("Monaco", 16), width=10, command=pause, state='disabled').grid(row=6,column=2)
            return
        if num<0 or num>10:
            tkinter.messagebox.showinfo('错误', '搜索数量在1-10页之间')
            b1 = Button(root, text='运行', font=("Monaco", 16), width=10, command=execute_asyn, state='normal').grid(row=6, column=1, sticky=E)
            b2 = Button(root, text='停止', font=("Monaco", 16), width=10, command=pause, state='disabled').grid(row=6,column=2)
        print(num)
        p = ttk.Progressbar(root, orient="horizontal", length=300, mode='determinate',maximum=int(num*30)).grid(row=4, column=0,columnspan=3)

        try:
            dataList = getManyPages(keyWord, num)  # 参数1:关键字，参数2:要下载的页数
        except:
            pass
        try:
            getImg(dataList, userPath)  # 参数2:指定保存的路径
            tkinter.messagebox.showinfo('成功', '执行完毕')
            b1 = Button(root, text='运行', font=("Monaco", 16), width=10, command=execute_asyn, state='normal').grid(row=6, column=1, sticky=E)
            b2 = Button(root, text='停止', font=("Monaco", 16), width=10, command=pause, state='disabled').grid(row=6,column=2)
        except:
            pass

    th = threading.Thread(target=sp)
    th.setDaemon(True)
    th.start()


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)



def pause():
    global th
    global b1
    global b2
    b1 = Button(root, text='运行', font=("Monaco", 16), width=10, command=execute_asyn,state='normal').grid(row=6, column=1, sticky=E)
    b2 = Button(root, text='停止', font=("Monaco", 16), width=10, command=pause,state='disabled').grid(row=6, column=2)
    stop_thread(th)

Label(root,text = "选择存放图片的文件夹:",font=("Monaco", 16)).grid(row = 0, column = 0)
entry0=Entry(root, textvariable = path,font=("Monaco", 16),state=DISABLED).grid(row = 0, column = 1)
Button(root, text = "浏览", command = selectPath,font=("Monaco", 16),width=10).grid(row = 0, column = 2)

Label(root, text="要搜索的图片的关键字:",font=("Monaco", 16)).grid(row=1)
entry2=Entry(root,font=("Monaco", 16))
entry2.grid(row=1, column=1)

Label(root, text="爬取的页数:",font=("Monaco", 16)).grid(row=2,column=0)
w = Spinbox(root, from_=1,to=10,font=("Monaco", 15),width=21)
w.grid(row=2, column=1)
Label(root, text=" *30张",font=("Monaco", 16)).grid(row=2, column=2)

Label(root, text="                   ",font=("Monaco", 6)).grid(row=3,column=2)

Label(root, text="                   ",font=("Monaco", 3)).grid(row=5,column=2)
b1=Button(root, text='运行',font=("Monaco", 16),width=10,command=execute_asyn).grid(row=6, column=1,sticky=E)
b2=Button(root, text='停止',font=("Monaco", 16),width=10,command=pause ,state='disabled').grid(row=6, column=2)
Label(root, text="                   ",font=("Monaco", 4)).grid(row=7,column=0)
Label(root, text="    ",font=("Monaco", 4)).grid(row=7,column=3)

root.mainloop()