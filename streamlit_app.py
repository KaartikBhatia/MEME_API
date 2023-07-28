import streamlit as st
from utils import MEME_APIConnection

# Create the NASA API connection
meme_conn = st.experimental_connection("meme", type=MEME_APIConnection)

# Streamlit app
def main():
    st.title("🚀MEME API Connection with Streamlit")
    st.markdown(
    """
    This app is an official submission to the Streamlit Connections Hackathon.
     - [Hackathon Link](https://discuss.streamlit.io/t/connections-hackathon/47574)
     - [GitHub Repo](https://github.com/KaartikBhatia/MEME_API)
     - [MEME API's](https://imgflip.com/api)
    """)


    st.markdown(
        """🚀 Explore MEMES with the MEME API! 🌌
            Check out all the memes and their respective names in the sidebar.
            Then simply choose the meme name, upper text and lower text and click Generate!
        """
    )

    st.sidebar.title("Here's the list of all memes!")
    # meme_conn.images return a list of dicitonaries: [{'name': 'memename', 'url': 'url'}, {'name': 'memename', 'url': 'url'}]
    all_memes_images = meme_conn.images

    for image in all_memes_images:
        st.sidebar.image(image['url'], caption=image['name'], width=300)


    # meme_conn.names return list of all meme names
    meme_name = st.selectbox("Select a MEME name", meme_conn.names)

    # Get meme details
    meme_details = meme_conn.query_meme(meme_name)

    if meme_details:
        name = meme_details['name']
        id = meme_details['id']
        url = meme_details['url']

    # Upper Text / Lower Text 
    upper_text = st.text_input('Upper Text')
    lower_text = st.text_input('Lower Text')
    
    if(st.button("Generate MEME!")):
        if(upper_text == "" and lower_text == ""):
            image_url = meme_conn.create_meme(id, " ", " ")
            st.write(image_url)
            st.image(image_url)
        else:
            image_url = meme_conn.create_meme(id, upper_text, lower_text)
            st.write(image_url)
            st.image(image_url)

if __name__ == "__main__":
    main()
