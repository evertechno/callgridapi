import streamlit as st
import requests
import json

# URL of the Flask API
API_URL = "https://gridapi.onrender.com/generate"

# Function to call the Flask API and retrieve generated content
def generate_content(prompt):
    """Function to interact with the Flask API and generate content."""
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"prompt": prompt})

    try:
        # Send the POST request to the API
        response = requests.post(API_URL, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        result = response.json()

        return result

    except requests.exceptions.RequestException as e:
        # Display error if API call fails
        st.error(f"Error communicating with the API: {str(e)}")
        return None

# Streamlit User Interface
st.title("AI Content Generation and Originality Check")
st.write("Enter a prompt below, and the app will generate content, check for similarities online, and provide a rewritten version if necessary.")

# User input prompt
prompt = st.text_area("Enter your prompt here:", "", height=200)

if st.button("Generate Content"):
    if prompt.strip():  # Ensure prompt is not empty
        # Call the API to generate content
        result = generate_content(prompt.strip())

        if result:
            st.subheader("Generated Content:")
            st.write(result.get("generated_content"))

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
