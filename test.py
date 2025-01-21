import pandas as pd
import streamlit as st
import plotly.express as px 
from plotly_calplot import calplot

df = pd.read_csv('soldiers_info_detaild.csv')

st.set_page_config(
    page_title="נתוני נופלים חרבות ברזל",
    page_icon="yizkor-22.jpg",
    layout="wide",
    )
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

st.title("נתוני נופלים חרבות ברזל")

col1, col2 = st.columns([0.4, 0.6],gap="medium")

with col1:
    rank_data = df.Rank.value_counts()
    st.markdown("### דרגות הנופלים")
    st.bar_chart(rank_data, horizontal=True)
    st.divider()


    st.markdown("### גילאי הנופלים")
    col3, col4 = st.columns(2,gap="small")
    with col3:
        st.markdown(f"ממוצע גילאים **{df.Age_fallen.mean():.1f}**")
    with col4:
        st.markdown(f"סטיית תקן  **{df.Age_fallen.std():.1f}**")
    age_data = df.Age_fallen.value_counts()
    st.bar_chart(age_data)
    st.divider()


    st.markdown("### נופלים סדירים ומילואים")
    miluim_data = df.Miluim.value_counts()
    miluim_data.index = ["סדיר", "מילואים"]
    miluim_data = miluim_data.reset_index()
    miluim_data.columns = ['index', 'count']
    miluim_chart = px.pie(
        miluim_data, 
        values='count', 
        names='index',
        hover_name='index',
        hover_data={'index': False},
        labels={'count': 'נופלים', 'index': 'שירות'},
        )
    st.plotly_chart(miluim_chart)


with col2:
    date_data = df.Date_fallen.value_counts().reset_index()
    date_data.columns = ['Date_fallen', 'Count'] 
    st.markdown("### כמות נפילות לפי יום")
    tab1, tab2 = st.tabs(["לוח שנה", "הצג נופלים"])
    with tab1:
        dates = calplot(
                    date_data,
                    x='Date_fallen',
                    y='Count',
                    name='נופלים',
                    colorscale=[[0, 'lightblue'], [0.5, 'blue'], [1, 'blue']],
                    space_between_plots=0.1,
                    )
        st.plotly_chart(dates)
    with tab2:
        dt, _ = st.columns([6, 35])
        chosen_date = dt.date_input(
            "בחר תאריך", 
            label_visibility="visible",
            min_value=df.Date_fallen.min(), 
            max_value=df.Date_fallen.max(), 
            format="DD/MM/YYYY",
            key="date"
            )
        
        chosen_date = pd.to_datetime(chosen_date).date()
        df['Date_fallen'] = pd.to_datetime(df['Date_fallen']).dt.date
        date_df = df.loc[df.Date_fallen == chosen_date, ['Name','Rank', 'Age_fallen']]
        date_df.columns = ['שם', 'דרגה', 'גיל']
        if date_df.empty == False:
            st.dataframe(date_df, hide_index=True, width=500)
        else:
            st.write("### לשמחתנו אין נופלים בתאריך זה")
    st.divider()

    st.markdown("### כמות הנופלים לפי עיר")
    tab3, tab4 = st.tabs(["מפה", "הצג נופלים"])

    with tab3:
        city_df = df.groupby(['City', 'lat', 'lon']).size().reset_index(name='Count')
        fig = px.scatter_mapbox(
            city_df, 
            lat="lat", 
            lon="lon", 
            color="Count", 
            size="Count", 
            hover_name="City",
            hover_data={"lat": False, "lon": False, "City": False},
            zoom=7.1, 
            height=900,
            width=200,
            mapbox_style="carto-positron",
            size_max=25,
            center={"lat": 31.3999, "lon": 34.7818},
            color_continuous_scale=[[0, 'lightblue'], [0.5, 'blue'], [1, 'blue']]
            )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)
    with tab4:
        txt_box, _ = st.columns([10, 35])
        pick_city = txt_box.selectbox("בחר עיר", df.City.sort_values().unique())
        city_data = df.loc[df.City == pick_city, ['Name','Rank', 'Age_fallen']]
        city_data.columns = ['שם', 'דרגה', 'גיל']
        st.dataframe(city_data, hide_index=True, width=500)
