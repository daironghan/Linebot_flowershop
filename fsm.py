from transitions.extensions import GraphMachine

from utils import send_text_message, send_image_message

from bs4 import BeautifulSoup
import requests
import pandas as pd

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_houseplant(self, event):
        text = event.message.text
        return text == "盆栽推薦"
    
    def on_enter_houseplant(self, event):
        send_text_message(event.reply_token, '請問你有養過植物嗎？輸入"是"或"否"')

    def is_going_to_hpReccomend(self, event):
        text = event.message.text
        return text == "否" or text == "是" 

    def on_enter_hpReccomend(self, event):
        text = event.message.text
        if text == "是":
            send_text_message(event.reply_token, '推薦給你 虎尾蘭 \n有著「空氣清淨機」的稱號 而且很好照顧大約兩三周澆一次水即可 新手也能上手呦~')
        else:
            send_text_message(event.reply_token, '推薦給你 虎尾蘭 \n有著「空氣清淨機」的稱號 而且很好照顧大約兩三周澆一次水即可 新手也能上手呦~\n輸入"圖片"可查看它的圖片')
            #send_image_message(event.reply_token, "https://images.unsplash.com/photo-1599009944997-3544a939813c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NXx8c25ha2UlMjBwbGFudHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60")
        self.go_back()
    
    def is_going_to_hpImage(self, event):
        text = event.message.text
        return text == "圖片" 

    def on_enter_hpImage(self, event):
        send_image_message(event.reply_token, "https://images.unsplash.com/photo-1599009944997-3544a939813c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NXx8c25ha2UlMjBwbGFudHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60")
        self.go_back()

    def is_going_to_lan(self, event):
        text = event.message.text
        return text == "花語" 

    def on_enter_lan(self, event):
        send_text_message(event.reply_token, '請輸入花的名稱')
    
    def is_going_to_lanSearch(self, event):
        return True

    def on_enter_lanSearch(self, event):
        # web crawling
        url = 'https://silviayellow.pixnet.net/blog/post/354111760-%E8%8A%B1%E8%AA%9E%E5%A4%A7%E5%85%A8%EF%BD%9C%E8%8A%B1%E8%AA%9E%E7%A5%9D%E7%A6%8F%EF%BD%9C%E7%89%B9%E5%88%A5%E7%9A%84%E8%8A%B1%E8%AA%9E%EF%BD%9C533%E7%A8%AE%E8%8A%B1%E7%9A%84'
        re = requests.get(url)
        re.encoding = 'utf-8'
        soup = BeautifulSoup(re.text, 'lxml')
        flowers = []
        lans = []
        t = soup.find('table').tbody.find_all('tr')
        for i in t:
            flowers.append(i.find_all('td')[1].text)
            lans.append(i.find_all('td')[3].text)
        dic = {"Flowers":flowers, "Language": lans}
        df = pd.DataFrame(dic)
        found = False #flag
        s = event.message.text
        for i in range(len(df.index)):
            if df.Flowers[i] == s or df.Flowers[i] == s[:-1] or df.Flowers[i] == s+"花":
                found = True
                send_text_message(event.reply_token, df.Language[i])
        if not found:
            send_text_message(event.reply_token, "抱歉查無資料:(")
        self.go_back()