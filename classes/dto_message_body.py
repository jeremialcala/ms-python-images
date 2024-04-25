# -*- coding: utf-8 -*-
import logging

from faker import Faker
from pydantic import BaseModel

from .tool_settings import Settings


fk = Faker()
settings = Settings()
log = logging.getLogger(settings.environment)


class MessageBody(BaseModel):
    fileName: str
    data: str
