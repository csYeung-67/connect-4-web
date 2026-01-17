# 四子棋網頁遊戲 (Connect 4 Web Game)

一個基於 Minimax 演算法和 Alpha-Beta 剪枝的智能四子棋網頁遊戲，支援人對人和人對 AI 兩種模式。

## 功能特點

- 🎮 **雙模式遊戲**：支援人對人和人對 AI 兩種遊戲模式
- 🤖 **智能 AI**：使用 Minimax 演算法配合 Alpha-Beta 剪枝，搜尋深度為 3
- 🎨 **現代化 UI**：響應式設計，美觀的動畫效果
- 📱 **響應式布局**：適配桌面和移動設備
- ⚡ **即時反饋**：流暢的落子動畫和勝利提示

## 項目結構

```
connect-4-web/
├── frontend/              # 前端代碼（部署到 GitHub Pages）
│   ├── index.html        # 主頁面
│   ├── style.css         # 樣式
│   ├── game.js           # 遊戲邏輯
│   └── api.js            # API 調用
├── backend/              # 後端代碼
│   ├── app.py           # Flask 應用
│   ├── agent.py         # AI Agent 邏輯
│   └── requirements.txt # Python 依賴
└── README.md            # 說明文檔
```

## 快速開始

### 本地開發

#### 1. 後端設置

```bash
# 進入後端目錄
cd backend

# 創建虛擬環境（可選但推薦）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 運行後端服務器
python app.py
```

後端服務將在 `http://localhost:5000` 運行。

#### 2. 前端設置

```bash
# 進入前端目錄
cd frontend

# 使用任何靜態文件服務器運行
# 方法 1: 使用 Python
python -m http.server 8000

# 方法 2: 使用 Node.js (需要安裝 http-server)
npx http-server -p 8000

# 方法 3: 使用 VS Code Live Server 擴展
```

前端將在 `http://localhost:8000` 運行。

#### 3. 配置 API URL

如果後端運行在不同的地址或端口，請編輯 `frontend/api.js` 中的 `API_BASE_URL`：

```javascript
const API_BASE_URL = 'http://localhost:5000'; // 修改為您的後端地址
```

## 部署指南

### 前端部署（GitHub Pages）

1. **準備倉庫**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **啟用 GitHub Pages**
   - 進入 GitHub 倉庫設置
   - 找到 "Pages" 選項
   - 選擇源分支（通常是 `main`）
   - 選擇源目錄為 `/frontend`
   - 保存設置

3. **更新 API URL**
   - 編輯 `frontend/api.js`
   - 將 `API_BASE_URL` 設置為您的後端部署地址

### 後端部署選項

#### 選項 1: Render（推薦）

1. 註冊 [Render](https://render.com) 帳號
2. 創建新的 Web Service
3. 連接您的 GitHub 倉庫
4. 設置：
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && python app.py`
   - **Environment**: Python 3
5. 部署完成後，更新前端的 `API_BASE_URL` 為 Render 提供的 URL

#### 選項 2: Railway

1. 註冊 [Railway](https://railway.app) 帳號
2. 創建新項目並連接 GitHub 倉庫
3. 設置根目錄為 `backend`
4. Railway 會自動檢測 Python 項目並安裝依賴
5. 部署完成後，更新前端的 `API_BASE_URL`

#### 選項 3: Heroku

1. 在 `backend` 目錄創建 `Procfile`：
   ```
   web: python app.py
   ```

2. 安裝 Heroku CLI 並登錄
3. 創建應用：
   ```bash
   heroku create your-app-name
   ```

4. 部署：
   ```bash
   git subtree push --prefix backend heroku main
   ```

#### 選項 4: 本地運行（開發測試）

按照「快速開始」部分的說明在本地運行後端。

## API 文檔

### 健康檢查

```
GET /api/health
```

響應：
```json
{
  "status": "ok",
  "message": "Connect 4 AI API is running"
}
```

### 獲取 AI 移動

```
POST /api/move
```

請求體：
```json
{
  "board": [0,0,1,2,...],  // 扁平化棋盤，0=空，1=玩家1，2=玩家2
  "mark": 1,               // AI 的玩家標記 (1 或 2)
  "rows": 6,               // 可選，默認 6
  "columns": 7,            // 可選，默認 7
  "inarow": 4,             // 可選，默認 4
  "depth": 3               // 可選，默認 3
}
```

響應：
```json
{
  "column": 3,             // AI 選擇的列索引 (0-6)
  "status": "success"
}
```

## 技術棧

### 前端
- HTML5
- CSS3 (動畫、響應式設計)
- JavaScript (ES6+)

### 後端
- Python 3
- Flask (Web 框架)
- NumPy (數組處理)
- Flask-CORS (跨域支持)

### AI 演算法
- Minimax 演算法
- Alpha-Beta 剪枝優化

## 遊戲規則

1. 遊戲在 6x7 的棋盤上進行
2. 玩家輪流在列頂部落子
3. 棋子會落在該列最下方的空位
4. 率先在水平、垂直或對角線方向連成 4 子的玩家獲勝
5. 如果棋盤填滿且無人獲勝，則為平局

## 開發說明

### 調整 AI 難度

在 `backend/agent.py` 的 `get_ai_move` 函數中，可以調整 `depth` 參數：
- `depth=3`：中等難度（默認）
- `depth=4`：困難
- `depth=5`：極難（計算時間較長）

或在 API 請求中傳遞 `depth` 參數。

### 自定義樣式

編輯 `frontend/style.css` 可以自定義：
- 顏色主題
- 動畫效果
- 響應式斷點

## 故障排除

### 後端無法連接

1. 確認後端服務正在運行
2. 檢查 `API_BASE_URL` 是否正確
3. 確認 CORS 設置正確（後端已配置允許所有來源）

### AI 響應緩慢

- 降低 `depth` 參數值
- 檢查服務器性能
- 考慮使用更強大的服務器

### 前端無法加載

- 檢查文件路徑是否正確
- 確認所有 JavaScript 文件都已正確引用
- 查看瀏覽器控制台的錯誤信息

## 許可證

MIT License

## 貢獻

歡迎提交 Issue 和 Pull Request！

## 聯繫方式

如有問題或建議，請在 GitHub 上創建 Issue。
