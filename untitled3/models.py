# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class SearchReport(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    digest = models.CharField(max_length=400, blank=True, null=True)
    url = models.CharField(max_length=800, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    key_word = models.CharField(max_length=255, blank=True, null=True)
    report_time = models.CharField(max_length=255, blank=True, null=True)
    collect_time = models.CharField(max_length=255, blank=True, null=True)
    statue = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'search_report'