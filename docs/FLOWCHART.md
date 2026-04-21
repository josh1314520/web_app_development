# 系統流程與使用者流程圖 (Flowcharts)

本文檔根據專案的需求規格 (PRD) 描述系統的「使用者流程圖」與「系統序列圖」。
> **備註**：由於目前尚未定義詳細的架構文件 (`docs/ARCHITECTURE.md`)，因此系統序列圖中的參與者（Flask, SQLite, HTML/Jinja2）是直接根據 PRD 中所規範的技術堆疊進行假設與設計。

## 1. 使用者流程圖 (User Flow)

描述使用者進入「食譜收藏夾」後，如何在一系列頁面與操作中完成新增、檢視、編輯與刪除等操作。

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 食譜列表]
    B --> C{要執行什麼操作？}
    
    C -->|使用搜尋列 / 點選分類標籤| B
    C -->|點擊「新增食譜」按鈕| D[新增空白食譜表單頁]
    C -->|點擊任一食譜項目| E[檢視專屬食譜明細頁]
    
    D -->|填寫標題食材等並送出| F[新增成功]
    F --> B
    
    E --> G{在明細頁的操作}
    G -->|返回| B
    G -->|點擊「修改」| H[進入編輯表單頁]
    G -->|點擊「刪除」| I[刪除食譜]
    
    H -->|修改內容並送出| J[編輯成功]
    J --> E
    
    I -->|確認刪除| K[刪除成功]
    K --> B
```

## 2. 系統序列圖 (Sequence Diagram)

以 MVP 核心功能「使用者新增食譜」為例，描述前端瀏覽器、後端 Flask Controller 以及 SQLite 資料庫之間的完整資料流與互動步驟。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (HTML/Jinja2)
    participant Flask as 伺服器 (Flask Route/Model)
    participant DB as 資料庫 (SQLite)

    %% 進入新增頁面
    User->>Browser: 點擊首頁「新增食譜」按鈕
    Browser->>Flask: GET /recipes/new
    Flask-->>Browser: 回傳新增表單的網頁 (HTML)
    Browser-->>User: 顯示表單
    
    %% 送出表單儲存
    User->>Browser: 填寫完整資料 (標題, 食材, 步驟, 分類 ...) 並點擊送出
    Browser->>Flask: POST /recipes (攜帶表單資料 Payload)
    
    alt 資料驗證成功
        Flask->>DB: INSERT INTO recipes (title, ingredients, ...)
        DB-->>Flask: 資料庫寫入成功
        Flask-->>Browser: 302 Redirect 導向首頁 /recipes
        Browser->>Flask: GET /recipes
        Flask->>DB: SELECT * FROM recipes (可加上分類/搜尋條件)
        DB-->>Flask: 回傳最新的食譜清單
        Flask-->>Browser: 渲染清單頁面 (Jinja2)
        Browser-->>User: 顯示包含新食譜首頁視圖
    else 資料驗證失敗 (例如：漏填必填欄位)
        Flask-->>Browser: 回傳帶有錯誤提示語的表單網頁
        Browser-->>User: 畫面提示補齊欄位資料
    end
```

## 3. 功能清單對照表

根據 PRD 定義的功能與上述流程，規劃出對應的後端操作、URL 路徑與 HTTP 方法：

| 功能區域 | 對應行為與說明 | URL 路徑 | HTTP 方法 |
| -------- | -------------- | -------- | --------- |
| **首頁與清單** | 顯示所有食譜的清單；也支援透過 Query String（諸如 `?q=關鍵字` 或 `?category=中式`）過濾資料。 | `/` 或 `/recipes` | `GET` |
| **新增食譜 (檢視)** | 從伺服器取得一張空白的新增表單。 | `/recipes/new` | `GET` |
| **新增食譜 (動作)** | 接收來自表單送交的新增請求，並將此份食譜儲存進資料庫，完成後返回列表。 | `/recipes` | `POST` |
| **檢視食譜明細** | 查看某一筆特定食譜 (`<id>`) 的詳細資訊，包含所有食材與實作步驟。 | `/recipes/<id>` | `GET` |
| **編輯食譜 (檢視)** | 取得一份含有該食譜 (`<id>`) 現有資料的表單，讓使用者進行修改。 | `/recipes/<id>/edit` | `GET` |
| **編輯食譜 (動作)** | 儲存針對特定食譜所做的變更，完成後刷新明細頁面。 | `/recipes/<id>` | `POST` (或用 `PUT`) |
| **刪除食譜** | 從資料庫裡將特定的食譜資料完全移除。 | `/recipes/<id>/delete` | `POST` (或用 `DELETE`) |
