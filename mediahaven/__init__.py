#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mediahaven.mediahaven import MediaHavenClient

# Records
from mediahaven.resources.records import Records
from mediahaven.resources.field_definitions import FieldDefinitions
from mediahaven.resources.organisations import Organisations

class MediaHaven(MediaHavenClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = Records(self)
        self.fields = FieldDefinitions(self)
        self.organisations = Organisations(self)
