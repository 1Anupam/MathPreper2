"""
This file contains some common MongoDB code.
"""
import os
import json
import pymongo as pm
from pymongo.server_api import ServerApi
import bson.json_util as bsutil


# all of these will eventually be put in the env:
user_nm = "user1"
cloud_svc = "cluster0.ewjxh.mongodb.net"
# passwd = os.environ.get("MONGO_PASSWD", '')
passwd = 'ask739'
cloud_mdb = "mongodb+srv"
db_params = "retryWrites=true&w=majority"

db_nm = 'MathPrepper'

REMOTE = "0"
LOCAL = "1"

client = None


def get_client():
    """
    This provides a uniform way to get the client across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    """
    global client
    if os.environ.get("LOCAL_MONGO", REMOTE) == LOCAL:
        print("Connecting to Mongo locally.")
        client = pm.MongoClient()
    else:
        print("Connecting to Mongo remotely.")
        client = pm.MongoClient("mongodb+srv://user1:aks739@cluster0.ewjxh.mongodb.net/MathPrepper?retryWrites=true&w=majority")
    return client


def fetch_one(collect_nm, filters={}):
    """
    Fetch one record that meets filters.
    """
    return client[db_nm][collect_nm].find_one(filters)


def del_one(collect_nm, filters={}):
    """
    Fetch one record that meets filters.
    """
    return client[db_nm][collect_nm].delete_one(filters)


def fetch_all(collect_nm):
    all_docs = []
    for doc in client[db_nm][collect_nm].find():
        all_docs.append(json.loads(bsutil.dumps(doc)))
    return all_docs


def fetch_all_as_dict(collect_nm, key_nm):
    all_list = fetch_all(collect_nm, key_nm)
    print(f'{all_list=}')
    all_dict = {}
    for doc in all_list:
        print(f'{doc=}')
        all_dict[doc[key_nm]] = doc[key_nm]
    return all_dict


def insert_doc(collect_nm, doc):
    return client[db_nm][collect_nm].insert_one(doc)
    
