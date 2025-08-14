This program sends an email to the user with a daily workout planner.
It can be automated using PythonAnywhere by uploading the main.py file and creating a daily task with the following command:

export MY_EMAIL={YOUR_EMAIL}; export TARGET_EMAIL={DESTINATION_EMAIL}; export PASSWORD={APP_PASSWORD}; python3 main.py

- The APP_PASSWORD can be created in the settings of your email provider.
- If you are not using a gmail account, change the "smtp.gmail.com" argument from SMTP method to your email host.

Used:
PythonAnywhere