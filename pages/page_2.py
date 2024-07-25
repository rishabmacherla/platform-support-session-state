import streamlit as st
import pandas as pd
import pydeck as pdk
import uuid
from urllib.error import URLError
import components.authenticate as authenticate
import random
# Page configuration
st.set_page_config(page_title="Mapping Demo", page_icon="🌍")
# Check authentication

res = {}
cur_sys_id = uuid.UUID(int=uuid.getnode())
user_det, info = authenticate.get_token_group_info(cur_sys_id)
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



        # Rest of the page

        if (
            res["authenticated"]
            and "group2" in res["user_cognito_groups"]
        ):
            st.markdown("# Mapping Demo")
            st.sidebar.header("Mapping Demo")
            st.write(
                """This demo shows how to use
            [`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
            to display geospatial data."""
            )
            @st.cache_data
            def from_data_file(filename):
                url = (
                    "http://raw.githubusercontent.com/streamlit/"
                    "example-data/master/hello/v1/%s" % filename
                )
                return pd.read_json(url)
            try:
                    ALL_LAYERS = {
                        "Bike Rentals": pdk.Layer(
                            "HexagonLayer",
                            data=from_data_file("bike_rental_stats.json"),
                            get_position=["lon", "lat"],
                            radius=200,
                            elevation_scale=4,
                            elevation_range=[0, 1000],
                            extruded=True,
                        ),
                        "Bart Stop Exits": pdk.Layer(
                            "ScatterplotLayer",
                            data=from_data_file("bart_stop_stats.json"),
                            get_position=["lon", "lat"],
                            get_color=[200, 30, 0, 160],
                            get_radius="[exits]",
                            radius_scale=0.05,
                        ),
                        "Bart Stop Names": pdk.Layer(
                            "TextLayer",
                            data=from_data_file("bart_stop_stats.json"),
                            get_position=["lon", "lat"],
                            get_text="name",
                            get_color=[0, 0, 0, 200],
                            get_size=15,
                            get_alignment_baseline="'bottom'",
                        ),
                        "Outbound Flow": pdk.Layer(
                            "ArcLayer",
                            data=from_data_file("bart_path_stats.json"),
                            get_source_position=["lon", "lat"],
                            get_target_position=["lon2", "lat2"],
                            get_source_color=[200, 30, 0, 160],
                            get_target_color=[200, 30, 0, 160],
                            auto_highlight=True,
                            width_scale=0.0001,
                            get_width="outbound",
                            width_min_pixels=3,
                            width_max_pixels=30,
                        ),
                    }
                    st.sidebar.markdown("### Map Layers")
                    selected_layers = [
                        layer
                        for layer_name, layer in ALL_LAYERS.items()
                        if st.sidebar.checkbox(layer_name, True)
                    ]
                    if selected_layers:
                        st.pydeck_chart(
                            pdk.Deck(
                                map_style="mapbox://styles/mapbox/light-v9",
                                initial_view_state={
                                    "latitude": 37.76,
                                    "longitude": -122.4,
                                    "zoom": 11,
                                    "pitch": 50,
                                },
                                layers=selected_layers,
                            )
                        )
                    else:
                        st.error("Please choose at least one layer above.")
            except URLError as e:
                st.error(
                        """
                        **This demo requires internet access.**
                        Connection error: %s
                    """
                        % e.reason
                )
        else:
            if res["authenticated"]:
                st.write("You do not have access. Please contact the administrator.")
            else:
                st.write("Please login!")

    #
if not(check):
    st.error("Please login again")
    authenticate.button_login()