import logging
from logging import config
from PIL import Image
import base64, binascii
import io
from uuid import uuid4, UUID
from classes import ImageData, MessageBody, Settings, ResponseData
from inspect import currentframe
from utils import is_base64, configure_logging

settings = Settings()
log = logging.getLogger(settings.environment)
logging.config.dictConfig(configure_logging())


async def ctr_store_new_image(msg: MessageBody, _uuid: UUID = uuid4()) -> ResponseData:
    log.info(f"Starting {currentframe().f_code.co_name} uuid: {str(_uuid)}")
    resp = ResponseData(uuid=_uuid, code=500, message="SOME INTERNAL ERROR")
    try:
        if is_base64(msg.data):
            image_bytes = base64.b64decode(msg.data, validate=True)
            image = Image.open(io.BytesIO(image_bytes))
            ImageData(
                _uuid=_uuid,
                imageData=msg.data,
                imageType=image.format,
                imageFilename=msg.fileName,
                imageSize=image.size,
                imageMode=image.mode,
                imageFormat=image.format_description
            ).save()
            resp = ResponseData(code=200, message="PROCESS COMPLETED SUCCESSFULLY")

    except binascii.Error as e:
        resp = ResponseData(code=500, message=f"we have problems with the bytes? ---> {e.__str__()}")
        log.error(resp.message)
    except Exception as e:
        resp = ResponseData(code=500, message=f"this is an error ---> {e.__str__()}")
        log.error(resp.message)
    finally:
        log.info(f"{currentframe().f_code.co_name} finish response code: {resp.code}")
        return resp




