# -*- coding: utf-8 -*-
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import datetime as dt

class MyprojectPipeline(object):
    def process_item(self, item, spider):
        return item


class FirestoreExport(object):

    def __init__(self):
        CREDENTIAL = os.path.join(os.path.dirname(__file__), "credential.json")
        cred = credentials.Certificate(CREDENTIAL)
        default_app = firebase_admin.initialize_app(cred)

    def process_item(self, item, spider):
        db = firestore.client()

        tdatetime = dt.datetime.now() + dt.timedelta(hours=9)
        tstr = tdatetime.strftime('%Y-%m-%d')

        valuid = item['valuid']
        ref = db.collection(tstr).document(valuid)
        ref.set(item)

        return item
