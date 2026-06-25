# CheckItNow Demo

獨立 Web 版 demo，方便之後 **換 logo / 品牌** 俾唔同客。  
唔再用 Streamlit — KPI 撳掣、篩選、scroll 全部用原生 HTML/JS。

## 結構

```
demo/
  config/branding.json    ← 改 app 名、tagline、logo 路徑、主色
  web/assets/logo.svg     ← 換客戶 logo
  web/index.html          ← 頁面
  web/css/style.css       ← 樣式
  web/js/app.js           ← KPI 點擊、scroll、compose
  logic/                  ← Python 業務邏輯（從 app.py 抽出）
  data/clients.json       ← 本地資料（首次執行自動建立）
  data/backups/           ← 自動備份（daily + recent 快照）
  config/backup_settings.json ← 備份保留天數等
  server.py               ← FastAPI
  run_dev.py              ← 開發：瀏覽器預覽
  run_desktop.py          ← 桌面視窗（之後打包 EXE 用）
```

## 快速開始

```powershell
cd demo
pip install -r requirements.txt
python run_dev.py
```

瀏覽器會開：`http://127.0.0.1:8765`

桌面視窗版：

```powershell
python run_desktop.py
```

## 換客戶品牌

1. 編輯 `config/branding.json`：

```json
{
  "appName": "Acme Tracker",
  "tagline": "Your tagline",
  "subtitle": "Short description",
  "logo": "/assets/logo.svg",
  "logoAlt": "Acme",
  "primaryColor": "#007AFF",
  "footerNote": "© Acme Ltd."
}
```

2. 替換 `web/assets/logo.svg`（或改 `logo` 指向 PNG）

3. 重新啟動 server

## KPI 行為

| 撳格 | 篩選 | Scroll 到 |
|------|------|-----------|
| 追蹤中 | 全部 | 追蹤看板 |
| 待處理 | 30 天內 | 優先處理 |
| 已完成 | 里程碑客戶 | 追蹤看板 |
| 已逾期 | 逾期 | 追蹤看板 |

## 打包 EXE（Windows）

已與 Airlink 版功能同步（Clients 分組／Closed、Milestones 提醒、排期編輯、Excel 匯出等）：

```powershell
cd demo
powershell -ExecutionPolicy Bypass -File build_exe.ps1
```

輸出：`dist\CheckItNow\CheckItNow.exe` — 整個 `CheckItNow\` 資料夾 zip 交付。

Itch 零售 zip：

```powershell
powershell -ExecutionPolicy Bypass -File package_itch_release.ps1
```

## 打包 Mac 版（.app）

**必須喺 macOS 機 build**（Windows 無法產出 `.app`）。流程同 Windows demo 一樣：本機 server + pywebview 視窗 + `data/` 喺 app 隔離。

```bash
cd demo
chmod +x build_mac.sh package_itch_release_mac.sh
./build_mac.sh
```

輸出：`dist/CheckItNow/CheckItNow.app` — 連同 `data/`、`config/` 一齊 zip。

Itch 零售 zip：

```bash
./package_itch_release_mac.sh
```

輸出：`release/CheckItNow-Mac-v1.6.0.zip`

注意：
- 首次開啟未簽名 app：右鍵 → Open
- 正式出街建議 **Apple Developer 簽名 + notarize**
- Mac 通知用系統 Notification Center（唔使 winotify）

### 冇 Mac？用 GitHub Actions 雲端 build

1. Push repo 去 GitHub（要包含 `demo/` 同 `.github/workflows/build-mac.yml`）
2. GitHub → **Actions** → **Build macOS app** → **Run workflow**
3. 約 5–10 分鐘後，喺該次 run 底部 **Artifacts** 下載：
   - `CheckItNow-Mac-itch-zip` → 直接 upload 去 itch.io
   - `CheckItNow-Mac-folder` → 解壓檢查用
4. 打 tag（例如 `v1.6.0`）push 上去都會自動 build

CI 產出 **Apple Silicon (arm64)** zip（GitHub Mac runner 原生架構）。舊 Intel Mac 唔支援；未簽名，用戶首次可能要右鍵 Open。

開發預覽：`python run_dev.py` → http://127.0.0.1:8765

正式出街建議再加 code signing，並在 installer 附 WebView2 runtime（舊 Win10 機）。

## 自動備份（Auto-Backup）

- 每次 **儲存 clients.json 前** 自動複製到 `data/backups/`
- **Daily rolling**：`backups/daily/clients-YYYY-MM-DD.json`（預設保留 45 日）
- **Recent snapshots**：`backups/recent/`（預設保留最近 8 次存檔前快照）
- **Atomic write**：先寫 `.tmp` 再替換，減少斷電損壞
- **自動還原**：主檔 JSON 損壞時，啟動會從最新備份還原
- 設定 → **Restore latest backup** 可手動一鍵還原

對外可描述：*Daily rolling backup — offline, no cloud required.*

## Forgot password

Demo uses local sign-in (no email reset). If someone forgets their password:

1. **Settings → Admin: reset user password** — sign in as `admin`, open Settings, scroll to the collaboration section, and reset the user account (requires admin password).
2. **Change your own password** — Settings → Account password (current + new password) while signed in.
3. **Manual recovery (local PC only)** — edit `config/collab.json` next to the EXE and set the `users` entry, or disable collaboration in Settings to remove the login gate (defaults: `admin`/`admin`, `user`/`user` on next enable).

Passwords are stored in plain text in `config/collab.json` for this demo — not suitable for production without hashing.

## 同 Streamlit 版關係

- 父目錄 `app.py` = 舊 Streamlit prototype  
- `demo/` = 新架構，之後為客戶 fork 呢個 folder 改 branding 就得
