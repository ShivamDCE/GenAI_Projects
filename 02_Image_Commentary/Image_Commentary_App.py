import streamlit as st
import openai 
from dotenv import load_dotenv
import os
from groq import Groq

# Set page config
st.set_page_config(
    page_title="Image Analysis with AI",
    page_icon="🖼️",
    layout="centered"
)

# Add title and description
st.title("AI Image Analysis")
st.markdown("Upload an image or provide an image URL to get AI-generated commentary.")

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Create input field for image URL
image_url = st.text_input("Enter Image URL", "https://static.seekingalpha.com/uploads/2016/1/19/saupload_fredgraph.jpg")

# Add a file uploader
uploaded_file = st.file_uploader("Or upload an image", type=["jpg", "jpeg", "png"])

# Add a button to trigger analysis
if st.button("Analyze Image"):
    try:
        # Show loading spinner
        with st.spinner("Analyzing image..."):
            # Create the completion request
            completion = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Write a detailed commentary on the trend observed in the image?"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": current_image_url
                                }
                            }
                        ]
                    }
                ],
                temperature=1,
                max_completion_tokens=300,
                top_p=1,
                stream=False,
                stop=None,
            )

            # Display the image
            st.image(image_url, caption="Analyzed Image", use_column_width=True)
            
            # Display the analysis
            st.subheader("AI Analysis")
            st.write(completion.choices[0].message.content)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add footer
st.markdown("---")
st.markdown("Built with Streamlit and Groq AI")