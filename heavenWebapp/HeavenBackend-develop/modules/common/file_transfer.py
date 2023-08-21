import os
import uuid
from collections.abc import Generator
from typing import TYPE_CHECKING

import rest_framework.request
from django.http import StreamingHttpResponse


def downlod_csv(data: list[str], filename: str) -> StreamingHttpResponse:
    """downlod_csv

    Args:
        data (list[str]): csv 파일로 다운로드할 데이터
                            [
                                ["Name", "Age", "City"],
                                ["John", "30", "New York"],
                                ["Jane", "25", "Los Angeles"],
                                ["Mike", "35", "Chicago"],
                            ]
        filename (str): 다운로드되는 file 이름(확장자 포함)

    Returns:
        StreamingHttpResponse: file 다운로드
    """

    def stream_csv_data() -> Generator[str]:
        for row in data:
            yield ",".join(row) + "\n"

    response = StreamingHttpResponse(
        streaming_content=stream_csv_data(), content_type="text/csv"
    )
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response


def chunk_bytes_data(bytes_data, chunk_size=8192) -> Generator[bytes]:
    start = 0
    end = chunk_size

    while start < len(bytes_data):
        yield bytes_data[start:end]
        start = end
        end += chunk_size


def download_bytes(data: bytes, filename: str) -> StreamingHttpResponse:
    """downlod_csv

    Args:
        data (bytes): 파일로 다운로드할 데이터
                            b"test data"
        filename (str): 다운로드되는 file 이름(확장자 포함)

    Returns:
        StreamingHttpResponse: file 다운로드
    """

    response = StreamingHttpResponse(
        chunk_bytes_data(data), content_type="application/octet-stream"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def uploaded_file_to_bytes(request: rest_framework.request.Request) -> bytes:
    """uploaded_file

    Args:
        request (rest_framework.request.Request): http file upload request

    Returns:
        bytes: upload된 파일의 bytes 데이터
    """
    file_obj = request.data["file_data"]

    file_data = file_obj.read()
    return file_data


def uploaded_file_to_fs(
    request: rest_framework.request.Request, save_direcotry: str
) -> str:
    """uploaded_file_to_fs
    업로드된 파일을 file system에 저장
    파일 이름은 uuid V4로 랜덤하게 생성

    Args:
        request (rest_framework.request.Request): http file upload request
        save_direcotry (str): 파일을 저장할 디렉토리

    Returns:
        str: _description_
    """
    file_obj = request.data["file_data"]
    origin_file_name = file_obj.name

    ext = os.path.splitext(origin_file_name)[1]
    if ext:
        filename: str = f"{uuid.uuid4()}{ext}"
    else:
        filename: str = f"{uuid.uuid4()}"

    file_path: str = os.path.join(save_direcotry, filename)
    with open(file_path, "wb") as file:
        file.write(file_obj.read())

    return file_path, origin_file_name
