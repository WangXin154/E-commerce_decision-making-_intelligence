
# CLV Prediction Project - Business Insights

## 1. Model Performance
- Best model: Random Forest
- RMSE on log target: 0.2637
- R² on log target: 0.8112
- MAE on raw target: 2.0837
- RMSE on raw target: 35.4938

## 2. Customer Value Distribution
- Top 10% positive-customer contribution: 37.13% of total future GMV
- Platinum average predicted CLV: 146.29
- Gold average predicted CLV: 15.56
- Silver average predicted CLV: 0.20
- Bronze average predicted CLV: 0.00

## 3. Top 5 Predictive Factors
- R_score: 0.6299
- total_orders: 0.0573
- F_score: 0.0558
- exploration_rate: 0.0498
- unique_products_purchased: 0.0336

## 4. Value-Risk Findings
                   customer_count  predicted_clv_mean  predicted_clv_sum  actual_gmv_mean  actual_gmv_sum  risk_score_mean
strategy_quadrant                                                                                                         
Protect                       269               67.64           18195.14           120.92        32528.06             0.53
Retain                         43               69.79            3000.81           136.34         5862.66             0.82
Nurture                      8936                0.01              45.73             0.00            0.00             0.54
Low Priority                 4515                0.00              17.15             0.00            0.00             0.88

## 5. Marketing Budget Suggestions
- Platinum budget per customer: 6892.28
- Platinum expected ROI: 0.02x

## 6. Business Actions
1. Focus on high-value customers with VIP-style retention and service.
2. Apply differentiated marketing by customer value tier.
3. Prioritize urgent retention for high-value high-risk customers.
4. Develop uplift strategies for lower-value but promising customers.
5. Evaluate acquisition efficiency with a CLV-to-CAC logic.
