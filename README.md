# CMoney 形象網站 prototype

單一自我包含的 `index.html`（CSS 與 JS 全部內嵌），圖片放在 `assets/`。
直接開 `index.html` 就能看，部署到 GitHub Pages 不需要任何 build。

```
index.html            # 首頁，全部樣式與腳本內嵌在此
business-groups.html  # 事業群詳細頁
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
| 1 | `hero` | 深 `--ink` | 0.88 視窗 |
| 2 | `who` | 白 | 1.13 |
| 3 | `northstar` | 深（新增） | 0.48 |
| 4 | `values` | 白 | 0.58 |
| 5 | `values-stack` | 淺灰 `#f6f6f6`（新增） | 2.18 |
| 6 | `values-outro` | 深（新增） | 0.46 |
| 7 | `how` | 白 | 0.53 |
| 8 | `how-compare` | 淺灰（新增） | 1.09 |
| 9 | `what` | 深 | 0.57 |
| 10 | `groups` | 白（新增） | 1.74 |
| 11 | `founder` | 白（全幅出血，非 `.container`） | 1.02 |
| 12 | `cta` | 深 | 0.62 |

新增的 class：`.section--statement`（短深色宣言段）。
底色一度改成 `#f3efe9` 暖灰，後因對齊官網色票（官網僅有 `#f6f6f6` 一個淺灰底）改回 `#f6f6f6`。

### 2. Hero 與 `who` 的交界

- `.hero__stats{margin-bottom:-64px}`：數據卡一半壓在深色、一半落進白區
- `.hero` 拿掉 `overflow:hidden`，改由 `.hero__bg` 裁切（否則卡片會被切掉）
- `.hero::after`：底部 180px 由 `rgba(0,0,0,0)` 漸層收束到 `#fff`
- `#aboutus` 上緣 `calc(var(--section-pad) + 64px)` 接住越界的卡片
- `.stat` 底色改 `rgba(38,38,38,.92)` + `backdrop-filter`，避免浮在漸層白上失去對比
- `#aboutus` 開頭一個 `.section-cue`（紅色漸淡細線 +「接下來：我們是誰」）

### 3. 進場動畫

reveal 觸發門檻太深，捲動時會出現整片空白的視窗。已改為
`rootMargin:"0px 0px -5% 0px"`、`threshold:0.05`，位移 28→24px、0.8s→0.55s。

### 4. 導覽

`navOwner` 把新增的區塊對應回原本的五個選單項（`northstar`→`who`、
`values-stack`/`values-outro`→`values`、`how-compare`→`how`、`groups`→`what`）。

## 設計規範（對齊 cmoney.tw/careers）

> 完整版見 [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md)：色票鐵則、字級階梯、間距、元件規則與二選一情境題的出題／解析規範。

色票、字級、字重以官網實測值為準，**新增任何色值或字級前請先確認官網有無對應**。

- **色票（全站僅這 11 色）**：`#e21e28`（主色）／`#a0151c` hover／`#811117` active／
  `#f39ea3`（深底上的紅字）／`#262626`／`#595959`／`#959595`／`#bfbfbf`／`#d9d9d9`／
  `#f6f6f6`／`#ffffff`
- **字級（9 階，固定 px，不用 clamp）**：52/64 · 40/48 · 30/36 · 24/32 · 20/32 · 20/28 ·
  18/28 · 18/24 · 16/24 · 14/20 · 12/16
- **字重僅 400 / 500 / 600**，`letter-spacing` 一律 `.004em`（uppercase 標籤 `.08em`）
- **字體**：官網系統字堆疊，不載入 webfont
- **行動版斷點 `max-width:768px`**：H1 52→30、H2 30→24、H3 24→20、desc 20→18

刻意破格的地方已在 CSS 加註解：

| 例外 | 值 | 理由 |
|---|---|---|
| `.hero__title` | `clamp(44px,6.4vw,92px)` / 700 / `-.075em` | 保留原視覺重量 |
| Display 層（`.h2` / `.statement`） | 52/64，≤1200 降 40/48，≤768 降 30/36 | 借官網 H1 的階給章節主標，拉開與段內小標的層級 |
| `.founder__title` / `.founder__kicker` | 44/60 / 700（紅字 900）、16/24 / 500 / `ls 2px` | 照 Figma node 6727:13541 實作，只限創辦人區塊 |

深底上的紅字一律用 `#f39ea3`：`#e21e28` 在 `#262626` 上只有 3.21:1，不過 AA。

## 改動時要注意

- **不要破壞 `assets/` 的相對路徑**，也不要把圖片轉成 data URI（檔案會爆）。
- `#values-stack` 的 `.vstack` 是 sticky 堆疊卡，由 `updateStack()` 計算景深；
  三張卡必須留在**同一個** section 裡，拆開就失效。
- `#work-compare` 的 `.cmp` 有展開互動（`.cmp__opt` / `.cmp__reveal`），
  以及 `prefers-reduced-motion` 的退場處理，改版面時要一起測。
- 所有動效都有 `@media (prefers-reduced-motion:reduce)` 的對應規則，新增效果請比照。
- 手機 ≤768px 有獨立的間距與越界量（`.hero__stats{margin-bottom:-48px}` 等），
  以及官網的字級降階規則，改標題時兩邊都要看。

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
