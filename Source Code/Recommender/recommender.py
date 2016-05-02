import random
from operator import *
from shutil import *
import itertools
import math
import sys

#if len(sys.argv) != 2:
    #print "Enter valid function type"
    #exit(1)
#function = sys.argv[1]

usermovies = []
netflix_list={}
all_movie_list=[]
movie = {}

def load_data(filename, user):
	f=open(filename)
	
	for line in f:
		data = line.strip().split(',')
		data[0]=int(data[0].strip())
		data[1]=int(data[1].strip())
		all_movie_list.append(data[0])
		if data[1] == user:
			usermovies.append((data[0], int(data[2])))
		if data[0] not in netflix_list.keys():
			netflix_list[data[0]]={int(data[1]):int(data[2])}
		else:
			netflix_list[data[0]].update({int(data[1]):int(data[2])})
			
#Calculate Similarity score based on the eucledian distance.
def calculate_similarity(movie1,movie2):
    eucledian_distance=[]
    for movie in netflix_list[movie1]:
      if movie in netflix_list[movie2]:
        eucledian_distance.append(pow(int(netflix_list[movie1][movie]) - int(netflix_list[movie2][movie]),2))

    sum_eucledian_distance=sum(eucledian_distance)

    if sum_eucledian_distance==0:
        return 0
    else:
        return 1/(1+math.sqrt(sum_eucledian_distance))
		
def calculate_pearson_coefficient(movie1,movie2):
    movie_list=[]
    for movie in netflix_list[movie1]:
	    if movie in netflix_list[movie2]:
                movie_list.append(movie)


    movie_count= float(len(movie_list))

#If they have no ratings in common, return 0
    if movie_count==0.0:
        return 0

    sum1=0.0
    sum2=0.0

#Add up all the preferences
    for movie in movie_list:
	    sum1= sum1+ netflix_list[movie1][movie]

    for movie in movie_list:
	    sum2= sum2+ netflix_list[movie2][movie]


#Sum up the squares
    for movie in movie_list:
	    sum1_squares= sum1+ pow(netflix_list[movie1][movie],2)

    for movie in movie_list:
	    sum2_squares= sum2+ pow(netflix_list[movie2][movie],2)

    product=0.0

#Sum up the products
    for movie in movie_list:
	    product= product + netflix_list[movie1][movie] * netflix_list[movie2][movie]

    numerator=0.0
    denominator=0.0
    numerator= (product - (sum1*sum2)/movie_count)
    denominator=math.sqrt((sum1_squares/movie_count-pow(sum1,2)/movie_count*movie_count)*(sum2_squares/movie_count- pow(sum2,2)/movie_count*movie_count))

    if denominator==0.0:
        return 0
    return numerator/denominator
	
def top_similar_movies(movie,n,function=calculate_similarity):
    similarity_scores=[]
    for other_movie in netflix_list:
        if other_movie!=movie:
            similarity_scores.append([function(movie,other_movie),other_movie])

    similarity_scores.sort()
    similarity_scores.reverse()
    
    return similarity_scores[:n]
	
			
def recommend_movies(user, n):
	
	sim_movies = []
	
	for i in range(len(usermovies)):
		rec = top_similar_movies(int(usermovies[i][0]), 5)
		for entry in rec:
			sim_movies.append((entry[0]*usermovies[i][1], entry[1]))
	sim_movies.sort()
	sim_movies.reverse()
	
	for i in range(n):
		print movie[sim_movies[i][1]]

def fetch_movie_titles(year):
	filename = 'movie_titles.txt'
	
	with open(filename, 'r') as file:
		for line in file:
			data = line.strip().split(',')
			if data[1] in year:
				movie[int(data[0])] = data[2]	

def main():
	load_data("movie_data.txt", 2020475)
	fetch_movie_titles(['2005'])
	recommend_movies(2020475, 5)
	



if __name__=="__main__":
	main()