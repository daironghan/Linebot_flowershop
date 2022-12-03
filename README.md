/home/os2022/HW/TOC-Project-2020-master

start virtual environment
```
pipenv shell
```
ngrok http 8000

## 介紹
GreenFingers 是一個有趣的植物小教室 
希望可以把植物的樂趣分享給大家～

## 功能
1. 台灣植物名錄：查詢現有的台灣植物物種
    - 連結 社團法人中華民國自然生態保育協會-臺灣物種名錄 TaiCoL API version 1.1
    - 提供普通查詢以及進階查詢兩種方式
2. 小學堂：透過答題方式測試自己對植物的了解
    - 隨機挑選題目給使用者 最多答3題
    - 答錯一題就結束測驗
3. 室內盆栽推薦：根據使用者的回答來推薦適合的室內盆栽
    - 使用Line Messaging Api中的Imagemap Message傳送圖片按鈕
4. 花語查詢：查詢花語背後的
    - 使用網路爬蟲爬取部落客資料

https://developers.line.biz/en/docs/messaging-api/message-types/#text-messages

花語資料來源：https://silviayellow.pixnet.net/blog/post/354111760-%E8%8A%B1%E8%AA%9E%E5%A4%A7%E5%85%A8%EF%BD%9C%E8%8A%B1%E8%AA%9E%E7%A5%9D%E7%A6%8F%EF%BD%9C%E7%89%B9%E5%88%A5%E7%9A%84%E8%8A%B1%E8%AA%9E%EF%BD%9C533%E7%A8%AE%E8%8A%B1%E7%9A%84

### Resources
https://marketingliveincode.com/?p=4442
https://exam.naer.edu.tw/base/otc/testStoreFile/10016635a8cca09390e9.pdf
http://www.whjhs.tyc.edu.tw/wp-content/uploads/doc/wh211/108%E8%A3%9C%E8%80%838%E5%B9%B4%E7%B4%9A%E7%94%9F%E7%89%A9%E8%A9%A6%E9%A1%8C%E9%A1%8C%E5%BA%AB%E5%8F%8A%E8%A7%A3%E7%AD%94.pdf
http://eweb.tmps.tp.edu.tw/nano-new/doucment/1-2-1%E8%8E%96%E7%9A%84%E5%BD%A2%E8%83%BD%E6%85%8B%E8%88%87%E7%B0%A1%E5%96%AE%E5%88%86%E9%A1%9E-%E8%A9%A6%E9%A1%8C.pdf