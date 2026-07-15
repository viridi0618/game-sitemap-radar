# Witchbrook Pre-Launch Guide — 需求文档

> 日期：2026-07-15
> 站点类型：预发布信息型 + 任务解释型 guide hub
> 评级：A-
> 首批页面：16 页
> 状态：老大已审核，修 6 点后进入 Codex 框架阶段
> 最近修改：2026-07-15（老大审核后）
> **Template: Moonlight Peaks guide site template**
> **Domain: witchbrookguide.com** (待确认)
> **Site name: Witchbrook Guide**

---

## IMPORTANT — Template Requirement

This Witchbrook project must be built by adapting the existing Moonlight Peaks guide site template.
Use the Moonlight Peaks project as the visual and engineering base:
- same overall page layout
- same dark cozy guide style
- same GuideCard / GuidePage structure
- same SEO/schema patterns
- same data-driven guides.ts approach
- same image field structure
- same sitemap / robots approach
- same Header / Footer / card-based navigation style

Do not rebuild from scratch.
Do not create a new design system.
Do not switch framework or routing style.
Do not replace the existing Moonlight-style components unless a small adaptation is necessary.

Adapt the branding, colors, copy, navigation, metadata, and content from Moonlight Peaks to Witchbrook.
The final site should feel like a Witchbrook-themed version of the Moonlight Peaks guide site, not a generic new wiki.

Moonlight 的结构 + Witchbrook 的品牌。

## Cleanup Checklist (Remove All Moonlight Peaks Traces)

Remove all Moonlight Peaks-specific content, metadata, routes, images, schema names, footer references, and copy unless intentionally reused as a comparison link.

After adaptation, the site must NOT contain:
- "Moonlight Peaks Guide" as site name
- `moonlightpeaksguide.wiki` as canonical URL
- Moonlight-specific metadata / OG images
- Moonlight-specific guide routes
- Moonlight image credits or screenshot URLs
- Moonlight schema names

Exception: `/games-like-witchbrook/` may mention Moonlight Peaks as a similar game — that is content, not template residue.

---

## PART 1: PAGE_SPEC（页面定义）

### P0 — 搜索流量页（9 页）

| # | slug | title (SEO) | meta description | H1 | 目标关键词 |
|---|------|-------------|------------------|----|-----------|
| 1 | / | Witchbrook Guide: Release Date, Platforms, Co-op & Gameplay | Witchbrook guide for release date, Switch, Xbox, PS5 status, multiplayer, co-op, classes, romance, Mossport, and gameplay details. | Witchbrook Guide | witchbrook, witchbrook guide |
| 2 | /release-date | Witchbrook Release Date: When Is Witchbrook Coming Out? [2026] | Witchbrook release date update: planned for 2026 on PC, Nintendo Switch, Switch 2, and Xbox. No exact date yet. Here's everything we know. | Witchbrook Release Date | witchbrook release date, when is witchbrook coming out |
| 3 | /platforms | Witchbrook Platforms: PC, Switch, Switch 2, Xbox & PS5 Status | Witchbrook confirmed platforms: PC (Steam), Nintendo Switch, Nintendo Switch 2, Xbox. PS5 and PS4 status explained. No PlayStation version announced. | Witchbrook Platforms | witchbrook platforms |
| 4 | /switch | Witchbrook on Nintendo Switch: Release, Features & What We Know | Witchbrook is confirmed for Nintendo Switch in 2026. Details on Switch version, features, and how it compares to other platforms. | Witchbrook on Nintendo Switch | witchbrook switch |
| 5 | /switch-2 | Witchbrook on Nintendo Switch 2: Confirmed, Day-1 Launch | Witchbrook confirmed for Nintendo Switch 2, launching day-1 alongside Switch, Xbox, and PC. New features and footage from Nintendo Direct. | Witchbrook Switch 2 | witchbrook switch 2 |
| 6 | /xbox | Witchbrook on Xbox: Series X|S, Xbox One, Co-op & Features | Witchbrook is confirmed for Xbox One and Xbox Series X|S. See Xbox store features, online co-op, cross-platform support, Smart Delivery, achievements, and Game Pass status. | Witchbrook Xbox | witchbrook xbox |
| 7 | /ps5 | Is Witchbrook Coming to PS5 or PS4? PlayStation Status Explained | Witchbrook is NOT currently announced for PS5 or PS4. Confirmed platforms are PC, Nintendo Switch, Switch 2, and Xbox. Other platforms TBD. | Witchbrook PS5 | witchbrook ps5, witchbrook ps4 |
| 8 | /multiplayer | Witchbrook Multiplayer & Co-op: Online Play, Player Count & Split-Screen | Witchbrook supports up to 4-player online co-op. No split-screen. Cross-platform multiplayer on Xbox. All Witchbrook multiplayer and co-op details in one guide. | Witchbrook Multiplayer | witchbrook multiplayer, witchbrook co op, witchbrook online co-op |
| 9 | /steam | Witchbrook on Steam: Wishlist, Features & System Requirements | Witchbrook Steam page is live. Wishlist now, see system requirements (Windows 10+, quad-core, 8GB RAM, 4GB VRAM, 2GB storage), and Steam features. | Witchbrook Steam | witchbrook steam |

### P1 — 玩法页（4 页）

| # | slug | title (SEO) | meta description | H1 | 目标关键词 |
|---|------|-------------|------------------|----|-----------|
| 10 | /classes | Witchbrook Classes & Subjects: What We Know So Far | Witchbrook classes and college subjects explained, including confirmed magical study areas, assignments, exams, spells, and what remains unknown before release. | Witchbrook Classes & Subjects | witchbrook classes |
| 11 | /assignments | Witchbrook Assignments: How College Tasks, Merits & Exams Work | Witchbrook assignments explained: how to complete college tasks, earn merits, spend them at the college shop, and qualify for exams. | Witchbrook Assignments | witchbrook assignments |
| 12 | /witchy-business | Witchbrook Witchy Business: Start Your Own Magic Shop | Witchbrook witchy business system explained: start your magic business, fulfill orders, use your moped or broom for deliveries, and sell at the Sunday market. | Witchbrook Witchy Business | witchbrook business, witchbrook money |
| 13 | /romance | Witchbrook Romance: Characters, Relationships & Dating Guide | Witchbrook romance guide with revealed dating details, relationship mechanics, confirmed character reveals, and what remains unknown before release. | Witchbrook Romance | witchbrook romance |

### P2 — SEO 拓展页（3 页）

| # | slug | title (SEO) | meta description | H1 | 目标关键词 |
|---|------|-------------|------------------|----|-----------|
| 14 | /witchbrook-vs-stardew-valley | Witchbrook vs Stardew Valley: Similarities, Differences & Which to Play | Witchbrook vs Stardew Valley comparison: both are pixel-art life sims from Chucklefish, but Witchbrook adds magic school, co-op, and witch business. | Witchbrook vs Stardew Valley | witchbrook vs stardew valley, witch stardew valley |
| 15 | /games-like-witchbrook | 10 Games Like Witchbrook: Cozy Magic School & Witch Life Sims | Looking for games like Witchbrook? Discover similar magic school sims, witch life sims, and cozy RPGs to play while you wait for the 2026 release. | Games Like Witchbrook | games like witchbrook |
| 16 | /faq | Witchbrook FAQ: Release, Platforms, Multiplayer, Romance & More | Frequently asked questions about Witchbrook: release date, platforms, multiplayer, co-op, romance, classes, business, and everything we know so far. | Witchbrook FAQ | witchbrook faq |

---

## PART 2: SOURCE_LOG（来源记录）

### L1 — Official Sources ✅

| # | Source | URL | Data Used |
|---|--------|-----|-----------|
| L1-1 | Witchbrook Official Site | https://www.witchbrook.com/ | FAQ: release window, platforms, languages, developers, community links |
| L1-2 | Witchbrook Official Blog — "Life at Witchbrook" (June 2026) | https://www.witchbrook.com/dev-blog-life-at-witchbrook/ | Classes, assignments, knowledge, exams, spells, wellbeing, graduation, covenmate stories, witchy business, Sunday market, free time |
| L1-3 | Steam Store Page | https://store.steampowered.com/app/1846700/Witchbrook | Features: Single-player, Online Co-op, Steam Achievements, Steam Cloud. System requirements. Languages. Game description. |
| L1-4 | Xbox Store Page | https://www.xbox.com/en-US/games/store/witchbrook/9P54Q8W3TF4W | Xbox features: 4K, 120fps, Smart Delivery, cross-platform, Xbox achievements, cloud saves, 60fps+, Optimized for Series X|S |
| L1-5 | Chucklefish Blog — Switch 2 Announcement (Feb 2025) | https://chucklefish.org/blog/witchbrook-is-coming-to-nintendo-switch-2/ | Switch 2 day-1 launch confirmed, Nintendo Direct footage |
| L1-6 | First Look Trailer (YouTube) | https://www.youtube.com/watch?v=TIKSGazNOqg | Gameplay footage, visual references |
| L1-7 | Official Press Kit | https://chucklefish.org/presskit/ | Press screenshots for imagery |
| L1-8 | Witchbrook Oracle Newsletter Signup | https://www.witchbrook.com/ | Newsletter subscription link |

### L2 — Media Sources ✅

| # | Source | URL | Data Used |
|---|--------|-----|-----------|
| L2-1 | RPG Site — Delay to 2026 | https://www.rpgsite.net/news/18709-witchbrook-release-date-delayed-2026-chucklefish | Delay announcement Oct 15, 2025 |
| L2-2 | GamesRadar — "Everything we know" | https://www.gamesradar.com/games/simulation/witchbrook-guide | Overview of confirmed features |
| L2-3 | Co-Optimus | https://www.co-optimus.com/game/16682/switch-2/witchbrook.html | Co-op details: online only, no split-screen |
| L2-4 | Gamepressure — PS5/PS4 status | https://www.gamepressure.com/newsroom/when-to-expect-witchbrook-on-playstation-ps4-ps5-and-xbox-console/z37c18 | PlayStation platform uncertainty |

### L3 — Community Sources ⚠️

| # | Source | URL | Data Used | Note |
|---|--------|-----|-----------|------|
| L3-1 | Reddit r/Witchbrook | https://www.reddit.com/r/Witchbrook/ | Community sentiment, PS5 discussion, co-op speculation | Only for sentiment, not facts |
| L3-2 | Steam Discussions — Co-op | https://steamcommunity.com/app/1846700/discussions/0/651441305622190948 | Dev response: "No plans for split screen" | Dev comment = L2 quality within L3 platform |
| L3-3 | NiaMeowDB | https://meowdb.com/db/witchbrook | Character catalog, area catalog, class catalog | Fan-compiled, cross-referenced with official sources |

### ⚠️ 冲突/不确定项

| # | Issue | Source A | Source B | 处理方式 |
|---|-------|----------|----------|----------|
| U-1 | Original target "Winter 2025" | RPG Site + Reddit history | Now 2026 (official FAQ) | 使用 2026，提及曾推迟 |
| U-2 | PS5/PS4 status | Official FAQ: "Other platforms TBD" | Community: "No PS5 announced" | 写成 "Not announced, other platforms TBD" |
| U-3 | Exact number of romance candidates | Steam: "colourful cast of datable characters" | NiaMeowDB: "5 confirmed" | 写 "multiple romance candidates revealed so far include Hana, Pip, Eli, Cormac" |
| U-4 | Split-screen co-op | Dev on Steam: "No plans for split screen" | — | 明确写 "Online only, no split-screen" |
| U-5 | Exact release date | Official: "won't share a specific date until super sure" | — | 写 "No exact date announced, 2026 window" |

---

## PART 3: CONTENT_DATA（页面内容数据）

### 3.1 站点通用数据

```yaml
game:
  name: Witchbrook
  developer: Chucklefish (London, UK) co-developed with Robotality (Hamelin, Germany)
  publisher: Chucklefish
  genre: Life simulation, Social RPG, Indie
  engine: Halley (custom, by Chucklefish CTO Rodrigo)
  composer: David Fenn
  art_director: Steph
  modes: Single-player, Online co-op (1-4 players)
  release_window: 2026
  release_status: No exact date — "won't share a specific date until we're super sure"
  esrb: Teen (Suggestive Themes, Users Interact)
  languages: English, French, German, Spanish (Spain), Brazilian Portuguese, Japanese, Simplified Chinese, Traditional Chinese (+ more TBD)
  steam_app_id: 1846700
  original_target: Winter 2025 (delayed Oct 15, 2025)
  development_approach: Zero-crunch studio policy

setting:
  location: Mossport — a vibrant seaside city
  main_location: Witchbrook College
  player_home: Aunt's cottage (inherited), woodland setting with garden
  seasons: Yes — Winter, Spring (confirmed to have visual/event changes)
  npc_system: Every character has unique daily schedule, seasonal routines, events
  atmosphere: Cozy, magical, Ghibli-inspired (Kiki's Delivery Service, Tiffany Aching)

platforms:
  confirmed:
    - Steam (PC, Windows 10+, 64-bit)
    - Nintendo Switch
    - Nintendo Switch 2 (day-1 launch with all other platforms)
    - Xbox One
    - Xbox Series X|S
  not_announced:
    - PS5: "Other platforms TBD" per official FAQ
    - PS4: Not announced
    - Mac: Not announced
    - Mobile: Not announced
  xbox_features:
    note: "The Xbox store currently lists these as capabilities. Actual performance may vary by console, display, and final release build."
    store_listed:
      - 4K Ultra HD
      - 120 fps
      - 60 fps+
      - Smart Delivery
      - Optimized for Xbox Series X|S
      - Xbox achievements
      - Xbox cloud saves
      - Xbox cross-platform multiplayer
      - Xbox cross-platform co-op
      - Xbox Live Cross-Gen Multiplayer
      - Variable Refresh Rate
    game_pass_status: "Not confirmed. The Xbox store mentions that online multiplayer on console requires a Game Pass subscription (Core/Ultimate), but that does not mean Witchbrook is included in Game Pass."

steam_features:
  - Steam Achievements
  - Steam Cloud
  - Single-player
  - Online Co-op

system_requirements:
  minimum:
    os: Windows 10+, 64-bit only
    processor: Quad-core CPU
    memory: 8 GB RAM
    graphics: DX11 compatible, 4 GB VRAM
    directx: Version 11
    storage: 2 GB
  recommended: 64-bit processor and OS (no further details listed)

multiplayer:
  type: Online co-op only (no local/split-screen)
  players: 1-4
  cross_platform: Confirmed for Xbox (cross-platform multiplayer, cross-platform co-op)
  gameplay_in_coop: "Race on brooms through the park, hone spellcrafting, or just hang out in Mossport"
  dev_quote: "No plans for split screen, but we'll be talking more about how our co-op works at a later date!"

gameplay_systems:
  classes_notes: "The following subject areas are referenced across official dev blogs and store pages. Not all may be formal named 'classes' — treat them as confirmed magical study areas until the full curriculum is revealed."
  classes:
    - Alchemy: teas → salves → potions. Client-facing. Hands-on.
    - Divination: tarot (day), constellations (night). Held in Observatory/Astronomy Tower.
    - Herbology: magical plant cultivation, ties into potion brewing.
    - Spell-casting: hands-on. Unlock spells after each exam via Prof. Carlyle. Guidance spells, broom flight.
    - Broom-flying: indoor beginner → outdoor flight. Earn license.
    - Arcane Arts: advanced, exam-gated (Semester 1+2 pass required). Rituals and demons. Dedicated classroom.
  assignments:
    description: Weekly tasks posted by the college. Consult residents, diagnose solutions, use library.
    rewards: College merits → spend in college shop. Thank-you gifts from NPCs.
    purpose: Merits enable exam entry.
  knowledge_collection:
    description: Encyclopedia tracking everything you learn. Unlock entries through discovery and practice.
    example: Find herb → unlock description. Grow it multiple times → unlock growth time info.
    library: Borrow books from school library (must return on time), gradually rely on own knowledge.
  exams:
    description: Tests on knowledge categories relevant to the exam topic.
    example: "Magical medicine exam tests herbal tea, salve, and Herbology knowledge categories."
    passing: Required to advance to next grade, unlocking new classes, spells, areas.
    study_groups: Coven members test you with mock exams.
    grades: Depends on knowledge accumulated in tested categories.
  spells:
    description: Learned one-on-one from Professor Carlyle after each completed exam.
    wand: Basic telekinesis from the start — move objects, furniture.
    examples: Guidance spells (track rare ingredients), broom flight, "large variety of useful spells."
  wellbeing:
    description: Wellness system tracking self-care.
    positive_triggers: Petting dog, walking in nature, talking with friend.
    negative_triggers: Staying up late, upsetting friend.
    daily_tally: Events tallied at end of day.
    bonuses: Increased income, better deals, gifts, relationship benefits, better exam performance.
  witchy_business:
    description: Start your own witch business, fulfill orders for Mossport townsfolk.
    delivery: Moped (early) or broom (after license).
    relationships: Higher relationship with clients → perks and business upgrades.
    sunday_market: Sell goods from a stall, negotiate deals with townsfolk.
  graduation:
    description: Complete set of grade exams to advance. Many stay as postgrads to fill knowledge collection and improve grades.
  coven_system:
    description: You live and study with a coven of witches. Coven leader: Professor Carlyle.
    stories: Each covenmate has unique visual novel-style story that unlocks with relationship level.
    free_time: Build relationships, dates, fashion, interior design, clubs, cooking, gardening, festivals.

romance:
  general_notes: "Revealed so far. Not all candidates confirmed with L1 official sources — treat as 'reported / revealed' not 'full confirmed roster.'"
  confirmed_candidates:
    - Hana Sato: First dateable character revealed. Tied to Calico fashion shop. Upbeat social energy.
    - Pip: Witch-mechanic, harbour workshop, chaotic inventiveness. Magic-meets-machinery.
    - Cormac: Gifted artist, The Briny Brush near Parasol Sands. "Black sheep" type.
    - Eli: Oracle editor, School Shop connection. Information-network hook.
  mechanics_known: Build relationships, go on dates, pick gifts for romantic dates (from Steam description).
  not_known: Exact gift preferences, heart-event steps, romance route walkthroughs.

characters:
  named_confirmed:
    - Fable: Cottage familiar (greedy, has a plan for your business)
    - Professor Carlyle: Coven head, teaches spells one-on-one
  note: Hundreds of citizens with routines, seasons, events. Full list TBD post-launch.

mossport_areas:
  known_locations:
    - Witchbrook College (Library, Alchemy Lab, Observatory/Astronomy Tower, Arcane Arts classroom, College shop, hallways)
    - Calico (clothing shop at 8 Whitecap Esplanade)
    - The Briny Brush (near Parasol Sands)
    - School Shop
    - Docklands (Pip's garage/workshop)
    - Sunday market
    - Player cottage (woodland, with garden)
    - Arcade
    - Pub
  note: 44+ catalogued areas per NiaMeowDB (fan source, not fully verified). Not writing exhaustive list pre-launch.

vs_stardew_valley:
  similarities:
    - Pixel art aesthetic
    - Life sim structure (farming/gardening, relationships, fishing, crafting)
    - Chucklefish published Stardew Valley (coincidence — Witchbrook is developed by Chucklefish themselves)
    - Seasonal events and festivals
    - Relationship building and romance
    - Town with shops and characters with schedules
  differences:
    - Magic school setting vs farm setting
    - Up to 4-player online co-op (Stardew supports co-op but Witchbrook designed for it from day 1)
    - No traditional farming — gardening exists but business is the economic core
    - Class/exam progression system
    - Witch business model (fulfilling orders) vs Stardew's sell-crops model
    - Visual novel-style character stories
    - Broom/moped traversal vs horse/walking

games_like_witchbrook:
  - Stardew Valley (farming life sim, same publisher)
  - Moonlight Peaks (cozy supernatural life sim, upcoming)
  - Little Witch in the Woods (witch-in-training, pixel art)
  - Wylde Flowers (witch life sim with farming, fully voiced)
  - Sun Haven (magic farming RPG, multiplayer)
  - Potion Permit (alchemy-focused town sim)
  - Kitaria Fables (farming action RPG with magic)
  - Fields of Mistria (retro-inspired farming RPG, early access)
  - Spellcaster University (magic school management)
  - Hogwarts Legacy (AAA magic school RPG, different genre but same fantasy)
```

### 3.2 页面要点大纲

**`/` — 首页**
- 一句话总结 Witchbrook 是什么
- 关键信息速览（release/platform/players/price TBD）
- 链接到子页面
- 嵌入 Steam 预告片
- Newsletter signup CTA
- Steam wishlist CTA

**`/release-date/`**
- 当前状态：Planned for 2026, no exact date
- 历史：原计划 Winter 2025 → Oct 15 2025 宣布推迟
- 开发者说法："won't share a specific date until we're super sure"
- 原因：平台提交、bug、本地化、移植、打磨 — 多重因素
- playtest 进行中（第一个学年就要 40-50 小时）
- 语言本地化进行中，可能比已公布的 8 种更多

**`/platforms/`**
- 确认平台表格
- PS5/PS4 状态："Other platforms TBD"
- 各平台功能对比
- FAQ 嵌入

**`/switch/` — `/switch-2/` — `/xbox/` — `/ps5/` — `/steam/`**
- 每个平台单独页面，详述该平台特性
- PS5 页面：明确写"not announced" + 引导到 platforms 页

**`/multiplayer/`**
- 1-4 人在线合作
- 跨平台确认（Xbox）
- 无分屏（开发者确认）
- Co-op 能做什么：竞速、法术练习、闲逛

**`/classes/`**
- 6 门课简介
- 解锁条件（Arcane Arts 需要考试）
- 在哪里上课

**`/assignments/`**
- 如何接任务 → 完成 → 得奖励 → 解锁考试

**`/witchy-business/`**
- 商业系统全流程
- moped vs broom 配送
- Sunday market

**`/romance/`**
- 4 个已确认候选人简介
- 已知约会机制
- 强调"更多信息等发售"

**`/witchbrook-vs-stardew-valley/`**
- 相似点和差异对比表格
- 不踩任何一方，客观比较

**`/games-like-witchbrook/`**
- 10 款类似游戏 + 简短推荐理由

**`/faq/`**
- 整合所有常见问题

---

## PART 4: 内容红线 + Codex 禁止事项

### ✅ 可以写
- 官方 FAQ 已确认的信息
- Steam/Xbox 商店页功能标签
- 开发者博客中描述的系统
- 开发者社交媒体回复
- 公告过的角色名和简介
- "planned" / "confirmed so far" / "officially listed" 措辞
- 来源标注
- "we'll update this page when more is revealed"

### ❌ 禁止写
- best gifts / gift preferences
- all characters list / full NPC catalog
- all spells list / spell names beyond what's confirmed
- all recipes / potion recipes
- exam answers / study guides
- class tier list / class ranking
- business profit calculator
- map locations (beyond named areas from official sources)
- full romance guide / romance walkthrough
- character schedules / routines
- fabricated release dates or price estimates
- first-person reviews pretending to have played

### 📝 措辞规范
- ❌ "You can romance 5 characters"
- ✅ "At least 4 romance candidates have been officially revealed: Hana, Pip, Eli, and Cormac"
- ❌ "Witchbrook releases in Q3 2026"
- ✅ "Witchbrook is planned for release in 2026. No exact date has been announced."
- ❌ "The game features a 40-hour campaign"
- ✅ "According to the dev blog, playtesting the first in-game year takes around 40-50 hours depending on playstyle"

---

## PART 5: 内部链接网络

```
/ → 所有子页面
/release-date/ → /platforms/
/platforms/ → /switch/, /switch-2/, /xbox/, /ps5/, /steam/
/switch/ → /switch-2/, /platforms/
/switch-2/ → /switch/, /platforms/
/xbox/ → /multiplayer/, /platforms/
/ps5/ → /platforms/
/multiplayer/ → /platforms/, /switch/, /xbox/, /steam/
/steam/ → /platforms/, /release-date/
/classes/ → /assignments/, /witchy-business/
/assignments/ → /classes/, /exams/(future)
/witchy-business/ → /classes/
/romance/ → /characters/(future)
/faq/ → 所有子页面
/witchbrook-vs-stardew-valley/ → /games-like-witchbrook/
/games-like-witchbrook/ → /witchbrook-vs-stardew-valley/
```

---

## PART 6: Codex 交付要求

### 技术栈
- Next.js static export, adapted from the existing Moonlight Peaks guide site template.
- TypeScript
- Tailwind CSS

The Witchbrook site should reuse the Moonlight Peaks template architecture and visual style:
- data-driven guide pages
- GuideCard image/card layout
- GuidePage hero layout
- dark cozy theme
- schema helpers
- site-config pattern
- sitemap/robots pattern
- SEO validation scripts where applicable

### 数据架构
```ts
// src/data/guides.ts
export interface Guide {
  slug: string;
  title: string;        // <title> tag
  metaDescription: string;
  h1: string;
  intent: string;
  priority: 'P0' | 'P1' | 'P2';
  sections: Section[];  // content structure
  faq?: FAQ[];          // structured FAQ items
  internalLinks: string[];
}

export interface Section {
  heading: string;
  content: string;      // raw text — 龙虾 fill in later
  sourceLevel: 'L1' | 'L2' | 'L3';
  sourceUrl?: string;
}
```

### Sitemap & Robots 生成方式
- 使用 Next.js 动态路由：`src/app/sitemap.ts` 从 `guides.ts` 自动读取所有 slug 生成 sitemap
- 使用 Next.js 动态路由：`src/app/robots.ts` 自动生成 robots
- 不要使用手动编辑的 `public/sitemap.xml`（除非现有模板本身就是静态 sitemap）
- 以后新增页面不需要手改 sitemap

### SEO Checklist（Codex 必须全过）
1. 每个页面 unique title（50-60 字符）
2. 每个页面 unique meta description（120-160 字符）
3. Canonical URL 正确
4. OG tags 完整（og:title, og:description, og:image, og:url, og:type）
5. Twitter card (summary_large_image)
6. BreadcrumbList schema
7. Article schema（内容页）
8. FAQ schema（FAQ 页 + 各页底部 FAQ）
9. WebSite schema（首页）
10. Sitemap 完整
11. robots.txt 配置
12. Viewport meta tag
13. 所有 img 有 alt
14. 出站链接 rel="nofollow noopener noreferrer"
15. 无 broken internal links
16. NEXT_PUBLIC_SITE_URL 环境变量已设置

---

## 附录：项目文件结构

```
witchbrook-guide/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── [slug]/page.tsx
│   ├── components/
│   │   ├── GuideCard.tsx
│   │   ├── GuidePage.tsx
│   │   ├── Footer.tsx
│   │   └── Header.tsx
│   ├── data/
│   │   ├── guides.ts          ← 龙虾编辑
│   │   ├── faq.ts             ← 龙虾编辑
│   │   └── navigation.ts      ← 龙虾编辑
│   └── lib/
│       └── site-config.ts
├── public/
│   └── images/
├── next.config.ts
├── vercel.json
├── src/app/sitemap.ts (auto-generated from guides.ts)
├── src/app/robots.ts (auto-generated)
└── robots.txt (fallback, if template requires)
```

---

## 下一步

1. **老大审核** → 确认/修改 PAGE_SPEC + CONTENT_DATA + SOURCE_LOG
2. **Codex 搭框架** → 生成 16 页路由 + SEO 骨架 + 数据文件结构
3. **龙虾填充内容** → 在 guides.ts 中填入有「人味儿」的内容
4. **老大审核** → 内容终审
5. **上线** → Vercel 部署 + DNS + GSC + AdSense
