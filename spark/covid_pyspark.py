from pyspark.sql import SparkSession

my_spark = SparkSession \
    .builder \
    .appName("myApp") \
    .config("spark.mongodb.input.uri", "mongodb+srv://admin:admin@cluster0-skgzv.mongodb.net/covid_db.covid_collection?retryWrites=true&w=majority") \
    .config("spark.mongodb.output.uri", "mongodb+srv://admin:admin@cluster0-skgzv.mongodb.net/covid_db.covid_collection") \
    .getOrCreate()
	
	
pyspark --conf "spark.mongodb.input.uri=mongodb+srv://admin:admin@cluster0-skgzv.mongodb.net/test?retryWrites=true&w=majority" --conf "spark.mongodb.output.uri=mongodb+srv://admin:admin@cluster0-skgzv.mongodb.net/test" --packages org.mongodb.spark:mongo-spark-connector_2.12:2.4.1

df = spark.read.format("mongo").load()

df = spark.read.format("com.mongodb.spark.sql.DefaultSource").option("database","covid_db").option("collection", "covid_collection").load()

spark-shell --conf "spark.mongodb.input.uri=spark.mongodb.input.uri=mongodb+srv://admin:admin@cluster0-skgzv.mongodb.net/test?retryWrites=true&w=majority" --conf "spark.mongodb.input.uri=mongodb+srv://admin:admin@cluster0-skgzv.mongodb.net/test" --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1

import com.mongodb.spark._

val rdd = MongoSpark.load(sc)

println(rdd.count)
println(rdd.first.toJson)