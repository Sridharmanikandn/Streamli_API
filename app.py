import streamlit as st  
import requests  
from streamlit_option_menu import option_menu
import time
import json
import altair as alt  
import pandas as pd
from datetime import datetime

with st.sidebar:
    selected = option_menu(
        menu_title= "Main Menu",
        options= ["Home","Dashboard"],
        icons= ["house","speedometer"],
        menu_icon= "Cast"
    )

def authenticate_user():
    otp_url = "https://api.prac360.com/auth/otp/8870677228"
    verify_url = "https://api.prac360.com/auth/verify"
    API_HEADER = {"tenantid": "33c75f9f", "appinfo": "CUSTOMER"}

    response = requests.get(otp_url, headers=API_HEADER)
    
    if response.status_code == 200:
        print("Successfully get the OTP")
        print(response.status_code)
    else:
        print("Not Successfully get the OTP")
        return None
    
    time.sleep(1)
    
    otp_data = {
        "otp": 242629,
        "mobileNumber": "8870677228"
    }
    
    verify_response = requests.post(verify_url, json=otp_data, headers=API_HEADER)
    
    if verify_response.status_code == 201:
        json_object = verify_response.json()
        token = json_object['data']['token']
        print("Successfully Authentication")
        print(token)
        return token
    else:
        print("Authentication failed")
        return None

auth_token = authenticate_user()
if auth_token:
    api_headers_with_token = {"Authorization": f"Bearer {auth_token}","tenantid": "33c75f9f", "appinfo": "CUSTOMER"}
    API_ENDPOINT = "https://api.prac360.com/dashboard/slotreport"
def fetch_slots():
    breatheasy='5f0a9c7f624afc79798e66d7'
    chestcare ='a8b466a5ddeeb379556f3024'
    option = st.selectbox(
        'selected the Clinics',
        ("breatheasy", "chestcare"))
    if option == "breatheasy":
        value =breatheasy
    if option == "chestcare":
        value =chestcare    
    d = st.date_input("Start Date" )    
    print(d)
    d1 = st.date_input("End Date")
    print(d1)
    start_date = str(d)
    end_date = str(d1)
    
    payload = {
        "doctorIds": [value],
        "slotType": ["CUSTOMER"],
        "startDate":start_date,
        "endDate": end_date,
        "slotView": True
    }
    response = requests.post(API_ENDPOINT, headers=api_headers_with_token, json=payload)
    print(response)
    


    if response.status_code == 201:
        data = response.json()
        if data ["statusCode"] == 1037:
        #    st.error('No data to show')
            print("Status error")
        else: 
           for slot in data['data']['slots']:
            slot['date'] = datetime.strptime(slot['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            slots_data = data['data']['slots']
            print(slots_data)
        if data["statusCode"] == 1001:  
            return slots_data
        else:
            # st.error(f"API erroring: {data['msg']}")
            print("API error")
    else:
        st.error(f"API errors: {response.status_code}")

    return None

if selected == "Home":
        st.title(f"you selected the {selected}")
   
        slots = fetch_slots()       
        if slots:
           st.write("## Slot Booking Summary")
           st.dataframe(slots) 
        else:
             st.warning("No data available for selected dates.")
         
if selected == "Dashboard":
          st.title(f"you selected the {selected}")
          Chart = fetch_slots()       
          if Chart:
           df = pd.DataFrame(Chart)
           charting = alt.Chart(df).mark_bar().encode(
                x='date',
                y='bookedAppointments:Q',
                tooltip=['bookingPerSlot','bookedAppointments', 'slotId','date','listOfAppointmentId']
           ).interactive()
           st.altair_chart(charting, use_container_width=True)
          else:
             st.warning("No data available for selected dates.")
       