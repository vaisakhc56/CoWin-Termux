#  COWIN VACCINE AVAILABILITY NOTIFIER
Get notified on your phone when there is a vaccine slot available at your location, by running a script on your phone. Uses Co-Win public APIs. 


  ## Getting Started
  By using Tremux you can run script and recieve the notification on your phone.
  - ### Setting Up Termux

    - Install Termux App  [Link](https://play.google.com/store/apps/details?id=com.termux&hl=en_IN&gl=US).

    - Install Termux:API App on phone to recieve notifications [Link](https://play.google.com/store/apps/details?id=com.termux.api&hl=en).

 - ### Installing Packages 
   - Install Python

         pkg install python

   - Install Termux-API Package
         
         pkg install termux-api

   - Install Git

         pkg install git
         
   - Clone Repo 
         
         git clone https://github.com/truroshan/cowin-termux

   - Install Requirements.txt using pip
        
         pip install -r requirements.txt


## Running Script

Install [python](https://wiki.termux.com/wiki/Python), if not already installed on Termux. Then run the following command:

    python cowin.py --p <PIN-CODE> --a <YOUR-AGE> --t <INTERVAL-MINUTE>

Replace the arguments above with the required values like mentioned below

  - Replace `--p=<PIN-CODE>` with your pincode.


Optional arguments accepted:

  - Pass `--a=<YOUR-AGE>` with your age (default is 18).

  - Pass `--t=<INTERVAL-IN-MINUTES>` to change the frequency of calling Cowin API  (default is 1 min).
