import streamlit as st
import time
import numpy as np
import components.authenticate as authenticate
import uuid
import random
# Page configuration
st.set_page_config(page_title="Plotting Demo", page_icon="📈")
# Check authentication

res = {}
cur_sys_id = uuid.UUID(int=uuid.getnode())
user_det, info = authenticate.get_token_group_info(cur_sys_id)
check = False
for i in user_det:
    user_sys_id = user_det[i]['user_system_id']
    if user_det[i]['auth_code'] == info['auth_code'] and user_sys_id == uuid.UUID(int=uuid.getnode()):
        # st.write("hi")
        check = True
        user_group = user_det[i]['user_groups']
        access_token = user_det[i]['access_token']
        auth_code = user_det[i]['auth_code']
        res = authenticate.set_st_state_vars(access_token, auth_code, user_group)

        if res["authenticated"]:
            authenticate.button_logout()
        else:
            authenticate.button_login()



# Add login/logout buttons

# Rest of the page

        if (
            res["authenticated"]
            and "group1" in res["user_cognito_groups"]
        ):
            st.markdown("# Plotting Demo")
            st.sidebar.header("Plotting Demo")
            st.write(
                """This demo illustrates a combination of plotting and animation with
            Streamlit. We're generating a bunch of random numbers in a loop for around
            5 seconds. Enjoy!"""
            )
            progress_bar = st.sidebar.progress(0)
            status_text = st.sidebar.empty()
            last_rows = np.random.randn(1, 1)
            chart = st.line_chart(last_rows)
            for i in range(1, 101):
                    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
                    status_text.text("%i%% Complete" % i)
                    chart.add_rows(new_rows)
                    progress_bar.progress(i)
                    last_rows = new_rows
                    time.sleep(0.05)
            progress_bar.empty()
            # Streamlit widgets automatically run the script from top to bottom. Since
                # this button is not connected to any other logic, it just causes a plain
                # rerun.
            st.button("Re-run")
        else:
            if res["authenticated"]:
                st.write("You do not have access. Please contact the administrator.")
            else:
                st.write("Please login!")
if not(check):
    st.error("Please login again")
    authenticate.button_login()
