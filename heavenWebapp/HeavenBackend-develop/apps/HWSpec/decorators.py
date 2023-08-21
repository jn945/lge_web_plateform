from functools import wraps

from .models import Power, Soc
from .serializers import PowerSerializer, SocSerializer


def switch_model_based_on_category():
    category_field_name = "category"
    model_mapping = {
        "soc": (Soc, SocSerializer),
        "power": (Power, PowerSerializer),
    }

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            category = request.query_params.get(category_field_name)
            if category and category in model_mapping:
                model_class, serializer_class = model_mapping[category]
                self.queryset = model_class.objects.all()
                self.serializer_class = serializer_class
            return view_func(self, request, *args, **kwargs)

        return wrapper

    return decorator
