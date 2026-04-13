# Module 07 — Customer Lifetime Value (CLV) Prediction

## Overview

This module builds a Customer Lifetime Value (CLV) prediction workflow to estimate future customer value and convert those predictions into business-facing decision tools.

The purpose of the module is not limited to regression accuracy. It is designed to support:
- future customer-value estimation
- high-value customer identification
- retention and budget prioritization
- value–risk decision mapping
- interpretable discussion with business stakeholders

Within the broader e-commerce decision-intelligence system, this module forms the **customer-value prioritization layer**.

---

## Business Question

This module is designed to answer the following core questions:

1. Which customers are likely to generate the highest future value?
2. How should predicted future value guide retention and budget allocation?
3. Which customers deserve premium protection because they are both valuable and at risk?
4. Can CLV prediction be made interpretable enough to support stakeholder discussion and operational prioritization?

From a business perspective, this module turns customer-value modeling into a practical resource-allocation framework rather than a standalone regression exercise. :contentReference[oaicite:2]{index=2}

---

## Data Source

This module uses customer-level behavioral and value-related features built from the project’s MySQL warehouse and earlier analytical layers.

The feature space is designed to summarize:
- recency-style activity behavior
- purchase count and frequency
- spending intensity
- exploration breadth
- purchased-product variety
- other customer-level historical behavior summaries

The module produces downstream artifacts such as:
- customer value tiers
- value–risk matrix outputs
- budget-allocation views
- high-value customer profiles
- model interpretability plots. 

Representative portfolio artifacts mentioned in the deck include:
- `budget_allocation_overview`
- `customer_tier_statistics`
- `high_value_customer_profile`. :contentReference[oaicite:4]{index=4}

---

## Methodology

### 1. CLV Target Framing
The module treats CLV as a forward-looking customer-value prediction task. Instead of focusing only on historical spend, it aims to estimate **future customer value** and make that usable for prioritization.

This framing makes the module relevant for:
- CRM planning
- budget allocation
- retention prioritization
- high-value customer protection

### 2. Feature Construction
The model uses customer-level historical behavior features that reflect both activity and value structure.

Representative feature groups include:
- recency-related scores
- frequency and order-count indicators
- spending-based variables
- exploration breadth
- purchased-variety indicators

The deck explicitly shows that the final model interpretation is behavior-driven rather than opaque: **R_score** is the dominant feature in the displayed feature-importance ranking, while order count, frequency, exploration, and purchased variety appear as the second tier of signals. :contentReference[oaicite:5]{index=5}

### 3. Regression Modeling
This module compares regression-style models to estimate future customer value. The goal is to identify a model that is not only accurate enough for prediction but also useful enough for business translation.

The modeling workflow is designed to include:
- feature engineering
- train/test evaluation
- model comparison
- output export for downstream business use

### 4. Value Tier Construction
Predicted CLV is converted into business-readable customer-value tiers so that the result can be used operationally rather than remaining as a raw regression score.

The deck explicitly identifies **value tiers** as one of the core outputs of the module. :contentReference[oaicite:6]{index=6}

### 5. Value–Risk Integration
The module is linked with the churn/risk layer to build a **value–risk matrix**.

This is one of the most important design features of the module because it distinguishes:
- high CLV + high risk
- high CLV + lower risk
- lower CLV groups

The deck states the business logic directly:
- **High CLV + high risk → most urgent save list**
- **High CLV + lower risk → protect experience and expand share of wallet**
- **Lower CLV groups → use selective or automated interventions**. :contentReference[oaicite:7]{index=7}

### 6. Budget Allocation Translation
The CLV pipeline is also used for budget and resource allocation. Instead of treating CLV as a technical score, the module translates future value into action logic.

The deck explicitly notes that the same CLV pipeline supports both **customer prioritization** and **budget allocation outputs**, which makes CLV useful as a decision layer rather than just a regression score. :contentReference[oaicite:8]{index=8}

### 7. Explainability Layer
To make the module business-friendly, the project includes interpretability outputs.

According to the portfolio deck, the model is “interpretable enough to drive discussion with business stakeholders,” and the feature-importance view provides a concrete bridge from model output to customer-behavior explanation. :contentReference[oaicite:9]{index=9}

---

## Key Findings

### 1. Customer value is concentrated rather than evenly distributed
A central insight of the module is that customer value is not spread evenly across the user base. Instead, it is concentrated in a relatively small upper segment of customers.

The portfolio deck summarizes this directly: customer value is concentrated in a small set of upper tiers rather than evenly distributed. :contentReference[oaicite:10]{index=10}

### 2. CLV prediction is useful beyond regression
The module’s strongest business contribution is that it treats CLV as a decision-support signal, not merely as a model output.

The same pipeline supports:
- customer prioritization
- high-value customer identification
- budget-allocation outputs
- retention decision logic. :contentReference[oaicite:11]{index=11}

### 3. Value–risk combination creates a stronger action framework
A predicted value score alone is not enough. The module becomes much more useful when future value is combined with churn or risk signals.

This creates an operating framework where:
- high-value high-risk customers become the most urgent save list
- high-value lower-risk customers become protection and expansion targets
- lower-value customers can be handled with lower-touch strategies. :contentReference[oaicite:12]{index=12}

### 4. The model is interpretable in behavior terms
The module does not stop at predictive output. It also explains **why** some customers are likely to be valuable.

The deck’s interpretability page highlights:
- **R_score** as the dominant feature
- order count, frequency, exploration, and purchased variety as the second tier of signals

This is especially useful for stakeholder communication, CRM planning, and interview discussion. :contentReference[oaicite:13]{index=13}

### 5. The module produces reusable business artifacts
The project does not keep CLV results inside the notebook only. It exports and visualizes outputs such as:
- value tiers
- value–risk matrix
- budget-allocation outputs
- high-value customer profile views
- interpretability plots. 

---

## Core Business Outputs

Representative outputs of the module include:

- customer value tiers
- value–risk matrix
- budget-allocation overview
- customer-tier statistics
- high-value customer profile
- model interpretability plots. 

These outputs make the CLV module useful for:
- retention prioritization
- CRM targeting
- budget planning
- dashboard reporting
- executive storytelling

---

## Value Tier Interpretation

### Lower Value Groups
These customers are expected to generate relatively lower future value.

**Business meaning**
- use selective intervention
- emphasize scalable and lower-cost CRM actions
- avoid over-allocating premium resources

### Mid Value Groups
These customers are meaningful but not yet premium.

**Business meaning**
- monitor for growth potential
- target with structured activation and loyalty-building actions
- combine with churn risk to identify upgrade opportunities

### High Value Groups
These customers are expected to contribute disproportionately high future value.

**Business meaning**
- protect proactively
- allocate more retention budget
- use higher-touch service or premium targeting
- prioritize when risk signals also become elevated

---

## Business Recommendations

Based on the module design and observed outputs, the following actions are recommended:

1. **Use CLV as a prioritization layer, not only a prediction score**  
   The main value of CLV comes from deciding where retention, service, and budget should go first. :contentReference[oaicite:16]{index=16}

2. **Combine CLV with churn risk before deciding intervention intensity**  
   The value–risk matrix is more actionable than value scores alone. High CLV + high risk should become the primary save list. :contentReference[oaicite:17]{index=17}

3. **Allocate premium treatment to top-value customers selectively**  
   High-value customers should receive differentiated service, but the strongest priority should go to those who are also at risk.

4. **Use explainability outputs in stakeholder communication**  
   Feature-importance views make it easier to justify why certain customer groups deserve more budget or attention. :contentReference[oaicite:18]{index=18}

5. **Feed CLV outputs into downstream decision systems**  
   CLV results should connect with:
   - churn monitoring
   - recommendation strategy
   - CRM prioritization
   - dashboard reporting
   - budget planning

---

## Technical Implementation

This module demonstrates the following technical capabilities:

- customer-level value prediction
- regression-oriented machine learning workflow
- feature engineering for future-value estimation
- model comparison and output export
- value-tier translation for business use
- integration of predicted value with risk scoring
- model interpretability for stakeholder discussion

The module fits into a broader pipeline of:
historical behavior → feature engineering → CLV prediction → value tiering → value–risk strategy → budget allocation output

---

## Files and Deliverables

Primary notebook:
- `Statistical_analysis_report/07_Customer_Lifetime_Value_Prediction.ipynb`

Representative business-facing deliverables include:
- budget allocation overview
- customer tier statistics
- high-value customer profile
- value–risk matrix visual
- feature-importance / interpretability plots. 

Depending on the notebook version, the output folder may also include:
- CLV prediction tables
- tier-level summaries
- customer-level scoring files
- feature-importance figures
- customer-strategy slices

---

## Module Position in the Full Project

This module forms the **customer-value prioritization layer** of the broader e-commerce decision-intelligence system.

It connects naturally with:
- RFM segmentation
- churn prediction
- recommendation strategy
- dashboard reporting
- retention and budget allocation decisions

It helps move the project from customer analysis and risk prediction toward value-based business prioritization. 

---

## Next-Step Notes

Future improvements for this module may include:

- tighter calibration between churn and CLV priority rules
- more explicit budget-allocation simulation
- deeper comparison of regression models
- stronger customer-level strategy export
- integration into the future Streamlit dashboard
- modularization into reusable `src/models/clv.py` logic