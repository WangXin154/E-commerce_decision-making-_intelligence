# Module 03 — Product Category Analysis

## Overview

This module analyzes product-category performance from multiple business perspectives, including sales scale, revenue concentration, pricing structure, customer satisfaction, temporal behavior, and strategic category grouping.

The purpose of this module is not only to rank categories by revenue, but also to identify which categories should be protected, improved, selectively scaled, or managed as long-tail segments. It therefore acts as the category-portfolio strategy layer of the broader e-commerce intelligence system.

---

## Business Question

This module is designed to answer the following core questions:

1. Which product categories are the main revenue and order-volume drivers?
2. Which categories show strong customer satisfaction and future growth potential?
3. Which categories are commercially important but operationally problematic?
4. How concentrated is the category portfolio, and what does that imply for strategy?

From a business perspective, this module translates category-level sales and satisfaction metrics into category strategy decisions such as prioritization, quality improvement, growth investment, and long-tail management.

---

## Data Source

This module uses two analytical datasets derived from the MySQL warehouse:

### 1. Category-level aggregated dataset
Each row represents one product category and contains key performance indicators such as:
- order count
- customer count
- total revenue
- total GMV
- average price
- average freight
- average review score
- bad review rate
- repeat proxy
- category lifetime

This dataset contains:
- **73 product categories**
- **14 variables**
- no missing values in the category-level table

### 2. Order-level transaction dataset
A more detailed order-item level dataset is used for price, review, time, and satisfaction analysis.

This dataset contains:
- **111,426 transaction records**
- **12 variables**

Some missing values exist in behavior-specific fields such as:
- `delivered_days`
- `review_score`
- `review_comment_len`

These missing values are relatively limited and are handled through task-specific subsets rather than global row deletion.

---

## Methodology

### 1. Data Loading and Structure Validation
The module first validates:
- field structure
- data types
- completeness
- category uniqueness
- transaction coverage

This ensures that category-level and order-level analyses can be combined safely.

### 2. Exploratory Data Analysis
EDA is used to understand the category portfolio before strategic interpretation.

Main checks include:
- missing-value review
- numerical distributions
- descriptive statistics
- outlier detection using the IQR rule
- boxplots for sales, price, freight, review score, and bad-review rate

The analysis shows that the category portfolio is highly uneven, with sales and revenue concentrated in a limited number of categories.

### 3. Category Ranking and Pareto Analysis
The notebook ranks categories by:
- order count
- total revenue
- customer count
- satisfaction-related metrics

A Pareto analysis is then used to identify the core revenue-driving categories.

Key result:
- **16 categories** account for around **80%** of platform revenue

This means the platform depends heavily on a relatively small set of categories.

### 4. BCG-Style Strategic Classification
The module applies a BCG-style matrix using category revenue and category satisfaction as strategic axes.

Categories are grouped into:
- **Star**
- **Problem**
- **Opportunity**
- **Dog**

This moves the analysis from pure ranking into decision-oriented portfolio management.

### 5. Customer Preference by Segment
The category analysis is linked with the earlier RFM segmentation logic to compare category preference across customer groups.

This helps answer:
- which categories matter across all segments
- which categories are more concentrated in higher-value clusters
- where category demand is broad versus segment-specific

### 6. Pricing and Satisfaction Analysis
At the order level, the module investigates:
- price distributions across major categories
- category-level review structure
- bad-review-rate patterns
- category satisfaction composition

### 7. Time and Geography Extensions
The notebook extends the category analysis into:
- monthly trend patterns for major categories
- category performance by region
- state-level category share differences

This helps connect category strategy with time and geography.

### 8. Statistical Validation
To test whether observed category differences are statistically meaningful, the module uses:

- **Chi-square test** for category vs. satisfaction level
- **One-way ANOVA** for price differences across categories
- **Correlation analysis** for category metrics

This gives the module both descriptive and inferential strength.

---

## Key Findings

### 1. Category sales are highly concentrated
The platform’s category structure is not evenly distributed.

Key findings include:
- the platform contains **73** categories
- only **16 categories** contribute roughly **80%** of total revenue
- the largest revenue category is **`beleza_saude`**

This means the platform relies strongly on a limited group of commercially important categories.

### 2. Revenue is mainly driven by sales volume rather than price
The correlation between `order_count` and `total_revenue` is extremely strong:

- **r = 0.96**

This indicates that the strongest revenue categories are also the categories with the largest sales volume, rather than simply the most expensive categories.

### 3. Satisfaction differences exist, but they are smaller than sales differences
Category performance varies far more in commercial scale than in average review score.

Descriptive analysis shows:
- `order_count` and `total_revenue` are strongly right-skewed
- `avg_review_score` is much more concentrated around the low-4 range
- `avg_price`, `avg_freight`, and `bad_review_rate` show meaningful variation across categories

This suggests that category strategy should not be based on sales alone.

### 4. Several high-revenue categories also show experience risk
The BCG-style analysis identifies categories that are commercially strong but still have weaker-than-median satisfaction performance.

Examples of **Problem** categories include:
- `cama_mesa_banho`
- `moveis_decoracao`
- `informatica_acessorios`

These categories are strategically important because they generate major revenue, but they also carry customer-experience risk.

### 5. Star categories combine scale with relatively strong satisfaction
Examples of **Star** categories include:
- `beleza_saude`
- `esporte_lazer`
- `cool_stuff`
- `automotivo`

These categories already perform well commercially while maintaining above-median satisfaction, which makes them strong candidates for continued resource support.

### 6. Category and satisfaction are statistically associated
The chi-square test for category and satisfaction level shows:

- **χ² = 330.17**
- **degrees of freedom = 18**
- **p < 0.001**

This indicates that satisfaction outcomes are not evenly distributed across categories.

The visual interpretation suggests that categories such as:
- `cama_mesa_banho`
- `informatica_acessorios`
- `moveis_decoracao`

have relatively larger low-satisfaction shares, while:
- `beleza_saude`
- `brinquedos`

show a stronger high-satisfaction composition.

### 7. Price differences across categories are statistically significant
The one-way ANOVA result confirms that average product prices differ significantly across major categories:

- **F = 328.28**
- **p < 0.001**

This means category pricing structures are meaningfully different, not random.

For example:
- categories such as `relogios_presentes` and `informatica_acessorios` tend to have higher price levels
- categories such as `telefonia` and `brinquedos` are relatively lower-priced

### 8. Review risk and review score are strongly inverse
The correlation matrix shows that:

- `bad_review_rate` and `avg_review_score` have a very strong negative relationship: **r = -0.96**
- `avg_price` and `avg_review_score` are almost unrelated: **r = 0.02**

This suggests that customer satisfaction is not determined simply by higher prices. Instead, bad-review structure is a much more direct signal of category experience quality.

### 9. Segment-level preference is not identical across customer groups
The notebook suggests that major customer groups share some common core categories, but their spending structures differ.

A notable finding is that:
- **Cluster 1** contributes the highest GMV across most major categories
- higher-value groups are more concentrated in selected categories

This means category strategy can be linked with customer segmentation rather than treated as a purely product-side problem.

### 10. The portfolio is diverse, but strategic value is concentrated
The KPI-style summary shows:
- total categories: **73**
- total revenue: **R$13.45 million**
- total orders: **98,019**
- average review score: **4.02**
- core categories contributing ~80% revenue: **16**
- **19 Star** categories
- **18 categories** in each of the other three strategic groups

This means the category portfolio is broad, but business value is concentrated in a small subset of strategically important categories.

---

## Key Metrics

| Metric | Result |
|---|---:|
| Number of categories | 73 |
| Category-level variables | 14 |
| Order-level transaction records | 111,426 |
| Core categories contributing ~80% revenue | 16 |
| Total platform revenue | R$13.45 million |
| Total orders | 98,019 |
| Average category-level review score | 4.02 |
| Chi-square statistic | 330.17 |
| Chi-square degrees of freedom | 18 |
| Chi-square p-value | < 0.001 |
| ANOVA F-statistic | 328.28 |
| ANOVA p-value | < 0.001 |
| Correlation: order_count vs total_revenue | 0.96 |
| Correlation: bad_review_rate vs avg_review_score | -0.96 |
| Correlation: avg_price vs avg_review_score | 0.02 |

---

## Strategic Interpretation

### Star Categories
These categories combine strong revenue performance with relatively strong satisfaction.

**Examples**
- `beleza_saude`
- `esporte_lazer`
- `cool_stuff`
- `automotivo`

**Strategic direction**
- maintain visibility
- strengthen supply and inventory support
- continue promotional prioritization

---

### Problem Categories
These categories are commercially important but show below-median satisfaction or higher experience risk.

**Examples**
- `cama_mesa_banho`
- `moveis_decoracao`
- `informatica_acessorios`

**Strategic direction**
- improve product quality and expectation management
- monitor logistics burden and after-sales issues
- reduce review-risk drivers

---

### Opportunity Categories
These categories have relatively strong satisfaction but lower current scale.

**Strategic direction**
- selective growth investment
- targeted promotion
- controlled exposure expansion

---

### Dog / Long-Tail Categories
These categories contribute less revenue and do not currently stand out on satisfaction.

**Strategic direction**
- maintain low-cost operations
- avoid over-allocation of resources
- manage as long-tail support categories unless new evidence emerges

---

## Business Recommendations

Based on the findings, the module recommends the following actions:

1. **Protect the core revenue base**  
   Ensure inventory, promotion, and supply stability in major core categories.

2. **Fix high-revenue problem categories first**  
   The biggest business leverage comes from improving customer experience in categories that already generate meaningful revenue.

3. **Scale high-satisfaction opportunity categories selectively**  
   These categories may offer lower-risk growth.

4. **Link category strategy with customer segmentation**  
   Category management should not be isolated from user-value structure.

5. **Use category risk metrics as operational monitoring signals**  
   Review-score distribution and bad-review-rate should be tracked alongside revenue metrics.

---

## Technical Implementation

This module demonstrates the following technical capabilities:

- category-level KPI analysis
- multi-granularity analysis using aggregated and transaction-level data
- IQR-based outlier detection
- Pareto analysis
- BCG-style strategic classification
- customer-segment preference comparison
- category-level time and geographic extensions
- chi-square testing
- ANOVA for pricing differences
- correlation analysis for portfolio interpretation
- export of reusable category strategy outputs

---

## Files and Deliverables

Primary notebook:
- `Statistical_analysis_report/03_Product_Category_Analysis.ipynb`

Main exported files include:
- `output/category_bcg_classification.csv`
- `output/core_categories_pareto.csv`
- `output/category_strategy_groups.json`

Possible analytical outputs include:
- category ranking tables
- Pareto charts
- BCG-style classification tables
- pricing boxplots
- satisfaction composition visuals
- category-metric correlation heatmaps

---

## Module Position in the Full Project

This module forms the **product portfolio strategy layer** of the broader e-commerce decision-intelligence system.

It connects naturally with:
- user segmentation
- regional analysis
- time-series analysis
- recommendation design
- business reporting

It helps move the project beyond customer-only analysis into product-side business decision support.

---

## Next-Step Notes

Future improvements for this module may include:

- linking category strategy with margin or profitability measures
- adding seller-level category performance
- incorporating sentiment analysis from review text
- connecting category strategy with recommender-system weighting
- integrating category portfolio views into the future dashboard