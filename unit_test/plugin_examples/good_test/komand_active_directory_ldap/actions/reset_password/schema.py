# GENERATED BY KOMAND SDK - DO NOT EDIT
import komand
import json


class Component:
    DESCRIPTION = "Reset a users password"


class Input:
    DISTINGUISHED_NAME = "distinguished_name"
    NEW_PASSWORD = "new_password"
    

class Output:
    SUCCESS = "success"
    

class ResetPasswordInput(komand.Input):
    schema = json.loads("""
   {
  "type": "object",
  "title": "Variables",
  "properties": {
    "distinguished_name": {
      "type": "string",
      "title": "Distinguished Name",
      "description": "The distinguished name of the user whose membership will be modified e.g. CN=user,OU=domain_users,DC=mydomain,DC=com",
      "order": 1
    },
    "new_password": {
      "type": "string",
      "title": "New Password",
      "displayType": "password",
      "description": "The new password",
      "format": "password",
      "order": 2
    }
  },
  "required": [
    "distinguished_name",
    "new_password"
  ]
}
    """)

    def __init__(self):
        super(self.__class__, self).__init__(self.schema)


class ResetPasswordOutput(komand.Output):
    schema = json.loads("""
   {
  "type": "object",
  "title": "Variables",
  "properties": {
    "success": {
      "type": "boolean",
      "title": "Success",
      "description": "Operation status",
      "order": 1
    }
  }
}
    """)

    def __init__(self):
        super(self.__class__, self).__init__(self.schema)
