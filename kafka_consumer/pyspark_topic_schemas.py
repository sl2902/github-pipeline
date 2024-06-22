from pyspark.sql.types import (
    StructType, 
    StructField, 
    StringType, 
    IntegerType, 
    LongType, 
    BooleanType, 
    TimestampType,
    DateType
)

# Define the PySpark schema
spark_schemas = {
    "commits":  StructType([
                    StructField("owner", StringType(), True),
                    StructField("repo", StringType(), True),
                    StructField("commit_sha", StringType(), True),
                    StructField("url", StringType(), True),
                    StructField("comment_count", IntegerType(), True),
                    StructField("commit_message", StringType(), True),
                    StructField("author_id", LongType(), True),
                    StructField("author_login", StringType(), True),
                    StructField("author_type", StringType(), True),
                    StructField("author_name", StringType(), True),
                    StructField("commit_author_date", TimestampType(), True),
                    StructField("commit_author_email", StringType(), True),
                    StructField("committer_id", LongType(), True),
                    StructField("committer_login", StringType(), True),
                    StructField("committer_type", StringType(), True),
                    StructField("committer_name", StringType(), True),
                    StructField("commit_committer_date", TimestampType(), True),
                    StructField("commit_committer_email", StringType(), True),
                    StructField("commit_verification_reason", StringType(), True),
                    StructField("commit_verification_verified", BooleanType(), True),
                    StructField("response", StringType(), True),
                    StructField("created_date", TimestampType(), True)
                ]),
    "issues":   StructType([
                    StructField("owner", StringType(), True),
                    StructField("repo", StringType(), True),
                    StructField("id", LongType(), True),
                    StructField("number", LongType(), True),
                    StructField("title", StringType(), True),
                    StructField("state", StringType(), True),
                    StructField("created_at", TimestampType(), True),
                    StructField("updated_at", TimestampType(), True),
                    StructField("closed_at", TimestampType(), True),
                    StructField("comments", LongType(), True),
                    StructField("draft", BooleanType(), True),
                    StructField("author_association", StringType(), True),
                    StructField("user_id", LongType(), True),
                    StructField("label_id", LongType(), True),
                    StructField("repository_url", StringType(), True),
                    StructField("total_count", IntegerType(), True),
                    StructField("plus1", IntegerType(), True),
                    StructField("minus1", IntegerType(), True),
                    StructField("laugh", IntegerType(), True),
                    StructField("hooray", IntegerType(), True),
                    StructField("confused", IntegerType(), True),
                    StructField("heart", IntegerType(), True),
                    StructField("rocket", IntegerType(), True),
                    StructField("eyes", IntegerType(), True),
                    StructField("response", StringType(), True),
                    StructField("created_date", TimestampType(), True)
    ])

}