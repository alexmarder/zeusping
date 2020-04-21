
import sys
import os
import shlex
import subprocess
import glob
import time
import datetime
import wandio

data_dir = sys.argv[1]

# Load Swift credentials
# NOTE: This did not work (apparently 'source' is a shell-specific command), so I just source ~/.limbo-cred in for_cron_swiftsyncer.sh
# source_cmd = 'source /home/ubuntu/limbo-cred'
# sys.stderr.write("{0}\n".format(source_cmd) )
# os.system(source_cmd)
# args = shlex.split(source_cmd)    
# print args
# try:
#     subprocess.check_call(args)
# except subprocess.CalledProcessError:
#     sys.stderr.write("Source limbo-cred command failed; exiting\n")
#     sys.exit(1)


while True:

    curr_time = time.time()
    until_time = curr_time - 60*15 # Get all gz files that were produced before 15 minutes    

    unsorted_files = glob.glob('{0}/*warts*'.format(data_dir) )
    sorted_files = sorted(unsorted_files, key = lambda f: os.path.getctime(f) )
    
    for fil in sorted_files:
        # print fil
        parts = fil.strip().split('.')
        # print parts
        file_name = fil.strip().split('/')[-1]
        file_pref = parts[0].strip().split('/')[-1]
        # print file_pref
        this_t = int(parts[1])

        if this_t > until_time:
            break


        # If the file isn't already compressed, compress it
        if file_name[-2:] == 'gz':
            was_compressed = 1
        else:
            was_compressed = 0        
            # Compress this file
            gzip_cmd = 'gzip {0}'.format(fil)
            sys.stderr.write("{0}\n".format(gzip_cmd) )
            args = shlex.split(gzip_cmd)    

            try:
                subprocess.check_call(args)
            except subprocess.CalledProcessError:
                sys.stderr.write("Gzip failed for f {0}; exiting\n".format(fil) )
                sys.exit(1)

                
        round_number = this_t/600
        round_tstart = round_number * 600
        round_tend = round_tstart + 600

        round_tstart_dt = datetime.datetime.utcfromtimestamp(round_tstart)

        if was_compressed == 1:
            # The file had already been compressed. No need to add the 'gz' extension
            object_name = 'datasource=zeusping/campaign=CO_VT_RI/year={0}/month={1}/day={2}/hour={3}/{4}'.format(round_tstart_dt.year, round_tstart_dt.strftime("%m"), round_tstart_dt.strftime("%d"), round_tstart_dt.strftime("%H"), file_name)
        else:
            # We just compressed the file. Add the 'gz' extension
            object_name = 'datasource=zeusping/campaign=CO_VT_RI/year={0}/month={1}/day={2}/hour={3}/{4}.gz'.format(round_tstart_dt.year, round_tstart_dt.strftime("%m"), round_tstart_dt.strftime("%d"), round_tstart_dt.strftime("%H"), file_name)
        # print object_name

        if was_compressed == 1:
            file_to_write = fil
        else:
            file_to_write = "{0}.gz".format(fil)
        
        # This would swift upload without wandio:
        # swift_cmd = 'swift upload zeusping-warts {0} --object-name={1}'.format(file_to_write, object_name)
        # sys.stderr.write("{0}\n".format(swift_cmd) )
        # args = shlex.split(swift_cmd)    

        # try:
        #     subprocess.check_call(args)
        # except subprocess.CalledProcessError:
        #     sys.stderr.write("Swift upload failed for f {0}; exiting\n".format(fil) )
        #     sys.exit(1)

        # This swift uploads with wandio:
        
        try:
            # sys.stderr.write("fil: {0}\n".format(fil) )                        
            # sys.stderr.write("File to write: {0}\n".format(file_to_write) )
            # sys.stderr.write("Object_name: {0}\n".format(object_name) )
            wandio.swift.upload(file_to_write, 'zeusping-warts', object_name)
            sys.stderr.write("Swift upload successful for file {0}\n".format(fil) )
        except:
            sys.stderr.write("Swift upload failed for file {0}; exiting\n".format(fil) )            
            sys.exit(1)

        # rm the original file
        os.remove(file_to_write)
        # sys.exit(1)

    time.sleep(30)

