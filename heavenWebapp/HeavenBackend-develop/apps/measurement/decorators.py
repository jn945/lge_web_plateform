from functools import wraps

from rest_framework.exceptions import PermissionDenied


def check_user_group():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            user_dict = {"requester": [0, 1, 3], "responder": [2, 3]}
            user = request.user
            result = request.data["result"]
            for group_name in user_dict:
                if (
                    user.groups.filter(code=group_name).exists()
                    and int(result) in user_dict[group_name]
                ):
                    return view_func(self, request, *args, **kwargs)
            raise PermissionDenied("You do not have permission to perform this action.")

        return wrapper

    return decorator
