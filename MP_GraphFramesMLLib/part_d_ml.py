from pyspark.ml.classification import RandomForestClassifier
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler

sc = SparkContext()
spark = SparkSession.builder.appName('RandomForest').getOrCreate()


def predict(df_train, df_test):
    # TODO: Train random forest classifier

    # Hint: Column names in the given dataframes need to match the column names
    # expected by the random forest classifier `train` and `transform` functions.
    # Or you can alternatively specify which columns the `train` and `transform`
    # functions should use

    # Initialize and train the Random Forest Classifier
    rf = RandomForestClassifier(labelCol='label', featuresCol='features')
    model = rf.fit(df_train)
    
    # Make predictions on the test data
    predictions = model.transform(df_test)

    # Result: Result should be a list with the trained model's predictions
    # for all the test data points
    
    #Establish list for return data
    list_of_predictions = []
    
    #Load list_of_connected_components with results
    for row in predictions.select("prediction").collect():
        list_of_predictions.append(row.asDict()['prediction'])
    
    return list_of_predictions
    #return []


def parse_line(line):
    # TODO: Parse data from line into an RDD
    # Hint: Look at the data format and columns required by the KMeans fit and
    # transform functions
    
    return tuple((float(feature) for feature in line.split(',')))
    #return []


def main():
    ## Preprocess training data...
    #raw_training_data = sc.textFile("/MP_GraphFramesMLLib/dataset/training.data")
    raw_training_data = sc.textFile("dataset/training.data")

    # TODO: Convert text file into an RDD which can be converted to a DataFrame
    # Hint: For types and format look at what the format required by the
    # `train` method for the random forest classifier
    # Hint 2: Look at the imports above
    rdd_train = raw_training_data.map(parse_line).zipWithIndex().map(lambda x : (x[1],) + x[0])

    # TODO: Create dataframe from the RDD
    train_data = rdd_train.collect()
    columns = ["id", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "label"]
    df_train = spark.createDataFrame(train_data, columns)

    #Use VectorAssembler to assemble all features into a vector
    assembler = VectorAssembler(inputCols=[f"f{x}" for x in range(1,9)], outputCol="features")
    transformed_df_train = assembler.transform(df_train).select("label", "features")

    ## Preprocess test data...
    #raw_test_data = sc.textFile("/MP_GraphFramesMLLib/dataset/test-features.data")
    raw_test_data = sc.textFile("dataset/test-features.data")

    # TODO: Convert text file lines into an RDD we can use later
    rdd_test = raw_test_data.map(parse_line).zipWithIndex().map(lambda x : (x[1],) + x[0])

    # TODO:Create dataframe from RDD
    test_data = rdd_test.collect()
    columns = ["id", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8"]
    df_test = spark.createDataFrame(test_data, columns)

    #Use VectorAssembler to assemble all features into a vector
    assembler = VectorAssembler(inputCols=[f"f{x}" for x in range(1,9)], outputCol="features")
    transformed_df_test = assembler.transform(df_test).select("features")

    #predictions = predict(df_train, df_test)
    predictions = predict(transformed_df_train, transformed_df_test)

    # You can take a look at dataset/test-labels.data to see if your
    # predictions were right
    for pred in predictions:
        print(int(pred))


if __name__ == "__main__":
    main()

# https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.classification.RandomForestClassifier.html
# https://www.google.com/search?q=random+forest+classifier+pyspark+example&sca_esv=04d1cbeef736a982&rlz=1C1CHBF_enUS1071US1071&ei=aZTtZ-7mA9e2wN4Pstnh4QY&ved=0ahUKEwiuv8DujrqMAxVXG9AFHbJsOGwQ4dUDCBA&uact=5&oq=random+forest+classifier+pyspark+example&gs_lp=Egxnd3Mtd2l6LXNlcnAiKHJhbmRvbSBmb3Jlc3QgY2xhc3NpZmllciBweXNwYXJrIGV4YW1wbGUyBhAAGBYYHjILEAAYgAQYhgMYigUyCBAAGIAEGKIEMggQABiiBBiJBUjpClCTAVjqCXABeAGQAQCYAZgBoAGkB6oBAzAuOLgBA8gBAPgBAZgCCaACwgfCAgoQABiwAxjWBBhHmAMAiAYBkAYIkgcDMS44oAe_GbIHAzAuOLgHuQc&sclient=gws-wiz-serp
# https://stackoverflow.com/questions/46710934/pyspark-sql-utils-illegalargumentexception-ufield-features-does-not-exist/46729342#46729342
# https://stackoverflow.com/questions/46814164/random-forest-using-pyspark-ml-for-dataframes
# https://www.google.com/search?q=random+forest+classifier+pyspark+example+&sca_esv=aff5b07d3c99793e&rlz=1C1CHBF_enUS1071US1071&ei=-aftZ_KUFJvfp84PyYiP4Ak&ved=0ahUKEwiy9dDCobqMAxWb78kDHUnEA5wQ4dUDCBA&uact=5&oq=random+forest+classifier+pyspark+example+&gs_lp=Egxnd3Mtd2l6LXNlcnAiKXJhbmRvbSBmb3Jlc3QgY2xhc3NpZmllciBweXNwYXJrIGV4YW1wbGUgMgYQABgWGB4yCxAAGIAEGIYDGIoFMggQABiiBBiJBTIIEAAYgAQYogRImgpQ6wRY6wRwAXgBkAEAmAF1oAF1qgEDMC4xuAEDyAEA-AEBmAICoAJ_wgIKEAAYsAMY1gQYR5gDAIgGAZAGCJIHAzEuMaAHpwKyBwMwLjG4B3g&sclient=gws-wiz-serp