# 路由設計文件 (Routes Design)

本文件依據 PRD 與 Flowchart 設計，定義「食譜收藏夾」後端 Flask 應用程式所有的 URL 路由配置、針對每個畫面的輸入輸出邏輯，以及所需的對應 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 (Jinja2) | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 / 清單 | GET | `/` 或 `/recipes` | `recipes/index.html` | 呈現包含所有食譜的清單以及過濾欄位 |
| 新增食譜頁面 | GET | `/recipes/new` | `recipes/new.html` | 顯示用以填寫新增資料的空白表單 |
| 建立食譜操作 | POST | `/recipes` | — | 接收表單 Payload 後存檔，成功即轉址 |
| 檢視食譜明細 | GET | `/recipes/<int:id>` | `recipes/detail.html` | 呈現單一食譜的完整圖文與料理步驟 |
| 編輯食譜頁面 | GET | `/recipes/<int:id>/edit` | `recipes/edit.html` | 顯示已帶入預先舊有資料的編輯表單 |
| 更新食譜操作 | POST | `/recipes/<int:id>/update` | — | 接收編輯表單將其覆寫資料庫，完畢後轉址 |
| 刪除食譜操作 | POST | `/recipes/<int:id>/delete` | — | 將該筆食譜予以移除，處理完畢後轉址 |

> **補充**：為了配合純 HTML 表單無法使用 `PUT` 與 `DELETE` 規範的限制，資料更新與刪除的執行動作皆由 `POST` 請求並於結尾輔加明確的動詞（`/update`, `/delete`）來替代。

## 2. 每個路由的詳細說明

### GET `/recipes` (與 `/`)
- **輸入**: Query String 參數如 `?q=鬆餅` (關鍵字搜尋)，或是 `?category=甜點` (切換分類)。皆為非必填。
- **處理邏輯**: 讀取 Query String，呼叫 `Recipe.get_all(search_query, category_filter)`。
- **輸出**: 傳遞 `recipes` 變數並渲染 `recipes/index.html`。
- **錯誤處理**: 例外資料由模板呈現空狀態列表即可。

### GET `/recipes/new`
- **輸入**: 無
- **處理邏輯**: 僅需呼叫渲染 HTML 視圖。
- **輸出**: 渲染至 `recipes/new.html`。

### POST `/recipes`
- **輸入**: 包含在 `request.form` 當中的 `title`, `ingredients`, `instructions`, `category`。
- **處理邏輯**: 驗證必填欄位 (標題不得為空等)。驗證通過後呼叫 `Recipe.create(...)` 方法寫入。
- **輸出**: (302 Redirect) 導回 `/recipes`。
- **錯誤處理**: 若必填資料漏短，利用 `flash()` 附加錯誤訊息，並渲染 `recipes/new.html`、退回過往使用者輸入的暫存值。

### GET `/recipes/<int:id>`
- **輸入**: Route URL 參數 `id`。
- **處理邏輯**: 呼叫 `Recipe.get_by_id(id)` 將單一物件抓取出來。
- **輸出**: 將資料傳遞給 `recipes/detail.html` 渲染。
- **錯誤處理**: 若 `Recipe.get_by_id` 回傳 `None`，引發 `abort(404)` 表示找不到頁面。

### GET `/recipes/<int:id>/edit`
- **輸入**: Route URL 參數 `id`。
- **處理邏輯**: 同樣呼叫 `Recipe.get_by_id(id)` 取出舊有資料來填充表單初始值。
- **輸出**: 將資料載入 `recipes/edit.html` 並渲染給客戶端。
- **錯誤處理**: 若回傳 `None`，則引發 `abort(404)`。

### POST `/recipes/<int:id>/update`
- **輸入**: Route URL 參數 `id` 以及伴隨而來的 `request.form` 修改值。
- **處理邏輯**: 進行欄位驗證，沒問題後呼叫 `Recipe.update(...)` 行為。
- **輸出**: (302 Redirect) 成功後導回 `/recipes/<id>` 重新讓他看見修改後的結果。
- **錯誤處理**: 若因漏項驗證失敗，執行與新增介面相似的模式，帶著錯誤重新渲染 `recipes/edit.html`。

### POST `/recipes/<int:id>/delete`
- **輸入**: Route URL 參數 `id`。
- **處理邏輯**: 直接執行 `Recipe.delete(id)` 等動作來完全丟棄。
- **輸出**: (302 Redirect) 完成後導回 `/recipes` 主列表清單。
- **錯誤處理**: 找不到紀錄或是刪除意外時均安全轉址。

## 3. Jinja2 模板清單

專案所涉及的前端視圖應安排於目錄：`app/templates/`。

- `base.html` (所有頁面的骨幹，預期含有 Navbar、共同樣式設定與 Footer，其餘由各頁透過 `extends 'base.html'` 與 `block content` 接續撰寫)
- `recipes/index.html` (首頁/清單畫⾯)
- `recipes/new.html` (新建畫⾯)
- `recipes/detail.html` (明細畫⾯)
- `recipes/edit.html` (編輯畫⾯)
