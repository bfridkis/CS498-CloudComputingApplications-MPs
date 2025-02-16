import json
import sys
import logging
import redis
import pymysql
#import os


# TODO 1
DB_HOST = "database-1-mp6.cluster-cdaace60ubjw.us-east-1.rds.amazonaws.com" # Add DB end point
DB_USER = "admin" # Add your database user
DB_PASS = "fridkis2MP6" # Add your database password
DB_NAME = "mp6_db" # Add your database name
DB_TABLE = "mp6_table1" # Add your table name
REDIS_URL = "redis://mp6-cache-eb9cwu.serverless.use1.cache.amazonaws.com:6379" # Add redis end point "redis://<end point>"
REDIS_HOST = "mp6-cache-eb9cwu.serverless.use1.cache.amazonaws.com"
REDIS_PORT = 6379

TTL = 60

class DB:
    def __init__(self, **params):
        params.setdefault("charset", "utf8mb4")
        params.setdefault("cursorclass", pymysql.cursors.DictCursor)

        self.mysql = pymysql.connect(**params)

    def query(self, sql):
        with self.mysql.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def record(self, sql, values):
        with self.mysql.cursor() as cursor:
            cursor.execute(sql, values)
            return cursor.fetchone()

    def get_idx(self, table_name):
        with self.mysql.cursor() as cursor:
            cursor.execute(f"SELECT MAX(id) as id FROM {table_name}")
            idx = str(cursor.fetchone()['id'] + 1)
            return idx

    #def insert(self, idx, data, table_name):
    def insert(self, data, table_name):
        with self.mysql.cursor() as cursor:
            hero = data["hero"]
            power = data["power"]
            name = data["name"]
            xp = data["xp"]
            color = data["color"]
            
            #sql = f"INSERT INTO {table_name} (`id`, `hero`, `power`, `name`, `xp`, `color`) VALUES ('{idx}', '{hero}', '{power}', '{name}', '{xp}', '{color}')"
            sql = f"INSERT INTO {table_name} (`hero`, `power`, `name`, `xp`, `color`) VALUES ('{hero}', '{power}', '{name}', '{xp}', '{color}')"
            result = cursor.execute(sql)
            self.mysql.commit()
            return result

 # TODO 2
def read(use_cache, xps, Database, Cache):
    # Implement Lazy Loading strategy
    
    result = []
    
    if use_cache: # Use cache
      
        for xp in xps:
            res = Cache.get(xp)
            if res:
                res = json.loads(res)
                #print(f"cache response: {res} respone type: {type(res)}")
                result.append(res)
            else:
                sql = f"SELECT * FROM {DB_TABLE} WHERE xp = {xp}"
                #res = Database.query(sql)[0]
                res = Database.record(sql, None)
                #print(f"database response: {res} respone type: {type(res)}")
                Cache.setex(xp, TTL, json.dumps(res))
                result.append(res)
       
    else: # Do not use cache
        for xp in xps:
            sql = f"SELECT * FROM {DB_TABLE} WHERE xp = {xp}"
            #res = Database.query(sql)[0]
            res = Database.record(sql, None)
            result.append(res)
    
    return result

# TODO 3
def write(use_cache, records, Database, Cache):
    # Implement Write Through strategy
    
    for record in records:
        
        result = Database.insert(record, DB_TABLE)
        
        if use_cache: # Use cache
            sql = f"SELECT * FROM {DB_TABLE} WHERE xp = {record["xp"]}"
            res = Database.query(sql)[0]
            Cache.setex(record["xp"], TTL, json.dumps(res))
                
        # else: # Do not use cache
            
def lambda_handler(event, context):
    
    #print(os.listdir('/opt/python/lib/python3.13/site-packages/'))
    #print(sys.path)

    print(f"incoming event: {event}")
    
    USE_CACHE = (event['USE_CACHE'] == "True")
    REQUEST = event['REQUEST']
    
    # Initialize database
    try:
        Database = DB(host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_NAME)
    except pymysql.MySQLError as e:
        print("ERROR: Unexpected error: Could not connect to MySQL instance.")
        print(e)
        sys.exit()

    #testq = "SELECT * FROM mp6_table1 ORDER BY name LIMIT 10;"
    #print(Database.query(testq))
        
    # Initialize cache
    #Cache = redis.Redis.from_url(REDIS_URL)    #Won't work because ssl has to be set to True for serverless cache
    Cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, ssl=True, decode_responses=True, ssl_cert_reqs="none")
    #Cache = redis.RedisCluster(host=REDIS_HOST, port=REDIS_PORT, ssl=True)
    #print(Cache.ping())
    
    result = []
    if REQUEST == "read":
        # event["SQLS"] is a list of all xps for which you have to query the database or redis.
        result = read(USE_CACHE, event["SQLS"], Database, Cache)
        
    elif REQUEST == "write":
        # event["SQLS"] should be a list of jsons. You have to write these rows to the database.
        write(USE_CACHE, event["SQLS"], Database, Cache)
        result = "write success"
    
    print(f"outgoing result: {result} result type: {type(result)}")
    #print(f"outgoing result[0]: {result[0]} result[0] type: {type(result[0])}")
    
    
    return {
        'statusCode': 200,
        'body': result
    }
    
    
# References
# https://github.com/aws-samples/amazon-elasticache-samples/blob/master/database-caching/example.py
# https://www.geeksforgeeks.org/how-to-install-python-packages-for-aws-lambda-layers/
# https://docs.aws.amazon.com/lambda/latest/dg/python-package.html
# https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/LambdaRedis.html
# https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/in-transit-encryption-enable-python.html#:~:text=The%20redis%2Dpy%2Dcluster%20client,until%20the%20migration%20is%20finished.
# https://redis-py.readthedocs.io/en/latest/examples/ssl_connection_examples.html
# https://repost.aws/questions/QUowoYijPgQZaV-1jes94UKA/how-to-gain-access-to-serverless-elasticache-redis-from-firewalled-vpc
# https://aws.amazon.com/getting-started/hands-on/boosting-mysql-database-performance-with-amazon-elasticache-for-redis/

# Notes
# Needed to add the "AmazonElastiCacheFullAccess" and "AWSLambdaVPCAccessExecutionRole" permission policies to the lambda IAM role (Actally no, this wasn't necessary after all!)
## The big hold up getting the lambda to talk to the (serverless) cache was the specification of ssl in the Redis connection/constructor call.
## See: https://repost.aws/questions/QUowoYijPgQZaV-1jes94UKA/how-to-gain-access-to-serverless-elasticache-redis-from-firewalled-vpc