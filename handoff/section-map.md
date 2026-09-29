# 區塊地圖

每個區塊的 id、內容、互動，以及對應的 Figma frame。
**改到區塊結構（新增、刪除、改 id、搬順序）時要同步更新這份。**

Figma 設計稿：[CMoney 形象網站｜Design handoff](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6866-2795)（頁面「新內容by ken」裡的 Section「Design handoff」，2026-09-29 由 HTML 1440 寬轉出）。
Figma frame 欄位是各區塊在稿上的 frame；圖層名稱沿用 HTML 的 id／class。按下、捲動、hover 之後的樣子另外放在「30 互動狀態｜index.html」「31 互動狀態｜business-groups.html」。

## `index.html`（首頁）

| # | id | 導覽歸屬 | 內容 | 互動（JS / CSS） | Figma frame |
|---|---|---|---|---|---|
| — | `#siteHeader` | — | Logo、五個錨點選單、「看職缺」 | 捲動超過 12px 加陰影；≤980 收成漢堡選單；目前章節高亮 | [6875:2946](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6875-2946) |
| 1 | `#hero` | （全熄） | 使命主標、兩顆 CTA、四個數據卡 | 數字從 0 跑到終值；數據卡一半壓進下一區 | [6871:2795](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6871-2795) |
| 2 | `#aboutus` | 關於我們 | VISION → MISSION → METHOD 三卡 | 三卡隨捲動由淡轉實，目前那張紅框 | [6871:2849](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6871-2849) |
| 3 | `#values` | 價值觀 | 價值觀章節主標段 | 主標與說明依捲動由淡轉實 | [6871:2882](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6871-2882) |
| 4 | `#values-stack` | 價值觀 | 三張價值觀卡、金句、延伸閱讀 | 三張卡捲動時疊起來（sticky）。**三張 `.vstack` 必須在同一個 section 裡** | [6871:2890](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6871-2890) |
| 5 | `#values-outro` | 價值觀 | 深色宣言段 | 淡入 | [6871:2946](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6871-2946) |
| 6 | `#work` | 工作文化 | 工作文化章節主標段 | 主標與說明依捲動由淡轉實 | [6871:2950](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6871-2950) |
| 7 | `#work-compare` | 工作文化 | 「多數公司與我們的差異」卡、四個二選一情境題、求職入口 | 差異說明展開／收合；情境題作答前解析鎖住；分頁顯示作答狀態 | [6874:2795](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6874-2795) |
| 8 | `#business` | 事業群 | 深色宣言段 | 淡入 | [6874:2932](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6874-2932) |
| 9 | `#groups` | 事業群 | 四張事業群卡（連到 `business-groups.html#...`） | hover 展開產品面板；子元素依序淡入 | [6874:2936](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6874-2936) |
| 10 | `#northstar` | 事業群 | 4×4 產品 icon 牆、求職入口 | icon 由右欄往左欄淡入 | [6875:2795](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6875-2795) |
| 11 | `#founder` | 創辦人的話 | 創辦人照片與引言 | 引言逐字淡入；大圖載完才淡入 | [6875:2833](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6875-2833) |
| 12 | `#cta` | （全熄） | 結尾 CTA 與團隊照片 | — | [6875:2859](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6875-2859) |
| — | `footer.site-footer` | — | 網站地圖、社群連結 | — | [6875:2875](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6875-2875) |

所有互動在 `prefers-reduced-motion:reduce` 時都直接顯示最終狀態，細節見 [DESIGN-SYSTEM.md](../DESIGN-SYSTEM.md) §8。

## `business-groups.html`（事業群詳細頁）

| # | id | 內容 | 互動 | Figma frame |
|---|---|---|---|---|
| — | `#siteHeader` | 同首頁 Header 元件，加「回 CMoney 形象官網」 | 同首頁 | [6879:3032](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6879-3032) |
| — | `#rail` | 左側導覽：年份（里程碑）、事業群名稱 | 標示目前章節；點事業群平滑捲動並把 hash 寫進網址 | [6886:2795](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6886-2795) |
| 1 | `header.hero` | 頁首大圖與標題 | — | [6877:2795](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6877-2795) |
| 2 | `#ms` | 里程碑時間軸「從一套法人決策工具，到一千萬人的日常」 | 進度線隨捲動推進、段落進場、標示目前段落；數據進場時跑數字 | [6877:2803](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6877-2803) |
| 3 | `#groups` | 過渡段 | — | [6877:2921](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6877-2921) |
| 4 | `#finance` | 金融事業群 | — | [6877:2926](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6877-2926) |
| 5 | `#partnership` | 合作夥伴事業群 | — | [6879:2795](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6879-2795) |
| 6 | `#global` | 國際金融事業群 | — | [6879:2883](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6879-2883) |
| 7 | `#consumer` | 消費事業群 | — | [6879:2946](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6879-2946) |
| 8 | `section.fcta` | 結尾 Footer CTA | — | [6879:3023](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6879-3023) |

首頁 `#groups` 四張卡的連結依賴這四個錨點 id，改 id 要兩頁一起改。

## 互動狀態（Figma）

| 狀態 | Figma frame |
|---|---|
| Header 捲動後（陰影＋目前章節高亮） | [6882:2795](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6882-2795) |
| VISION／MISSION／METHOD 捲動中 | [6882:2823](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6882-2823) |
| 差異對照表：全部收合／全部展開 | [6882:2846](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6882-2846) ／ [6882:2903](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6882-2903) |
| 情境題 1 選 A／選 B | [6883:2795](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6883-2795) ／ [6883:2860](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6883-2860) |
| 情境題 2／3／4 選 B | [6883:2925](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6883-2925) ／ [6885:2795](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6885-2795) ／ [6885:2860](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6885-2860) |
| 事業群卡 hover：金融／合作夥伴／消費／國際金融 | [6885:2925](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6885-2925) ／ [6885:2954](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6885-2954) ／ [6885:2981](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6885-2981) ／ [6885:3008](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6885-3008) |
| 事業群頁左側導覽：里程碑段／事業群段 | [6886:2795](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6886-2795) ／ [6886:2811](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6886-2811) |
| 事業群頁里程碑時間軸捲動中 | [6886:2822](https://www.figma.com/design/1sL3DgPchc2IEgcwHCs0ws/?node-id=6886-2822) |
