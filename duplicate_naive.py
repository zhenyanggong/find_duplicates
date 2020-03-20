import string
import sys
import os
import random
import collections
import csv
random.seed(3)

def get_command():
# get command line argument
	input_path = ""
	output_path = ""
	k = 0
	for i in range(len(sys.argv)):
		if sys.argv[i] == "--input_path":
			i += 1
			input_path = sys.argv[i]
		elif sys.argv[i] == "--output_path":
			i += 1
			output_path = sys.argv[i]
		elif sys.argv[i] == "-k":
			i += 1
			k = int(sys.argv[i])
	return input_path, output_path, k

def n_gram(input_data, k):
	sh = []
	if int(len(input_data)) >= k:
		for pos, token in enumerate(input_data):
			if pos + k <= len(input_data):
				sh.append(input_data[pos:pos + k])
		return sh
	else:
		printf("n_gram error")
	pass 

def get_shingle(input_path, k):
	total_shingle = []
	shingle_map = {}
	txt_files = []
	with open(input_path) as f:
		txt_files = f.readlines()
	txt_files = [x.strip() for x in txt_files]
	for file_path in txt_files:
		with open(file_path, 'rb') as file:

			#print(input_path+'/'+file_path)
			data = file.read()
			#print(data)
			shingles = n_gram(data, k)
			file_path = file_path.split('/')[1]
			file_index = int(file_path.split('.')[0])
			# save key as file number
			shingle_map[file_index] = shingles
			for i in shingles:
				if i not in total_shingle:
					total_shingle.append(i)
			#total_shingle = total_shingle.union(shingles)
	#print(shingle_map)
	#print(len(total_shingle))
	return total_shingle, shingle_map, len(txt_files)

def matrix(shingle_map, total_shingle):
	binary_matrix = {}
	for key, value in shingle_map.items():
		binary_list = []
		for shingle in total_shingle:
			if shingle in value:
				binary_list.append(1) 
			else:
				binary_list.append(0)
		binary_matrix[key] = binary_list
	#print(binary_matrix)
	return binary_matrix

def candidate(shingle_map):
	candidate_dict = dict()
	key_list = list(shingle_map.keys())
	#print(key_list)
	# find candidate pair
	for key in key_list:
		candidate_dict[key] = key_list
		#candidate_dict[key].remove(key)
		candidate_dict[key] = [x for x in candidate_dict[key] if x != key]
	#print(candidate_dict)
	return candidate_dict

def similarity(data1, data2):
	if len(data1) != len(data2):
		printf('similarity error') 
	union = 0.0
	common = 0.0
	result = 0.0
	for i in range(len(data1)):
		if (data1[i] == 1 or data2[i] == 1):
			union += 1.0
		if (data1[i] == 1 and data2[i] == 1):
			common += 1.0
	result = common / union
	#if result > 0.7:
		#print(result)
	return result

def duplicate(candidate_dict, signatures):
	for key, values in candidate_dict.items():
		if len(values) == 0:
			candidate_dict[key].append(-1)
		else:
			for value in values:
				#print(value)
				#print(key)
				if similarity(signatures[key], signatures[value]) < 0.7:
					candidate_dict[key] = [x for x in candidate_dict[key] if x != value]
		if len(candidate_dict[key]) == 0:
			candidate_dict[key].append(-1)
	return candidate_dict

def main():
# wirete main here
	input_path, output_path, k = get_command()
	total_shingle, shingle_map, number_file = get_shingle(input_path, k)
	#print('number of file')
	#print(number_file)
	shingle_matrix = matrix(shingle_map, total_shingle)
	candidate_dict = candidate(shingle_matrix)
	duplicate_dict = duplicate(candidate_dict, shingle_matrix)
	od = collections.OrderedDict(sorted(duplicate_dict.items()))
	with open(output_path,'w') as file:
		writer = csv.writer(file)
		for key, value in od.items():
			value.sort();
			temp = "";
			for i in value:
				temp += str(i)
				temp += " "
			temp = temp[:-1]
			writer.writerow([key, temp])

	file.close()


if __name__ == '__main__':
	main()
