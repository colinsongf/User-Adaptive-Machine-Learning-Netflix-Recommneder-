
import csv
import math


def fetch_movie_titles(year):
	filename = 'Netflix_Dataset\download\movie_titles.txt'
	
	with open(filename, 'r') as file:
		movie = {}
		for line in file:
			data = line.strip().split(',')
			if data[1] in year:
				movie[data[0]] = data[2]
	return movie
	
def create_data_file(movie):

	path = 'Netflix_Dataset\download\training_set\mv_'
	
	datafile = open('movie_data.txt', 'w')
	
	for key in movie:
		suff = key.zfill(7)
		filename = path + suff + '.txt'
		with open(filename, 'r') as file:
			next(file)
			for line in file:
				data = line.strip().split(',')
				datafile.write(key+','+data[0]+','+data[1]+'\n')
	datafile.close()

def create_data_file2(meanstd):

	datafile = open('movie_data_normalized.txt', 'w')
	
	meanfile = open('mean_std.txt', 'w')
	
	with open('movie_data.txt', 'r') as file:
			for line in file:
				data = line.strip().split(',')
				normscore = 0
				if meanstd[data[1]][1] > 0:
					normscore = round((float(data[2]) - meanstd[data[1]][0])/meanstd[data[1]][1], 2)
				else:
					normscore = data[2]
				datafile.write(data[0]+','+data[1]+','+str(normscore) +'\n')
				meanfile.write(str(meanstd[data[1]][0])+','+str(meanstd[data[1]][1])+'\n')
	datafile.close()
	meanfile.close()
	
def calculate_user_mean():
	user = {}
	with open('movie_data.txt', 'r') as file:
		for line in file:
			data = line.split(',')
			if data[1] not in user:
				user[data[1]] = (int(data[2]), 1)
			else:
				temp = user[data[1]]
				user[data[1]] = (temp[0] + int(data[2]), temp[1] + 1)
	
	usermean = {}
	for key in user:
		temp = user[key]
		usermean[key] = round(float(temp[0])/temp[1],2)
	
	userstd = {}
	with open('movie_data.txt', 'r') as file:
		for line in file:
			data = line.split(',')
			if data[1] not in userstd:
				userstd[data[1]] = pow(float(data[2]) - usermean[data[1]],2)
			else:
				userstd[data[1]] = userstd[data[1]] + pow(float(data[2]) - usermean[data[1]],2)
	
	meanstd = {}
	for key in user:
		meanstd[key] = (usermean[key], round(math.sqrt(userstd[key]/user[key][1]),2), user[key][1])
		
	print len(meanstd)
	
	return meanstd
	
def main():
	#movie = fetch_movie_titles(['2005'])
	#create_data_file(movie)
	meanstd = calculate_user_mean()
	create_data_file2(meanstd)

if __name__=="__main__":
    	main()