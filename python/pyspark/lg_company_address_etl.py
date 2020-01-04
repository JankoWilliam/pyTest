from pyspark.context import SparkContext
from pyspark import SparkConf,HiveContext

conf = SparkConf.setAppName("py_test")
sc = SparkContext(conf)
hiveContext = HiveContext(sc)

hiveContext.sql("select company_name,company_place  from ci_ods.ods_spider_recruit_lg_content").write.mode("overwrite").saveAsTable("tmp.tmp_spider_recruit_lg_address")


