import streamlit as st
import components.authenticate as authenticate
import uuid

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)
res = {}
user_det, info = authenticate.get_token_group_info()
check = False
for i in user_det:
    user_sys_id = user_det[i]['user_system_id']
    if user_det[i]['auth_code'] == info['auth_code'] and user_sys_id == uuid.UUID(int=uuid.getnode()):
        check = True
        user_group = user_det[i]['user_groups']
        access_token = user_det[i]['access_token']
        auth_code = user_det[i]['auth_code']
        res = authenticate.set_st_state_vars(access_token, auth_code, user_group)

        if res["authenticated"]:
            authenticate.button_logout()
        else:
            authenticate.button_login()


        if (
            res["authenticated"]
            and "group2" in res["user_cognito_groups"]
        ):
            st.write("# Welcome to Streamlit! 👋")
            st.markdown(
                """
                Page 3
            """
            )
        else:
            if res['authenticated']:
                st.error("You don't have access.")
            else:
                st.error("Please login!")
if not(check):
    st.error("Please login again")
    authenticate.button_login()