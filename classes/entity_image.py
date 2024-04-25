# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from uuid import uuid4, UUID

from mongoengine import *

from enums import Status
from .tool_settings import Settings

settings = Settings()
log = logging.getLogger(settings.environment)
connect(
    db=settings.db_name,
    username=settings.db_username,
    password=settings.db_password,
    host=settings.db_host
)
"""
    This is a Simple entity that will save an image on base64 encoded form.
"""


class Image(Document):
    _uuid = UUIDField(required=True, unique=True, default=uuid4())
    image = StringField()
    imageType = StringField()  # This will have the base64encoded data
    imageFilename = StringField()
    imageSize = StringField()
    imageMetadata = DictField(default=None)
    createdAt = DateTimeField(required=True, default=datetime.now())
    status = IntField(required=True, default=Status.REG.value)
    statusDate = DateTimeField(required=True, default=datetime.now())

    @staticmethod
    async def get_image_from_uuid(uuid: UUID):
        image = None
        try:
            image = [image for image in Image.objects(_uuid=uuid)][-1]
        except ValueError as e:
            log.error(e.__str__())
        finally:
            return image
