# API

## FORUM

- (GET) /forum

    show forum page.
---
- (GET) /get_forum_data
    > return

    e.g.
    ```
    {
      "content": [
        {
          "comment": "hello",
          "id": 3,
          "time": "Tue, 14 Apr 2020 17:18:36 GMT",
          "user_email": "test@test",
          "user_id": 1,
          "user_name": "test"
        },
        {
          "comment": "testtest",
          "id": 2,
          "time": "Tue, 14 Apr 2020 17:07:13 GMT",
          "user_email": "test@test",
          "user_id": 1,
          "user_name": "test"
        },
        {
          "comment": "testtest",
          "id": 1,
          "time": "Tue, 14 Apr 2020 17:06:46 GMT",
          "user_email": "test@test",
          "user_id": 1,
          "user_name": "test"
        }
      ],
      "count": 3
    }
    ```
---
- (POST) /comment

    > payload
    
    | name | data type | description |
    | ------ | ------ | ------ |
    | comment | text | comment |
    | video_id | int | video id |
    | tag | list(string) | tags |

    e.g.
    ```
    {
      "comment": "testtest",
      "video_id": 233,
      "tag": ["taiwan", "car"]
    }
    ```
    
    redirect to `$SERVER:/forum`
    

## USER AUTHENTICATION

- (GET) /login

    show login page.
---
- (POST) /login
    > payload

    | name | data type | description |
    | ------ | ------ | ------ |
    | email | string | account email |
    | password | string | password |
    
    e.g.
    ```
    {
      "email": "test@test",
      "password": "test"
    }
    ```
    redirect to `$SERVER:/`
---
- (GET) /singup

    show singup page.
---
- (POST) /singup
    > payload

    | name | data type | description |
    | ------ | ------ | ------ |
    | email | string | account email |
    | password | string | password |
    | name | string | user name |
    | student_id | int | student id |
    ...

    redirect to `$SERVER:/login`

