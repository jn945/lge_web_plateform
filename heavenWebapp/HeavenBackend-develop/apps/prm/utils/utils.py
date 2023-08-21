from datetime import datetime

from apps.prm.models import PlanSeries
from apps.prm.serializers import PlanSeriesSerializer


def combine(self, serializer):
    plan_series = PlanSeries.objects.filter(plan_id=self.kwargs["plan_id"])
    plan_series_serializer = PlanSeriesSerializer(plan_series, many=True)
    response_data = {
        "datetime": datetime.now(),
        "message": "OK",
        "data": {"series": plan_series_serializer.data, "table": serializer.data},
    }
    return response_data
