# 計算機演算法期末Project - 旅遊規劃王

## 簡訊

- 最詳細的專案報告，在[此PDF報告檔](/期末報告_旅遊規劃王.pdf)

- 組員名單有:
  - 106362501 簡浩庭
  - 106362505 何宗龍
  - 106362512 王志嘉

- 專案網站連結(已掛，請clone本專案並自行build):
<https://static-welder-265301.an.r.appspot.com/>

- 應用程式建立影片:
<https://www.youtube.com/watch?v=WIAq-PkkLdc>

- 操作說明影片:
<https://www.youtube.com/watch?v=e6bXcmSvU3o>

- 備註:

  1. 附件為.env檔 ，這個 .env 檔案是我們應用程式所使用到的機敏資料，它包含了google map api 與 mongodb connectiobn string 以及 map box api key等等，這個檔案得放在專案資料夾下的根目錄，得跟Dockerfile放在同一層資料下在執行 docker-compose -f "docker-compose.yml" up -d --build 時， docker-compose.yml 會引入 .env 的環境變數以讓後端的程式使用，若沒有這個 .env 檔案，程式執行起來就會出錯(找不到MongoDB連結與Google Map 要使用的API Key)
  2. 網站若送出時出現500 ServerError 的訊息是因為 Google API 回傳了不符預期的資料 (Google map 找不到該地點的交通資訊導致)，請回第一頁並選擇其他景點。

## 動機與目的

1. 行程路線障礙者良藥。出遊玩時總是會計劃著許多地區的景點，但總是難以規劃出較適合之路徑，造成通勤時間與成本的增加。
2. 為了避免花過多的時間與成本在交通上，程式取得多個景點位置後將規劃出一條通車時間最短之路徑。
3. 規劃好景點後，天氣總是不盡人意。如:下雨天造成原本計畫泡湯、空氣不佳導致吸入過多髒空氣、熱指數過高容易造成中暑...等，所以需要一個平台整合自訂的景點即時資訊
4. 為了讓使用者能更快更方便的獲得天氣或空氣品質等資訊，減少反覆查詢到各個資訊平台查詢之困擾，且程式會藉由這些資訊判斷是否適合前往。
5. 經由程式規劃與推薦後，就能達到節省交通時間與降低敗興而歸的情況，藉此提升使用者旅遊品質與家庭和諧。這個服務對於有一堆想去的地方，卻不知如何安排行車流而焦頭爛耳，也為您的家庭和諧提供的優良服務阿!!

## 預計完成功能

1. 主要頁面分為兩頁：

- 景點選擇：
  - 使用者可任選多個景點(10個以內)，並設定出發地，此頁面中主要區分為兩個區塊：
    - 提供全台灣景點列表與基本介紹或相關資訊等等
    - 顯示已選擇的項目清單
- 行程安排推薦結果：
  - 顯示預計花費總里程
    - 安排順序Tabale與項目資訊
    - Google map 路線標記

2. ~~程式串接資訊開放平台的景點資料至 Mongodb Atlas，並使用 mongoengine SDK 製作 ODM 模型，取得天氣資料後，抓出雨量、空氣品質指標等資訊，顯示於(B)介面上。~~ Done.

3. 介面上顯示出等級時間內是否有雨量累積(毫米)。
4. 判斷空氣品質指標AQI:0~50顯示良好，51~100顯示普通，100以上顯示不健康。
5. 熱指數：藉由溫度與濕度，判斷環境舒適程度。
6. 除了顯示天氣狀況外，程式會推薦使用者一條最短路徑(環)，讓使用者節省交通上的時間與成本。

## 使用語言、平台、開發環境

- 前端應用組件與模板框架
  - HTML
  - CSS
  - JavaScript
  - jQuery
  - Datatable
  - Bootstrap
- 後端處理之程式語言
  - Python
- 後端框架與模板引擎
  - Flask
  - Jinja2
- 資料庫與其ODM框架
  - Mongodb Atlas
  - Mongoengine
- 主要使用模組與SDK及API
  - google-maps-services-python
  - Google Maps Directions API
  - Google Maps Distance Matrix API
  - Google Maps JavaScript API
- 部屬平台
  - Google Cloud Platform App Engine
- 開發環境
  - Windows WSL2 Ubuntu 18.04
  - Docker Engine 19.03.12
  - Kubernetes 1.18.3
- API來源:
  - 民生公務物聯網 API
  - 民生公務物聯網-中央氣象局-雨量站 API
  - 民生公務物聯網-環保署-國家空品測站監測資料 API
  - 景點 - 觀光資訊資料庫 API

## 使用資料結構與演算法分析

1. 使用資料結構:

- Hash Table: Python 內建型態 Dictionary 他能幫我們以鍵對值來儲存我們的資料，以及使用nested的方式儲存稍微複雜的資料。
- Queue: 我們有 Python 中使用 threading 模組，以使用多個子執行緒去訪問來源資料(API)並存儲到 Mongodb 做紀錄與存入 Queue 中(因在做多個子執行緒時無法直接return 資料，且稍後前端會需要這些值的資訊) ，這樣才能照每個 job 完成的順序並將其取出，最後再回送至前端。

2. 使用演算法:

- TSP: [程式碼位置](/backend/resource/RoutePlanning/TravelGraph.py)

  | 比較項目 | Brute | Force backtracking | 2-opt |
  | :-----: | :---: | :---------------: | :----: |
  | 優點 | 一定可以找到最佳解 | 優化版的暴力法，透過遞迴尋找邊界以壓縮暴力法枚舉的所有可能| 效率高，速度快
  | 缺點 | 需用較多硬體資源，要探討的情況有多種 | 不好找到能修改 backtracking 的切入點</br>該方法效率還是比較低 | 只有局部最佳化是一種隨機性算法，結果可能會不同。

- Search:

  在前端的部分，在第二個顯示Result頁面的時候，因為後端傳回的資料並不是根據我傳入的順序做回傳，所以前端必須根據回傳的項目給定index，再經由Datatable排序此欄位。這邊直接利用Javascript Array內建的indexOf函式取得排好序Array的index，設給列的欄位值，針對 String.prototype.indexOf() 做源碼的探討發現他有定義了

  1. LinearSearch
  2. BoyerMooreSearch
  3. BoyerMooreHorspoolSearch
  4. SingleCharSearch
  5. InitialSearch
  
  內建會根據傳入的初始data做搜尋演算法的選擇，我們也能理解這種概念的作法，因為再老師的課程中，經由引導性和思考讓我們理解到「沒有最好的演算法，只有最適合的演算法」。

## GOOGLE_PLACES_API_KEY 所需求的 Google API 權限

- [Google API 申請連結](https://console.developers.google.com/?hl=zh-tw)
  - Distance Matrix API
  - Directions API
  - Maps JavaScript API

## 應用程式環境變數設定

請依照 sample.env 將正確的環境變數代上即可。

其餘服務請自行 google 生出乃

```bash
GOOGLE_PLACES_API_KEY=
MONGODB_CONNECTIONSTRING=
MONGODB_DB=
MONGODB_HOST=
MAPBOX_API_KEY=
```
