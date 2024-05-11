from pyspark.sql import SparkSession, functions, types
import sys
import re

def path_to_hour(path):
    match = re.search(r'pagecounts-(\d{8}-\d{2})', path)
    if match is None:
        return None
    return match.group(1)

spark = SparkSession.builder.appName('wikipedia_popular').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

path_to_hour_udf = functions.udf(path_to_hour, types.StringType())

schema = types.StructType([
    types.StructField('lang', types.StringType()),
    types.StructField('title', types.StringType()),
    types.StructField('views', types.IntegerType()),
    types.StructField('bytes', types.LongType()),
])

lines = spark.read.csv(sys.argv[1], schema=schema, sep=' ').withColumn('hour', path_to_hour_udf(functions.input_file_name()))

filtered_lines = lines.filter(
    (lines['lang'] == 'en') &
    (lines['title'] != 'Main_Page') &
    (~lines['title'].startswith('Special:'))
).cache()

most_viewed = filtered_lines.groupBy('hour').max('views').withColumnRenamed('max(views)', 'views')

result = most_viewed.join(filtered_lines, on=['hour', 'views'], how='left')

result = result.sort('hour', 'title').select('hour', 'title', 'views')

result.write.csv(sys.argv[2], mode='overwrite')

spark.stop()
