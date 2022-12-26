Running the linebot
```
pipenv shell
ngrok http 8000
python3 app.py
```


## 介紹
GreenFingers 是一個有趣的植物小教室 
希望可以把植物的樂趣分享給大家～

## 主要功能
1. 台灣植物名錄：查詢現有的台灣植物物種
    - 連結 社團法人中華民國自然生態保育協會-臺灣物種名錄 TaiCoL API version 1.1
    - 提供普通查詢以及進階查詢兩種方式
2. 小學堂：透過答題方式測試自己對植物的了解
    - 隨機挑選題目給使用者
3. 室內盆栽推薦：根據使用者的回答來推薦適合的室內盆栽
    - 使用Line Messaging Api中的Imagemap Message傳送圖片按鈕
4. 花語查詢：查詢花語背後的
    - 使用網路爬蟲爬取部落客資料
## FSM
![](https://github.com/daironghan/Linebot_GreenFingers/blob/main/img/fsm.jpg?raw=true)

## 示範
首先，輸入任何訊息之後會進入首頁，可以在這裡點選想要的功能

![](https://github.com/daironghan/Linebot_GreenFingers/blob/main/img/menu_sci.jpg?raw=true)
![](https://github.com/daironghan/Linebot_GreenFingers/blob/main/img/menu_test.jpg?raw=true)
![](https://github.com/daironghan/Linebot_GreenFingers/blob/main/img/menu_hp.jpg?raw=true)
![](https://github.com/daironghan/Linebot_GreenFingers/blob/main/img/menu_lan.jpg?raw=true)

### 台灣植物名錄：查詢現有的台灣植物物種
    - 使用者可依據指示進行「一般查詢」
    - 亦可對「一般查詢」物種進行「進階查詢」
    - 可重新「一般查詢」或「進階查詢」
![](https://github.com/daironghan/Linebot_GreenFingers/blob/main/img/ex_sci.jpg?raw=true)

### 小學堂：透過答題方式測試自己對植物的了解
    - 隨機挑選題目給使用者 最多答3題
    - 答錯一題就結束測驗
    - 可重新進行測驗
![](https://github.com/daironghan/Linebot_GreenFingers/blob/main/img/ex_test.jpg?raw=true)

### 室內盆栽推薦：根據使用者的回答來推薦適合的室內盆栽   
    - 首先會對使用者進行簡單的訪問
    - 會依據使用者的回覆推薦對應的盆栽
    - 點選圖片即可獲得更詳細的介紹
![](https://github.com/daironghan/Linebot_GreenFingers/blob/main/img/ex_hp.jpg?raw=true)

### 花語查詢：查詢花語背後的
    - 首先會對使用者進行簡單的訪問
    - 會依據使用者的回覆推薦對應的盆栽
    - 可重復查詢
![](https://github.com/daironghan/Linebot_GreenFingers/blob/main/img/ex_lan.jpg?raw=true)

### FSM
輸入fsm可隨時查看FSM圖即目前的state
![](https://github.com/daironghan/Linebot_GreenFingers/blob/main/img/ex_fsm.jpg?raw=true)

### 輸入錯誤
若使用者輸入錯誤將顯示如下
![](https://github.com/daironghan/Linebot_GreenFingers/blob/main/img/ex_error.jpg?raw=true)

## 來加入好友吧！
![](https://github.com/daironghan/Linebot_GreenFingers/blob/main/img/qrcode.png?raw=true)

## Resources
臺灣物種名錄 TaiCoL API: https://taibnet.sinica.edu.tw/chi/taicol_api.php

花語： https://silviayellow.pixnet.net/blog
