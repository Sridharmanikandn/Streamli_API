import streamlit as st  
import requests  
from streamlit_option_menu import option_menu
import time
import json
import altair as alt  
import pandas as pd
from datetime import datetime
import io

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
        token = json_object ['data']['token']
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
def fetch_slots(Slot_view): 
    get_all_hospital = "https://api.prac360.com/v1/hospital"
    response = requests.get(get_all_hospital,headers=api_headers_with_token)
    hospital_info= []
    if response.status_code == 200: 
      print(response.json())
      hospital_data =  response.json()
      if hospital_data ["statusCode"] == 1001:
          for hospital in hospital_data ["data"]:
              hospital_id = hospital["_id"]
              hospital_name = hospital["name"]
              hospital_info.append({"hospital_id": hospital_id, "hospital_name": hospital_name})
      else:
        print("can't get the hospital name and ID's ")
    else:
        
        print("Error:", response.status_code, response.text)
    
    hospital_name = [hospital["hospital_name"] for hospital in hospital_info]
    selected_hospital = st.selectbox('Select a hospital:', hospital_name)
    selected_hospital_id = None
    for hospital in hospital_info:
        if hospital["hospital_name"] == selected_hospital:
         selected_hospital_id = hospital["hospital_id"]
         break
     

    HOSPITAL_ENDPOINT = "https://api.prac360.com/v1/doctor/onhospital/"   
    response = requests.get(HOSPITAL_ENDPOINT+selected_hospital_id, headers=api_headers_with_token)
    doctor_info = []
    if response.status_code == 200: 
      print(response.json())
      json_data =  response.json()
      if json_data ["statusCode"] == 1001:
            print('valid data')
            for doctor in json_data["data"]["doctorIds"]:
               doctor_id = doctor["_id"]
               doctor_name = doctor["profileId"]["name"]
               doctor_info.append({"doctor_id": doctor_id, "doctor_name": doctor_name})

            output_filename = "doctor_info.json"
            with open(output_filename, "w") as output_file:
              json.dump(doctor_info, output_file, indent=4)
            print("Doctor information has been saved to", output_filename) 
            print(doctor_info)  
      else:
        print("can't get the doctors name and ID's ")
    else:
        
        print("Error:", response.status_code, response.text)


    doctor_names = [doctor["doctor_name"] for doctor in doctor_info]
    selected_doctor = st.selectbox('Select a doctor:', doctor_names)
    selected_doctor_id = None
    for doctor in doctor_info:
     if doctor["doctor_name"] == selected_doctor:
         selected_doctor_id = doctor["doctor_id"]
         HOSPITAL_ID_ = str(selected_doctor_id)
         break
   
    
    
    d = st.date_input("Start Date" )    
    print(d)
    d1 = st.date_input("End Date")
    print(d1)
    start_date = str(d)
    end_date = str(d1)
    
    payload = {
        "doctorIds": [HOSPITAL_ID_],
        "slotType": ["CUSTOMER"],
        "startDate":start_date,
        "endDate": end_date,
        "slotView": Slot_view,
        "appointmentStatus":["BOOKED","RESCHEDULED","VISITED"]

    }
    response = requests.post(API_ENDPOINT, headers=api_headers_with_token, json=payload)
    print(response)
    


    if response.status_code == 201:
        data = response.json()
        if data ["statusCode"] == 1001:
            print("Status error") 
            if Slot_view == False:
                json_data= data['data']['slots']
                print(json_data)
                booking_per_slot = json_data['bookingPerSlot']
                booked_appointments = json_data['bookedAppointments']
                print("Booking Per Slot:", booking_per_slot)
                print("Booked Appointments:", booked_appointments)
                return booking_per_slot, booked_appointments
            else:
              for slot in data['data']['slots']:
               slot['date'] = datetime.strptime(slot['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
               slots_data = data['data']['slots']
               print(slots_data)  
               return slots_data
        else:
            st.warning("No data available for selected dates.")
    else:
        st.error(f"API errors: {response.status_code}")

    return None

if selected == "Home":
        st.title(f"you selected the {selected}")
        option = st.radio("Do you want to see the Total Appointments for selected dates", ("Not-now", "Yes"))
        if option == "Not-now":
               value=True
        elif option == "Yes":
                value=False
        result= fetch_slots(Slot_view=value)
        if isinstance(result, tuple):
             booking_per_slot, booked_appointments = result
             print(result)
             containers = st.container()
             containers.write("Booking per Appointment")
             containers.write(booking_per_slot)   
             containerss = st.container()
             containerss.write("Total Appointments")
             containerss.write(booked_appointments)    
        else:
           st.write("## Slot Booking Summary")
           st.dataframe(result)
           if option == "Not-now" :   
             if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
               df = pd.DataFrame(result)
               excel_buffer = io.BytesIO()
               df.to_excel(excel_buffer, index=False, header=True)
               st.download_button( 
                label="Download Excel",
                data=excel_buffer.getvalue(),
                file_name="slot_booking_summary.xlsx", 
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  
            )
        
        
         
if selected == "Dashboard":
          st.title(f"you selected the {selected}")
          Chart = fetch_slots(Slot_view=True)       
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
       