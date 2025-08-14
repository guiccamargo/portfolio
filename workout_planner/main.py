import datetime
import os
import smtplib

from dotenv import load_dotenv

load_dotenv()

# Weekly plan
PLAN = {
    "Monday": {"workout": "Abdominal", "duration": 22},
    "Tuesday": {"workout": "Braço", "duration": 17},
    "Wednesday": {"workout": "Costa", "duration": 13},
    "Thursday": {"workout": "Abdominal", "duration": 22},
    "Friday": {"workout": "Peito", "duration": 10},
    "Saturday": {"workout": "Braço", "duration": 17},
    "Sunday": {"workout": "Costa", "duration": 13},
}

# Set email values
MY_EMAIL = os.getenv("MY_EMAIL")
TARGET_EMAIL = os.getenv("TARGET_EMAIL")
PASSWORD = os.getenv("PASSWORD")


def send_email():
    """
    This function sends an email with the workout plan for today.
    """
    current_day = datetime.datetime.today().strftime("%A")

    today_workout = PLAN[current_day]

    mesage = f"Workout for today: {today_workout["workout"]} for {today_workout["duration"]} minutes."

    try:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=TARGET_EMAIL,
                msg=f"Subject:{current_day} Workout\n\n{mesage}"
            )
    except Exception as e:
        print(str(e))


send_email()
