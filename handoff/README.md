# 交接說明

給接手的設計師。AI 工具的規則在根目錄 [AGENTS.md](../AGENTS.md)（Claude Code 透過 `CLAUDE.md` 讀同一份）。

## 這個專案是什麼

CMoney 形象網站的 HTML prototype。**HTML 是正本**，Figma 稿是從 HTML 產生的副本。

- 線上預覽：https://eureka-uiux.github.io/cmoney-brand-site-prototype/index.html
- 本機預覽：直接用瀏覽器開 `index.html`，不需要安裝任何東西。
- 部署：push 到 `main`，GitHub Pages 自動更新。

## 檔案

```
index.html              首頁（正本）
business-groups.html    事業群詳細頁（正本）
assets/                 兩頁共用的圖片
DESIGN-SYSTEM.md        色票、字級、間距、元件規則
AGENTS.md / CLAUDE.md   AI 協作規則
handoff/
  README.md             這份
  section-map.md        區塊地圖（id、內容、互動、Figma frame）
  content.md            全站文案清單（腳本產生，不要手改）
  assets.md             圖片清單（腳本產生，不要手改）
tools/handoff.py        產生清單＋檢查
archive/                封存版本，不再維護
```

## 日常修改流程

1. 用 Claude Code 或 Cursor 開這個資料夾，直接用中文描述要改什麼（例如「把 #hero 的主標改成…」、「把 founder.jpg 換成這張」）。
2. AI 改完會跑 `python3 tools/handoff.py inventory` 和 `check`。
3. **看 `handoff/content.md` 的 git diff**：只該出現你要改的字。多了或少了，就是改到不該改的地方。
4. 用瀏覽器在電腦、平板、手機寬度各看一次。

### 要改文案

改 HTML，不是改 `content.md`。可以先在 `content.md` 搜尋那段字，找到頁面和行號後交給 AI。

### 要換圖

1. 新圖放進 `assets/`。最保險的做法是沿用原檔名直接覆蓋。
2. 在 `assets.md` 查這張圖用在哪幾處（同一個 icon 在首頁可能出現 2 次、在詳細頁再 1 次）。
3. 注意解析度：全幅大圖的原檔寬度建議至少 2 倍顯示寬度。目前幾張大圖只有約 1264px（見下方待確認）。

### 從 Figma 調整

在 Figma 改完後，把 frame 連結給 AI，請它「把這個 frame 的差異套回 HTML」。以 HTML 為準，Figma 改完一定要回寫 HTML 才算數。

## 待確認

盤點時發現、還沒決定怎麼處理的事項。處理完請從清單刪掉。

**圖片**

- [ ] **14 張 AI 實驗室 icon 沒有被使用**：`icon-ailab-app-01`～`12.png`、`icon-ailab-diary.png`、`icon-ailab-taigang.png`。commit `8768912` 移除 AI Lab 事業群後就沒有引用了。要刪除，還是保留給之後用？
- [ ] **3 張 PNG 已經被 WebP 取代**：`screen-chipk.png`、`screen-creator.png`、`screen-einvoice.png`，頁面用的是同名的 `.webp`。要刪除嗎？
- [ ] **大圖解析度不足**：`hero.jpg` 1248×832、`cta-team.jpg` 1264×842、`hero-groups.jpg` 1264×843、`founder.jpg` 832×1248，都是從 Figma 匯出的。在高解析度螢幕上會糊，正式上線前需要原圖。
- [ ] `footer-cta-office.jpg` 只有 659×440，要確認它在詳細頁的顯示尺寸是否足夠。

**色票外的色值**（`check` 的 ⚠️）

- [ ] `index.html` 708–709 行還有 `#f3efe9`：DESIGN-SYSTEM.md 寫這個暖灰「已改回 `#f6f6f6`」，但 CSS 裡仍有兩處。要確認是殘留還是被覆寫掉的舊規則。
- [ ] `index.html` 的 `#25282f`、`#030508`（221、230、231 行）、`#0f0f0f`（199 行）、`#000`（134 行），以及 `business-groups.html` 的 `#000`、`#111`：要收進 token，還是在 DESIGN-SYSTEM.md 列為刻意破格？

**命名**

- [ ] `index.html` 的 CSS／JS 註解裡的「v2」是指 2026-09-23 那次改版，和已封存的 `archive/index-v2.html` 是兩回事。要不要把註解改成日期，避免混淆？
- [ ] `<title>` 還是「CMoney 形象網站_價值觀互動」，看起來是工作中的名稱。要改嗎？

## 封存

- `archive/index-v2.html`：工作文化區「先看差異、情境二選一、適合度」的另一個版本（commit `457ad40`）。圖片路徑已經改成 `../assets/`，還是可以直接打開，但不再維護。
- 領導團隊區塊和 `leader-*.png` 人物照已經從官網拿掉，repo 裡也刪除了。
