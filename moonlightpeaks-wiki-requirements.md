# Moonlight Peaks Wiki — 完整需求文档 (v5 — Final)

---

## 1. 站点定位

**不是数据库 wiki，而是任务解决型攻略站。**

区别于 wiki.gg（全量数据库），本站每个页面精准回答一个搜索意图。

**不做的事：**
- 不做 53 个独立作物页面（thin content）
- 不做全角色数据库
- 不做假冒评测
- 不编造数据
- 不大段改写/近似复述 PC Gamer / IGN / Eurogamer 原文

**第一批 17 页，新游小站测试。7-14 天 GSC 观察后决定是否扩。**

---

## 2. 事实来源分级（Codex 必须遵守）

| 级别 | 来源 | 规则 |
|------|------|------|
| **L1 官方** | Steam 商店、Nintendo.com、moonlightpeaks.com、Google Play | 平台、价格、发布日期、模式、文件大小优先用官方源 |
| **L2 高质量攻略** | PC Gamer、IGN、Eurogamer、GameRant、LadiesGamers | 任务步骤可用，但必须改写为原创结构和措辞，不能近似复述 |
| **L3 社区** | Reddit、Discord、Steam 讨论、Facebook CozyGamers | 必须标注 "reported by players" / "community reports suggest" / "TBD" |

**禁止：**
- 把 L3 社区信息写成官方事实
- 编造缺失数据
- 从 L2 攻略站直接搬运段落或近似改写诗歌/原文

---

## 3. 页面清单

---

### P0 - 高概率拿展示（9页）

---

## 3.1 `/switch/`

| 字段 | 内容 |
|------|------|
| **Title** | `Is Moonlight Peaks on Switch? Switch & Switch 2 Guide` |
| **Meta Description** | `Moonlight Peaks is available on Nintendo Switch and Switch 2. Compare versions, upgrade pack details, demo availability, file size, performance notes, and where to buy.` |
| **H1** | `Is Moonlight Peaks on Nintendo Switch?` |
| **目标关键词** | moonlight peaks switch, switch 2, switch 1, switch price, nintendo |
| **需 FAQ schema** | ✅ |
| **需 Breadcrumb schema** | ✅ |

**页面大纲：**
1. 直接回答：Yes, available on Switch 1 & Switch 2 (Jul 7, 2026)
2. 快速总结表：平台 / 价格 / 文件大小 / 分辨率 / 帧率 / 玩家数
3. Switch 1 vs Switch 2 详细对比
4. 价格说明（标注 region/sale may vary）
5. Demo 可用性
6. 实体版 vs 数字版
7. FAQ

**已确认（L1 官方，Nintendo.com）：**
- Switch 1 文件大小: 2.5 GB
- Switch 2 文件大小: 4.5 GB
- Single system: 1 player
- Switch 2: higher resolution and improved frame rates
- Release date: July 7, 2026

**已确认（L3 community-reported）：**
- Switch 1 价格约 $34.99
- Switch 2 价格约 $39.99
- Switch 1 → Switch 2 upgrade 约 $5.00
- ⚠️ 标注：Prices shown on eShop may vary by region and sale period.

**不确定：**
- Switch 1/2 具体分辨率数值 → TBD
- 帧率具体数值 → TBD
- 实体版确切实体发售日期 → TBD

---

## 3.2 `/ps5/`

| 字段 | 内容 |
|------|------|
| **Title** | `Is Moonlight Peaks on PS5? — PlayStation & Xbox Status` |
| **Meta Description** | `Moonlight Peaks is NOT on PS5 or Xbox. Available on PC (Steam), macOS, Nintendo Switch, Switch 2, and Android. No PlayStation release has been announced.` |
| **H1** | `Is Moonlight Peaks on PS5?` |
| **目标关键词** | moonlight peaks ps5, is moonlight peaks on ps5 |
| **需 FAQ schema** | ✅ |
| **需 Breadcrumb schema** | ✅ |

**页面大纲：**
1. 直接回答：No, not on PS5. As of now, no PS5 or Xbox version has been announced.
2. 当前官方平台列表（Steam / macOS / Switch / Switch 2 / Android）
3. Demo only on Steam and Nintendo Switch
4. FAQ（含 "Will it come to PS5?" — 不要写死"永久不会"）

**已确认（L1 官方，moonlightpeaks.com）：**
- 平台入口: Steam, Nintendo Switch 2, Nintendo Switch, Google Play
- Demo: Steam and Nintendo Switch only

---

## 3.3 `/multiplayer/`

| 字段 | 内容 |
|------|------|
| **Title** | `Is Moonlight Peaks Multiplayer? Co-op & Online Play` |
| **Meta Description** | `Moonlight Peaks is a single-player game with no multiplayer or co-op mode. Available on Steam, Switch, Switch 2, and Android.` |
| **H1** | `Is Moonlight Peaks Multiplayer?` |
| **目标关键词** | is moonlight peaks multiplayer, moonlight peaks co-op |
| **需 FAQ schema** | ✅ |
| **需 Breadcrumb schema** | ✅ |

**页面大纲：**
1. 直接回答：No, single-player only
2. 官方来源：Steam 标注 Single-player / Nintendo 标注 single system 1 player
3. 当前平台
4. FAQ（含 "Does Moonlight Peaks require Nintendo Switch Online?" — 标注无多人模式列出，NSO 可能用于云存档但非必需）

**已确认（L1 官方）：**
- Steam: Single-player
- Nintendo: Single system 1 player

---

## 3.4 `/beginner-guide/`

| 字段 | 内容 |
|------|------|
| **Title** | `Moonlight Peaks Beginner Guide — First Week Tips & What to Do First` |
| **Meta Description** | `Just started Moonlight Peaks? First night walkthrough, which crops to plant, how to unlock tools, and essential tips from the community for a strong start.` |
| **H1** | `Moonlight Peaks Beginner Guide` |
| **目标关键词** | moonlight peaks beginner guide, what to do first, beginner tips |
| **需 FAQ schema** | ✅ |
| **需 Breadcrumb schema** | ✅ |

**页面大纲：**
1. 游戏简介（吸血鬼种田经营模拟，Little Chicken / XSEED）
2. 角色创建（名字、农场名、Hellkitten 名，外观不影响玩法）
3. 第一晚流程（可用 L2 攻略信息但用自己的语言改写）
   - 从棺材醒来（6 PM）
   - 见 Orlock（醉醺醺的叔叔，L2: LadiesGamers / IGN）
   - 种 Blood Grape
   - Town Hall 登记（Mayor Brook）
   - 认识居民
4. 前 7 天指南（标注 "typically" / "usually"）
5. 工具速览
6. 关键机制
7. 20 Tips（short bullet point format）
8. FAQ

**内容规则：**
- 时间估计用 "usually" / "around" / "approximately"
- 不确定具体触发条件的标注 TBD
- 任务步骤改写 L2 攻略站（不直接搬运原文）

---

## 3.5 `/romance-guide/`

| 字段 | 内容 |
|------|------|
| **Title** | `Moonlight Peaks Romance Guide — Dating, Marriage & Romance Options` |
| **Meta Description** | `Complete Moonlight Peaks romance guide: romanceable characters, dating, gifts, marriage, and how relationships work in the vampire farming sim.` |
| **H1** | `Moonlight Peaks Romance Guide` |
| **目标关键词** | moonlight peaks romance guide, is there romance, romance options |
| **需 FAQ schema** | ✅ |
| **需 Breadcrumb schema** | ✅ |

**页面大纲：**
1. 直接回答：Yes, approximately two dozen romanceable characters（官方商店用词）
2. 恋爱机制（提升好感、送礼、约会、4心表白、可能约多人）
3. 角色表格：名称 / 类型 / 家族 / 简介 / 可攻略
4. 重点角色展开
5. 婚姻说明
6. 配偶变吸血鬼
7. FAQ

**注意：**
- ⚠️ 不要在 title/meta 里写死 "23" — 用 "romance options" / "romanceable characters"
- 正文里可以写 "Most guides currently list 23 romanceable characters, while official store pages describe 'two dozen'" — 标注会持续更新

---

## 3.6 `/samael-romance/`

| 字段 | 内容 |
|------|------|
| **Title** | `How to Unlock Samael Romance in Moonlight Peaks` |
| **Meta Description** | `Step-by-step guide to dating Samael Ambrosia: unlock path, quest requirements, where to find him, loved gifts, and common blockers.` |
| **H1** | `How to Unlock Samael Romance in Moonlight Peaks` |
| **目标关键词** | moonlight peaks samael romance unlock, how to date samael |
| **需 FAQ schema** | ✅ |
| **需 Breadcrumb schema** | ✅ |

**页面大纲：**
1. Samael 是谁（Orlock 的侄子，Broken Lamp 酒吧老板）
2. 在哪里找到他
3. 解锁条件 / 需求清单
4. 分步解锁路径（清单化，不要叙事段落）
5. 遇到障碍时怎么办
6. 礼物偏好
7. 关键剧情节点
8. FAQ

**⚠️ Codex 要求：**
- 禁止近似复述 PC Gamer 原文
- 用清单/表格结构替代叙述段落
- 只写流程步骤，不搬 PC Gamer 的描写文字
- 内链自然提到 Orlock

---

## 3.7 `/treasure-hunt-clues/`

| 字段 | 内容 |
|------|------|
| **Title** | `Moonlight Peaks Elvira Treasure Hunt Clues Guide` |
| **Meta Description** | `Can't find Elvira's treasure? All five clue locations with exact spots, map areas, and what to look for in each location.` |
| **H1** | `Elvira Treasure Hunt Clue Locations — Moonlight Peaks` |
| **目标关键词** | moonlight peaks treasure hunt clues, elvira treasure hunt |
| **需 FAQ schema** | ✅ |
| **需 Breadcrumb schema** | ✅ |

**页面大纲：**
1. 简短介绍 + 触发方式
2. 线索位置表格：编号 / 区域 / 具体位置 / 要寻找的东西 / 备注
3. 奖励
4. FAQ

**已确认（L2，PC Gamer）：**
- 共 5 个线索
- 位置：The Broken Lamp / Ambrosia graveyard / Webb of Wonders / Cave of Echoes / Khazan Temple
- 奖励：可挂在家里的 painting

**⚠️ Codex 要求：**
- 用简洁表格呈现位置信息
- 不要复制 PC Gamer 的诗句原文
- 不搬 PC Gamer 的叙事/描写段落

---

## 3.8 `/fallen-tree/`

| 字段 | 内容 |
|------|------|
| **Title** | `Where to Find the Fallen Tree in Moonlight Peaks — Location & Spell` |
| **Meta Description** | `Find the fallen tree blocking the waterfall in Moonlight Peaks. Exact location (Moonlit Pines), required Arborascend spell, how to get it, and common mistakes.` |
| **H1** | `Where to Find the Fallen Tree in Moonlight Peaks` |
| **目标关键词** | moonlight peaks fallen tree, where to find fallen tree, arborascend |
| **需 FAQ schema** | ✅ |
| **需 Breadcrumb schema** | ✅ |

**页面大纲：**
1. Quick answer（位置 + 所需法术）
2. 属于哪个任务
3. 精确位置描述
4. 所需法术 (Arborascend)
5. 如何获取 Arborascend
6. 常见错误
7. 相关页面链接
8. FAQ

**已确认（L2，PC Gamer）：**
- 任务: "The Mysterious Bay"
- 位置: Moonlit Pines, Luna 的 seed cart 附近
- 挡住 Luna cottage 楼梯西边的 waterfall
- 需要 Arborascend spell
- Arborascend 在 Webb of Wonders (Sabrina) 购买
- 常见错误: 不要先去 Howling Marshes 或 Luna Bay 找

**⚠️ 改写为清单结构，不要复述 PC Gamer 原文。**

---

## 3.9 `/is-moonlight-peaks-worth-it/`

| 字段 | 内容 |
|------|------|
| **Title** | `Is Moonlight Peaks Worth It? — Price, Platforms & What Players Say` |
| **Meta Description** | `Should you buy Moonlight Peaks? Price ($34.99), platforms, Steam rating (Very Positive), gameplay overview, who should buy and who should wait.` |
| **H1** | `Is Moonlight Peaks Worth It?` |
| **目标关键词** | is moonlight peaks worth it |
| **需 FAQ schema** | ✅ |
| **需 Breadcrumb schema** | ✅ |

**页面大纲：**
1. 快速回答（for most cozy farming sim fans, yes — with caveats）
2. 价格与平台
3. Steam 评价快照（引用公开数据，不假装自己测评）
4. 游戏系统概述
5. 适合谁买 / 谁该等
6. 同类游戏
7. FAQ

**⚠️ 风险评估：这是购买决策页，不是评测。**
- 基于 Steam 公开数据 + 社区反馈汇总
- 不写第一人称
- 不假装玩过

---

### P1 - 核心玩法补充（7页）

---

## 3.10 `/money-guide/`

| 字段 | 内容 |
|------|------|
| **Title** | `How to Make Money Fast in Moonlight Peaks — Gold Farming Guide` |
| **Meta Description** | `Best ways to earn coins in Moonlight Peaks: profitable crops by season, keg processing, fishing tips, job board, and what NOT to sell early.` |
| **H1** | `How to Make Money in Moonlight Peaks` |
| **目标关键词** | how to make money moonlight peaks, gold guide, money fast |
| **需 FAQ schema** | ✅ |
| **需 Breadcrumb schema** | ✅ |

**页面大纲：**
1. 赚钱途径排名
2. 加工经济（Keg → 葡萄酿酒，Reddit 玩家验证）
3. 各季节推荐作物
4. Chester 销售箱
5. 任务板
6. 不要早期卖材料
7. FAQ

**内容规则：** 标注社区信息来源（Reddit/LadiesGamers），不编造售价数据。

---

## 3.11 `/gift-guide/`

| 字段 | 内容 |
|------|------|
| **Title** | `Moonlight Peaks Gift Guide — Best Gifts for Every Character` |
| **Meta Description** | `Complete Moonlight Peaks gift guide: loved and disliked gifts for romanceable characters, gift-giving mechanics explained. Updated as community data grows.` |
| **H1** | `Moonlight Peaks Gift Guide` |
| **目标关键词** | moonlight peaks gift guide, best gifts, loved gifts |
| **需 FAQ schema** | ✅ |
| **需 Breadcrumb schema** | ✅ |

**页面大纲：**
1. 送礼机制
2. 角色礼物表格
3. 礼物获取途径
4. FAQ

**⚠️ 大部分角色具体礼物偏好 → 社区数据仍在填充，诚实标注 "TBD" 或 "Community reports suggest..."**

---

## 3.12 `/spells-guide/`

| 字段 | 内容 |
|------|------|
| **Title** | `Moonlight Peaks Spells Guide — Magic, Mana & How to Unlock Spells` |
| **Meta Description** | `How to unlock magic in Moonlight Peaks: spell list with cast patterns, mana system, wand upgrades, and shapeshifting forms. All known spells from Eurogamer's guide.` |
| **H1** | `Moonlight Peaks Spells Guide` |
| **目标关键词** | moonlight peaks spells guide, how to unlock spells |
| **需 FAQ schema** | ✅ |
| **需 Breadcrumb schema** | ✅ |

**页面大纲：**
1. 魔杖获取 + 修复
2. Mana 系统
3. 基础咒语表格
4. 高级咒语
5. 变形系统
6. FAQ

**已确认（L2，Eurogamer）：**
- Aquaflux I / Aborascend I / Ethereal Hands I / Maturio I

---

## 3.13 `/farming-guide/`

| 字段 | 内容 |
|------|------|
| **Title** | `Moonlight Peaks Farming Guide — All Crops, Seasons & Profit Tips` |
| **Meta Description** | `Complete Moonlight Peaks farming guide: crop list by season, grow times, seed prices, magic crops (Aquaflux), trees, herbs, and which crops to plant for profit.` |
| **H1** | `Moonlight Peaks Farming Guide` |
| **目标关键词** | moonlight peaks farming guide, crops, seeds |
| **需 FAQ schema** | ✅ |
| **需 Breadcrumb schema** | ✅ |

**页面大纲：**
1. 耕种基础
2. 全季节作物表格（53 seeds，Eurogamer 数据）
3. 魔法作物 / 树木 / 草药 / 蘑菇
4. 最佳利润推荐
5. FAQ

**内容规则：** 改写 Eurogamer 数据表格为原创格式，不要直接复制原文的表格排版和措辞。

---

## 3.14 `/fishing-guide/`

| 字段 | 内容 |
|------|------|
| **Title** | `Moonlight Peaks Fishing Guide — Rod, Fish Locations & Tips` |
| **Meta Description** | `How to get the fishing rod from Noel, all known fish species with spawn locations, rod upgrades, and fishing mechanics tips.` |
| **H1** | `Moonlight Peaks Fishing Guide` |
| **目标关键词** | moonlight peaks fishing guide, how to fish |
| **需 FAQ schema** | ✅ |
| **需 Breadcrumb schema** | ✅ |

**页面大纲：**
1. 鱼竿获取
2. 钓鱼操作
3. 鱼竿升级
4. 钓鱼技巧
5. 鱼类表格
6. FAQ

---

## 3.15 `/steam-deck/`

| 字段 | 内容 |
|------|------|
| **Title** | `Moonlight Peaks Steam Deck — Performance, Settings & Known Issues` |
| **Meta Description** | `How Moonlight Peaks runs on Steam Deck: performance notes, recommended settings, battery life, and known issues like long loading times.` |
| **H1** | `Moonlight Peaks on Steam Deck` |
| **目标关键词** | moonlight peaks steam deck |
| **需 FAQ schema** | ✅ |
| **需 Breadcrumb schema** | ✅ |

**页面大纲：**
1. 兼容性状态
2. 性能表现
3. 推荐设置
4. 已知问题
5. FAQ

**已确认（L2，Steam Deck HQ）：** 游戏已评测，有已知长加载时间问题
**不确定：** Steam Deck Verified 状态 → TBD

---

## 3.16 `/games-like-moonlight-peaks/`

| 字段 | 内容 |
|------|------|
| **Title** | `10 Games Like Moonlight Peaks — Similar Cozy Farming Sims` |
| **Meta Description** | `Love Moonlight Peaks? Try Stardew Valley, Fields of Mistria, Wylde Flowers, Coral Island and more cozy farming sims with romance, magic and crafting.` |
| **H1** | `Games Like Moonlight Peaks` |
| **目标关键词** | games like moonlight peaks, similar games |
| **需 FAQ schema** | ✅ |
| **需 Breadcrumb schema** | ✅ |

**页面大纲：**
1. 简短 intro
2. 对比表：名称 / 平台 / 相似点 / 不同点
3. 每个游戏 2-3 句推荐
4. FAQ

---

### P2 - 首页（最后做）

---

## 3.17 `/` (首页)

| 字段 | 内容 |
|------|------|
| **Title** | `Moonlight Peaks Guide — Romance, Gifts, Money, Spells & Beginner Tips` |
| **Meta Description** | `Unofficial Moonlight Peaks guide collection: romance options, best gifts, money tips, spell list, beginner walkthrough, Switch & PS5 info.` |
| **H1** | `Moonlight Peaks Guide` |
| **目标关键词** | moonlight peaks, moonlight peaks guide |
| **需 FAQ schema** | ✅ |
| **需 Breadcrumb schema** | ✅ |

**页面大纲：**
1. Hero 区（h1 + 副标题 + 信息卡）
2. 导航网格 6 个核心入口
3. 快速 FAQ
4. 底部 FAQ（3 个）
5. 页脚 + Not affiliated disclaimer

**额外 Schema 要求：** WebSite + Organization JSON-LD

---

## 4. 页面优先级汇总

| 优先级 | 页面 | 理由 |
|--------|------|------|
| P0 | `/switch/` | 高流量平台确认词 |
| P0 | `/ps5/` | 高搜索量平台确认词 |
| P0 | `/multiplayer/` | PAA 精准回答 |
| P0 | `/beginner-guide/` | 新玩家第一站 |
| P0 | `/romance-guide/` | "is there romance" 精准匹配 |
| P0 | `/samael-romance/` | PC Gamer 验证卡点词 |
| P0 | `/treasure-hunt-clues/` | PC Gamer 验证卡点词 |
| P0 | `/fallen-tree/` | PC Gamer 验证卡点词 |
| P0 | `/is-moonlight-peaks-worth-it/` | 购买决策（非评测） |
| P1 | `/money-guide/` | 核心玩法刚需 |
| P1 | `/gift-guide/` | 恋爱系统配套 |
| P1 | `/spells-guide/` | 特色系统 |
| P1 | `/farming-guide/` | 核心玩法 |
| P1 | `/fishing-guide/` | 核心玩法 |
| P1 | `/steam-deck/` | 硬件长尾 |
| P1 | `/games-like-moonlight-peaks/` | 发现型流量 |
| P2 | `/` | 最后做（内容汇总后首页自动获取权重） |

---

## 5. 统一 SEO Checklist（每页强制）

```
[ ] <title> 50-60 字符，核心关键词前置
[ ] <meta description> 120-160 字符，含关键词
[ ] <link rel="canonical"> 指向自身 URL（禁止全站指向首页）
[ ] <meta name="robots" content="index,follow">
[ ] og:title / og:description / og:type: article / og:locale: en_US
[ ] og:image URL 可访问，1200x630
[ ] twitter:card = summary_large_image
[ ] twitter:title / twitter:description / twitter:image
[ ] BreadcrumbList JSON-LD schema
[ ] FAQPage JSON-LD schema（每页底部 1-2 FAQ）
[ ] Article JSON-LD schema
[ ] <html lang="en">
[ ] <meta name="viewport" content="width=device-width, initial-scale=1">
[ ] 所有 <img> 有 alt
[ ] 站内链接不加 nofollow，站外 rel="noopener noreferrer nofollow"
[ ] h1 与 title 语义一致
[ ] 数据用 <table> 标签
[ ] sitemap.xml 包含所有路由 + lastmod
[ ] robots.txt 允许抓取所有页面
[ ] 面包屑导航（Home > Page）
[ ] 首页额外：WebSite + Organization JSON-LD
```

---

## 6. 内部链接策略

- 首页导航网格 → 6 个核心 P0/P1 入口
- 每页底部 "Related Guides"（2-3 个链接）
- 交叉链接网络：
  - `/romance-guide/` ↔ `/samael-romance/` ↔ `/gift-guide/`
  - `/farming-guide/` ↔ `/money-guide/`
  - `/beginner-guide/` ↔ `/farming-guide/` ↔ `/fishing-guide/`
  - `/switch/` ↔ `/ps5/` ↔ `/steam-deck/`
  - `/fallen-tree/` ↔ `/samael-romance/` ↔ `/spells-guide/`（Arborascend）
- 页脚：全部 17 页入口

---

## 7. 设计风格

- 深色 "cozy gothic" — 深紫 `#2D1B4E` + 暗蓝 + 柔和金色点缀
- 数据表暗色背景 + hover 行高亮
- 移动端优先
- 卡片式导航
- 工具型站点，不过度花哨

---

## 8. 风险提醒 + 禁止事项

1. **不是官方站** — 页脚 "Not affiliated with Little Chicken / XSEED Games"
2. **不做假评测** — worth-it 页基于 Steam 公开数据，不写第一人称
3. **不硬编数据** — 未确认的写 "TBD" / "Currently unclear" / "Community reports suggest..."
4. **不硬编角色/礼物/作物/鱼类**
5. **不与 wiki.gg 做纯数据库正面对抗**
6. **Orlock 后置** — 等 GSC 出现 "orlock moonlight peaks" 精确查询
7. **不确定信息诚实标注**
8. **不大段改写/近似复述** PC Gamer、IGN、Eurogamer、GameRant 原文段落
9. **不确定的时间用 "usually" / "around"** — 不写 "Day 5 exactly"
10. **价格标注 region/sale may vary**
11. **不在任何 meta description 里写死不更新的事实（如固化价格、写死角色数量）**

---

## 9. 数据源优先级表

| 级别 | 来源 | 使用规则 |
|------|------|---------|
| **L1 Official** | Steam、Nintendo.com、moonlightpeaks.com、Google Play | 平台、价格、发布日期、模式、文件大小优先用官方源 |
| **L2 Guide** | PC Gamer、IGN、Eurogamer、GameRant、LadiesGamers | 任务步骤可用，改写为原创结构，不复述原文 |
| **L3 Community** | Reddit r/MoonlightPeaks、Discord、Steam discussions、Facebook | 标注 "community-reported" / "TBD"，不能作官方事实 |

---

## 10. 后续扩展规则

- 7-14 天观察 GSC
- "orlock moonlight peaks" 精确查询出现 → 开 `/characters/orlock/`
- 新任务/地点卡点词出现 → 加单页
- "moonlight peaks ios" 出现搜索量 → 开 `/ios/`
- 无信号不盲目堆页
- P0 GSC 展示良好 → 逐步上 P2/P3
