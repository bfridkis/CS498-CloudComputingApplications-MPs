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
    kmeans = KMeans(k=NUM_CLUSTERS, seed=SEED, maxIter=MAX_ITERATIONS, initMode=INITIALIZATION_MODE)
    model = kmeans.fit(df)
    
    #Make predictions
    predictions = model.transform(df)
    
    #Establish list for return data
    list_of_k_groups = []
    
    #Load list_of_connected_components with results
    for row in predictions.select(["id", "prediction"]).groupby('prediction').agg(collect_list('id').alias('cluster_neighbors')).select('cluster_neighbors').collect():
        list_of_k_groups.append(row.asDict()['cluster_neighbors'])
    
    return list_of_k_groups
    
    #return [[]]


def parse_line(line):
    # TODO: Parse data from line into an RDD
    # Hint: Look at the data format and columns required by the KMeans fit and
    # transform functions
    
    return tuple((field if field == line.split(',')[0] else float(field) for field in line.split(',')))
    #return []

f = sc.textFile("/MP_GraphFramesMLLib/dataset/cars.data")

rdd = f.map(parse_line)

# TODO: Convert RDD into a dataframe
data = rdd.collect()
columns = ["id", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11"]
df = spark.createDataFrame(data, columns)

#Use VectorAssembler to assemble all features into a vector
assembler = VectorAssembler(inputCols=[f"f{x}" for x in range(1,12)], outputCol="features")
transformed_df = assembler.transform(df)

clusters = get_clusters(transformed_df, NUM_CLUSTERS, MAX_ITERATIONS,
                        INITIALIZATION_MODE, SEED)
for cluster in clusters:
    print(','.join(cluster))
    
    
    
# From Saharsh
#aggregated = transformed.groupBy('prediction').agg(F.collect_list("name"))
aggregated = predictions.groupBy('prediction').agg(F.collect_list("id"))
aggregated = aggregated.withColumnRenamed("collect_list(id)", "names")

return aggregated.rdd.map(lambda x: x[1]).collect()
def parse_line(line):
    features = line.split(",")
    return [features[0], Vectors.dense([float(_) for _ in features[1:]])]