from pymongo import MongoClient
from utilities.customLogger import LogGen
from datetime import datetime
from utilities.readProperties import ReadConfig
import json

client = MongoClient(ReadConfig.get_db_details('url'))
db = client[ReadConfig.get_db_details('db')]
collection = db[ReadConfig.get_db_details('collection')]
company_collection = db[ReadConfig.get_db_details('company')]
ignore_collection = db[ReadConfig.get_db_details('ignorelist')]
logger = LogGen.loggen('linkedin_automation')

class db_ops:

    @staticmethod
    def delete_doc(c, query):
        try:
            if c == "company_collection":
                company_collection.delete_one(query)
                return True
            elif c == "main":
                collection.delete_one(query)
                return True
            return False
        except Exception as e:
            print(f'Error in delete_doc: {str(e)}')

    @staticmethod
    def check_availability(c, query):
        try:
            if c == "company_collection":
                if company_collection.find_one(query):
                    return True
                else:
                    return False
            if c == "main":
                if collection.find_one(query):
                    return True
                else:
                    return False
        except Exception as e:
            print(f'Error in check_availability:{str(e)}')

    @staticmethod
    def insertion(c, document):
        try:
            if c == "main":
                collection.insert_one(document)

            if c == "company_collection":
                company_collection.insert_one(document)

        except Exception as e:
            print(f'Error in insertion: {str(e)}')

    def company_without_details():
        try:
            full_details = collection.find({'portal': 'naukri'})
            ignore_company_details = ignore_collection.find({}, {"company": 1, "_id": 0})
            ignore_company_name_list = [document["company"].lower() for document in ignore_company_details]
            result_docs = []
            for doc in full_details:
                query = {"company": doc["company"].lower(), "follower": {'$exists': False}}
                if not company_collection.find_one({"company": doc["company"].lower()}) or company_collection.find_one(query):
                    if doc["company"].lower() not in ignore_company_name_list:
                        result_docs.append(doc["company"])
                        print(f'check {doc["company"]}')
                    # else:
                    #     company_collection.delete_one({"company": doc["company"]})
                    #     print(f'{doc["company"]} deleted')

            result_docs = list(set(result_docs))
            print(result_docs)
            return result_docs
        except Exception as e:
            print(f'Error in company_without_details: {str(e)}')

    def insert_company_details(result):
        try:
            print(f'Inserting {result}')
            # with open(r'./testCases/companydetails.json', 'r', encoding='utf-8') as file:
            #     details = json.load(file)
            doc = result
            # for doc in details:
            if (('services' in doc['industry'].lower() and 'consulting' in doc['industry'].lower())
                    or 'e.learning' in doc['industry'].lower()) \
                    and not ignore_collection.find_one({'company': doc['company'].lower()}):

                ignore_collection.insert_one({'company': doc['company'].lower()})
                print(f"{doc['company']} added to ignore")
            if not company_collection.find_one({'company': doc['company'].lower()}):
                company_collection.insert_one(doc)
            if company_collection.find_one({'company': doc['company'].lower(), 'follower': {'$exists': False}}):
                company_collection.update_many({'company': doc['company'].lower()}, {'$set': doc})

        except Exception as e:
            print(f'Error in insert_company_details: {str(e)}')

class insertDB:
    success = 0
    def insert_company(company):
        if not company_collection.find_one({'company': company}):
            company_collection.insert_one({'company': company})
    @staticmethod
    def start_insert(doclist):
        try:
            # print(f'Total {len(doclist)} inserting...')
            file_data_list = []
            failed_to_insert = []
            for doc in doclist:
                try:
                    insertDB.insert_company(doc['company'])
                    if not collection.find_one(doc):
                        doc['time'] = datetime.now()
                        doc['portal'] = 'naukri'
                        file_data_list.append(doc)
                        collection.insert_one(doc)
                        insertDB.success += 1
                        print(f'{doc["company"]} inserted successfully')
                except Exception as e:
                    failed_to_insert.append(doc)
                    print(f'Error in start_insert: {str(e)}')
                    logger.error(f'Error in start_insert: {str(e)}')

            print(f'{insertDB.success} inserted in DB')
            if failed_to_insert:
                print(f'Retrying to insert {len(doclist) - insertDB.success} ')
                insertDB.start_insert(failed_to_insert)
            else:
                print(f'All Inserted in DB')
                return True
            # if file_data_list:
            #     collection.insert_many(file_data_list)
            #     return True
        except Exception as e:
            print(f'Error in start_insert {str(e)}')
            logger.error(f'Error in start_insert: {str(e)}')
            return False
