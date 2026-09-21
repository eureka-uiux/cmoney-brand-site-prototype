# CMoney 形象網站 prototype

單一自我包含的 `index.html`（CSS 與 JS 全部內嵌），圖片放在 `assets/`。
直接開 `index.html` 就能看，部署到 GitHub Pages 不需要任何 build。

```
index.html            # 首頁，全部樣式與腳本內嵌在此
business-groups.html  # 事業群詳細頁
proto-groups.html     # 事業群卡片原型（舊版，未連入首頁）
proto-groups-v2.html  # 事業群卡片原型 v2
assets/               # 47 個圖片檔，首頁與詳細頁共用
.nojekyll             # GitHub Pages 不要跑 Jekyll
```

> **圖片一定要跟著 `assets/` 一起放。** `index.html` 內的圖片全部用相對路徑
> （`assets/hero.jpg`、`assets/screen-chipk.png` …），單獨把 `index.html` 拿出來開會整頁掉圖。

## 這一版改了什麼

問題：全頁 9,629px 只切成 8 個區塊，其中 `values` 2,529px、`what` 1,888px 等於 2–3 個
視窗高；中段 `how` + `what` 連續 3,147px 純白；捲動時資訊沒有推進感。

### 1. 重新切塊（8 塊 → 12 塊）

長區塊裡的「宣言」獨立成短的深色段落，當成節奏上的休止符。

| # | section id | 底色 | 高度（1440×900） |
|---|---|---|---|
| 1 | `hero` | 深 `--ink-900` | 0.88 視窗 |
| 2 | `who` | 白 | 1.13 |
| 3 | `northstar` | 深（新增） | 0.48 |
| 4 | `values` | 白 | 0.58 |
| 5 | `values-stack` | 暖灰 `#f3efe9`（新增） | 2.18 |
| 6 | `values-outro` | 深（新增） | 0.46 |
| 7 | `how` | 白 | 0.53 |
| 8 | `how-compare` | 暖灰（新增） | 1.09 |
| 9 | `what` | 深 | 0.57 |
| 10 | `groups` | 白（新增） | 1.74 |
| 11 | `founder` | 暖灰 | 1.29 |
| 12 | `cta` | 深 | 0.62 |

新增的 class：`.section--statement`（短深色宣言段）。
底色從 `#f9f9f9` / `#f6f6f6` 改成 `#f3efe9` 暖灰，和白色才分得出來。

### 2. Hero 與 `who` 的交界

- `.hero__stats{margin-bottom:-64px}`：數據卡一半壓在深色、一半落進白區
- `.hero` 拿掉 `overflow:hidden`，改由 `.hero__bg` 裁切（否則卡片會被切掉）
- `.hero::after`：底部 180px 由 `rgba(9,16,28,0)` 漸層收束到 `#fff`
- `#who` 上緣 `calc(var(--section-pad) + 64px)` 接住越界的卡片
- `.stat` 底色改 `rgba(20,27,38,.92)` + `backdrop-filter`，避免浮在漸層白上失去對比
- `#who` 開頭一個 `.section-cue`（紅色漸淡細線 +「接下來：我們是誰」）

### 3. 進場動畫

reveal 觸發門檻太深，捲動時會出現整片空白的視窗。已改為
`rootMargin:"0px 0px -5% 0px"`、`threshold:0.05`，位移 28→24px、0.8s→0.55s。

### 4. 導覽

`navOwner` 把新增的區塊對應回原本的五個選單項（`northstar`→`who`、
`values-stack`/`values-outro`→`values`、`how-compare`→`how`、`groups`→`what`）。

## 改動時要注意

- **不要破壞 `assets/` 的相對路徑**，也不要把圖片轉成 data URI（檔案會爆）。
- `#values-stack` 的 `.vstack` 是 sticky 堆疊卡，由 `updateStack()` 計算景深；
  三張卡必須留在**同一個** section 裡，拆開就失效。
- `#how-compare` 的 `.cmp` 有展開互動（`.cmp__opt` / `.cmp__reveal`），
  以及 `prefers-reduced-motion` 的退場處理，改版面時要一起測。
- 所有動效都有 `@media (prefers-reduced-motion:reduce)` 的對應規則，新增效果請比照。
- 手機 ≤768px 有獨立的間距與越界量（`.hero__stats{margin-bottom:-48px}` 等）。

## 還沒處理的兩塊

- `values-stack` 2.18 視窗 — sticky 堆疊本身就是三張卡輪替，要再壓就得拆成三段，會失去堆疊效果。
- `groups` 1.74 視窗 — 五張卡兩欄三列，可再拆成「金融／合作夥伴／消費」與「國際／AI Lab」兩塊。

## 部署

```bash
git add -A
git commit -m "重新切塊：8 段 → 12 段，新增深色宣言段與暖灰底色；hero 數據卡越界與收束漸層"
git push
```

GitHub Pages 設定在 Settings → Pages → Source 選 `main` / `root`，
`.nojekyll` 已經在 repo 根目錄。
