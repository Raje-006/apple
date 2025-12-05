import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title('Amazon Product Analysis Dashboard')

# Load Data
df = pd.read_csv('amazon.csv')

# Data Cleaning and Preprocessing (moved from previous cells to be self-contained in app.py)
df['discounted_price'] = df['discounted_price'].str.replace('₹', '').str.replace(',', '').astype(float)
df['actual_price'] = df['actual_price'].str.replace('₹', '').str.replace(',', '').astype(float)
df['discount_percentage'] = df['discount_percentage'].str.replace('%', '').astype(float)

# Convert 'rating' to numeric, coercing errors to NaN
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# Convert 'rating_count' to numeric, handling commas and then converting to integer, coercing errors to NaN
df['rating_count'] = df['rating_count'].str.replace(',', '', regex=False).astype(float)
df['rating_count'] = df['rating_count'].fillna(0).astype(int)

# Extract main category
df['category'] = df['category'].astype(str)
df['main_category'] = df['category'].apply(lambda x: x.split('|')[0] if pd.notnull(x) and x != 'nan' else 'Unknown')

# Display the first few rows of the DataFrame
st.write("### Data Preview")
st.dataframe(df.head())

st.sidebar.header('Visualization Settings')

# Scatter Plot
st.subheader('Scatter Plot: Discounted Price vs. Rating')

# Select numerical columns for scatter plot
numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
x_axis = st.sidebar.selectbox('Select X-axis for Scatter Plot', numerical_cols, index=numerical_cols.index('discounted_price'))
y_axis = st.sidebar.selectbox('Select Y-axis for Scatter Plot', numerical_cols, index=numerical_cols.index('rating'))

if x_axis and y_axis:
    scatter_fig = px.scatter(df, x=x_axis, y=y_axis, title=f'{y_axis} vs. {x_axis}', hover_data=['product_name', 'category'])
    st.plotly_chart(scatter_fig, width='stretch') # Changed use_container_width to width='stretch'

# Count Plot
st.subheader('Count Plot: Product Category Distribution')
# Ensure 'category' column exists and handle potential non-string types if any remained after initial load
if 'category' in df.columns:
    # Use the first part of the category for better visualization if applicable
    # No need for category_options and selected_category_col here if we are directly plotting 'main_category'
    # The previous error was also due to the selectbox for 'category_col' returning a list ['category'] instead of a string 'category'
    # Correcting this logic and using the derived 'main_category' directly for the plot.

    count_fig = px.histogram(df, x='main_category', title='Product Category Distribution', color='main_category')
    st.plotly_chart(count_fig, width='stretch')
else:
    st.write("Category column not found in DataFrame.")

# Pie Chart
st.subheader('Pie Chart: Distribution by Main Category')
# For a pie chart, we want to show the proportion of items in each category
pie_chart_col = st.sidebar.selectbox('Select Column for Pie Chart', ['main_category']) # Offer 'main_category' as an option

if pie_chart_col:
    # Calculate value counts for the selected column
    pie_data = df[pie_chart_col].value_counts().reset_index()
    pie_data.columns = [pie_chart_col, 'count']
    pie_fig = px.pie(pie_data, values='count', names=pie_chart_col, title=f'Distribution by {pie_chart_col}', hole=0.3)
    st.plotly_chart(pie_fig, width='stretch')

# Summary Report
st.subheader('Summary Report')
if st.button('Generate Summary Report'):
    st.write("#### Descriptive Statistics")
    st.dataframe(df.describe(include='all'))

    st.write("#### Top 10 Product Categories")
    if 'main_category' in df.columns:
        st.write(df['main_category'].value_counts().head(10))
    else:
        st.write("Main category column not available for summary.")

    st.write(f"#### Average Rating and Discount Percentage")
    avg_rating = df['rating'].mean()
    avg_discount = df['discount_percentage'].mean()
    st.write(f"Average Product Rating: {avg_rating:.2f}")
    st.write(f"Average Discount Percentage: {avg_discount:.2f}%")
