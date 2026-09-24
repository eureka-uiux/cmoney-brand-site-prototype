# CMoney 形象網站 prototype｜AI 協作規則

給 Claude Code、Cursor 等 AI 工具讀的規則。人類接手請先看 [handoff/README.md](handoff/README.md)。

## 正本

- **HTML 是唯一正本。** Figma 設計稿、`handoff/*.md` 都是從 HTML 產生的副本；不一致時以 HTML 為準。
- 要改的頁面只有兩個：`index.html`（首頁）、`business-groups.html`（事業群詳細頁）。
- `archive/` 是封存版本，**不要修改、不要從裡面搬程式碼回來**。
- 所有 CSS、JS 都內嵌在各自的 HTML 裡，沒有 build、沒有套件。直接用瀏覽器開檔預覽。

## 開工前先讀

1. [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md)：11 色、9 階字級、間距 token、元件規則、刻意破格清單。
2. [handoff/section-map.md](handoff/section-map.md)：每個區塊的 id、用途、互動、對應 Figma frame。
3. 要改文案或換圖時，先在 [handoff/content.md](handoff/content.md) / [handoff/assets.md](handoff/assets.md) 找到它在 HTML 的行號。

## 鐵則

- **不新增色票外的色值、9 階外的字級、既有值以外的圓角。** 真的需要時停下來問，不要自己加。
- **深底上的紅字用 `--red-300`**，不是 `--red`。
- **圖片一律放 `assets/`、用相對路徑 `assets/xxx`**，不要轉 data URI、不要用外部圖床。
- 換圖時沿用原檔名，或同時更新所有引用處（`handoff/assets.md` 列了每張圖用在哪幾行，同一張 icon 常常出現在 2～3 處）。
- 同一段文案可能在多處重複（例如 Header 與 Footer 導覽、兩頁共用的 Header）。改字前在 `handoff/content.md` 搜尋一次，確認所有出現處。
- 按下才出現的文字寫在 `<script>` 裡（`handoff/content.md` 每頁最後的「JS 動態文案」）。改按鈕文案時 HTML 和 JS 都要改。
- 互動改動要同時處理 `prefers-reduced-motion:reduce`（CSS 與 JS 都有對應分支）。
- 設計沒定義的狀態、邊界情境，**列出來問設計師，不要自己補一個看起來合理的答案**。

## 改完必做

```bash
python3 tools/handoff.py inventory
python3 tools/handoff.py check
```

- `inventory` 會從 HTML 重新產生 `handoff/content.md`、`handoff/assets.md`。**用 `git diff handoff/` 確認文案差異只包含你打算改的部分**；多出來或消失的字就是改壞了。
- `check` 出現 ❌ 必須處理；⚠️ 是既有的已知提醒（見 `handoff/README.md` 待確認），不要新增。
- 至少用 1440、768、375 三個寬度看過改動的區塊。
- 如果改到 token、元件規則或刻意破格，同步更新 `DESIGN-SYSTEM.md`；改到區塊結構，同步更新 `handoff/section-map.md`。

## 從 Figma 回改

設計師在 Figma 調整後，會給你 frame 連結。流程：

1. 用 Figma MCP 讀該 frame，**只把差異套回 HTML**，不要依 Figma 重寫整段。
2. Figma 的值若不在 DESIGN-SYSTEM.md 的 token 內，先回報，不要直接寫死新值。
3. 改完照「改完必做」跑一次。

## Commit

- 訊息用繁體中文，一句話說明改了哪個區塊的什麼，例如：`運作方式差異卡：拿掉 hover 浮起`。
- `handoff/*.md` 跟著 HTML 一起 commit。
