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
	n = 0
	p = 0
	r = 0
	b = 0
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
		elif sys.argv[i] == "-n":
			i += 1
			n = int(sys.argv[i])
		elif sys.argv[i] == "-p":
			i += 1
			p = int(sys.argv[i])
		elif sys.argv[i] == "-r":
			i += 1
			r = int(sys.argv[i])
		elif sys.argv[i] == "-b":
			i += 1
			b = int(sys.argv[i])
	return input_path, output_path, k, n, p, r, b

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
	#print(txt_files)
	for file_path in txt_files:
		with open(file_path, 'r') as file:

			#print(input_path+'/'+file_path)
			data = file.read()
			#print(data)
			shingles = n_gram(data, k)
			file_path = file_path.split('/')[1]
			file_index = int(file_path.split('.')[0])
			# save key as file number
			# print(file_index)
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

def calculate_sig(colunm, a, b, m, p):
	sig = sys.maxsize;
	temp = 0
	for idx, val in enumerate(colunm):
		if val == 1:
			temp = (((a * idx) + b) % p) % m
			if temp < sig:
				sig = temp
	return sig


def minhash(binary_matrix, n, p):
	signatures = {}
	for key, value in binary_matrix.items():
			signatures[key] = []
	for i in range(n):
		a = random.randint(0, p)
		b = random.randint(0, p)
		for key, value in binary_matrix.items():
			m = len(value)
			sig = calculate_sig(value, a, b, m, p)
			signatures[key].append(sig)
	#print(signatures)
	return signatures


def lsh(signatures, r, b):
	lsh_dict = {}
	for key, value in signatures.items():
		for pos, sig in enumerate(value):
			if (pos + r <= len(value)) and (pos % r) == 0:
				# hashket is string = first row position + values
				hashkey = ""
				hashkey = str(pos) + ','
				for i in range(r):
					hashkey += str(value[pos + i])
				if hashkey in lsh_dict:
					lsh_dict[hashkey].append(key)
				else:
					lsh_dict[hashkey] = [key]
	# print(lsh_dict)
	return lsh_dict

def candidate(lsh_dict, number_file):
	candidate_dict = {}
	# find candidate pair
	for key, values in lsh_dict.items():
		if len(values) > 1:
			for value1 in values:
				for value2 in values:
					if value1 != value2:
						if value1 not in candidate_dict:
							candidate_dict[value1] = [value2]
						else:
							if value2 not in candidate_dict[value1]:
								candidate_dict[value1].append(value2)
		else:
			# fill dict
			if values[0] not in candidate_dict:
				candidate_dict[values[0]] = []
	#print(candidate_dict)
	return candidate_dict

def similarity(data1, data2):
	if len(data1) != len(data2):
		printf('similarity error') 
	union = len(data1)
	common = 0.0
	result = 0.0
	for i in range(len(data1)):
		if (data1[i] == data2[i]):
			common += 1.0
	result = common / union
	#print(result)
	return result

def duplicate(candidate_dict, signatures):
	duplicate_dict = {}
	for key, values in candidate_dict.items():
		duplicate_dict[key] = []
		if len(values) == 0:
			duplicate_dict[key].append(-1)
		else:
			for value in values:
				if similarity(signatures[key], signatures[value]) > 0.7:
					duplicate_dict[key].append(value)
		if len(duplicate_dict[key]) == 0:
			duplicate_dict[key].append(-1)
	return duplicate_dict

def main():
# wirete main here
	input_path, output_path, k, n, p, r, b = get_command()
	total_shingle, shingle_map, number_file = get_shingle(input_path, k)
	#print('number of file')
	#print(number_file)
	shingle_matrix = matrix(shingle_map, total_shingle)
	signatures = minhash(shingle_matrix, n, p)
	lsh_dict = lsh(signatures, r,  b)
	candidate_dict = candidate(lsh_dict, number_file)
	duplicate_dict = duplicate(candidate_dict, signatures)
	od = collections.OrderedDict(sorted(candidate_dict.items()))
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