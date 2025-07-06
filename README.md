# Workcohol-project
Financial Advisor
# 💰 Financial Advisor Dashboard

A comprehensive financial planning and portfolio analysis tool built with Streamlit. This interactive web application helps users analyze their investment portfolios, get personalized recommendations, and plan for retirement.

## 🌟 Features

### 📊 Portfolio Analysis
- **Interactive Portfolio Visualization**: Pie charts and allocation tables
- **Performance Tracking**: Monthly and YTD returns with benchmark comparison
- **Risk Assessment**: Portfolio risk scoring (1-10 scale)
- **Asset Allocation**: Detailed breakdown of investments

### 🎯 Personalized Recommendations
- **Risk-Based Suggestions**: Tailored to Conservative, Moderate, or Aggressive profiles
- **Age-Appropriate Allocation**: Dynamic recommendations based on user age
- **Goal-Oriented Planning**: Retirement, wealth building, income generation
- **Portfolio Optimization**: Alerts for rebalancing opportunities

### 📈 Financial Analysis
- **Savings Rate Analysis**: Track and optimize your savings habits
- **Cash Flow Visualization**: Monthly income vs expenses breakdown
- **Risk Profiling**: Comprehensive risk assessment tools

### 🔮 Future Projections
- **Retirement Planning**: Calculate projected retirement savings
- **Scenario Analysis**: Conservative, moderate, and aggressive growth scenarios
- **Goal Tracking**: Monitor progress toward financial objectives
- **Compound Growth Visualization**: Interactive charts showing savings growth

### ❓ FAQ Management
- **Built-in Financial FAQs**: Common investment and financial questions
- **Custom FAQ Upload**: Upload your own CSV files with Q&A content
- **Search & Filter**: Find relevant information quickly
- **Category Organization**: FAQs organized by topic

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/financial-advisor-dashboard.git
   cd financial-advisor-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 📋 Requirements

```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.24.0
plotly>=5.15.0
yfinance>=0.2.0
```

## 🛠️ Usage

### Getting Started
1. **Set Your Profile**: Enter your age, risk tolerance, and investment goals in the sidebar
2. **Input Financial Data**: Add your current savings, income, and expenses
3. **Portfolio Setup**: Enter your current asset allocations

### Navigation
- **📊 Portfolio**: View current portfolio allocation and performance
- **🎯 Recommendations**: Get personalized investment suggestions
- **📈 Analysis**: Analyze savings rate and financial health
- **🔮 Projections**: Plan for retirement and future goals
- **❓ FAQ**: Access financial education resources

### FAQ Management
- Upload custom FAQ files using the CSV template
- Search and filter questions by category
- Download the FAQ template for easy customization

## 📁 Project Structure

```
financial-advisor-dashboard/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── data/                 # Data files (optional)
│   └── faq_template.csv  # FAQ template
├── assets/               # Images and static files
└── .gitignore           # Git ignore file
```

## 🎨 Customization

### Adding New Asset Classes
Modify the `portfolio_data` dictionary in the sidebar section to include additional asset types.

### Custom Risk Scoring
Update the `risk_weights` dictionary in the `calculate_risk_score()` function to adjust risk calculations.

### Styling
The application uses custom CSS defined in the `st.markdown()` section. Modify the styles to match your preferences.

## 📊 Data Sources

- **Market Data**: Yahoo Finance API (yfinance)
- **Portfolio Data**: User input via Streamlit interface
- **FAQ Data**: CSV upload or built-in default questions

## 🔧 Technical Details

### Key Functions
- `create_portfolio_pie_chart()`: Portfolio visualization
- `calculate_portfolio_metrics()`: Risk and performance calculations
- `get_investment_recommendations()`: Personalized suggestions
- `calculate_retirement_projection()`: Future value calculations

### Data Management
- Session state management for user data persistence
- CSV file handling for FAQ content
- Real-time data fetching from financial APIs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit**: For the amazing web app framework
- **Plotly**: For interactive visualizations
- **Yahoo Finance**: For market data API
- **Pandas**: For data manipulation capabilities

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the FAQ section in the app
- Review the documentation

## 🔄 Updates

### Version 1.0.0
- Initial release with core portfolio analysis features
- Personalized investment recommendations
- Retirement planning tools
- FAQ management system

---

**⭐ If you find this project helpful, please give it a star on GitHub!**
