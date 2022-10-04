#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mediahaven.mediahaven import MediaHavenClient

# Records
from mediahaven.resources.records import Records
from mediahaven.resources.organisations import Organisations

class MediaHaven(MediaHavenClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = Records(self)
        self.organisations = Organisations(self)
