import streamlit as st
import pandas as pd
import plotly.express as px
from millify import millify
from streamlit_extras.colored_header import colored_header

st.set_page_config(
    page_title="BTFN Winners",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": "https://twitter.com/MercyArems",
        "About": None
    }
)

text_1 = '<p style="font-family:sans-serif; color:#4d372c; font-size: 20px;">In a world where crypto headlines and sensational claims seem to pop up as often as cat memes, it\'s essential to separate fact from fiction. <a href="https://twitter.com/nic__carter">Nic Carter</a> recognized this and initiated the <a href="https://x.com/nic__carter/status/1717622001014067417?s=20">Break The Fake News Bounty</a> – a $500 BTC reward for intrepid analysts willing to dissect the <a href="https://niccarter.info/wp-content/uploads/Hamas-Militants-Behind-Israel-Attack-Raised-Millions-in-Crypto-WSJ.pdf">WSJ\'s claims</a> and <a href="https://www.warren.senate.gov/imo/media/doc/2023.10.17 Letter%20to%20Treasury%20and%20White%20House%20re%20Hamas%20crypto%20security.pdf">Senator Elizabeth Warren\'s letter</a>, challenging the very fabric of crypto narrative.</p>'

text_2 = '<p style="font-family:sans-serif; color:#4d372c; font-size: 20px;">The winners embarked on a quest, delving into complex cryptocurrency data to reveal the truth concealed within the depths of the blockchain. This dashboard not only unveils the numbers behind the winners and their triumphant submissions but also pays homage to the data providers who played a crucial role in this quest. The impact of their findings might just shape the future of the crypto industry and policymaking.</p>'

st.markdown(f'<h1 style="color:#434346;font-size:60px;text-align:center;">{"Break The Fake News Winners"}</h1>', unsafe_allow_html=True)
colored_header(
    label="",
    description="",
    color_name="gray-70",
)
st.markdown(text_1, unsafe_allow_html=True)
st.markdown(text_2, unsafe_allow_html=True)
colored_header(
    label="",
    description="",
    color_name="gray-70",
)

column_names = ['author_x_username', 'submission_type', 'data_provider', 'submission_url', 'prize_usd']
df = pd.read_csv("winners.csv", names=column_names)
df['data_provider'] = df['data_provider'].str.split(', ')
df.index = df.index + 1

col_1, col_2, col_3, col_4 = st.columns(4)
with col_1:
    st.metric("Winning Submissions", len(df))
with col_2:
    st.metric("Unique Winners", df['author_x_username'].nunique())
with col_3:
    st.metric("Total Amount Paid", "$" + f"{df['prize_usd'].sum()}")
with col_4:
    st.metric("Average Amount Paid", "$" + millify(f"{df['prize_usd'].mean()}", precision=2))

value_counts = df['submission_type'].value_counts().reset_index()
# Rename the columns for the pie chart
value_counts.columns = ['Submission Type', 'Count']
# Create a pie chart using Plotly Express
fig_1 = px.pie(value_counts, names='Submission Type', values='Count', title="Winning Submission Types")


# Flatten the lists and handle NaN values
df_1 = df.explode('data_provider').dropna(subset=['data_provider'])

# Count the occurrences of each data provider
data_provider_counts = df_1['data_provider'].value_counts().reset_index()
data_provider_counts.columns = ['Data Provider', 'Count']

# Create a Pie Chart using Plotly Express
fig_2 = px.pie(data_provider_counts, names='Data Provider', values='Count', title="Data Provider Distribution")


# Filter out lists with only one item and drop NaN values
filtered_df = df[df['data_provider'].apply(lambda x: isinstance(x, list) and len(x) > 1 if x is not None else False)].dropna(subset=['data_provider'])

# Count the occurrences of each data provider combination
data_provider_counts = filtered_df['data_provider'].apply(tuple).value_counts().reset_index()
data_provider_counts.columns = ['Data Provider Combination', 'Count']

# Format the label names by joining the items with commas and spaces
data_provider_counts['Data Provider Combination'] = data_provider_counts['Data Provider Combination'].apply(lambda x: ', '.join(x))

# Create a Pie Chart using Plotly Express
fig_3 = px.pie(data_provider_counts, names='Data Provider Combination', values='Count', title="Data Provider Combinations Distribution [Submissions With >1 Data Provider]")

top_authors = df.groupby("author_x_username")["prize_usd"].sum().reset_index()
top_authors = top_authors.sort_values(by="prize_usd", ascending=False)
fig_4 = px.bar(top_authors, x="author_x_username", y="prize_usd", title="Authors by Prize Earnings")
fig_4.update_xaxes(title_text="Author Username")
fig_4.update_yaxes(title_text="Total Prize Earnings (USD)")


col_a, col_b = st.columns(2)
with col_a:
    st.plotly_chart(fig_1, use_container_width=True)
with col_b:
    st.plotly_chart(fig_2, use_container_width=True)
col_a, col_b = st.columns(2)
with col_a:
    st.plotly_chart(fig_3, use_container_width=True)
with col_b:
    st.plotly_chart(fig_4, use_container_width=True)

st.subheader("Winning Submissions")
st.dataframe(df, use_container_width=True)

st.download_button(
    label="Download data as CSV",
    data=df.to_csv().encode('utf-8'),
    file_name='winners.csv',
    mime='text/csv',
)
