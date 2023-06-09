import streamlit as st
import pandas as pd
import plotly.express as px
import random
import requests

from numerize.numerize import numerize
from utils import data_path,summary_config,PERMISSION_URLS,assign_role,check_access,Role
 
def choose_permission_urls(urls):
    return random.choice(urls)

 
def get_permission(urls):
    url = choose_permission_urls(urls)
    resp = requests.get(url)
    if resp and resp.status_code == 200:
        permission = resp.json()
        st.session_state.role = assign_role(permission["role"])
        st.session_state.dashboard_permissions = permission["dashboard_permissions"]
    else:
        st.session_state.role = assign_role("default")
        st.session_state.dashboard_permissions = None

@st.cache_data
def load_data(data_path=data_path):
    df = pd.read_csv(data_path)
    return df


def display_title(title_mid):
    with title_mid:
        st.title(f"Facebook Campaign Dashboard - {st.session_state['role'].name}")


def display_sidebar(df):
    with st.sidebar:
        Campaign_filter = st.multiselect(
            label="Select The Campaign",
            options=df["campaign"].unique(),
            default=df["campaign"].unique(),
        )

        Age_filter = st.multiselect(
            label="Select Age Group",
            options=df["age"].unique(),
            default=df["age"].unique(),
        )

        Gender_filter = st.multiselect(
            label="Select Gender Group",
            options=df["gender"].unique(),
            default=df["gender"].unique(),
        )
    return Campaign_filter, Age_filter, Gender_filter

def display_click_rate(st_container,df):
    with st_container:
        df3 = df.groupby(by = ['campaign']).sum()[['Impressions','Clicks']].reset_index()
        df3['CTR'] =round(df3['Clicks']/df3['Impressions'] *100,3)
        fig_CTR_by_campaign = px.bar(df3,
                                x='campaign',
                                y='CTR',
                                title='<b>Click Through Rate</b>')
        fig_CTR_by_campaign.update_layout(title = {'x' : 0.5},
                                        plot_bgcolor = "rgba(0,0,0,0)",
                                        xaxis =(dict(showgrid = False)),
                                        yaxis =(dict(showgrid = False)))
        st.plotly_chart(fig_CTR_by_campaign,use_container_width=True)

def display_daily_impressions(st_container,df):
    with st_container:
        fig_impressions_per_day = px.line(df,x='date',
                                        y=['Impressions'],
                                        color='campaign',
                                        title='<b>Daily Impressions By Campaign</b>')
        fig_impressions_per_day.update_xaxes(rangeslider_visible=True)
        fig_impressions_per_day.update_layout(xaxis_range=['2021-01-01','2021-01-31'],
                                            showlegend = False,
                                            title = {'x' : 0.5},
                                            plot_bgcolor = "rgba(0,0,0,0)",
                                            xaxis =(dict(showgrid = False)),
                                            yaxis =(dict(showgrid = False)),)
        st.plotly_chart(fig_impressions_per_day,use_container_width=True)

@check_access(Role.ADMIN)
def display_ads_by_gender(st_container,df):
    with st_container:
        df4 = df.groupby(by='gender').sum()[['Spent']].reset_index()
        fig_spend_by_gender = px.pie(df4,names='gender',values='Spent',title='<b>Ad Spend By Gender</b>')
        fig_spend_by_gender.update_layout(title = {'x':0.5}, plot_bgcolor = "rgba(0,0,0,0)")
        st.plotly_chart(fig_spend_by_gender,use_container_width=True)

@check_access(Role.ADMIN)
def display_age_demographics(st_container,df):
    with st_container:
        df5 = df.groupby(by='age').sum()[['Spent','Total_Conversion']].reset_index()
        df5['CPC'] = round(df5['Spent']/df5['Total_Conversion'],2)
        fig_CPC_by_age = px.bar(df5,x = 'age',y='CPC',title='<b>Cost Per Conversion By Age Demographic</b>')
        fig_CPC_by_age.update_layout(title = {'x':0.5},xaxis =(dict(showgrid = False)),yaxis =(dict(showgrid = False)), plot_bgcolor = "rgba(0,0,0,0)")
        st.plotly_chart(fig_CPC_by_age,use_container_width=True)  


def get_summary(df, col):
    return numerize(float(df[col].sum()))


def init_session():
    if "role" not in st.session_state:
        st.session_state['role'] = None

    if "dashboard_permissions" not in st.session_state:
        st.session_state['dashboard_permissions'] = None
      
def main(df):
    header_left, title_mid, header_right = st.columns([1, 2, 1], gap="large")
    display_title(title_mid)
    Campaign_filter, Age_filter, Gender_filter = display_sidebar(df)
    filtered_df = df.query(
        "campaign == @Campaign_filter & age == @Age_filter & gender == @Gender_filter"
    )
  
    all_columns = st.columns(len(summary_config), gap="large")
    for i, config_key in enumerate(summary_config):
        with all_columns[i]:
            st.image(summary_config[config_key]['image'], use_column_width="Auto")
            st.metric(
                label=summary_config[config_key]['label'], value=get_summary(filtered_df, config_key)
            )

    Q1_container,Q2_container = st.columns(2)
    Q3_container,Q4_container = st.columns(2)
    
    display_click_rate(Q1_container,filtered_df)
    display_daily_impressions(Q2_container,filtered_df)
    
    display_ads_by_gender(Q3_container,filtered_df)

    display_age_demographics(Q4_container,filtered_df)
    
if __name__ == "__main__":
    st.set_page_config(
        page_title="Facebook Ad Campaign Dashboard",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    df = load_data()
    init_session()
    get_permission(PERMISSION_URLS)
    main(df)
