import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the Streamlit page configuration
st.set_page_config(
    layout='wide',
    page_title='Dashboard',
    page_icon='📊'
)

# Load your dataset
df = pd.read_csv("D:/data sicece 2/39/assignement/df.csv")

# Check and drop the 'Unnamed: 0' column if it exists
if 'Unnamed: 0' in df.columns:
    df.drop('Unnamed: 0', axis=1, inplace=True)

# Print column names for debugging
st.write("Columns in DataFrame:", df.columns)

# Convert date columns to datetime
df['order_date'] = pd.to_datetime(df['order_date'])
df['delivery_date'] = pd.to_datetime(df['delivery_date'])

# Descriptive statistics
num = df.describe()  # Numerical statistics
cat = df.describe(include='object')  # Categorical statistics

# Create tabs for the application
tab1, tab2 = st.tabs(['📈 Descriptive Stats', '📊 Charts'])

# Tab 1: Descriptive Statistics
with tab1:
    col1, col2, col3 = st.columns([6, 0.5, 6])
    
    with col1:
        st.subheader('Numerical Descriptive Statistics')
        st.dataframe(num.T, 700, 150)  # Transpose for better readability

    with col3:
        st.subheader('Categorical Descriptive Statistics')
        st.dataframe(cat.T, 700, 150)  # Transpose for better readability

# Tab 2: Charts
with tab2:
    st.subheader('Charts')

    # Sidebar selections
    product_name = st.sidebar.selectbox("Select Product Name", df['product_name'].unique())
    delivery_date = st.sidebar.selectbox('Select Delivery Date', df['delivery_date'].unique())
    price = st.sidebar.radio('Select Price', sorted(df['price'].unique()), index=0, horizontal=True)

    # Scatter plot for delivery date vs product name
    fig4 = px.scatter(df, x='delivery_date', y='product_name', title='Delivery Date vs Product Name')
    st.plotly_chart(fig4)

    # Bar chart for total price by product name
    fig5 = px.bar(df, x='product_name', y='total_price', color_discrete_sequence=px.colors.qualitative.Pastel, title='Total Price by Product Name')
    st.plotly_chart(fig5)

    # Bar chart for price per unit by product name
    fig6 = px.bar(df, x='product_name', y='price_per_unit', title='Price Per Unit by Product Name')
    st.plotly_chart(fig6)

    # Sales Over Time (Bar Chart)
    sales_over_time = px.bar(
        df.groupby('order_date')['total_price'].sum().reset_index(),
        x='order_date', y='total_price',
        title='Total Sales Over Time',
        labels={'order_date': 'Order Date', 'total_price': 'Total Sales ($)'},
        template='plotly'
    )
    st.plotly_chart(sales_over_time)

    # Top Product Categories (Pie Chart)
    top_categories = px.pie(
        df.groupby('product_type')['total_price'].sum().reset_index(),
        values='total_price', names='product_type',
        title='Sales by Product Category',
        labels={'product_type': 'Product Category', 'total_price': 'Total Sales ($)'},
        template='plotly'
    )
    st.plotly_chart(top_categories)

    # Customer Age Distribution (Histogram)
    age_distribution = px.histogram(
        df, x='age',
        title='Customer Age Distribution',
        labels={'age': 'Age', 'count': 'Number of Customers'},
        template='plotly'
    )
    st.plotly_chart(age_distribution)
