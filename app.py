import streamlit as st
import pandas as pd
import json
import requests
import plotly.graph_objects as go
# from Linkedin_scraping import get_linkedin_info
from places_api import google_data

GMAPS_API_KEY="AIzaSyBja88VRg3fkfpYcseDWpQXuVuOGdLKEBI"

def main():
    st.set_page_config(page_title='ESDC', page_icon=':office:',layout='wide')
    st.sidebar.title("Menu")
    app_mode = st.sidebar.selectbox("Please select a page", ["MainPage", "Business Tracker"])

    if app_mode=="MainPage":
        load_mainpage()
    
    elif app_mode=="Business Tracker":
        load_business()
    

def load_mainpage():
    st.header("Welcome To the Business Tracker")

def check_nan(x):
    if type(x)==float:
        return [0,0]
    else:
        return json.loads(x)['coordinates']

def lat(x):
        return x[1]

def lon(x):
    return x[0]

@st.cache
def load_data():
    df = pd.read_csv('business-licences-hackathon.csv', sep=';')  
    df['Geom'] = df['Geom'].apply(check_nan)
    df['lat'] = df['Geom'].apply(lat)
    df['lon'] = df['Geom'].apply(lon)
    return df

def process_issue(df, business_name):
    df_van = df[df['City']=='Vancouver']
    df_company = df_van[df_van['BusinessName']==business_name]
    df_company = df_company[['LicenceNumber','Status','IssuedDate','ExpiredDate']]
    df_company['Year'] = df_company['LicenceNumber'].apply(lambda x: "20"+str(x[:2]))
    df_company['color'] = df['Status'].apply(lambda status:color_code(status))
    df_company.loc[df_company.IssuedDate.isnull(), 'IssuedDate'] = 'N/A'
    df_company.loc[df_company.ExpiredDate.isnull(), 'ExpiredDate'] = 'N/A'
    df_company = df_company.sort_values(by=['Year'])
    return df_company

def render_plot(df_company):
    fig = go.Figure(data=[go.Table(header=dict(values=["<b>Year<b>", "<b>Status</b>","<b>IssuedDate<b>","<b>ExpiredDate<b>"],line_color='white', fill_color='lightskyblue',align='center', font=dict(color='black', size=12)),cells=dict(
    values=[df_company.Year, df_company.Status, df_company.IssuedDate, df_company.ExpiredDate],
    line_color=[df_company.color], fill_color=[df_company.color],
    align='center', font=dict(color='black', size=11)))])
    st.plotly_chart(fig)

def render_linkedin_card(business_name):
    linkedin_json = get_linkedin_info(business_name)
    st.write(linkedin_json)
    linkedin_card = """
                
                <body>
                <div class="card" style="box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2); max-width: 300px; margin: auto;text-align: center;font-family: arial;">
                <img src="https://softwareengineeringdaily.com/wp-content/uploads/2020/02/LinkedIn.jpg" alt="John" style="width:100%">
                <h1>Linkedin</h1>
                <p class="title" style="color: grey;font-size: 18px;">Industry: {}</p>
                <p class="title" style="color: grey;font-size: 18px;">HQ: </p>
                <p class="title" style="color: grey;font-size: 18px;">Company Type: </p>
                <p class="title" style="color: grey;font-size: 18px;">Founded:</p>
                <p class="title" style="color: grey;font-size: 18px;">Employees: </p>
                
                <p><button style ="border: none;outline: 0;display: inline-block;padding: 8px;color: white;background-color: #000;text-align: center;cursor: pointer;width: 100%;font-size: 18px;">Confidence Score: 68%</button></p>
                </div>

                </body>""".format("Sammy")
    #st.markdown(linkedin_card, unsafe_allow_html=True)

def render_google_data(business_code,business_name,GMAPS_API_KEY):
    google_response = google_data(business_code,business_name,GMAPS_API_KEY)
    # st.write(json_data)
    google_card = """
                
                <body>
                <div class="card" style="box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2); max-width: 800px; margin: auto;text-align: center;font-family: arial;">
                <img src="" alt="John" style="width:100%">
                <h1>Google Reviews</h1>
                <p class="title" style="color: grey;font-size: 18px;"><b>Business Name</b>: {}</p>
                <p class="title" style="color: grey;font-size: 18px;"><b>Business Status</b>:{} </p>
                <p class="title" style="color: grey;font-size: 18px;"><b>Address</b>:{} </p>
                <p class="title" style="color: grey;font-size: 18px;"><b>Rating</b>:{}</p>
                <p class="title" style="color: grey;font-size: 18px;"><b>Phone Number</b>:{}</p>
                <p class="title" style="color: grey;font-size: 18px;"><b>Review Time</b>:{} </p>
                <p class="title" style="color: grey;font-size: 18px;"><b>Review</b>:{}</p>
                <p class="title" style="color: grey;font-size: 18px;"><b>Author URL</b>: <a href="{}" target="_blank">link</a></p>
                <p class="title" style="color: grey;font-size: 18px;"><b>Website</b>:<a href="{}"> website</a></p>
                
                <p><button style ="border: none;outline: 0;display: inline-block;padding: 8px;color: white;background-color: #000;text-align: center;cursor: pointer;width: 100%;font-size: 18px;">Confidence Score: 68%</button></p>
                </div>

                </body>""".format(google_response['name'], google_response['status'], google_response['address'], google_response['rating'], google_response['number'], google_response['review_time'], google_response['review text'], google_response['author url'], google_response['website'])

    st.markdown(google_card, unsafe_allow_html=True)
    

def color_code(status):
    if status=='Pending':
        return 'rgb(255, 255, 102)'
    elif status=='Issued':
        return 'rgb(204, 255, 229)'
    elif status=='Cancelled':
        return 'rgb(255, 153, 153)'
    elif status=='Gone Out of Business':
        return 'rgb(204, 153, 255)'
    elif status=='Inactive':
        return 'rgb(224, 224, 224)'


def load_business():
    business_data = load_data()
    # row_num = st.number_input('Choose the display size', min_value=5)
    business_name = st.selectbox('Select The Business you want to explore',business_data['BusinessName'].unique())
    business_df = business_data[business_data['BusinessName']==business_name]
    business_count = business_df['BusinessName'].count()
    business_code = business_df['PostalCode'].unique()
    
    issue_df = process_issue(business_data, business_name)
    render_plot(issue_df)
    # if len(business_code)==1:
    #     st.write("Found 1 Matching Pincode")
    render_google_data(business_code,business_name,GMAPS_API_KEY)
    
    #    st.write(response.json())
    st.write("There are "+str(business_count)+" Matches for "+business_name)
    
    if st.checkbox("View Records"):
        st.write(business_df)
    if st.checkbox("View On Map"):
        st.map(business_df)
    st.subheader("Linkedin")
    # render_linkedin_card(business_name)
    

if __name__ == "__main__":
    main()