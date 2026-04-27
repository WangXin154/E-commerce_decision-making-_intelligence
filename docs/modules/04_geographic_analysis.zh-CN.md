# 模块 04 —— 地理区域分析

## 模块概述

本模块从地理区域视角分析电商业务表现，重点研究巴西不同州和城市在市场规模、物流表现、客户满意度以及商品需求结构上的差异。

本模块并不把 geography 当作一个背景字段，而是将“地区”作为业务决策层来处理。分析目标是识别核心市场、高客单潜力市场、物流压力市场以及优先问题区域，并将这些发现进一步转化为差异化的区域运营策略。

---

## 业务问题

本模块主要回答以下几个核心问题：

1. 哪些州和城市是最重要的商业市场？
2. 区域销售表现的集中度有多高？
3. 物流差异中有多少来自跨州交易结构？
4. 哪些地区既具有商业重要性，又存在明显的客户体验问题？
5. 不同地区的商品需求结构是否存在差异？
6. 是否可以将区域市场划分为可解释、可执行的市场类型？

从业务角度看，本模块用于支持区域优先级管理、物流优化、市场扩张排序以及州级运营策略设计。

---

## 数据来源

本模块结合了多个来自 MySQL 数据仓库的区域相关数据集。

### 1. 州级汇总数据集
用于州级 KPI 比较、集中度分析和区域聚类。

主要字段包括：
- `customer_state`
- `order_count`
- `customer_count`
- `total_gmv`
- `total_revenue`
- `avg_order_value`
- `avg_delivery_days`
- `avg_freight_cost`
- `delay_rate`
- `avg_review_score`
- `bad_review_rate`
- 复购代理指标

该数据集特点：
- 覆盖 **27 个巴西州 / 联邦单位**
- 全国范围完整覆盖
- 无缺失值

### 2. 城市级汇总数据集
用于城市集中度分析和头部城市比较。

### 3. 买家–卖家路径数据集
用于分析：
- 同州交易 vs 跨州交易
- 路径级物流表现
- 运费与配送压力

### 4. 订单级明细数据集
用于分析：
- 州级品类偏好
- 满意度结构
- 州 × 品类 GMV 对比

因此，本模块在需要时会保留交易级明细，而不是只依赖聚合表。

---

## 方法论

### 1. 数据检查与准备
分析首先完成：
- 数据结构检查
- 缺失值检查
- 面向不同任务的子集构建（配送、评论、路径等）

这样可以避免不必要的全局删行，同时保留分析灵活性。

### 2. 区域探索性分析
EDA 用于理解：
- 州级销售分布
- 区域覆盖情况
- 销售集中度
- 州间规模差异

主要方法包括：
- 数值分布分析
- 州级排名表
- 初步集中度检查

### 3. 区域销售排名与集中度分析
本模块从以下维度比较州级市场：
- `total_gmv`
- `order_count`
- `avg_order_value`

之后进一步使用以下方法度量区域集中度：
- GMV 份额分析
- 核心州贡献分析
- Lorenz curve
- Gini coefficient

### 4. 地理可视化
notebook 增加了空间视角，包括：
- 州级气泡地图
- 头部城市排名图
- 核心州内部城市集中度分析

### 5. 基于聚类的区域分层
本模块使用州级特征进行聚类，覆盖：
- 市场规模
- 客单价值
- 物流质量
- 满意度表现

聚类特征包括：
- `total_gmv`
- `avg_order_value`
- `avg_review_score`
- `avg_delivery_days`
- `delay_rate`
- `avg_freight_cost`

聚类数选择依据：
- inertia
- silhouette score
- Davies–Bouldin score

最终选择：
- **K = 4**

之后再将 cluster 结果翻译为业务可读的市场类型名称。

### 6. 物流表现分析
本模块进一步比较：
- 各州平均配送时长
- 各州 delay rate
- 各州平均运费
- 同州与跨州交易差异
- 主要买卖路径
- 运费与配送速度关系

并进一步构建物流风险视图，识别结构性服务压力地区。

### 7. 满意度与问题区域识别
为了把运营表现和客户体验连接起来，本模块分析：
- 各州平均评分
- 各州差评率
- 满意度与物流指标关系
- 高销量但满意度偏弱的州
- 不同区域 cluster 的满意度画像

### 8. 区域商品偏好分析
本模块还延伸到商品策略层，分析：
- 各州头部品类
- 州级品类偏好热力图
- 基于 Location Quotient (LQ) 的特色品类
- 区域 cluster 的品类结构
- 优先问题区域的品类结构

### 9. 统计验证
主要区域发现通过以下方法进行验证：
- ANOVA：验证不同区域 cluster 之间的满意度差异
- Chi-square：验证州与满意度等级分布之间的关系
- Correlation：验证延迟率、评分与差评率之间的关系

### 10. 区域策略输出
最后，本模块将分析结果转化为：
- market-type strategy
- priority problem-region action table
- final regional operating logic

---

## 核心发现

### 1. 区域销售高度集中
平台虽然覆盖了巴西全部 **27** 个州，但销售表现极不均衡。

关键集中度结果包括：
- `SP` 单州贡献约 **37.39%** 的总 GMV
- `SP + RJ + MG` 三州合计贡献约 **62.54%**
- 前 10 个州贡献约 **87.38%**
- 仅 **7 个核心州** 就贡献了约 **80%** 的 GMV
- 州级 GMV 的 **Gini coefficient = 0.7032**

这说明平台业务高度依赖少数核心区域市场。

### 2. 大市场主要由规模驱动，而不一定由高客单价驱动
州级 `total_gmv` 与 `order_count` 的排名高度一致，说明头部区域之所以强，主要是因为交易量大。

相比之下，`avg_order_value` 排名明显不同。像 `PB`、`AL`、`RO` 这样的州在客单价维度表现更强，但并不是总 GMV 最大的市场。

这意味着：
- 有些州是**规模驱动型核心市场**
- 有些州则是**高客单潜力市场**

### 3. 城市层面的集中度比州层面更强
在城市层面，`sao paulo` 的 GMV 远高于其他城市，`rio de janeiro` 排在第二，但也与第一存在明显差距。

在头部州内部，城市集中度也存在明显不同：
- `RJ` 高度集中，`rio de janeiro` 单城贡献约 **54.24%**
- `MG` 明显更分散，`belo horizonte` 仅贡献约 **22.48%**

这说明有些强州高度依赖单一核心城市，而另一些州则有更广泛的城市基础支撑。

### 4. K = 4 的区域聚类形成了清晰的市场类型
最终 K-Means 结果选择 **K = 4**，得到四类可解释的区域市场：

- **Balanced Core Markets**
- **High-AOV Potential Markets**
- **Logistics-Stressed Markets**
- **Super Core Outlier Market**

聚类画像如下：

| Cluster Name | State Count | Total GMV | Avg Order Value | Avg Review Score | Avg Delivery Days | Delay Rate | Avg Freight Cost |
|---|---:|---:|---:|---:|---:|---:|---:|
| Balanced Core Markets | 9 | 829,470.36 | 167.33 | 4.08 | 14.34 | 7.34 | 24.74 |
| High-AOV Potential Markets | 9 | 103,874.92 | 221.27 | 4.09 | 20.82 | 6.22 | 40.93 |
| Logistics-Stressed Markets | 8 | 193,209.16 | 211.72 | 3.80 | 22.54 | 14.00 | 39.97 |
| Super Core Outlier Market | 1 | 5,939,079.38 | 142.27 | 4.18 | 8.70 | 4.37 | 17.37 |

这说明区域表现并不是单一维度的问题，而是市场规模、客单价值、物流和满意度共同作用的结果。

### 5. 跨州交易是物流压力的重要结构性来源
本模块发现，同州交易与跨州交易之间存在明显物流差距：

- **Same State 平均配送时长 = 7.87 天**
- **Cross State 平均配送时长 = 14.99 天**
- **Same State 平均运费 = 13.46**
- **Cross State 平均运费 = 23.68**

Welch’s t-test 进一步表明这种差异极其显著：
- **t = -145.4815**
- **p < 0.001**

这是本模块最强的运营发现之一：跨州交易结构本身就是造成配送压力、运费上升和客户体验下降的重要原因。

### 6. 有相当一部分物流既“贵”又“慢”
运费与配送时长分析表明，运费更高并不意味着配送更快。

一个关键结果是：
- 约 **30.88%** 的有效记录同时落在 **高成本 + 慢配送** 区域

这说明平台中有一部分物流活动既低效又昂贵，属于明显的运营改进空间。

### 7. 客户满意度差异与物流压力高度一致
无论从州级比较还是 cluster 级比较，都能看出满意度并不是随机分布的。

Cluster 级满意度画像如下：

| Cluster Name | Avg Review Score | Bad Review Rate | Avg Delivery Days | Delay Rate |
|---|---:|---:|---:|---:|
| Super Core Outlier Market | 4.18 | 12.59 | 8.70 | 4.37 |
| High-AOV Potential Markets | 4.09 | 14.21 | 20.82 | 6.22 |
| Balanced Core Markets | 4.08 | 14.81 | 14.34 | 7.34 |
| Logistics-Stressed Markets | 3.80 | 20.99 | 22.54 | 14.00 |

其中最弱的一类显然是 **Logistics-Stressed Markets**，说明物流压力与客户体验下降在结构上是重叠出现的。

### 8. 优先问题区域具有真实商业重要性
本模块识别出了“高订单量 + 低于中位满意度”的优先问题区域。

代表性的优先问题州包括：
- `RJ`
- `BA`
- `CE`
- `ES`
- `GO`
- `PA`
- `PE`

其中 `RJ` 最值得优先修复，因为它同时具备：
- 高订单量
- 较弱平均评分
- 较高差评率
- 偏高延迟率

因此它不是边缘小市场的问题，而是高商业影响区域的服务风险。

### 9. 区域需求结构既有共享核心，也有明显差异
在主要州中，多数头部品类会重复出现，例如：
- `beleza_saude`
- `relogios_presentes`
- `esporte_lazer`
- `informatica_acessorios`

但不同州的品类组合并不完全相同，部分州在某些品类上表现出更高相对集中度。

这意味着区域商品策略应同时兼顾：
- 全国统一的核心需求
- 局部区域的结构差异

### 10. 核心区域发现得到了强统计证据支持
本模块使用多种统计方法验证核心结论：

- 不同 regional cluster 的满意度差异 ANOVA：
  - **F = 32.4459**
  - **p < 0.001**
  - **eta-squared = 0.7383**

- `state × satisfaction_level` 的卡方检验：
  - **χ² = 683.0632**
  - **df = 18**
  - **p < 0.001**

- 相关性结果：
  - `delay_rate` 与 `avg_review_score`：**r = -0.805**
  - `delay_rate` 与 `bad_review_rate`：**r = 0.808**

这些结果共同说明：物流可靠性、区域类型和客户满意度之间存在结构性关联，而不是偶然现象。

---

## 关键指标

| 指标 | 结果 |
|---|---:|
| 覆盖州数量 | 27 |
| SP 的 GMV 占比 | 37.39% |
| 前 3 州 GMV 占比 | 62.54% |
| 前 10 州 GMV 占比 | 87.38% |
| 贡献约 80% GMV 的核心州数 | 7 |
| 州级 GMV Gini coefficient | 0.7032 |
| 最终聚类数 | 4 |
| Same State 平均配送时长 | 7.87 |
| Cross State 平均配送时长 | 14.99 |
| Same State 平均运费 | 13.46 |
| Cross State 平均运费 | 23.68 |
| 高成本 + 慢配送占比 | 30.88% |
| Cluster ANOVA F 值 | 32.4459 |
| Cluster ANOVA p 值 | < 0.001 |
| Eta-squared | 0.7383 |
| Chi-square 统计量 | 683.0632 |
| Chi-square 自由度 | 18 |
| Chi-square p 值 | < 0.001 |
| delay_rate 与 avg_review_score 相关系数 | -0.805 |
| delay_rate 与 bad_review_rate 相关系数 | 0.808 |

---

## 区域分层业务解读

### Super Core Outlier Market
这是一个由单一极强市场构成的特殊 cluster。

**画像**
- GMV 规模压倒性领先
- 物流表现最好
- 满意度表现最好

**策略方向**
- 保护领导地位
- 守住服务质量
- 深化留存与价值挖掘

---

### Balanced Core Markets
这类州共同构成了稳定的商业基础盘。

**画像**
- 具有一定 GMV 规模
- 满意度较稳
- 物流压力可控

**策略方向**
- 稳定并高效扩张
- 强化品类与物流支持
- 保持核心区域韧性

---

### High-AOV Potential Markets
这类州不是最大市场，但单位订单价值更高。

**画像**
- 平均客单价较高
- 规模中等
- 满意度尚可
- 运费负担高于核心市场

**策略方向**
- 有选择地扩张
- 在购买力明确的前提下增长
- 避免在规模不足和物流未准备好时过快投入

---

### Logistics-Stressed Markets
这类州体现出明显的服务与运营压力。

**画像**
- 配送时间最长
- 延迟率最高
- 满意度最低
- 运费压力较高

**策略方向**
- 先修复运营再扩大规模
- 优先提升路径可靠性
- 降低配送压力
- 稳定客户体验

---

## 业务建议

基于本模块结果，建议采用以下区域策略逻辑：

1. **先保护核心市场**  
   平台价值仍然高度集中在最强市场，尤其是 Super Core Outlier Market 和更广泛的 Balanced Core Markets。

2. **有选择地扩张，而不是全国统一推进**  
   High-AOV Potential Markets 只有在购买力明确、运营条件可控时才适合扩张。

3. **服务弱区必须先修复再增长**  
   Logistics-Stressed Markets 和 Priority Problem Regions 不应在物流和客户体验未修复前被强推增长。

4. **把跨州交易结构作为运营预警信号**  
   跨州交易暴露度应被持续监控，因为它是造成延迟和运费压力的最清晰结构性来源之一。

5. **把 geography 与商品策略结合起来**  
   区域需求结构并不完全相同，因此品类配置、活动设计和推荐策略应兼顾全国共性与局部差异。

6. **让区域风险指标可运营化**  
   延迟率、差评率、路径压力等指标应联合监控，而不是孤立看待。

---

## 技术实现要点

本模块体现了以下技术能力：

- 州级与城市级地理 KPI 分析
- 基于份额、Lorenz 曲线与 Gini 的集中度度量
- 地图与城市排名可视化
- K-Means 区域分层
- 路径级物流分析
- 同州 / 跨州交易比较
- 问题州识别
- 州级商品偏好分析
- Location Quotient (LQ) 分析
- ANOVA、Chi-square、Correlation 统计验证
- 导出区域策略表供下游汇报使用

---

## 文件与交付物

核心 notebook：
- `Statistical_analysis_report/04_Geographic_Analysis.ipynb`

核心输出文件包括：
- `output/04_geographic_analysis/state_clustered_results.csv`
- `output/04_geographic_analysis/priority_problem_region_actions.csv`
- `output/04_geographic_analysis/market_type_strategy.csv`
- `output/04_geographic_analysis/final_regional_conclusion.csv`
- `output/04_geographic_analysis/cluster_satisfaction_profile.csv`
- `output/04_geographic_analysis/problem_region_category_share.csv`
- `output/04_geographic_analysis/statistical_validation_summary.csv`
- `output/04_geographic_analysis/regional_key_findings.json`

可视化输出可能包括：
- 州级气泡地图
- 城市 GMV 排名图
- 集中度图
- cluster 可视化图
- 问题区域比较图
- 品类热力图

---

## 在完整项目中的位置

本模块在整个“电商智能决策系统”中承担的是**区域策略层**的角色。

它可以自然连接到：
- 品类分析
- 满意度分析
- 时间序列需求监控
- 流失与 CLV 优先级判断
- 后续 Dashboard 与业务汇报体系

它让整个项目从用户和商品分析进一步扩展到区域运营决策。

---

## 后续优化方向

本模块未来可以进一步扩展：

- 加入 seller 端 geography 和仓储逻辑
- 将路径压力与 seller 表现连接
- 引入 choropleth map 和更丰富的地理可视化
- 将区域策略与利润率 / 边际贡献结合
- 在后续 Streamlit Dashboard 中集成区域 KPI