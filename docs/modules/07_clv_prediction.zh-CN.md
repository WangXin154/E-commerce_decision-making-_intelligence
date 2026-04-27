# 模块 07 —— 客户生命周期价值（CLV）预测

## 模块概述

本模块构建了一个客户生命周期价值（CLV）预测流程，用于估计未来客户价值，并将预测结果进一步转化为面向业务的决策工具。

本模块的目标并不只是提升回归模型精度，而是让 CLV 结果能够真正支持：
- 未来客户价值判断
- 高价值客户识别
- 留存与预算优先级分配
- value–risk 决策映射
- 面向业务方的可解释输出

在整个电商智能决策系统中，本模块承担的是**客户价值优先级层**的角色。

---

## 业务问题

本模块主要回答以下几个核心问题：

1. 哪些客户未来最有可能贡献更高价值？
2. 预测出的未来价值应如何指导留存和预算分配？
3. 哪些客户既高价值又有风险，因此最值得优先保护？
4. CLV 预测结果能否做到足够可解释，从而支持业务讨论与资源优先级决策？

从业务角度看，本模块的意义在于：  
它将客户价值建模转化为一个可执行的资源配置框架，而不仅仅是一个回归任务。:contentReference[oaicite:21]{index=21}

---

## 数据来源

本模块使用来自项目 MySQL 数据仓库及前序分析层的客户级行为与价值特征。

特征空间主要用于概括：
- recency 类活跃度特征
- 购买次数与频率
- 消费强度
- 探索广度
- 已购商品多样性
- 其他客户级历史行为摘要

本模块进一步生成的业务输出包括：
- 客户价值分层
- value–risk 矩阵
- 预算分配视图
- 高价值客户画像
- 模型解释图。

在 portfolio deck 中明确提到的代表性 artifact 包括：
- `budget_allocation_overview`
- `customer_tier_statistics`
- `high_value_customer_profile`。:contentReference[oaicite:23]{index=23}

---

## 方法论

### 1. CLV 目标定义
本模块将 CLV 视为一个面向未来的客户价值预测问题。与只看历史消费不同，它关注的是**未来客户价值**，并让这个预测结果可被业务方直接用于优先级判断。

因此，本模块天然适用于：
- CRM 资源分配
- 预算投放
- 留存优先级判断
- 高价值客户保护

### 2. 特征构建
模型使用客户级历史行为特征，既覆盖活跃程度，也覆盖价值结构。

代表性特征组包括：
- recency 相关得分
- frequency 和订单数指标
- spending 类变量
- exploration breadth
- purchased variety 指标

portfolio deck 的解释页明确表明，这个模型的解释是基于用户行为结构的，而不是黑盒：  
图中的 **R_score** 是最重要的特征，订单数、频率、探索度和购买多样性属于第二层核心信号。:contentReference[oaicite:24]{index=24}

### 3. 回归建模
本模块比较多种回归类模型，用于估计未来客户价值。  
目标并不只是找一个“数值最好”的模型，而是找到一个既具备预测价值、又能支持业务转译的模型。

完整流程包括：
- 特征工程
- train/test 评估
- 模型比较
- 结果导出，供后续业务模块使用

### 4. 价值分层
预测出的 CLV 并不会只保留为原始回归数值，而会进一步转化为业务可读的价值层级，以便运营和管理使用。

portfolio deck 也明确将 **value tiers** 作为该模块的核心输出之一。:contentReference[oaicite:25]{index=25}

### 5. 价值–风险整合
本模块进一步与 churn / risk 层结合，构建 **value–risk matrix**。

这是本模块最重要的设计之一，因为它区分了：
- high CLV + high risk
- high CLV + lower risk
- lower CLV groups

deck 中直接给出了业务逻辑：
- **High CLV + high risk → 最优先挽回名单**
- **High CLV + lower risk → 重点保护体验并提升 share of wallet**
- **Lower CLV groups → 使用选择性或自动化干预**。:contentReference[oaicite:26]{index=26}

### 6. 预算分配转译
CLV 流程不只用于识别谁重要，也用于预算和资源分配。  
也就是说，本模块把“未来价值”翻译成了“资源应该往哪里倾斜”。

portfolio deck 明确指出：同一套 CLV pipeline 同时支持 **customer prioritization** 和 **budget allocation outputs**，因此它不是简单的回归分数，而是一个真正的决策层。:contentReference[oaicite:27]{index=27}

### 7. 可解释性输出
为了让业务侧能够接受和使用模型，本模块还包含了解释层。

根据 portfolio deck，该模型“足够可解释，可以支持与业务利益相关方展开讨论”，而 feature-importance 图则为“模型输出 → 用户行为解释”提供了清晰桥梁。:contentReference[oaicite:28]{index=28}

---

## 核心发现

### 1. 客户价值不是均匀分布的，而是高度集中
本模块最核心的业务结论之一是：客户价值并不是平均分布在所有用户身上，而是集中在少数高层级客户中。

portfolio deck 直接总结道：客户价值集中在少数 upper tiers 中，而不是均匀分布。:contentReference[oaicite:29]{index=29}

### 2. CLV 的价值不只在预测，而在决策支持
本模块最强的业务贡献不只是回归建模，而是把 CLV 作为一个决策支持信号使用。

同一套流程可支持：
- 客户优先级判断
- 高价值客户识别
- 预算分配输出
- 留存决策逻辑。:contentReference[oaicite:30]{index=30}

### 3. 价值与风险结合后，业务动作框架更强
单独的价值分数并不足够。  
本模块的真正实用性，来自未来价值与 churn / risk 信号的结合。

这使业务可以形成：
- 高价值高风险用户 → 最优先挽回
- 高价值低风险用户 → 重点保护并提升价值
- 低价值用户 → 使用更低触达成本的策略。:contentReference[oaicite:31]{index=31}

### 4. 模型具备行为层面的可解释性
本模块并没有停留在“预测出一个值”，而是进一步解释了**为什么某些客户更有价值**。

deck 的解释页指出：
- **R_score** 是最重要特征
- order count、frequency、exploration、purchased variety 属于第二层重要信号

这对于业务沟通、CRM 运营和面试展示都非常重要。:contentReference[oaicite:32]{index=32}

### 5. 模块生成了可复用的业务 artifact
本项目并没有把 CLV 结果留在 notebook 内部，而是导出并可视化了如下结果：
- value tiers
- value–risk matrix
- budget allocation outputs
- high-value customer profile
- interpretability plots。

---

## 核心业务输出

本模块的代表性输出包括：

- 客户价值分层（value tiers）
- value–risk matrix
- budget allocation overview
- customer tier statistics
- high-value customer profile
- feature importance / interpretability plots。

这些输出使本模块可直接用于：
- 留存优先级判断
- CRM 定向运营
- 预算规划
- Dashboard 报告
- 高层业务故事表达

---

## 价值分层解读

### Lower Value Groups
这些客户未来预计贡献的价值相对较低。

**业务意义**
- 使用选择性干预
- 优先采用低成本、可扩展的 CRM 策略
- 不宜过度投入高级资源

### Mid Value Groups
这些客户具有一定意义，但还不是最核心的价值群体。

**业务意义**
- 持续观察其增长潜力
- 使用结构化激活和 loyalty-building 动作
- 结合 churn risk 找出可升级的人群

### High Value Groups
这些客户预计会贡献显著更高的未来价值。

**业务意义**
- 主动保护
- 分配更多留存预算
- 使用更高触达等级的服务或策略
- 若同时出现风险信号，应优先处理

---

## 业务建议

基于本模块设计与当前输出，建议采取以下动作：

1. **把 CLV 当作优先级分层，而不只是预测分数**  
   CLV 的核心价值在于决定资源应该先投向谁。:contentReference[oaicite:35]{index=35}

2. **先将 CLV 与 churn risk 结合，再决定干预强度**  
   value–risk matrix 比单独的价值分数更可执行。高 CLV + 高风险应成为优先 save list。:contentReference[oaicite:36]{index=36}

3. **对高价值客户提供差异化保护，但要有选择性**  
   高价值客户值得更高等级服务，但最应优先的仍是“高价值且有风险”的那部分用户。

4. **将解释性输出用于业务沟通**  
   feature-importance 图能帮助解释为什么某类客户值得投入更多预算和资源。:contentReference[oaicite:37]{index=37}

5. **将 CLV 输出接入下游决策系统**  
   CLV 结果应进一步连接到：
   - churn 监控
   - 推荐策略
   - CRM 优先级
   - Dashboard 汇报
   - 预算分配逻辑

---

## 技术实现要点

本模块体现了以下技术能力：

- 客户级未来价值预测
- 面向回归任务的机器学习流程
- 面向未来价值估计的特征工程
- 模型比较与结果导出
- 将预测值转化为业务可读的 value tiers
- 将客户价值与风险信号整合
- 为业务方提供可解释性输出

本模块在整体链路中的位置是：

历史行为 → 特征工程 → CLV 预测 → 价值分层 → value–risk 策略 → 预算分配输出

---

## 文件与交付物

核心 notebook：
- `Statistical_analysis_report/07_Customer_Lifetime_Value_Prediction.ipynb`

代表性的业务交付物包括：
- budget allocation overview
- customer tier statistics
- high-value customer profile
- value–risk matrix 图
- feature importance / interpretability plots。

根据 notebook 版本不同，输出目录中也可能包含：
- CLV 预测表
- 分层汇总表
- 客户级评分文件
- 特征重要性图
- 客户策略切片文件

---

## 在完整项目中的位置

本模块在整个“电商智能决策系统”中承担的是**客户价值优先级层**的角色。

它可以自然连接到：
- RFM 用户分群
- 流失预测
- 推荐系统策略
- Dashboard 汇报
- 留存与预算配置决策

它让整个项目从“理解用户”和“预测风险”进一步走向“基于价值做业务优先级判断”。

---

## 后续优化方向

本模块未来可以继续扩展：

- 更紧密地打通 churn 与 CLV 优先级规则
- 增加更明确的预算分配模拟
- 更深入地比较不同回归模型
- 强化客户级策略导出
- 接入未来的 Streamlit Dashboard
- 抽取为可复用的 `src/models/clv.py` 模块