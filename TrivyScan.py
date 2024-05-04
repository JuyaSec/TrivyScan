#!/usr/bin/python3

import subprocess
import threading
import time
from termcolor import colored
from datetime import datetime

print ("="*44)
print ("Start Scanning : %s" % time.strftime("%a %d %b %Y %H:%M:%S %p"))
print ("="*44)

def Run_trivy(Image_scan):
		
	try:
		start_time = time.monotonic()
		Trivy_command  =  ["trivy", "image", "-f", "json", "-o", Image_scan+".json", Image_scan]
		Trivy_result   =  subprocess.run(Trivy_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		end_time = time.monotonic()
		runtime = end_time - start_time
		if Trivy_result.returncode == 0 :
			print (colored(f"Successfully Scanned Image '{Image_scan}'", "green"))
			print (f"Runtime Image Scan: {runtime:.2f} seconds")
			print ("-"*41)
		else :
			print (colored(f"Error scanning '{Image_scan}:{Trivy_result.stderr.decode()}'", "red"))
		
	except subprocess.CalledProcessError as e:
		 print (colored(f"An error occurred while scanning {Image_scan}: {e}", "red"))
	

if __name__ == "__main__":
    
	Docker_image = subprocess.check_output(['docker', 'images', '--format', '{{.Repository}}:{{.Tag}}']).decode('utf-8').splitlines() 
	Image_list   =   []   
	threads      =   []

	for Image_add in Docker_image :
          	Image_list.append(Image_add)

	for Image_scan in Image_list:
			
		t = threading.Thread(target=Run_trivy, args=(Image_scan,))
		threads.append(t)
		t.start()
	for Thread_scan in threads:
    		Thread_scan.join()





