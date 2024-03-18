import requests
import time
import json

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
print("second time take the token")
print(auth_token)
api_headers_with_token = {"tenantid": "33c75f9f", "appinfo": "CUSTOMER", "Authorization": f"Bearer {auth_token}"}
API_ENDPOINT = "https://api-staging.agamworks.com/dashboard/slotreport"





