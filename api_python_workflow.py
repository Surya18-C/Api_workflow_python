import requests
from urllib.parse import urlencode

# Constants
BASE_URL = "http://52.172.161.46:8081/kyvos/rest"
LOGIN_URL = f"{BASE_URL}/login"
PARAM_UPDATE_URL = f"{BASE_URL}/rdatasets/addUpdateUserParams"
PROCESS_MODEL_URL = f"{BASE_URL}/smodels/process"
JOB_STATUS_URL = f"{BASE_URL}/smodels/jobStatus"

# Credentials
USERNAME = "powerbiuser"
PASSWORD = "Welcome@1234"

# Parameters
folder_id = "folder_17369445026759127071078127752581"
dataset_id = "17381482665992127029029111213702"
param_name = "Location_ID"
param_value = "A134"
smodel_id = "SMODEL_OBJECT_17194863114789127072017142225560"
smodel_name = "Test Model"

#  Login and get session ID
def login():
    payload = {
        "username": USERNAME,
        "password": PASSWORD
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(LOGIN_URL, headers=headers, data=payload)
    if response.status_code == 200:
        response_text = response.text
        start_index = response_text.find("<SUCCESS>") + 9
        end_index = response_text.find("</SUCCESS>")
        session_id = response_text[start_index:end_index]
        return session_id
    else:
        raise Exception(f"Login failed. Status Code: {response.status_code}, Response: {response.text}")

# Update user parameters
def update_user_params(session_id):
    url = f"{PARAM_UPDATE_URL}?{urlencode({'folderId': folder_id, 'datasetId': dataset_id})}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "sessionid": session_id
    }
    # Format the payload for x-www-form-urlencoded
    payload = {
        "userParameters": f'[{{"name": "{param_name}", "value": "{param_value}"}}]'
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to update user parameters. Status Code: {response.status_code}, Response: {response.text}")

# Process model
def process_model(session_id):
    url = f"{PROCESS_MODEL_URL}?smodelId={smodel_id}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "sessionid": session_id,
        "smodelName": smodel_name
    }
    payload = {
        "jobType": "FULL"
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to process model. Status Code: {response.status_code}, Response: {response.text}")

# Step 4: Get job status
def get_job_status(session_id):
    url = f"{JOB_STATUS_URL}?{urlencode({'smodelId': smodel_id, 'smodelName': smodel_name})}"
    headers = {
        "Accept": "application/xml",
        "sessionId": session_id
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to get job status. Status Code: {response.status_code}, Response: {response.text}")

# Main workflow
def main():
    try:

        session_id = login()
        print("Logged in successfully. Session ID:", session_id)


        update_user_params(session_id)
        print("User parameters updated successfully.")


        process_model(session_id)
        print("Model processing started.")


        job_status = get_job_status(session_id)
        print("Job Status:", job_status)

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()