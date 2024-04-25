# -*- coding: utf-8 -*-
from uuid import uuid4, UUID
from datetime import datetime
from pydantic import BaseModel, Field


class ResponseData(BaseModel):
    uuid: UUID = Field(default=uuid4())
    code: int = Field(default=200, examples=[201, 204, 400, 401, 403])
    message: str = Field(default="PROCESS COMPLETED SUCCESSFULLY")
    data: dict | list | object | None = None
    timestamp: datetime = datetime.now()
