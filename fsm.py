from transitions.extensions import GraphMachine

from utils import send_text_message, send_image_message, send_imagemap

from bs4 import BeautifulSoup
import requests
import pandas as pd


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    
    # 盆栽推薦
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
            send_imagemap(event.reply_token, "https://github.com/daironghan/Linebot_flowershop/blob/main/img/hpAdvanced.jpg?raw=true"
            , "馬拉巴栗","長壽花","七里香","天堂鳥")
        else:
            send_imagemap(event.reply_token, "https://github.com/daironghan/Linebot_flowershop/blob/main/img/hpNewbie.jpg?raw=true"
            , "龜背芋","白牡丹","圓葉椒草","虎尾蘭")
        self.go_back()
    
    def is_going_to_hpNewbie(self, event):
        text = event.message.text
        return text == "龜背芋" or text == "白牡丹" or text == "圓葉椒草" or text == "虎尾蘭"
    
    def on_enter_hpNewbie(self, event):
        text = event.message.text
        if text == "龜背芋":
            send_text_message(event.reply_token, "\U0001F331龜背芋 又稱龜背竹\n葉子的形狀很特別 能營造出熱帶雨林的氣息~ 最近在許多室內擺設都能看到他的蹤跡呦")
        elif text == "白牡丹":
            send_text_message(event.reply_token, "\U0001F331白牡丹\n屬於近期很夯的多肉植物 如玫瑰的外型非常漂亮 適合養在乾燥通風的環境")
        elif text == "圓葉椒草":
            send_text_message(event.reply_token, "\U0001F331圓葉椒草\n外型可愛 圓圓的葉子像硬幣 因此又稱圓葉發財樹 是新手的選擇之一喔")
        elif text == "虎尾蘭":
            send_text_message(event.reply_token, "\U0001F331虎尾蘭\n有著「空氣清淨機」的稱號 很好照顧大約兩三周澆一次水即可 新手也能上手呦~")
        self.go_back()
    
    def is_going_to_hpAdvanced(self, event):
        text = event.message.text
        return text == "馬拉巴栗" or text == "長壽花" or text == "七里香" or text == "天堂鳥"
    
    def on_enter_hpAdvanced(self, event):
        text = event.message.text
        if text == "馬拉巴栗":
            send_text_message(event.reply_token, "\U0001F331馬拉巴栗 又稱發財樹\n原生於中美墨西哥 常見於辦公室 也適合送禮呦")
        elif text == "長壽花":
            send_text_message(event.reply_token, "\U0001F331長壽花\n開花時顏色鮮艷 可為空間帶來許多色彩 因名字吉祥許多人也拿來送禮喔")
        elif text == "七里香":
            send_text_message(event.reply_token, "\U0001F331七里香 原名月橘\n屬於比較有挑戰的植物 但其自然的香氣可比人工的香分厲害呦")
        elif text == "天堂鳥":
            send_text_message(event.reply_token, "\U0001F331天堂鳥\n堪稱室內植物界的女王 屬於室內大型植物而且生長非常快速 適合室內空間較大者種植")
        self.go_back()

    # 花語
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
        found = False # flag
        s = event.message.text
        for i in range(len(df.index)):
            if df.Flowers[i] == s or df.Flowers[i] == s[:-1] or df.Flowers[i] == s+"花":
                found = True
                send_text_message(event.reply_token, df.Language[i])
        if not found:
            send_text_message(event.reply_token, "抱歉查無資料:(")
        self.go_back()