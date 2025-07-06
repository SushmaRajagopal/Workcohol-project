import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import warnings
import io
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Financial Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for better styling
st.markdown("""
<style>
                    
    .main-header {
        font-size: 2.5rem;
        font-family: 'Calibri', sans-serif;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        font-family: 'Inter', sans-serif;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .recommendation-card {
        background-color: #e8f4f8;
        font-family: 'Inter', sans-serif;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .recommendation-card h4 {
        color: #1f4e79;
        margin-bottom: 0.5rem;
    }
    .recommendation-card p {
        color: #2c5282;
        margin: 0;
    }
    .warning-card {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
    }
    .warning-card h4 {
        color: #856404;
        margin-bottom: 0.5rem;
    }
    .warning-card p {
        color: #856404;
        margin: 0;
    }
    .success-card {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
    }
    .success-card h4 {
        color: #155724;
        margin-bottom: 0.5rem;
    }
    .success-card p {
        color: #155724;
        margin: 0;
    }
    .faq-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #6c757d;
    }
    .faq-question {
        color: #495057;
        font-family: 'Inter', sans-serif;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .faq-answer {
        color: #6c757d;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = {
        'Stocks': 45000,
        'Bonds': 18000,
        'Real Estate': 9000,
        'Cash': 3000,
        'Commodities': 0,
        'Crypto': 0
    }

# Initialize FAQ data
if 'faq_data' not in st.session_state:
    # Default FAQ data
    st.session_state.faq_data = pd.DataFrame({
        'Question': [
            'What is a good savings rate?',
            'How should I allocate my portfolio by age?',
            'What is the difference between stocks and bonds?',
            'How much should I save for retirement?',
            'What is dollar-cost averaging?',
            'Should I invest in index funds or individual stocks?',
            'What is an emergency fund and how much should I save?',
            'How do I determine my risk tolerance?',
            'What are the benefits of diversification?',
            'When should I rebalance my portfolio?'
        ],
        'Answer': [
            'A good savings rate is typically 10-20% of your income. If you can save 20% or more, you\'re in excellent shape for building wealth.',
            'A common rule is to subtract your age from 100 to get your stock allocation percentage. For example, if you\'re 30, consider 70% stocks and 30% bonds.',
            'Stocks represent ownership in companies and offer growth potential but with higher risk. Bonds are loans to companies/governments and provide steady income with lower risk.',
            'Aim to save 10-15% of your income for retirement. The earlier you start, the more compound interest works in your favor.',
            'Dollar-cost averaging involves investing a fixed amount regularly regardless of market conditions. This helps reduce the impact of market volatility.',
            'Index funds offer instant diversification and low fees, making them ideal for beginners. Individual stocks require more research and carry higher risk.',
            'An emergency fund should cover 3-6 months of expenses. Keep it in a high-yield savings account for easy access.',
            'Risk tolerance depends on your age, income stability, investment timeline, and emotional comfort with market fluctuations.',
            'Diversification reduces risk by spreading investments across different asset classes, sectors, and geographic regions.',
            'Rebalance your portfolio annually or when allocations drift more than 5-10% from your target percentages.'
        ],
        'Category': [
            'Savings', 'Asset Allocation', 'Investments', 'Retirement', 'Investment Strategy',
            'Investment Strategy', 'Emergency Planning', 'Risk Management', 'Portfolio Management', 'Portfolio Management'
        ]
    })

def create_portfolio_pie_chart(portfolio_data):
    """Create portfolio allocation pie chart"""
    df = pd.DataFrame(list(portfolio_data.items()), columns=['Asset', 'Value'])
    df = df[df['Value'] > 0]  # Only show assets with value > 0
    
    fig = px.pie(df, values='Value', names='Asset', 
                title='Portfolio Allocation',
                color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    return fig

def get_market_data(symbols=['SPY', 'AGG', 'VTI', 'BND'], period='1y'):
    """Fetch market data for comparison"""
    try:
        data = yf.download(symbols, period=period, group_by='ticker', auto_adjust=True)
        return data
    except:
        # Return dummy data if yfinance fails
        dates = pd.date_range(end=datetime.now(), periods=252, freq='D')
        dummy_data = {}
        for symbol in symbols:
            dummy_data[symbol] = pd.DataFrame({
                'Close': np.random.randn(252).cumsum() + 100
            }, index=dates)
        return dummy_data

def calculate_portfolio_metrics(portfolio_data):
    """Calculate key portfolio metrics"""
    total_value = sum(portfolio_data.values())
    
    # Calculate allocation percentages
    allocations = {asset: (value/total_value)*100 for asset, value in portfolio_data.items() if value > 0}
    
    # Simulate returns (in real app, use actual historical data)
    np.random.seed(42)  # For consistent results
    monthly_return = np.random.normal(0.8, 2.5)  # 0.8% average monthly return
    ytd_return = np.random.normal(8.5, 15)  # 8.5% average YTD return
    
    metrics = {
        'total_value': total_value,
        'monthly_return': monthly_return,
        'ytd_return': ytd_return,
        'allocations': allocations,
        'risk_score': calculate_risk_score(allocations)
    }
    
    return metrics

def calculate_risk_score(allocations):
    """Calculate portfolio risk score (1-10 scale)"""
    risk_weights = {
        'Stocks': 0.8,
        'Bonds': 0.2,
        'Real Estate': 0.6,
        'Cash': 0.0,
        'Commodities': 0.7,
        'Crypto': 1.0
    }
    
    weighted_risk = sum(allocations.get(asset, 0) * weight for asset, weight in risk_weights.items())
    risk_score = (weighted_risk / 100) * 10
    return min(risk_score, 10)

def get_investment_recommendations(risk_tolerance, age, investment_goal):
    """Generate investment recommendations based on user profile"""
    recommendations = {}
    
    if risk_tolerance == 'Conservative':
        recommendations = {
            'Government Bonds': {'allocation': 40, 'reason': 'Stable income with capital preservation'},
            'High-Grade Corporate Bonds': {'allocation': 30, 'reason': 'Moderate returns with lower risk'},
            'Dividend Stocks': {'allocation': 20, 'reason': 'Steady income from established companies'},
            'Cash/Money Market': {'allocation': 10, 'reason': 'Liquidity and emergency fund'}
        }
    elif risk_tolerance == 'Moderate':
        recommendations = {
            'Index Funds': {'allocation': 35, 'reason': 'Broad market exposure with low fees'},
            'Growth Stocks': {'allocation': 25, 'reason': 'Long-term capital appreciation'},
            'Investment Grade Bonds': {'allocation': 25, 'reason': 'Income generation and stability'},
            'REITs': {'allocation': 15, 'reason': 'Real estate exposure and dividends'}
        }
    else:  # Aggressive
        recommendations = {
            'Growth Stocks': {'allocation': 40, 'reason': 'High growth potential'},
            'Small-Cap Stocks': {'allocation': 25, 'reason': 'Higher risk, higher reward'},
            'International/Emerging Markets': {'allocation': 20, 'reason': 'Geographic diversification'},
            'Corporate Bonds': {'allocation': 15, 'reason': 'Income component'}
        }
    
    # Age-based adjustment
    if age > 50:
        # Increase bond allocation for older investors
        for asset in recommendations:
            if 'Bond' in asset:
                recommendations[asset]['allocation'] += 5
            elif 'Stock' in asset or 'Growth' in asset:
                recommendations[asset]['allocation'] -= 2
    
    return recommendations

def calculate_retirement_projection(current_savings, monthly_contribution, years_to_retirement, expected_return=0.07):
    """Calculate retirement savings projection"""
    future_value = current_savings * (1 + expected_return) ** years_to_retirement
    
    # Future value of annuity (monthly contributions)
    if monthly_contribution > 0:
        monthly_rate = expected_return / 12
        months = years_to_retirement * 12
        annuity_fv = monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        future_value += annuity_fv
    
    return future_value

def load_faq_from_csv(uploaded_file):
    """Load FAQ data from uploaded CSV file"""
    try:
        df = pd.read_csv(uploaded_file)
        # Ensure required columns exist
        required_columns = ['Question', 'Answer']
        if not all(col in df.columns for col in required_columns):
            st.error("CSV file must contain 'Question' and 'Answer' columns")
            return None
        
        # Add Category column if it doesn't exist
        if 'Category' not in df.columns:
            df['Category'] = 'General'
        
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {str(e)}")
        return None

def main():
    st.markdown('<h1 class="main-header">💰 Financial Advisor</h1>', unsafe_allow_html=True)
    st.markdown("### Personalized Investment Analysis & Recommendations")
    
    # Sidebar for user inputs
    st.sidebar.header("👤 Your Profile")
    
    # User profile inputs
    age = st.sidebar.slider("Age", 18, 80, 35)
    risk_tolerance = st.sidebar.selectbox("Risk Tolerance", ["Conservative", "Moderate", "Aggressive"])
    investment_goal = st.sidebar.selectbox("Primary Goal", 
                                         ["Retirement", "Wealth Building", "Income Generation", "Education Fund"])
    current_savings = st.sidebar.number_input("Current Savings ($)", value=50000, step=1000)
    monthly_income = st.sidebar.number_input("Monthly Income ($)", value=5000, step=500)
    monthly_expenses = st.sidebar.number_input("Monthly Expenses ($)", value=3500, step=500)
    monthly_investment = st.sidebar.number_input("Monthly Investment ($)", value=500, step=100)
    
    # Portfolio inputs
    st.sidebar.header("💼 Current Portfolio")
    portfolio_data = {}
    portfolio_data['Stocks'] = st.sidebar.number_input("Stocks ($)", value=st.session_state.portfolio_data['Stocks'])
    portfolio_data['Bonds'] = st.sidebar.number_input("Bonds ($)", value=st.session_state.portfolio_data['Bonds'])
    portfolio_data['Real Estate'] = st.sidebar.number_input("Real Estate ($)", value=st.session_state.portfolio_data['Real Estate'])
    portfolio_data['Cash'] = st.sidebar.number_input("Cash ($)", value=st.session_state.portfolio_data['Cash'])
    portfolio_data['Commodities'] = st.sidebar.number_input("Commodities ($)", value=st.session_state.portfolio_data['Commodities'])
    portfolio_data['Crypto'] = st.sidebar.number_input("Crypto ($)", value=st.session_state.portfolio_data['Crypto'])
    
    # Update session state
    st.session_state.portfolio_data = portfolio_data
    
    # Calculate metrics
    metrics = calculate_portfolio_metrics(portfolio_data)
    savings_rate = ((monthly_income - monthly_expenses) / monthly_income) * 100 if monthly_income > 0 else 0
    
    # Main dashboard
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Portfolio", "🎯 Recommendations", "📈 Analysis", "🔮 Projections", "❓ FAQ"])
    
    with tab1:
        st.header("Portfolio Overview")
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Value", f"${metrics['total_value']:,.0f}", 
                     f"{metrics['monthly_return']:+.1f}%")
        
        with col2:
            st.metric("Monthly Return", f"{metrics['monthly_return']:+.1f}%", 
                     "vs last month")
        
        with col3:
            st.metric("YTD Performance", f"{metrics['ytd_return']:+.1f}%", 
                     "vs S&P 500")
        
        with col4:
            st.metric("Risk Score", f"{metrics['risk_score']:.1f}/10", 
                     f"{risk_tolerance}")
        
        st.divider()
        
        # Portfolio visualization
        col1, col2 = st.columns(2)
        
        with col1:
            # Portfolio pie chart
            fig_pie = create_portfolio_pie_chart(portfolio_data)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Asset allocation table
            st.subheader("Asset Breakdown")
            df_portfolio = pd.DataFrame(list(portfolio_data.items()), columns=['Asset', 'Value'])
            df_portfolio = df_portfolio[df_portfolio['Value'] > 0]
            df_portfolio['Percentage'] = (df_portfolio['Value'] / df_portfolio['Value'].sum() * 100).round(1)
            df_portfolio['Value'] = df_portfolio['Value'].apply(lambda x: f"${x:,.0f}")
            df_portfolio['Percentage'] = df_portfolio['Percentage'].apply(lambda x: f"{x}%")
            st.dataframe(df_portfolio, use_container_width=True, hide_index=True)
        
        # Performance comparison chart
        st.subheader("Performance Comparison")
        
        # Create dummy performance data
        dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
        performance_data = pd.DataFrame({
            'Date': dates,
            'Your Portfolio': np.random.randn(12).cumsum() + 100,
            'S&P 500': np.random.randn(12).cumsum() + 100,
            'Bond Index': np.random.randn(12).cumsum() + 100
        })
        
        fig_line = px.line(performance_data, x='Date', y=['Your Portfolio', 'S&P 500', 'Bond Index'],
                          title='Portfolio Performance vs Benchmarks')
        st.plotly_chart(fig_line, use_container_width=True)
    
    with tab2:
        st.header("Investment Recommendations")
        
        # Get recommendations
        recommendations = get_investment_recommendations(risk_tolerance, age, investment_goal)
        
        st.markdown(f"**Based on your {risk_tolerance.lower()} risk profile and {investment_goal.lower()} goal:**")
        
        # Display recommendations
        for asset, details in recommendations.items():
            st.markdown(f"""
            <div class="recommendation-card">
                <h4>{asset} - {details['allocation']}%</h4>
                <p>{details['reason']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Portfolio optimization suggestions
        st.subheader("Portfolio Optimization")
        
        current_stock_pct = metrics['allocations'].get('Stocks', 0)
        recommended_stock_pct = 100 - age  # Age-based rule
        
        if abs(current_stock_pct - recommended_stock_pct) > 10:
            if current_stock_pct > recommended_stock_pct:
                st.markdown(f"""
                <div class="warning-card">
                    <h4>⚠️ High Stock Allocation</h4>
                    <p>Consider reducing stock allocation from {current_stock_pct:.1f}% to ~{recommended_stock_pct}% based on your age.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="success-card">
                    <h4>📈 Growth Opportunity</h4>
                    <p>Consider increasing stock allocation from {current_stock_pct:.1f}% to ~{recommended_stock_pct}% for better growth potential.</p>
                </div>
                """, unsafe_allow_html=True)
        
        if metrics['allocations'].get('Cash', 0) > 15:
            st.markdown("""
            <div class="warning-card">
                <h4>💰 High Cash Allocation</h4>
                <p>Consider investing excess cash in diversified funds to improve returns.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.header("Financial Analysis")
        
        # Savings rate analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Savings Rate Analysis")
            st.metric("Current Savings Rate", f"{savings_rate:.1f}%")
            
            if savings_rate < 10:
                st.markdown("""
                <div class="warning-card">
                    <h4>⚠️ Low Savings Rate</h4>
                    <p>Consider increasing your savings rate to at least 10-15% of income.</p>
                </div>
                """, unsafe_allow_html=True)
            elif savings_rate > 20:
                st.markdown("""
                <div class="success-card">
                    <h4>✅ Excellent Savings Rate</h4>
                    <p>You're on track for strong financial growth!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="success-card">
                    <h4>✅ Good Savings Rate</h4>
                    <p>Your savings rate is healthy for building wealth.</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("Risk Assessment")
            
            # Fixed Risk gauge with properly centered number
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = metrics['risk_score'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Portfolio Risk Score", 'font': {'size': 20}},
                number = {
                    'font': {'size': 50, 'color': 'darkblue'},
                    'valueformat': '.1f'
                },
                gauge = {
                    'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "darkblue", 'thickness': 0.3},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 3], 'color': "lightgreen"},
                        {'range': [3, 7], 'color': "yellow"},
                        {'range': [7, 10], 'color': "lightcoral"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 8
                    }
                }
            ))
            
            fig_gauge.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=60, b=20),
                font={'color': "darkblue"},
                paper_bgcolor="white",
                plot_bgcolor="white"
            )
            
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Monthly cash flow analysis
        st.subheader("Monthly Cash Flow")
        cash_flow_data = {
            'Category': ['Income', 'Expenses', 'Available for Investment'],
            'Amount': [monthly_income, -monthly_expenses, monthly_income - monthly_expenses],
            'Color': ['green', 'red', 'blue']
        }
        
        fig_bar = px.bar(cash_flow_data, x='Category', y='Amount', color='Color',
                        title='Monthly Cash Flow Analysis')
        fig_bar.update_traces(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab4:
        st.header("Future Projections")
        
        # Retirement planning
        years_to_retirement = max(65 - age, 0)
        retirement_projection = calculate_retirement_projection(
            current_savings, monthly_investment, years_to_retirement
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Retirement Projection")
            st.metric("Projected Retirement Savings", f"${retirement_projection:,.0f}")
            st.metric("Years to Retirement", f"{years_to_retirement} years")
            
            # Retirement needs (25x annual expenses rule)
            annual_expenses = monthly_expenses * 12
            retirement_needs = annual_expenses * 25
            st.metric("Estimated Retirement Needs", f"${retirement_needs:,.0f}")
            
            if retirement_projection >= retirement_needs:
                st.markdown("""
                <div class="success-card">
                    <h4>✅ On Track for Retirement</h4>
                    <p>Your current savings plan should meet your retirement needs!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                shortfall = retirement_needs - retirement_projection
                st.markdown(f"""
                <div class="warning-card">
                    <h4>⚠️ Retirement Shortfall</h4>
                    <p>You may have a shortfall of ${shortfall:,.0f}. Consider increasing monthly contributions.</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("Savings Growth Projection")
            
            # Create projection chart
            years = list(range(0, years_to_retirement + 1))
            projected_values = []
            
            for year in years:
                value = calculate_retirement_projection(current_savings, monthly_investment, year)
                projected_values.append(value)
            
            projection_df = pd.DataFrame({
                'Year': [datetime.now().year + year for year in years],
                'Projected Value': projected_values
            })
            
            fig_projection = px.line(projection_df, x='Year', y='Projected Value',
                                   title='Retirement Savings Growth')
            fig_projection.add_hline(y=retirement_needs, line_dash="dash", 
                                   line_color="red", annotation_text="Retirement Goal")
            st.plotly_chart(fig_projection, use_container_width=True)
        
        # Scenario analysis
        st.subheader("Scenario Analysis")
        
        scenarios = {
            'Conservative (5% return)': calculate_retirement_projection(current_savings, monthly_investment, years_to_retirement, 0.05),
            'Moderate (7% return)': calculate_retirement_projection(current_savings, monthly_investment, years_to_retirement, 0.07),
            'Aggressive (9% return)': calculate_retirement_projection(current_savings, monthly_investment, years_to_retirement, 0.09)
        }
        
        scenario_df = pd.DataFrame(list(scenarios.items()), columns=['Scenario', 'Projected Value'])
        scenario_df['Projected Value'] = scenario_df['Projected Value'].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(scenario_df, use_container_width=True, hide_index=True)
    
    with tab5:
        st.header("Frequently Asked Questions")
        
        # FAQ CSV upload section
        st.subheader("📁 Upload Custom FAQ")
        uploaded_file = st.file_uploader("Upload CSV file with FAQ data", type=['csv'])
        
        if uploaded_file is not None:
            new_faq_data = load_faq_from_csv(uploaded_file)
            if new_faq_data is not None:
                st.session_state.faq_data = new_faq_data
                st.success("FAQ data loaded successfully!")
        
        # Download template button
        template_df = pd.DataFrame({
            'Question': ['What is compound interest?', 'How do I start investing?'],
            'Answer': ['Compound interest is interest earned on both principal and previously earned interest.', 'Start by determining your risk tolerance and investment goals, then consider low-cost index funds.'],
            'Category': ['Investments', 'Getting Started']
        })
        
        csv_buffer = io.StringIO()
        template_df.to_csv(csv_buffer, index=False)
        csv_string = csv_buffer.getvalue()
        
        st.download_button(
            label="📥 Download FAQ Template",
            data=csv_string,
            file_name="faq_template.csv",
            mime="text/csv"
        )
        
        st.divider()
        
        # FAQ display section
        st.subheader("💡 Investment & Financial FAQs")
        
        # Category filter
        categories = ['All'] + list(st.session_state.faq_data['Category'].unique())
        selected_category = st.selectbox("Filter by Category", categories)
        
        # Search functionality
        search_query = st.text_input("🔍 Search FAQs", placeholder="Type keywords to search...")
        
        # Filter FAQ data
        filtered_faq = st.session_state.faq_data.copy()
        
        if selected_category != 'All':
            filtered_faq = filtered_faq[filtered_faq['Category'] == selected_category]
        
        if search_query:
            mask = (filtered_faq['Question'].str.contains(search_query, case=False, na=False) |
                   filtered_faq['Answer'].str.contains(search_query, case=False, na=False))
            filtered_faq = filtered_faq[mask]
        
        # Display FAQs
        if filtered_faq.empty:
            st.info("No FAQs found matching your criteria.")
        else:
            for idx, row in filtered_faq.iterrows():
                with st.expander(f"❓ {row['Question']}"):
                    st.markdown(f"**Category:** {row['Category']}")
                    st.markdown(f"**Answer:** {row['Answer']}")
        
        st.divider()
        
        # FAQ Statistics
        st.subheader("📊 FAQ Statistics")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Questions", len(st.session_state.faq_data))
            st.metric("Categories", len(st.session_state.faq_data['Category'].unique()))
        
        with col2:
            # Category distribution
            category_counts = st.session_state.faq_data['Category'].value_counts()
            fig_cat = px.bar(x=category_counts.index, y=category_counts.values,
                            title='Questions by Category')
            fig_cat.update_layout(height=300)
            st.plotly_chart(fig_cat, use_container_width=True)

if __name__ == "__main__":
    main()