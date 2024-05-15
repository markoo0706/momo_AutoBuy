## 說明
- 利用 Python Selenium 套件進行自動化刷新＆購買商品。
## 使用工具
* Python
* Selenium
* Chrome browser
## 使用方法
- 安裝 virtualenv，指令：pip install virtualenv
- 創建虛擬環境，指令：virtualenv .venv(可以自己決定虛擬環境名稱，.venv為建議預設值)
- 啟動虛擬環境，指令：source .venv/bin/activate
- 安裝套件，指令：pip install -r requirements.txt
- 到 settings.py 裡面填入相關資料。
- 執行 create_json.ipynb，右上角可選擇執行環境，先選python，在選.venv（都選最上面的！），有什麼要安裝的就都按「是」。
- 按照 create_json.ipynb的步驟進行，並生成 momo.json 的 cookies。
- 執行主要程式：python main.py。
- 真的要執行購買動作時，就取消註解 main.py 的第62行：# order_save_button.click()  ### 真的要買才解除註解！，若僅為測試的的話就保持註解即可，否則會直接下單購買，導致需要手動退貨。
  