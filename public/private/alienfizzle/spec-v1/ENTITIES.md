# ENTITIES · 舰舰别炸

> 所有数值引 `data.json` 字段路径, 不硬编。术语引 `T.xxx.yyy` (对应 terms.js)。

---

## 主角 (Player)

**工厂**: `createPlayer()` (L1411)

| 运行时字段 | 来源 | data.json path |
|---|---|---|
| x | `W / 2` (居中) | `data.world.canvas.W` |
| y | `PLAYER_Y` | `data.world.lanes.PLAYER_Y` |
| w | `CFG.player.width` | `data.player.width` |
| h | `CFG.player.height` | `data.player.height` |
| lastShot | 0 (运行时计时) | — |

射击间隔: `data.player.bulletInterval` (ms)

---

## AUV 副手 (BOBO)

**工厂**: `createNuo(offsetX, isMirror=false)` (L1421)
**属性工厂**: `createNuoStats()` (L1435) — 返回 `{...CFG.nuo.base, silenceUntil: 0}`

主 AUV 和镜像 AUV 共享一份 stats 引用 (`G.nuoStats`)。

| 运行时字段 | 来源 | data.json path |
|---|---|---|
| w, h | `CFG.nuo.width` | `data.bobo.width` |
| offsetX | 参数传入 | — |
| isMirror | 参数传入 | — |
| lastShot | 0 | — |

**AUV 基础属性** (createNuoStats):

| 字段 | data.json path |
|---|---|
| atk | `data.bobo.base.atk` |
| spd | `data.bobo.base.spd` |
| blt | `data.bobo.base.blt` |
| vel | `data.bobo.base.vel` |
| crt | `data.bobo.base.crt` |
| critDmg | `data.bobo.base.critDmg` |

射击间隔: `data.bobo.bulletInterval` (ms)
静默时间: `data.bobo.silenceMs` (ms)

---

## 子弹 (Bullet)

**工厂**: `createBullet(x, y, owner, atk, vel, crit)` (L1439)

| 运行时字段 | 来源 | data.json path |
|---|---|---|
| w | `CFG.bullet.width` | `data.bullet.width` |
| h | `CFG.bullet.height` | `data.bullet.height` |
| vy | `-CFG.bullet.speed * vel * velMult` | `data.bullet.speed` |
| atk | 参数 | — |
| owner | `'player'` 或 `'nuo'` | — |
| crit | 参数 (bool) | — |

快枪手 (`T.masteries.a_rapid`) 将 `playerBulletVelMult` 设为 1.5。

---

## 敌人 (Enemies)

**工厂**: `createEnemy(type, customX, customY)` (L1449)

### 运行时字段

| 字段 | 来源 | 备注 |
|---|---|---|
| x | 随机或 customX | 接敌通道内 |
| y | `HORIZON_Y + 5` 或 customY | |
| w, h | `tcfg.w/h` | 型号模板 |
| hp, maxHp | `tcfg.hp` | |
| speed | `tcfg.speed * G.diffMult` | 难度缩放 |
| dps | `tcfg.dps * G.diffMult` | 难度缩放 |
| armor | `tcfg.armor` | 0-1 减伤比例 |
| shield | `tcfg.shield` | |
| score | `tcfg.score` | |
| isMiniBoss | `tcfg.isMiniBoss` | 0/1/2/3 |
| isFinalBoss | `tcfg.isFinalBoss` | bool |
| type | 参数 | |
| atDefense | false | 到达防线标记 |
| burnUntil, burnDmg, lastBurnTick | 0 | 燃烧状态 |
| slowUntil, slowMult | 0, 1 | 减速状态 |
| stunUntil | 0 | 麻痹状态 |

### 6 型模板

| type | data.json path | 档次 |
|---|---|---|
| small | `data.enemies.small` | `T.enemies.tierMinion` |
| elite | `data.enemies.elite` | `T.enemies.tierElite` |
| miniA | `data.enemies.miniA` | `T.enemies.tierMiniBoss` |
| miniB | `data.enemies.miniB` | `T.enemies.tierMiniBoss` |
| miniC | `data.enemies.miniC` | `T.enemies.tierMiniBoss` |
| boss | `data.enemies.boss` | `T.enemies.tierFinalBoss` |

每型字段: hp / speed / dps / w / h / color / shield / armor / score (+ isMiniBoss/isFinalBoss)

### 20 只具名敌人 (T.enemyList)

具名敌人是叙事层 (spec/UI 显示), 6 型模板是机制层 (运行时实例化)。映射关系:

| 档次 | 模板 type | 具名 ID |
|---|---|---|
| `T.enemies.tierMinion` | small | E01-E04 |
| `T.enemies.tierElite` | elite | E05-E11 |
| `T.enemies.tierMiniBoss` | miniA/miniB/miniC | E12-E17 |
| `T.enemies.tierFinalBoss` | boss | E18-E20 |

| ID | 中文名 (T.enemyList.Exx) | 档次 |
|---|---|---|
| E01 | 跳弹菌 | 小兵 |
| E02 | 刺蒲团 | 小兵 |
| E03 | 泡泡兵 | 小兵 |
| E04 | 自爆熊 | 小兵 |
| E05 | 盾墙客 | 精英 |
| E06 | 喷毒手 | 精英 |
| E07 | 脑罐博士 | 精英 |
| E08 | 重炮蓝 | 精英 |
| E09 | 心灵者 | 精英 |
| E10 | 祭司眼镜 | 精英 |
| E11 | 毒爆胖 | 精英 |
| E12 | 钻地兽 | 小 BOSS |
| E13 | 蛛母眼 | 小 BOSS |
| E14 | 腐化嘴 | 小 BOSS |
| E15 | 浮游炮台 | 小 BOSS |
| E16 | 熔岩龙 | 小 BOSS |
| E17 | 机甲首 | 小 BOSS |
| E18 | 冰白触手王 | 大 BOSS |
| E19 | 翠绿魔王 | 大 BOSS |
| E20 | 水晶脑主 | 大 BOSS |

族名: `T.enemies.speciesEN` (Ossyr) / `T.enemies.speciesCN` (厄司)

**注**: 20 只具名敌人是纯叙事/视觉层 (UI 显示名 + 美术差异), 运行时行为完全由 6 型模板决定, 无特殊 AI 或独有技能.

---

## 宝箱 (Treasure)

**工厂**: `createTreasure()` (L1481) → `_createTreasureInner()` (L1490)

生成间隔: `data.treasure.spawnInterval` (ms)

### 配件 Perks (按序解锁)

共 8 件, 按固定顺序解锁。data.json path: `data.treasure.perks[i]`

| 序号 | id | desc (原文) | data.json HP path |
|---|---|---|---|
| 1 | fireRate | 主角射速 +1%/s 持续 | `data.treasure.perks[0].hp` |
| 2 | multiShot | 弹道 +1, 每 30s +1 | `data.treasure.perks[1].hp` |
| 3 | atkUp | 主角攻击每 5s +1 | `data.treasure.perks[2].hp` |
| 4 | explosive | 命中点小范围爆炸 | `data.treasure.perks[3].hp` |
| 5 | ricochet | 子弹弹射下一个敌人 | `data.treasure.perks[4].hp` |
| 6 | laser | 每 3s 折射激光 | `data.treasure.perks[5].hp` |
| 7 | mirror | 复制副手 NUO | `data.treasure.perks[6].hp` |
| 8 | ultimate | 每 10s 全屏爆炸 | `data.treasure.perks[7].hp` |

HP 受 `slotGrowth` 递增: `perk.hp * slotGrowth^slotIdx`

### 循环增益 RepeatBuffs

8 件 perk 全解锁后进入循环阶段。data.json path: `data.treasure.repeatBuffs[i]`

| id | desc |
|---|---|
| atk++ | 主角伤害 +25% |
| spd++ | 射速 +20% |
| crit++ | 暴击率 +1.5% |

HP 公式: `(repeatHpStart + n * repeatHpStep) * slotGrowth^slotIdx`
- `data.treasure.hpCurve.repeatHpStart`
- `data.treasure.hpCurve.repeatHpStep`

### 诱饵 Decoy

障碍宝箱, 打破无奖励。

| 字段 | data.json path |
|---|---|
| 基础 HP | `data.treasure.hpCurve.decoyHpBase` |
| HP 比例 | `data.treasure.hpCurve.decoyRatio` |
| 颜色 | `data.treasure.hpCurve.decoyColor` |

### 布局

| 字段 | data.json path |
|---|---|
| 宽 | `data.treasure.layout.w` |
| 高 | `data.treasure.layout.h` |
| 列数 | `data.treasure.layout.colCount` |
| 槽高 | `data.treasure.layout.slotHeight` |
| 顶部 Y | `data.treasure.layout.topY` |
| 下落速度 | `data.treasure.layout.fallSpeed` |
| 初始数量 | `data.treasure.layout.initCount` |

---

## 状态门 (State Gate)

**工厂**: `createStateGate(opts)` (L1556)

尺寸: `data.world.lanes.GATE_WIDTH` x `data.world.lanes.GATE_HEIGHT`
推进速度: `data.gate.tick.speed * G.diffMult`
生成间隔: `data.gate.tick.gateInterval` (秒)

减益概率随时间爬升: t=0s P=0.2, t=90s P=0.8, 之后恒 0.8。
游戏前 120s 排除防线三维 (defenseArmor/defenseMaxHP/defenseHeal)。

### 8 维表格

data.json path: `data.gate.dimensions[i]`

| key | label | vmin | vmax | step | unit |
|---|---|---|---|---|---|
| atk | 攻击力 | - | + | per step | |
| spd | 攻速 | - | + | per step | x |
| crt | 暴击率 | - | + | per step | % |
| critDmg | 暴击伤害 | - | + | per step | % |
| silence | 火力静默 | - | + | per step | ms |
| defenseArmor | 防线护甲 | - | + | per step | % |
| defenseMaxHP | 防线上限 | - | + | per step | |
| defenseHeal | 防线回血 | - | + | per step | |

每维具体数值见 `data.gate.dimensions[]`。

运行时字段: x, y, w, h, dim, value, state (`'debuff'`/`'buff'`/`'released'`), released, speed。

---

## 金门 (Golden Gate)

**工厂**: `spawnGoldenGate()` (L5748)

Boss 击杀奖励, value=vmax 满增益, 碰即触发, 不占 maxConcurrent。
随机选一个维度, 给满 vmax。

**生成时机**: 每次击杀 mini-boss (miniA/miniB/miniC) 或 final boss 时触发 `triggerBossReward` → `spawnGoldenGate`. 即每个 boss 级敌人击杀都产出一道金门.

---

## AUV 激光 (BOBO Laser)

**类**: `class BoboLaserBeam` (L2411)

data.json path: `data.bobo.laser`

| 字段 | 含义 | data.json path |
|---|---|---|
| attackSpeed | 秒/发 | `data.bobo.laser.attackSpeed` |
| rangeRatio | 射程比 (通道长) | `data.bobo.laser.rangeRatio` |
| damageRatio | 伤害比 (相对主角攻击力) | `data.bobo.laser.damageRatio` |
| hatredPriority | 仇恨优先级 | `data.bobo.laser.hatredPriority` |

仇恨优先级 (高→低): attacking_defense > boss > elite > minion。
同仇恨值优先血量少的敌人。

---

## 技能卡 (Skills)

共 5 张, 每张 3 级。data.json path: `data.skills[i]`

| id | 名称 (T.skills.xxx) | Lv1 desc | Lv2 desc | Lv3 desc |
|---|---|---|---|---|
| together | `T.skills.together` 别站一起 | 每 10s 主角丢一枚手雷, 对以主要目标为圆心、直径 1/3 通道宽的圆形区域造成 150 点爆炸伤害 | 质变: 爆炸伤害 +30% (195) | 完全体: 范围 x1.5 + 0.6s 后二段爆炸 (60% 伤害) |
| flywheel | `T.skills.flywheel` 飞轮海 | 每 10s 发射一个飞轮到接敌通道, 触敌后展开旋转形成通道宽的圆形伤害区域, 50 伤/秒 持续 6s | 质变: 飞轮持续 9s, 伤害区半径 +30% | 完全体: 持续 12s, 且飞轮沿通道从触发位置向顶端移动 |
| mercy | `T.skills.mercy` 恩赐解脱 | 每 12s 锁定最高优先级目标发一颗超级子弹, 24x atk 真伤 + 概率变异 (32/48/64/80/96/112x); 锥形硬控 1s; 击杀 40% 再触发无上限 | 质变: 同时锁定 2 目标, 锥形扩至 90度; 变异 32-128x 期望 61x; 击杀 50% 再触发 | 完全体: 同时锁定 5 目标, 锥形扩至 120度; 变异 48-160x 期望 77x; 击杀 60% 再触发; 颤栗改恐惧: 逆行 1.5s + 归位 1.5s 共 3s |
| highvoltage | `T.skills.highvoltage` 高压领域 | 每 20s 在接敌通道下半部 (0.4x通道长) 创造高压电区, 每 0.5s 一跳 100 伤, 穿过子弹带电麻痹 0.5s, 持续 10s | 质变: 范围扩至 0.5x通道长 + 敌人触边缘麻痹 2s, 进入区内每 2s 麻痹 0.5s | 完全体: 范围扩至 0.6x通道长 + 越靠底部伤害越高 (曲线) + 首次撞防线免伤并麻痹 3s |
| laserpierce | `T.skills.laserpierce` 激光贯穿 | 蓄力 2s 后由 BOBO 发射一根 60px 宽贯穿激光, 对一条直线上所有敌人造成 800 (playerAtk x 32) 伤害 | Lv1 + 2.5s 沿线余波, 每 0.5s 沿线 100 (playerAtk x 4) 伤 | Lv2 + 3s 内每 0.5s 从随机目标额外发射一根 5px 小激光, 200 (playerAtk x 8) 伤 |

标签: `data.tags[skillId]`

---

## 精通卡 (Masteries)

共 26 张, 7 类 (A/B/C/D/E/F/G)。data.json path: `data.masteries[i]`

### A · 子弹形态 (6 张)

| id | 名称 (T.masteries.xxx) | desc | 标签 |
|---|---|---|---|
| a_pierce | 集束枪管 | 普攻+20%, 穿透 1 (次级目标伤害 60%) | `data.tags.a_pierce` |
| a_bounce | 裂头弹 | 击中主目标瞬间分裂 2 颗小子弹, 50% 伤害, 不再穿透/分裂, 继承攻击特效 | `data.tags.a_bounce` |
| a_explode | 爆炸弹 | 子弹命中产生小范围爆炸, 30% 主伤害 | `data.tags.a_explode` |
| a_focusbeam | 集束激光 | 普攻+20%, BOBO 激光折射 +2 | `data.tags.a_focusbeam` |
| a_burst | 连发快射 | 攻速+30%, 弹道+2, 单发伤害降为 35% (不可重复获取) | `data.tags.a_burst` |
| a_rapid | 快枪手 | 主角子弹飞行速度x1.5, 5% 概率爆头 (+50% 主伤 + 目标减速 50% 持续 0.5s) [不可重复] | `data.tags.a_rapid` |

### B · 状态施加 (3 张, 全必触发)

| id | 名称 | desc | 标签 |
|---|---|---|---|
| b_burn | 燃烧弹 | 必触发点燃, 2 秒内 50% 主伤害 DoT | `data.tags.b_burn` |
| b_slow | 减速弹 | 必触发减速 30% 持续 2 秒 | `data.tags.b_slow` |
| b_poison | 毒液弹 | 命中挂毒, 每 0.5s 扣 20 真伤, 持续 4s, 可叠 3 层 (每层x1.5) | `data.tags.b_poison` |

### C · 特殊触发 (2 张)

| id | 名称 | desc | 标签 |
|---|---|---|---|
| c_feast | 食髓 | 击杀精英以上敌人后 5s 内攻速+50% | `data.tags.c_feast` |
| c_meltdown | 熔核 | 自动循环 11 秒: 3s 爬升 (1x-3x攻速) + 5s 满态 (3x攻速) + 3s 静默 | `data.tags.c_meltdown` |

### D · 伤害修饰 (2 张)

| id | 名称 | desc | 标签 |
|---|---|---|---|
| d_hunter | 精英以上猎手 | 对精英+boss 单位 +30% 伤害 | `data.tags.d_hunter` |
| d_weak | 弱者克星 | 对被施加减益 (减速/麻痹/燃烧等) 的单位 +40% 伤害 | `data.tags.d_weak` |

### E · 防线相关 (5 张)

| id | 名称 | desc | 标签 |
|---|---|---|---|
| e_reinforce | 防线加固 | 防线 HP +30% | `data.tags.e_reinforce` |
| e_echo | 回响 | 每击杀 20 个敌人, 防线回 1% HP | `data.tags.e_echo` |
| e_desperate | 绝境反击 | 防线 HP 每下降 2%, 攻击力+1% | `data.tags.e_desperate` |
| e_root | 扎根 | 护盾 (defenseMax x 0.8%/秒), 护盾期间被攻击反弹真伤 (defenseMax x 5% + 护盾 x 20%). 受击后暂停积累 10s [不可重复] | `data.tags.e_root` |
| e_plasma | 等离子防线 | 每 20s 用满 defenseMax 护盾替换原护盾. 护盾被击破瞬间, 对最近 3 敌方形范围造成击破前护盾峰值等值的真实伤害 (不递减) [不可重复] | `data.tags.e_plasma` |

### F · Meta (3 张)

| id | 名称 | desc | 标签 |
|---|---|---|---|
| f_greed | 贪婪 | 击杀敌人 2% 概率立即召唤一道状态门 | `data.tags.f_greed` |
| f_resonance | 共鸣 | 每持有 1 张精通卡, 攻击力+2% | `data.tags.f_resonance` |
| f_gamble | 恶魔赌局 | 摇一个系数重构主角+Bobo 面板 (0.5x-2.0x, EV=1.14, 可重复获取) | `data.tags.f_gamble` |

### G · AUV 强化 (5 张, 全不可重复)

| id | 名称 | desc | 标签 |
|---|---|---|---|
| g_focus | 激光聚焦 | Bobo 弹射 +3 | `data.tags.g_focus` |
| g_burn | 激光爆燃 | Bobo 激光命中产生爆炸 (半径 25px, 主伤 15%) + 点燃 | `data.tags.g_burn` |
| g_guide | 激光制导 | Bobo 攒 20 次攻击发一道 5s 制导激光, 击杀跳目标 | `data.tags.g_guide` |
| g_dmg | 激光强化 | Bobo 激光伤害 +50% | `data.tags.g_dmg` |
| g_speed | 激光攻速 | Bobo 激光间隔 -30% | `data.tags.g_speed` |

---

## 恶魔赌局系数分布

data.json path: `data.demonGamble[i]`

9 档, EV = 1.14。见 `data.demonGamble` 数组 (coeff + probability)。

---

## 防线 (Defense)

最大 HP: `data.defense.maxHP`

防线 HP 归零 = Game Over。

---

*产出: Phase 2 Dev-B ENTITIES.md · 覆盖 8 实体类 + 5 技能卡 + 26 精通卡 + 20 具名敌人*
