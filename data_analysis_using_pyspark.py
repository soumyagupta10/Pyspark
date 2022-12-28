# -*- coding: utf-8 -*-
"""Data analysis using Pyspark.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AZQG34rf6Q8yvOVlui_ZQSuNDQPKNqix

### Mount the google drive
"""

from google.colab import drive
drive.mount('/content/drive')

"""
Installing pyspark module"""

!pip install pyspark

"""Importing the modules """

from pyspark.sql import SparkSession
from pyspark.sql.functions import count, desc , col, max ,struct
import matplotlib.pyplot as plts

"""Creating spark session"""

spark = SparkSession.builder.appName('spark_app').getOrCreate()

spark

"""
Importing the *Listenings.csv* file: """

# listening_csv_path = spark.read.csv('/content/drive/MyDrive/dataset/listenings.csv')
listening_df = spark.read.option('header',True).csv('/content/drive/MyDrive/dataset/listenings.csv')

"""Let's check the data:"""

listening_df.show()

"""*let*'s delete useless columns:"""

listening_df = listening_df.drop('date')

"""drop the null rows:"""

listening_df = listening_df.na.drop()

listening_df.show()

"""let's see the schema: """

listening_df.printSchema()

"""let's see the shape of our dataframe: """

shape = (listening_df.count(),len(listening_df.columns))
print(shape)

"""

**Query #0:**
select two columns: track and artist"""

q0 = listening_df.select('artist','track')
q0.show()

"""

**Query #1**: Let's find all of the records of those users who have listened to ***Rihanna***"""

q1 =listening_df.select('user_id').filter(listening_df.artist == 'Rihanna')
q1.show()

"""**Query #2:**

Let's find top 10 users who are fan of ***Rihanna***
"""

q2 = listening_df.select('user_id').filter(listening_df.artist=='Rihanna').groupby('user_id').agg(count('user_id').alias('count')).orderBy(desc('count')).limit(10)
q2.show()

"""**Query #3:**

find top 10 famous tracks 
"""

q3 = listening_df.select('artist','track').groupBy('artist','track').agg(count('track').alias('count')).orderBy(desc('count')).limit(10)
q3.show()

"""**Query #4:**

find top 10 famous tracks of ***Rihanna*** 
"""

q4 = listening_df.select('artist','track').filter(listening_df.artist=='Rihanna').groupBy('track').agg(count('track').alias('count')).orderBy(desc('count')).limit(10)
q4.show()

"""**Query #5:**

find top 10 famous albums 
"""

q5= listening_df.select('album').groupBy('album').agg(count('album').alias('count')).orderBy(desc('count')).limit(10)
q5.show()

q5= listening_df.select('artist','album').groupBy('artist','album').agg(count('*').alias('count')).orderBy(desc('count')).limit(10)
q5.show()

listening_df.show()

"""# Task 4 :
importing the ***genre.csv*** file:
"""

genre_df = spark.read.option('header',True).csv('/content/drive/MyDrive/dataset/genre.csv')

"""let's check the data"""

listening_df.show()

genre_df.show()

"""Let's inner join these two data frames"""

data = listening_df.join(genre_df,how='inner',on='artist')
data.show()

"""**Query #6**

find top 10 users who are fan of ***pop*** music
"""

q6 = data.select('user_id','genre').filter(data.genre=='pop').groupBy('user_id','genre').agg(count('genre').alias('count')).orderBy(desc('count')).limit(10)
q6.show()

"""**Query #7**

find top 10 famous genres
"""

q7= data.select('genre').groupBy('genre').agg(count('genre').alias('count')).orderBy(desc('count')).limit(10)
q7.show()

"""# Task 5:
**Query #8**

find out each user favourite genre
"""

q8_1 = data.select('user_id','genre').groupBy('user_id','genre').agg(count('*').alias('count')).orderBy('user_id')
q8_1.show()

q8_2= q8_1.groupBy('user_id').agg(max(struct(col('count'),col('genre'))).alias('max')).select(col('user_id'),col('max.genre'))
q8_2.show()

"""**Query #9**

find out how many pop,rock,metal and hip hop singers we have

and then visulize it using bar chart 
"""

q9 = genre_df.select('genre').filter((genre_df.genre=='pop')|(genre_df.genre=='rock')|(genre_df.genre=='metal')|(genre_df.genre=='hip hop')).groupBy('genre').agg(count('genre').alias('count'))
q9.show()

"""Now, let's visualize the results using ***matplotlib***"""

q9_list=q9.collect()

labels = [row['genre'] for row in q9_list]
count = [row['count'] for row in q9_list]

count

"""now lets visualize these two lists using a bar chart"""

plts.bar(labels,count)
plts.ylabel('No of singers')
plts.xlabel('Genre')

