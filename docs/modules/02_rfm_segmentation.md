# Module 02 — User Segmentation & Value Analysis (RFM Model)

## Overview

This module builds a business-oriented customer segmentation framework using the RFM methodology: **Recency**, **Frequency**, and **Monetary** value. The goal is to move from raw behavioral aggregation to actionable customer groups that support retention strategy, activation design, value prioritization, and downstream personalization.

Rather than using a purely textbook RFM approach, this module adapts the scoring logic to the actual behavior distribution in the dataset, where purchase frequency is extremely skewed and most users are one-time buyers.

---

## Business Question

This module is designed to answer the following core questions:

1. Which customer groups deserve differentiated retention or activation campaigns?
2. How concentrated is customer value across the user base?
3. Can RFM-based behavioral segmentation provide a reliable and statistically valid foundation for business strategy?

From a business perspective, this module translates user purchase behavior into operational segments that can support CRM planning, retention prioritization, and future personalization workflows.

---

## Data Source

The module is based on the aggregated customer behavior view used in the project warehouse, centered on user-level purchase history.

Core variables include:

- `unique_user_id`
- `recency`
- `frequency`
- `monetary`
- `state`
- customer activity and spending summaries

The analysis keeps only users with at least one completed purchase.

---

## Methodology

### 1. Data Preparation
The module starts from user-level behavioral aggregates and filters to valid purchasing users only.

Initial data profile after filtering:
- total users with `order_count > 0`: **96,219**
- missing monetary values: **680**
- final users after dropping missing RFM records: **95,539**

The module standardizes variable names into:
- `recency`
- `frequency`
- `monetary`

### 2. EDA and Data Diagnostics
Before segmentation, the notebook examines:
- missing values
- outliers
- skewness
- non-normality
- cumulative inequality patterns

Key diagnostics show:
- Frequency is highly concentrated at 1 purchase
- Monetary is right-skewed
- Recency has a broader business-relevant spread
- Outliers are retained because they may represent important customer types

IQR-based outlier checks show:
- recency outliers: **3**
- frequency outliers: **2,878** (**3.01%**)
- monetary outliers: **7,612** (**7.97%**)

### 3. Refined RFM Scoring Logic
A standard quantile-based frequency score would not work well in this dataset because the majority of users have `frequency = 1`.

Therefore, the module uses a refined scoring approach:

- **Recency**: quantile-based scoring from 5 to 1, where more recent users receive higher scores
- **Frequency**:
  - all users with `frequency = 1` receive **F_score = 1**
  - only repeat buyers (`frequency >= 2`) are split into scores **2–5**
- **Monetary**: ranked quantile-based scoring from 1 to 5

Two total scores are then created:
- `RFM_score_simple`
- `RFM_score_weighted`

The weighted score is defined as:

- **0.4 × R + 0.1 × F + 0.5 × M**

This design intentionally downweights frequency and emphasizes monetary value, given the extreme sparsity in repeat purchases.

### 4. Clustering
After RFM feature construction, the module standardizes RFM variables and performs K-Means clustering.

Cluster quality is evaluated using:
- Elbow method
- Silhouette score
- Davies–Bouldin index
- Calinski–Harabasz score

The final selected solution is **K = 3**.

Clustering quality:
- **Silhouette score = 0.4557**
- **Davies–Bouldin = 0.7619**
- **Calinski–Harabasz = 48636.7004**

### 5. Statistical Validation
The module validates whether clusters differ significantly using:
- Kruskal–Wallis tests
- pairwise Mann–Whitney U tests with Bonferroni correction
- Spearman correlation between RFM scores and monetary value
- chi-square test for geography vs. cluster

This makes the segmentation statistically grounded rather than purely visual.

### 6. Business Translation
After clustering, each cluster is mapped into a business-readable segment name:

- **Cluster 0** → Lapsed Single-Purchase Users
- **Cluster 1** → Recent Single-Purchase Users
- **Cluster 2** → High-Value Repeat Customers

The module then extends the analysis into:
- value concentration
- churn-risk heuristics
- strategy matrix
- experiment design
- simplified LTV estimation for top-value users

---

## Key Findings

### 1. The customer base is dominated by single-purchase users
The data shows an extremely concentrated purchase-frequency distribution. Most users purchased only once, which is why a refined frequency-scoring method was necessary.

This is a meaningful business finding by itself: customer repetition is weak, so activation and second-purchase conversion are strategically important.

### 2. A 3-cluster solution produces clear and interpretable behavioral groups
The final segmentation results are:

- **Cluster 0**: 39,363 users (**41.20%**)
- **Cluster 1**: 53,291 users (**55.78%**)
- **Cluster 2**: 2,885 users (**3.02%**)

Average RFM profiles:

| Cluster | Recency | Frequency | Monetary |
|---|---:|---:|---:|
| 0 | 391.80 | 1.00 | 162.27 |
| 1 | 131.59 | 1.00 | 159.81 |
| 2 | 224.04 | 2.11 | 325.69 |

This shows three distinct business personas:
- older one-time buyers
- recent one-time buyers
- a small but clearly more valuable repeat-buyer group

### 3. Cluster differences are statistically significant
Kruskal–Wallis tests show strong differences across clusters:

- recency: **H = 67989.9210**, **p ≈ 0**
- frequency: **H = 95292.1431**, **p ≈ 0**
- monetary: **H = 2366.6007**, **p ≈ 0**

This confirms that the clusters are not arbitrary grouping artifacts.

Pairwise Mann–Whitney tests further show:
- recency differs significantly across all cluster pairs
- frequency differs significantly when Cluster 2 is involved
- monetary differs significantly across cluster comparisons

### 4. Weighted RFM scoring aligns strongly with customer value
Spearman correlations between RFM score and monetary value show:

- simple RFM vs monetary: **rho = 0.6978**
- weighted RFM vs monetary: **rho = 0.7826**

This indicates that the weighted scoring logic is more aligned with actual user value than the simple unweighted version.

### 5. The segmentation has weak but statistically significant geographic structure
The chi-square test for `state × cluster` gives:

- **chi2 = 364.8234**
- **dof = 52**
- **p = 1.5096e-48**

This suggests that geography is not the dominant driver of segmentation, but it is still related to customer composition across regions.

### 6. Value is unevenly distributed, but not concentrated only in the smallest cluster
Value contribution by cluster shows:

| Cluster | User Ratio | GMV Ratio |
|---|---:|---:|
| 0 | 41.20% | 40.32% |
| 1 | 55.78% | 53.75% |
| 2 | 3.02% | 5.93% |

Cluster 2 is clearly the highest-value segment on a per-user basis, but Cluster 1 still contributes the largest total GMV because it contains most of the user base.

This means the business should not focus only on VIP retention; it also needs large-scale activation among recent one-time buyers.

### 7. Cluster 0 carries the highest churn-like inactivity risk
Using the 75th percentile of recency as a churn proxy threshold:

- churn threshold: **351 days**
- churn rate in Cluster 0: **59.24%**
- churn rate in Cluster 1: **0.00%**
- churn rate in Cluster 2: **21.21%**

The notebook also estimates that recovering 10% of churned users in Cluster 0 could generate about:

- **376,440.11** in GMV uplift

This makes Cluster 0 a strong reactivation target.

### 8. Cluster 1 is the best experimental segment for second-purchase activation
Cluster 1 represents recent single-purchase users and is therefore the most promising activation segment.

The notebook’s A/B-test design assumes:
- baseline conversion: **5%**
- target conversion: **7%**
- minimum detectable effect: **2 percentage points**
- required sample size per group: **30,913**
- required total sample size for 4 groups: **123,652**

Available users in Cluster 1:
- **53,291**

This means the exact 4-group test design is underpowered with current data, but the framework is useful for future CRM experimentation.

### 9. Cluster 2 supports a strong VIP retention case
For Cluster 2 (High-Value Repeat Customers), the notebook estimates:

- average order value: **163.49**
- average purchase frequency: **2.11**
- average customer lifetime: **85 days**
- estimated annual frequency: **9.10**
- adjusted LTV: **2902.18**
- average LTV across all customers: **165.83**
- Cluster 2 premium: **17.5×**

This provides a strong justification for higher-touch retention and VIP-style service.

---

## Key Metrics

| Metric | Result |
|---|---:|
| Users after `order_count > 0` filter | 96,219 |
| Final users after dropping missing RFM values | 95,539 |
| Missing monetary values | 680 (0.71%) |
| Final number of clusters | 3 |
| Silhouette score | 0.4557 |
| Davies–Bouldin index | 0.7619 |
| Calinski–Harabasz score | 48636.7004 |
| Cluster 0 size | 39,363 (41.20%) |
| Cluster 1 size | 53,291 (55.78%) |
| Cluster 2 size | 2,885 (3.02%) |
| Weighted RFM vs monetary Spearman rho | 0.7826 |
| Churn threshold (recency proxy) | 351 days |
| Cluster 0 churn rate | 59.24% |
| Cluster 2 adjusted LTV | 2902.18 |
| Cluster 2 LTV premium vs overall average | 17.5× |

---

## Segment Interpretation

### Cluster 0 — Lapsed Single-Purchase Users
**Profile**
- older recency
- one-time purchasers
- moderate spending
- highest inactivity risk

**Business meaning**
These users bought before but have now become inactive. They are the primary reactivation pool.

**Suggested action**
- win-back campaigns
- reminders and reactivation offers
- selective incentive design
- lower-cost automated retention tactics

---

### Cluster 1 — Recent Single-Purchase Users
**Profile**
- lowest recency
- one-time purchasers
- similar spend level to Cluster 0
- large user base

**Business meaning**
This is the most important growth segment for converting first-time customers into repeat buyers.

**Suggested action**
- second-purchase activation campaigns
- onboarding journeys
- post-purchase email / coupon flows
- controlled CRM experiments

---

### Cluster 2 — High-Value Repeat Customers
**Profile**
- highest frequency
- highest monetary value
- small population
- strongest per-user economic value

**Business meaning**
This is the premium customer segment and should receive protection and upsell attention.

**Suggested action**
- VIP retention
- premium service
- priority support
- loyalty perks
- high-value personalized recommendations

---

## Business Recommendations

Based on the segmentation results, the module suggests the following actions:

1. **Reactivate Cluster 0 efficiently**  
   Focus on low-cost win-back strategies and identify the most recoverable inactive users.

2. **Convert Cluster 1 into repeat buyers**  
   This is the best segment for experimentation and repeat-purchase growth.

3. **Protect and expand Cluster 2**  
   Use premium service and loyalty mechanics to preserve and deepen high-value relationships.

4. **Use weighted RFM as an operational scoring layer**  
   The weighted score is better aligned with value and can be reused in recommendation, churn, or CRM prioritization workflows.

5. **Link segmentation to downstream decision systems**  
   This module should feed later layers such as churn modeling, CLV modeling, dashboard reporting, and recommendation routing.

---

## Technical Implementation

This module demonstrates the following technical capabilities:

- SQL-to-notebook analytical workflow
- missing-value diagnostics
- outlier analysis and retention decisions
- custom RFM scoring design for skewed behavioral data
- clustering model selection and validation
- non-parametric statistical testing
- value concentration analysis
- business translation from clusters to actions
- export of structured segmentation results for downstream modules

---

## Files and Deliverables

Primary notebook:
- `Statistical_analysis_report/02.User_Segmentation_vs_Value_Analysis_(RFM Model).ipynb`

Main exported files:
- `output/user_segments_rfm.csv`
- `output/cluster_centers.csv`

Exported segmentation fields include:
- `unique_user_id`
- `cluster`
- `segment`
- `recency`
- `frequency`
- `monetary`
- `R_score`
- `F_score`
- `M_score`
- `RFM_score_simple`
- `RFM_score_weighted`
- `is_repeat_customer`
- `is_churned`
- `strategy`

These outputs are designed for downstream use in:
- churn modeling
- recommendation logic
- dashboards and reporting
- marketing automation

---

## Module Position in the Full Project

This module is one of the central business-analysis layers in the broader e-commerce decision-intelligence system. It transforms raw transactional behavior into a reusable segmentation layer that supports:

- retention strategy
- CRM prioritization
- user-value interpretation
- activation campaign design
- later personalization and recommendation workflows

It is therefore both a business-analysis module and a bridge into later machine learning and decision-support layers.

---

## Next-Step Notes

Future improvements for this module may include:

- add more longitudinal behavioral features
- combine RFM segmentation with churn and CLV scores
- extend segmentation into dashboard monitoring
- validate segment actions through live A/B testing
- connect segment profiles with recommendation routing logic