  #!/usr/bin/env python
VERSION='1.0.0'
SCRIPTNAME='Motion Cleaner'
import os, sys, time, datetime

# Name: DB Backup

# Author: Oscar Söderholm

# Email: oscar@lycan.se

# Date: 2012-12-19

# Dependencies: Python

#

# Suggested place for execution:

# flags: chmod+x

##### OPTIONS #####

SEPARATION_MODE = True # Set to FALSE to create a single file containing all databases.

KEEP_MAX_DAYS = 5 # NUMBER OF DAYS TO KEEP BACKUPS. (Zero keeps all)
USE_BZIP2 = True # IF TRUE WILL COMPRESS DUMP USING BZIP2
USE_LOG = True # TURN LOGGING TO FILE ON OR OFF
UPLOAD_MOTION_PICS = False
UPLOAD_MOTION_VIDS = False
UPLOAD_SNAPSHOTS = False
UPLOAD_TIMELAPSE = False

##### VARIABLES #####

SNAPSHOTS = /motion/snapshots
MOTION_PICS = /motion/motion_pics
MOTION_VIDS = /motion/motion_vid
TIMELAPSE = /motion/timelapse

LOGFILE = '/var/log/db_backup.log' # PATH TO LOGFILE.
BACKUP_DIRECTORY='/backups' # DIRECTORY WHERE THE BACKUPS WILL BE KEPT
DB_USER = 'root' # A MYSQL USER THAT HAS SUFFICIENT PRIVILEGES
DB_PASS = '' # PASSWORD FOR THE USER

DATABASES = [ # ARRAY OF DATABASES TO BE BACKED UP IF RUNNING IN SEPARATION MODE

'mysql',
'test'
]

### FUNCTIONS

#-------------------------------------------------------------------------------------------

def log(message):
if USE_LOG == True:
f = open(LOGFILE, 'a')
f.write('\t'+message+'\n')
f.close()

#-------------------------------------------------------------------------------------------

def now():
return datetime.datetime.now()

#-------------------------------------------------------------------------------------------

def createDateDir():
dirName = str(BACKUP_DIRECTORY)+'/'+str(now())[:10]
if not os.path.exists(dirName):
os.makedirs(dirName)
os.chdir(dirName)
log('* STORING TO FOLDER: \t\t\t'+str(dirName)+'\n')

#-------------------------------------------------------------------------------------------

def checkdate():
#if date is monday
#if date is TUESday
#if date is wednsday
#if date is thursday
#if date is friday
#if date is saturday
#if date is sunday

def dumpDB():
if SEPARATION_MODE == False:
db_bak_file = 'databases.'+str(now())[:10]+'.sql'
log('$ DUMPING ALL DATABASES\t\t\t->\t'+str(db_bak_file))

os.system("mysqldump --all-databases -u "+DB_USER+" -p"+DB_PASS+" > "+db_bak_file)

if USE_BZIP2:
os.system("bzip2 "+db_bak_file)
log('$ COMPRESSED '+str(db_bak_file)+'\t->\t'+str(db_bak_file)+'.bz2')
else:
for database in DATABASES:
db_bak_file = database+'.'+str(now())[:10]+'.sql'
log('$ DUMPING\t'+str(database)+'\t\t\t->\t'+str(db_bak_file))
os.system("mysqldump -u "+DB_USER+" -p"+DB_PASS+" "+database+" > "+db_bak_file)
if USE_BZIP2:
os.system("bzip2 "+db_bak_file)
log('$ COMPRESSED\t'+str(db_bak_file)+'\t->\t'+str(db_bak_file)+'.bz2')

#-------------------------------------------------------------------------------------------

def cleaner():
if KEEP_MAX_DAYS == 0:
pass
else:
log('\n\t$ CHECKING IF CLEANING IS NEEDED')
for item in os.listdir(BACKUP_DIRECTORY):
if os.path.isdir(os.path.join(BACKUP_DIRECTORY, item)):

t1 = datetime.datetime.strptime(str(now())[:4]+'-'+str(now())[5:7]+'-'+str(now())[8:10],'%Y-%m-%d')

t2 = datetime.datetime.strptime(str(item)[:4]+'-'+str(item)[5:7]+'-'+str(item)[8:10],'%Y-%m-%d')

delta = (t2 - t1)
days_old = int(str(delta.days))
if str(days_old)[:1] == '-' :
if int(str(days_old)[1:5]) > KEEP_MAX_DAYS:
log('- '+item+' is older than '+str(KEEP_MAX_DAYS)+' days. Deleted.')
itemList = os.listdir(BACKUP_DIRECTORY+'/'+item+'/')
for content in itemList:
os.remove(BACKUP_DIRECTORY+'/'+item+'/'+content)
os.rmdir(BACKUP_DIRECTORY+'/'+item)

#-------------------------------------------------------------------------------------------

log('\n\n\n\t###############################################\n\t BACKUP IS RUNNING: '+str(now())+'\n\t###############################################')

log('* LOGGING TO FILE: \t\t\t'+str(USE_LOG))
log('* COMPRESSING FILES bzip2: \t\t'+str(USE_BZIP2))
log('* USING SEPARATION MODE: \t\t'+str(SEPARATION_MODE))
if SEPARATION_MODE == True:
log('* BACKING UP THESE DATABASES:')
for database in DATABASES:
log('\t\t\t\t'+str(database))
else:
log('* BACKING UP THESE DATABASES: \t\tAll')

if KEEP_MAX_DAYS == 0:
log('* KEEPING BACKUPS: \t\t\tForever')
else:
log('* KEEPING BACKUPS FOR (DAYS): \t\t'+str(KEEP_MAX_DAYS))

log('* BACKING UP TO (DIRECTORY) :\t\t'+str(BACKUP_DIRECTORY))
log('* MYSQL USER: \t\t\t\t'+str(DB_USER))

createDateDir()
dumpDB()
cleaner()

log('\n\t BACKUP FINISHED: '+str(now())+'\n\t###############################################')