import sys
assert sys.version_info >= (3, 8) # make sure we have Python 3.8+
from pyspark.sql import SparkSession, functions, types

comments_schema = types.StructType([
    types.StructField('archived', types.BooleanType()),
    types.StructField('author', types.StringType()),
    types.StructField('author_flair_css_class', types.StringType()),
    types.StructField('author_flair_text', types.StringType()),
    types.StructField('body', types.StringType()),
    types.StructField('controversiality', types.LongType()),
    types.StructField('created_utc', types.StringType()),
    types.StructField('distinguished', types.StringType()),
    types.StructField('downs', types.LongType()),
    types.StructField('edited', types.StringType()),
    types.StructField('gilded', types.LongType()),
    types.StructField('id', types.StringType()),
    types.StructField('link_id', types.StringType()),
    types.StructField('name', types.StringType()),
    types.StructField('parent_id', types.StringType()),
    types.StructField('retrieved_on', types.LongType()),
    types.StructField('score', types.LongType()),
    types.StructField('score_hidden', types.BooleanType()),
    types.StructField('subreddit', types.StringType()),
    types.StructField('subreddit_id', types.StringType()),
    types.StructField('ups', types.LongType()),
    #types.StructField('year', types.IntegerType()),
    #types.StructField('month', types.IntegerType()),
])


def main(in_directory, out_directory):
    comments = spark.read.json(in_directory, schema=comments_schema)

    avg_scores_df = comments.groupBy("subreddit").agg(functions.avg("score").alias("avg_score"))

    avg_scores_df = avg_scores_df.filter(avg_scores_df["avg_score"] > 0)

    comments_with_avg = comments.join(avg_scores_df, "subreddit")
    comments_with_rel_score = comments_with_avg.withColumn("rel_score", comments_with_avg["score"] / comments_with_avg["avg_score"])

    max_rel_scores_df = comments_with_rel_score.groupBy("subreddit").agg(functions.max("rel_score").alias("max_rel_score"))

    best_comments_df = comments_with_rel_score.join(max_rel_scores_df, "subreddit").filter(comments_with_rel_score["rel_score"] == max_rel_scores_df["max_rel_score"])

    best_comments_df.select("subreddit", "author", "rel_score").write.mode('overwrite').json(out_directory, compression="none")


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    spark = SparkSession.builder.appName('Reddit Relative Scores').getOrCreate()
    assert spark.version >= '3.2' # make sure we have Spark 3.2+
    spark.sparkContext.setLogLevel('WARN')

    main(in_directory, out_directory)
