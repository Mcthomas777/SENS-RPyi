import RPi.GPIO as GPIO
import os, sys
from time import sleep

"""
GPIO numbering mode
=============================
GPIO.BCM --> GPIO numbering
GPIO.BOARD -->  pin numbering
"""
GPIO.setmode(GPIO.BCM)

#configuration of our GPIO 26 as Input
GPIO.setup(26, GPIO.IN)

#File that you wanna run
path_to_programm = '/home/pi/Projet_Stage/Prototype_A/'
programme_py = 'Data_collect_CSVIncluded.py'
while True :
    
    #we use pgrep to have some knowledge about our thread statue

    if os.system('pgrep /home/pi/Projet_Stage/Prototype_A/Data_collect_CSVIncluded.py' ) == 1:
        if GPIO.input(26) == True :
            print('killing process...')
            os.system('pkill $(pgrep -f /home/pi/Projet_Stage/Prototype_A/Data_collect_CSVIncluded.py)')
            break
        
        
        if GPIO.input(26) == False:
            print('already processing')
            pass
        
    else :
        if GPIO.input(26) == False :
            print('Launching process...')
            os.system( 'python3 ' + path_to_programm + programme_py)
            
        if GPIO.input(26) == True:
            print('alreaydy down...')
            pass

    sleep(5)    
        


