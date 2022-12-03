from transitions.extensions import GraphMachine

from utils import send_text_message, send_image_message, send_imagemap

from bs4 import BeautifulSoup
import requests
import pandas as pd
import random

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    # # menu
    # def on_enter_user(self, event):
    #     send_text_message(event.reply_token,'\U0001F335輸入"臺灣植物名錄"\n可查尋臺灣的現有的植物物種喔\n\n\U0001F335輸入"冷知識"\n可以學到一個植物的小小冷知識\n\n\U0001F335輸入"室內盆栽推薦"\n看了許多植物的知識後是不是也想種種看呢~\n\n\U0001F335輸入"花語"\n可查詢各種花背後的意含呦')

    # 台灣植物名錄
    def is_going_to_sci(self, event):
        text = event.message.text
        return text == "台灣植物名錄" or text == "臺灣植物名錄"
    
    def on_enter_sci(self, event):
        send_text_message(event.reply_token, '請問要搜尋什麼植物？\n輸入俗稱即可\n\n查詢資料庫請稍等~')

    def is_going_to_sciSearch(self, event):
        return True
    
    def on_enter_sciSearch(self, event):
        text = event.message.text
        response = requests.get(f"http://api.taicol.tw/v1/?common={text}")
        response.encoding = 'utf-8'
        data = response.json()
        msg = "臺灣現有物種:\n"
        found = False
        name = []
        name_code = []
        for i in range(1,len(data),1):
            if data[i]['kingdom_c'] == "植物界":
                found = True
                name_code.append(data[i]['name_code'])
                name.append(data[i]['common_name'])
                s = f"\U0001F33F{data[i]['common_name']}\n"
                msg = msg + s
        msg = msg + '\n\U0001F338輸入"搜尋植物" 搜尋別的植物\n\n\U0001F338輸入"進階查詢" 進階查詢某個物種\n\n\U0001F338輸入"返回" 返回主選單'
        global nameCode
        nameCode = pd.DataFrame.from_dict({'name':name, 'name_code':name_code})
        if found:
            send_text_message(event.reply_token, msg)
        else:
            send_text_message(event.reply_token, '查無資料:(\n還要搜尋別的植物嗎？請輸入"是"或"否"')
    
    def is_going_to_sciSearchAgain(self, event):
        text = event.message.text
        if text == "返回":
            self.go_back()
        return text == "搜尋植物"
    
    def is_going_to_sciAdvanced(self, event):
        text = event.message.text
        return text == "進階查詢"
    
    def on_enter_sciAdvanced(self, event):
        send_text_message(event.reply_token, '請輸入以上列表中要進階查詢的物種')

    def is_going_to_sciAdSearch(self, event):
        for i in range(len(nameCode.index)):
            if nameCode.iat[i,0] == event.message.text:
                global nc
                nc = nameCode.iat[i,1]
                print(nc, event.message.text)
                return True
        return False

    def on_enter_sciAdSearch(self, event):
        response = requests.get(f"http://api.taicol.tw/v1/?namecode={nc}")
        response.encoding = 'utf-8'
        data = response.json()
        msg = f"\U0001F33F學名:{data[1]['name']}\n俗名:{data[1]['common_name']}\n門:{data[1]['phylum_c']}\n綱:{data[1]['class_c']}\n目:{data[1]['order_c']}\n科:{data[1]['family_c']}\n屬:{data[1]['genus_c']}"
        msg = msg + '\n\n\U0001F338輸入"搜尋植物" 搜尋別的植物\n\n\U0001F338輸入"進階查詢" 重新進階查詢某個物種\n\n\U0001F338輸入"返回" 返回主選單'
        send_text_message(event.reply_token, msg)

    def is_going_to_sciAdSearchAgain(self, event):
        text = event.message.text
        return text == "進階查詢"

    # 小學堂
    def is_going_to_test(self, event):
        text = event.message.text
        return text == "小學堂"

    def on_enter_test(self, event):
        send_text_message(event.reply_token, '準備好開始測驗了嗎？\n\n\U0001F338輸入"開始" 開始答題\n\U0001F338輸入"返回" 返回主選單')
    
    def is_going_to_q1(self, event):
        text = event.message.text
        if text == "返回":
            self.go_back()
        return text == "開始"
    
    def on_enter_q1(self, event):
        r = random.randint(0,2)
        msg = ""
        global qcnt 
        qcnt = 0
        global ans
        global q
        if r==0:
            q = "「樹幹」是指大樹的哪個部位呢？\n(A) 根 (B) 莖 (C) 葉 (D)花"
            ans = "b"
        elif r==1:
            q = "植物體內輸送水分的路線是？\n(A) 莖→根→葉 (B) 莖→葉→根 (C) 葉→根→莖 (D) 根→莖→葉"
            ans = "d"
        elif r==2:
            q = "下述何者植物非裸子植物?\n(A) 銀杏 (B)蘇鐵 (C)紅檜 (D)桑樹"
            ans = "b"
        msg = q + '\n\n\U0001F338請輸入英文字母回答'
        send_text_message(event.reply_token, msg)

    def is_going_to_q2(self, event):
        text = event.message.text.lower()
        return text == ans

    def on_enter_q2(self, event):
        r = random.randint(0,2)
        global qcnt 
        qcnt = 1
        global ans
        global q
        global sol
        msg = ""
        if r==0:
            q = "下列哪一組植物具有肥大的根，可儲存大量的養分？\n(A) 石蓮、地瓜 (B) 胡蘿蔔、白蘿蔔 (C) 馬鈴薯、芋頭 (D) 仙人掌、馬鈴薯"
            ans = "b"
        elif r==1:
            q = "胚珠受粉後，會在什麼構造內形成「種子」？\n(A) 子宮 (B) 柱頭 (C) 花柱 (D) 子房"
            ans = "d"
        elif r==2:
            q = "「木本莖」的敘述，下列哪一項是錯誤的？\n((A) 枝幹容易形成樹蔭，提供人們乘涼 (B) 一個人的手臂有時無法完整環抱樹幹 (C) 莖通常粗壯，不容易推動 (D) 通常在莖的表面會長出細毛"
            ans = "d"
        msg = q + '\n\n\U0001F338請輸入英文字母回答'
        send_text_message(event.reply_token, msg)
    
    def is_going_to_q3(self, event):
        text = event.message.text.lower()
        return text == ans

    def on_enter_q3(self, event):
        r = random.randint(0,2)
        msg = ""
        global qcnt 
        qcnt = 2
        global ans
        global q
        global sol
        if r==0:
            q = "下列哪一種植物的是草本莖？\n(A) 牽牛花 (B) 臺灣欒樹 (C) 七里香 (D) 松樹。"
            ans = "a"
        elif r==1:
            q = "下列關於植物光週期調控的敘述，何者正確？\n(A) 光週期日照時間短於臨界日照時間時才開花的植物為短日照植物(B) 所有植物開花與否皆受光週期的影響 (C) 日照期對植物開花的影響比連續黑暗期更重要 (D) 短日照植物在光週期中受紅光（R）短暫處理，不會影響其開花"
            ans = 'a'
        elif r==2:
            q = "「草本莖」植物的敘述，哪一項是正確的？\n(A)芋頭的莖屬於鱗莖 (B) 馬鈴薯的莖屬於球莖 (C) 蛇莓的走莖可以用來繁殖 (D) 絲瓜捲鬚莖是為了美觀而生長的"
            ans = "c"
        msg = q + '\n\n\U0001F338請輸入英文字母回答'
        send_text_message(event.reply_token, msg)

    def is_going_to_testResult(self, event):
        text = event.message.text.lower()
        return (text != ans or qcnt==2) and (text == 'a' or text == 'b' or text == 'c' or text == 'd')

    def on_enter_testResult(self, event):
        msg = ""
        if event.message.text.lower() == ans:
            msg = "\U0001F3C6植物小達人\n答對題數: 3\n好厲害全部都答對囉~"
        elif qcnt == 2:
            msg = f"錯了！正確答案為：{ans.upper()}\n"
            msg = msg + "\n\U0001F44D答對題數: 2\n差一點就全對囉~"
        elif qcnt == 1:
            msg = f"錯了！正確答案為：{ans.upper()}\n"
            msg = msg + "\n\U0001F44D答對題數: 1\n有進步的空間！"
        elif qcnt == 0:
            msg = f"錯了！正確答案為：{ans.upper()}\n"
            msg =  msg +"\n\U0001F342答對題數: 0\n看來要多補充一點植物的知識囉~"
        msg = msg + '\n\n\U0001F338輸入"重新開始" 重新開始測驗\n\U0001F338輸入"返回" 返回主選單'
        send_text_message(event.reply_token, msg)
    
    def is_going_to_testAgain(self, event):
        text = event.message.text
        if text == "返回":
            self.go_back()
        return text == "重新開始"

    # 盆栽推薦
    def is_going_to_houseplant(self, event):
        text = event.message.text
        return text == "盆栽推薦"
    
    def on_enter_houseplant(self, event):
        send_text_message(event.reply_token, '請問有養過植物嗎？輸入"是"或"否"')

    def is_going_to_hpPet(self, event):
        text = event.message.text
        global newbie
        if text == "否":
            newbie = True
        elif text == "是":
            newbie = False
        return text == "否" or text == "是" 
    
    def on_enter_hpPet(self, event):
        send_text_message(event.reply_token, '請問預計種植盆栽的空間有養寵物嗎？\n輸入"是"或"否"')

    def is_going_to_hpReccomend(self, event):
        text = event.message.text
        return text == "否" or text == "是" 

    def on_enter_hpReccomend(self, event):
        text = event.message.text
        print(newbie)
        if text == "是": # 有寵物
            if newbie == True:
                send_imagemap(event.reply_token, "https://github.com/daironghan/Linebot_GreenFingers/blob/main/img/hp_new_pet.jpg?raw=true"
                , "空氣鳳梨","白牡丹","圓葉椒草","西瓜皮椒草")
            else:
                send_imagemap(event.reply_token, "https://github.com/daironghan/Linebot_GreenFingers/blob/main/img/hp_a_pet.jpg?raw=true"
                , "青蘋果竹芋","吊蘭","非洲菫","袖珍椰子")
        else: # 沒寵物
            if newbie == True:
                send_imagemap(event.reply_token, "https://github.com/daironghan/Linebot_GreenFingers/blob/main/img/hp_new_nopet.jpg?raw=true"
                , "龜背芋","白牡丹","圓葉椒草","虎尾蘭")
            else:
                send_imagemap(event.reply_token, "https://github.com/daironghan/Linebot_GreenFingers/blob/main/img/hp_a_nopet.jpg?raw=true"
                , "馬拉巴栗","長壽花","七里香" ,"天堂鳥")
    
    def is_going_to_hpInfo(self, event):
        text = event.message.text
        if text == "返回":
            self.go_back()
        plants = ["空氣鳳梨","白牡丹","圓葉椒草","西瓜皮椒草", "龜背芋","虎尾蘭", "青蘋果竹芋","吊蘭","非洲菫","袖珍椰子", "天堂鳥", "七里香", "長壽花", "馬拉巴栗"] #14
        for p in plants:
            if text == p:
                return True
        return False
    
    def on_enter_hpInfo(self, event):
        text = event.message.text
        msg = ""
        if text == "龜背芋":
            msg = "\U0001F331龜背芋 又稱龜背竹\n葉子的形狀很特別，能營造出熱帶雨林的氣息~ 最近在許多室內擺設都能看到他的蹤跡呦"
        elif text == "白牡丹":
            msg = "\U0001F331白牡丹\n屬於近期很夯的多肉植物，如玫瑰的外型非常漂亮，適合養在乾燥通風的環境"
        elif text == "圓葉椒草":
            msg = "\U0001F331圓葉椒草\n外型可愛，圓圓的葉子像硬幣，因此又稱「圓葉發財樹」，是新手的選擇之一喔"
        elif text == "虎尾蘭":
            msg = "\U0001F331虎尾蘭\n有著「空氣清淨機」的稱號，很好照顧大約兩三周澆一次水即可，新手也能上手呦~"
        elif text == "馬拉巴栗":
            msg = "\U0001F331馬拉巴栗 又稱發財樹\n原生於中美墨西哥，常見於辦公室，也適合送禮呦"
        elif text == "長壽花":
            msg = "\U0001F331長壽花\n開花時顏色鮮艷，可為空間帶來許多色彩，因名字吉祥許多人也拿來送禮喔"
        elif text == "七里香":
            msg = "\U0001F331七里香 原名月橘\n屬於比較有挑戰的植物，但其自然的香氣可比人工的香分厲害呦"
        elif text == "天堂鳥": 
            msg = "\U0001F331天堂鳥\n堪稱室內植物界的女王，屬於室內大型植物而且生長非常快速，適合室內空間較大者種植"
        elif text == "青蘋果竹芋":
            msg = "\U0001F331青蘋果竹芋\n原生於陰涼的森林因此對光教敏，感容易焦邊，是頗具挑戰性的植物呦"
        elif text == "吊蘭":
            msg = "\U0001F331吊蘭\n常見的居室垂掛植物之一，是良好的室內空氣淨化植物，可吸收甲醛等有毒氣體功能呦"
        elif text == "非洲菫":
            msg = "\U0001F331非洲菫\n花色與花型非常多樣性，是難得室內低光度可開花的植物喔~"
        elif text == "袖珍椰子":
            msg = "\U0001F331袖珍椰子\n為最據代表性的椰子類植物中小型，想要為室內增添一番渡假風的不防試試"
        elif text == "西瓜皮椒草":
            msg = "\U0001F331西瓜皮椒草\n圓的葉子配上條紋非常可愛，注意須須培養於排水透氣性良好的土壤"
        elif text == "空氣鳳梨":
            msg = "\U0001F331空氣鳳梨\n有許多品種，最大特色是能完全生活於空氣之中、不需要土壤，因此也有人稱它為「空氣草」"
        msg = msg + '\n\n\U0001F338點選其他盆栽\n或\n\U0001F338輸入"返回" 返回主選單'
        send_text_message(event.reply_token, msg)

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
                msg = df.Language[i]+ '\n\n\U0001F338輸入"重新搜尋" 重新查詢花語\n\U0001F338輸入"返回" 返回主選單'
                send_text_message(event.reply_token, msg)
        if not found:
            send_text_message(event.reply_token, '抱歉查無資料:(\n\n\U0001F338輸入"重新搜尋" 重新查詢花語\n\U0001F338輸入"返回" 返回主選單')
        

    def is_going_to_lanSearchAgain(self, event):
        text = event.message.text
        if text == "返回":
            self.go_back()
        return text == "重新搜尋"