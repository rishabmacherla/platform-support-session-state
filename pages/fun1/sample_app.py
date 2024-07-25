# import streamlit as st
#
# lis = ["my_page.py","page1.py","page2.py"]
# text = st.text_input("utils")
# lis1 = []
# for i in lis:
#     if text in i:
#         lis1.append(i)
# val = st.radio("hi", options = lis1)
# print(val)
# if val == "page2.py":
#     st.switch_page(f"pages/fun1/{lis[0]}")
# # if val == "my_page.py":
# #     st.switch_page(f"pages/{lis[0]}")

import streamlit as st

def page2():
    st.title("Second page")

pg = st.navigation([
    st.Page("my_page.py", title="First page", url_path="my_page.py", icon="🔥", default=False)
    # st.Page(page2, title="Second page", icon=":material/favorite:"),
])
pg.run()