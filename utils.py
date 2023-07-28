import requests
from requests.adapters import HTTPAdapter
from streamlit.connections import ExperimentalBaseConnection

class MEME_APIConnection(ExperimentalBaseConnection[requests.Session]):
    """Basic st.experimental_connection implementation for NASA API"""

    def __init__(self, connection_name: str):

        self._connect()

        response = requests.get("https://api.imgflip.com/get_memes")
        response.raise_for_status()
        data = response.json()
        self.meme_data = []

        all_meme_data = data['data']['memes']
        for meme in all_meme_data:
            if(meme['box_count'] <= 2):
                self.meme_data.append(meme)

        self.names = [meme['name'] for meme in self.meme_data]
        self.images = [{'name' : meme['name'], 'url' : meme['url']} for meme in self.meme_data]

        super().__init__(connection_name)

    def _connect(self) -> requests.Session:
        """Connects to the Session

        :returns: requests.Session
        """
        session = requests.Session()
        session.mount("https://", HTTPAdapter(max_retries=5))
        return session

    def query_meme(self, name):
        return next((meme for meme in self.meme_data if meme['name'] == name), None)


    def create_meme(self, id, upper_text, lower_text):
        
        post_url = "https://api.imgflip.com/caption_image"
        payload = {
            "template_id": id,
            "text0": upper_text,
            "text1": lower_text,
            "username": "temp_st",
            "password": "dummy@12345",
        }

        response = requests.post(post_url, data=payload)

        data = response.json()
        print(data)
        if data["success"]:
            return data["data"]["url"]
        else:
            return "https://www.freecodecamp.org/news/content/images/2021/03/ykhg3yuzq8931--1-.png"
