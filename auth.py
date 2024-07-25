import boto3


# to get username for each group
my_client = boto3.client('iam')
# iam = boto3.resource('iam')
# print(iam.list_profiles())
response = my_client.list_groups()
for group in response['Groups']:
    group_details = my_client.get_group(GroupName=group['GroupName'])
    print(group_details)
    for user in group_details['Users']:
        print(" - ", user['UserName'])


# to get users of a specific groups and verify them with the username provided by the signup page

# username_from_signup_page = "rishabmacherla"
# success = False
#
# for user in my_client.get_group(GroupName = "aws_prep_group"):
#     if username_from_signup_page == user:
#         success = True
# if not success:
#     return "return with some error message"
# else:
#     return "with some success message"
#
# users = my_client.list_users()["Users"]
# # if "rishabmacherla" in users['Username']
# print(users)

# print(list(my_client.users.all()))