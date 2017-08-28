# -*- coding: utf-8 -*-
import requests
import re
import time, sys, os
import mp3play
from Tkinter import *
from ctypes import windll
import pygame
from optparse import OptionParser


def get_cli_options():
    parser = OptionParser(usage="usage: python %prog [options]",
                          description=""".........Zabbix Spider.........""")
    parser.add_option("-t", "-t",
                      dest="type",
                      help="1)slience , 2)noise ")
    '''
    parser.add_option("-m", "-m",
                      dest="mode",
                      help="1)company , 2)home")   
    ''' 
    (options, args) = parser.parse_args()
    return options

def get_regex(type):
    auth_data = {
        "autologin": 1,
        "enter": "Sign in",
        "name": "xxxx",
        "password": "xxxx"
    }
    url = "http://dbmonitor.jd.com/index.php"
    '''
    if mode == "1":
        url = "http://zabbixm.mysql.jddb.com/index.php"
    elif mode == "2":
        url = "http://dbmonitor.jd.com/index.php"
    '''
    s = requests.session()
    r = s.post(url, data=auth_data)
    # print r.cookies
    token = r.cookies["zbx_sessionid"]
    # print token
    # print help(token)
    # print help(r.cookies)
    token = r.cookies["zbx_sessionid"][-16:]


    while True:
        try:
            #data = "favobj=hat&favref=hat_syssum&favaction=refresh"
            #url = "http://dbmonitor.jd.com/dashboard.php?output=html&sid=%s&upd_counter=1&pmasterid=mainpage&" % token

            #data = "favobj=hat&favref=hat_syssum&favaction=refresh"
            #url = "http://dbmonitor.jd.com/dashboard.php?output=html&sid=%s&upd_counter=&pmasterid=dashboard&" % token 

            url = "http://dbmonitor.jd.com/zabbix.php?action=widget.issues.view&sid=%s&upd_counter=37&pmasterid=dashboard" %token

            '''
            if mode == "1":
                url = "http://zabbixm.mysql.jddb.com/dashboard.php?output=html&sid=%s&upd_counter=1&pmasterid=mainpage&" % token
            elif mode == "2":
                url = "http://dbmonitor.jd.com/dashboard.php?output=html&sid=%s&upd_counter=1&pmasterid=mainpage&" % token
            '''
            #url += data
            r = s.post(url)
            '''
            print r.text
            reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
            for ip in reip.findall(r.text):
                print "ip>>>", ip
            
            restr = re.compile(
                r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]) Server is Down|(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]) OS has just been restarted|(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]) Slave Run failed Error|(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]) MYSQL Port cannnot Connet|(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]) mysqld has just been restarted|(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]) Disk space Full on|(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]) SlaveDelay lag too much')
            '''
            restr = re.compile(
                r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]) Server is Down|(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]) OS has just been restarted|(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]) Slave Run failed Error|(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]) MYSQL Port cannnot Connet|(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]) mysqld has just been restarted')
            
            for value in restr.findall(r.text):
                print value
                if type=='1':
                    showMessage(value)
                elif type=='2':
                    while True:
                        do_alert()
                        time.sleep(10)
        except Exception as e:
            auth_data = {
                "autologin": 1,
                "enter": "Sign in",
                "name": "zhaochen72",
                "password": "Runrabbit.0615"
            }
            url = "http://dbmonitor.jd.com/index.php"
            '''
            if mode == "1":
                url = "http://zabbixm.mysql.jddb.com/index.php"
            elif mode == "2":
                url = "http://dbmonitor.jd.com/index.php"
            '''
            s = requests.session()
            r = s.post(url, data=auth_data)
            # print r.cookies
            token = r.cookies["zbx_sessionid"]
            # print token
            # print help(token)
            # print help(r.cookies)
            token = r.cookies["zbx_sessionid"][-16:]
   
        time.sleep(30)

def do_alert():
    '''
    WM_APPCOMMAND = 0x319
    APPCOMMAND_VOLUME_UP = 0x0a
    APPCOMMAND_VOLUME_DOWN = 0x09
    APPCOMMAND_VOLUME_MUTE = 0x08
    hwnd = windll.user32.GetForegroundWindow()
    windll.user32.PostMessageA(hwnd, WM_APPCOMMAND, 0, APPCOMMAND_VOLUME_MUTE * 0x10000)
    '''
    pygame.mixer.init()
    track = pygame.mixer.music.load('4215.mp3')
    pygame.mixer.music.play()


def showMessage(alert_txt):
    # show reminder message window
    root = Tk()  # 建立根窗口
    # root.minsize(500, 200)   #定义窗口的大小
    # root.maxsize(1000, 400)  #不过定义窗口这个功能我没有使用
    root.withdraw()  # hide window
    # 获取屏幕的宽度和高度，并且在高度上考虑到底部的任务栏，为了是弹出的窗口在屏幕中间
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight() - 100
    root.resizable(False, False)
    # 添加组件
    root.title("Warning!!")
    frame = Frame(root, relief=RIDGE, borderwidth=3)
    frame.pack(fill=BOTH, expand=1)  # pack() 放置组件若没有则组件不会显示
    # 窗口显示的文字、并设置字体、字号
    label = Label(frame, text=alert_txt, font="Monotype\ Corsiva -20 bold")
    label.pack(fill=BOTH, expand=1)
    # 按钮的设置
    button = Button(frame, text="OK", font="Cooper -25 bold", fg="red", command=root.destroy)
    button.pack(side=BOTTOM)

    root.update_idletasks()
    root.deiconify()  # now the window size was calculated
    root.withdraw()  # hide the window again 防止窗口出现被拖动的感觉 具体原理未知？
    root.geometry('%sx%s+%s+%s' % (root.winfo_width() + 10, root.winfo_height() + 10,
                                   (screenwidth - root.winfo_width()) / 2, (screenheight - root.winfo_height()) / 2))
    root.deiconify()
    root.mainloop()


if __name__ == '__main__':
    options = get_cli_options()
    type=options.type
    #mode=options.mode
    get_regex(type)
