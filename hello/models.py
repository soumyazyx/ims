from django.db import models


class Item(models.Model):

    LOCATIONS = [
        ("Location1", "Location1"),
        ("Location2", "Location2"),
    ]
    TYPES = [
        ("Flight", "Flight"),
        ("Ground", "Ground"),
    ]

    remarks = models.TextField(default='')
    added_ts = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    location = models.CharField(max_length=50, choices=LOCATIONS)
    item_type = models.CharField(max_length=50, choices=TYPES)
    item_name = models.CharField(max_length=255)
    model_num = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    item_serial_num = models.CharField(max_length=255)
    calibration_date = models.DateTimeField()

    def __str__(self):
        return "{}|{}".format(self.item_serial_num, self.added_ts)
