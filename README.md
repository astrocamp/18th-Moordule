# Moordule 多揪

![moordule](<https://miro.medium.com/v2/resize:fit:1400/format:webp/1*M9eXElapdctvl-nQbPG38w.jpeg> =300x300)
![moordule-text](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*sphjBoiQpYV1I4Z5hOl5Qw.jpeg)

### 揪朋友 來多揪 越揪越多好朋友

![Moordule-QRcode] (https://miro.medium.com/v2/resize:fit:1400/format:webp/1*eUziMkHk2T129_qoLBXSFQ.png)

掃描 QR Code，輕鬆加入聚會，開啟人生新篇章

專案網址 : https://moordule.com  
 

### 關於多揪

---

Moordule 多揪 是一個以**聚會**為出發點的交友平台，讓使用者更容易接觸到與自己興趣相近的朋友圈。


用戶可以：
- 參與有興趣的聚會，在線下與同好者見面交流
- 創建聚會，舉辦自己的興趣的聚會，找同好者  


## 功能說明
### 會員功能：

- 參與聚會
- 創建聚會
- 儲值

### 聚會功能：
- 六大聚會種類，輕鬆找到志同道合的朋友


### 金流功能：
- 使用Line Pay 簡單加值 



## 環境設定

### 安裝環境

git clone https://github.com/astrocamp/18th-Moordule.git(將專案複製到本地)  
cd 18th-Moordule(進入專案目錄)

- poetry 輸出 requirements.txt:
  `poetry export -f requirements.txt --output requirements.txt`
- 安裝所有套件: `poetry install`
- 安裝裝 npm:`npm i`

### 執行環境

- 開啟開發伺服器: `poetry run python manage.py runserver`
- 啟動 CSS & JS 打包: `npm run dev`
- 產生資料庫: `poetry run python manage.py makemigrations`
- 運行資料庫遷移: `poetry run python manage.py migrate`
- 建立聚會類別: `poetry run python manage.py seed_categories`

## 技術使用

前端：`HTML`,`CSS`,`Tailwind CSS`,`JavaScript`,`HTMX`,`Alpine.js`
後端：`Python`,`Django`
資料庫：`PostgreSQL`, [TablePlus](https://tableplus.com/)
版本控制：`Git`, `GitHub`
第三方登入：`Google`
金流：`Line Pay`
圖片上傳：`AWS S3` 
部署：`Zeabur`
排版設計:`Design.com`, `Illustrator`, `Canva`
專案規劃：`Miro`, `Asana`


## 團隊成員

🌟 鄧鈺馨 Cindy [GitHub](https://github.com/YuHsinTengCindy)  
- 頁面切版
- 聚會系統
- 創建聚會

柳澤豐 RichardT [GitHub](https://github.com/richart-coder)  
- 環境設定
- 資料庫
- 會員系統

🎀 雷衍辰 Joanna [GitHub](https://github.com/JoannaLei21) 
- 設計頁面
- 金流串接
- Google 地圖串接

🌟 張家瑞 Gary [GitHub](https://github.com/Gary0306)  
- 搜尋功能
- Google 日曆串接

🌎 陳思妤 Emma [GitHub](https://github.com/Emma-EC)  
- 頁面切版
- Google 第三方登入

王廷安 [GitHub](https://github.com/Tingan111)  
- 圖片上傳
- 通知視窗
