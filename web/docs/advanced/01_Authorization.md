# Authentication and authorization

> **Workflow position:** after `00_Introduction.ipynb`, before the SensorThings entity notebooks.  
> This notebook prepares the users and policies used by the rest of the workflow.

This notebook explains two separate concepts:

- **Authentication**: proving who the client is. In practice, the user logs in and receives an access token.
- **Authorization**: deciding what that authenticated user is allowed to do. In istSOS4, this is controlled through roles and policies.

A user account alone is not enough. The user also needs a policy that grants permissions on the API resources.

## What you will do

1. Log in as administrator.
2. Create a `viewer` user and assign a viewer policy.
3. Verify that `viewer` can read data but cannot create data.
4. Create an `editor` user and assign an editor policy.
5. Verify that `editor` can create and read data.

## Roles used in the workshop

| Role | Typical user | Main capability | Used here for |
|---|---|---|---|
| `admin` | System administrator | Full access, including user and policy management | Creating users and policies |
| `viewer` | Dashboard, public app, reporting user | Read-only access | Demonstrating limited access |
| `editor` | Data manager or workshop participant | Create and manage resources | Running notebooks `02`, `03`, and `04` |
| `sensor` | Device or ingestion process | Submit observations | Context only |
| `obs_manager` | Data quality manager | Manage and correct observations | Context only |

> Use unique usernames in a shared workshop instance. Existing users or policies may cause the API to return a conflict/error response.

### :lucide-play: Setup

Import the libraries used in this notebook and define the base URL of the istSOS4 API.

When the notebook runs inside the Jupyter Docker container, the API is reachable through the Docker service name:

```python
IST_SOS_ENDPOINT = "http://api:5000/v4/v1.1"
```


```python
import requests
from istsos_utils import (
    REQUEST_TIMEOUT,
    auth_headers,
    display_error_response,
    display_json,
    login,
)

IST_SOS_ENDPOINT = "http://api:5000/v4/v1.1"
```

### :lucide-play: Login as administrator

The administrator account is required for access-management tasks:

- creating users;
- assigning roles;
- creating policies.

The login request returns an access token. The token is passed in the `Authorization` header of the following requests.


```python
admin_username = input("Enter administrator username: ")
admin_password = input("Enter administrator password: ")

if not admin_username or not admin_password:
    print("Username or password is empty")
else:
    admin_token, login_body = login(
        IST_SOS_ENDPOINT,
        admin_username,
        admin_password,
        timeout=REQUEST_TIMEOUT,
    )

    if admin_token:
        print(f"Logged in as {admin_username}")
```

### :lucide-play: Create a `viewer` user

The administrator now creates a new user with the `viewer` role.

The `viewer` role is intended for clients that only need to consult data, such as dashboards or public applications.

> This request must use an administrator token. Normal users cannot create other users.


```python
viewer_username = input("Enter viewer username: ")
viewer_password = input("Enter viewer password: ")

if not viewer_username or not viewer_password:
    print("Username or password is empty")
else:
    viewer_user = {
        "username": viewer_username,
        "password": viewer_password,
        "role": "viewer",
    }
    
    response = requests.post(
        IST_SOS_ENDPOINT + "/Users",
        headers=auth_headers(admin_token),
        json=viewer_user,
        timeout=REQUEST_TIMEOUT,
    )
    
    if response.status_code == 201:
        print(f"{viewer_username} user created successfully")
    else:
        display_error_response(response)
```

### :lucide-play: Create a policy for the `viewer`

The policy gives the `viewer` user its actual permissions.

For this notebook, the policy grants read-only access. The next section verifies this behaviour with two requests:

- a `GET` request that should succeed;
- a `POST` request that should fail.


```python
viewer_policy = {
    "users": [viewer_username],
    "name": "workshop",
    "permissions": {"type": "viewer"},
}

response = requests.post(
    IST_SOS_ENDPOINT + "/Policies",
    headers=auth_headers(admin_token),
    json=viewer_policy,
    timeout=REQUEST_TIMEOUT,
)

if response.status_code == 201:
    print(f"Viewer policy for {viewer_username} created successfully")
else:
    display_error_response(response)
```

### :lucide-play: Login as the `viewer`

Switch from the administrator account to the new `viewer` account.

From this point on, requests use `viewer_token`, so they are evaluated with viewer permissions.


```python
viewer_username = input("Enter viewer username: ")
viewer_password = input("Enter viewer password: ")

if not viewer_username or not viewer_password:
    print("Username or password is empty")
else:
    viewer_token, login_body = login(
        IST_SOS_ENDPOINT,
        viewer_username,
        viewer_password,
        timeout=REQUEST_TIMEOUT,
    )

    if viewer_token:
        print(f"Logged in as {viewer_username}")
```

### :lucide-play: Test the `viewer` permissions

Expected behaviour:

- reading data should work;
- creating data should be rejected by the API.

#### Retrieve data as `viewer`

The `viewer` is allowed to read data, so this request should return the available `Thing` resources.


```python
response = requests.get(
    IST_SOS_ENDPOINT + "/Things",
    headers=auth_headers(viewer_token),
    timeout=REQUEST_TIMEOUT,
)

if response.status_code == 200:
    display_json(response.json())
else:
    display_error_response(response)
```

#### Try to create data as `viewer`

This request is intentionally expected to fail. It demonstrates that the `viewer` policy prevents write operations.

#### Request body: example `Thing`

A `Thing` represents an entity being observed or monitored. Here we try to create an example `Thing` for Lugano Lake while still using `viewer_token`.


```python
thing = {
    "name": "Lugano Lake",
    "description": "The Alpine lake located in Southern Switzerland",
    "properties": {
        "Max depth": "288 m",
    },
}

response = requests.post(
    IST_SOS_ENDPOINT + "/Things",
    json=thing,
    headers=auth_headers(viewer_token, "Create new thing"),
    timeout=REQUEST_TIMEOUT,
)

if response.status_code == 201:
    print(f"Thing created successfully ({response.headers['location']})")
else:
    display_error_response(response)
```

### :lucide-play: Login again as administrator

To create the `editor` user and its policy, switch back to the administrator account.


```python
admin_username = input("Enter administrator username: ")
admin_password = input("Enter administrator password: ")

if not admin_username or not admin_password:
    print("Username or password is empty")
else:
    admin_token, login_body = login(
        IST_SOS_ENDPOINT,
        admin_username,
        admin_password,
        timeout=REQUEST_TIMEOUT,
    )

    if admin_token:
        print(f"Logged in as {admin_username}")
```

### :lucide-play: Create an `editor` user

The administrator now creates a user with the `editor` role.

The `editor` role is used by the following notebooks because it can create and manage the SensorThings resources used in the workflow.


```python
editor_username = input("Enter editor username: ")
editor_password = input("Enter editor password: ")

if not editor_username or not editor_password:
    print("Username or password is empty")
else:
    editor_user = {
        "username": editor_username,
        "password": editor_password,
        "role": "editor",
    }
    
    response = requests.post(
        IST_SOS_ENDPOINT + "/Users",
        headers=auth_headers(admin_token),
        json=editor_user,
        timeout=REQUEST_TIMEOUT,
    )
    
    if response.status_code == 201:
        print(f"{editor_username} user created successfully")
    else:
        display_error_response(response)
```

### :lucide-play: Create a policy for the `editor`

The policy grants the `editor` user broader permissions than the `viewer`.

After this step, the `editor` credentials can be used in notebooks `02`, `03`, and `04`.


```python
editor_policy = {
    "users": [editor_username],
    "name": "workshop",
    "permissions": {"type": "editor"},
}

response = requests.post(
    IST_SOS_ENDPOINT + "/Policies",
    headers=auth_headers(admin_token),
    json=editor_policy,
    timeout=REQUEST_TIMEOUT,
)

if response.status_code == 201:
    print(f"Editor policy for {editor_username} created successfully")
else:
    display_error_response(response)
```

### :lucide-play: Login as the `editor`

Log in as the newly created `editor` user.

The returned `editor_token` is used to test that editor permissions are active.


```python
editor_username = input("Enter editor username: ")
editor_password = input("Enter editor password: ")

if not editor_username or not editor_password:
    print("Username or password is empty")
else:
    editor_token, login_body = login(
        IST_SOS_ENDPOINT,
        editor_username,
        editor_password,
        timeout=REQUEST_TIMEOUT,
    )

    if editor_token:
        print(f"Logged in as {editor_username}")
```

### :lucide-play: Test the `editor` permissions

Expected behaviour:

- creating new data should work;
- reading data should work.

This confirms that the `editor` user is ready for the following notebooks.

#### Create data as `editor`

Unlike the `viewer`, the `editor` is allowed to create new resources.

#### Request body: example `Thing`

This is the same Lugano Lake example used in the viewer test, but now the request uses `editor_token`.


```python
thing = {
    "name": "Lugano Lake",
    "description": "The Alpine lake located in Southern Switzerland",
    "properties": {
        "Max depth": "288 m",
    },
}

response = requests.post(
    IST_SOS_ENDPOINT + "/Things",
    json=thing,
    headers=auth_headers(editor_token, "Create new thing"),
    timeout=REQUEST_TIMEOUT,
)

if response.status_code == 201:
    print(f"Thing created successfully ({response.headers['location']})")
else:
    display_error_response(response)
```

#### Retrieve data as `editor`

The `editor` is also allowed to read data, so this request should succeed.


```python
response = requests.get(
    IST_SOS_ENDPOINT + "/Things",
    headers=auth_headers(editor_token),
    timeout=REQUEST_TIMEOUT,
)

if response.status_code == 200:
    display_json(response.json())
else:
    display_error_response(response)
```
