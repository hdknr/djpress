# coding: utf-8
from django.dispatch import dispatcher


thumbnail_uploaded = dispatcher.Signal(providing_args=["intance", "response"])
