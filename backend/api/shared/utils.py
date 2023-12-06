import json
from typing import Union, Any
from flask import Response, request

from core.shared.models import User, Session


def session_data_dict(user: User,
                      session: Session) -> dict[str, Union[int, str, None]]:

    return {
        "sessionId": session.session_id,
        "userId": user.user_id,
        "username": user.username,
        "firstName": user.first_name,
        "lastName": user.last_name,
    }


def camelcase(s):
    if type(s) is str:
        parts = iter(s.split("_"))
        return next(parts) + "".join(i.title() for i in parts)
    else:
        return s


def dict_to_camel(source: dict, return_copy: bool = True):
    new_dict: dict = {}

    if return_copy:
        for key in source:
            new_key = camelcase(key)
            new_dict[new_key] = item_to_camel(source[key], return_copy=True)
    else:
        new_dict = source
        old_keys = []

        for key in source:
            old_keys.append(key)

        for key in old_keys:
            new_key = camelcase(key)
            item_to_camel(source["key"], return_copy=False)
            if new_key != key:
                source[new_key] = source.pop(key)

    return new_dict


def item_to_camel(source, return_copy: bool = True):
    if issubclass(type(source), dict):
        return dict_to_camel(source, return_copy=return_copy)
    elif issubclass(type(source), list):
        if return_copy:
            new_list = []
            for item in source:
                new_list.append(item_to_camel(item, return_copy=return_copy))
            return new_list
        else:
            for item in source:
                item_to_camel(item, return_copy=False)
            return source

    else:
        return source


def success_response(data: Union[dict, None] = None,
                     convert_keys_to_camel=False) -> Response:

    body: dict[str, Any] = {"result": "success"}
    if data is not None:
        if convert_keys_to_camel:
            body["data"] = item_to_camel(data)
        else:
            body["data"] = data

    return Response(response=json.dumps(body), status=200,
                    content_type="application/json")


def error_reponse(e: Exception) -> Response:
    body: dict[str, str] = {
        "result": "error",
        "error": str(e.args[0]) if len(e.args) > 0 else "Unknown"
    }

    return Response(response=json.dumps(body), status=400,
                    content_type="application/json")


def get_session_token() -> str:
    token = request.cookies.get("sessionToken")

    if not token:
        raise Exception("Session token not found or empty")

    return token
