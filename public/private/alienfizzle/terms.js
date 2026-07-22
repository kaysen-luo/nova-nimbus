/**
 * ═══════════════════════════════════════════════════════════════════
 *  terms.js · Alien Fizzle 术语中心表 (代码源头)
 * ═══════════════════════════════════════════════════════════════════
 *
 *  立表时间: 2026-07-22
 *  维护人:   Kaysen (定名 · 唯一命名权)
 *            Nova (代码引用 · 只引用不擅改)
 *  姊妹文档: ~/shared-agents/project-proposal/alien-fizzle/TERMS.md
 *            (人可读快照 + 命名变更史)
 *  管理方法: skill `project-terminology-central-registry`
 *  同步策略: C (手工同步, 无 build)
 *
 *  ─── 硬性纪律 ───────────────────────────────────────────────────
 *   1. 从 2026-07-22 起, **新增** UI 输出 / 文档标题 / 结算面板
 *      文字必须走 T.xxx, 不硬编字面。老代码渐进式迁移。
 *   2. 未定名项标 `// TODO 定名`, 保留占位, 不擅自发挥。
 *   3. 改名 = 改 terms.js 一行 + 走 skill 的改名 checklist:
 *        a. 改 terms.js 字面
 *        b. 全库 grep 旧字面 → 迁 T.xxx
 *        c. 同步刷 TERMS.md 命名变更史
 *        d. 通知合规 (若涉及项目名/角色名)
 * ═══════════════════════════════════════════════════════════════════
 */

const T = {
  // ─── 1. 项目本体 ────────────────────────────────────────────────
  project: {
    nameCN:    '舰舰别炸',           // 合规锁定名, 不可动 (软著 + ICP 备案)
    nameEN:    'Alien Fizzle',       // 合规锁定名, 不可动
    codename:  'alien-fizzle',       // slug, 目录/URL/AppID 内部锚点
    appId:     'wx52bccee83c7ef0de', // 微信小游戏 AppID (Kaysen 主体)
    version:   'v3.9',               // 当前 spec 权威版本 (随 spec 权威块递进)
    domain:    'alienfizzle.com',    // 未注册, K 说以后再说
    publishUrl:'https://nova-nimbus.pages.dev/private/alienfizzle/',
  },

  // ─── 2. 主角 ────────────────────────────────────────────────────
  hero: {
    name:     '主角',                // TODO 定名 (spec §2.1 仅称"主角", 待 K 拍板)
    role:     '守线人',              // spec §1 标题用词
  },

  // ─── 3. AI 伙伴 (BOBO) ─────────────────────────────────────────
  ai: {
    name:        'BOBO',             // 正式名 (2026-06 定, 早期代号 NUO 已废)
    nameCN:      '诺',               // 中文昵称 (spec §2.2 括注)
    fullName:    '悬浮球辅助机器人', // spec §2.2 标题描述
    mirrorName:  '镜像 BOBO',        // 无尽合成宝箱产出, 10s 临时召唤
    formerName:  'NUO',              // 已废弃 (2026-06 改为 BOBO)
  },

  // ─── 4. 敌人档位 (spec §2.4) ───────────────────────────────────
  enemies: {
    tierMinion:    '小兵',           // 4 款 · 消耗火力
    tierElite:     '精英怪',         // 7 款 · 引入策略应对
    tierMiniBoss:  '小 BOSS',        // 6 款 · 集火 3-5s 转折点
    tierFinalBoss: '大 BOSS',        // 3 款 · 关卡终局
    generalName:   '外星生物',       // 所有敌人统称
  },

  // ─── 5. 敌人具体名 (20 只 · spec §2.4.2-§2.4.5) ─────────────────
  enemyList: {
    // 小兵 (E01-E04)
    E01: '跳弹菌',
    E02: '刺蒲团',
    E03: '泡泡兵',
    E04: '自爆熊',
    // 精英 (E05-E11)
    E05: '盾墙客',
    E06: '喷毒手',
    E07: '脑罐博士',
    E08: '重炮蓝',
    E09: '心灵者',
    E10: '祭司眼镜',
    E11: '毒爆胖',
    // 小 BOSS (E12-E17)
    E12: '钻地兽',
    E13: '蛛母眼',
    E14: '腐化嘴',
    E15: '浮游炮台',
    E16: '熔岩龙',
    E17: '机甲首',
    // 大 BOSS (E18-E20)
    E18: '冰白触手王',
    E19: '翠绿魔王',
    E20: '水晶脑主',
  },

  // ─── 6. 技能升级卡 · 5 张 (spec §4.2, 2026-07-08 K 亲拍) ────────
  skills: {
    together:    '别站一起',         // 原手雷; 抽象意象派 (K 命名规则)
    flywheel:    '飞轮海',           // 旋转伤害区
    mercy:       '恩赐解脱',         // 点杀 + 颤栗减速
    highvoltage: '高压领域',         // 区域电击
    laserpierce: '激光贯穿',         // 穿透直线
  },

  // ─── 7. 枪械精通卡 · 22 张 (spec §4.6, A/B/C/D/E/F/G 七类) ──────
  masteries: {
    // A · 子弹形态 · 4 张
    a_pierce:     '集束枪管',        // 普攻+20%, 穿透2 (递减20%)
    a_bounce:     '裂头弹',          // TODO 定名确认 (spec V3.4 提到"裂头弹 a_bounce")
    a_burst:      '连发快射',        // 弹道 +N (V3.3.7 起 +2, 单发×0.55)
    a_focusbeam:  '集束激光',        // V3.9 新增 (普攻+20% + BOBO 折射+2)
    // B · 状态施加 · 3 张 (全必触发无概率)
    b_burn:       '燃烧弹',          // 2 秒 50% DoT
    b_slow:       '减速弹',          // 减速 30% / 2s
    b_poison:     '毒液弹',          // 每 0.5s 20 真伤, 3 层
    // C · 特殊触发 · 2 张
    c_feast:      '食髓',            // 击杀精英+ 5s 攻速+50%
    c_meltdown:   '熔核',            // 11s 循环 (爬升3+满5+静默3)
    // D · 伤害修饰 · 2 张
    d_hunter:     '精英以上猎手',    // 对精英+boss +30%
    d_weak:       '弱者克星',        // 对减益单位 +40%
    // E · 防线相关 · 5 张
    e_reinforce:  '防线加固',        // 防线 HP +30%
    e_echo:       '回响',            // 每 20 kill 回 1% HP
    e_desperate:  '绝境反击',        // 防线降 2% → 攻+1%
    e_root:       '扎根',            // 护盾 + 反弹真伤 (不可重复)
    e_plasma:     '等离子防线',      // 20s 满盾, 击破爆真伤 (不可重复)
    // F · Meta · 3 张
    f_greed:      '贪婪',            // 击杀 2% 概率召唤状态门
    f_resonance:  '共鸣',            // 每持有 1 张精通 攻+2%
    f_gamble:     '恶魔赌局',        // 单张可重复 · σ 系数 · EV≈1.14
    // G · BOBO 强化 · 3 张 (全不可重复)
    g_focus:      '激光聚焦',        // 弹射+5, 激光+100% (V3.5)
    g_burn:       '激光爆燃',        // 半径50, 主伤25% (V3.5)
    g_guide:      '激光制导',        // 攒 12 击, 5s 制导 (V3.5)
  },

  // ─── 8. 系统机制 ────────────────────────────────────────────────
  systems: {
    defenseLine:      '防线',        // 持久度归零 = Game Over (§7)
    statusGate:       '状态门',      // 平铺属性增益/减益, 撞击翻转 (§5)
    laneTreasure:     '宝箱通道',    // 左路静态 (§3, ui-wireframe)
    laneCombat:       '接敌通道',    // 右路动态 (§3)
    treasureChest:    '宝箱',        // 三选一 roguelike 抽卡 (§4.1)
    treasureExp:      '宝箱经验值',  // V3.3.5 新增门槛机制
    drawThree:        '三选一',      // 抽卡结算 UI (ui-wireframe s09)
    fireSilence:      '火力静默',    // 状态门特殊维度 (§5.6)
    doubleFire:       '双倍火力',    // 火力静默翻转 buff
    revive:           '复活',        // IAA 广告钩子, 每局限 3 次
    preExperience:    '预体验关卡',  // 满配开局钩子 (§7.5)
    endlessMode:      '无尽模式',    // 通关解锁 (§7.6)
    officialLevel:    '正式关卡',    // Lv2 三大关 M1-M3
    barrier:          '障碍',        // V3.6 新增 6 槽位宝箱障碍
    bobo_hate_P1:     '仇恨-防线',   // BOBO 4 阶仇恨 P1
    bobo_hate_P2:     '仇恨-Boss',   // P2
    bobo_hate_P3:     '仇恨-精英',   // P3
    bobo_hate_P4:     '仇恨-小兵',   // P4
  },

  // ─── 9. UI 文案 (ui-wireframe.html 已出现) ───────────────────────
  ui: {
    btnStart:         '开始游戏',    // 主菜单 CTA
    btnSettings:      '设置',
    btnEndless:       '无尽模式',    // 带 🔒 未解锁态
    btnStartPreExp:   '开始预体验',
    btnLaunch:        '出击',        // 正式关卡确认
    btnResume:        '继续',        // 暂停面板
    btnExitToMenu:    '退出到主菜单',
    btnBackToMenu:    '回主菜单',
    titlePause:       '暂停',
    titleDefeat:      '防线告破!',
    titleDrawCard:    '选择一张卡',
    subDrawCard:      '宝箱开启 · 三选一',
    labelSkill:       '技能',        // 抽卡类型 tag
    labelMastery:     '精通',        // 抽卡类型 tag
    labelLaneTreasure:'宝箱通道',    // 场内标签
    labelReviveUsed:  '复活 3 次已用尽',
    // TODO 定名: 结算面板标题 / 分数展示 / 好友榜 tab (spec §7.6 有需求, wireframe 未落)
  },
};

// ─── 递归冻结, 阻止运行期误改 ─────────────────────────────────────
function deepFreeze(obj) {
  Object.getOwnPropertyNames(obj).forEach((prop) => {
    const v = obj[prop];
    if (v && typeof v === 'object' && !Object.isFrozen(v)) deepFreeze(v);
  });
  return Object.freeze(obj);
}
deepFreeze(T);

// ─── 模块导出 ──────────
// nova-nimbus package.json 是 "type": "module", 走纯 ESM
// - ESM (Node/构建工具): import T from './terms.js'
// - 浏览器: <script type="module" src="./terms.js"></script> 后 T 挂 window
// - 单 HTML 内联 (策略 C): 复制本文件 T = { ... } 块到 <script> 里, 不带 export
if (typeof window !== 'undefined') {
  window.T = T;
}
export default T;
export { T };
