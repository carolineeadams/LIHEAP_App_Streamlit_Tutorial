#code for streamlit app demo creation for tutorial for streamlit-based interactive data visualizations
#Caroline Adams, last updated Nov 11 2022

#importing packages
import streamlit as st
import requests
import pandas as pd
import numpy as np
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px

#add title for streamlit app
st.title("Communities Placed At Highest Risk of the Negative Effects of Extreme Heat from Climate Change")

#add subheader for background context section
st.subheader("Background")

#add text to explain background of project and data visualizations
st.write("The Low Income Home Energy Assistance Program (LIHEAP) has been administered by the Department of Health and Human Services (HHS) since 1981 to provide low-income households with financial assistance to cover energy bills (heating, cooling) and weatherization of their homes. LIHEAP is a program highlighted under the Biden Administration's Justice40 Initiative, which pledges to allocate 40 percent of federal investments in climate-tangential areas to communities historically overburdened by pollution and the negative effects of climate change.")

st.write("The LIHEAP program offers financial assistance to households in need of support with energy (heat and cooling) and weatherization expenses. Program leaders anticipate that due to climate change, the program's role in supporting families with their cooling expenses will increase substantially over the next few decades and grow to be a larger proportion of the program's main focus. The LIHEAP program provides benefits to households with low incomes, older adults, young children, and people with disabilities. These populations match some of the communities that the the Environmental Protection Agency (EPA) has indicated are placed at highest risk of experiencing the negative effects of extreme heat due to climate change.")

st.write("This app retrieves publicly available data from the 2019 American Community Survey 5-Year Estimates related to the populations described above that are at highest risk of experiencing the negative effects of extreme heat. Variables can be explored in a variety of ways to understand variation across the United States in terms of proportions of populations in each state. An average vulnerability index is also calculated based on the available data to demonstrate which states have the highest proportions of populations vulnerable to extreme heat.")

#define dictionary of variables to pull from census api
dic = {"NAME": "State_Name",
    'B02001_001E': 'Total_Pop',
      "B18135_003E": "Under19_Disability",
      "B18135_014E": "19-64_Disability",
      "B18135_025E": "65Plus_Disability",
      'B02001_002E': 'White',
      "B27001_005E": "Male_under6_NoHC",
       "B27001_008E": "Male_6to18_NoHC",
       "B27001_011E": "Male_19to25_NoHC",
       "B27001_014E": "Male_26to34_NoHC",
       "B27001_017E": "Male_34to44_NoHC",
       "B27001_020E": "Male_45to54_NoHC",
       "B27001_023E": "Male_55to64_NoHC",
       "B27001_026E": "Male_65to74_NoHC",
       "B27001_029E": "Male_over75_NoHC",
       "B27001_033E": "Female_under6_NoHC",
       "B27001_036E": "Female_6to18_NoHC",
       "B27001_039E": "Female_19to25_NoHC",
       "B27001_042E": "Female_26to34_NoHC",
       "B27001_045E": "Female_34to44_NoHC",
       "B27001_048E": "Female_45to54_NoHC",
       "B27001_051E": "Female_55to64_NoHC",
       "B27001_054E": "Female_65to74_NoHC",
       "B27001_057E": "Female_over75_NoHC",
       "B09019_008E": "Female_livingalone",
       "B09019_005E": "Male_livingalone",
       'B01001_001E':'Age_Total',
        'B01001_020E': 'Male 65-66',
        'B01001_021E': 'Male 67-69',
        'B01001_022E': 'Male 70-74',
        'B01001_023E': 'Male 75-79',
        'B01001_024E': 'Male 80-84',
       'B01001_025E': 'Male >=85',
       'B01001_044E': 'Female 65-66',
        'B01001_045E': 'Female 67-69',
        'B01001_046E': 'Female 70-74',
        'B01001_047E': 'Female 75-79',
        'B01001_048E': 'Female 80-84',
       'B01001_049E': 'Female >=85',
       'B06012_002E': "Below 100% of poverty level",
       "B06012_003E": "100-149% of poverty level",
       'B06009_001E':'Total_Education_Pop',
       "B06009_002E": "Less than high school diploma"}

#get dictionary key names
variable_keys=dic.keys()

#joining strings in list of keys into one string
variable_keys_joined=','.join(variable_keys)

#get list of dictionary values
variable_names= list(dic.values())

#append FIPS as a variable name
variable_names.append("FIPS")

#define function to call API query and save request
#at cache feature to save collected data to local cache in app
@st.cache
def get_data():
    r = requests.get("https://api.census.gov/data/2019/acs/acs5", params = {"get":variable_keys_joined,"for":"state:*"})
    return r

#call function to get Census data
r = get_data()

#creating dataframe from census api data
census_df = pd.DataFrame(columns=variable_names, data=r.json()[1:])

#define function to clean census api data
#add cache feature to save obtained and cleaned data to local cache in app
@st.cache
def clean_dta(census_df):
    #obtain list of column names
    column_names=[census_df.columns]
    #turn certain variables into integers
    census_df[['Total_Pop', 'Under19_Disability', '19-64_Disability',
            '65Plus_Disability', 'White', 'Male_under6_NoHC', 'Male_6to18_NoHC',
            'Male_19to25_NoHC', 'Male_26to34_NoHC', 'Male_34to44_NoHC',
            'Male_45to54_NoHC', 'Male_55to64_NoHC', 'Male_65to74_NoHC',
            'Male_over75_NoHC', 'Female_under6_NoHC', 'Female_6to18_NoHC',
            'Female_19to25_NoHC', 'Female_26to34_NoHC', 'Female_34to44_NoHC',
            'Female_45to54_NoHC', 'Female_55to64_NoHC', 'Female_65to74_NoHC',
            'Female_over75_NoHC', 'Female_livingalone', 'Male_livingalone',
            'Age_Total', 'Male 65-66', 'Male 67-69', 'Male 70-74', 'Male 75-79',
            'Male 80-84', 'Male >=85', 'Female 65-66', 'Female 67-69',
            'Female 70-74', 'Female 75-79', 'Female 80-84', 'Female >=85',
            'Below 100% of poverty level', '100-149% of poverty level','Total_Education_Pop',
            'Less than high school diploma']] = census_df[['Total_Pop', 'Under19_Disability', '19-64_Disability',
            '65Plus_Disability', 'White', 'Male_under6_NoHC', 'Male_6to18_NoHC',
            'Male_19to25_NoHC', 'Male_26to34_NoHC', 'Male_34to44_NoHC',
            'Male_45to54_NoHC', 'Male_55to64_NoHC', 'Male_65to74_NoHC',
            'Male_over75_NoHC', 'Female_under6_NoHC', 'Female_6to18_NoHC',
            'Female_19to25_NoHC', 'Female_26to34_NoHC', 'Female_34to44_NoHC',
            'Female_45to54_NoHC', 'Female_55to64_NoHC', 'Female_65to74_NoHC',
            'Female_over75_NoHC', 'Female_livingalone', 'Male_livingalone',
            'Age_Total', 'Male 65-66', 'Male 67-69', 'Male 70-74', 'Male 75-79',
            'Male 80-84', 'Male >=85', 'Female 65-66', 'Female 67-69',
            'Female 70-74', 'Female 75-79', 'Female 80-84', 'Female >=85',
            'Below 100% of poverty level', '100-149% of poverty level','Total_Education_Pop',
            'Less than high school diploma']].apply(pd.to_numeric)
    #calculate number of individuals below 150% FPL
    census_df['Below_150_FPL'] = census_df['Below 100% of poverty level'] + census_df['100-149% of poverty level']
    #calculate percentage of individuals below 150%
    census_df['Percent_Below_150_FPL'] = census_df['Below_150_FPL']/census_df['Total_Pop']
    #calculate percentage of nonwhite individuals
    census_df['NonWhite_Perc'] = 1 - (census_df.White / census_df.Total_Pop)
    #calculate total individuals with disabilities
    census_df['Total_Disability'] = census_df['Under19_Disability'] + census_df['19-64_Disability'] + census_df['65Plus_Disability']
    #calculate percentage of individuals with disabilities
    census_df['Percent_Disability'] = census_df['Total_Disability']/census_df['Total_Pop']
    #calculate total uninsured individuals
    census_df['Total_Uninsured'] = census_df["Male_under6_NoHC"] +census_df["Male_6to18_NoHC"] +census_df["Male_19to25_NoHC"]+census_df["Male_26to34_NoHC"] +census_df["Male_34to44_NoHC"] +census_df["Male_45to54_NoHC"] +census_df["Male_55to64_NoHC"] +census_df["Male_65to74_NoHC"] +census_df["Male_over75_NoHC"]+census_df["Female_under6_NoHC"] +census_df["Female_6to18_NoHC"] +census_df["Female_19to25_NoHC"] +census_df["Female_26to34_NoHC"] +census_df["Female_34to44_NoHC"]+census_df["Female_45to54_NoHC"] + census_df["Female_55to64_NoHC"]+census_df["Female_65to74_NoHC"]+census_df["Female_over75_NoHC"]
    #calculate percent uninsured
    census_df['Percent_Uninsured'] = census_df['Total_Uninsured']/census_df['Total_Pop']
    #calculate total individuals living alone
    census_df['Total_Livingalone'] = census_df['Female_livingalone'] + census_df['Male_livingalone']
    #calculate percent living alone
    census_df['Percent_Livingalone'] = census_df['Total_Livingalone']/census_df['Total_Pop']
    #calculate total individuals with ages over 65
    census_df['Total_Over65'] = census_df['Male 65-66']+census_df['Male 67-69']+census_df['Male 70-74']+census_df['Male 75-79']+census_df['Male 80-84']+census_df['Male >=85']+census_df['Female 65-66']+census_df['Female 67-69']+census_df['Female 70-74']+census_df['Female 75-79']+census_df['Female 80-84']+census_df['Female >=85']
    #calculate percent individuals over 65
    census_df['Percent_Over65'] = census_df['Total_Over65']/census_df['Age_Total']
    #calculate percentage of individuals with no high school diploma
    census_df['Percent_NoHSDiploma'] = census_df['Less than high school diploma']/census_df['Total_Education_Pop']
    #subset dataframe to variables of interest
    census_df_lmtd=census_df[["State_Name", "FIPS", 'Total_Pop','Below_150_FPL', 'Percent_Below_150_FPL', 'NonWhite_Perc', 'Total_Disability', 'Percent_Disability', 'Total_Uninsured',  'Percent_Uninsured', 'Total_Livingalone', 'Percent_Livingalone', 'Total_Over65', 'Percent_Over65']]
    #set index to state name
    census_df_lmtd.set_index(['State_Name'], inplace=True)
    #calculate average vulnerable proportion
    census_df_lmtd['Average_Vulnerable_Proportion'] = census_df_lmtd[['Percent_Below_150_FPL', 'NonWhite_Perc', 'Percent_Disability', 'Percent_Uninsured','Percent_Livingalone', 'Percent_Over65']].mean(axis=1)
    #reset index
    census_df_lmtd.reset_index(inplace=True)
    #rename variables
    census_df_lmtd.rename(columns = {'FIPS':'STATEFP', "State_Name": "NAME", 'Total_Pop': 'Total Population','Below_150_FPL': "Individuals with Incomes Below 150% FPL", 'Percent_Below_150_FPL': "Percentage of Individuals with Incomes below 150% FPL", 'NonWhite_Perc': "Percentage of Racial/Ethnic Minoritized Individuals", 'Total_Disability': "Total Number of Individuals with Disabilities", 'Percent_Disability': "Percentage of Individuals with Disabilities", 'Total_Uninsured': "Total Number of Uninsured Individuals", 'Percent_Uninsured': "Percentage of Individuals without Health Insurance", 'Total_Livingalone': "Total Number of Individuals Living Alone", 'Percent_Livingalone': "Percentage of Individuals Living Alone", 'Total_Over65': "Total Number of Individuals Ages 65 and Over", 'Percent_Over65': "Percentage of Individuals Ages 65 and Over", "Average_Vulnerable_Proportion": "Average Percentage of Individuals in at Least One Vulnerable Community"}, inplace = True)
    #return limited dataframe
    return census_df_lmtd

#call cleaning function and save resulting dataframe to object
census_df_lmtd=clean_dta(census_df)

#adding subheader to streamlit app
st.subheader('Raw Data from the American Community Survey 5-Year Estimates (2019)')

#allow strealit app users to explore raw data if they check a box
if st.checkbox("Explore Raw Data"):
    st.dataframe(census_df_lmtd)

#create list of variables for users to select from
variable_list = ['Total Population', 'Individuals with Incomes Below 150% FPL', 'Percentage of Individuals with Incomes below 150% FPL',
       'Percentage of Racial/Ethnic Minoritized Individuals', 'Total Number of Individuals with Disabilities', 'Percentage of Individuals with Disabilities',
       'Total Number of Uninsured Individuals', 'Percentage of Individuals without Health Insurance', 'Total Number of Individuals Living Alone',
       'Percentage of Individuals Living Alone', 'Total Number of Individuals Ages 65 and Over', 'Percentage of Individuals Ages 65 and Over',
       'Average Percentage of Individuals in at Least One Vulnerable Community']

#create sidebar for users to select a variable of interest
variable_selected = st.sidebar.selectbox(label = "Choose a factor that places one at higher risk of experiencing negative effects from extreme heat", options = variable_list)

#add cache feature to save obtained and cleaned data to local cache after function is run in app
@st.cache
#define function to get geo data
def get_geo_dta():
    #set file path to shapefile document
    path = "Data/tl_2021_us_state.shp"
    #read in geopandas shapefile
    df = gpd.read_file(path)
    #save shapefile to dataframe
    df = df.to_crs("EPSG:4326")
    #drop state name column in census_lmtd df
    census_df_lmtd2=census_df_lmtd.drop(columns=['NAME'])
    #merge census_df_lmtd onto shapefile
    geo_dta = df.merge(census_df_lmtd2,on='STATEFP')
    #renaming FIPS code column to match geo_data columns
    geo_dta.rename(columns = {'STUSPS':'State'}, inplace = True)
    #removing non states
    non_states = ['VI','MP','GU','AS','PR']
    #saving another copy of geo_dta
    us51 = geo_dta
    #removing non states
    for n in non_states:
        us51 = us51[us51.State != n]
    return us51

#obtaining geo data
us51=get_geo_dta()

#add subheader for seaborn histogram
st.subheader("Distribution of Proportions of Selected Vulnerable Community Present Across all States in the U.S. (Source: American Community Survey 5-Year Estimates, 2019)")

#define function to plot histograms of nationwide distribution of vulnerable population
#add caching feature
@st.cache(allow_output_mutation=True)
def plot_hist(var):
    x1=census_df_lmtd[var]
    x1=x1.fillna(x1.mean())
    fig = sns.displot(census_df_lmtd, x=x1, color = "#FF6347")
    return fig

#run function and display plot in app
st.pyplot(plot_hist(variable_selected))

#add subheader for altair bar chart
st.subheader("Comparing Proportions of Selected Vulnerable Community Present in Each State (Source: American Community Survey 5-Year Estimates, 2019)")

#defining function to generate altair_chart
#add caching feature
@st.cache(allow_output_mutation=True)
def alt_chart(var):
    alt_plot = alt.Chart(census_df_lmtd).mark_bar(color="#4B0082").\
    encode(alt.X("NAME", sort="-y"),
           y=var)
    return alt_plot

#display chart in streamlit app
st.altair_chart(alt_chart(variable_selected))

#add subheader for U.S. map using plotly
st.subheader("Variation in Proportion of Selected Vulnerable Community Across the United States (Source: American Community Survey 5-Year Estimates, 2019)")

#defining function to plot variables by state
#adding caching feature
@st.cache(allow_output_mutation=True)
def StatesPlot(df,var):
    fig = px.choropleth(df,locations='State', color=var,
                           color_continuous_scale="pinkyl",
                           #range_color=(0, 0.4),
                           hover_name='NAME',
                           locationmode='USA-states',
                           scope="usa",
                           labels={var:var}
                          )
    return fig

#showing figure in streamlit app
st.plotly_chart(StatesPlot(us51,variable_selected))
