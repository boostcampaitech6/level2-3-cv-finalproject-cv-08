#######################CRUD#######################
# create code
create_01_success = "create success"
create_02_fail = "create fail"

# read code
read_01_success = "read success"
read_02_fail = "read fail"

# update code
update_01_success = "update success"
update_02_fail = "update fail"

# delete code
delete_01_success = "delete success"
delete_02_fail = "delete fail"

#######################ERROR#######################
# token error code
token_error = {"code": "TK02", "message": "Invalid token or can't find user. Please check the token"}

# field error code
field_error = "Can't find field: "

# enum class error code
enum_class_error = "Can't find enum class element: "

# _id error code
id_error = "Can't find _id or invalid _id: "

# celery error code
celery_error = "Already processed"

#######################AI#######################
# push celery code
celery_push_01_success = "celery push success"
celery_push_02_fail = "celery push fail"

# read code
read_celery_status_01_success = "read celery status success"
read_celery_status_02_fail = "read celery status fail"

######################USER######################
# email validation code
user_email_validation_01_success = "user email validation success"
user_email_validation_02_fail = "user email validation fail"
user_email_validation_03_already = "This email is already exist"

# signup code
user_signup_01_success = "user signup success"
user_signup_02_fail = "user signup fail"

# auth code
user_auth_01_success = "user auth success"
user_auth_02_notmatch = "user auth notmatch"
user_auth_03_fail = "user auth fail"

# find email code
user_email_find_01_success = "user email find success"
user_email_find_02_fail = "user email find fail"

# password validation code
user_password_validation_01_success = "user password validation success"
user_password_validation_02_fail = "user password validation fail"

# replace password code
user_password_replace_01_success = "user password replace success"
user_password_replace_02_fail = "user password replace fail"

# delete user code
user_delete_01_success = "user delete success"
user_delete_01_fail = "user delete fail"
