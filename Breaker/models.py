from django.db import models

class Alarm(models.Model):
    hist_timestamp = models.DateTimeField(
        null=False,
        default='1980-01-01 00:00:00'  # Default datetime value
    )
    hist_timestamp_dst = models.CharField(
        max_length=1,
        null=False,
        default='s'  # Default value
    )
    hcapi_subscript = models.IntegerField(
        null=False,
        default=0  # Default value
    )
    time = models.DateTimeField(
        null=True,  # TIME is nullable
        blank=True
    )
    text = models.TextField(
        null=True,  # TEXT is nullable
        blank=True
    )
    area = models.CharField(
        max_length=8,
        null=True,
        blank=True
    )
    category = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    excdef = models.CharField(
        max_length=8,
        null=True,
        blank=True
    )
    location = models.CharField(
        # max_length=12,
        null=True,
        blank=True
    )
    time_soe = models.DateTimeField(
        null=True,
        blank=True
    )
    compid = models.CharField(
        max_length=56,
        null=True,
        blank=True
    )
    seqnum = models.BigIntegerField(
        null=True,
        blank=True
    )
    audible = models.IntegerField(
        null=True,
        blank=True
    )
    event = models.IntegerField(
        null=True,
        blank=True
    )
    abnormal = models.IntegerField(
        null=True,
        blank=True
    )
    unackiss = models.IntegerField(
        null=True,
        blank=True
    )
    priornum = models.BigIntegerField(
        null=True,
        blank=True
    )
    ms = models.BigIntegerField(
        null=True,
        blank=True
    )
    time_dst = models.CharField(
        max_length=1,
        null=True,
        blank=True
    )
    time_soe_dst = models.CharField(
        max_length=1,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'alarm'  # This maps the model to the "ALARM" table
        managed = True  # Set to True if you want Django to manage migrations

    def __str__(self):
        return self.text if self.text else "Alarm Entry"
