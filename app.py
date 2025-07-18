# app.py
import streamlit as st
import requests

st.set_page_config(page_title="Shopify Insights Fetcher", layout="centered")

st.title(" Shopify Store Insights")
st.write("Enter a Shopify store URL to extract insights.")

# Input field
url = st.text_input("Shopify Store URL", placeholder="https://yourstore.myshopify.com")

# When button is clicked
if st.button("Fetch Insights"):
    if not url.strip():
        st.warning("Please enter a valid URL.")
    else:
        with st.spinner("Fetching insights..."):
            try:
                response = requests.post("http://127.0.0.1:8000/api/fetch-insights", json={"url": url})
                data = response.json()

                if data.get("status") == "success":
                    st.success("Insights fetched successfully!")

                    st.subheader("Brand:")
                    st.write(data["data"]["brand"])

                    st.subheader("🛒 Products:")
                    for p in data["data"]["products"]:
                        st.markdown(f"- {p}")

                    st.subheader("FAQs:")
                    for f in data["data"]["faqs"]:
                        st.markdown(f"- {f}")

                else:
                    st.error(f"Error: {data.get('message')}")

            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
