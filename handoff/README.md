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
3. 注意解析度：大圖的建議尺寸見下方〈大圖需要的尺寸〉。

### 從 Figma 調整

在 Figma 改完後，把 frame 連結給 AI，請它「把這個 frame 的差異套回 HTML」。以 HTML 為準，Figma 改完一定要回寫 HTML 才算數。

## 待確認

盤點時發現、還沒決定怎麼處理的事項。處理完請從清單刪掉。

**圖片**

- [ ] **5 張大圖需要換高解析原圖**：尺寸見下表。

### 大圖需要的尺寸

實測頁面上的顯示框（`object-fit:cover`，會裁切）。建議尺寸以 1440 寬筆電的 2 倍 Retina 為準，同時滿足 1920 桌機與手機直式裁切。

| 檔案 | 現在 | 顯示框 1920 / 1440 / 390 寬 | 建議尺寸（比例） | 最低可接受 |
|---|---|---|---|---|
| `hero.jpg` | 1248×832 | 1905×809 / 1425×762 / 390×919 | **2880×1920**（3:2） | 1920×1280 |
| `cta-team.jpg` | 1264×842 | 1905×719 / 1425×719 / 390×456 | **2880×1920**（3:2） | 1920×1280 |
| `hero-groups.jpg` | 1264×843 | 1905×556 / 1425×556 / 390×444 | **2880×1920**（3:2） | 1920×1280 |
| `footer-cta-office.jpg` | 659×440 | 1905×560 / 1425×559 / 390×440 | **2880×1920**（3:2） | 1920×1280 |
| `founder.jpg` | 832×1248 | 640×920 / 640×920 / 390×380 | **1280×1920**（2:3） | 1280×1920 |

- 維持現在的比例，換圖時版面不會變。
- 「最低可接受」是 1920 桌機 1 倍清晰的底線，Retina 螢幕上仍會略糊。
- **注意裁切**：桌機上 `hero-groups.jpg`、`footer-cta-office.jpg` 只顯示約 3.4:1 的橫條，3:2 原圖上下各約 28% 會被切掉；`hero.jpg` 在手機上是直式框，只顯示中間約 28% 的寬度。人物臉部與主體要放在畫面中央。
- `footer-cta-office.jpg` 現在在 1440 寬螢幕上被放大約 2.2 倍，是五張裡最糊的。
- 輸出 JPG，品質約 80%，每張盡量控制在 500KB 以內。

**頁面標題**

- [ ] `<title>` 與 `og:title` 還是工作中的名稱。官網格式是「CMoney｜頁名」（實測 `cmoney.tw/careers/aboutus` 為「CMoney｜關於我們」）。建議：

  | 頁面 | 欄位 | 現在 | 建議 |
  |---|---|---|---|
  | `index.html` | `<title>` | CMoney 形象網站_價值觀互動 | CMoney｜關於我們 |
  | `index.html` | `og:title` | CMoney 形象網站｜我們的使命，是幫助每個人做好人生的投資 | CMoney｜我們的使命，是幫助每個人做好人生的投資 |
  | `business-groups.html` | `<title>` | CMoney 事業群 | CMoney｜事業群 |

## 封存

- `archive/index-v2.html`：工作文化區「先看差異、情境二選一、適合度」的另一個版本（commit `457ad40`）。圖片路徑已經改成 `../assets/`，還是可以直接打開，但不再維護。
- 領導團隊區塊和 `leader-*.png` 人物照已經從官網拿掉，repo 裡也刪除了。
