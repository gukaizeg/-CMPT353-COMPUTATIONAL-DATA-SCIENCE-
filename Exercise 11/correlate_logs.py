import sys
assert sys.version_info >= (3, 8)  # make sure we have Python 3.8+
from pyspark.sql import SparkSession, functions, types, Row
import re

line_re = re.compile(r"^(\S+) - - \[\S+ [+-]\d+\] \"[A-Z]+ \S+ HTTP/\d\.\d\" \d+ (\d+)$")


def line_to_row(line):
    m = line_re.match(line)
    if m:
        return Row(hostname=m.group(1), bytes_transferred=int(m.group(2)))
    else:
        return None


def not_none(row):
    return row is not None


def create_row_rdd(in_directory, spark):
    log_lines = spark.sparkContext.textFile(in_directory)
    rows = log_lines.map(line_to_row).filter(not_none)
    return rows


def main(in_directory):
    spark = SparkSession.builder.appName('correlate logs').getOrCreate()
    assert spark.version >= '3.2'  # make sure we have Spark 3.2+
    spark.sparkContext.setLogLevel('WARN')

    logs = spark.createDataFrame(create_row_rdd(in_directory, spark))

    logs = logs.groupBy('hostname').agg(functions.count('*').alias('requests'), functions.sum('bytes_transferred').alias('total_bytes'))

    # calculate the sums required for the correlation coefficient formula
    sums = logs.groupBy().agg(
        functions.count('*').alias('n'),
        functions.sum('requests').alias('sum_x'),
        functions.sum('total_bytes').alias('sum_y'),
        functions.sum(functions.col('requests')*functions.col('requests')).alias('sum_x2'),
        functions.sum(functions.col('total_bytes')*functions.col('total_bytes')).alias('sum_y2'),
        functions.sum(functions.col('requests')*functions.col('total_bytes')).alias('sum_xy'),
    ).first()

    # calculate the correlation coefficient
    numerator = sums.n * sums.sum_xy - sums.sum_x * sums.sum_y
    denominator = ((sums.n * sums.sum_x2 - sums.sum_x**2) * (sums.n * sums.sum_y2 - sums.sum_y**2))**0.5

    r = numerator / denominator

    print(f"r = {r}\nr^2 = {r*r}")




if __name__=='__main__':
    in_directory = sys.argv[1]
    spark = SparkSession.builder.appName('correlate logs').getOrCreate()
    assert spark.version >= '3.2' # make sure we have Spark 3.2+
    spark.sparkContext.setLogLevel('WARN')

    main(in_directory)