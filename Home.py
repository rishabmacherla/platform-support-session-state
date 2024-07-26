import streamlit as st
import components.authenticate as authenticate
from getmac import get_mac_address as gma
import random
import time
import uuid

# Generate a timestamp-based I
st.set_page_config(
    page_title="Home",
    page_icon="👋",
)
st.title(uuid.UUID(int=uuid.getnode()))
st.write("# Welcome to Streamlit! 👋")
st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)
# Check authentication when user lands on the home page.
cur_sys_id = uuid.UUID(int=uuid.getnode())
st.title(uuid.uuid4())
user_det, info = authenticate.get_token_group_info(cur_sys_id)

# Add login/logout buttons
# print("session state when in home.py",st.session_state)
#
check = False
for i in user_det:
    user_sys_id = user_det[i]['user_system_id']
    if user_det[i]['auth_code'] == info['auth_code'] and user_sys_id == uuid.UUID(int=uuid.getnode()):
        check = True
        st.write("THis is home.py print")
        st.write(user_det)
        user_group = user_det[i]['user_groups']
        access_token = user_det[i]['access_token']
        auth_code = user_det[i]['auth_code']

        res = authenticate.set_st_state_vars(access_token, auth_code, user_group)

        if res["authenticated"]:
            authenticate.button_logout()
        else:
            authenticate.button_login()
        break
if not(check):
    st.error("Please login again")
    authenticate.button_login()
