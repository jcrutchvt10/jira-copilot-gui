
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

# Set the title of the Streamlit app
st.title("Copilot GUI for Jira Cloud")

# Input fields for Jira credentials and JQL query
email = st.text_input("Email")
api_token = st.text_input("API Token", type="password")
jql_query = st.text_input("JQL Query", value="project = ANF ORDER BY created DESC")

# Button to fetch issues
if st.button("Fetch Issues"):
    if not email or not api_token or not jql_query:
        st.error("Please fill in all fields.")
    else:
        # Jira Cloud API endpoint using the new /search/jql POST endpoint
        url = "https://anfcorp.atlassian.net/rest/api/3/search/"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "query": jql_query,
            "fields": ["key", "summary", "status"]
        }

        # Make the POST request to the Jira API
        response = requests.post(url, headers=headers, json=payload, auth=HTTPBasicAuth(email, api_token))

        # Handle the response
        if response.status_code == 200:
            data = response.json()
            issues = data.get("issues", [])
            if issues:
                # Extract relevant fields and display in a table
                rows = []
                for issue in issues:
                    key = issue.get("key", "")
                    summary = issue.get("fields", {}).get("summary", "")
                    status = issue.get("fields", {}).get("status", {}).get("name", "")
                    rows.append({"Key": key, "Summary": summary, "Status": status})
                df = pd.DataFrame(rows)
                st.dataframe(df)
            else:
                st.info("No issues found for the given JQL query.")
        else:
            st.error(f"Failed to fetch issues: {response.status_code} - {response.text}")
