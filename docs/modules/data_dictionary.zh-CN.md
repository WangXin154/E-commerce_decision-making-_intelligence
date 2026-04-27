## `docs/data_dictionary.zh-CN.md`

# 数据字典

## 概述

本项目基于 Olist 巴西电商公开数据集，采用分层数据设计。数据库首先保存原始导入表，然后构建一个简化的星型分析仓库，包含维度表和事实表，最后通过一组可复用 SQL 视图服务于满意度分析、RFM 分群、品类分析、区域分析、流失预测、CLV 预测和推荐系统等模块。:contentReference[oaicite:40]{index=40} :contentReference[oaicite:41]{index=41}

---

## 数据库

- **数据库名：** `ecommerce_platform`
- **字符集：** `utf8mb4`
- **排序规则：** `utf8mb4_0900_ai_ci` :contentReference[oaicite:42]{index=42}

---

## 第 1 层 —— 原始表（Raw Tables）

这些表用于保存从源数据直接导入的原始记录，是 ETL 的起点。:contentReference[oaicite:43]{index=43}

### 1. `customers_raw`

| 字段 | 类型 | 含义 |
|---|---|---|
| `customer_id` | `VARCHAR(50)` | 源数据中的客户 ID |
| `customer_unique_id` | `VARCHAR(50)` | 跨订单稳定的用户唯一标识 |
| `customer_zip_code_prefix` | `INT` | 邮编前缀 |
| `customer_city` | `VARCHAR(100)` | 客户城市 |
| `customer_state` | `VARCHAR(10)` | 客户所在州 |

### 2. `orders_raw`

| 字段 | 类型 | 含义 |
|---|---|---|
| `order_id` | `VARCHAR(50)` | 订单 ID，主键 |
| `customer_id` | `VARCHAR(50)` | 关联客户 |
| `order_status` | `VARCHAR(50)` | 订单状态 |
| `order_purchase_timestamp` | `VARCHAR(32)` | 下单时间 |
| `order_approved_at` | `VARCHAR(32)` | 审核时间 |
| `order_delivered_carrier_date` | `VARCHAR(32)` | 交给承运商时间 |
| `order_delivered_customer_date` | `VARCHAR(32)` | 送达客户时间 |
| `order_estimated_delivery_date` | `VARCHAR(32)` | 预计送达时间 |

**主键：** `order_id` :contentReference[oaicite:44]{index=44}

### 3. `products_raw`

| 字段 | 类型 | 含义 |
|---|---|---|
| `product_id` | `VARCHAR(50)` | 商品 ID，主键 |
| `product_category_name` | `VARCHAR(100)` | 商品品类 |
| `product_name_lenght` | `INT` | 商品名称长度 |
| `product_description_lenght` | `INT` | 商品描述长度 |
| `product_photos_qty` | `INT` | 商品图片数量 |
| `product_weight_g` | `INT` | 商品重量 |
| `product_length_cm` | `INT` | 长度 |
| `product_height_cm` | `INT` | 高度 |
| `product_width_cm` | `INT` | 宽度 |

### 4. `payments_raw`

| 字段 | 类型 | 含义 |
|---|---|---|
| `order_id` | `VARCHAR(50)` | 订单 ID |
| `payment_sequential` | `INT` | 支付序号 |
| `payment_type` | `VARCHAR(50)` | 支付方式 |
| `payment_installments` | `INT` | 分期数 |
| `payment_value` | `DECIMAL(10,2)` | 支付金额 |

**主键：** (`order_id`, `payment_sequential`) :contentReference[oaicite:45]{index=45}

### 5. `reviews_raw`

| 字段 | 类型 | 含义 |
|---|---|---|
| `review_id` | `VARCHAR(50)` | 评论 ID |
| `order_id` | `VARCHAR(50)` | 订单 ID |
| `review_score` | `INT` | 评论评分 |
| `review_comment_title` | `TEXT` | 评论标题 |
| `review_comment_message` | `TEXT` | 评论正文 |
| `review_creation_date` | `DATETIME` | 评论创建时间 |
| `review_answer_timestamp` | `DATETIME` | 回复时间 |

**主键：** (`review_id`, `order_id`) :contentReference[oaicite:46]{index=46}

### 6. `order_items_raw`

| 字段 | 类型 | 含义 |
|---|---|---|
| `order_id` | `VARCHAR(50)` | 订单 ID |
| `order_item_id` | `INT` | 订单内商品序号 |
| `product_id` | `VARCHAR(50)` | 商品 ID |
| `seller_id` | `VARCHAR(50)` | 卖家 ID |
| `shipping_limit_date` | `VARCHAR(32)` | 发货截止时间 |
| `price` | `DECIMAL(10,2)` | 商品价格 |
| `freight_value` | `DECIMAL(10,2)` | 运费 |

**主键：** (`order_id`, `order_item_id`) :contentReference[oaicite:47]{index=47}

### 7. `sellers_raw`

| 字段 | 类型 | 含义 |
|---|---|---|
| `seller_id` | `VARCHAR(50)` | 卖家 ID，主键 |
| `seller_zip_code_prefix` | `VARCHAR(5)` | 卖家邮编前缀 |
| `seller_city` | `VARCHAR(100)` | 卖家城市 |
| `seller_state` | `VARCHAR(5)` | 卖家所在州 |

:contentReference[oaicite:48]{index=48}

---

## 第 2 层 —— 数仓表（Warehouse Tables）

这一层是项目的核心分析仓库，主要由维度表和事实表组成。:contentReference[oaicite:49]{index=49}

### 1. `dim_user`

| 字段 | 类型 | 含义 |
|---|---|---|
| `user_id` | `VARCHAR(50)` | 数仓用户主键，来源于 `customer_id` |
| `unique_user_id` | `VARCHAR(50)` | 稳定用户唯一标识 |
| `city` | `VARCHAR(100)` | 城市 |
| `state` | `VARCHAR(10)` | 州 |

**主键：** `user_id` :contentReference[oaicite:50]{index=50}

### 2. `dim_product`

| 字段 | 类型 | 含义 |
|---|---|---|
| `product_id` | `VARCHAR(50)` | 商品 ID |
| `category` | `VARCHAR(100)` | 商品品类 |
| `weight_g` | `INT` | 重量 |
| `length_cm` | `INT` | 长度 |
| `height_cm` | `INT` | 高度 |
| `width_cm` | `INT` | 宽度 |

**主键：** `product_id` :contentReference[oaicite:51]{index=51}

### 3. `fact_order`

| 字段 | 类型 | 含义 |
|---|---|---|
| `order_id` | `VARCHAR(50)` | 订单 ID |
| `user_id` | `VARCHAR(50)` | 关联 `dim_user.user_id` |
| `order_status` | `VARCHAR(50)` | 订单状态 |
| `purchase_ts` | `DATETIME` | 下单时间 |
| `delivered_ts` | `DATETIME` | 实际送达时间 |
| `estimated_delivery_ts` | `DATETIME` | 预计送达时间 |
| `delivered_days` | `INT` | 从下单到送达的天数 |

**主键：** `order_id`  
**外键：** `user_id -> dim_user(user_id)`  
**索引：** `idx_order_user_purchase(user_id, purchase_ts)` :contentReference[oaicite:52]{index=52}

### 4. `fact_order_item`

| 字段 | 类型 | 含义 |
|---|---|---|
| `order_id` | `VARCHAR(50)` | 订单 ID |
| `order_item_id` | `INT` | 商品序号 |
| `product_id` | `VARCHAR(50)` | 商品 ID |
| `seller_id` | `VARCHAR(50)` | 卖家 ID |
| `shipping_limit_ts` | `DATETIME` | 发货时限时间 |
| `price` | `DECIMAL(10,2)` | 商品价格 |
| `freight_value` | `DECIMAL(10,2)` | 运费 |
| `gmv` | `DECIMAL(10,2)` | 交易额，定义为 `price + freight_value` |

**主键：** (`order_id`, `order_item_id`)  
**外键：** `order_id -> fact_order(order_id)`，`product_id -> dim_product(product_id)`  
**索引：** `idx_item_product(product_id)` :contentReference[oaicite:53]{index=53}

### 5. `fact_payment`

| 字段 | 类型 | 含义 |
|---|---|---|
| `order_id` | `VARCHAR(50)` | 订单 ID |
| `payment_sequential` | `INT` | 支付序号 |
| `payment_type` | `VARCHAR(50)` | 支付方式 |
| `payment_installments` | `INT` | 分期数 |
| `payment_value` | `DECIMAL(10,2)` | 支付金额 |

**主键：** (`order_id`, `payment_sequential`)  
**外键：** `order_id -> fact_order(order_id)` :contentReference[oaicite:54]{index=54}

### 6. `fact_review`

| 字段 | 类型 | 含义 |
|---|---|---|
| `review_id` | `VARCHAR(50)` | 评论 ID |
| `order_id` | `VARCHAR(50)` | 订单 ID |
| `review_score` | `INT` | 评论评分 |
| `review_comment_len` | `INT` | 评论文本长度 |
| `review_creation_ts` | `VARCHAR(32)` | 评论创建时间 |
| `review_answer_ts` | `VARCHAR(32)` | 评论回复时间 |

**主键：** `review_id`  
**外键：** `order_id -> fact_order(order_id)`  
**索引：** `idx_review_order(order_id)` :contentReference[oaicite:55]{index=55}

---

## ETL 与转换说明

ETL 过程先导入原始表，再生成数仓表。关键转换包括：

- `customers_raw` → `dim_user`
- `products_raw` → `dim_product`
- `orders_raw` 中字符串时间戳 → `fact_order` 中 `DATETIME`
- `delivered_days` 由下单时间和送达时间计算
- `fact_order_item.gmv = price + freight_value`
- `fact_review.review_comment_len` 由评论文本长度计算。:contentReference[oaicite:56]{index=56}

---

## 第 3 层 —— 分析视图（Analytical Views）

这些视图定义在 `create_views.sql` 中，是 notebook 和业务分析模块的通用语义层。:contentReference[oaicite:57]{index=57}

### 1. `view_user_behavior`
用户行为汇总视图。

**主要字段**
- `unique_user_id`
- `city`
- `state`
- `order_count`
- `total_spent`
- `avg_order_value`
- `last_purchase_date`
- `days_since_last_purchase`
- `first_purchase_date`
- `customer_lifetime_days`

**服务模块**
- 模块 02：RFM 分群
- 用户价值分析
- 个性化逻辑。:contentReference[oaicite:58]{index=58}

### 2. `view_product_sales`
商品级销售与评分汇总视图。

**主要字段**
- `product_id`
- `category`
- `sales_count`
- `total_revenue`
- `total_gmv`
- `avg_price`
- `avg_review_score`
- `review_count`
- `first_sale_date`
- `last_sale_date`

**服务模块**
- 商品排行
- 品类分析
- 推荐特征工程。:contentReference[oaicite:59]{index=59}

### 3. `view_category_sales`
基于商品销售视图滚动汇总的品类级视图。

**主要字段**
- `category`
- `product_count`
- `total_sales`
- `category_total_revenue`
- `avg_product_price`
- `avg_review_score`

**服务模块**
- 品类结构分析
- Pareto / BCG 风格分析。:contentReference[oaicite:60]{index=60}

### 4. `view_delivery_analysis`
订单级物流表现视图。

**主要字段**
- `order_id`
- `customer_state`
- `order_status`
- `delivered_days`
- `estimated_days`
- `is_delayed`
- `delay_days`
- `order_value`
- `review_score`

**服务模块**
- 模块 01：满意度与配送分析
- 区域物流分析。:contentReference[oaicite:61]{index=61}

### 5. `view_order_satisfaction`
订单级满意度标签视图。

**主要字段**
- `order_id`
- `user_id`
- `state`
- `purchase_ts`
- `delivered_days`
- `order_value`
- `review_score`
- `review_comment_len`
- `satisfaction_level`
- `delivery_period`

**服务模块**
- 满意度分组
- 配送周期比较
- 统计检验。:contentReference[oaicite:62]{index=62}

### 6. `view_order_complete`
宽表型订单分析视图。

**主要字段**
- 订单维度：`order_id`, `order_status`, `purchase_ts`, `delivered_ts`, `estimated_delivery_ts`, `delivered_days`
- 用户维度：`user_id`, `user_city`, `user_state`
- 商品维度：`product_category`, `product_id`
- 明细维度：`order_item_id`, `price`, `freight_value`, `gmv`, `seller_id`
- 卖家维度：`seller_city`, `seller_state`
- 支付维度：`payment_type`, `payment_installments`, `payment_value`
- 评论维度：`review_score`, `review_comment_len`
- 衍生标记：`is_delayed`, `is_satisfied`

**服务模块**
- 宽表型综合分析
- 后续 notebook 特征提取。:contentReference[oaicite:63]{index=63}

### 7. `view_category_analysis`
品类业务策略视图。

**主要字段**
- `category`
- `order_count`
- `customer_count`
- `total_revenue`
- `total_gmv`
- `avg_price`
- `avg_freight`
- `avg_review_score`
- `bad_review_rate`
- `avg_comment_len`
- `repeat_rate`
- `first_sale_date`
- `last_sale_date`
- `category_lifetime_days`

**服务模块**
- 模块 03：产品类别分析。:contentReference[oaicite:64]{index=64}

### 8. `view_geographic_state_summary`
州级 KPI 汇总视图。

**主要字段**
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
- `repeat_rate`

**服务模块**
- 模块 04：地理区域分析
- 州级聚类
- 区域物流与满意度比较。:contentReference[oaicite:65]{index=65}

### 9. `view_geographic_city_summary`
城市级 KPI 汇总视图。

**主要字段**
- `customer_state`
- `customer_city`
- `order_count`
- `customer_count`
- `total_gmv`
- `total_revenue`
- `avg_order_value`
- `avg_delivery_days`
- `avg_freight_cost`
- `avg_review_score`
- `bad_review_rate`

**服务模块**
- 模块 04：城市集中度分析。:contentReference[oaicite:66]{index=66}

### 10. `view_buyer_seller_distance`
买家–卖家地理关系视图。

**主要字段**
- `order_id`
- `buyer_state`
- `buyer_city`
- `seller_state`
- `seller_city`
- `trade_type`（`Same State` / `Cross State`）
- `delivered_days`
- `freight_value`
- `gmv`
- `review_score`

**服务模块**
- 同州 / 跨州物流比较
- 路径压力分析。:contentReference[oaicite:67]{index=67}

### 11. `view_user_clv_features`
客户级 CLV 特征视图。

**主要字段**
- `customer_unique_id`
- `total_orders`
- `total_gmv`
- `avg_order_value`
- `first_order_date`
- `last_order_date`
- `customer_lifetime_days`
- `days_since_last_order`
- `monthly_frequency`
- `unique_products_purchased`
- `unique_categories_purchased`
- `avg_payment_value`
- `max_installments_used`
- `avg_review_score`
- `satisfaction_rate`
- `bad_review_count`
- `avg_delivery_delay`
- `delay_rate`

**服务模块**
- 模块 07：CLV 预测。:contentReference[oaicite:68]{index=68}

### 12. `view_user_future_gmv`
CLV 目标值视图。

**主要字段**
- `customer_unique_id`
- `future_6m_gmv`
- `future_6m_orders`
- `is_active_future`

**服务模块**
- CLV 标签构建
- 未来价值建模。:contentReference[oaicite:69]{index=69}

---

## 额外 SQL 资产

这些 SQL 文件用于补充特征工程和模块化建模。

### 1. `create_view_user_churn_labels.sql`
创建基于快照的流失标签表 `churn_labels_tmp`。

**核心概念**
- `snapshot_id`
- `obs_date`
- `snapshot_key`
- `unique_user_id`
- `first_purchase_date`
- `last_purchase_date`
- `total_orders`
- `total_gmv`
- `days_since_last_order`
- `customer_age_days`
- 多时间窗流失标签：
  - `is_churned_30d`
  - `is_churned_60d`
  - `is_churned_90d`
  - `is_churned_180d`
  - `is_churned_270d`

**服务模块**
- 模块 06：客户流失预测
- snapshot-based retention modeling。:contentReference[oaicite:70]{index=70}

### 2. `user_category_preference.sql`
用户–品类偏好汇总。

| 字段 | 含义 |
|---|---|
| `unique_user_id` | 用户 ID |
| `category` | 商品品类 |
| `category_purchases` | 该品类购买次数 |
| `category_gmv` | 该品类 GMV |

**服务模块**
- 推荐系统个性化
- 用户偏好画像。:contentReference[oaicite:71]{index=71}

### 3. `user_satisfaction_features.sql`
用户级满意度与配送特征。

| 字段 | 含义 |
|---|---|
| `unique_user_id` | 用户 ID |
| `avg_rating` | 平均评分 |
| `rating_std` | 评分波动 |
| `bad_review_count` | 差评数 |
| `avg_delivery_days` | 平均送达天数 |
| `delayed_orders` | 延迟订单数 |

**服务模块**
- 流失特征
- CLV / 满意度增强特征
- 推荐用户画像。:contentReference[oaicite:72]{index=72}

---

## 表关系总结

### 核心关系流

```text
customers_raw ──> dim_user ──┐
                             ├── fact_order ──┬── fact_order_item ──> dim_product
orders_raw ──────────────────┘                ├── fact_payment
                                              └── fact_review

products_raw ──> dim_product
payments_raw ──> fact_payment
reviews_raw  ──> fact_review
order_items_raw ──> fact_order_item
sellers_raw ──> 宽表视图中的卖家属性
```
这个数仓结构为 8 个分析模块提供了统一数据基础，并通过共享 SQL views 连接到 notebook 和业务输出层。

## 模块映射

| 模块          | 主要数据资产                                                                                        |
| ----------- | --------------------------------------------------------------------------------------------- |
| 01 满意度与配送分析 | `view_delivery_analysis`, `view_order_satisfaction`, `fact_order`, `fact_review`              |
| 02 RFM 分群   | `view_user_behavior`                                                                          |
| 03 产品类别分析   | `view_category_analysis`, `view_category_sales`, `view_product_sales`                         |
| 04 地理区域分析   | `view_geographic_state_summary`, `view_geographic_city_summary`, `view_buyer_seller_distance` |
| 05 时间序列分析   | `fact_order`, `fact_order_item`, `dim_product` 及 notebook 中按时间聚合的数据                           |
| 06 客户流失预测   | `churn_labels_tmp`, `view_user_behavior`, 用户级工程化特征                                            |
| 07 CLV 预测   | `view_user_clv_features`, `view_user_future_gmv`                                              |
| 08 推荐系统     | 基于 `fact_order_item`, `fact_review`, `dim_product` 构建的用户–商品交互数据，以及用户增强特征                      |
这与 portfolio deck 中描述的整体项目架构一致：原始数据 → ETL → MySQL warehouse → 分析与建模模块 → 业务洞察输出。

## 备注
- 这个数仓更接近一个务实的星型分析仓库，而不是完全企业级标准化仓库。
- 很多模块级分析数据集是在 notebook 中基于 warehouse views 二次构建的，而不是永久存储为数据库表。
- Churn 与 CLV 两个模块都明显依赖时间窗和快照逻辑，而不是只依赖静态用户汇总。
