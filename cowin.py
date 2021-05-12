from cowin_api import CoWinAPI
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import fire
import sys
import os
import re

cowin = CoWinAPI()
scheduler = BlockingScheduler()

def notify():
    available_centers = cowin.get_availability_by_pincode(PINCODE,min_age_limt=AGE)

    AVAILABLE = False
    for center in available_centers.get('centers',[]):
        for session in center.get('sessions'):
            capacity = session.get('available_capacity')
            center_name = center.get('name')
            session_date = session.get('date')
            if capacity != 0 and center.get('center_id') in  CENTER_ID:
                
                MSG = f'{capacity} slots left [{session_date}] @ {center_name} ({PINCODE})'

                # Send Notification via Termux:API App
                os.system(f"termux-notification --content '{MSG}'")
                AVAILABLE =  True
    
    # When last Checked
    print("Last Checked  ⌛️ : " + datetime.now().strftime("%H:%M:%S"))
    sys.stdout.write("\033[F")
    
    # Stop Scheduler
    if AVAILABLE:
        print("Shutting Down CoWin Script 👩‍💻 ")
        scheduler.shutdown(wait=False)
        

def main(pincode, age = 45,time = 1):

    if age < 18 :
        print("Age is less than 18.") 
        return
    else:
        age = 18 if 18 <= age < 45 else 45

    available_centers = cowin.get_availability_by_pincode(str(pincode),min_age_limt=age)

    CENTERS = {}

    print("Select Vaccination Center 🏥 :")
    for index,center in enumerate(available_centers.get('centers',[]),start=1):
        print(f'{index} : {center.get("name")}')
        CENTERS[index] = center.get('center_id')
    

    global CENTER_ID, AGE, PINCODE

    print("-"*20)
    print("Enter Multiple Value with Space. \n(Example : 1 2 3 4)")
    print("-"*20)

    INDEX_S = input("Enter Index's : ")

    INDEX_S = re.findall("(\d)",INDEX_S)
    

    CENTER_ID = []
    for  index in INDEX_S:
        if CENTERS.get(int(index)):
            CENTER_ID.append(CENTERS.get(int(index)))

    if not INDEX_S or not CENTER_ID:
        print("No Index Selected\n Program exited.")
        exit()

    AGE, PINCODE = age,str(pincode)

    os.system("clear")

    scheduler.add_job(notify, 'cron',hour = "10-22", minute = f'0-59/{time}')




if __name__ == '__main__':
    
    fire.Fire(main)

    print("CoWin Slot Checker 💉 ..")

    scheduler.start()
