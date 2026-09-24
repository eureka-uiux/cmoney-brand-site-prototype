# 區塊地圖

每個區塊的 id、內容、互動，以及對應的 Figma frame。
**改到區塊結構（新增、刪除、改 id、搬順序）時要同步更新這份。**

Figma frame 欄位目前空白，等 HTML → Figma 設計稿產出後補上連結。

## `index.html`（首頁）

| # | id | 導覽歸屬 | 內容 | 互動（JS / CSS） | Figma frame |
|---|---|---|---|---|---|
| — | `#siteHeader` | — | Logo、五個錨點選單、「看職缺」 | 捲動超過 12px 加陰影；≤980 收成漢堡選單；目前章節高亮 | |
| 1 | `#hero` | （全熄） | 使命主標、兩顆 CTA、四個數據卡 | 數字從 0 跑到終值；數據卡一半壓進下一區 | |
| 2 | `#aboutus` | 關於我們 | VISION → MISSION → METHOD 三卡 | 三卡隨捲動由淡轉實，目前那張紅框 | |
| 3 | `#values` | 價值觀 | 價值觀章節主標段 | 主標與說明依捲動由淡轉實 | |
| 4 | `#values-stack` | 價值觀 | 三張價值觀卡、金句、延伸閱讀 | 三張卡捲動時疊起來（sticky）。**三張 `.vstack` 必須在同一個 section 裡** | |
| 5 | `#values-outro` | 價值觀 | 深色宣言段 | 淡入 | |
| 6 | `#work` | 工作文化 | 工作文化章節主標段 | 主標與說明依捲動由淡轉實 | |
| 7 | `#work-compare` | 工作文化 | 「多數公司與我們的差異」卡、四個二選一情境題、求職入口 | 差異說明展開／收合；情境題作答前解析鎖住；分頁顯示作答狀態 | |
| 8 | `#business` | 事業群 | 深色宣言段 | 淡入 | |
| 9 | `#groups` | 事業群 | 四張事業群卡（連到 `business-groups.html#...`） | hover 展開產品面板；子元素依序淡入 | |
| 10 | `#northstar` | 事業群 | 4×4 產品 icon 牆、求職入口 | icon 由右欄往左欄淡入 | |
| 11 | `#founder` | 創辦人的話 | 創辦人照片與引言 | 引言逐字淡入；大圖載完才淡入 | |
| 12 | `#cta` | （全熄） | 結尾 CTA 與團隊照片 | — | |
| — | `footer.site-footer` | — | 網站地圖、社群連結 | — | |

所有互動在 `prefers-reduced-motion:reduce` 時都直接顯示最終狀態，細節見 [DESIGN-SYSTEM.md](../DESIGN-SYSTEM.md) §8。

## `business-groups.html`（事業群詳細頁）

| # | id | 內容 | 互動 | Figma frame |
|---|---|---|---|---|
| — | `#siteHeader` | 同首頁 Header 元件，加「回 CMoney 形象官網」 | 同首頁 | |
| — | `#rail` | 左側導覽：年份（里程碑）、事業群名稱 | 標示目前章節；點事業群平滑捲動並把 hash 寫進網址 | |
| 1 | `header.hero` | 頁首大圖與標題 | — | |
| 2 | `#ms` | 里程碑時間軸「從一套法人決策工具，到一千萬人的日常」 | 進度線隨捲動推進、段落進場、標示目前段落；數據進場時跑數字 | |
| 3 | `#groups` | 過渡段 | — | |
| 4 | `#finance` | 金融事業群 | — | |
| 5 | `#partnership` | 合作夥伴事業群 | — | |
| 6 | `#global` | 國際金融事業群 | — | |
| 7 | `#consumer` | 消費事業群 | — | |
| 8 | `section.fcta` | 結尾 Footer CTA | — | |

首頁 `#groups` 四張卡的連結依賴這四個錨點 id，改 id 要兩頁一起改。
