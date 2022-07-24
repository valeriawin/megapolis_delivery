from json import JSONDecodeError

from fastapi import HTTPException
from pydantic.error_wrappers import ValidationError
from geojson_pydantic import Feature


async def get_request_data(request):
    try:
        request_data = await request.json()
    except JSONDecodeError as exception:
        raise HTTPException(
            status_code=400, detail="Nothing passed"
        ) from exception

    return request_data


async def validate_request_data(request_data):
    try:
        Feature(**request_data)
    except ValidationError as exception:
        raise HTTPException(
            status_code=422, detail="Invalid data passed"
        ) from exception

    return request_data


async def prepare_request_data(request):
    request_data = await get_request_data(request)
    prepared_data = await validate_request_data(request_data)

    return prepared_data
