---
title: Authorization
description: Authentication and authorization mechanisms in istSOS4 SensorThingsAPI implementation
icon: lucide/key
---

## OpenAPI and Authorization
OpenAPI is a specification for building APIs that includes support for defining security schemes and requirements. In our implementation, we have defined an OAuth2 security scheme in the OpenAPI documentation, which allows us to specify the [authentication](../concepts/authentication.md) mechanism for our API endpoints.

Navigate to the interactive documentation at: `/docs` <http://localhost:8018/v4/v1.1/docs> or <https://istsos.org/v4/v1.1/docs> and check the top-right corner of the page.

You will see something like this:

![Authorization Button Screenshot"](../images/authorization1.png)

!!! note "Authorize buttons"
    You have a shiny "Authorize" button on top of the page to set the whole API access.<br>
    Additionally, your path operation has a specific little lock in the top-right corner that you can click.


And if you click it, you have a little authorization form to type a <code>username</code> and <code>password</code> (and other optional fields):

![Login form](../images/authorization2.png)


## istSOS4 Roles and Permissions
In istSOS4 users have specific roles which define their access permissions.  
Permissions are managed trough database privileges to access specific entity of the Sensorthings schema.  
Therefore each role has a set of privileges that define the level of access granted to specific entity in the system.  
The following table outlines the different defined roles and their corresponding permissions.  


| Role          | Description                                          | Entity Permissions                                                                                                                                                                            |
| ------------- | ---------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `admin`       | Have all the privileges                              | All `PRIVILEGES` on all entity of sensorthings schema                                                                                                                                        |
| `viewer`      | Only view capabilities                               | `SELECT` privilege on all entity                                                                                                                                                             |
| `editor`      | Can do everything except defining users            | `SELECT` privilege on all entity<br>`INSERT`, `UPDATE`, `DELETE` privileges on all entity (except User element)                                                                                |
| `obs_manager` | Can view everything and manage observations          | `SELECT` privilege on all entity<br>`INSERT`, `UPDATE`, `DELETE` privileges on Observation element<br>`INSERT` privilege on FeaturesOfInterest element<br>`UPDATE` privilege on Datastream element |
| `sensor`      | Can view everything and only insert new observations | `SELECT` privilege on all entity<br>`INSERT` privilege on Observation and FeaturesOfInterest elements<br>`UPDATE` privilege on Datastream element                                                |

## Creating Users and Assigning Roles
To create users and assign roles in istSOS4, you can use the swagger interface to access the API provided by the system. This interface allows you to manage users, assign them specific roles, and control their access permissions.

The **User** entity is defined as follows:

| Properties | Type | Multiplicity and use | Description |
| ---------- | ---- | -------------------- | ----------- |
| username   | string(128) | One (mandatory) | The username of the user. |
| contact    | json        | One (optional)  | The json that describe the contact information including email, phone, and address. |
| uri        | URI         | One (mandatory) | The URI that identifies the user (for researcher is ORCID). |
| role       | string(128) | One (mandatory) | The role of the user. |

### :lucide-play: Login as admin
To create new users, you need to log in as an admin user. The admin user has full access to the system and can manage users and their roles. By default, the admin user is created with the following credentials:

- **username**: admin
- **password**: admin

After authenticating in the system, you will see it like:

![Create Things](../images/authorization3.png)

### :lucide-play: Create a viewer and an editor
Once you are logged in as an admin, you can create new users and assign them specific roles. 

To create a new user, you can send a POST request to the `/Users` endpoint with the following JSON body:

```json
  {
    "username": "name_of_user",
    "password": "password_of_user",
    "uri": "https://orcid.org/0000-0004-3456-7890",
    "role": "role_of_user",
    "contact": {
      "email": "jhon.smith@example.com",
      "phone": "+1234567890",
      "address": "123 Main Street, Brussels, Belgium"
    }
  }
```

Using the swagger interface, you can create:

- a user with the username "editor1/editor1" and assign them the "editor" role, which allows them to manage data but not create new users.
- a user with the username "viewer1/viewer1" and assign them the "viewer" role, which allows them to only view data without making any changes.

![Create User](../images/auth_create_editor.png)

### :lucide-play: Create the viewer and editor policies

Once the `editor1` and `viewer1` users have been created, you can assign them access policies.

A policy defines which users can access a specific resource and what level of permissions they have on it.

To create a new policy, send a POST request to the `/Policies` endpoint with the following JSON body.

For the editor user:

```json
{
  "users": [
    "editor1"
  ],
  "name": "workshop",
  "permissions": {
    "type": "editor"
  }
}
```

![Create User](../images/auth_create_editor_policy.png)


### :lucide-play: Test the authorization
Now that you have created new users with specific roles, you can test the authorization by logging in with those users and trying to perform actions that are restricted based on their roles.

Now logout from the admin account, login as a Viewer and try to create a Thing!

!!! remember
    To create an Element you need to execute a POST request with the appropriate body that represents the element you want to create.

![Login successfull](../images/authorization3b.png)

Since you're logged in as a Viewer, you do not have the necessary privileges to create a Thing. You should therefore see the following error message:

```json
{
  "code": 401,
  "type": "error",
  "message": "Insufficient privileges."
}
```