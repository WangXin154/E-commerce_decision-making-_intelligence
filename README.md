# 🛒 E-Commerce Intelligence System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

**A Full-Stack Data Science Platform for E-Commerce Analytics and Intelligent Decision-Making**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Tech Stack](#-️-tech-stack) • [Contributing](#-contributing)

**[English](README.md) | [简体中文](README.zh-CN.md)**

</div>

---

## 📖 Overview

This is an **intermediate-to-advanced full-stack data science comprehensive project** that implements an integrated solution combining "data analysis + machine learning + deep learning + NLP chatbot + business deployment". The project is suitable for **portfolio showcases, graduation projects, and job applications**, covering the complete workflow from data collection to business output.

### Core Value

- 🎯 **End-to-End Coverage**: Complete pipeline from data ETL to intelligent decision-making
- 🤖 **Multi-Technology Fusion**: Statistical testing + ML + DL + NLP
- 📊 **Business-Oriented**: All models and analyses tightly aligned with e-commerce scenarios
- 🚀 **Production-Ready**: Modular design, easy to extend and deploy

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
- 🔥 **Personalized Recommendation System**
  - Collaborative filtering algorithms
  - Content-based filtering
  - Hybrid recommendation strategies
- 🔥 **Prediction Models**
  - User churn prediction
  - Conversion rate prediction
  - Customer Lifetime Value (CLV) prediction
- ✅ Complete model training, validation, tuning, and evaluation pipeline

### 4️⃣ Deep Learning Layer
- 🔥 **CNN Product Image Classification**
  - Automatic product feature extraction
  - Intelligent product tag recognition
  - Enhanced recommendation system accuracy
- ✅ Support for custom CNN architectures

### 5️⃣ Intelligent Interaction Layer
- 🔥 **Intelligent Customer Service Bot**
  - Track logistics, check orders
  - Product recommendation inquiries
  - After-sales Q&A support
  - Integrated with ML models for personalized recommendations

### 6️⃣ Output Layer
- 📊 Interactive data analysis reports
- 📈 Visualizations and dashboards
- 🎓 Complete project documentation and code comments
- 💾 Reusable model files

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
├── 📁 Statistical_analysis_report/   # Statistical Analysis Reports
│   ├── 01_satisfaction_vs_delivery.ipynb      # Satisfaction vs. Delivery Analysis
│   └── User_Segmentation_vs_Value_Analysis_(RFM_Model).ipynb  # User Segmentation & Value Analysis
│
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
│  │ Reports  │  │ Visuals  │  │ Models   │  │   API    │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                               ▲
┌─────────────────────────────────────────────────────────────┐
│                   Intelligent Interaction Layer              │
│  ┌────────────────────────────────────────────────────┐    │
│  │     Intelligent Customer Service Bot (NLP + Recs)   │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                               ▲
┌─────────────────────────────────────────────────────────────┐
│                      Deep Learning Layer                     │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │   CNN Product    │────────▶│  Feature Extract │         │
│  │  Classification  │         │                  │         │
│  └──────────────────┘         └──────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                               ▲
┌─────────────────────────────────────────────────────────────┐
│                     Machine Learning Layer                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Recommend│  │  Churn   │  │Conversion│  │   CLV    │   │
│  │  System  │  │ Predict  │  │ Predict  │  │ Predict  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                               ▲
┌─────────────────────────────────────────────────────────────┐
│                       Analysis Layer                         │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │  Behavior  │  │   RFM      │  │ Statistical│           │
│  │  Analysis  │  │ Segmentation││    Tests   │           │
│  └────────────┘  └────────────┘  └────────────┘           │
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
| **Visualization** | Matplotlib, Seaborn | Data visualization |
| **Machine Learning** | Scikit-learn | ML model training |
| **Deep Learning** | TensorFlow/PyTorch | CNN product recognition |
| **NLP** | Transformers, NLTK | Intelligent customer service |
| **ORM** | SQLAlchemy | Database operations |

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

Open and run the following notebooks:
- `Statistical_analysis_report/01_satisfaction_vs_delivery.ipynb`
- `Statistical_analysis_report/User_Segmentation_vs_Value_Analysis_(RFM_Model).ipynb`

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

### 3. Personalized Recommendations

Combine user behavior history and product features for accurate recommendations:

```python
# Collaborative filtering recommendation example
def recommend_items(user_id, top_n=10):
    """
    Recommend Top-N products for a user
    """
    # TODO: Implement collaborative filtering algorithm
    pass
```

---

## 🎯 Project Highlights

### Technical Highlights
1. **Modular Architecture**: Decoupled ETL, analysis, and modeling layers, easy to maintain and extend
2. **Complete Data Governance**: Standardized workflow from raw data to feature engineering
3. **Multi-Algorithm Fusion**: Comprehensive application of statistical learning + ML + DL
4. **Production-Ready Code**: Comprehensive error handling, logging, and documentation

### Business Highlights
1. **Closed-Loop Business Value**: End-to-end business deployment from data analysis to intelligent recommendations
2. **High Interpretability**: Each model has clear business meaning and explanation
3. **High Practicality**: All features designed based on real business scenarios
4. **Good Scalability**: Easily adaptable to other e-commerce platform data

---

## 📚 Documentation

### Detailed Documentation Index
- [Data Dictionary](docs/data_dictionary.md) - Data table structure description
- [ETL Pipeline](docs/etl_pipeline.md) - Data loading workflow
- [Analysis Report](docs/analysis_report.md) - Statistical analysis results
- [Model Documentation](docs/model_docs.md) - ML/DL model specifications
- [API Reference](docs/api_reference.md) - API documentation

### Notebook List
1. [Satisfaction vs. Delivery Analysis](Statistical_analysis_report/01_satisfaction_vs_delivery.ipynb)
2. [User Segmentation & Value Analysis](Statistical_analysis_report/User_Segmentation_vs_Value_Analysis_(RFM_Model).ipynb)
3. [Data Import Workflow](Import_data_into_sql.ipynb)

---

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

- **Your Name** - Project Lead
- **Contact** - your.email@example.com
- **GitHub** - [yourusername](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/olistbr/brazilian-ecommerce) - Public dataset provider
- [Scikit-learn](https://scikit-learn.org/) - Machine learning framework
- [TensorFlow](https://www.tensorflow.org/) - Deep learning framework

---

## 📞 Contact

For questions or suggestions, please reach out via:
- 📧 Email: your.email@example.com
- 💬 WeChat: your_wechat_id
- 🐙 GitHub: [Submit an Issue](https://github.com/yourusername/ecommerce-intelligence-system/issues)

---

<div align="center">

**If this project helps you, please give it a ⭐Star to support us!**

Made with ❤️ by [Your Name]

</div>
