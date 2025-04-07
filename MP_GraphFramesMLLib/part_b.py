from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.functions import collect_list
import pyspark.sql.functions as F

############################################
#### PLEASE USE THE GIVEN PARAMETERS     ###
#### FOR TRAINING YOUR KMEANS CLUSTERING ###
#### MODEL                               ###
############################################

NUM_CLUSTERS = 4
SEED = 0
MAX_ITERATIONS = 100
INITIALIZATION_MODE = "random"

sc = SparkContext()
spark = SparkSession(sc)

def get_clusters(df, num_clusters, max_iterations, initialization_mode,
                 seed):
    # TODO:
    # Use the given data and the cluster pparameters to train a K-Means model
    # Find the cluster id corresponding to data point (a car)
    # Return a list of lists of the titles which belong to the same cluster
    # For example, if the output is [["Mercedes", "Audi"], ["Honda", "Hyundai"]]
    # Then "Mercedes" and "Audi" should have the same cluster id, and "Honda" and
    # "Hyundai" should have the same cluster id
    
    #Establish and train kmeans model
    kmeans = KMeans(k=NUM_CLUSTERS, seed=seed, maxIter=max_iterations, initMode=initialization_mode)
    model = kmeans.fit(df)
    
    #Make predictions
    predictions = model.transform(df)
    
    #Establish list for return data
    list_of_k_groups = []
    
    #Load list_of_connected_components with results
    for row in predictions.select(["id", "prediction"]).groupby('prediction').agg(collect_list('id').alias('cluster_neighbors')).select('cluster_neighbors').collect():
        list_of_k_groups.append(row.asDict()['cluster_neighbors'])
    
    return list_of_k_groups


def parse_line(line):
    # TODO: Parse data from line into an RDD
    # Hint: Look at the data format and columns required by the KMeans fit and
    # transform functions
    
    return tuple((field if field == line.split(',')[0] else float(field) for field in line.split(',')))
    #return []


if __name__ == "__main__":
    f = sc.textFile("dataset/cars.data")
    #f = sc.textFile("/MP_GraphFramesMLLib/dataset/cars.data")

    rdd = f.map(parse_line)

    # TODO: Convert RDD into a dataframe
    ## Strange finding - Using spark.createDataFrame results in a different output, even though the resulting dataframe looks identical to the dataframe produced by the alternative 'toDF' method.
    ## Even stranger, the expected outcome in the assignment prompt matches the result I get in using spark.createDataFrame but the autograder fails using this method,
    #### while using the toDF method does not produce the expected output per the assignment prompt, but passes the autograder.
    #data = rdd.collect()
    #columns = ["id", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11"]
    #df = spark.createDataFrame(data, columns)
    
    df = rdd.toDF(["id", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11"])
    
    #Use VectorAssembler to assemble all features into a vector
    assembler = VectorAssembler(inputCols=[f"f{x}" for x in range(1,12)], outputCol="features")
    transformed_df = assembler.transform(df)

    clusters = get_clusters(transformed_df, NUM_CLUSTERS, MAX_ITERATIONS, INITIALIZATION_MODE, SEED)
    for cluster in clusters:
        print(','.join(cluster))

# References
# https://www.google.com/search?q=kmeans+clustering+python+pyspark+ml&sca_esv=5d14021b5f0ff6fa&rlz=1C1CHBF_enUS1071US1071&ei=dXXtZ_KLI_mBwN4Psqy--A4&ved=0ahUKEwiymqWs8bmMAxX5ANAFHTKWD-8Q4dUDCBA&uact=5&oq=kmeans+clustering+python+pyspark+ml&gs_lp=Egxnd3Mtd2l6LXNlcnAiI2ttZWFucyBjbHVzdGVyaW5nIHB5dGhvbiBweXNwYXJrIG1sMgUQIRigATIFECEYoAEyBRAhGKABMgUQIRigATIFECEYqwIyBRAhGKsCSJcyUJkZWMAwcAN4AZABAJgBiQKgAeALqgEGMC4xMC4xuAEDyAEA-AEBmAIOoAKUDMICChAAGLADGNYEGEfCAg0QABiABBiwAxhDGIoFwgIFEAAYgATCAgYQABgWGB7CAggQABgWGAoYHsICCxAAGIAEGIYDGIoFwgIFEAAY7wXCAgUQIRifBZgDAIgGAZAGCpIHBjMuMTAuMaAHyUKyBwYwLjEwLjG4B4cM&sclient=gws-wiz-serp
# https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.clustering.KMeans.html
# https://www.google.com/search?q=data+format+and+columns+needed+by+pyspark+kmeans+fit&rlz=1C1CHBF_enUS1071US1071&oq=data+format+and+columns+needed+by+pyspark+kmeans+fit&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIHCAEQABjvBTIHCAIQABjvBTIKCAMQABiiBBiJBTIHCAQQABjvBdIBCTEyMjg2ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8
# https://www.google.com/search?q=kmeans+using+rdd+based+api+pyspark+named+points&sca_esv=57c84f4e1d2307b7&rlz=1C1CHBF_enUS1071US1071&ei=E8LtZ_LODYrKwN4P-Ynl6QM&ved=0ahUKEwiypOe0urqMAxUKJdAFHflEOT0Q4dUDCBA&uact=5&oq=kmeans+using+rdd+based+api+pyspark+named+points&gs_lp=Egxnd3Mtd2l6LXNlcnAiL2ttZWFucyB1c2luZyByZGQgYmFzZWQgYXBpIHB5c3BhcmsgbmFtZWQgcG9pbnRzMgoQIRigARjDBBgKSLsPUNwJWNgOcAJ4AZABAJgBeqABsASqAQMwLjW4AQPIAQD4AQGYAgWgAt0CwgIKEAAYsAMY1gQYR8ICCBAhGKABGMMEmAMAiAYBkAYIkgcDMi4zoAfhELIHAzAuM7gH0QI&sclient=gws-wiz-serp
# https://www.google.com/search?q=kmeans+clustering+python+pyspark+ml+with+point+name&sca_esv=5d14021b5f0ff6fa&rlz=1C1CHBF_enUS1071US1071&ei=IeDvZ5KuCfSCp84PpJyJ0Qk&ved=0ahUKEwjSwsetv76MAxV0wckDHSROIpoQ4dUDCBA&uact=5&oq=kmeans+clustering+python+pyspark+ml+with+point+name&gs_lp=Egxnd3Mtd2l6LXNlcnAiM2ttZWFucyBjbHVzdGVyaW5nIHB5dGhvbiBweXNwYXJrIG1sIHdpdGggcG9pbnQgbmFtZTIFECEYoAFItBpQvgNYtBlwA3gBkAEAmAGcAaAB8RKqAQQwLjE3uAEDyAEA-AEBmAIUoALJE8ICChAAGLADGNYEGEfCAgUQIRirAsICBRAhGJ8FmAMAiAYBkAYIkgcEMy4xN6AH3GWyBwQwLjE3uAesEw&sclient=gws-wiz-serp