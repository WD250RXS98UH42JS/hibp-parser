from multiprocessing import Process
from multiprocessing import cpu_count
import hashlib
import mmap
from datetime import datetime, time
from subprocess import check_output
import os
import sys

def encrypt_string(value):
    # Encrypt data with sha1
    sha_signature = hashlib.sha1(value.encode()).hexdigest()
    return sha_signature

def create_hashes_list(start_value, end_value):
    # Create hashes list from possible input values
    value = start_value
    while (value <= end_value):
        value_hash = encrypt_string(str(value))
        hashes_list.append(value_hash.upper())
        value += 1
    log_info = "Hashes list was created successfully. There are " + \
            str(sum(1 for item in hashes_list)) + \
            " elements saved."
    logger("-1", "COMMON", "INFO", log_info)
    return True

def count_db_file_lines():
    # Get count of lines in db file
    with open(db_file) as file:
        lines_count = sum(1 for line in file)
    log_info = "There are " + str(lines_count) + " lines in DB file."
    logger("-1", "COMMON", "INFO", log_info)
    return lines_count

def get_data_for_analysis(process_index, process_count, file_lines_count):
    # Gets presetted amount of strings from db file
    lines_to_process_count = file_lines_count // process_count
    start_index = lines_to_process_count * process_index + 1
    end_index = start_index + lines_to_process_count - 1
    if file_lines_count - end_index < process_count:
        end_index = file_lines_count
    data = check_output([
		"sed",
		"-n",
        "%s,%sp" % (start_index, end_index),
		db_file
	])
    log_info = "Lines for executing: from " + str(start_index) + " to " + str(end_index)
    logger(process_index, "LOG", "INFO", log_info)
    return data

def search_matches_in_db(process_index):
    # Search matches of hashes in part of db
    data = get_data_for_analysis(process_index, process_count, file_lines_count).split("\n")
    counter = 1
    for item in data:
        hash = item.split(":")[0]
        if hash in hashes_list:
            log_info = [hashes_list.index(hash), hash]
            logger(process_index, "RESULT", "RESULT", log_info)
        else:
            if counter % processed_strings == 0:
                log_info = str(counter) + " entries was compared."
                logger(process_index, "LOG", "PROGRESS", log_info)
        counter += 1
    return True

def logger(process_index, target, code, log_info):
    # Generate info should be logged
    log_msg = ""
    current_time = datetime.now()
    seconds_left = (current_time - start_time).seconds
    if target == "LOG":
        log_msg = str(current_time) + "\t" + \
                code + "\t" + \
                log_info + \
                " Seconds passed: " + str(seconds_left) + "\n"
        log_file = log_path + "process-"+str(process_index)+".log"

    elif target == "RESULT":
        result = str(start_value + log_info[0])
        log_msg = str(current_time) + "\t" + \
                    code + "\t" + \
                    log_info[1] + " - " + \
                    result + "\t" + \
                    " Seconds passed: " + str(seconds_left) + "\n"
        log_file = log_path + "result.log"

    elif target == "COMMON":
        log_msg = str(current_time) + "\t" + \
                code + "\t" + \
                log_info + \
                " Seconds passed: " + str(seconds_left) + "\n"
        log_file = log_path + "common.log"

    with open(log_file, 'a+') as file:
        file.write(log_msg)
    print(log_msg)

####################################################################################
# You can set values in this section

# Path to db file (including file name)
db_file = '3.txt'
# Path to logs folder (without file name)
log_path = 'logs/'
# First value in values array
start_value = 9166800000
# End value in values array
end_value = 9166899999
# Number of processed strings to create log record about
processed_strings = 100000
####################################################################################

# Do not change this variables!

# Get current time for further calculations
start_time = datetime.now()
# List contains finded values
items = []
# List contains all possible values hashes
hashes_list = []


# Create folder for logs
try:
    os.mkdir(log_path)
except OSError:
    print ("Creation of the directory %s failed" % log_path)
    sys.exit(1)

create_hashes_list_result = create_hashes_list(start_value, end_value)
if create_hashes_list_result:
    file_lines_count = count_db_file_lines()
    process_count = cpu_count()
    for process_index in range (0, process_count):
        try:
            p = Process(target=search_matches_in_db, args=(process_index,))
            # p.daemon = True
            p.start()
        except Exception as e:
            logger(process_index, "LOG", "ERROR", e)