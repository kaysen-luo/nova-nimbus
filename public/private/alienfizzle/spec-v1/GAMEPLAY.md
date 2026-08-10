# GAMEPLAY · 舰舰别炸

## 核心循环

**触发**: `requestAnimationFrame` 驱动 `loop(ts)`, 每帧算 `dt` 后调用 `update(dt)`.

**执行**: update 按固定顺序 tick 所有子系统 — 主角横移 → BOBO 跟随 → 射击 → 配件 tick → BOBO 激光 → 技能 → 子弹 → 敌人生成/推进 → 宝箱 → 状态门 → 金门 → 防线 HP 检测 → 通关检测.

**结束**: `G.defenseHP <= 0` 触发 Game Over (预体验走复活弹窗); final boss 被击杀置 `G.victory` → 触发胜利结算.

## 射击与伤害

**射击节奏**: shootLoop 每帧判断 `G.now - lastShot >= effInterval`. `effInterval = data.player.bulletInterval / spdMult`. spdMult 受精通卡 c_feast (×1.5) 和 c_meltdown (11s 循环: 0-3s 线性爬升 1→3x, 3-8s 恒 3x, 8-11s 完全静默) 叠乘, 再乘 `G.playerSpdMult` (a_burst +30%).

**子弹**: `createBullet` 产出, `vy = -data.bullet.speed * vel * velMult`. 子弹按 x 位置判定通道归属 — L 通道打宝箱, R 通道打敌人.

**玩家移动约束**: 玩家 x 可全屏自由拖拽 (0 ~ `data.world.canvas.W`), 无通道锁定. 子弹从主角 x 位置发射, x < `data.world.lanes.SPLIT_X` 的子弹击中左通道宝箱, x >= SPLIT_X 的子弹击中右通道敌人. 实战中玩家通常靠右站位以输出敌人.

**伤害公式**:
```
baseAtk = (20 + G.playerAtkBonus) * G.playerAtkMult * G.playerBurstDmgMult
effDmg  = baseAtk * critMult * armorReduction * masteryMult
critMult = 2 + data.nuo.base.critDmg + playerCritDmgExtra  (暴击时)
armorReduction = 1 - e.armor
```

**伤害修饰 (damageEnemy)**: 按优先级叠乘 — vulnMult (恩赐易损 ×1.2) → d_hunter (精英/boss ×1.3^n) → d_weak (带减益 ×1.4^n) → f_resonance (精通总数 ×0.02/张) → e_desperate (防线损失% ×0.01/2%档/n).

**爆头**: a_rapid 5% 触发, +50% 主伤并施加 0.5s 50% 减速.

## 敌人系统

**生成**: `spawnEnemies` 读运行时相位表 `G.runtimePhases` 获取当前 phase. phase 配置 `waveInterval` / `eliteProb` / `eliteInjects` / boss 触发点.

- 散兵 `spawnScatter`: 按 eliteProb 概率出 elite, 其余 small; 三车道随机.
- 方阵 `spawnFormation`: 按预设 spec 在右通道内映射坐标生成, 后排 y 偏移为负 (从远处飞入).
- Boss 序列 `G.runtimeBosses`: 按关卡配置, mini-boss 均匀分布于 30%~80% 时间轴, final boss 在 86.7% 处.

**停刷规则**: elapsed >= `data.levels[n].durationScale * 300`s 后停刷; final boss 在场彻底停刷; mini-boss 在场暂停散兵.

**敌人状态 tick (updateEnemies)**: 冰冻 → 燃烧 DoT (0.5s/tick) → 麻痹 → 毒液 DoT (0.5s/tick, 真伤 × 1.5^层) → 恐惧反推 → 减速/颤栗 → 正常前推. 到达 DEFENSE_Y 后进入 `atDefense` 攻击防线.

## 宝箱与抽卡

**生成**: 击杀敌人累积经验 → 满阈值触发 `spawnNewChest`. 阈值公式: `data.chestExpTune.initialThreshold * data.chestExpTune.growthExponent^tier`.

**宝箱种类**: perk (前 8 个固定序列) → buff (循环). HP = `(base + repeatCount * step) * slotGrowth^slotIdx`.

**配件 (Perk) 运行时效果**:
1. fireRate — 获取后每 1s 射速永久 +1% (tick 累积, 无上限)
2. multiShot — 弹道 +1, 此后每 30s 再 +1 (上限 base+4)
3. atkUp — 每 5s 主角攻击力 +1 (绝对值, 无上限)
4. explosive — 子弹命中时在命中点产生 `e.w × 0.5` 半径爆炸, 对范围内其他敌人造成 30% 主伤
5. ricochet — 子弹命中后弹射到最近未命中敌人 (半径 120px), 伤害 70% 衰减, 只弹 1 次
6. laser — 每 3s BOBO 从主角位置向最近敌人折射一道激光, 伤害 = playerAtk × 0.8, 可被 a_focusbeam +2 增加折射次数
7. mirror — 生成镜像 AUV (offsetX 对称), 共享 nuoStats, 独立射击和激光
8. ultimate — 每 10s 全屏爆炸, 对所有右通道敌人造成 playerAtk × 4 伤害

**6 槽位队列**: 每列 A(防线端)~F(传送门端) 共 6 槽; 击破任一后全体向 A 顺移 (瞬移填坑). 障碍在真宝箱落定后倒计时到期 50% 概率挤入.

**破箱 → 三选一**: `applyTreasure` → `triggerCardSelection` → `CardPool.drawThree` 按权重不放回抽 3 张 (技能卡权重 1.0/1.3, 精通卡 1.5). 已满级/一次性已拿不进池.

**UI 操作**: 点击卡片 → `selectCard` → `applyCardEffect`; 免费刷新 (每局 1 次); 广告刷新 (2 次); 广告全拿 (三张全生效, 每局 1 次).

## 精通卡效果

26 张精通卡按类别:

- **A 子弹形态**: a_pierce (穿透+普攻×1.2), a_bounce (弹射), a_explode (爆裂), a_focusbeam (集束+×1.2), a_burst (攻速+30%/弹道+2/单发×0.35), a_rapid (子弹飞速×1.5/5%爆头)
- **B 状态施加**: b_burn (燃烧), b_slow (减速), b_poison (毒液)
- **C 攻速周期**: c_feast (击杀精英/boss → 5s ×1.5 攻速), c_meltdown (11s 循环: 爬升→满→静默)
- **D 伤害修饰**: d_hunter (精英/boss +30%^n), d_weak (带减益 +40%^n)
- **E 防线**: e_reinforce (最大 HP ×1.3), e_echo (每 N 杀回血), e_desperate (损失% 加伤), e_root (扎根护盾, 0.8%/s, 反弹真伤), e_plasma (20s 一次满盾, 破盾触发屑刃 AOE)
- **F 特殊**: f_resonance (精通总数 ×2%/张), f_greed (加速出箱), f_gamble (恶魔赌局)
- **G BOBO**: g_focus (弹射链), g_burn (爆燃+点燃), g_dmg (+50% 伤害), g_speed (-30% 间隔), g_guide (制导激光)

## 技能系统

5 张技能卡, 各 3 级, 获取时立即施放一次后进入 CD, 此后每 CD 到期自动施放.

- **T.skill.together** (CD `data.skills.together.cooldown`): 锁离防线最近敌人, 600ms 后主爆 `playerAtk × 6` (Lv2 ×1.3 + 灼烧尸爆, Lv3 二段 ×0.6 + 40% 概率链式再释放, chain≤15).
- **T.skill.flywheel** (CD `data.skills.flywheel.cooldown`): 飞轮海, 全场 AOE.
- **T.skill.mercy** (CD `data.skills.mercy.cooldown`): 锁头排序 (atDefense > boss/elite/small > 血%高). Lv1 锁 1 / Lv2 锁 2 / Lv3 锁 5. 伤害 = `playerAtk × rollMercyMult(level)`. 全等级施加 5s 易损 (×1.2) + 身后锥形颤栗. Lv2 秒杀 50% 再触发, Lv3 100%.
- **T.skill.highvoltage** (CD `data.skills.highvoltage.cooldown`): 高压领域. Lv3 撞防线首次 stun 3s + playerAtk×12.
- **T.skill.laserpierce** (CD `data.skills.laserpierce.cooldown`): 激光贯穿, 从主角沿方向延伸到 HORIZON_Y 的矩形扫描, 命中沿线所有敌人. 200px 圆形跨通道宝箱 AOE.

**rollMercyMult**: 按等级各有 7 档概率分布 (Lv1: 24~112x, Lv2: 32~128x, Lv3: 48~160x).

## 状态门

**生成**: 同屏上限 `data.gate.maxConcurrent`; 严格按 `G.gateInterval` 间隔. 前 120s 排除防线三维.

**减益爬升**: 随时间 P(debuff) = clamp(0.2 + 0.6 × min(t, 90)/90, 0.2, 0.8). 减益初始值 ∈ [vmin, 0], 增益初始值 ∈ [step, vmax×0.5].

**推进**: 世界坐标下移, 投影到屏幕检测碰撞玩家. 碰到 → `applyGateToNuo` 结算维度值; 出底部 → 移除.

**维度效果**: 8 维 — atk/spd/blt/vel/crt/critDmg/defenseArmor/defenseMaxHP/defenseHeal/silence. silence 减益 = 静默 N ms; silence 增益 = 双倍火力 N ms (攻速 ×2, 到期精准还原). crt/critDmg 同步写主角字段; blt 同步 multiShot (+N, 总上限 base+4).

## AUV 激光

**BOBO 激光循环 (updateBoboLasers)**: 按 `data.boboLaser.attackSpeed` 秒/发, 持有 g_speed 则 ×0.7.

**目标选取 (rankedBoboTargets)**: P0 atDefense (点残止血: 血少优先) → P1 未 atDefense (最靠防线优先, 平局血少优先). 射程 = 通道高度 × `data.boboLaser.rangeRatio`.

**伤害**: `playerAtk × data.boboLaser.damageRatio × (nuoStats.atk / data.nuo.base.atk)`. 持有 g_dmg → ×1.5. 吃暴击.

**分叉链 (fireBoboLaserChain)**: g_focus 启用弹射, 从主目标找次近敌人链式命中.

**爆燃 (g_burn)**: 主目标 2s 燃烧 + 25px 半径小爆炸 (主伤 15%), 邻居也吃点燃.

**制导激光 (g_guide)**: 每 N 次普通攻击触发, 5s 持续锁定, 200ms/tick 40 伤害, 无视射程, 目标丢失自动跳转.

## 防线

**HP 系统**: 初始 `data.defense.maxHP`. 敌人 atDefense 时每帧 `dps × dt × (1 - G.defenseArmor)`. 先扣扎根盾 → 再扣等离子盾 → 剩余扣 HP.

**扎根 (e_root)**: 无受击 10s 后 0.8%/s×defenseMax 持续涨盾 (无上限). 扎根盾 >0 时反弹真伤: `defenseMax × 0.05 + shieldRoot × 0.20`, 1s CD/敌.

**等离子 (e_plasma)**: 每 20s 满额 defenseMax 护盾覆盖 plasmaShield. 总盾 (root+plasma) 被击破瞬间 → 屑刃 (triggerShardBurst): 对最近 3 敌造成历史峰值盾量真伤.

## 恶魔赌局

**触发**: 获取 f_gamble 精通卡时立即摇一次.

**系数**: `rollDemonGamble` 从 `DEMON_GAMBLE_DISTRIBUTION` 按概率抽一档 coeff (参见 `data.demonGamble.distribution`).

**结算**: 所有已积累增益的"偏离基线部分" × coeff. 公式: `stat = base + (stat - base) × coeff`. 影响 playerAtkBonus / playerAtkMult / playerCritBonus / nuoStats (atk/spd/blt/crt/critDmg).

## 关卡流程

**选关 (showLevelSelect)**: 3 关 + 无尽模式 (未开放). 关卡解锁链: preExp → Lv1 → Lv2 → Lv3.

**startGame**: 按关卡配置 diffMult / enemyMult / durationScale, 拉伸 PHASES 时间轴生成 `G.runtimePhases` + `G.runtimeBosses`. 关卡时长 = 300 × durationScale (5/7/9 min).

**复活 (reviveWithAd)**: 最多 3 次. 防线回 50%, 全体敌人反推 10s (rewindUntil), 期间不刷新新敌人. 清空子弹, 保留宝箱/状态门.

**Game Over (triggerGameOver)**: 记录击杀/分数/时长, 展示结算面板 + 复活按钮 (若剩余次数 >0).

## 预体验关卡

**触发**: currentLevel=0, 进入 `startPreExperience`.

**流程**: 10s 静默期 (可移动不可开火, 敌人从顶端错峰列队) → 解禁开火 → 8 波 6×10 方阵 (PRE_EXP_COMPOSITIONS) 依次刷出 → 全灭通关.

**特殊规则**: 主角 3 弹道 / 射速 ×3 / 暴率 25% / BOBO 属性用 PRE_EXP_STATS 覆盖; 宝箱 HP ×1.5; 精通卡效果 ×2; 状态门延迟 10s 才出.

**死亡**: 防线归零 → showPreExpReviveDialog (不走 Game Over).

## 透视投影

**模型**: 一点透视, 灭点在 HORIZON_Y. `perspectiveScale(y) = PERSPECTIVE_SCALE_FAR + (1 - far) × ((y - HORIZON_Y) / (DEFENSE_Y - HORIZON_Y))^0.7`. y=DEFENSE_Y 时 scale=1 (近端), y=HORIZON_Y 时 scale=`data.perspective.scaleFar`.

**API 族**: `worldToScreenPoint(x, y)` → 仅投影 x; `worldSizeToScreenSize` / `worldCenterRectToScreenPolygon` / `worldCircleToScreenPolygon` 逐角投影, 碰撞判定统一消费屏幕多边形 bounds.

## 输入与适配

**输入 (setupInput)**: mouse down/move/up + touch start/move/end 驱动 `G.pointerX` → update 里 clamp 映射主角 x. 三选一 UI 激活时优先吞掉指针事件. 键盘 P 暂停 / R 重置 / M 静音.

**HiDPI (applyHiDPI)**: canvas 按 `devicePixelRatio` 放大物理尺寸, CSS 恢复逻辑尺寸.

**移动端 (fitMobileCanvas)**: 检测 `isMobileMode` 后调整 canvas fit 策略, 保持 414×736 逻辑视口.

## 进度持久化

**存储**: `localStorage`, key 前缀 `nova_alienfizzle_`.

**PROGRESS_KEYS**: preExpCompleted / level1Completed / level2Completed / level3Completed. `getProgress(key)` 读 / `setProgress(key)` 写 / `markLevelCompleted(level)` 通关时标记.

**当前关卡**: `Storage.set('currentLevel', n)`, 下次启动默认进入上次关卡.
