import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(layout="wide")
st.title('Pizza Sales Interactive Dashboard')

# Load the dataset
df = pd.read_csv('/content/pizza_sales.csv')

# Convert 'order_date' to datetime, handling mixed formats
df['order_date'] = pd.to_datetime(df['order_date'], format='mixed')
# Convert 'order_time' to time objects
df['order_time'] = pd.to_datetime(df['order_time'], format='%H:%M:%S').dt.time

# Extract month and day of week
df['month'] = df['order_date'].dt.month_name()
df['day_of_week'] = df['order_date'].dt.day_name()

st.write("### Raw Data Sample")
st.dataframe(df.head())

st.write("### Data after Preprocessing")
st.dataframe(df.head())

st.sidebar.header('Filter Options')

# Pizza Category Filter
pizza_categories = df['pizza_category'].unique()
selected_categories = st.sidebar.multiselect(
    'Select Pizza Category',
    pizza_categories,
    default=pizza_categories
)

# Pizza Size Filter
pizza_sizes = df['pizza_size'].unique()
selected_sizes = st.sidebar.multiselect(
    'Select Pizza Size',
    pizza_sizes,
    default=pizza_sizes
)

# Filter DataFrame based on selections
filtered_df = df[
    (df['pizza_category'].isin(selected_categories)) &
    (df['pizza_size'].isin(selected_sizes))
]

st.write('### Filtered Data Sample')
st.dataframe(filtered_df.head())

st.subheader('Pizza Category Distribution')
category_counts = filtered_df['pizza_category'].value_counts().reset_index()
category_counts.columns = ['Category', 'Count']
chart_category = alt.Chart(category_counts).mark_bar().encode(
    x=alt.X('Category:N', sort='-y'),
    y='Count:Q',
    tooltip=['Category', 'Count']
).properties(title='Pizza Category Distribution')
st.altair_chart(chart_category, width='stretch')

st.subheader('Pizza Size Distribution')
size_counts = filtered_df['pizza_size'].value_counts().reset_index()
size_counts.columns = ['Size', 'Count']
chart_size = alt.Chart(size_counts).mark_arc().encode(
    theta=alt.Theta(field='Count', type='quantitative'),
    color=alt.Color(field='Size', type='nominal', title='Pizza Size'),
    tooltip=['Size', 'Count', alt.Tooltip('Count', format='.1%')] # Show percentage in tooltip
).properties(title='Pizza Size Distribution')
st.altair_chart(chart_size, width='stretch')

# Scatter Plot Controls and Visualization
st.subheader('Scatter Plot: Total Price vs Quantity')

x_axis_options = ['quantity', 'total_price']
y_axis_options = ['total_price', 'quantity']

x_axis_col = st.sidebar.selectbox('Select X-axis for Scatter Plot', x_axis_options, index=0)
y_axis_col = st.sidebar.selectbox('Select Y-axis for Scatter Plot', y_axis_options, index=0)
color_by_col = st.sidebar.selectbox('Color points by', ['pizza_category', 'pizza_size'], index=0)

scatter_chart = alt.Chart(filtered_df).mark_circle().encode(
    x=alt.X(x_axis_col, type='quantitative'),
    y=alt.Y(y_axis_col, type='quantitative'),
    color=alt.Color(color_by_col, type='nominal'),
    tooltip=['pizza_name', 'quantity', 'total_price', 'pizza_category', 'pizza_size']
).properties(
    title=f'{y_axis_col.replace("_", " ").title()} vs {x_axis_col.replace("_", " ").title()}'
).interactive()
st.altair_chart(scatter_chart, width='stretch')

# Summary Report Button
st.write('### Data Summary Report')
if st.button('Generate Summary Report'):
    st.dataframe(filtered_df.describe())
