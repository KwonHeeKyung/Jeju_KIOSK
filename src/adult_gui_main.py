# Made by Kim.Seung.Hwan / ksana1215@interminds.ai
#-*- coding: utf-8 -*-
import os
from tkinter import*
import tkinter.font
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk, Image, ImageEnhance, ImageDraw
from playsound import playsound
import json
import datetime
import request_main
import configparser

config = configparser.ConfigParser()
config.read(os.path.join(os.path.split(__file__)[0],'config.ini'))

#키오스크 UI
class Uipage:
    def __init__(self,root,rd):
        self.rd=rd
        self.root = root
        self.root.title("INTERMINDS")
        self.cf_path = config['path']['path']
        self.deviceId = config['refrigerators']['deviceId']
        self.canvas = Canvas(self.root, height=1024, width=600)
        self.start_img = PhotoImage(file=self.cf_path+'asset/START.png')
        self.auth_select_img = PhotoImage(file=self.cf_path + 'asset/SELECT_ADULT.png')
        self.auth_adult_img = PhotoImage(file=self.cf_path+'asset/AUTH_ADULT.png')
        self.auth_adult_mobile = PhotoImage(file=self.cf_path + 'asset/AUTH_ADULT_MOBILE.png')
        self.auth_adult_rrn = PhotoImage(file=self.cf_path + 'asset/AUTH_ADULT_RRN.png')
        self.auth_wait_img = PhotoImage(file=self.cf_path + 'asset/AUTH_ADULT_INFO.png')
        self.auth_fail_img = PhotoImage(file=self.cf_path+'asset/AUTH_FAIL.png')
        self.sign_img = PhotoImage(file=self.cf_path+ 'asset/SIGN.png')
        self.card_img = PhotoImage(file=self.cf_path+'asset/CARD_INSERT.png')
        self.remove_img = PhotoImage(file=self.cf_path+'asset/REMOVE_CARD.png')
        self.shop_img = PhotoImage(file=self.cf_path + 'asset/SHOPPING.png')
        if self.deviceId[0] == 'c':
            self.shop_img = PhotoImage(file=self.cf_path + 'asset/SHOPPING_CIGARETTE.png')
        self.device_err_img = PhotoImage(file=self.cf_path+'asset/DEVICE_ERR.png')
        self.fail_img = PhotoImage(file=self.cf_path+'asset/DEVICE_FAIL.png')
        self.hh_deny_img = PhotoImage(file=self.cf_path+'asset/HH_DENY.png')
        self.sspay_deny_img = PhotoImage(file=self.cf_path+'asset/SSPAY_DENY.png')
        self.payment_fail_img = PhotoImage(file=self.cf_path+'asset/PAYMENT_FAIL.png')
        self.no_money_img = PhotoImage(file=self.cf_path+'asset/NO_MONEY.png')
        self.admin_img = PhotoImage(file=self.cf_path+'asset/ADMIN.png')
        self.end_img = PhotoImage(file=self.cf_path+'asset/END.png')
        self.end_none_img = PhotoImage(file=self.cf_path+'asset/END_NONE.png')
        self.inf_img = PhotoImage(file=self.cf_path+'asset/INFER.png')
        self.canvas.bind("<Button-1>", self.S_BTN)
        self.readRedis()
        self.rd.flushdb()
        self.root.attributes('-fullscreen', True)
        self.cnt = 0
        self.START_PAGE()
        self.b1 = "up"
        self.signLen = 0
        self.orderText = StringVar()
        self.orderAmt = StringVar()
        self.drawingArea = None
        self.signImage = None
        self.xold = None
        self.yold = None

    #시작화면 복귀
    def comeback(self):
        page_timer = self.rd.get('nowPage')
        if page_timer is None:
            pass
        elif page_timer == b'sign':
            self.cnt += 1
            if self.cnt >= 100:
                self.cnt = 0
                self.START_PAGE()
                return
        elif page_timer == b'auth_adult':
            self.cnt += 1
            if self.cnt >= 100:
                self.cnt = 0
                self.START_PAGE()
                return
        elif page_timer == b'pass_auth':
            self.cnt += 1
            if self.cnt >= 100:
                self.cnt = 0
                self.START_PAGE()
                return
        elif page_timer == b'mobile_auth':
            self.cnt += 1
            if self.cnt >= 100:
                self.cnt = 0
                self.START_PAGE()
                return
        elif page_timer == b'rrn_auth':
            self.cnt += 1
            if self.cnt >= 100:
                self.cnt = 0
                self.START_PAGE()
                return
        elif page_timer == b'end':
            self.cnt += 1
            if self.cnt == 30:
                self.cnt = 0
                self.START_PAGE()
                return
        elif page_timer == b'end_none':
            self.cnt += 1
            if self.cnt == 20:
                self.cnt = 0
                self.START_PAGE()
                return
        elif page_timer == b'fail':
            self.cnt += 1
            if self.cnt == 30:
                self.cnt = 0
                self.START_PAGE()
                return
        elif page_timer == b'auth_fail':
            self.cnt += 1
            if self.cnt == 30:
                self.cnt = 0
                self.START_PAGE()
                return
        elif page_timer == b'no_money':
            self.cnt += 1
            if self.cnt == 30:
                self.cnt = 0
                self.START_PAGE()
                return
        elif page_timer == b'hh_deny':
            self.cnt += 1
            if self.cnt == 30:
                self.cnt = 0
                self.START_PAGE()
                return
        elif page_timer == b'sspay_deny':
            self.cnt += 1
            if self.cnt == 30:
                self.cnt = 0
                self.START_PAGE()
        elif page_timer == b'start':
            self.cnt = 0
            return
        else:
            self.cnt = 0
        self.root.after(1000, self.comeback)

    #터치 버튼 이벤트
    def S_BTN(self, event):
        flg = self.rd.get('nowPage')
        if flg == None:
            pass
        elif flg == b'start':
            if 170 < event.x < 425 and 520 < event.y < 630:
                request_main.check_status()
        elif flg == b'sign':
            if 110 < event.x < 280 and 900 < event.y < 990:
                self.START_PAGE()
            if 320 < event.x < 480 and 900 < event.y < 990:
                if self.signLen >10:
                    log_time = datetime.datetime.now()
                    log_time = log_time.strftime("%Y-%m-%d-%H-%M-%S")
                    self.signImage.save(self.cf_path+f'consent/{log_time}.bmp')
                    self.rd.set('msg', 'card')
        elif flg == b'auth_adult' or b'pass_auth' or b'mobile_auth' or b'rrn_auth':
            if 210 < event.x < 380 and 900 < event.y < 990:
                self.START_PAGE()
            # if flg == b'auth_adult' and 385 < event.x < 460 and 665 < event.y < 750:
            #     self.AUTH_PASS()
            # elif flg == b'auth_adult' and 320 < event.x < 420 and 770 < event.y < 870:
            #     self.AUTH_MOBILE()
            # elif flg == b'auth_adult' and 450 < event.x < 530 and 770 < event.y < 870:
            #     self.AUTH_RRN()
            if flg == b'auth_adult' and 85 < event.x < 220 and 645 < event.y < 775:
                self.AUTH_PASS()
            elif flg == b'auth_adult' and 245 < event.x < 375 and 645 < event.y < 775:
                self.AUTH_MOBILE()
            elif flg == b'auth_adult' and 410 < event.x < 515 and 645 < event.y < 775:
                self.AUTH_RRN()
        elif flg == b'wait_mobileid':
            if 210 < event.x < 380 and 900 < event.y < 990:
                self.START_PAGE()
        elif flg == b'auth_fail':
            if 210 < event.x < 380 and 900 < event.y < 990:
                self.START_PAGE()
        elif flg == b'fail':
            if 210 < event.x < 380 and 900 < event.y < 990:
                self.START_PAGE()
        elif flg == b'no_money':
            if 210 < event.x < 380 and 900 < event.y < 990:
                self.START_PAGE()
        elif flg == b'hh_deny':
            if 210 < event.x < 380 and 900 < event.y < 990:
                self.START_PAGE()
        elif flg == b'sspay_deny':
            if 210 < event.x < 380 and 900 < event.y < 990:
                self.START_PAGE() 
        elif flg == b'end':
            if 210 < event.x < 380 and 900 < event.y < 990:
                self.START_PAGE()
        elif flg == b'end_none':
            if 210 < event.x < 380 and 900 < event.y < 990:
                self.START_PAGE()

    #시작 화면
    def START_PAGE(self):
        self.clearAllWidgets()
        self.rd.set('nowPage','start')
        self.canvas.create_image(0, 0, anchor=NW, image=self.start_img)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.comeback()

    #성인 인증 요청
    def AUTH_ADULT(self):
        self.rd.set('nowPage', 'auth_adult')
        self.canvas.create_image(0, 0, anchor=NW, image=self.auth_select_img)
        self.comeback()

    # PASS 인증
    def AUTH_PASS(self):
        self.rd.set('nowPage', 'pass_auth')
        self.canvas.create_image(0, 0, anchor=NW, image=self.auth_adult_img)
        self.cnt = 0
        self.playWav('auth_pass')

    # 모바일 신분증 인증 QR 스캔
    def AUTH_MOBILE(self):
        self.rd.set('nowPage', 'mobile_auth')
        self.canvas.create_image(0, 0, anchor=NW, image=self.auth_adult_mobile)
        self.cnt = 0
        self.playWav('auth_mobile')

    # 모바일 신분증 인증 정보보내기
    def WAIT_ADULT(self):
        self.canvas.create_image(0, 0, anchor=NW, image=self.auth_wait_img)

    # 정부24 주민등록증 모바일 확인 서비스
    def AUTH_RRN(self):
        self.rd.set('nowPage', 'rrn_auth')
        self.canvas.create_image(0, 0, anchor=NW, image=self.auth_adult_rrn)
        self.cnt = 0
        self.playWav('auth_rrn')

    # 성인 인증 실패
    def AUTH_FAIL(self):
        self.rd.set('nowPage', 'auth_fail')
        self.cnt = 0
        self.canvas.create_image(0, 0, anchor=NW, image=self.auth_fail_img)
        self.comeback()

    #정보제공동의
    def SIGN_PAGE(self):
        self.rd.set('sign','o')
        self.rd.set('nowPage','sign')
        self.canvas.create_image(0, 0, anchor=NW, image=self.sign_img)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.drawingArea = Canvas(self.canvas, width=390, height=120, bg='white', bd=0, highlightthickness=0)
        self.drawingArea.place(x=103, y=730)
        self.drawingArea.bind("<Motion>", self.motion)
        self.drawingArea.bind("<ButtonPress-1>", self.b1down)
        self.drawingArea.bind("<ButtonRelease-1>", self.b1up)
        self.signImage = Image.new("RGB", (500, 200), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.signImage)
        # self.comeback()
        self.cnt = 0

    # 터치 싸인 그리기 모션 1
    def b1down(self,event):
        self.b1 = "down"

    # 터치 싸인 그리기 모션 2
    def b1up(self,event):
        self.b1 = "up"
        self.xold = None
        self.yold = None

    # 터치 싸인 그리기 모션 3
    def motion(self,event):
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                event.widget.create_line(self.xold, self.yold, event.x, event.y, smooth='true', width=3, fill='black')
                self.draw.line(((self.xold,self.yold),(event.x,event.y)),(0,128,0),width=3)
                self.signLen = event.x+event.y
        self.xold = event.x
        self.yold = event.y

    #카드 삽입 오쳥
    def CARD_PAGE(self):
        self.clearAllWidgets()
        self.rd.set('nowPage', 'card')
        self.canvas.create_image(0, 0, anchor=NW, image=self.card_img)

    #카드 제거 요청
    def REMOVE_PAGE(self):
        self.clearAllWidgets()
        self.rd.set('nowPage', 'remove')
        self.canvas.create_image(0, 0, anchor=NW, image=self.remove_img)

    #문열리고 쇼핑시작
    def SHOPPING_PAGE(self):
        self.rd.set('nowPage', 'shopping')
        self.canvas.create_image(0, 0, anchor=NW, image=self.shop_img)

    #문닫히고 인퍼런스
    def INF_PAGE(self):
        self.rd.set('nowPage','inf')
        self.canvas.create_image(0, 0, anchor=NW, image=self.inf_img)

    #영수증 화면
    def END(self):
        order_list = json.loads(self.rd.get('ol'))
        self.rd.set('nowPage', 'end')
        self.canvas.create_image(0,0, anchor=NW, image=self.end_img)
        self.orderText.set('')
        tp = []
        for order_list in order_list:
            strOut = order_list['goodsName'] + '\n'
            strOut2 = '%30s' % str(format(int(order_list['goodsCnt']))) +' '*6 + format(int(order_list['goodsPrice']),',') + '원' + '\n'
            orders = strOut + strOut2 + '-------------------------------------------\n'
            self.orderText.set(self.orderText.get() + orders)
            price =int(order_list['goodsPrice']) * int(order_list['goodsCnt'])
            tp.append(price)
            total_price =sum(tp)
        orderFont = tkinter.font.Font(family="맑은 고딕", weight="bold",size=14)
        self.orderAmt.set(format(int(total_price), ','))
        self.orderFrame = Frame(self.canvas)
        self.orderBar = Scrollbar(self.orderFrame)
        self.orderAmtLabel = Label(self.canvas, bd=0, textvariable=self.orderAmt, font=("맑은 고딕", 30, "bold"), width=10, bg='white', anchor='e') #총 결제금액
        self.orderBar.pack(side = RIGHT, fill = "y")
        self.orderBox = Text(self.orderFrame,height = 8, width = 30, yscrollcommand = self.orderBar.set,wrap = "none",selectbackground = "white",selectforeground = "black",font=orderFont,borderwidth=0)
        self.orderBox.pack()
        self.orderBox.insert('1.0', self.orderText.get())
        self.orderBox.configure(state='disabled')
        self.orderBar.config(command = self.orderBox.yview)
        self.orderAmtLabel.place(x=192, y=523)
        self.orderFrame.place(x=128, y=637)
        self.orderBox.tag_add('found', 1.0, 1.0)
        self.orderBox.tag_config('found', foreground='white')
        self.rd.set('box','o')
        self.comeback()

    #아무것도 안삼
    def END_NONE(self):
        self.rd.set('nowPage', 'end_none')
        self.canvas.create_image(0, 0, anchor=NW, image=self.end_none_img)
        self.comeback()

    #상태조회 오류
    def FAIL_PAGE(self):
        self.rd.set('nowPage', 'fail')
        self.canvas.create_image(0, 0, anchor=NW, image=self.fail_img)
        self.comeback()

    #키오스크 장치 오류
    def DEVICE_ERR_PAGE(self):
        self.clearAllWidgets()
        self.rd.set('nowPage', 'device_err')
        self.canvas.create_image(0, 0, anchor=NW, image=self.device_err_img)

    #현대,하나카드 거절
    def HH_DENY(self):
        self.rd.set('nowPage', 'hh_deny')
        self.canvas.create_image(0, 0, anchor=NW, image=self.hh_deny_img)
        self.comeback()
        
    #삼성페이 거절
    def SSPAY_DENY(self):
        self.rd.set('nowPage', 'sspay_deny')
        self.canvas.create_image(0, 0, anchor=NW, image=self.sspay_deny_img)
        self.comeback()

    #결제 실패
    def PAYMENT_FAIL_PAGE(self):
        self.rd.set('nowPage', 'fail')
        self.canvas.create_image(0, 0, anchor=NW, image=self.payment_fail_img)
        self.comeback()

    #잔액 부족
    def NO_MONEY(self):
        self.rd.set('nowPage', 'no_money')
        self.canvas.create_image(0, 0, anchor=NW, image=self.no_money_img)
        self.comeback()

    #관리자 권한 점유
    def ADMIN_PAGE(self):
        self.rd.set('nowPage','admin')
        self.canvas.create_image(0,0, anchor=NW, image=self.admin_img)

    #페이지 루프
    def readRedis(self):
        try:
            msg = self.rd.get("msg")
            if msg is None:
                pass
            elif msg == b'START':
                self.START_PAGE()
                self.rd.delete('msg')

            elif msg == b'000':
                self.AUTH_ADULT()
                self.playWav('auth_adult')
                self.rd.delete('msg')

            elif msg == b'mobile_id':
                self.WAIT_ADULT()
                self.playWav('wait_mobileid')
                self.rd.delete('msg')

            elif msg == b'001':
                self.FAIL_PAGE()
                self.playWav('device_fail') 
                self.rd.delete("msg")

            elif msg == b'device_err':
                self.DEVICE_ERR_PAGE()
                self.rd.delete("msg")
                
            elif msg == b'sign':
                self.SIGN_PAGE()
                self.playWav('adult_agree')
                self.rd.delete('msg')

            elif msg == b'card':
                self.CARD_PAGE()
                self.playWav('card')
                self.rd.delete("msg")

            elif msg == b'remove':
                self.REMOVE_PAGE()
                self.playWav('remove')
                self.rd.delete("msg")

            elif msg == b'hh_deny':
                self.HH_DENY()
                self.playWav('hh_deny')
                self.rd.delete("msg")
                
            elif msg == b'sspay_deny':
                self.SSPAY_DENY()
                self.playWav('sspay_deny')
                self.rd.delete("msg")

            elif msg == b'auth_fail':
                self.AUTH_FAIL()
                self.playWav('auth_fail')
                self.rd.delete("msg")

            elif msg == b'003':
                self.PAYMENT_FAIL_PAGE()
                self.playWav('payment_fail')
                self.rd.delete("msg")

            elif msg == b'no_money':
                self.NO_MONEY()
                self.playWav('no_money')
                self.rd.delete("msg")

            elif msg == b'shopping':
                self.SHOPPING_PAGE()
                self.playWav('shopping')
                self.rd.delete("msg")

            elif msg == b'admin':
                self.ADMIN_PAGE()
                self.playWav('admin')
                self.rd.delete("msg")

            elif msg == b'admin_close':
                self.START_PAGE()
                self.playWav('admin_close')
                self.rd.delete('msg')
            
            elif msg == b'infer':
                self.INF_PAGE()
                self.playWav('infer')
                self.rd.delete('msg')

            elif msg == b'end':
                self.END()
                self.playWav('end')
                self.rd.delete('msg')

            elif msg == b'end_none':
                self.END_NONE()
                self.playWav('end_none')
                self.rd.delete('msg')

        except Exception as ex:        
            pass
        self.root.after(1000,self.readRedis)       
        
    #음성 안내
    def playWav(self, audio_file):
        playsound(self.cf_path+'voice/'+audio_file + ".mp3", False)
        
    #위젯 초기화
    def clearAllWidgets(self):
        if self.rd.get('box') == b'o':
            self.orderAmtLabel.place_forget()
            self.orderFrame.place_forget()
            self.orderBar.pack_forget()
            self.orderBox.pack_forget()
            self.rd.delete('ol')
            self.rd.set('box','c')
        elif self.rd.get('sign') == b'o':
            self.drawingArea.place_forget()
            self.rd.set('sign','c')
