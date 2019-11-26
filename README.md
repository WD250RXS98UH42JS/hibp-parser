# Have I Been Pwned? passwords database parser

This script checks the values of predefined numeric array are exist in Have I Been Pwned? passwords database.
It can be useful for security research or if you want to check leakages of your own numeric passwords.

The largest passwords DB file is about ~25 GB when unarchived - it's about ~555M strings there. It's very huge amount of data which can takes a lot of time to be parsed.
This script was created to process data in multi-processing mode - it checks available CPU threads and creates the same number of threads to process data faster.
Also, script are speed and memory optimized.

## Customization possibilities
If you want to optimize this code for your needs, essential things you should change are ***search_matches_in_db()*** and ***create_hashes_list()*** methods. 
**create_hashes_list()** method takes start_value and end_value variables, iterates over that range and creates list of SHA-1 hashes. It can be easily changed to make hashes list using alphanumeric values stored in list, external file or something else.
**search_matches_in_db()** method strictly working only with data represents the same as entries of Have I Been Pwned database. It iterates over all entries in DB data, and compares it's value with every item stored in hashes_list. In case of matching, log entry will be created and echoed.

## Processing time
It's highly recommended to use GCP, AWS or any cloud provider's virtualization features to run this script instead of local running to significally decreasing processing time.

### Example
**Cloud provider:** GCP
**VM type:** N2 Custom, 12 CPU / 8-10+ GB RAM
**Region:** europe-west1 (Belgium)
**Zone:** europe-west1-b
**Hourly rate:** about $0.382

**Data:** ~7 GB
**Data entries:** ~170M

**Average CPU load:** 100%
**Average Mem load:** ~6,5 GB
**Time to process:** ~11000 sec (about 3 hours)

![Example](https://github.com/WD250RXS98UH42JS/hibp-parser/raw/master/images/1.png "htop")

![Example](https://github.com/WD250RXS98UH42JS/hibp-parser/raw/master/images/2.png "logs")

## Usage

Get sources
```bash
git clone https://github.com/WD250RXS98UH42JS/hibp-parser.git
```

Go to project folder and place there database file which can be founded here: [Have I Been Pwned? Passwords](https://haveibeenpwned.com/Passwords)
Its preferred to use database in SHA-1 format, which ordered by prevalence.

Also you need to setup these values in main.py:
```python
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
```

After doing all changes just run this script using Python 2:
```bash
python2 ./main.py
```
