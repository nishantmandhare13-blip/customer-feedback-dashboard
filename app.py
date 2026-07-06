
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Customer Feedback Dashboard",layout="wide")
st.markdown("""
<style>
.stApp{background:#0f172a;color:white}
div[data-testid="metric-container"]{background:#1e293b;padding:15px;border-radius:12px}
</style>
""",unsafe_allow_html=True)

sample=Path("sample_feedback.csv")
if sample.exists():
    df=pd.read_csv(sample,parse_dates=["Date"])
else:
    df=pd.DataFrame()

up=st.sidebar.file_uploader("Upload CSV",type="csv")
if up is not None:
    df=pd.read_csv(up,parse_dates=["Date"])

st.title("📊 Customer Feedback Analysis Dashboard")
if df.empty:
    st.warning("No data.")
    st.stop()

regions=st.sidebar.multiselect("Region",sorted(df.Region.unique()),default=list(df.Region.unique()))
df=df[df.Region.isin(regions)]
c1,c2,c3=st.columns(3)
c1.metric("Feedback",len(df))
c2.metric("Avg Rating",round(df.Rating.mean(),2))
c3.metric("Positive %",round((df.Sentiment=="Positive").mean()*100,1))

col1,col2=st.columns(2)
with col1:
    fig=px.histogram(df,x="Rating",color="Rating",template="plotly_dark")
    st.plotly_chart(fig,use_container_width=True)
with col2:
    fig=px.pie(df,names="Sentiment",template="plotly_dark",hole=.5)
    st.plotly_chart(fig,use_container_width=True)

df["Month"]=df["Date"].dt.to_period("M").astype(str)
trend=df.groupby("Month").size().reset_index(name="Count")
fig=px.line(trend,x="Month",y="Count",markers=True,template="plotly_dark")
st.plotly_chart(fig,use_container_width=True)
st.dataframe(df,use_container_width=True)
