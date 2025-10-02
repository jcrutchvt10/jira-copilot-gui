import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

# Set page configuration
st.set_page_config(page_title="Jira Copilot GUI", layout="wide")

# Title of the app
st.title("🧠 Copilot GUI for Jira Cloud")

# Sidebar inputs
st.sidebar.header("🔐 Jira Credentials")
email = st.sidebar.text_input("Email", placeholder="your.email@anfcorp.com")
api_token = st.sidebar.text_input("API Token", type="password", placeholder="Your Jira API token")

st.sidebar.header("🔍 JQL Query")
jql_query = st.sidebar.text_input("Enter JQL", placeholder="e.g. project = ABC ORDER BY created DESC")

# Main section
if st.sidebar.button("Fetch Issues"):
    if not email or not api_token or not jql_query:
        st.error("Please fill in all fields to proceed.")
    else:
        with st.spinner("Fetching issues from Jira..."):
            url = "https://anfcorp.atlassian.com/rest/api/3/search"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            params = {
                "jql": jql_query,
                "fields": "key,summary,status"
            }

            response = requests.get(url, headers=headers, params=params, auth=HTTPBasicAuth(email, api_token))

            if response.status_code == 200:
                data = response.json()
                issues = data.get("issues", [])
                if issues:
                    st.success(f"Fetched {len(issues)} issues.")
                    table_data = []
                    for issue in issues:
                        key = issue["key"]
                        summary = issue["fields"]["summary"]
                        status = issue["fields"]["status"]["name"]
                        table_data.append({"Key": key, "Summary": summary, "Status": status})
                    st.dataframe(table_data)
                else:
                    st.warning("No issues found for the given JQL query.")
            else:
                st.error(f"Failed to fetch issues. Status code: {response.status_code}")
                st.json(response.json())
