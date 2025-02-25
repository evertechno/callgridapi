import streamlit as st
import requests
import json

# URL for the API
API_URL = "https://gridapi.onrender.com/generate"

def generate_content(prompt):
    """Function to interact with the API and generate content."""
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"prompt": prompt})

    try:
        # Send a POST request to the API
        response = requests.post(API_URL, headers=headers, data=data)
        response.raise_for_status()

        # Parse response JSON
        result = response.json()

        return result

    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the API: {e}")
        return None

# Streamlit UI
st.title("Content Generation with AI")
st.write("Enter a prompt below to generate content and check for originality.")

# User input prompt
prompt = st.text_area("Prompt", "", height=200)

if st.button("Generate Content"):
    if prompt.strip():
        # Call the API to generate content
        result = generate_content(prompt.strip())

        if result:
            st.subheader("Generated Content:")
            st.write(result["generated_content"])

            if "similar_content" in result and result["similar_content"]:
                st.subheader("Similar Content Found:")
                for item in result["similar_content"]:
                    st.write(f"**Title:** {item['title']}")
                    st.write(f"**Link:** {item['link']}")
                    st.write(f"**Snippet:** {item['snippet']}")
                    st.write("---")
            
            if "regenerated_content" in result and result["regenerated_content"]:
                st.subheader("Regenerated Content for Originality:")
                st.write(result["regenerated_content"])

            if "message" in result:
                st.write(result["message"])
    
    else:
        st.error("Please enter a prompt before generating content.")
