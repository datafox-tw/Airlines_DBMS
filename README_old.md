# Fly to Past
以下使用VS Code進行示範。

## 1. 安裝資料庫備份檔
在PostgreSQL安裝根目錄底下的airline_big5.sql或是airline_utf8.sql，請注意若PostgreSQL的版本過舊，可能會出現安裝失敗的情形。

## 2. 修改.env
打開根目錄底下的.env並填寫連線到資料庫的相關資訊，若相關設定有所不同，請依照註解中的格式進行修改。

![image](https://hackmd.io/_uploads/ByArYMR8p.png)

## 3. 進入虛擬環境並安裝所需套件

1. 開啟終端機，並移動路徑到專案根目錄
2. 輸入以下指令進入虛擬環境
```
db_env\Scripts\activate
```
3. 輸入以下指令安裝所需套件
```
pip install -r requirements.txt
```
4. 輸入以下指令啟動flask
```
flask run
```

備註：如果照這些步驟進行後仍無法成功執行第4步的指令，可以考慮省略步驟2，直接使用執行端環境進行步驟3和4。
===
2026 更新
我打算重新構築這份我在２０２３年初學database management的破破code變成可以上github demo的code, 當時主要是在sql邏輯、正規化、er diagram設計上花費力氣但是實際前端操作系統就是爛 我打算先想辦法做到以下事情
1. 在我的電腦裡面跑得起來（我有裝postgres)
2. 把這個破版本上傳到github上然後標記這是最一開始的版本
3. 設定新分支，開始修正前端、增加一些功能（簡單的flask框架就好）
4. 讓看我這個repo的人可以知道怎麼互動 以及應該抱持怎麼樣心情看待他