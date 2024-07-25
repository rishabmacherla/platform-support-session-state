import streamlit as st
from dotenv import load_dotenv
import os
import boto3
from botocore.exceptions import ClientError
import hashlib
import hmac
import base64
# from authenticate import get_auth_code, get_user_tokens

load_dotenv()
COGNITO_DOMAIN = os.environ.get("COGNITO_DOMAIN")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
APP_URI = os.environ.get("APP_URI")


def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def add_user_to_cognito(name, user_name, user_email, temp_password):
    my_user = boto3.client('cognito-idp')
    try:
        response = my_user.admin_create_user(
            UserPoolId=os.environ.get("USER_POOL_ID"),
            Username=user_name,
            UserAttributes=[
                {
                    'Name' : "name",
                    'Value' : name
                },
                {
                    'Name' : 'email',
                    'Value' : user_email
                },
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                }
            ],
            ValidationData=[
                {
                    'Name' : 'email',
                    'Value' : user_email
                },
                {
                    'Name' : 'custom:username',
                    'Value' : user_name
                }
            ],
            TemporaryPassword=temp_password,
            ForceAliasCreation=True,
            # MessageAction='RESEND',
            DesiredDeliveryMediums=[
                'EMAIL',
            ]
        )
        # auth_code = get_auth_code()
        # print(auth_code)
        # access_token = get_user_tokens(auth_code)
        # print(access_token)
        # res = my_user.set_user_mfa_preference(
        #     AccessToken = access_token[1],
        #     SoftwareTokenMfaSettings = {
        #         "Enabled": True,
        #         "PreferredMfa": True
        #     }
        # )

        st.success("User Successfully Created")
        add_user_to_group(user_name, group)
        return response
    except my_user.exceptions.UsernameExistsException as e:
        return {"error": False,
                "success": True,
                "message": "This username already exists",
                "data": None}
    except my_user.exceptions.InvalidPasswordException as e:
        return {"error": False,
                "success": True,
                "message": "Password should have Caps,\
                                      Special chars, Numbers",
                "data": None}
    except my_user.exceptions.UserLambdaValidationException as e:
        return {"error": False,
                "success": True,
                "message": "Email already exists",
                "data": None}
    except Exception as e:
        return {"error": False,
                "success": True,
                "message": str(e),
                "data": None}


def add_user_to_group(user_name, group):
    my_user = boto3.client('cognito-idp')

    user_pool_id = os.environ.get("USER_POOL_ID")
    group_name = group

    try:
        my_user.get_group(
            UserPoolId=user_pool_id,
            GroupName=group_name
        )
        response = my_user.admin_add_user_to_group(
            UserPoolId=user_pool_id,
            Username=user_name,
            GroupName=group_name)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Exception('Error')
        else:
            st.success("User Successfully added to Group.")

    except ClientError as e:
        if e.response['Error']['Code'] == "ResourceNotFoundException":
            st.error("""Sorry! You don't have a group with the specified Group Name. 
                     Please make sure you provide a valid group name to add the user to.
                     """)


st.subheader("Create User and add User to a Specified Group in Cognito")

with st.form("my_form"):
    name = st.text_input(label="**Name of the user you want to add**")
    user_name = st.text_input(label="**User Name**")
    user_email = st.text_input(label="**User Email**")
    temp_password = st.text_input(label="**Temporary Password**", type="password")
    group = st.text_input(label="**Group to which user should be added**")

    add = st.form_submit_button(label="**Add a User**", type="primary")

if add:
    if name and user_name and temp_password and group and user_email:
        if "@gmail.com" in user_email:
            signup_output = add_user_to_cognito(name, user_name, user_email, temp_password)
            st.success(signup_output)
        else:
            st.error("Please make sure you enter a valid Gallup Mail Address")
    else:
        st.error("Please make sure all the details are filled.")