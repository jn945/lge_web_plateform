import io
import json
import os
from datetime import datetime

import pandas as pd
import pdfkit
import reversion
from bs4 import BeautifulSoup
from django.db import transaction
from django.db.models import Max
from django.http import Http404, HttpResponse
from drf_yasg.utils import swagger_auto_schema
from fpdf import FPDF
from modules.common.params import CommonParams
from modules.common.utils import (
    convert_excel_to_pdf,
    get_objects_from_table,
    make_comment,
    make_excel,
    synchronizer_B_from_A,
)
from modules.common.viewset import CustomViewset
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import registerFont, stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import PageBreak, SimpleDocTemplate, Table, TableStyle
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from reversion.models import Version
from tabulate import tabulate

from .models import ProductSpecification
from .params import DocumentParam
from .serializers import ProductSpecificationSerializer


class ProductSpecificationViewSet(CustomViewset):
    queryset = ProductSpecification.objects.all()
    serializer_class = ProductSpecificationSerializer

    @swagger_auto_schema(
        tags=["[Document] ProductSpecification"],
        manual_parameters=CommonParams.list_get_params,
        operation_description="설명입니다",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[Document] ProductSpecification"], operation_description="설명입니다"
    )
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        with reversion.create_revision():
            super().create(request, *args, **kwargs)
            response_data = {"datetime": datetime.now(), "message": "OK"}
            return Response(response_data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["[Document] ProductSpecification"], operation_description="설명입니다"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[Document] ProductSpecification"], operation_description="설명입니다"
    )
    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        is_released = request.data.pop("is_released", None)
        partial = kwargs.pop("partial", False)
        # super() update 부
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        response_data = {"datetime": datetime.now(), "message": "OK"}
        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["[Document] ProductSpecification"], operation_description="설명입니다"
    )
    def partial_update(self, request, *args, **kwargs):
        with reversion.create_revision():
            return super().partial_update(request, *args, **kwargs)

    # atomic하게 처리
    @transaction.atomic
    @swagger_auto_schema(
        tags=["[Document] ProductSpecification"], operation_description="설명입니다"
    )
    def destroy(self, request, *args, **kwargs):
        try:
            revision = Version.objects.filter(object_id=self.kwargs["id"])
            revision.delete()
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            print(e)
            transaction.set_rollback(True)

    @swagger_auto_schema(
        tags=["[Document] ProductSpecification pdf"],
        manual_parameters=DocumentParam.get_pdf,
        operation_description="설명입니다",
    )
    def return_pdf(self, request, *args, **kwargs):

        # query parameter 로 id_list(str) -> id_list(list) 받기
        id_list = self.request.GET.get("id_list")
        id_list = id_list.split(",") if id_list else []
        id_list = [int(item) for item in id_list]

        queryset_db = []
        # queryset으로 해당 정보에 맞는 object set 찾기
        for inv in self.queryset.filter(id__in=id_list):
            db_data = inv.db
            db_data["title"] = inv.title
            queryset_db.append(db_data)
        # 엑셀 생성
        excel_path = make_excel(queryset_db)
        # 보내주기
        if self.request.GET.get("export_type") == "pdf":
            pdf_path = "example_data/data.pdf"

            convert_excel_to_pdf(excel_path, "example_data/data.pdf")
            with open(pdf_path, "rb") as file:
                response = HttpResponse(
                    file.read(),
                    content_type="application/pdf",
                )
                response["Content-Disposition"] = f"attachment; filename={pdf_path}"
                return response
        else:
            with open(excel_path, "rb") as file:
                response = HttpResponse(
                    file.read(),
                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
                response["Content-Disposition"] = f"attachment; filename={excel_path}"
            return response

        # pdf 생성
        # path = "out.pdf"
        # doc = SimpleDocTemplate(
        #     path,
        #     pagesize=landscape(letter),
        #     topMargin=inch,
        #     bottomMargin=inch,
        #     rightMargin=inch,
        #     leftMargin=inch,
        # )

        # 표 생성 및 html 화
        # data.columns = [1, 2, 3, 4]  # db["table_col"]
        # html_content = data.to_html(index=False)
        # soup = BeautifulSoup(html_content, "html.parser")

        # # 표 데이터 파싱
        # table_data = []
        # rows = soup.find_all("tr")
        # for row in rows:
        #     cells = row.find_all(["th", "td"])
        #     table_row = [cell.get_text().strip() for cell in cells]
        #     table_data.append(table_row)

        # # 표 스타일 설정
        # table_style = TableStyle(
        #     [
        #         ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
        #         ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        #         ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        #         ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        #         ("FONTSIZE", (0, 0), (-1, 0), 12),
        #         ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        #         ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        #         ("GRID", (0, 0), (-1, -1), 1, colors.black),
        #     ]
        # )

        # # 표 가로 길이 설정
        # table = Table(table_data, style=table_style)
        # table_width, table_height = table.wrap(doc.width, doc.height)
        # doc.pagesize = landscape((letter[1], table_width + inch * 2))

        # # 표를 문서에 추가
        # com1 = make_comment("This is Prargragh 1")
        # com2 = make_comment("This is Prargragh 2")
        # elements = [*com1, PageBreak(), table, PageBreak() * com2, table]
        # pdf_file = doc.build(elements)

        # with open(path, "rb") as pdf_file:
        #     pdf_content = pdf_file.read()

        # # Return the PDF file as a response
        # response = HttpResponse(pdf_content, content_type="application/pdf")
        # response["Content-Disposition"] = 'attachment; filename="out.pdf"'
        return Response("done")
