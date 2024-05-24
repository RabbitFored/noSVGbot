import pymongo
import os

def scrape(data):
    myclient = pymongo.MongoClient(os.environ['mongo_uri'])
    database = myclient['noSVG']

    userid = data.chat.id
    chattype = data.chat.type


    collection = database["usercache"]
    if (chattype == 'group') or (chattype == 'supergroup'):
        collection = database["groupcache"]


    manybase = myclient['manybase']
    cluster = manybase["totalcache"]
    if (chattype == 'group') or (chattype == 'supergroup'):
        cluster = manybase["groupical"]

    firstseen = data.date
    result = collection.find_one({'userid': userid})
    manyres = cluster.find_one({'userid': userid})
    try:
        result['userid']
        userexist = True

    except:
        userexist = False

    try:
        manyres['userid']
        exuser = True
    except:
        exuser = False

    title = data.chat.title
    username = data.chat.username
    firstname = data.chat.first_name
    lastname = data.chat.last_name
    dc = data.from_user.dc_id

    scraped = {}
    scraped['userid'] = userid
    scraped['chattype'] = chattype

    if (chattype == 'group') or (chattype == 'supergroup'):
        scraped['title'] = title
        scraped['type'] = chattype
        scraped['username'] = username
        scraped['dc'] = dc
        scraped['firstseen'] = firstseen
    else:
        scraped['username'] = username
        scraped['firstname'] = firstname
        scraped['lastname'] = lastname
        scraped['is-banned'] = False
        scraped['dc'] = dc
        scraped['firstseen'] = firstseen


    if (userexist == False):
        collection.insert_one(scraped)

    if (exuser == False):
        cluster.insert_one(scraped)