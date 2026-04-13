# Module 01 — Satisfaction vs Delivery

## Overview

This module examines the relationship between delivery performance and customer satisfaction in an e-commerce setting. The analysis focuses on whether delayed delivery is associated with lower review scores and lower satisfaction probability, and whether this relationship remains statistically meaningful across multiple analytical methods.

This module serves as one of the foundational business-analysis components in the project because it links operational performance directly to customer experience.

---

## Business Question

This module is designed to answer two core questions:

1. Are delayed orders more likely to generate low customer satisfaction?
2. Is the relationship between delivery delay and satisfaction statistically significant and operationally meaningful?

From a business perspective, this module helps determine whether logistics performance should be treated as a core driver of retention and service quality management.

---

## Data Source

The analysis is based on order-level and review-level data derived from the Olist Brazilian e-commerce dataset. The key variables used in this module include:

- `delivered_days`
- `is_delayed`
- `review_score`
- `is_satisfied`
- `order_value`

The data was joined and cleaned before statistical analysis and modeling.

---

## Methodology

This module combines exploratory analysis, statistical inference, and predictive modeling.

### 1. Exploratory Data Analysis
The first step examines the distributions of delivery duration, order value, and customer review score. This helps identify skewness, outliers, and potential non-linear effects.

Main checks include:
- distribution plots
- box plots
- correlation heatmap
- multicollinearity check using VIF
- IQR-based outlier diagnostics

### 2. Statistical Testing
To validate the relationship between delay and satisfaction, several statistical methods are used:

- contingency table analysis
- chi-square test
- Welch’s t-test
- one-way ANOVA
- OLS regression

This combination provides both categorical and continuous perspectives on satisfaction outcomes.

### 3. Predictive Modeling
The module also includes classification-oriented modeling to assess whether logistics variables can predict satisfaction outcomes.

Models and techniques used include:
- logistic regression
- multivariate logistic regression
- Random Forest
- XGBoost
- ROC comparison
- threshold optimization using a cost-sensitive framework

### 4. Feature Engineering
To improve model flexibility, the module introduces:
- log transformation of order value
- non-linear delivery terms
- interaction terms between delivery and value-related features

---

## Key Findings

### 1. Delivery delay has a strong negative relationship with customer satisfaction
The analysis shows a substantial drop in satisfaction among delayed orders.

From the contingency table:
- non-delayed orders: 85,626 satisfied vs 22,272 dissatisfied
- delayed orders: 1,931 satisfied vs 5,617 dissatisfied

This translates into:
- satisfaction rate of about **79%** for non-delayed orders
- satisfaction rate of about **25%** for delayed orders
- a drop of about **54 percentage points**

This is the clearest business signal in the module: delivery delay is strongly associated with dissatisfaction.

### 2. Statistical evidence is extremely strong
The chi-square test shows an extremely significant relationship between delay status and satisfaction:

- **Chi-square = 11131.46**
- **p < 0.001**

This indicates that delay and satisfaction are not independent and that the observed difference is highly unlikely to be due to chance.

### 3. Logistics variables are more important than order value
The correlation analysis shows:
- `delivered_days` and `is_delayed` are positively related
- both `delivered_days` and `is_delayed` are negatively correlated with satisfaction
- `order_value` has only a weak direct linear relationship with satisfaction

This suggests that service execution matters more than basket value in explaining customer experience in this dataset.

### 4. Delay reduces both satisfaction probability and average review score
Welch’s t-test confirms that delayed orders have significantly lower mean review scores than on-time orders, with **p < 0.001**. The effect size is also described as practically meaningful, not only statistically significant.

The ANOVA analysis further suggests a dose–response pattern:
- shorter delivery durations have the highest satisfaction
- moderate delays reduce satisfaction
- severe delays reduce satisfaction further

This means the impact is not merely binary; longer delivery duration progressively erodes customer experience.

### 5. Logistic regression shows a large operational effect
The simple logistic regression result shows:

- coefficient for delay: **β₁ = -2.41**
- odds ratio: **0.089**

This means delayed orders are only about **8.9% as likely** to achieve positive satisfaction outcomes compared with non-delayed orders, or roughly **11 times less likely** to produce a satisfied customer.

### 6. Predictive power exists, but logistics alone is not enough
The notebook shows that logistics-related features do have predictive value, but performance remains moderate:

- ROC-AUC is around **0.660**

This means delivery timing matters, but it does not fully explain satisfaction on its own. Additional variables such as product characteristics, return behavior, and service interactions would likely improve the model.

### 7. Threshold optimization improves business alignment
The module also explores threshold optimization from a cost-sensitive perspective and identifies an operating threshold near **0.37**, rather than the default 0.50.

This is important because in business settings, missing a high-risk dissatisfaction case can be more costly than investigating a false alarm.

---

## Key Metrics

| Metric | Result |
|---|---:|
| Non-delayed satisfaction rate | ~79% |
| Delayed satisfaction rate | ~25% |
| Satisfaction gap | ~54 percentage points |
| Chi-square statistic | 11131.46 |
| Chi-square p-value | < 0.001 |
| Logistic coefficient for delay | -2.41 |
| Delay odds ratio | 0.089 |
| Approximate ROC-AUC | 0.660 |
| Suggested optimized threshold | ~0.37 |

---

## Business Interpretation

This module shows that delivery performance is not only a logistics issue, but also a customer-experience and retention issue.

Three business implications stand out:

### 1. Delivery timeliness is a major satisfaction lever
A large share of dissatisfaction can be linked to delayed delivery. This means logistics operations should be treated as a customer-satisfaction driver, not only a fulfillment KPI.

### 2. High-delay segments should be monitored proactively
Regions, order types, or product categories with higher delay risk should be flagged earlier for intervention.

### 3. Logistics data can support service-risk prediction
Even though the predictive power is only moderate, delivery-related features already provide useful signal for identifying orders or customers that may require proactive support.

---

## Business Recommendations

Based on the findings, the following actions are recommended:

1. **Prioritize delay reduction in high-risk operational segments**  
   Focus on regions, sellers, or product categories with systematically longer delivery times.

2. **Introduce proactive service recovery for delayed orders**  
   Customers with delayed deliveries should receive automated updates, compensation logic, or service outreach before dissatisfaction escalates.

3. **Use delay-related variables in retention and service-risk workflows**  
   Delivery duration and delay flags should be integrated into broader churn-risk or customer-experience monitoring systems.

4. **Expand future modeling with richer features**  
   Add product, service, and after-sales variables to improve dissatisfaction prediction accuracy.

---

## Technical Implementation

This module demonstrates the following technical capabilities:

- business-oriented exploratory data analysis
- statistical testing for categorical and continuous outcomes
- feature engineering for non-linear modeling
- regression and classification modeling
- threshold tuning for cost-sensitive decision-making
- interpretation of both inferential and predictive outputs

The module is implemented in Jupyter Notebook and fits into the wider project workflow of:

raw data → MySQL warehouse → joined analytical dataset → statistical analysis → predictive modeling → business recommendations

---

## Files and Deliverables

Primary notebook:
- `Statistical_analysis_report/01_Satisfaction_vs_Delivery.ipynb`

Related deliverables may include:
- plots of delivery distribution
- box plots for delay and order value
- correlation heatmaps
- contingency table outputs
- logistic regression and ROC analysis
- summary interpretations

---

## Module Position in the Full Project

This module is an early-stage operational analysis component in the overall e-commerce decision-intelligence project. It supports later business thinking around:

- retention strategy
- service quality improvement
- regional logistics analysis
- predictive customer-risk workflows

It is therefore not just a standalone statistical exercise, but a foundation for broader decision-support logic across the project.

---

## Next-Step Notes

Possible future enhancements for this module include:

- add regional and category-level delay segmentation
- incorporate seller-level logistics performance
- include return/refund behavior as additional outcome signals
- connect dissatisfaction prediction with churn-risk analysis
- turn the module into a dashboard page for operational monitoring