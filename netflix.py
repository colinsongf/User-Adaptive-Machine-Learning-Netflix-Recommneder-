import random
from operator import *
from shutil import *
import itertools
import math
#from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating


f=open("/home/rajadhva/Machine_Learning/movie_data.txt")

netflix_list={}
all_movie_list=[]
for line in f:
    data = line.strip().split(',')
    data[0]=int(data[0].strip())
    #print data[0]
    all_movie_list.append(int(data[1]))
    if data[0] not in netflix_list.keys():
        netflix_list[data[0]]={int(data[1]):int(data[2])}
    else:
        netflix_list[data[0]].update({int(data[1]):int(data[2])})
    #print data[0] + " " + data[1] + " " + data[2]

print netflix_list[14518]

i=0
for x,y in netflix_list.items():
    print x
    print y
    print netflix_list[x]
    i+=1
    if i==5:
        break;

#for x in xrange(0,5):
 #   print netflix_list[i]
'''
random.shuffle(netflix_list)
trainData=netflix_list[:40]
validationData=netflix_list[40:80]
testData=netflix_list[80:]

i=0
for x in xrange(0,5):
    print testData[i]
    i+=1

#print trainData
'''
#Calculate Similarity score based on the eucledian distance.

def calculate_similarity(user1,user2):
    eucledian_distance=[]
    for movie in netflix_list[user1]:
      if movie in netflix_list[user2]:
        eucledian_distance.append(pow(int(netflix_list[user1][movie]) - int(netflix_list[user2][movie]),2))

    sum_eucledian_distance=sum(eucledian_distance)

    if sum_eucledian_distance==0:
        return 0
    else:
        return 1/(1+math.sqrt(sum_eucledian_distance))


#print calculate_similarity(13759,8210)

def calculate_pearson_coefficient(user1,user2):
    movie_list=[]
    for movie in netflix_list[user1]:
	    if movie in netflix_list[user2]:
                movie_list.append(movie)


    movie_count= float(len(movie_list))
    print movie_count
#If they have no ratings in common, return 0
    if movie_count==0.0:
        return 0
    sum1=0.0
    sum2=0.0
#Add up all the preferences
    for movie in movie_list:
	    sum1= sum1+ netflix_list[user1][movie]

    for movie in movie_list:
	    sum2= sum2+ netflix_list[user2][movie]


#Sum up the squares
    for movie in movie_list:
	    sum1_squares= sum1+ pow(netflix_list[user1][movie],2)

    for movie in movie_list:
	    sum2_squares= sum2+ pow(netflix_list[user2][movie],2)
    #print sum1
    #print sum2
    product=0.0
#Sum up the products
    for movie in movie_list:
	    product= product + netflix_list[user1][movie] * netflix_list[user2][movie]
    #print product
    numerator=0.0
    denominator=0.0
    numerator= (product - (sum1*sum2)/movie_count)
    #print numerator
    denominator=math.sqrt((sum1_squares/movie_count-pow(sum1,2)/movie_count*movie_count)*(sum2_squares/movie_count- pow(sum2,2)/movie_count*movie_count))
    print denominator

    if denominator==0.0:
        return 0
    return numerator/denominator


#print calculate_pearson_coefficient(13759,10250)


def top_similar_users(user,n,function=calculate_pearson_coefficient):
    similarity_scores=[]
    for other_user in netflix_list:
        if other_user!=user:
            #print(function(user,other_user))
            similarity_scores.append([function(user,other_user),other_user])

    similarity_scores.sort()
    similarity_scores.reverse()
    for x in range(0,n):
        print similarity_scores[x]

    similarity_scores[:n]

top_similar_users(17,3)

def final_recommendations(user,n,function=top_similar_users):
    unique_movies=set(all_movie_list)
    temp_list=netflix_list[user]
    user_movies=temp_list.keys()
    different_movies=[]
    different_movies=unique_movies-user_movies

    similar_users=top_similar_users(user,10)

    for movie in different_movies:
        for user in similar_users:




