# 🛒 E-Commerce Intelligence System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Completion](https://img.shields.io/badge/Completion-80%25-blue)

**A Comprehensive Data Science Platform for E-Commerce Analytics and Intelligent Decision-Making**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Tech Stack](#-️-tech-stack) • [Contributing](#-contributing)

**[English](README.md) | [简体中文](README.zh-CN.md)**

</div>

---

## 📖 Overview

This is an **intermediate-to-advanced data science comprehensive project** that implements an integrated solution combining "data analysis + machine learning + business intelligence". The project is suitable for **portfolio showcases, graduation projects, and job applications**, covering the complete workflow from data collection to business insights.

### Core Value

- 🎯 **End-to-End Coverage**: Complete pipeline from data ETL to intelligent decision-making
- 🤖 **Multi-Technology Integration**: Statistical testing + Machine Learning + Advanced Analytics
- 📊 **Business-Oriented**: All models and analyses tightly aligned with e-commerce scenarios
- 🚀 **Production-Ready**: Modular design with 8 completed analysis modules

### Project Status

**Completed Modules (8/8):**
- ✅ Satisfaction & Delivery Analysis
- ✅ User Segmentation (RFM Model)
- ✅ Product Category Analysis
- ✅ Geographic Analysis
- ✅ Time Series Analysis & Forecasting
- ✅ Customer Churn Prediction
- ✅ Customer Lifetime Value (CLV) Prediction
- ✅ Recommendation System (Collaborative Filtering & Hybrid)

**Deployment & Presentation Layer:**
- ✅ Interactive Streamlit Dashboard (5 pages)
---

## ✨ Features

### 1️⃣ Data Layer
- ✅ MySQL-based data warehouse design
- ✅ Advanced SQL queries: multi-table joins, window functions
- ✅ Pandas data cleaning and feature engineering
- ✅ Batch data import support (ETL Pipeline)

### 2️⃣ Analysis Layer
- ✅ User behavior analysis (RFM Model)
- ✅ Exploratory Data Analysis (EDA) reports
- ✅ Statistical testing: Chi-square test, linear regression, logistic regression
- ✅ Customer satisfaction analysis
- ✅ Delivery timeliness vs. satisfaction correlation analysis

### 3️⃣ Machine Learning Layer
- ✅ **Personalized Recommendation System**
  - User-based collaborative filtering
  - Item-based collaborative filtering
  - Content-based filtering
  - Hybrid recommendation strategies
- ✅ **Prediction Models**
  - Customer churn prediction (Classification models)
  - Customer Lifetime Value (CLV) prediction (Regression models)
  - Time series forecasting
- ✅ Complete model training, validation, tuning, and evaluation pipeline

### 4️⃣ Output Layer
- 📊 Interactive data analysis reports
- 📈 Streamlit dashboard with 5 interactive pages
- 🧭 Business overview, user insights, product performance, recommendation system, and geographic analysis
- 🎓 Complete project documentation and code comments
- 💾 Reusable model files and CSV outputs

---

## 🏗️ Architecture

```
E-Commerce Intelligence System
│
├── 📁 data/                          # Data Layer
│   ├── brazilian-ecommerce.zip       # Raw data archive
│   ├── olist_customers_dataset.csv   # Customer data
│   ├── olist_orders_dataset.csv      # Order data
│   ├── olist_order_items_dataset.csv # Order item data
│   ├── olist_order_payments_dataset.csv  # Payment data
│   ├── olist_order_reviews_dataset.csv   # Review data
│   ├── olist_products_dataset.csv    # Product data
│   ├── olist_sellers_dataset.csv     # Seller data
│   └── olist_geolocation_dataset.csv # Geolocation data
│
├── 📁 src/                           # Source Code
│   ├── etl/                          # ETL Data Loading Module
│   │   ├── load_customers.py         # Customer data loader
│   │   ├── load_orders.py            # Order data loader
│   │   ├── load_order_items.py       # Order item loader
│   │   ├── load_payments.py          # Payment data loader
│   │   ├── load_products.py          # Product data loader
│   │   ├── load_reviews.py           # Review data loader
│   │   └── load_sellers.py           # Seller data loader
│   │
│   ├── analysis/                     # Data Analysis Module
│   │   ├── user_behavior_analysis.py # User behavior analysis
│   │   └── satisfaction_model.py     # Satisfaction model
│   │
│   └── utils/                        # Utility Module
│       ├── db.py                     # Database connection
│       └── log.py                    # Logging utility
│
├── 📁 sql/                           # SQL Scripts
│   ├── ecommerce_platform.sql        # Database creation script
│   └── create_views.sql              # View creation script
│
├── 📁 Statistical_analysis_report/   # Statistical Analysis Reports (8 Modules)
│   ├── 01_Satisfaction_vs_Delivery.ipynb      # Satisfaction vs. Delivery Analysis
│   ├── 02_User_Segmentation_vs_Value_Analysis_(RFM_Model).ipynb  # User Segmentation (RFM)
│   ├── 03_Product_Category_Analysis.ipynb     # Product Category Analysis
│   ├── 04_Geographic_Analysis.ipynb           # Geographic Distribution Analysis
│   ├── 05_Time_Series_Analysis.ipynb          # Time Series Forecasting
│   ├── 06_Customer_Churn_Prediction.ipynb     # Churn Prediction Model
│   ├── 07_Customer_Lifetime_Value_Prediction.ipynb  # CLV Prediction Model
│   └── 08_Recommendation_System.ipynb         # Recommendation System
├── 📁 dashboard/                     # Streamlit Dashboard App
│   ├── Home.py                       # Business overview homepage
│   ├── pages/
│   │   ├── 1_User_Insights.py        # RFM + Churn + CLV dashboard
│   │   ├── 2_Recommendation_System.py # Recommendation dashboard
│   │   ├── 3_Product_Performance.py   # Category & BCG dashboard
│   │   └── 4_Geographic_Analysis.py   # Regional performance dashboard
│   └── utils/
│       └── data_loader.py            # Shared dashboard data loader
│
├── 📁 output/
│   └── 📁 dashboard/                 # Dashboard-ready CSV outputs
├── 📁 text/                          # Documentation Resources
│   └── prompt.txt                    # Project requirements document
│
└── Import_data_into_sql.ipynb        # Data Import Notebook
```

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Output Layer                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Reports  │  │ Visuals  │  │ Models   │  │   CSV    │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                               ▲
┌─────────────────────────────────────────────────────────────┐
│                     Machine Learning Layer                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Recommend│  │  Churn   │  │Time Series│  │   CLV    │   │
│  │  System  │  │ Predict  │  │ Forecast │  │ Predict  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                               ▲
┌─────────────────────────────────────────────────────────────┐
│                       Analysis Layer                         │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │ Satisfaction│  │   RFM      │  │ Geographic │           │
│  │  Analysis  │  │ Segmentation│  │  Analysis  │           │
│  └────────────┘  └────────────┘  └────────────┘           │
│  ┌────────────┐  ┌────────────┐                            │
│  │  Product   │  │ Statistical│                            │
│  │  Category  │  │   Tests    │                            │
│  └────────────┘  └────────────┘                            │
└─────────────────────────────────────────────────────────────┘
                               ▲
┌─────────────────────────────────────────────────────────────┐
│                        Data Layer                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │   MySQL    │  │  Pandas    │  │  NumPy     │           │
│  │ Warehouse  │  │  Cleaning  │  │ Computing  │           │
│  └────────────┘  └────────────┘  └────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Core Technologies
| Category | Technology | Purpose |
|----------|-----------|---------|
| **Language** | Python 3.8+ | Main development language |
| **Database** | MySQL 8.0+ | Data storage and querying |
| **Data Processing** | Pandas, NumPy | Data cleaning and analysis |
| **Visualization** | Matplotlib, Seaborn, Plotly | Data visualization |
| **Machine Learning** | Scikit-learn, XGBoost, LightGBM | ML model training |
| **Statistics** | SciPy, Statsmodels | Statistical testing |
| **ORM** | SQLAlchemy, PyMySQL | Database operations |
| **Notebook** | Jupyter | Interactive development |

### Key Dependencies
```txt
pandas>=1.3.0
numpy>=1.21.0
pymysql>=1.0.0
sqlalchemy>=2.0.0
scikit-learn>=1.0.0
matplotlib>=3.4.0
seaborn>=0.11.0
jupyter>=1.0.0
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- At least 4GB available memory
- At least 5GB disk space

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ecommerce-intelligence-system.git
cd ecommerce-intelligence-system
```

#### 2. Create Virtual Environment
```bash
# Using venv
python -m venv venv

# Windows activation
venv\Scripts\activate

# Linux/Mac activation
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Database Configuration

**Create the database:**
```bash
mysql -u root -p < sql/ecommerce_platform.sql
```

**Configure database connection:**

Edit `src/utils/db.py` and modify the database configuration:
```python
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "your_username",
    "password": "your_password",
    "database": "ecommerce_platform",
    "charset": "utf8mb4"
}
```

#### 5. Data Import

**Method 1: Using Python Scripts**
```bash
python src/etl/load_customers.py
python src/etl/load_orders.py
python src/etl/load_order_items.py
python src/etl/load_payments.py
python src/etl/load_products.py
python src/etl/load_reviews.py
python src/etl/load_sellers.py
```

**Method 2: Using Jupyter Notebook**
```bash
jupyter notebook Import_data_into_sql.ipynb
```

#### 6. Run Analysis

**Launch Jupyter Notebook:**
```bash
jupyter notebook
```

Open and run the analysis notebooks in order:
1. `Statistical_analysis_report/01_Satisfaction_vs_Delivery.ipynb`
2. `Statistical_analysis_report/02_User_Segmentation_vs_Value_Analysis_(RFM_Model).ipynb`
3. `Statistical_analysis_report/03_Product_Category_Analysis.ipynb`
4. `Statistical_analysis_report/04_Geographic_Analysis.ipynb`
5. `Statistical_analysis_report/05_Time_Series_Analysis.ipynb`
6. `Statistical_analysis_report/06_Customer_Churn_Prediction.ipynb`
7. `Statistical_analysis_report/07_Customer_Lifetime_Value_Prediction.ipynb`
8. `Statistical_analysis_report/08_Recommendation_System.ipynb`

#### 7. Launch the Dashboard

After generating the required outputs, run the Streamlit dashboard:

```bash
python -m streamlit run dashboard/Home.py
```
---

## 📊 Usage Examples

### Example 1: User Behavior Analysis

```python
from src.analysis.user_behavior_analysis import UserBehaviorAnalyzer
from src.utils.db import get_engine

# Initialize analyzer
engine = get_engine()
analyzer = UserBehaviorAnalyzer(engine)

# RFM Analysis
rfm_result = analyzer.rfm_analysis()
print(rfm_result.head())

# Customer Segmentation
segments = analyzer.customer_segmentation(n_clusters=4)
print(segments)
```

### Example 2: Query Order Data

```python
from src.utils.db import get_connection, execute_sql

conn = get_connection()

# Query order status distribution
sql = """
SELECT
    order_status,
    COUNT(*) as order_count
FROM orders_raw
GROUP BY order_status
"""

result = execute_sql(conn, sql)
print(result)
```

### Example 3: Satisfaction Analysis

```python
import pandas as pd
from src.utils.db import get_engine

engine = get_engine()

# Query orders and reviews join data
sql = """
SELECT
    o.order_id,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    r.review_score
FROM orders_raw o
JOIN olist_order_reviews_dataset r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
"""

df = pd.read_sql(sql, engine)

# Calculate delay days
df['delay_days'] = (
    pd.to_datetime(df['order_delivered_customer_date']) -
    pd.to_datetime(df['order_estimated_delivery_date'])
).dt.days

# Analyze delay vs. satisfaction relationship
print(df.groupby('delay_days')['review_score'].mean())
```

---

## 📈 Core Features Demo

### 1. Customer Segmentation (RFM Model)

Segment customers based on **Recency**, **Frequency**, and **Monetary** dimensions:

| Segment | Characteristics | Marketing Strategy |
|---------|----------------|-------------------|
| **High-Value Customers** | High R, High F, High M | VIP exclusive service, priority recommendations |
| **Potential Growth** | High R, Low F, High M | Promotions, bundle sales |
| **At-Risk Customers** | Low R, High F, High M | Member care, retention campaigns |
| **Regular Customers** | Other | Regular marketing, coupons |

### 2. Delivery Timeliness & Satisfaction

Statistical analysis of delivery delay impact on customer satisfaction:

- ✅ On-time delivery: Average rating 4.5 ⭐
- ⚠️ Delay 1-3 days: Average rating 3.8 ⭐
- ❌ Delay 3+ days: Average rating 2.5 ⭐

**Business Insight**: Optimize logistics delivery timeliness to directly improve customer satisfaction and repurchase rates.

### 3. Recommendation System

Multi-algorithm hybrid recommendation system:
- **User-based Collaborative Filtering**: Find similar users and recommend their preferred items
- **Item-based Collaborative Filtering**: Recommend items similar to user's purchase history
- **Content-based Filtering**: Recommend based on product features and categories
- **Hybrid Strategy**: Weighted combination of multiple algorithms

**Key Features:**
- Handles sparse data effectively
- Personalized recommendations for 93,000+ users
- 32,000+ products coverage
- Multiple recommendation strategies for different user segments

---
## Selected Visual Highlights

### CLV Tier Overview
![CLV Overview](docs/images/clv_overview.png)

### Value-Risk Matrix
![Value Risk Matrix](docs/images/value_risk_matrix.png)

### Feature Importance
![Feature Importance](docs/images/feature_importance.png)


---

## 🖥️ Interactive Dashboard

A Streamlit dashboard has been added as the presentation layer of the project.

### Included Pages
- **Home**: KPI overview, monthly trend monitoring, forecast tracking, anomaly detection
- **User Insights**: RFM segmentation, churn risk, CLV tiers, value-risk matrix
- **Recommendation System**: user-level recommendation lookup, offline evaluation, business impact summary
- **Product Performance**: BCG classification, Pareto concentration, category strategy groups
- **Geographic Analysis**: state clusters, satisfaction profiles, regional strategy outputs

### Run Locally
```bash
python -m streamlit run dashboard/Home.py
```

## 🎯 Project Highlights

### Technical Highlights
1. **Modular Architecture**: Decoupled ETL, analysis, and modeling layers, easy to maintain and extend
2. **Complete Data Governance**: Standardized workflow from raw data to feature engineering
3. **Multi-Algorithm Application**: Statistical testing, machine learning, and advanced analytics
4. **8 Complete Analysis Modules**: From data exploration to predictive modeling
5. **Production-Ready Code**: Comprehensive error handling, logging, and documentation
6. **Scalable Recommendation Engine**: Handles 93K+ users and 32K+ products efficiently

### Business Highlights
1. **Closed-Loop Business Value**: End-to-end business deployment from data analysis to intelligent recommendations
2. **High Interpretability**: Each model has clear business meaning and explanation
3. **High Practicality**: All features designed based on real business scenarios
4. **Good Scalability**: Easily adaptable to other e-commerce platform data

---

## 📚 Documentation

### Detailed Documentation Index
- [Data Dictionary](docs/modules/data_dictionary.md) - Data table structure description
- [ETL Pipeline](docs/etl_pipeline.md) - Data loading workflow
- [Analysis Report](docs/analysis_report.md) - Statistical analysis results
- [Model Documentation](docs/model_docs.md) - ML/DL model specifications
- [API Reference](docs/api_reference.md) - API documentation

### Analysis Modules
1. [Satisfaction vs. Delivery Analysis](Statistical_analysis_report/01_Satisfaction_vs_Delivery.ipynb) - Statistical correlation analysis
2. [User Segmentation (RFM Model)](Statistical_analysis_report/02_User_Segmentation_vs_Value_Analysis_(RFM_Model).ipynb) - Customer clustering
3. [Product Category Analysis](Statistical_analysis_report/03_Product_Category_Analysis.ipynb) - BCG matrix & Pareto analysis
4. [Geographic Analysis](Statistical_analysis_report/04_Geographic_Analysis.ipynb) - Regional insights
5. [Time Series Analysis](Statistical_analysis_report/05_Time_Series_Analysis.ipynb) - Trend forecasting
6. [Customer Churn Prediction](Statistical_analysis_report/06_Customer_Churn_Prediction.ipynb) - Classification models
7. [CLV Prediction](Statistical_analysis_report/07_Customer_Lifetime_Value_Prediction.ipynb) - Regression models
8. [Recommendation System](Statistical_analysis_report/08_Recommendation_System.ipynb) - Collaborative & hybrid filtering
9. [Data Import Workflow](Import_data_into_sql.ipynb) - ETL pipeline

---

## Module Documentation

Detailed module documentation is available below:

1. [Module 01 — Satisfaction vs Delivery](docs/modules/01_satisfaction_vs_delivery.md)
2. [Module 02 — User Segmentation & Value Analysis (RFM)](docs/modules/02_rfm_segmentation.md)
3. [Module 03 — Product Category Analysis](docs/modules/03_product_category_analysis.md)
4. [Module 04 — Geographic Analysis](docs/modules/04_geographic_analysis.md)
5. [Module 05 — Time Series Analysis](docs/modules/05_time_series_analysis.md)
6. [Module 06 — Customer Churn Prediction](docs/modules/06_churn_prediction.md)
7. [Module 07 — Customer Lifetime Value (CLV) Prediction](docs/modules/07_clv_prediction.md)
8. [Module 08 — Recommendation System](docs/modules/08_recommendation_system.md)

### Chinese Versions

1. [模块 01 —— 满意度与配送分析](docs/modules/01_satisfaction_vs_delivery.zh-CN.md)
2. [模块 02 —— 用户分群与价值分析（RFM 模型）](docs/modules/02_rfm_segmentation.zh-CN.md)
3. [模块 03 —— 产品类别分析](docs/modules/03_product_category_analysis.zh-CN.md)
4. [模块 04 —— 地理区域分析](docs/modules/04_geographic_analysis.zh-CN.md)
5. [模块 05 —— 时间序列分析](docs/modules/05_time_series_analysis.zh-CN.md)
6. [模块 06 —— 客户流失预测](docs/modules/06_churn_prediction.zh-CN.md)
7. [模块 07 —— 客户生命周期价值（CLV）预测](docs/modules/07_clv_prediction.zh-CN.md)
8. [模块 08 —— 推荐系统](docs/modules/08_recommendation_system.zh-CN.md)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

### Contribution Workflow
1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Standards
- Follow PEP 8 Python code style guidelines
- Add appropriate comments and docstrings
- Ensure all tests pass
- Update relevant documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

---

## 👨‍💻 Author

- **Your Name** - Xin Wang
- **Contact** - 17310353826@163.com
- **GitHub** - [Xin](https://github.com/yourusername/ecommerce-intelligence-system)

---

## 🙏 Acknowledgments

- [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/olistbr/brazilian-ecommerce) - Public dataset provider
- [Scikit-learn](https://scikit-learn.org/) - Machine learning framework
- [TensorFlow](https://www.tensorflow.org/) - Deep learning framework

---

## 📞 Contact

For questions or suggestions, please reach out via:
- 📧 Email: 17310353826
- 💬 WeChat: WX3119096786
- 🐙 GitHub: [Submit an Issue](https://github.com/yourusername/ecommerce-intelligence-system/issues)

---

<div align="center">

**If this project helps you, please give it a ⭐Star to support us!**

Made with ❤️ by [Xin Wang]

</div>
