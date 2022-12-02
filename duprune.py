from sys import argv
import hashlib
import os

# This creates a unique identifier for data in each file
# It returns hashied md5 + sha1 string of file data. 
# Data needs to be a file.read() object
def hash_data(data):
	# instantiate the hashing objects
	md5 = hashlib.md5()
	sha1 = hashlib.sha1()

	# hash the file data
	md5.update(data)
	sha1.update(data)

	# return the hashes as a contatinated string
	hashed_string = str(md5.hexdigest()) + ' : ' + str(sha1.hexdigest())
	return hashed_string

# This is the main function call
def main():

	# validate an argument has been given (might convert to argparse for ease)
	if len(argv) > 1:

		# These are just for storing metrics
		files = []
		checked = []
		duplicate = []

		# setting path variables
		unique_fp = 'unique_files'
		files = os.listdir(argv[1])

		# remove file incase it already exists and create new file
		os.system('rm -rf '+unique_fp)
		print('[+] Creating folder for unique files')
		os.system('mkdir '+unique_fp)

		print('[+] Hashing, identifying duplicates, and copying unique files')
		# loop through the filenames
		for i in files:
			
			# store full path for the file
			file_path = argv[1] +'/'+ i

			# do not try to open the directory just created
			if argv[1]+i != argv[1]+unique_fp:

				# Open the file as read binary
				with open(file_path, 'rb') as f:

					# Sanitize the filepath of formatted characters
					file_path = file_path.replace('(', '\(').replace(')', '\)').replace(' ', '\ ')

					# read in the file and get the hashed data
					data = f.read()
					hashed_string = hash_data(data)

					# If the file is new -> add to checked & copy it to new directory
					if hashed_string not in checked:
						checked.append(hashed_string)
						os.system('cp '+file_path+' '+unique_fp)

						# debugging 
						if '-v' in argv:
							print(i + ':\t'+hashed_string + ' (new)')
							# print('[+] Copying unique file: '+i)

					# If file is not new -> add to duplicated
					elif hashed_string in checked:
						duplicate.append(hashed_string)

						# debugging
						if '-v' in argv:
							print(i + ':\t'+hashed_string + ' (DUPLICATE)')

					# close file and move onto next in array
					f.close()

		# Once complete print out some metrics and filepath of unique files
		print('\n[+] *PROCESSING DONE* RESULTS:')
		print('[+] \tUnique files found:    ',len(checked))
		print('[+] \tDuplicate files found: ',len(duplicate))
		print('[+] \tOutput location:       ',argv[1]+'/'+unique_fp)

	# argument not specified -> print usage
	else:
		print('[-] ERROR: File Path not specifie in arguments')
		print('[+] Usage: duprune.py <file_path> [-v]')
		print('[+] requirements: hashlib')


# if not imported -> call main
if __name__ == '__main__':
	print('   //////////////////////////////////////////')
	print('  // Developed Tiernan Hilley AKA cy3rtea //')
	print(' //  [+] Launching Duprune...            //')
	print('//////////////////////////////////////////\n')
	main()

# if imported -> print this out
else:
	print('   //////////////////////////////////////////')
	print('  //[+] Successfully imported duprune.py  //')
	print(' // Developed Tiernan Hilley AKA cy3rtea //')
	print('//////////////////////////////////////////\n')