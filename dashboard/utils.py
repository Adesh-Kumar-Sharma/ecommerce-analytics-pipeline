import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from config.database import db_manager

class DashboardUtils:
    def __init__(self):
        self.db = db_manager
    
    @st.cache_data
    def load_data(_self, query):
        """Load data with caching"""
        return _self.db.execute_query(query)
    
    def create_metric_cards(self, col1, col2, col3, col4, metrics):
        """Create metric cards"""
        with col1:
            st.metric(
                label="Total Revenue",
                value=f"${metrics['total_revenue']:,.2f}",
                delta=f"{metrics.get('revenue_change', 0):.1f}%"
            )
        
        with col2:
            st.metric(
                label="Total Orders",
                value=f"{metrics['total_orders']:,}",
                delta=f"{metrics.get('orders_change', 0):.1f}%"
            )
        
        with col3:
            st.metric(
                label="Total Customers",
                value=f"{metrics['total_customers']:,}",
                delta=f"{metrics.get('customers_change', 0):.1f}%"
            )
        
        with col4:
            st.metric(
                label="Avg Order Value",
                value=f"${metrics['avg_order_value']:.2f}",
                delta=f"{metrics.get('aov_change', 0):.1f}%"
            )
    
    def create_revenue_chart(self, df):
        """Create revenue trend chart"""
        fig = px.line(
            df, 
            x='summary_date', 
            y='total_revenue',
            title='Daily Revenue Trend',
            labels={'total_revenue': 'Revenue ($)', 'summary_date': 'Date'}
        )
        fig.update_traces(line_color='#1f77b4', line_width=3)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        return fig
    
    def create_category_chart(self, df):
        """Create category performance chart"""
        fig = px.treemap(
            df,
            path=['category', 'subcategory'],
            values='total_revenue',
            title='Revenue by Category and Subcategory'
        )
        return fig
    
    def create_customer_segment_chart(self, df):
        """Create customer segment analysis chart"""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Customers by Segment', 'Revenue by Segment'),
            specs=[[{"type": "pie"}, {"type": "pie"}]]
        )
        
        # Customers pie chart
        fig.add_trace(
            go.Pie(
                labels=df['customer_segment'],
                values=df['order_count'],
                name="Customers"
            ),
            row=1, col=1
        )
        
        # Revenue pie chart
        fig.add_trace(
            go.Pie(
                labels=df['customer_segment'],
                values=df['total_spent'],
                name="Revenue"
            ),
            row=1, col=2
        )
        
        fig.update_layout(title_text="Customer Segment Analysis")
        return fig
    
    def create_growth_chart(self, df):
        """Create monthly growth chart"""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Monthly Revenue', 'Growth Rate %'),
            vertical_spacing=0.12
        )
        
        # Revenue bars
        fig.add_trace(
            go.Bar(
                x=df['month'],
                y=df['revenue'],
                name='Revenue',
                marker_color='lightblue'
            ),
            row=1, col=1
        )
        
        # Growth rate line
        fig.add_trace(
            go.Scatter(
                x=df['month'],
                y=df['revenue_growth_pct'],
                mode='lines+markers',
                name='Revenue Growth %',
                line=dict(color='red', width=3),
                marker=dict(size=8)
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title_text="Monthly Performance and Growth",
            showlegend=False
        )
        return fig

utils = DashboardUtils()
