from pyspark import SparkContext
from numpy import array
from pyspark.mllib.clustering import KMeans, KMeansModel

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


def get_clusters(data_rdd, num_clusters=NUM_CLUSTERS, max_iterations=MAX_ITERATIONS,
                 initialization_mode=INITIALIZATION_MODE, seed=SEED):
    # TODO:
    # Use the given data and the cluster pparameters to train a K-Means model
    # Find the cluster id corresponding to data point (a car)
    # Return a list of lists of the titles which belong to the same cluster
    # For example, if the output is [["Mercedes", "Audi"], ["Honda", "Hyundai"]]
    # Then "Mercedes" and "Audi" should have the same cluster id, and "Honda" and
    # "Hyundai" should have the same cluster id
    return [[]]


if __name__ == "__main__":
    #f = sc.textFile("dataset/cars.data")
    f = sc.textFile("/MP_GraphFramesMLLib/dataset/cars.data")

    # TODO: Parse data from file into an RDD
    rdd = f.map(lambda line: array([x if x == line.split(',')[0] else float(x) for x in line.split(',')]))
    rdd_names = rdd.map(lambda x : x[0])
    rdd_features = rdd.map(lambda x : list(x[1:])).map(array)
    clusters = get_clusters(data_rdd)

    for cluster in clusters:
        print(','.join(cluster))

# https://www.google.com/search?q=kmeans+using+rdd+based+api+pyspark+named+points&sca_esv=57c84f4e1d2307b7&rlz=1C1CHBF_enUS1071US1071&ei=E8LtZ_LODYrKwN4P-Ynl6QM&ved=0ahUKEwiypOe0urqMAxUKJdAFHflEOT0Q4dUDCBA&uact=5&oq=kmeans+using+rdd+based+api+pyspark+named+points&gs_lp=Egxnd3Mtd2l6LXNlcnAiL2ttZWFucyB1c2luZyByZGQgYmFzZWQgYXBpIHB5c3BhcmsgbmFtZWQgcG9pbnRzMgoQIRigARjDBBgKSLsPUNwJWNgOcAJ4AZABAJgBeqABsASqAQMwLjW4AQPIAQD4AQGYAgWgAt0CwgIKEAAYsAMY1gQYR8ICCBAhGKABGMMEmAMAiAYBkAYIkgcDMi4zoAfhELIHAzAuM7gH0QI&sclient=gws-wiz-serp