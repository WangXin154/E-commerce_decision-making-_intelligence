# Module 05 — Time Series Analysis

## Overview

This module analyzes the e-commerce business from a time-series perspective, focusing on how order demand evolves over time and how short-term forecasts can support operational decision-making.

The analysis goes beyond simple forecasting. It first studies the business at multiple temporal granularities — daily, monthly, weekly, and hourly — then decomposes the series into structural components, identifies anomalies, compares category-level temporal behavior, and finally evaluates several forecasting models for short-horizon prediction.

This module forms the forecasting layer of the broader e-commerce decision-intelligence system.

---

## Business Question

This module is designed to answer the following core questions:

1. What are the major trend and seasonality patterns in platform order demand?
2. Are there clear weekly and intraday demand rhythms that matter operationally?
3. Which unusual periods deviate from the normal trend–seasonal structure?
4. Do major product categories follow similar temporal dynamics?
5. Which forecasting model is most reliable for short-term order prediction?
6. What does the next 30-day demand outlook imply for planning and monitoring?

From a business perspective, this module supports short-term planning, promotional timing, workload management, anomaly awareness, and future dashboard forecasting features.

---

## Data Source

This module uses the order-level e-commerce dataset after preprocessing and timestamp standardization.

The working dataset includes fields such as:
- `order_id`
- `order_purchase_timestamp`
- `price`
- `freight_value`
- `gmv`
- `product_id`
- `category_name_english`

The analysis aggregates transaction data into multiple temporal views:

- **daily series** for forecasting and decomposition
- **monthly series** for medium-term trend analysis
- **weekday-level aggregation** for weekly demand rhythm
- **hourly aggregation** for intraday demand behavior
- **category-level temporal subsets** for category comparison

Key dataset sizes include:
- daily aggregation: **612 observed days**
- completed daily regularized series: **714 days**
- monthly aggregation: **23 months**

---

## Methodology

### 1. Multi-Granularity Descriptive Time-Series Analysis
The module first explores time from several business-relevant levels:

- **Daily**: base signal for trend and volatility
- **Monthly**: medium-term business growth pattern
- **Weekly**: demand concentration by weekday
- **Hourly**: intraday customer activity rhythm

This step establishes operational intuition before model building.

### 2. Daily Series Regularization
Because some calendar dates are missing in the raw daily series, the time series is converted into a regular daily-frequency series before decomposition and forecasting.

Key preparation result:
- original daily length: **612**
- regularized daily length: **714**

This indicates that some dates had no observed orders and were filled as part of time-series preparation.

### 3. Seasonal Decomposition
The module applies **additive seasonal decomposition** to the daily order series:

`Y(t) = Trend(t) + Seasonal(t) + Residual(t)`

This separates business movement into:
- long-term trend
- repeating seasonal pattern
- irregular residual movement

### 4. Stationarity Testing
Before ARIMA-family modeling, the module applies the **ADF test** to both:
- the original daily series
- the first-differenced series

This checks whether the raw series is stationary or whether differencing is required.

### 5. Anomaly Detection
The residual component from seasonal decomposition is used for anomaly detection.

The module uses the **IQR rule** on residuals:
- Q1 = **-18.78**
- Q3 = **19.10**
- IQR = **37.87**
- lower bound = **-75.59**
- upper bound = **75.91**

Residuals beyond these thresholds are marked as anomalies.

### 6. Category-Based Temporal Comparison
To compare temporal dynamics across products, the module selects the **top 5 categories by order volume** and analyzes:
- monthly trend by category
- weekday demand pattern by category

Top 5 categories:
1. `cama_mesa_banho` — **9,272** orders
2. `beleza_saude` — **8,647** orders
3. `esporte_lazer` — **7,530** orders
4. `informatica_acessorios` — **6,530** orders
5. `moveis_decoracao` — **6,307** orders

### 7. Forecasting Model Comparison
The module evaluates multiple forecasting approaches on the daily order series using a **holdout test set of the last 30 days**.

Train-test split:
- training set: **684 days**
- test set: **30 days**
- test period: **2018-07-31 to 2018-08-29**

Tested models:
- Naive Forecast
- Moving Average
- Auto-ARIMA
- SARIMA
- Exponential Smoothing
- Tuned Prophet

### 8. Residual Diagnostics and Stability Validation
After holdout evaluation, the module further checks model adequacy using:
- residual mean / variance review
- Ljung–Box test
- Shapiro–Wilk test
- residual distribution and Q-Q plot
- residuals vs fitted plot
- walk-forward validation

This makes the forecasting evaluation more robust than a single split.

### 9. Future Forecast Generation
The final selected forecasting logic is re-fitted on the full daily series to generate a **30-day future forecast** with confidence intervals.

---

## Key Findings

### 1. The business shows a strong upward trend over time
The daily and monthly series both show a clear growth path from late 2016 into 2018, indicating strong business expansion rather than a flat demand structure.

Monthly summary statistics show:
- total observed months: **23**
- average monthly order count: **4,194.70**
- average monthly GMV: **670,424.90**
- average monthly order value: **154.39**

The monthly series suggests rapid platform growth through 2017, followed by a relatively higher operating level in 2018.

### 2. Demand is strongly concentrated on weekdays
The weekday pattern is clearly business-day oriented.

Order counts by weekday:
- Monday: **15,701**
- Tuesday: **15,503**
- Wednesday: **15,076**
- Thursday: **14,323**
- Friday: **13,685**
- Saturday: **10,555**
- Sunday: **11,635**

This indicates that order activity is highest on weekdays and weaker on weekends, which is important for staffing, campaign timing, and operational planning.

### 3. Intraday demand follows a stable business-hour rhythm
The hourly pattern shows:
- very low demand in the early morning
- rapid ramp-up after **08:00**
- highest activity from late morning to evening
- strongest hour at **16:00** with **6,476** orders

This suggests that user purchasing behavior follows a relatively stable intraday cycle rather than being evenly distributed across 24 hours.

### 4. The daily series is trend-driven and non-stationary in raw form
The ADF test confirms that the original daily order series is non-stationary:

- ADF statistic: **-2.4588**
- p-value: **0.1258**

After first-order differencing, the series becomes stationary:

- ADF statistic: **-6.5542**
- p-value: **0.0000**

This supports the use of differencing in ARIMA-family forecasting.

### 5. The decomposition shows both rising trend and meaningful seasonal structure
The decomposition result indicates that the series is shaped mainly by:
- a rising long-term trend
- a repeating seasonal pattern
- residual noise with some extreme points

This means the business is not purely random or purely seasonal; it is a growing platform with recurring weekly rhythm plus temporary shocks.

### 6. The series contains clear anomaly clusters rather than random isolated noise
Using the IQR rule on decomposition residuals, the module identifies:

- **33 anomaly points**
- anomaly rate: **4.82%**

These anomalies are not evenly spread across the full period. Instead, they cluster around specific dates, which suggests real business events or structural disruptions rather than normal background variation.

### 7. Major categories follow the same broad growth direction, but not identical intensity
The top 5 categories all broadly follow the platform’s overall growth trend, especially from 2017 into 2018, but their demand levels and fluctuation intensity differ.

This means platform growth is shared across multiple major categories, but category-specific planning still matters.

### 8. Forecast accuracy differs depending on the evaluation metric
The holdout comparison table shows:

| Model | MAE | RMSE | MAPE (%) |
|---|---:|---:|---:|
| Naive | 81.33 | 111.61 | 154.85 |
| Moving Average | 79.77 | 96.75 | 126.26 |
| Auto-ARIMA (1,1,1) | 79.44 | 95.38 | 122.88 |
| SARIMA(1,1,1)(1,1,1,7) | **72.16** | 95.98 | 136.15 |
| Exponential Smoothing | 79.02 | 98.85 | 132.94 |
| Prophet | 82.86 | **92.14** | **107.09** |

This means:
- **SARIMA** performs best on **MAE**
- **Prophet** performs best on **RMSE** and **MAPE**

No single model dominates every metric.

### 9. Prophet tuning materially improves business-facing forecasting quality
The tuned Prophet model is selected using lightweight hyperparameter search.

Best parameters:
- `changepoint_prior_scale = 0.1`
- `seasonality_prior_scale = 0.1`
- `seasonality_mode = additive`

Cross-validation results for the best Prophet setting:
- CV MAE: **42.64**
- CV RMSE: **51.81**
- CV MAPE: **0.2265**

Although Prophet is not the best holdout model on MAE, it performs strongly on RMSE, MAPE, and future forecast smoothness, making it a strong business-facing forecasting choice.

### 10. SARIMA residuals show useful but mixed diagnostic evidence
For `SARIMA(1,1,1)(1,1,1,7)`:
- residual length: **684**
- residual mean: **0.0026**
- residual std: **44.1853**

Ljung–Box test results at lags 7, 14, and 21 all show very high p-values, suggesting no strong remaining autocorrelation.

However, the Shapiro–Wilk test gives:
- statistic: **0.4560**
- p-value: **0.0000**

This means residuals are not normally distributed even though the mean is near zero and autocorrelation appears controlled. In practice, the model captures a large part of the structure, but not all distributional irregularity.

### 11. Walk-forward validation changes the interpretation of “best model”
A single 30-day holdout split is not enough to judge forecast stability.

Walk-forward validation results show:
- **SARIMA**
  - validation windows: **320**
  - average MAE: **65.63**
  - MAE std: **95.26**
- **Prophet**
  - validation windows: **23**
  - average MAE: **55.91**
  - MAE std: **27.11**

This suggests Prophet is more stable across repeated forecast windows in the reduced-frequency validation setup, even though SARIMA wins the original holdout comparison on MAE.

### 12. The 30-day forecast suggests a stable near-term demand level rather than explosive further growth
The final 30-day Prophet forecast starts around:
- **2018-08-30 forecast = 166.79**
- then fluctuates in a moderate range with confidence intervals

The near-term projection remains broadly aligned with the recent historical level rather than suggesting another major upward surge. This indicates:
- short-term demand is likely to remain active
- volatility remains possible
- planning should assume moderate stability, not hypergrowth

---

## Key Metrics

| Metric | Result |
|---|---:|
| Observed daily points | 612 |
| Regularized daily series length | 714 |
| Monthly observations | 23 |
| Average monthly order count | 4,194.70 |
| Average monthly GMV | 670,424.90 |
| Average monthly order value | 154.39 |
| Monday order count | 15,701 |
| Peak hourly order count | 6,476 at 16:00 |
| Original-series ADF p-value | 0.1258 |
| Differenced-series ADF p-value | 0.0000 |
| Number of anomalies | 33 |
| Anomaly rate | 4.82% |
| Train length | 684 days |
| Test length | 30 days |
| Best MAE model | SARIMA(1,1,1)(1,1,1,7) |
| Best RMSE / MAPE model | Prophet |
| SARIMA holdout MAE | 72.16 |
| Prophet holdout RMSE | 92.14 |
| Prophet holdout MAPE | 107.09% |
| SARIMA walk-forward average MAE | 65.63 |
| Prophet walk-forward average MAE | 55.91 |

---

## Business Interpretation

### Trend
The business is clearly growing over time, which implies that operational planning cannot rely on static averages.

### Seasonality
Demand has a meaningful weekly rhythm:
- stronger weekday activity
- weaker weekend demand
- predictable intraday usage pattern

This is useful for staffing, promotions, customer service timing, and fulfillment capacity planning.

### Anomalies
Anomalies are clustered, which suggests they may correspond to holidays, campaigns, disruptions, or event-driven demand spikes rather than ordinary noise.

### Forecasting
Forecasting is useful here not because the series is perfectly stable, but because the business shows:
- structural trend
- recurring seasonality
- manageable short-horizon predictability

The module therefore supports both descriptive monitoring and short-term forecast planning.

---

## Business Recommendations

Based on the findings, the module recommends the following actions:

1. **Use weekday and hourly patterns for operational scheduling**  
   Staffing, promotion timing, and service readiness should reflect the strong weekday and daytime concentration.

2. **Monitor anomaly periods explicitly**  
   Dates with extreme deviations should be investigated and linked to campaigns, holidays, or logistics disruptions.

3. **Use short-term forecasting for tactical planning**  
   A 30-day forecast is useful for short-term order-volume planning, especially for inventory, support, and fulfillment preparation.

4. **Do not rely on a single evaluation metric**  
   Model choice should depend on business objective:
   - use **SARIMA** when minimizing average absolute error is the priority
   - use **Prophet** when smoother business-facing forecasts and stronger RMSE / MAPE performance matter more

5. **Connect time-series outputs with category and regional modules**  
   Forecasting becomes more useful when integrated with category demand monitoring and region-level operations.

---

## Technical Implementation

This module demonstrates the following technical capabilities:

- time-based aggregation from transactional data
- multi-granularity descriptive time-series analysis
- additive seasonal decomposition
- ADF stationarity testing
- anomaly detection using residual IQR logic
- category-level temporal comparison
- forecasting model benchmarking
- hyperparameter tuning for Prophet
- residual diagnostics for SARIMA
- walk-forward validation for forecast stability
- export of reusable outputs for dashboards and reporting

---

## Files and Deliverables

Primary notebook:
- `Statistical_analysis_report/05_Time_Series_Analysis.ipynb`

Main saved outputs:
- `output/05_time_series_analysis/anomalies.csv`
- `output/05_time_series_analysis/future_30day_forecast.csv`
- `output/05_time_series_analysis/model_comparison.csv`
- `output/05_time_series_analysis/monthly_statistics.csv`

Typical visual outputs include:
- daily trend plots
- monthly trend plots
- weekday and hourly pattern charts
- decomposition figures
- anomaly plots
- category monthly comparison charts
- forecast comparison plots
- Prophet confidence-interval forecast
- SARIMA residual diagnostics
- walk-forward validation error plots

---

## Module Position in the Full Project

This module forms the **forecasting and temporal-monitoring layer** of the broader e-commerce decision-intelligence system.

It connects naturally with:
- product category analysis
- geographic demand monitoring
- churn and CLV planning
- dashboard development
- future inventory and campaign planning extensions

It adds the “time” dimension to the project, which is essential for turning static business analysis into forward-looking decision support.

---

## Next-Step Notes

Future improvements for this module may include:

- adding category-level forecasting for top product groups
- linking forecasts with regional sales monitoring
- testing seasonal ARIMA variants more systematically
- extending validation windows for stronger model comparison
- adding inventory-oriented forecasting outputs
- integrating forecasting visuals into the future Streamlit dashboard