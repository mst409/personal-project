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
st.markdown("""
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """, unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns([0.5, 0.6],gap="medium")
    col2.header(f'נתוני {df.Name.count()} חללי צה"ל הי"ד במלחמת חרבות ברזל',anchor=False)
with st.container():
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1],gap="medium")
    st.image('לכידה-3.png', use_container_width=True)

with st.container():
    col1, col2 = st.columns([0.7, 0.3], gap="medium")

    with col1:
        rank_data = df.Rank.value_counts()
        st.bar_chart(rank_data, horizontal=True)
    with col2:
        st.markdown("## דרגות הנופלים")
        st.text("בגרף זה ניתן לראות את כמות הנופלים לפי דרגה")
    st.divider()
with st.container():
    col1, col2 = st.columns([0.4, 0.6], gap="medium")
    with col1:
        st.markdown("## גילאי הנופלים")
        st.text(f""".בגרף זה ניתן לראות את כמות הנופלים לפי גיל
                ,ממוצע הגילאים הינו {df.Age_fallen.mean():.1f}
                עם סטיית תקן של {df.Age_fallen.std():.1f} חודשים""")
    with col2:
        age_data = df.Age_fallen.value_counts()
        age_data.columns = ['גיל', 'נופלים']
        st.bar_chart(data=age_data)
    st.divider()

with st.container():
    col1, col2, col3 = st.columns([0.3, 0.1, 0.4], gap="medium")
    with col1:
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
    with col3:
        st.markdown("## נופלים סדירים ומילואים")
        st.text("בגרף זה ניתן לראות את כמות הנופלים לפי סוג שירות")
    st.divider()

with st.container():
    col1, col2 = st.columns([0.3, 0.7], gap="medium")
    with col1:
        st.markdown("### כמות נפילות לפי יום")
        st.text('''.בגרף זה ניתן לראות את כמות הנופלים לפי יום
                בבחירת האפשרות 'הצג נופלים' ניתן לראות את כל הנופלים בתאריך נבחר''')
    with col2:
        tab1, tab2 = st.tabs(["לוח שנה", "הצג נופלים"])
        date_data = df.Date_fallen.value_counts().reset_index()
        date_data.columns = ['Date_fallen', 'Count'] 
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

with st.container():
    col1, col2 = st.columns([0.65, 0.35], gap="medium")
    with col2:
        st.markdown("### כמות הנופלים לפי עיר")
        st.text('''.בגרף זה ניתן לראות את כמות הנופלים לפי עיר
                בבחירת האפשרות 'הצג נופלים' ניתן לראות את כל הנופלים בעיר נבחרת''')
    with col1:
        tab1, tab2 = st.tabs(["מפה", "הצג נופלים"])
        with tab1:
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
        with tab2:
            txt_box, _ = st.columns([10, 35])
            pick_city = txt_box.selectbox("בחר עיר", df.City.sort_values().unique())
            city_data = df.loc[df.City == pick_city, ['Name','Rank', 'Age_fallen']]
            city_data.columns = ['שם', 'דרגה', 'גיל']
            st.dataframe(city_data, hide_index=True, width=500)
    st.divider()