from django.db import models

from schematics.models import Model as SchematicsModel
from schematics.types import StringType, DecimalType, DateTimeType

from datetime import datetime


class AnyData(SchematicsModel):
    city = StringType()
    temperature = DecimalType()
    taken_at = DateTimeType(default=datetime.now)


class GenericModel(models.Model):
    any_data = JSONField()

    def __unicode__(self):
        return unicode(self.id)

    def to_dict(self):
        return AnyData(raw_data=self.any_data).to_native()

