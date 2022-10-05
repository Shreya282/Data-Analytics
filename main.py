import pandas as pd
import plotly.express as px
import streamlit as st
import math
from PIL import Image
import numpy as np

showWarningOnDirectExecution = False

# ------------------------------------------ BASICS ---------------------------------------
st.set_page_config(page_title="Food Hub", page_icon=":bar_chart:", layout="wide")
heading = '<p style="font-family:sans-serif; font-size: 50px; text-align: center; color: #33322d;">FOOD HUB</p>'
st.markdown(heading, unsafe_allow_html=True)
def main():
    page_bg_img = '''
            <style>
            body {
            background-image: url("https://us.123rf.com/450wm/phordi/phordi1808/phordi180800248/105834874-lights-on-gray-background.jpg?ver=6");
            background-repeat: no-repeat;
            background-size: 1600px 720px;
            }
            </style>
            '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# ------------------------------------------ READ EXCEL ---------------------------------------
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io='zomato_1.xlsx',
        engine='openpyxl',
        sheet_name='zomato (1)',
        skiprows=0,
        usecols="B:N",
        nrows=51718,
    )
    return df

df = get_data_from_excel()
# st.dataframe(df.head(5))

# ------------------------------------------ CONTENT ---------------------------------------
content = '<p style="font-family:sans-serif; font-size: 18px; text-align: left">Food hub is an organization that offers access to multiple restaurants through a single website. It is a centrally located facility with a business management structure facilitating the aggregation, storage, processing, distribution, and/or marketing of local/regional restaurants. Community food hubs expand market access for small to medium-sized restaurants and enhance producer viability and capacity.  The basic idea is to analyse the Zomato dataset to get a fair idea about the factors affecting the establishment of different types of restaurants at different places in Bengaluru, aggregate rating of each restaurant, Bengaluru being one such city has more than 12,000 restaurants with restaurants serving dishes from all over the world. The aim is to analyze the data to get a fair idea about the demand of different restaurants and analyse demography of the location as it will help new restaurants in deciding their theme, menus, cuisine, cost etc for a particular location. We also aim to find similarities between neighbourhood restaurants of Bengaluru on the basis of food.</p>'
st.markdown(content, unsafe_allow_html=True)
image = Image.open('img.png')
st.image(image, caption='Restaurants in Bangalore',width=600)

# ------------------------------------------ SIDEBAR ---------------------------------------
st.sidebar.header("Apply Filters:")

names = st.sidebar.multiselect(
    "Select the Restaurant name:",
    options=df["restaurants"].unique()
)

res_type = st.sidebar.multiselect(
    "Select the Restaurant type:",
    options=df["rest_type"].unique()
    )

df_selection_type = df.query(
    "rest_type == @res_type "
)

# ------------------------------------------ MAIN PAGE ---------------------------------------
new_title = '<p style="font-family:sans-serif; font-size: 35px; color:#99512c; text-align: center">Find the best restaurant in town!!!</p>'
st.markdown(new_title, unsafe_allow_html=True)

# ------ Filter 1: Select restaurant name for details ----------
new_title = '<p style="font-family:sans-serif; font-size: 25px; color:#173247; text-align: center"><u>Restaurant Details</u?</p>'
st.markdown(new_title, unsafe_allow_html=True)
for i in range(len(names)):
    name = names[i]

    # considering each name at a time
    df_selection = df.query(
        "restaurants == @name"
    )
    # average rating
    average_rating = round(df_selection["rating"].mean(), 1)
    star_rating = ":star:" * int(round(average_rating, 0))
    # average cost
    average_cost = round(df_selection['cost_for_two'].mean(), 1)
    cost = int(round(average_cost, 0))
    # available cuisines
    cuisines = df_selection['cuisines'].tolist()
    cuisine = []
    for inp in cuisines:
        j = inp.split(",")
        for el in j:
            if el not in cuisine:
                cuisine.append(el)

    st.subheader(f"{name}")
    print(name[i])
    st.subheader("Cuisines: {}".format(f"{cuisine}"))
    st.subheader("Cost for two: " + f"{cost}")
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
    st.markdown("___",unsafe_allow_html=False)
    # st.write(":heavy_minus_sign:" * 34)

# ----------------------------Filter 2: restaurants and rating ------------------------------------
new_title = '<p style="font-family:sans-serif; font-size: 25px; color:#173247; text-align: center"><u>Compare Restaurants(based on ratings)</u?</p>'
st.markdown(new_title, unsafe_allow_html=True)
restaurants = df['restaurants'].unique().tolist()
rating = df['rating'].unique().tolist()

rating_selection = st.slider('Rating:',
                           min_value=min(rating),
                           max_value=max(rating),
                           value=(min(rating), max(rating)))

res_selection = st.multiselect('Restaurants:',
                               restaurants,
                               default=restaurants[0])
mask = (df['rating'].between(*rating_selection)) & (df['restaurants'].isin(res_selection))
num_of_result = df[mask].shape[0]
st.markdown(f'Available Results: {num_of_result}')
if num_of_result > 0:
    df_grouped = df[mask].groupby(by=['restaurants']).mean()[['rating']]
    df_grouped = df_grouped.rename({'rating': 'rating'})
    df_grouped = df_grouped.reset_index()
    bar_chart = px.bar(df_grouped,
                       x='restaurants',
                       y='rating',
                       text='restaurants',
                       color_discrete_sequence=['#F67726']*len(df_grouped),
                       template='plotly_white')
    st.plotly_chart(bar_chart)
    st.markdown("___",unsafe_allow_html=False)



# -----------------------Filter 3: name of restaurants based on cuisines --------------------------------------------
new_title = '<p style="font-family:sans-serif; font-size: 25px;color:#173247;text-align: center"><u>Famous locations for specific restaurant type</u?</p>'
st.markdown(new_title, unsafe_allow_html=True)
mask_4 = (df['rest_type'].isin(res_type))
number_of_result = df[mask_4].shape[0]
st.markdown(f'*Total locations available for selected restaurant type: {number_of_result}*')
if number_of_result > 0:
    df_grouped1 = df[mask_4].groupby(by=['location']).count()[['rest_type']]
    df_grouped1 = df_grouped1.rename(columns={'location': 'location'})
    df_grouped1 = df_grouped1.reset_index()

    bar_chart_loc = px.bar(df_grouped1,
                           x='location',
                           y='rest_type',
                           text='rest_type',
                           title = f"<b>Restaurant type: {res_type} based on location</b>",
                           color_discrete_sequence = ['#F63366']*len(df_grouped1),
                           template= 'plotly_white')
    st.plotly_chart(bar_chart_loc)
st.markdown("___",unsafe_allow_html=False)



# ----- Filter 4: Res type based on location -------------
new_title = '<p style="font-family:sans-serif; font-size: 25px; color:#173247; text-align: center"><u>List of Restaurants having the selected cuisine type</u?</p>'
st.markdown(new_title, unsafe_allow_html=True)
cuisine_3 = []
cuisines = df["cuisines"].tolist()
for i in cuisines:
    item = i.split(",")
    for peritem in item:
        if peritem not in cuisine_3:
            cuisine_3.append(peritem)
cuisine_type = st.sidebar.multiselect(
    "Select the Cuisine Type:",
    options=sorted(set(cuisine_3))
)
cu_lis = []
for i in df['cuisines']:
    for j in cuisine_type:
        if j in i:
            cu_lis.append(i)

df_sel = df.query(
    "cuisines == @cu_lis"
)

if len(df_sel) != 0:
    st.subheader("The following restaurants have the selected cuisines: ")
for el in df_sel['restaurants'].unique():
    st.subheader(f"{el}")
st.markdown("___", unsafe_allow_html=False)



# ------------------Filter 5: top location -------------
new_title = '<p style="font-family:sans-serif; font-size: 25px; color:#173247; text-align: center"><u>Top Restaurants based on votes in a specific location</u?</p>'
st.markdown(new_title, unsafe_allow_html=True)
input_col, pie_col = st.columns(2)
n = input_col.text_input('How many top restaurants(based on votes) would you like to see?',3)
n = int(n)

df_table = pd.read_excel('zomato_1.xlsx',
                   sheet_name= 'zomato (1)',
                   usecols='A:N',
                   nrows=50,
                   header=0)
df_table = df_table.head(n)
pie_chart = px.pie(df_table,
                   title=f'Top {n} Restuarants based on votes',
                   values='votes',
                   #title = '<b>Top rated restaurants</b>',
                   names='restaurants')
st.plotly_chart(pie_chart)
st.markdown("___", unsafe_allow_html=False)

# ------------------Filter 6: ---------------------------------------------------------
new_title = '<p style="font-family:sans-serif; font-size: 25px; color:#173247; text-align: center"><u>List of Restaurants based on location and cost for two people</u?</p>'
st.markdown(new_title, unsafe_allow_html=True)
location = st.sidebar.multiselect(
    "Select the Location:",
    options = df["location"].unique()
)

cost = st.sidebar.multiselect(
    "Select the Cost:",
    options = df["cost_for_two"].unique()
)

df_selection_pk = df.query(
    "cost_for_two == @cost & location == @location"
)

resto = df_selection_pk["restaurants"].values
temp_rate = df_selection_pk["rating"].fillna(0)
average_rate = round(temp_rate.mean(), 1)


if math.isnan(average_rate):
    star_rate = ":star:" * 0
else:
    star_rate = ":star:" * int(round(average_rate, 0))
avg_cost = round(df_selection_pk['cost_for_two'].mean(), 1)


left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Average Cost:")
    st.subheader(f"{avg_cost:,}  ")

with middle_column:
    st.subheader("Average rating:")
    st.subheader(f"{average_rate} {star_rate}")

with right_column:
    st.subheader("Restaurants ")
    unique_elements, counts_elements = np.unique(resto, return_counts=True)
    arr = np.asarray((unique_elements, counts_elements)).T
    for i in arr:
        st.subheader(i)
st.markdown("___",unsafe_allow_html=False)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

