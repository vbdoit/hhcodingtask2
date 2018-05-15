import json

from django.db import models
from jsonfield import JSONField

from schematics.models import Model as SchematicsModel
from schematics.types import StringType, DecimalType, DateTimeType

from datetime import datetime


class AnyData(SchematicsModel):
    city = StringType(required=True)
    temperature = DecimalType(required=True)
    taken_at = DateTimeType(default=datetime.now)


class GenericModel(models.Model):
    any_data = JSONField()

    def __unicode__(self):
        return unicode(self.id)

    def to_dict(self):
        result = AnyData(raw_data=json.loads(self.any_data)).to_native()
        result['id'] = self.pk
        return result
