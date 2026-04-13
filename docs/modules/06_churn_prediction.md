# Module 06 — Customer Churn Prediction

## Overview

This module builds a customer churn prediction workflow for e-commerce retention decision-making. Its purpose is to identify which users are likely to become inactive, convert that prediction into user-level risk scores and business-readable risk tiers, and support prioritized retention intervention.

The module is not framed as a pure modeling exercise. Instead, it treats churn prediction as an operational decision layer that connects historical customer behavior, snapshot-based labeling, machine learning risk scoring, and downstream strategy outputs.

Within the broader project, this module forms the **retention-risk layer** of the decision-intelligence system.

---

## Business Question

This module is designed to answer the following core questions:

1. Which customers are most likely to churn?
2. How should retention strategy prioritize different risk groups?
3. Which users are both valuable and at risk, and therefore most urgent to save?
4. Can snapshot-based churn modeling produce reusable outputs for CRM, dashboarding, and downstream personalization?

From a business perspective, the goal is to move from descriptive user behavior analysis to a predictive retention framework.

---

## Data Source

This module uses customer-behavior data built from the project warehouse and churn-label views created from historical order activity.

The workflow is based on **user-level and snapshot-level behavioral data**, typically including:

- customer identity keys
- recency / activity timing
- order count and purchase frequency
- spending and value-related features
- product and category breadth
- historical engagement summaries
- churn labels generated from snapshot logic

The module is designed to work with rolling or repeated behavioral snapshots rather than relying on a single static cut.

Representative downstream outputs include:
- `user_churn_scores_latest_user_level.csv`
- `user_churn_scores_snapshot_level.csv`
- `modeling_data.csv`

These outputs support both model development and business-facing risk use.

---

## Methodology

### 1. Churn Problem Definition
The module defines churn as a future inactivity outcome derived from historical transaction windows. Instead of relying only on one final observation date, the notebook is structured around **snapshot-based churn labeling**, which makes the modeling setup closer to how churn scoring would operate in production.

This design improves:
- realism of the prediction task
- reusability for future scoring
- comparability across time windows

### 2. Feature Construction
The model uses customer-level behavioral features derived from past transactions, such as:

- recency-style activity features
- order frequency and count
- monetary features
- category exploration / product diversity
- customer behavioral intensity signals
- aggregated purchase-history indicators

The feature layer is designed to capture both:
- **how recently** a user interacted
- **how much** the user has purchased
- **how broadly** the user has explored the platform

### 3. Snapshot-Based Modeling Dataset
The notebook constructs a modeling table where each row represents a user or user-snapshot observation, with:
- historical features
- a future churn label
- a clear separation between feature window and label window

This is a stronger setup than a simple one-time retrospective label because it better matches real churn prediction use cases.

### 4. Exploratory Analysis
Before modeling, the module examines:
- label balance
- feature distribution
- class imbalance risk
- possible leakage issues
- behavior differences between churned and retained users

This ensures that the churn problem is framed as a valid prediction task rather than a post-hoc descriptive comparison.

### 5. Model Comparison
The notebook compares multiple classification models, including linear and tree-based approaches, to balance interpretability and predictive power.

Representative model families include:
- Logistic Regression
- Random Forest
- gradient-boosting / boosting-based models
- XGBoost / LightGBM-style ensemble models

This allows the project to compare:
- baseline linear performance
- nonlinear tree-based learning
- stronger boosted classifiers

### 6. Evaluation Design
The module evaluates model performance using standard binary-classification metrics such as:
- ROC-AUC
- precision
- recall
- F1-score
- confusion-matrix logic
- threshold-based business interpretation

Because churn prediction is a business-priority problem, threshold choice matters as much as model ranking.

### 7. Risk Scoring and Tiering
After model selection, predicted churn probabilities are converted into operational outputs such as:
- churn probability
- risk level
- latest user-level score
- snapshot-level score history

This makes the model usable outside the notebook.

Typical business-readable tiers include:
- Low Risk
- Medium Risk
- High Risk

### 8. Retention Prioritization
The notebook goes beyond prediction and converts model outputs into intervention logic. In particular, it supports identifying customers who are:
- high-risk
- high-value
- both high-risk and high-value

This is especially important because not all churn cases have equal business impact.

### 9. Output Export
The module exports structured files that can be reused by:
- CLV analysis
- recommendation routing
- future dashboard pages
- business reporting
- CRM targeting logic

---

## Key Findings

### 1. Churn prediction is framed as a practical retention problem, not just a classification task
The strongest design choice in this module is the use of snapshot-based churn labeling and risk scoring. This makes the workflow much closer to how a real retention-risk model would be used in practice.

### 2. Recent inactivity is one of the most important churn signals
As in many commerce-retention settings, recency-related behavior is central to churn prediction. Users with weaker recent activity are much more likely to fall into higher-risk groups.

This makes the model operationally useful, because recency is both interpretable and actionable.

### 3. Tree-based models are well suited to churn scoring
The module compares multiple classifiers rather than relying on a single method. In this kind of behavioral-risk problem, nonlinear tree-based models are especially useful because they can capture:
- threshold effects
- feature interaction
- nonlinear purchase-behavior patterns

This gives the module stronger predictive flexibility than a linear-only approach.

### 4. Probability outputs are more useful than hard labels alone
The notebook treats churn prediction as a risk-scoring problem, not only a yes/no classification problem. This allows the business to:
- prioritize intervention intensity
- separate medium-risk from truly urgent high-risk users
- combine churn risk with customer value in later decision layers

### 5. High-risk users are not all equally important
A core business insight is that churn scoring becomes much more useful when combined with value-based prioritization.

This leads naturally to groups such as:
- high-risk / high-value users
- high-risk / low-value users
- low-risk / high-value users

That distinction matters because retention resources are limited.

### 6. Snapshot-level outputs support future monitoring
Because the module exports both latest user-level scores and snapshot-level scoring history, it supports:
- current-state intervention targeting
- trend monitoring over time
- future dashboard integration
- comparison with CLV or recommendation outputs

### 7. The module creates a reusable retention decision layer
The most important contribution of this module is not just the trained classifier. It is the full pipeline from:
historical behavior → churn label → model probability → risk tier → retention priority output

That makes the module reusable inside a broader decision-support system.

---

## Key Outputs

Representative output files include:

- `output/06_churn_prediction/user_churn_scores_latest_user_level.csv`
- `output/06_churn_prediction/user_churn_scores_snapshot_level.csv`
- `output/06_churn_prediction/modeling_data.csv`

Depending on the notebook version, the output folder may also include:
- model comparison tables
- feature importance charts
- confusion matrices
- ROC plots
- intervention-priority lists
- high-value / high-risk customer files

These outputs make the module useful for both analysis and downstream operational use.

---

## Risk Interpretation Framework

### Low Risk
These users show relatively stable recent activity and weaker immediate signs of attrition.

**Business meaning**
- maintain regular engagement
- avoid over-investing retention budget

### Medium Risk
These users show some warning signals but are not yet urgent loss cases.

**Business meaning**
- monitor carefully
- use moderate-touch reminder or offer strategies

### High Risk
These users show strong signs of likely inactivity and should be prioritized for intervention.

**Business meaning**
- intervene earlier
- combine with customer value to decide intervention depth
- use this group as the core save-list candidate set

---

## Business Recommendations

Based on the module design and outputs, the following actions are recommended:

1. **Use churn probability as a ranking score, not just a binary flag**  
   Retention strategy should prioritize users continuously by risk rather than relying only on yes/no churn labels.

2. **Prioritize high-risk and high-value users first**  
   The most urgent save-list should come from the overlap between churn risk and customer value.

3. **Build differentiated intervention intensity by risk tier**  
   Low-risk, medium-risk, and high-risk users should not receive the same operational treatment.

4. **Refresh scores on a repeated snapshot basis**  
   Churn scoring is most useful when updated regularly rather than treated as a one-time model output.

5. **Connect churn outputs with downstream modules**  
   Churn scores should feed into:
   - CLV prioritization
   - recommendation strategy
   - dashboard alerts
   - CRM campaign targeting

---

## Technical Implementation

This module demonstrates the following technical capabilities:

- churn-label design based on behavioral snapshots
- supervised classification workflow
- feature engineering for customer-risk prediction
- comparison of multiple classification models
- probability-based scoring rather than label-only prediction
- export of user-level and snapshot-level outputs
- translation from model output to retention strategy

The module is implemented in a notebook-based workflow but already produces structured files suitable for later dashboarding and service integration.

---

## Files and Deliverables

Primary notebook:
- `Statistical_analysis_report/06_Customer_Churn_Prediction.ipynb`

Representative outputs:
- `output/06_churn_prediction/user_churn_scores_latest_user_level.csv`
- `output/06_churn_prediction/user_churn_scores_snapshot_level.csv`
- `output/06_churn_prediction/modeling_data.csv`

Possible additional deliverables:
- model comparison summary
- feature importance visualization
- ROC / PR evaluation plots
- retention-priority lists
- high-value high-risk user slices

---

## Module Position in the Full Project

This module forms the **predictive retention layer** of the broader e-commerce decision-intelligence system.

It connects naturally with:
- RFM segmentation
- CLV prediction
- recommendation strategy
- future dashboard monitoring
- customer-priority decision logic

It helps move the project from descriptive customer understanding into predictive customer-risk management.

---

## Next-Step Notes

Future improvements for this module may include:

- stronger threshold calibration based on business cost
- more explicit treatment of class imbalance
- repeated backtesting across multiple snapshot periods
- tighter integration with CLV-based prioritization
- deployment into dashboard-based retention monitoring
- modularization into reusable `src/models/churn.py` logic