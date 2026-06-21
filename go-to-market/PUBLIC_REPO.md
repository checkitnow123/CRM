# CheckItNow — Public Demo Repo (最小檔案清單)

用途：**只放 Streamlit 試玩版**，接 Streamlit Community Cloud。  
桌面 EXE 完整源碼（`demo/`、`airlink/`）請放 **私人 repo**。

---

## 必須上傳（6 個）

```
checkitnow-demo/
├── app.py                 # 主程式（Streamlit 入口）
├── requirements.txt       # 依賴：streamlit, pandas
├── .gitignore             # 排除真實 data、EXE、build
├── .streamlit/
│   └── config.toml        # Cloud 主題 / headless
├── data/
│   └── sample_clients.json   # 可選；虛擬範例說明（非執行必需）
└── README.md              # 一頁說明 + 試玩連結（見下方範本）
```

| 檔案 | 說明 |
|------|------|
| `app.py` | **Main file path** 填這個 |
| `requirements.txt` | 目前只需 `streamlit>=1.29.0` 和 `pandas>=2.0.0` |
| `.streamlit/config.toml` | 已含 primaryColor `#007AFF` |
| `.gitignore` | 確保 `data/clients.json`、`**/dist/` 永不 commit |

---

## 絕對不要放進公開 repo

| 路徑 | 原因 |
|------|------|
| `demo/`、`airlink/` | 桌面版完整源碼 + 打包邏輯 |
| `**/dist/`、`**/build/`、`*.exe` | 編譯產物 |
| `**/data/clients.json` | 可能含真實客戶 |
| `**/data/backups/` | 備份 |
| `.env`、`.streamlit/secrets.toml` | 機密 |
| 任何真實 email / 電話 / 公司名 | 個資 |

---

## 建議 repo 設定

- **Repo 名稱：** `checkitnow-demo` 或 `checkitnow-flight-test`
- **Visibility：** Public
- **License：** 可加 `LICENSE`（Proprietary / All Rights Reserved），註明「試玩源碼僅供評估，禁止再分發」
- **Description：** `Interactive flight-test demo — client & service CRM for tutors, coaches, and field service.`

---

## Streamlit Cloud 部署步驟

1. Push 上述檔案到 GitHub `main` 分支  
2. 開啟 https://share.streamlit.io → **Create app**  
3. Repository：`你的帳號/checkitnow-demo`  
4. Branch：`main`  
5. **Main file path：** `app.py`  
6. **Deploy** → 得到 `https://<app-name>.streamlit.app`  
7. 把此 URL 填進 cold email 的 `[DEMO_LINK]`

本地先測：

```powershell
cd checkitnow-demo
pip install -r requirements.txt
streamlit run app.py
```

---

## README.md 範本（可直接貼到公開 repo）

```markdown
# CheckItNow — Interactive Flight Test Demo

**Try it in your browser (no download):** [DEMO_LINK]

Track clients, session milestones, and renewal reminders — built for tutors, coaches, therapists, and small service businesses.

- This repo is the **web sandbox only** (fictional Client A/B/C/D data).
- **Production delivery:** standalone Windows `.exe`, 100% offline, data stays on your PC.
- Custom builds from **$1,499 USD** — enterprise scope from **$9,999 USD**.
- Email: checkitnow123@gmail.com

© CheckItNow. Demo source for evaluation only; not licensed for redistribution.
```

---

## 雙 repo 策略（推薦）

| Repo | 內容 | 可見性 |
|------|------|--------|
| `checkitnow-demo` | 上表 6 檔 | **Public** |
| `checkitnow`（本機完整專案） | `demo/`、`airlink/`、打包腳本 | **Private** |

公開庫被 fork 只會抄到試玩版，抄唔到可賣的 EXE 產品線。

---

## 上線前 30 秒檢查

- [ ] 試玩頁頂部見到 **Interactive Flight Test Demo Only**
- [ ] 底部見到 **$9,999 / $1,499** 與 email
- [ ] 範例客戶為 Client A–D、`@example.com`
- [ ] `git status` 無 `clients.json`、無 `dist/`
- [ ] Streamlit Cloud 部署成功、手機可開
