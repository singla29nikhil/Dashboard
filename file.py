# importing libraries
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import json
import requests
from streamlit_lottie import st_lottie 

# Setting Page title
st.set_page_config(page_title="Car Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# Reading csv file
# URL:https://www.kaggle.com/rustydigg918/exploratory-data-analysis-on-car-sales-data/data
df=pd.read_csv('cars.csv')

# Creating sidebar
st.sidebar.header("Please Filter Here:")

# Creating select bar for vehice type
vtype = st.sidebar.multiselect(
    "Select the Vehicle Type:",
    options=df["Vehicle_type"].unique(),
    default=df["Vehicle_type"].unique(),
)

# Creating select bar for Car Manufacturers whose info we want to show 
man = st.sidebar.multiselect(
    "Select the Car Manufacturer:",
    options=df["Manufacturer"].unique(),
    default=["BMW","Porsche","Audi","Chevrolet","Dodge","Infiniti","Jeep","Cadillac","Mitsubishi","Hyundai"],
    
    
)

#selecting only selected records from dataframe
df_s= df.query(
    "Manufacturer == @man & Vehicle_type ==@vtype"
)
# To show the heading of main page
st.title(":bar_chart:CAR SALES ANALYSIS")
st.markdown("##")

# To show the animation on the dashboard
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_hello = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_rddfnr10.json")
st.markdown("""---""")
st_lottie(
    lottie_hello,
    height=600,
    width=700,
    key=None,
)
st.markdown("""---""")

# To show the total sales and average car price 
sales = int(df["Sales_in_thousands"].sum())
avg = round(df["Price_in_thousands"].mean(), 2)

left_column, middle_column = st.columns(2)
with left_column:
    st.subheader("Total Sales: ")
    st.subheader(sales*1000)
with middle_column:
    st.subheader("Average Car Price:")
    st.subheader(f"${avg*1000:,}")
st.markdown("""---""")

# Grouping data by Manufacturers and getting total sales
t=(
       df_s.groupby(by=["Manufacturer"]).sum()[["Sales_in_thousands"]].sort_values(by="Sales_in_thousands")
)

# Creating bar chart
fig_product_sales = px.bar(
    t,
    x="Sales_in_thousands",
    y=t.index,
    orientation="h",
    labels={"Sales_in_thousands":"Sales(in thousands)"},
    title="<b>Total Car Sales Of Varous Manufacturers </b>",
    color_discrete_sequence=["#0083B8"] * len(t),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor= "rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# Grouping data according to Manufacturers and getting average car price
t=(
       df_s.groupby(by=["Manufacturer"]).mean()[["Price_in_thousands"]].sort_values(by="Price_in_thousands")
)
# Creating Bar Chart
t_product_sales = px.bar(
    t,
    x="Price_in_thousands",
    y=t.index,
    orientation="h",
    labels={"Price_in_thousands":"Price(in thousands)"},
    title="<b>Average Car Prices Of Various Manufacturers</b>",
    color_discrete_sequence=["#0083B8"] * len(t),
    template="plotly_white",
)
t_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales, use_container_width=True)
right_column.plotly_chart(t_product_sales, use_container_width=True)

# For Getting average resale value for various Manufacturers
t=(
       df_s.groupby(by=["Manufacturer"]).mean()[["__year_resale_value"]].sort_values(by="__year_resale_value")
)

# Creating bar chart
r= px.bar(
    t,
    x="__year_resale_value",
    y=t.index,
    orientation="h",
    labels={"__year_resale_value":"Year_Resale_Value(in thousands)"},
    title="<b>Average Car Resale Values</b>",
    color_discrete_sequence=["#0083B8"] * len(t),
    template="plotly_white",
)
r.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# For getting total number of Car models for various Manufacturers
t=(
    df_s.groupby(by=["Manufacturer"]).size()
)
# Creating line chart
fig = px.line(
    t,
    labels={"Price_in_thousands":"Price(in thousands)","value":"Number Of Models"},
    markers=True,
    text="value",
    title="<b>Number Of Car Models Of Various Manufacturers</b>",
    )
# To show no. of car models on line chart
fig.update_traces(textposition="bottom right")
fig.update_layout(
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False))
)
left_column, right_column = st.columns(2)
left_column.plotly_chart(r, use_container_width=True)
right_column.plotly_chart(fig, use_container_width=True)
st.markdown("""---""")

# Creating scatter plot showing relationship between Price and Resale value of cars
k=px.scatter(df,
x=['__year_resale_value'],
y="Price_in_thousands",
orientation="v",
color_discrete_sequence=['blue'],
labels={"Price_in_thousands":"Price(in thousands)","value":"Resale Value(in thousands)"},
title="<b>Price vs Resale Value<b>")
k.update_layout(
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False))
    
)
# Creating scatter plot showing relationship between Price and HorsePower of cars
b=px.scatter(df,
x=['Horsepower'],
y="Price_in_thousands",
color_discrete_sequence=['blue'],
labels={"Price_in_thousands":"Price(in thousands)","value":"Horsepower"},
title="<b>Price vs Horsepower<b>")
b.update_layout(
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False))
    
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(k, use_container_width=True)
right_column.plotly_chart(b, use_container_width=True)
