from functools import reduce
from operator import and_

from apps.accounts.models import User
from django.contrib.auth.models import AnonymousUser
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.cache import never_cache
from drf_yasg.utils import swagger_auto_schema
from modules.common.params import CommonParams
from modules.common.utils import bulk_create
from modules.exceptions.custom_exceptions import CustomDictException
from rest_framework import exceptions, status, viewsets
from rest_framework.response import Response


class CustomViewset(viewsets.ModelViewSet):

    # AnonymousUser일 경우 creator=1 로 지정합니다
    def perform_create(self, serializer):
        if isinstance(self.request.user, AnonymousUser):
            serializer.save(creator=User.objects.get(id=1))
        else:
            serializer.save(creator=self.request.user)

    @never_cache
    def list(self, request, *args, **kwargs):
        """
        Args:
            column_name : listing 할 column name
            field_name : search 시, 검색할 column 이름
            search_query : search 시, 검색할 keyword
            fields : 특정 column 만 반환 시, 반환할 columns
        Returns:
            Response : 반환 데이터"""

        # Get query parameters
        column_name = request.query_params.get("column_name", None)
        field_name = request.query_params.get("search_field_name", None)
        search_query = request.query_params.get("keyword", None)
        fields = self.request.query_params.get("fields", None)
        filtered_data = None

        # field_name 과 search_query 를 이용해서 search 된 결과 반환
        if search_query:
            search_query = search_query.split(",")
        if field_name and search_query:
            print("execute search query")
            field_name_list = field_name.split(",")
            # field_name 이 list로 들어올 경우, 다중 field search
            if len(field_name_list) > 1:
                queries = []
                for field, word in zip(field_name_list, search_query):
                    queries.append(Q(**{field + "__icontains": word}))
                # queries 리스트의 모든 조건을 AND 연산으로 결합
                query = reduce(and_, queries)
                queryset = self.queryset.filter(query)
            # field_name 이 list로 들어올 경우, 다중 keyword search
            else:
                query = Q()  # 빈 Q 객체 생성
                for word in search_query:
                    query |= Q(**{field_name + "__icontains": word})
            queryset = self.queryset.filter(query)
            if field_name == "year":
                queryset = queryset.order_by("year")
        else:
            # field_name 과 search_query 가 주어지지 않았다면 일반 결과 반환
            print("execute normal query")
            queryset = self.filter_queryset(self.get_queryset())

        # 특정 column 만 반환 시, 반환할 columns 만 반환
        if fields:
            fields = fields.split(",")
            queryset = queryset.values(*fields)
            if "year" in fields:
                queryset.values(*fields)
            response_data = {
                "datetime": timezone.now(),
                "message": "OK",
                "data": queryset,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        #  listing : 중복을 제거하여 반환
        if column_name:
            queryset = list(set(queryset.values_list(column_name, flat=True)))
            if column_name == "year":
                queryset = sorted(queryset, reverse=True)
            response_data = {
                "datetime": timezone.now(),
                "message": "OK",
                "data": queryset,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        # 데이터 직렬화
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        if filtered_data:
            response_data = {
                "datetime": timezone.now(),
                "message": "OK",
                "data": filtered_data,
            }
        else:
            print("else")
            print(serializer)
            response_data = {
                "datetime": timezone.now(),
                "message": "OK",
                "data": serializer.data,
            }

        return Response(response_data, status=status.HTTP_200_OK)

    @never_cache
    def create(self, request, *args, **kwargs):
        """
        Args:
            mode : merge(create + update + delete)
            return : 반환할 데이터 선택, (미선택 시, 반환하지 않음)
        Returns:
            Response : 반환 데이터"""
        queryset = self.get_queryset()
        if request.GET.get("mode", None) == "merge":
            print(queryset)
            post_id_list = [inv.id for inv in queryset.iterator()]
            pre_id_list = [inv["id"] for inv in request.data]

            for id in set(post_id_list) - set(pre_id_list):
                queryset.get(id=id).delete()
            for row in request.data:
                # 가져온 data에서 id 제거
                row_id = row.pop("id")
                # id == 0 이면 새로 생성
                if row_id == 0:
                    serializer = self.get_serializer(data=row)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)

                # post_row 가져오고 id, creator, created_at 제거
                else:
                    post_row = self.get_serializer(queryset.get(id=row_id)).data
                    post_row.pop("id")
                    post_row.pop("creator")
                    post_row.pop("created_at")
                    # 다르면 수정
                    if post_row != row:
                        serializer = self.get_serializer(
                            queryset.get(id=row_id), data=row
                        )
                        serializer.is_valid(raise_exception=True)
                        self.perform_update(serializer)
                    # 같으면 pass
                    else:
                        pass

        elif request.GET.get("mode", None) == "upsert":
            for row in request.data:
                # 가져온 data에서 id 제거
                row_id = row.pop("id")
                # id == 0 이면 새로 생성
                if row_id == 0:
                    serializer = self.get_serializer(data=row)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)

                # post_row 가져오고 id, creator, created_at 제거
                else:
                    post_row = self.get_serializer(queryset.get(id=row_id)).data
                    post_row.pop("id")
                    post_row.pop("creator")
                    post_row.pop("created_at")
                    # 다르면 수정
                    if post_row != row:
                        serializer = self.get_serializer(
                            queryset.get(id=row_id), data=row
                        )
                        serializer.is_valid(raise_exception=True)
                        self.perform_update(serializer)
                    # 같으면 pass
                    else:
                        pass

        elif request.GET.get("mode", None) == "update":
            for row in request.data:
                row_id = row.pop("id")
                post_row = self.get_serializer(queryset.get(id=row_id)).data
                serializer = self.get_serializer(queryset.get(id=row_id), data=row)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

        else:
            serializer = bulk_create(self, request)
        response_data = {"datetime": timezone.now(), "message": "OK"}

        # return data 시, 생성된 데이터 반환
        if request.query_params.get("return", None) == "data":
            response_data["data"] = serializer.data
        elif request.query_params.get("return", None) == "id":
            response_data["data"] = {"id": serializer.data["id"]}
        return Response(response_data, status=status.HTTP_201_CREATED)

    @never_cache
    def retrieve(self, request, *args, **kwargs):

        fields = self.request.query_params.get("fields", None)
        if fields:
            fields = fields.split(",")
            self.queryset = self.queryset.values(*fields)
            print(self.queryset)
            if "year" in fields:
                self.queryset.values(*fields)
        response_data = {
            "datetime": timezone.now(),
            "message": "OK",
            "data": super().retrieve(request, *args, **kwargs).data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @never_cache
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        response_data = {"datetime": timezone.now(), "message": "OK"}
        return Response(response_data, status=status.HTTP_200_OK)

    @never_cache
    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        response_data = {"datetime": timezone.now(), "message": "OK"}
        return Response(response_data, status=status.HTTP_200_OK)

    @never_cache
    @swagger_auto_schema(
        manual_parameters=CommonParams.list_get_params,
    )
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        response_data = {"datetime": timezone.now(), "message": "OK"}
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
