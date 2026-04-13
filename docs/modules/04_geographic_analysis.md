# Module 04 — Geographic Analysis

## Overview

This module analyzes e-commerce performance from a geographic perspective, focusing on how regional market value, logistics performance, customer satisfaction, and product demand structure vary across Brazilian states and cities.

Rather than treating geography as a background attribute, this module uses region as a business decision layer. The analysis identifies core regional markets, high-potential markets, logistics-stressed markets, and priority problem regions, then translates those findings into differentiated regional strategy recommendations.

---

## Business Question

This module is designed to answer the following core questions:

1. Which states and cities are the strongest commercial markets?
2. How concentrated is regional sales performance?
3. How much of the logistics gap is driven by cross-state trade structure?
4. Which regions combine commercial importance with weak customer experience?
5. Do different regions show different product-demand structures?
6. Can regional markets be grouped into interpretable business types for strategy planning?

From a business perspective, this module supports regional prioritization, logistics improvement, market expansion sequencing, and state-level operational strategy.

---

## Data Source

This module combines multiple geography-related datasets built from the MySQL warehouse.

### 1. State-level summary dataset
Used for regional KPI comparison, concentration analysis, and clustering.

Main fields include:
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
- repeat-purchase proxy

This table covers:
- **27 Brazilian states / federal units**
- full national coverage
- no missing values

### 2. City-level summary dataset
Used for urban concentration analysis and top-city ranking.

### 3. Buyer–seller route dataset
Used for:
- same-state vs cross-state trade comparison
- route-level logistics analysis
- freight and delivery-pressure analysis

### 4. Order-level detailed dataset
Used for:
- category preference analysis
- state-level satisfaction structure
- state-category GMV comparison

The module keeps transaction-level detail where needed instead of relying only on aggregated tables.

---

## Methodology

### 1. Data Validation and Preparation
The analysis begins with:
- data structure checks
- missing-value review
- dataset-specific subsets for delivery, review, and route analysis

This avoids unnecessary global row deletion while preserving analytical flexibility.

### 2. Exploratory Regional Analysis
EDA is used to understand:
- state-level sales distribution
- state coverage
- regional concentration
- scale differences across states

This includes:
- numerical distribution analysis
- state ranking tables
- preliminary concentration checks

### 3. Regional Sales Ranking and Concentration
The module compares states by:
- `total_gmv`
- `order_count`
- `avg_order_value`

It then measures regional concentration using:
- GMV share analysis
- core-state contribution analysis
- Lorenz curve
- Gini coefficient

### 4. Geographic Visualization
The notebook adds spatial views through:
- state-level bubble maps
- top-city ranking visuals
- city concentration analysis within top states

### 5. Regional Segmentation with Clustering
State-level clustering is built using features covering:
- market scale
- customer value
- logistics quality
- customer satisfaction

Clustering variables include:
- `total_gmv`
- `avg_order_value`
- `avg_review_score`
- `avg_delivery_days`
- `delay_rate`
- `avg_freight_cost`

Model selection uses:
- inertia
- silhouette score
- Davies–Bouldin score

The final chosen solution is:
- **K = 4**

The clusters are then translated into business names.

### 6. Logistics Performance Analysis
The module compares:
- delivery speed by state
- delay rate by state
- freight cost by state
- same-state vs cross-state trade
- major buyer–seller routes
- freight cost vs delivery speed relationship

It also creates a logistics-risk view to identify states under structural service pressure.

### 7. Satisfaction and Problem-Region Analysis
To connect operations with customer experience, the module evaluates:
- average review score by state
- bad-review rate by state
- satisfaction vs logistics relationship
- high-volume weak-satisfaction states
- satisfaction profile by regional cluster

### 8. Regional Product Preference Analysis
The module extends into product strategy by analyzing:
- top categories by state
- category-preference heatmaps
- Location Quotient (LQ) for state specialty categories
- category structure by regional cluster
- category structure in priority problem regions

### 9. Statistical Validation
The main geographic findings are validated using:
- ANOVA for satisfaction differences across regional clusters
- chi-square test for state vs satisfaction-level association
- correlation analysis between delay, review score, and bad-review rate

### 10. Regional Strategy Translation
The module concludes by converting the findings into:
- market-type strategy
- priority problem-region action table
- final regional operating logic

---

## Key Findings

### 1. Regional sales are highly concentrated
The platform has full national coverage across all **27** Brazilian states, but sales are highly uneven.

Key concentration results:
- `SP` alone contributes about **37.39%** of total GMV
- `SP + RJ + MG` together contribute about **62.54%**
- top 10 states contribute about **87.38%**
- only **7 core states** contribute about **80%** of GMV
- state-level GMV **Gini coefficient = 0.7032**

This means the business depends strongly on a small number of regional markets.

### 2. Large markets are mainly driven by scale, not necessarily by high order value
State rankings by `total_gmv` and `order_count` are highly consistent, which suggests that leading regions are primarily strong because of transaction volume.

By contrast, the `avg_order_value` ranking looks different. States such as `PB`, `AL`, and `RO` appear stronger on a per-order basis even though they are not the largest markets in absolute GMV.

This means:
- some states are **scale-driven core markets**
- some smaller states are **high-value potential markets**

### 3. City-level concentration is even stronger than state-level concentration
At the city level, `sao paulo` dominates by a very large margin, followed by `rio de janeiro`.

Within top states, internal concentration also differs:
- `RJ` is highly concentrated, with `rio de janeiro` contributing about **54.24%** of state-level city GMV
- `MG` is much less concentrated, with `belo horizonte` contributing only about **22.48%**

This means some strong states depend heavily on a single metropolitan center, while others are supported by a broader urban base.

### 4. A 4-cluster regional segmentation produces clear market types
The final K-Means solution uses **K = 4** and creates four interpretable regional groups:

- **Balanced Core Markets**
- **High-AOV Potential Markets**
- **Logistics-Stressed Markets**
- **Super Core Outlier Market**

Cluster profiles:

| Cluster Name | State Count | Total GMV | Avg Order Value | Avg Review Score | Avg Delivery Days | Delay Rate | Avg Freight Cost |
|---|---:|---:|---:|---:|---:|---:|---:|
| Balanced Core Markets | 9 | 829,470.36 | 167.33 | 4.08 | 14.34 | 7.34 | 24.74 |
| High-AOV Potential Markets | 9 | 103,874.92 | 221.27 | 4.09 | 20.82 | 6.22 | 40.93 |
| Logistics-Stressed Markets | 8 | 193,209.16 | 211.72 | 3.80 | 22.54 | 14.00 | 39.97 |
| Super Core Outlier Market | 1 | 5,939,079.38 | 142.27 | 4.18 | 8.70 | 4.37 | 17.37 |

This segmentation shows that regional performance is not one-dimensional. Market scale, customer value, logistics, and satisfaction interact in different ways.

### 5. Cross-state trade is a major structural driver of logistics pressure
The module finds a very large gap between same-state and cross-state transactions:

- **Same State avg delivery days = 7.87**
- **Cross State avg delivery days = 14.99**
- **Same State avg freight value = 13.46**
- **Cross State avg freight value = 23.68**

A Welch’s t-test confirms the delivery-time difference is extremely significant:
- **t = -145.4815**
- **p < 0.001**

This is one of the strongest operational findings in the module: inter-state trade structure is a major source of delivery pressure, cost burden, and weaker customer experience.

### 6. A meaningful share of logistics is both costly and slow
The freight-vs-delivery analysis shows that expensive shipping does not automatically result in faster delivery.

A notable result is that:
- about **30.88%** of valid records fall into the joint area of **high cost + slow delivery**

This suggests an important portion of logistics activity is both operationally inefficient and expensive.

### 7. Customer satisfaction differences align strongly with logistics pressure
State-level and cluster-level comparisons show that satisfaction is not randomly distributed.

Cluster-level satisfaction profile:

| Cluster Name | Avg Review Score | Bad Review Rate | Avg Delivery Days | Delay Rate |
|---|---:|---:|---:|---:|
| Super Core Outlier Market | 4.18 | 12.59 | 8.70 | 4.37 |
| High-AOV Potential Markets | 4.09 | 14.21 | 20.82 | 6.22 |
| Balanced Core Markets | 4.08 | 14.81 | 14.34 | 7.34 |
| Logistics-Stressed Markets | 3.80 | 20.99 | 22.54 | 14.00 |

The weakest-performing group is clearly **Logistics-Stressed Markets**, where poor logistics and weak satisfaction overlap.

### 8. Priority problem regions are commercially meaningful, not marginal
The notebook identifies high-volume states with below-median satisfaction as priority concern areas.

Representative priority problem regions include:
- `RJ`
- `BA`
- `CE`
- `ES`
- `GO`
- `PA`
- `PE`

Among them, `RJ` stands out as the most urgent high-impact recovery market because it combines:
- high order volume
- weak average review score
- high bad-review rate
- elevated delay rate

### 9. Regional demand structure has a shared core but also meaningful variation
Across major states, several categories repeatedly appear among top GMV drivers, including:
- `beleza_saude`
- `relogios_presentes`
- `esporte_lazer`
- `informatica_acessorios`

However, category mix is not identical across states. Some states show stronger relative concentration in specific categories.

This means regional product strategy should combine:
- national assortment consistency
- selective local adaptation

### 10. The main findings are strongly supported by statistical evidence
The module validates its main conclusions using multiple methods:

- ANOVA for satisfaction differences across regional clusters:
  - **F = 32.4459**
  - **p < 0.001**
  - **eta-squared = 0.7383**

- Chi-square for `state × satisfaction_level`:
  - **χ² = 683.0632**
  - **df = 18**
  - **p < 0.001**

- Correlation results:
  - `delay_rate` vs `avg_review_score`: **r = -0.805**
  - `delay_rate` vs `bad_review_rate`: **r = 0.808**

These results make the interpretation coherent: logistics reliability, regional type, and customer satisfaction are structurally linked.

---

## Key Metrics

| Metric | Result |
|---|---:|
| Number of states covered | 27 |
| SP GMV share | 37.39% |
| Top 3 states GMV share | 62.54% |
| Top 10 states GMV share | 87.38% |
| Core states contributing ~80% GMV | 7 |
| State-level GMV Gini coefficient | 0.7032 |
| Chosen number of clusters | 4 |
| Same-state avg delivery days | 7.87 |
| Cross-state avg delivery days | 14.99 |
| Same-state avg freight value | 13.46 |
| Cross-state avg freight value | 23.68 |
| High cost + slow delivery share | 30.88% |
| Cluster ANOVA F-statistic | 32.4459 |
| Cluster ANOVA p-value | < 0.001 |
| Eta-squared | 0.7383 |
| Chi-square statistic | 683.0632 |
| Chi-square degrees of freedom | 18 |
| Chi-square p-value | < 0.001 |
| Correlation: delay_rate vs avg_review_score | -0.805 |
| Correlation: delay_rate vs bad_review_rate | 0.808 |

---

## Regional Segment Interpretation

### Super Core Outlier Market
This cluster is represented by a single structurally dominant market.

**Profile**
- overwhelming GMV scale
- strongest logistics performance
- strongest satisfaction performance

**Strategic direction**
- protect leadership
- defend service quality
- deepen retention and value extraction

---

### Balanced Core Markets
These states provide a broad, stable commercial base.

**Profile**
- meaningful GMV scale
- relatively solid satisfaction
- manageable logistics pressure

**Strategic direction**
- stabilize and expand efficiently
- support assortment and logistics capacity
- maintain core regional resilience

---

### High-AOV Potential Markets
These states are not the largest markets, but they show stronger per-order spending.

**Profile**
- high average order value
- moderate scale
- acceptable satisfaction
- higher freight burden than core markets

**Strategic direction**
- grow selectively
- expand where purchasing power is visible
- avoid overexpansion before scale and logistics justify it

---

### Logistics-Stressed Markets
These states combine weak service quality with operational pressure.

**Profile**
- longest delivery times
- highest delay rate
- weakest satisfaction
- high freight burden

**Strategic direction**
- repair operations before scaling
- improve route reliability
- reduce delivery pressure
- stabilize customer experience

---

## Business Recommendations

Based on the findings, the module recommends the following strategy logic:

1. **Protect the core first**  
   Core value is still concentrated in the strongest markets, especially the Super Core Outlier Market and the broader Balanced Core Markets.

2. **Expand selectively, not uniformly**  
   High-AOV Potential Markets justify growth only when purchasing power is visible and operational conditions remain manageable.

3. **Repair weak service regions before scaling them**  
   Logistics-Stressed Markets and priority problem regions should not be pushed aggressively for growth before logistics and customer experience improve.

4. **Use cross-state trade structure as an operating warning signal**  
   Cross-state exposure should be monitored because it is one of the clearest structural drivers of delay and freight pressure.

5. **Combine geography with product strategy**  
   Regional demand is not identical, so assortment, campaigns, and category emphasis should reflect both shared national demand and local variation.

6. **Make regional risk operationally visible**  
   Metrics such as delay rate, bad-review rate, and route pressure should be tracked together rather than in isolation.

---

## Technical Implementation

This module demonstrates the following technical capabilities:

- state-level and city-level geographic KPI analysis
- concentration measurement using share analysis, Lorenz curve, and Gini coefficient
- map-based and city-based geographic visualization
- K-Means regional segmentation
- route-level logistics analysis
- same-state vs cross-state trade comparison
- risk-state identification
- state-level product preference analysis
- Location Quotient (LQ) analysis
- ANOVA, chi-square, and correlation-based validation
- export of regional strategy tables for downstream reporting

---

## Files and Deliverables

Primary notebook:
- `Statistical_analysis_report/04_Geographic_Analysis.ipynb`

Core exported outputs include:
- `output/04_geographic_analysis/state_clustered_results.csv`
- `output/04_geographic_analysis/priority_problem_region_actions.csv`
- `output/04_geographic_analysis/market_type_strategy.csv`
- `output/04_geographic_analysis/final_regional_conclusion.csv`
- `output/04_geographic_analysis/cluster_satisfaction_profile.csv`
- `output/04_geographic_analysis/problem_region_category_share.csv`
- `output/04_geographic_analysis/statistical_validation_summary.csv`
- `output/04_geographic_analysis/regional_key_findings.json`

Potential visual deliverables include:
- state-level bubble map
- city GMV ranking plots
- concentration plots
- cluster visualizations
- problem-region comparison charts
- category heatmaps

---

## Module Position in the Full Project

This module forms the **regional strategy layer** of the broader e-commerce decision-intelligence system.

It connects naturally with:
- product category analysis
- satisfaction analysis
- time-series demand monitoring
- churn and CLV prioritization
- future dashboard and business reporting

It expands the project from user- and product-level analysis into geographic operating strategy.

---

## Next-Step Notes

Future improvements for this module may include:

- adding seller-side geography and warehouse logic
- connecting route pressure with seller performance
- introducing choropleth maps and richer geospatial visuals
- combining regional strategy with margin or profitability measures
- integrating geographic KPIs into the future Streamlit dashboard