// Generated from ../manifest.json; do not edit by hand.
window.CONCEPT_MANIFEST = {
  "version": "0.4",
  "game_name": "訴訟之神之路",
  "scope": "單張動作插畫與男女主角版本",
  "presentation": "single_static_image",
  "art_direction": "延續PDF概念圖的精緻2D插畫，平滑輪廓與自然材質；每個動作一張完整場景，無逐格或自動播放。",
  "excluded_actions": [
    "job_hop"
  ],
  "variants": [
    {
      "id": "male",
      "title": "男性主角"
    },
    {
      "id": "female",
      "title": "女性主角"
    }
  ],
  "audio": "不含音樂與其他音訊",
  "actions": [
    {
      "id": "breakfast",
      "title": "吃早餐",
      "category": "日常行動",
      "description": "在辦公桌前吃早餐，暫時享受安靜的一刻。",
      "availability": "09:00；額外動作，不推進時段",
      "images": {
        "male": "action_stills/male/breakfast.png",
        "female": "action_stills/female/breakfast.png"
      },
      "default_variant": "male"
    },
    {
      "id": "write_brief",
      "title": "寫書狀",
      "category": "日常行動",
      "description": "俯身書寫書狀，桌邊放著待處理的卷宗。",
      "availability": "09:00／13:00／16:00",
      "images": {
        "male": "action_stills/male/write_brief.png",
        "female": "action_stills/female/write_brief.png"
      },
      "default_variant": "male"
    },
    {
      "id": "slack",
      "title": "摸魚",
      "category": "日常行動",
      "description": "靠在椅背上伸懶腰，讓腦袋休息一下。",
      "availability": "09:00／16:00",
      "images": {
        "male": "action_stills/male/slack.png",
        "female": "action_stills/female/slack.png"
      },
      "default_variant": "male"
    },
    {
      "id": "interview",
      "title": "面試新員工",
      "category": "日常行動",
      "description": "查看履歷，專心聆聽候選人介紹自己。",
      "availability": "開業律師；09:00／13:00／16:00",
      "images": {
        "male": "action_stills/male/interview.png",
        "female": "action_stills/female/interview.png"
      },
      "default_variant": "male"
    },
    {
      "id": "research",
      "title": "查找資料",
      "category": "日常行動",
      "description": "翻閱法律書籍，尋找案件需要的資料。",
      "availability": "13:00／16:00",
      "images": {
        "male": "action_stills/male/research.png",
        "female": "action_stills/female/research.png"
      },
      "default_variant": "male"
    },
    {
      "id": "flatter",
      "title": "拍老闆馬屁",
      "category": "日常行動",
      "description": "笑著遞上咖啡，老闆身邊還有一疊新卷宗。",
      "availability": "受僱律師；13:00",
      "images": {
        "male": "action_stills/male/flatter.png",
        "female": "action_stills/female/flatter.png"
      },
      "default_variant": "male"
    },
    {
      "id": "gym",
      "title": "健身",
      "category": "下班行動",
      "description": "握住啞鈴鍛鍊身體，釋放工作壓力。",
      "availability": "19:00",
      "images": {
        "male": "action_stills/male/gym.png",
        "female": "action_stills/female/gym.png"
      },
      "default_variant": "male"
    },
    {
      "id": "standup",
      "title": "看脫口秀",
      "category": "下班行動",
      "description": "坐在觀眾席笑著鼓掌，享受下班時光。",
      "availability": "19:00",
      "images": {
        "male": "action_stills/male/standup.png",
        "female": "action_stills/female/standup.png"
      },
      "default_variant": "male"
    },
    {
      "id": "legal_video",
      "title": "看法律講座影片",
      "category": "下班行動",
      "description": "在家觀看法律講座，邊聽邊做筆記。",
      "availability": "19:00",
      "images": {
        "male": "action_stills/male/legal_video.png",
        "female": "action_stills/female/legal_video.png"
      },
      "default_variant": "male"
    },
    {
      "id": "sleep",
      "title": "我只想睡覺",
      "category": "下班行動",
      "description": "躺在溫暖的被窩裡，安心睡去。",
      "availability": "19:00",
      "images": {
        "male": "action_stills/male/sleep.png",
        "female": "action_stills/female/sleep.png"
      },
      "default_variant": "male"
    },
    {
      "id": "tv_program",
      "title": "上電視節目",
      "category": "隨機事件",
      "description": "在節目上回應主持人的提問。",
      "availability": "接受媒體邀請時",
      "images": {
        "male": "action_stills/male/tv_program.png",
        "female": "action_stills/female/tv_program.png"
      },
      "default_variant": "male"
    },
    {
      "id": "news_interview",
      "title": "接受新聞採訪",
      "category": "隨機事件",
      "description": "面對記者的麥克風，清楚說明自己的觀點。",
      "availability": "接受新聞邀請時",
      "images": {
        "male": "action_stills/male/news_interview.png",
        "female": "action_stills/female/news_interview.png"
      },
      "default_variant": "male"
    },
    {
      "id": "consultation",
      "title": "客戶諮詢",
      "category": "隨機事件",
      "description": "向客戶解釋卷宗與法律問題。",
      "availability": "合署／開業；不預設一定簽約",
      "images": {
        "male": "action_stills/male/consultation.png",
        "female": "action_stills/female/consultation.png"
      },
      "default_variant": "male"
    },
    {
      "id": "assign_case",
      "title": "分派案件",
      "category": "職員管理",
      "description": "把案件卷宗交給同事，準備分工處理。",
      "availability": "開業；管理操作不推進時段",
      "images": {
        "male": "action_stills/male/assign_case.png",
        "female": "action_stills/female/assign_case.png"
      },
      "default_variant": "male"
    }
  ],
  "characters_path": "character_catalog.json",
  "character_counts": {
    "protagonist_variants": 4,
    "staff": 45,
    "candidates": 3,
    "total_pngs": 52
  },
  "environments": [
    {
      "id": "office",
      "title": "事務所",
      "image": "environments/office.png"
    },
    {
      "id": "home",
      "title": "下班後的家",
      "image": "environments/home.png"
    }
  ],
  "asset_status": "ready",
  "validation": "exports/static_asset_validation.json"
};

window.CONCEPT_CHARACTERS = {
  "version": "0.3",
  "game_name": "訴訟之神之路",
  "purpose": "概念插畫風透明立繪；不是可換裝的分層角色系統或動畫骨架",
  "counts": {
    "protagonist_variants": 4,
    "staff": 45,
    "candidates": 3,
    "total_pngs": 52
  },
  "characters": [
    {
      "id": "PRO-M-WORK",
      "label": "男主角・工作服",
      "title": "男主角・工作服",
      "kind": "protagonist",
      "group": "protagonist",
      "source_sheet": "characters/protagonist_variants_sheet.png",
      "source_rect": {
        "x": 344,
        "y": 0,
        "width": 249,
        "height": 586
      },
      "source_component": 1,
      "file": "characters/individual/PRO-M-WORK.png",
      "width": 249,
      "height": 586,
      "sha256": "76a17aa230f79866a043865343ea7297fc28d2256b46534aac48525bd9ff1f63",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "PRO-M-HOME",
      "label": "男主角・居家服",
      "title": "男主角・居家服",
      "kind": "protagonist",
      "group": "protagonist",
      "source_sheet": "characters/protagonist_variants_sheet.png",
      "source_rect": {
        "x": 803,
        "y": 0,
        "width": 244,
        "height": 585
      },
      "source_component": 9,
      "file": "characters/individual/PRO-M-HOME.png",
      "width": 244,
      "height": 585,
      "sha256": "80926677a6b0c4046379f05b2e34378d8b37b69fc5eb3ec562bf16f80b63f240",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": false
    },
    {
      "id": "PRO-F-WORK",
      "label": "女主角・工作服",
      "title": "女主角・工作服",
      "kind": "protagonist",
      "group": "protagonist",
      "source_sheet": "characters/protagonist_variants_sheet.png",
      "source_rect": {
        "x": 369,
        "y": 573,
        "width": 216,
        "height": 564
      },
      "source_component": 324,
      "file": "characters/individual/PRO-F-WORK.png",
      "width": 216,
      "height": 564,
      "sha256": "0be308de65d59083fada00eb73570944465d145f934abd0fb51759344610c605",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": false
    },
    {
      "id": "PRO-F-HOME",
      "label": "女主角・居家服",
      "title": "女主角・居家服",
      "kind": "protagonist",
      "group": "protagonist",
      "source_sheet": "characters/protagonist_variants_sheet.png",
      "source_rect": {
        "x": 808,
        "y": 571,
        "width": 242,
        "height": 565
      },
      "source_component": 326,
      "file": "characters/individual/PRO-F-HOME.png",
      "width": 242,
      "height": 565,
      "sha256": "6e03e87e60836700077daa809f25762ab34a3048d0c1aaf58076fbb9a0bc98d3",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": false
    },
    {
      "id": "EMP001",
      "label": "員工 EMP001",
      "title": "員工 EMP001",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_1.png",
      "source_rect": {
        "x": 62,
        "y": 0,
        "width": 229,
        "height": 487
      },
      "source_component": 1,
      "file": "characters/individual/EMP001.png",
      "width": 229,
      "height": 487,
      "sha256": "7cd6878298f23c7dbc94b4644755b6e53ffdd3a8e23848ee4771225aeb3daae4",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP002",
      "label": "員工 EMP002",
      "title": "員工 EMP002",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_1.png",
      "source_rect": {
        "x": 344,
        "y": 28,
        "width": 219,
        "height": 458
      },
      "source_component": 36,
      "file": "characters/individual/EMP002.png",
      "width": 219,
      "height": 458,
      "sha256": "e8de0a111ce5720b0351133530640837b03ccea5e4af7e0f369098f0a79de206",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": false
    },
    {
      "id": "EMP003",
      "label": "員工 EMP003",
      "title": "員工 EMP003",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_1.png",
      "source_rect": {
        "x": 616,
        "y": 0,
        "width": 212,
        "height": 485
      },
      "source_component": 7,
      "file": "characters/individual/EMP003.png",
      "width": 212,
      "height": 485,
      "sha256": "50902cc6333ee66239f90844c8815d1267dd89419fe5128e377496bfeaaf2219",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": false
    },
    {
      "id": "EMP004",
      "label": "員工 EMP004",
      "title": "員工 EMP004",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_1.png",
      "source_rect": {
        "x": 876,
        "y": 0,
        "width": 218,
        "height": 487
      },
      "source_component": 2,
      "file": "characters/individual/EMP004.png",
      "width": 218,
      "height": 487,
      "sha256": "cf96b5895a7116d264ceaf02a5c5a30c97cb85ef5014bf0e6a1b3ccf8d3b5115",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP005",
      "label": "員工 EMP005",
      "title": "員工 EMP005",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_1.png",
      "source_rect": {
        "x": 1146,
        "y": 0,
        "width": 240,
        "height": 484
      },
      "source_component": 3,
      "file": "characters/individual/EMP005.png",
      "width": 240,
      "height": 484,
      "sha256": "9bd30ce9f7c3485876ebfd384d843a2c42e1b197e1c5bed68011c6f965131788",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP006",
      "label": "員工 EMP006",
      "title": "員工 EMP006",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_1.png",
      "source_rect": {
        "x": 1461,
        "y": 24,
        "width": 159,
        "height": 457
      },
      "source_component": 30,
      "file": "characters/individual/EMP006.png",
      "width": 159,
      "height": 457,
      "sha256": "e183819a153a27b3b8c9b72cef7974f49dacafdd3b202a41c5db67a2e833f29c",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": false
    },
    {
      "id": "EMP007",
      "label": "員工 EMP007",
      "title": "員工 EMP007",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_1.png",
      "source_rect": {
        "x": 80,
        "y": 463,
        "width": 205,
        "height": 473
      },
      "source_component": 774,
      "file": "characters/individual/EMP007.png",
      "width": 205,
      "height": 473,
      "sha256": "b111e7553dd440dc4342a5c2e6b5cfc759308dd0327edc84957a83bea7596c06",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP008",
      "label": "員工 EMP008",
      "title": "員工 EMP008",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_1.png",
      "source_rect": {
        "x": 344,
        "y": 482,
        "width": 219,
        "height": 454
      },
      "source_component": 794,
      "file": "characters/individual/EMP008.png",
      "width": 219,
      "height": 454,
      "sha256": "a7c12c4ecd78d472460eea83ac3a5f2cfe397076da3220987b9229c4f5407214",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP009",
      "label": "員工 EMP009",
      "title": "員工 EMP009",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_1.png",
      "source_rect": {
        "x": 613,
        "y": 479,
        "width": 222,
        "height": 457
      },
      "source_component": 782,
      "file": "characters/individual/EMP009.png",
      "width": 222,
      "height": 457,
      "sha256": "5d6f242cd430e281f598f49503586cd992cdb084db3a15c4b9fb8ec2f3e10ab1",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP010",
      "label": "員工 EMP010",
      "title": "員工 EMP010",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_1.png",
      "source_rect": {
        "x": 873,
        "y": 470,
        "width": 249,
        "height": 466
      },
      "source_component": 778,
      "file": "characters/individual/EMP010.png",
      "width": 249,
      "height": 466,
      "sha256": "b5f6e69fd90029da388ce2576fe50febe995d6885d5b4b447d86a1ca752ba508",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP011",
      "label": "員工 EMP011",
      "title": "員工 EMP011",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_1.png",
      "source_rect": {
        "x": 1151,
        "y": 462,
        "width": 246,
        "height": 474
      },
      "source_component": 775,
      "file": "characters/individual/EMP011.png",
      "width": 246,
      "height": 474,
      "sha256": "03e6bb6318566e4a28916715d34312c2a57f33100ce3230c051b81aa0b9efb80",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP012",
      "label": "員工 EMP012",
      "title": "員工 EMP012",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_1.png",
      "source_rect": {
        "x": 1440,
        "y": 483,
        "width": 194,
        "height": 453
      },
      "source_component": 790,
      "file": "characters/individual/EMP012.png",
      "width": 194,
      "height": 453,
      "sha256": "ffdd71e2d4b7204168bbd43f2e161c9ce28cc291963d49a22dc4a05090e2e71f",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP013",
      "label": "員工 EMP013",
      "title": "員工 EMP013",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_2.png",
      "source_rect": {
        "x": 84,
        "y": 12,
        "width": 213,
        "height": 491
      },
      "source_component": 13,
      "file": "characters/individual/EMP013.png",
      "width": 213,
      "height": 491,
      "sha256": "047e0c45cc50a385f2ca0ace750f2da107ea18cf4ad110c0eb7ad1476bd83053",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": false
    },
    {
      "id": "EMP014",
      "label": "員工 EMP014",
      "title": "員工 EMP014",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_2.png",
      "source_rect": {
        "x": 351,
        "y": 0,
        "width": 185,
        "height": 505
      },
      "source_component": 1,
      "file": "characters/individual/EMP014.png",
      "width": 185,
      "height": 505,
      "sha256": "1f5ec91fb5465315c0b72184128795ef727f6e78c824ac76d38a0f1fd7469eba",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP015",
      "label": "員工 EMP015",
      "title": "員工 EMP015",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_2.png",
      "source_rect": {
        "x": 609,
        "y": 0,
        "width": 193,
        "height": 499
      },
      "source_component": 10,
      "file": "characters/individual/EMP015.png",
      "width": 193,
      "height": 499,
      "sha256": "fe066d2c322b6716f665220853ebc68ae1bc6a476dc66f3015bb6af92b403fa0",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": false
    },
    {
      "id": "EMP016",
      "label": "員工 EMP016",
      "title": "員工 EMP016",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_2.png",
      "source_rect": {
        "x": 848,
        "y": 0,
        "width": 244,
        "height": 504
      },
      "source_component": 2,
      "file": "characters/individual/EMP016.png",
      "width": 244,
      "height": 504,
      "sha256": "3e34fdafcc5ebc5b899f0891b54f1ce845dd2399fb89f996f41334738a4257ac",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP017",
      "label": "員工 EMP017",
      "title": "員工 EMP017",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_2.png",
      "source_rect": {
        "x": 1180,
        "y": 27,
        "width": 172,
        "height": 477
      },
      "source_component": 30,
      "file": "characters/individual/EMP017.png",
      "width": 172,
      "height": 477,
      "sha256": "4934e9826fcce24e1e860b271ee058e933e1ea919ef006c8383f93a537c248e7",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": false
    },
    {
      "id": "EMP018",
      "label": "員工 EMP018",
      "title": "員工 EMP018",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_2.png",
      "source_rect": {
        "x": 1419,
        "y": 63,
        "width": 203,
        "height": 438
      },
      "source_component": 69,
      "file": "characters/individual/EMP018.png",
      "width": 203,
      "height": 438,
      "sha256": "80049f79934651e9cdfdaf4332da9627c6eb37276bc7db7e576c82adaf63799e",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": false
    },
    {
      "id": "EMP019",
      "label": "員工 EMP019",
      "title": "員工 EMP019",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_2.png",
      "source_rect": {
        "x": 110,
        "y": 481,
        "width": 187,
        "height": 455
      },
      "source_component": 763,
      "file": "characters/individual/EMP019.png",
      "width": 187,
      "height": 455,
      "sha256": "465673f3bb72261cc216fc8dca800e7a16a1128a2f5b62001115a5cb6620d449",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP020",
      "label": "員工 EMP020",
      "title": "員工 EMP020",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_2.png",
      "source_rect": {
        "x": 328,
        "y": 478,
        "width": 237,
        "height": 458
      },
      "source_component": 750,
      "file": "characters/individual/EMP020.png",
      "width": 237,
      "height": 458,
      "sha256": "4340cdf64cf0618921e4248bd3bfe7e1ca99252e13c471de53a1862ed0972b30",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP021",
      "label": "員工 EMP021",
      "title": "員工 EMP021",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_2.png",
      "source_rect": {
        "x": 574,
        "y": 480,
        "width": 232,
        "height": 456
      },
      "source_component": 761,
      "file": "characters/individual/EMP021.png",
      "width": 232,
      "height": 456,
      "sha256": "01d30d527784d0e84133c3ddbbdd2363fb278ce183b5420485b428665d09ed8b",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP022",
      "label": "員工 EMP022",
      "title": "員工 EMP022",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_2.png",
      "source_rect": {
        "x": 875,
        "y": 495,
        "width": 215,
        "height": 441
      },
      "source_component": 786,
      "file": "characters/individual/EMP022.png",
      "width": 215,
      "height": 441,
      "sha256": "6e35bb8b7961c651b91a16ea6ecd6db113cc40471714fcbb193e0cd24fe85c9d",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP023",
      "label": "員工 EMP023",
      "title": "員工 EMP023",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_2.png",
      "source_rect": {
        "x": 1188,
        "y": 511,
        "width": 148,
        "height": 425
      },
      "source_component": 812,
      "file": "characters/individual/EMP023.png",
      "width": 148,
      "height": 425,
      "sha256": "40592e7c2778e2b8e6fc923f5f9d89dea68e65fcaf71797a9f7031f1406f843b",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP024",
      "label": "員工 EMP024",
      "title": "員工 EMP024",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_2.png",
      "source_rect": {
        "x": 1421,
        "y": 480,
        "width": 197,
        "height": 456
      },
      "source_component": 751,
      "file": "characters/individual/EMP024.png",
      "width": 197,
      "height": 456,
      "sha256": "4e6ad26662488adc8bfc3c3c599efeb9519c50b0607ebc35ef02e959ddaaf764",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP025",
      "label": "員工 EMP025",
      "title": "員工 EMP025",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_3.png",
      "source_rect": {
        "x": 26,
        "y": 0,
        "width": 250,
        "height": 487
      },
      "source_component": 3,
      "file": "characters/individual/EMP025.png",
      "width": 250,
      "height": 487,
      "sha256": "ce10fae2682b4596b72db0ae76872b900715f5b7798bba40602157314154f05c",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP026",
      "label": "員工 EMP026",
      "title": "員工 EMP026",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_3.png",
      "source_rect": {
        "x": 300,
        "y": 24,
        "width": 264,
        "height": 460
      },
      "source_component": 53,
      "file": "characters/individual/EMP026.png",
      "width": 264,
      "height": 460,
      "sha256": "1655e1d3eb92fc09246aed57885f01334a15ff7bcad7c6f16575c98c4ff15e05",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": false
    },
    {
      "id": "EMP027",
      "label": "員工 EMP027",
      "title": "員工 EMP027",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_3.png",
      "source_rect": {
        "x": 605,
        "y": 0,
        "width": 214,
        "height": 492
      },
      "source_component": 6,
      "file": "characters/individual/EMP027.png",
      "width": 214,
      "height": 492,
      "sha256": "cc6ffda71d56686381da1897aea123c9ac71d9132ebaa597e17ef16feff53b45",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP028",
      "label": "員工 EMP028",
      "title": "員工 EMP028",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_3.png",
      "source_rect": {
        "x": 869,
        "y": 0,
        "width": 216,
        "height": 487
      },
      "source_component": 1,
      "file": "characters/individual/EMP028.png",
      "width": 216,
      "height": 487,
      "sha256": "23367e097cf60c35dcd299ea0ff766ca3531ec2c248ed3e1e2cff6956246bc3a",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP029",
      "label": "員工 EMP029",
      "title": "員工 EMP029",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_3.png",
      "source_rect": {
        "x": 1162,
        "y": 0,
        "width": 243,
        "height": 492
      },
      "source_component": 2,
      "file": "characters/individual/EMP029.png",
      "width": 243,
      "height": 492,
      "sha256": "175c7963be4e873c1e293b7a30298291d5fd222b5ef97eeee7f888fce7f9a12e",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP030",
      "label": "員工 EMP030",
      "title": "員工 EMP030",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_3.png",
      "source_rect": {
        "x": 1428,
        "y": 0,
        "width": 234,
        "height": 493
      },
      "source_component": 10,
      "file": "characters/individual/EMP030.png",
      "width": 234,
      "height": 493,
      "sha256": "b2422d1a7d9c3d4e73ea2bb41f9b8e26837d633be4b30f5326df4ae5d2f307a4",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP031",
      "label": "員工 EMP031",
      "title": "員工 EMP031",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_3.png",
      "source_rect": {
        "x": 16,
        "y": 471,
        "width": 262,
        "height": 464
      },
      "source_component": 960,
      "file": "characters/individual/EMP031.png",
      "width": 262,
      "height": 464,
      "sha256": "202820cd9e78ad4427cf7d9e802f11786e4b1f59c85a0f4e52ec1952e40fe464",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP032",
      "label": "員工 EMP032",
      "title": "員工 EMP032",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_3.png",
      "source_rect": {
        "x": 312,
        "y": 460,
        "width": 248,
        "height": 475
      },
      "source_component": 908,
      "file": "characters/individual/EMP032.png",
      "width": 248,
      "height": 475,
      "sha256": "0e49389366c1ff1d98bf97ab95a2146f72206c09c13168bf0aaa6b4c4c61d57f",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP033",
      "label": "員工 EMP033",
      "title": "員工 EMP033",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_3.png",
      "source_rect": {
        "x": 591,
        "y": 512,
        "width": 203,
        "height": 423
      },
      "source_component": 1022,
      "file": "characters/individual/EMP033.png",
      "width": 203,
      "height": 423,
      "sha256": "35d58cf25df77d25564885f97fd069eaca99719446dc453b6b358cfe11f18213",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP034",
      "label": "員工 EMP034",
      "title": "員工 EMP034",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_3.png",
      "source_rect": {
        "x": 864,
        "y": 474,
        "width": 246,
        "height": 461
      },
      "source_component": 957,
      "file": "characters/individual/EMP034.png",
      "width": 246,
      "height": 461,
      "sha256": "3040c6478d8c5fb0e54051d2fe06603aaf699cccf304a24b9fe89c5e9b0753a9",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP035",
      "label": "員工 EMP035",
      "title": "員工 EMP035",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_3.png",
      "source_rect": {
        "x": 1166,
        "y": 496,
        "width": 231,
        "height": 439
      },
      "source_component": 1018,
      "file": "characters/individual/EMP035.png",
      "width": 231,
      "height": 439,
      "sha256": "2ff0fa76959368c599f6146793bda30afe5983d9e5c1a74cc75d1372c26b6ada",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP036",
      "label": "員工 EMP036",
      "title": "員工 EMP036",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_3.png",
      "source_rect": {
        "x": 1440,
        "y": 475,
        "width": 220,
        "height": 460
      },
      "source_component": 995,
      "file": "characters/individual/EMP036.png",
      "width": 220,
      "height": 460,
      "sha256": "af89c9d0887540e7fab05ad2608286ef050eb43aff8869d4a33f97d9b2c131ff",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP037",
      "label": "員工 EMP037",
      "title": "員工 EMP037",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_4.png",
      "source_rect": {
        "x": 96,
        "y": 13,
        "width": 236,
        "height": 482
      },
      "source_component": 10,
      "file": "characters/individual/EMP037.png",
      "width": 236,
      "height": 482,
      "sha256": "b6cc2fe744d46d2da2a9db5354642585025d6784db77588341eb30fa0b17ce3c",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": false
    },
    {
      "id": "EMP038",
      "label": "員工 EMP038",
      "title": "員工 EMP038",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_4.png",
      "source_rect": {
        "x": 381,
        "y": 0,
        "width": 233,
        "height": 500
      },
      "source_component": 1,
      "file": "characters/individual/EMP038.png",
      "width": 233,
      "height": 500,
      "sha256": "686bab7646457a62c8139ad28e8567771372796170d0d26cb50c6558852822ad",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP039",
      "label": "員工 EMP039",
      "title": "員工 EMP039",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_4.png",
      "source_rect": {
        "x": 653,
        "y": 18,
        "width": 189,
        "height": 484
      },
      "source_component": 21,
      "file": "characters/individual/EMP039.png",
      "width": 189,
      "height": 484,
      "sha256": "72cd52d52c14fd625e1b2070212090c2bc113562126e517570d7ca8de50769d3",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": false
    },
    {
      "id": "EMP040",
      "label": "員工 EMP040",
      "title": "員工 EMP040",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_4.png",
      "source_rect": {
        "x": 883,
        "y": 45,
        "width": 218,
        "height": 455
      },
      "source_component": 59,
      "file": "characters/individual/EMP040.png",
      "width": 218,
      "height": 455,
      "sha256": "2efbc2fd86065ac7b8300238c7d8817ce72dcdfaa873f9f8a0758ef603b9ba83",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": false
    },
    {
      "id": "EMP041",
      "label": "員工 EMP041",
      "title": "員工 EMP041",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_4.png",
      "source_rect": {
        "x": 1125,
        "y": 0,
        "width": 235,
        "height": 499
      },
      "source_component": 2,
      "file": "characters/individual/EMP041.png",
      "width": 235,
      "height": 499,
      "sha256": "69452b31b0e2b960b2f3088ffd309f5a235fab0ea6c37a17b9bb6a0fa3eda4c5",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP042",
      "label": "員工 EMP042",
      "title": "員工 EMP042",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_4.png",
      "source_rect": {
        "x": 1404,
        "y": 0,
        "width": 203,
        "height": 499
      },
      "source_component": 3,
      "file": "characters/individual/EMP042.png",
      "width": 203,
      "height": 499,
      "sha256": "4e67640b6a55f725547b71f6a5269329d70ca6a447c78565e96ff6a74d3ea445",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "EMP043",
      "label": "員工 EMP043",
      "title": "員工 EMP043",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_4.png",
      "source_rect": {
        "x": 110,
        "y": 506,
        "width": 169,
        "height": 423
      },
      "source_component": 967,
      "file": "characters/individual/EMP043.png",
      "width": 169,
      "height": 423,
      "sha256": "539eb0d4a8897532e4bb9deaeb448dc832341ad4c267fe4484eb2a865d14ba5f",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": false
    },
    {
      "id": "EMP044",
      "label": "員工 EMP044",
      "title": "員工 EMP044",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_4.png",
      "source_rect": {
        "x": 335,
        "y": 473,
        "width": 253,
        "height": 461
      },
      "source_component": 934,
      "file": "characters/individual/EMP044.png",
      "width": 253,
      "height": 461,
      "sha256": "51eac0736dd10f7dc04de481427dafe584daea655a888b385c0f39173c005070",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": false
    },
    {
      "id": "EMP045",
      "label": "員工 EMP045",
      "title": "員工 EMP045",
      "kind": "staff",
      "group": "staff",
      "source_sheet": "characters/staff_sheet_4.png",
      "source_rect": {
        "x": 638,
        "y": 497,
        "width": 207,
        "height": 437
      },
      "source_component": 963,
      "file": "characters/individual/EMP045.png",
      "width": 207,
      "height": 437,
      "sha256": "7348e41a51dc4778bade2b817f29547945768bc55daf09beecaa727e867a69f4",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "REC001",
      "label": "候選人 REC001",
      "title": "候選人 REC001",
      "kind": "candidate",
      "group": "candidate",
      "source_sheet": "characters/staff_sheet_4.png",
      "source_rect": {
        "x": 878,
        "y": 480,
        "width": 203,
        "height": 454
      },
      "source_component": 949,
      "file": "characters/individual/REC001.png",
      "width": 203,
      "height": 454,
      "sha256": "08c9795bf230a7d811ad9bb792f48e665f4b8cf739d36c181d77b376322ad393",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "REC002",
      "label": "候選人 REC002",
      "title": "候選人 REC002",
      "kind": "candidate",
      "group": "candidate",
      "source_sheet": "characters/staff_sheet_4.png",
      "source_rect": {
        "x": 1143,
        "y": 480,
        "width": 228,
        "height": 454
      },
      "source_component": 946,
      "file": "characters/individual/REC002.png",
      "width": 228,
      "height": 454,
      "sha256": "1c867c3407ca69723a4a35bf7029eee9994c32204c18f5c2bde9e32a1ce4695e",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": true
    },
    {
      "id": "REC003",
      "label": "候選人 REC003",
      "title": "候選人 REC003",
      "kind": "candidate",
      "group": "candidate",
      "source_sheet": "characters/staff_sheet_4.png",
      "source_rect": {
        "x": 1422,
        "y": 512,
        "width": 201,
        "height": 410
      },
      "source_component": 982,
      "file": "characters/individual/REC003.png",
      "width": 201,
      "height": 410,
      "sha256": "1ca70f53a177ba9f72fae085a55e660adef7aacddc9143739ec557e34321e58d",
      "source_figure_rgba_preserved": true,
      "source_edge_touch": false
    }
  ]
};
