#!/bin/bash
#MSCK repair commands for inrix and wavetronix 2021 and 2020 tables
aws athena start-query-execution --query-string "MSCK REPAIR TABLE inrix.inrix2020" --result-configuration "OutputLocation=s3://intrans-feed/Athena/"

aws athena start-query-execution --query-string "MSCK REPAIR TABLE inrix.inrix2021" --result-configuration "OutputLocation=s3://intrans-feed/Athena/"

aws athena start-query-execution --query-string "MSCK REPAIR TABLE wavetronix.wavetronix2020" --result-configuration "OutputLocation=s3://intrans-feed/Athena/"

aws athena start-query-execution --query-string "MSCK REPAIR TABLE wavetronix.wavetronix2021" --result-configuration "OutputLocation=s3://intrans-feed/Athena/"
