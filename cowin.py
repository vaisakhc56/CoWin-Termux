from cowin_api import CoWinAPI
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import fire
import sys
import os
import re

cowin = CoWinAPI()
scheduler = BlockingScheduler()

def line_break():
    print("-"*25)

def clear_screen():
    os.system("clear")

def notify():
    available_centers = cowin.get_availability_by_pincode(PINCODE,min_age_limt=AGE)

    for center in available_centers.get('centers',[]):

        for session in center.get('sessions')[1:]:  # Starting from Next Day

            center_name = center.get('name')
            center_id = center.get('center_id')

            capacity = session.get('available_capacity')
            session_date = session.get('date')
            vaccine_name = session.get('vaccine')

            if capacity != 0 and center_id in  CENTER_ID:

                MSG = f'💉 {capacity} #{vaccine_name} / {session_date} / {center_name} 📍{PINCODE}'

                # Send Notification via Termux:API App
                os.system(f"termux-notification --content '{MSG}'")

                CENTER_ID.remove(center_id)

    # When last Checked
    print("Last Checked  ✅ : " + datetime.now().strftime("%H:%M:%S") + " 🕐")
    sys.stdout.write("\033[F")

    # when CENTER_ID list is empty Stop Scheduler
    if not CENTER_ID:
        print("Shutting Down CoWin Script 👩‍💻 ")
        scheduler.shutdown(wait=False)


def main(pincode, age = 18,time = 1):

    if age < 18 :
        print("Age is less than 18.")
        return
    else:
        age = 18 if 18 <= age < 45 else 45

    available_centers = cowin.get_availability_by_pincode(str(pincode),min_age_limt=age)

    CENTERS = {}
    INDEX_S = []

    print(f"Select Vaccination Center ({pincode}) 💉 \n")
    for index,center in enumerate(available_centers.get('centers',[]),start=1):
        print(f'{index} : {center.get("name")}')
        CENTERS[index] = center.get('center_id')

        INDEX_S.append(index)

    print()

    global CENTER_ID, AGE, PINCODE

    line_break()
    print("""
* Select One Center
    input : 1
* Select Mutiple with Space
    input : 1 2 3 4
* Select All Center
    Hit Enter without Input\n""")

    line_break()

    input_index = input("Enter Index's : ")

    if input_index != '':
        INDEX_S = re.findall("(\d)",input_index)

    clear_screen()

    CENTER_ID = []
    for  index in INDEX_S:
        if CENTERS.get(int(index)):
            CENTER_ID.append(CENTERS.get(int(index)))

    AGE, PINCODE = age,str(pincode)

    clear_screen()

    scheduler.add_job(notify, 'cron',hour = "8-22", minute = f'0-59/{time}')
    print(f" 📍 {PINCODE} 💉 {AGE}+ ⌛️ {time} Minute")



if __name__ == '__main__':
    clear_screen()

    fire.Fire(main)

    print("CoWin Slot Checking 🔃\nfor Tomorrow and Day After 📆 ...")
    line_break()

    scheduler.start()
