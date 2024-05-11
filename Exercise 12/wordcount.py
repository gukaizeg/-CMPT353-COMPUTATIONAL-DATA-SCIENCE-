from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, lower, col, length
import sys

def main(input_directory, output_directory):
    spark = SparkSession.builder.appName('WordCount').getOrCreate()

    # Read text files in the input directory
    df = spark.read.text(input_directory)

    # Split the lines into words
    words = df.select(explode(split(df['value'], r'[\s\p{Punct}]+')).alias('word'))

    # Convert to lower case
    words = words.select(lower(col('word')).alias('word'))

    # Filter out empty strings
    words = words.filter(length(col('word')) > 0)

    # Count the words
    wordcounts = words.groupBy('word').count()

    # Sort by count in descending order, and then alphabetically
    wordcounts = wordcounts.sort(col('count').desc(), 'word')

    # Write the output as a CSV
    wordcounts.write.csv(output_directory, header=True)

    spark.stop()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: wordcount.py <input_directory> <output_directory>", file=sys.stderr)
        exit(-1)
        
    main(sys.argv[1], sys.argv[2])
