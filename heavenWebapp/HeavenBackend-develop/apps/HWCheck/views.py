import json
from datetime import datetime

import reversion
from apps.accounts.models import User
from django.db import transaction
from django.db.models import Max
from django.http import Http404
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from modules.common.params import CommonParams
from modules.common.utils import default_response, synchronizer_B_from_A
from modules.common.viewset import CustomViewset
from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from reversion.models import Version

from .models import Document, HWCheck, HWCheckInfo, HWCheckRow
from .serializers import (
    DocumentSerializer,
    HWCheckInfoSerializer,
    HWCheckRowSerializer,
    HWCheckSerializer,
    VersionSerializer,
)


def copy_document(row):
    with reversion.create_revision():
        row_id = row["id"]
        copy_doc_id = row["copy_from_document_id"]
        document = Document.objects.get(id=copy_doc_id)
        new_document = Document.objects.create(
            result=document.result,
            linked_db=document.linked_db,
            comment=document.comment,
            hw_check_row=HWCheckRow.objects.get(id=row_id),
        )
        # 새로운 doc_id 수정
        hw_check_row = HWCheckRow.objects.get(id=row_id)
        hw_check_row.document_id = new_document.id
        hw_check_row.save()
        reversion.set_comment("Copy From " + str(row["copy_from"]))


def create_or_update_document(document_detail, document_id=None):
    history_comment = document_detail.pop("history_comment", None)
    with reversion.create_revision():
        if document_id is None or document_id == 0:
            # 새로운 Document 생성
            document = Document.objects.create(
                result=document_detail["result"],
                linked_db=document_detail["linked_db"],
                comment=document_detail["comment"],
                hw_check_row=HWCheckRow.objects.get(id=document_detail["hw_check_row"]),
            )
            hw_check_row = HWCheckRow.objects.get(id=document_detail["hw_check_row"])
            hw_check_row.document_id = document.id
            hw_check_row.save()
            reversion.set_comment(history_comment)
        else:
            # 기존 Document 수정 (id = some_number인 Document를 찾음)
            document = Document.objects.get(id=document_id)
            document.result = document_detail["result"]
            document.linked_db = document_detail["linked_db"]
            document.comment = document_detail["comment"]
            document.hw_check_row = HWCheckRow.objects.get(
                id=document_detail["hw_check_row"]
            )
            document.save()
            reversion.set_comment(history_comment)

    return document


def check_is_done(self, request, *args, **kwargs):
    progress_list = HWCheckRow.objects.filter(
        hw_check_id=self.kwargs["hw_check_id"]
    ).values_list("progress", flat=True)
    hw_check_ins = HWCheck.objects.get(id=self.kwargs["hw_check_id"])
    print(progress_list)
    if "미진행" in progress_list or "진행중" in progress_list:
        if "해당없음" in progress_list or "준용" in progress_list or "완료" in progress_list:
            hw_check_ins.is_done = "진행중"
            hw_check_ins.save()
        else:
            hw_check_ins.is_done = "미진행"
            hw_check_ins.save()
    else:
        hw_check_ins.is_done = "완료"
        hw_check_ins.save()


# Create your views here.
class HWCheckViewSet(CustomViewset):
    queryset = HWCheck.objects.all()
    serializer_class = HWCheckSerializer

    @swagger_auto_schema(
        tags=["[HWCheck] HWCheck"],
        manual_parameters=CommonParams.list_get_params,
        operation_description="설명입니다",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @transaction.atomic
    @swagger_auto_schema(tags=["[HWCheck] HWCheck"], operation_description="설명입니다")
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        # Response 생성 부
        response_data = {"datetime": datetime.now(), "message": "OK"}
        return Response(response_data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["[HWCheck] HWCheck"],
        manual_parameters=CommonParams.retrieve_get,
        operation_description="설명입니다",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[HWCheck] HWCheck"], operation_description="설명입니다")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[HWCheck] HWCheck"], operation_description="설명입니다")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[HWCheck] HWCheck"], operation_description="설명입니다")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# Create your views here.
class HWCheckRowViewSet(CustomViewset):
    queryset = HWCheckRow.objects.all()
    serializer_class = HWCheckRowSerializer

    def perform_create(self, serializer):
        serializer.save(creator=User.objects.get(id=1))
        ins = serializer.instance
        if ins.document_id and ins.document_id == ins.copy_from_document_id:
            document = Document.objects.get(id=ins.copy_from_document_id)
            new_document = Document.objects.create()

            field_names = list(document.__dict__.keys())
            fields_to_exclude = ["_state", "id", "created_at"]
            filtered_field_names = [
                field for field in field_names if field not in fields_to_exclude
            ]

            synchronizer_B_from_A(
                filtered_field_names, document, new_document, create=False
            )
            # 새로운 copy from 및 row id 수정
            new_document.copy_from_document_id = document.id
            new_document.copy_from = ins.copy_from
            new_document.hw_check_row = ins
            new_document.save()
            # 새로운 doc_id 수정
            ins.document_id = new_document.id
            ins.save()

    def perform_update(self, serializer):
        # 저장
        serializer.save()

    def get_queryset(self):
        hw_check_id = self.kwargs["hw_check_id"]  # plan_id 값을 가져옴
        queryset = HWCheckRow.objects.filter(hw_check_id=hw_check_id).order_by(
            "main_part", "sub_part", "item"
        )
        return queryset

    @swagger_auto_schema(
        tags=["[HWCheck] HWCheck Row"], manual_parameters=CommonParams.list_get_params
    )
    def list(self, request, *args, **kwargs):
        self.queryset = self.get_queryset()
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[HWCheck] HWCheck Row"],
        manual_parameters=CommonParams.merge,
        operation_description="설명입니다",
    )
    # 리스트로 input를 받고 개별 생성 처리
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        if request.GET.get("mode") == "update":
            for row in request.data:
                document_detail = row.pop("document", None)
                instance = HWCheckRow.objects.get(id=row["id"])
                serializer = HWCheckRowSerializer(instance, data=row, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
                    raise exceptions.ValidationError

                if (
                    row["document_id"] == row["copy_from_document_id"]
                    and row["copy_from_document_id"]
                ):
                    copy_document(row)
                elif document_detail:
                    create_or_update_document(document_detail, row["document_id"])
                else:
                    pass

        response_data = {"datetime": datetime.now(), "message": "OK"}
        check_is_done(self, request, *args, **kwargs)
        return Response(response_data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["[HWCheck] HWCheck Row"],
        manual_parameters=CommonParams.retrieve_get,
        operation_description="설명입니다",
    )
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[HWCheck] HWCheck Row"], operation_description="설명입니다")
    # 리스트로 input를 받고 개별 수정 처리
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[HWCheck] HWCheck Row"], operation_description="설명입니다")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[HWCheck] HWCheck Row"],
        operation_description="설명입니다",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# @permission_classes((IsAuthenticated,))
# @authentication_classes((JSONWebTokenAuthentication,))
class HWCheckInfoViewSet(CustomViewset):
    queryset = HWCheckInfo.objects.all()
    serializer_class = HWCheckInfoSerializer

    @swagger_auto_schema(
        tags=["[HWCheck] HWCheck Info"],
        operation_description="설명입니다",
        manual_parameters=CommonParams.list_get_params,
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[HWCheck] HWCheck Info"], operation_description="설명입니다")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[HWCheck] HWCheck Info"], operation_description="설명입니다")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[HWCheck] HWCheck Info"], operation_description="설명입니다")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[HWCheck] HWCheck Info"], operation_description="설명입니다")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[HWCheck] HWCheck Info"], operation_description="설명입니다")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    # 해당 plan_id에 해당하는 plan_series만 가져오도록 설정
    def get_queryset(self):
        hw_check_row_id = self.kwargs["hw_check_row_id"]  # plan_id 값을 가져옴
        queryset = Document.objects.filter(
            hw_check_row_id=hw_check_row_id
        )  # plan 필드를 사용하여 필터링
        return queryset

    @swagger_auto_schema(
        tags=["[HWCheck] Document"],
        operation_description="설명입니다",
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return default_response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["[HWCheck] Document"],
        operation_description="********'history_comment'를 body에 추가해주세요*************",
        manual_parameters=CommonParams.merge,
    )
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # history comment는 별개로 작성
        # history create 부
        with reversion.create_revision():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            # history create 부
            history_comment = request.data.pop("history_comment", None)
            reversion.set_comment(history_comment)
            # syn
            syn_list = [
                # "due_date",
                # "common_user",
                # "progress",
                "result",
                "linked_db",
                # "copy_from",
                # "copy_from_document_id",
            ]
            synchronizer_B_from_A(
                syn_list,
                serializer.instance,
                HWCheckRow.objects.get(id=serializer.instance.hw_check_row_id),
                create=False,
            )
            # id 따로 저장
            hw_check_row_instance = HWCheckRow.objects.get(
                id=serializer.instance.hw_check_row_id
            )
            hw_check_row_instance.document_id = serializer.instance.id
            hw_check_row_instance.history_comment = history_comment
            hw_check_row_instance.save()
            response_data = {"datetime": datetime.now(), "message": "OK"}
            # is_done check
            check_is_done(self, request, *args, **kwargs)

            return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["[HWCheck] Document"], operation_description="설명입니다")
    def retrieve(self, request, *args, **kwargs):
        response_data = {
            "datetime": datetime.now(),
            "message": "OK",
            "data": super().retrieve(request, *args, **kwargs).data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["[HWCheck] Document"],
        operation_description="********'history_comment'를 body에 추가해주세요*************",
    )
    def update(self, request, *args, **kwargs):
        with reversion.create_revision():
            instance = self.get_object()
            hw_check_ins = HWCheckRow.objects.get(id=instance.hw_check_row_id)
            # history comment는 별개로 작성
            # reversion 부
            history_comment = request.data.pop("history_comment", None)
            reversion.set_comment(history_comment)
            partial = kwargs.pop("partial", False)
            # super() update 부
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, "_prefetched_objects_cache", None):
                instance._prefetched_objects_cache = {}
            # document를 HW Check Row에 synchronize
            syn_list = [
                # "due_date",
                # "common_user",
                # "progress",
                "result",
                "linked_db",
                # "copy_from",
                # "copy_from_document_id",
            ]
            synchronizer_B_from_A(
                syn_list,
                instance,
                hw_check_ins,
                create=False,
            )
            hw_check_ins.history_comment = history_comment
            hw_check_ins.save()
            response_data = {"datetime": datetime.now(), "message": "OK"}
            # is_done check
            check_is_done(self, request, *args, **kwargs)
            return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["[HWCheck] Document"],
        operation_description="********'history_comment'를 body에 추가해주세요*************",
    )
    def partial_update(self, request, *args, **kwargs):
        with reversion.create_revision():
            return super().partial_update(request, *args, **kwargs)

    # atomic하게 처리
    @transaction.atomic
    @swagger_auto_schema(tags=["[HWCheck] Document"], operation_description="설명입니다")
    def destroy(self, request, *args, **kwargs):
        revision = Version.objects.filter(object_id=self.kwargs["pk"])
        revision.delete()
        super().destroy(request, *args, **kwargs)
        response_data = {"datetime": datetime.now(), "message": "OK"}
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        tags=["[HWCheck] Document"],
        manual_parameters=CommonParams.delete_id_list,
        operation_description="설명입니다",
    )
    def delete_id_list(self, request, *args, **kwargs):
        id_list_str = request.GET.get("id_list")
        id_list = id_list_str.split(",")
        self.queryset.filter(id__in=id_list).delete()
        return default_response(None, status=status.HTTP_204_NO_CONTENT)


class DocumentHistoryApiviewList(APIView):
    queryset = Version.objects.all()
    serializer_class = DocumentSerializer

    @swagger_auto_schema(
        tags=["[HWCheck] Document History"], operation_description="설명입니다"
    )
    def get(self, request, *args, **kwargs):
        # hw_check_row_id 에 해당하는 document history만 filtering
        document_id = self.kwargs["document_id"]
        versions = self.queryset.filter(object_id=document_id)
        serialized_data_list, comment_list, final_data, created_list = [], [], [], []
        for version in versions:
            # string으로 쓰여진 reversion data를 Document에 맞춰서 instance화
            data = json.loads(version.serialized_data)[0]["fields"]
            # reversion id 로 id 변환
            data["id"] = version.id
            serialized_data_list.append(data)

            # history comment 가져오기
            comment = version.revision.comment
            created_at = version.revision.date_created
            created_list.append(created_at)
            comment_list.append(comment)
        # serialize 후 comment 삽입
        for doc, comment, created in zip(
            serialized_data_list, comment_list, created_list
        ):
            doc["history_comment"] = comment
            doc["created_at"] = created
            final_data.append(doc)
        # for history in final_data:
        #     common_user_id_list = history["common_user"]
        #     post_data = [
        #         {
        #             "id": id,
        #             "name": User.objects.get(id=id).name,
        #         }
        #         for id in common_user_id_list
        #     ]
        #     history["common_user"] = post_data

        response_data = {
            "datetime": datetime.now(),
            "message": "OK",
            "data": final_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class DocumentHistoryApiview(APIView):
    queryset = Version.objects.all()
    serializer_class = DocumentSerializer

    @swagger_auto_schema(
        tags=["[HWCheck] Document History"], operation_description="설명입니다"
    )
    def get(self, request, *args, **kwargs):
        document_history_id = self.kwargs["document_history_id"]
        versions = self.queryset.filter(id=document_history_id)
        data = json.loads(versions[0].serialized_data)[0]["fields"]
        data["id"] = versions[0].id
        data["common_user"] = [
            {
                "id": id,
                "name": User.objects.get(id=id).name,
            }
            for id in data["common_user"]
        ]
        response_data = {
            "datetime": datetime.now(),
            "message": "OK",
            "data": data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["[HWCheck] Document History"], operation_description="설명입니다"
    )
    def delete(self, request, *args, **kwargs):
        document_history_id = self.kwargs["document_history_id"]
        version = self.queryset.filter(id=document_history_id)
        version.delete()
        response_data = {"datetime": datetime.now(), "message": "OK"}
        return Response(response_data)


class DocumentPrevicousHistoryViewSet(APIView):
    @swagger_auto_schema(
        tags=["[HWCheck] Document Previous History"], operation_description="설명입니다"
    )
    def get(self, request, *args, **kwargs):
        document_id = self.kwargs["document_id"]
        queryset = Document.objects.get(id=document_id)
        document_history_ids = []
        if queryset.copy_from_document_id:
            while True:
                queryset = Document.objects.get(id=queryset.copy_from_document_id)
                document_history_ids.append(queryset.id)
                if not queryset.progress == "준용":
                    break
            versions = Version.objects.filter(object_id__in=document_history_ids)
            serialized_data_list = []
            for version in versions:
                data = json.loads(version.serialized_data)[0]["fields"]
                data["id"] = version.id
                serialized_data_list.append(data)
        else:
            response_data = {"datetime": datetime.now(), "message": "No content"}
            return Response(response_data)
        response_data = {
            "datetime": datetime.now(),
            "message": "OK",
            "data": serialized_data_list,
        }
        return Response(response_data, status=status.HTTP_200_OK)
