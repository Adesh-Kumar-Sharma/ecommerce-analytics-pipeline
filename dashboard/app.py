import streamlit as st
import pandas as pd
import plotly.express as px
from utils import utils
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        border: 1px solid #e6e9ef;
        padding: 1rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📊 Analytics Dashboard")
st.sidebar.markdown("---")

# Date range selector
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
with col2:
    end_date = st.date_input("End Date", datetime.now())

# Page selector
page = st.sidebar.selectbox(
    "Select Analysis",
    ["📈 Overview", "👥 Customers", "📦 Products", "📊 Advanced Analytics"]
)

st.sidebar.markdown("---")
refresh_button = st.sidebar.button("🔄 Refresh Data")

# Main content
if page == "📈 Overview":
    st.title("📈 Sales Overview Dashboard")
    st.markdown("Real-time business intelligence and key performance indicators")

    # Load daily sales data
    daily_sales_query = f"""
    SELECT * FROM sales_summary 
    WHERE summary_date BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY summary_date DESC
    """
    
    # Calculate the previous period for comparison
    period_days = (end_date - start_date).days
    prev_start_date = start_date - pd.Timedelta(days=period_days + 1)
    prev_end_date = start_date - pd.Timedelta(days=1)

    # Query the sales_summary table for BOTH periods
    current_df = utils.load_data(f"SELECT * FROM sales_summary WHERE summary_date BETWEEN '{start_date}' AND '{end_date}'")
    prev_df = utils.load_data(f"SELECT * FROM sales_summary WHERE summary_date BETWEEN '{prev_start_date}' AND '{prev_end_date}'")

    # Calculate the TOTALS for each period
    current_totals = {
        'total_revenue': current_df['total_revenue'].sum(),
        'total_orders': current_df['total_orders'].sum(),
        'total_customers': current_df['total_customers'].sum(), # This sums the daily counts
        'avg_order_value': current_df['avg_order_value'].mean()  # This takes the average of the daily averages
    }

    prev_totals = {
        'total_revenue': prev_df['total_revenue'].sum(),
        'total_orders': prev_df['total_orders'].sum(),
        'total_customers': prev_df['total_customers'].sum(),
        'avg_order_value': prev_df['avg_order_value'].mean()
    }

    # Calculate the percentage changes (deltas)

    # Check revenue
    if prev_totals['total_revenue'] > 0:
        revenue_change = ((current_totals['total_revenue'] - prev_totals['total_revenue']) / prev_totals['total_revenue']) * 100
    else:
        revenue_change = 0  # Can't calculate change from 0

    # Check orders
    if prev_totals['total_orders'] > 0:
        orders_change = ((current_totals['total_orders'] - prev_totals['total_orders']) / prev_totals['total_orders']) * 100
    else:
        orders_change = 0

    # Check customers
    if prev_totals['total_customers'] > 0:
        customers_change = ((current_totals['total_customers'] - prev_totals['total_customers']) / prev_totals['total_customers']) * 100
    else:
        customers_change = 0

    # Check average order value (must check for both NaN and 0)
    if pd.notna(prev_totals['avg_order_value']) and prev_totals['avg_order_value'] != 0:
        aov_change = ((current_totals['avg_order_value'] - prev_totals['avg_order_value']) / prev_totals['avg_order_value']) * 100
    else:
        aov_change = 0

    # Now that all variables are safely defined, add them to the dictionary
    current_totals['revenue_change'] = revenue_change
    current_totals['orders_change'] = orders_change
    current_totals['customers_change'] = customers_change
    current_totals['aov_change'] = aov_change

    # And pass the complete object to your function
    col1, col2, col3, col4 = st.columns(4)
    utils.create_metric_cards(col1, col2, col3, col4, current_totals)

    try:
        daily_sales = utils.load_data(daily_sales_query)
        
        if len(daily_sales) > 0:
            # Calculate metrics
            total_revenue = daily_sales['total_revenue'].sum()
            total_orders = daily_sales['total_orders'].sum()
            total_customers = daily_sales['total_customers'].sum()
            avg_order_value = daily_sales['avg_order_value'].mean()

            metrics = {
                'total_revenue': total_revenue,
                'total_orders': total_orders,
                'total_customers': total_customers,
                'avg_order_value': avg_order_value
            }
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(
                    utils.create_revenue_chart(daily_sales),
                    use_container_width=True
                )
            
            with col2:
                # Orders vs Customers chart
                fig = px.line(
                    daily_sales,
                    x='summary_date',
                    y=['total_orders', 'total_customers'],
                    labels={'summary_date': 'Date'},
                    title='Orders vs Customers Trend'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Recent performance table
            st.subheader("📋 Recent Performance (Last 7 Days)")
            recent_data = daily_sales.head(7)
            st.dataframe(
                recent_data[['summary_date', 'total_orders', 'total_revenue', 'total_customers', 'avg_order_value']],
                use_container_width=True
            )
        
        else:
            st.warning("No data found for the selected date range.")
            
    except Exception as e:
        st.error(f"Error loading data: {e}")

elif page == "👥 Customers":
    st.title("👥 Customer Analytics")
    st.markdown("Customer segmentation, behavior, and retention analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Customer segmentation
        try:
            customer_analysis = utils.load_data("SELECT cm.*, c.customer_segment FROM customer_metrics cm JOIN customers c ON cm.customer_id = c.customer_id")
            st.plotly_chart(
                utils.create_customer_segment_chart(customer_analysis),
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error loading customer analysis: {e}")
    
    with col2:
        # Customer retention
        try:
            retention_data = utils.load_data("SELECT customer_id, last_order, customer_lifetime_days FROM customer_metrics ORDER BY last_order DESC LIMIT 12")
            retention_data['customer_id'] = retention_data['customer_id'].astype(str)
            fig = px.bar(
                retention_data,
                x='customer_id',
                y='customer_lifetime_days',
                title='Customer Lifetime (in Days) for 12 Most Recent Customers',
                labels={'customer_lifetime_days': 'Customer Since (in Days)', 'customer_id': 'Customer ID'}
            )

            fig.update_xaxes(type='category')
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading retention data: {e}")
    
    # Customer metrics table
    st.subheader("📊 Customer Segment Details")
    try:
        st.dataframe(
            customer_analysis,
            use_container_width=True
        )
    except:
        st.info("Customer analysis data not available")

elif page == "📦 Products":
    st.title("📦 Product Performance")
    st.markdown("Product sales, category analysis, and inventory insights")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Category performance
        try:
            category_data = utils.load_data("""
                SELECT 
                    p.product_name,
                    p.category,
                    p.subcategory,
                    pm.total_quantity_sold,
                    pm.total_revenue,
                    pm.unique_orders,
                    pm.product_id
                FROM product_metrics pm
                JOIN products p ON pm.product_id = p.product_id
            """)

            st.plotly_chart(
                utils.create_category_chart(category_data),
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error loading category data: {e}")
    
    with col2:
        # Top products
        try:
            query = """
                SELECT 
                    p.product_name,
                    pm.total_quantity_sold,
                    pm.total_revenue
                FROM product_metrics pm
                JOIN products p ON pm.product_id = p.product_id
                ORDER BY pm.total_revenue DESC
                LIMIT 10
            """
            top_products = utils.load_data(query)
            st.subheader("🏆 Top 10 Products")
            for _, product in top_products.iterrows():
                st.metric(
                    label=product['product_name'][:30] + "...",
                    value=f"${product['total_revenue']:,.0f}",
                    delta=f"{product['total_quantity_sold']} units"
                )
        except Exception as e:
            st.error(f"Error loading top products: {e}")
    
    # Category performance table
    st.subheader("📊 Category Performance Details")
    try:
        st.dataframe(category_data, use_container_width=True)
    except:
        st.info("Category performance data not available")

elif page == "📊 Advanced Analytics":
    st.title("📊 Advanced Analytics")
    st.markdown("Growth trends, forecasting, and business intelligence")
    
    # Monthly growth analysis
    try:
        growth_data = utils.load_data("SELECT * FROM monthly_summary ORDER BY order_month DESC LIMIT 12")
        st.plotly_chart(
            utils.create_growth_chart(growth_data),
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Error loading growth data: {e}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Revenue Forecast")
        try:
            # Simple linear forecast (demonstration)
            recent_revenue = utils.load_data("""
                SELECT summary_date, total_revenue 
                FROM sales_summary 
                ORDER BY summary_date DESC 
                LIMIT 30
            """)
            
            if len(recent_revenue) > 0:
                # Calculate trend
                recent_revenue['days'] = range(len(recent_revenue))
                trend = np.polyfit(recent_revenue['days'], recent_revenue['total_revenue'], 1)
                
                # Create forecast
                future_days = range(len(recent_revenue), len(recent_revenue) + 7)
                forecast = [trend * day + trend for day in future_days]
                
                st.write(f"📊 **Average Daily Revenue**: ${recent_revenue['total_revenue'].mean():,.2f}")
                st.write(f"📈 **Trend**: ${trend:+.2f} per day")
                st.write(f"🔮 **7-Day Forecast**: ${sum(forecast):,.2f}")
            
        except Exception as e:
            st.error(f"Forecast calculation error: {e}")
    
    with col2:
        st.subheader("🎯 Key Insights")
        try:
            # Business insights
            insights_query = """
            SELECT 
                (SELECT COUNT(*) FROM customers WHERE customer_segment = 'Premium') as premium_customers,
                (SELECT AVG(profit_margin) FROM products) as avg_profit_margin,
                (SELECT category FROM product_metrics ORDER BY total_revenue DESC LIMIT 1) as top_category
            """
            insights = utils.load_data(insights_query)
            
            if len(insights) > 0:
                insight = insights.iloc
                st.write(f"👑 **Premium Customers**: {insight['premium_customers']:,}")
                st.write(f"💰 **Avg Profit Margin**: {insight['avg_profit_margin']:.1f}%")
                st.write(f"🏆 **Top Category**: {insight['top_category']}")
            
        except Exception as e:
            st.error(f"Insights calculation error: {e}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>📊 E-commerce Analytics Dashboard | Built with Streamlit & PostgreSQL</p>
    </div>
    """,
    unsafe_allow_html=True
)
