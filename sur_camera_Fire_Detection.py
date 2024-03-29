import cv2
import numpy as np
import smtplib
import playsound
import threading

# Initialize variables
Alarm_Status = False
Email_Status = False
Fire_Reported = 0



# Function to play alarm sound
def play_alarm_sound_function():
    while True:
        playsound.playsound("alarm.mp3", True)


# Function to send email
def send_mail_function():
    recipientEmail = "example1@gmail.com" #Give an reciptant email
    recipientEmail = recipientEmail.lower()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587) # 578 is the port number which is used to send mails
        server.ehlo()
        server.starttls()
        server.login("example2h@gmail.com", 'bhnjkjh') # add reciver email and the password
        server.sendmail('example2@gmail.com', recipientEmail,
                        "Warning A Fire Accident has been reported on ABC Company") #Add the message you want to send through main
        print("sent to {}".format(recipientEmail))
        server.close()
        print("mail send")
    except Exception as e:
        print(e)


# Video capture
video = cv2.VideoCapture("fire.mp4")

# Main loop
while True:
    (grabbed, frame) = video.read()
    if not grabbed:
        break

    frame = cv2.resize(frame, (960, 540))

    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(hsv, lower, upper)

    output = cv2.bitwise_and(frame, hsv, mask=mask)

    no_red = cv2.countNonZero(mask)

    if int(no_red) > 15000:
        Fire_Reported = Fire_Reported + 1

    cv2.imshow("output", output)

    if Fire_Reported >= 1:
        if Alarm_Status == False:
            threading.Thread(target=play_alarm_sound_function).start()
            Alarm_Status = True

        if Email_Status == False:
            threading.Thread(target=send_mail_function).start()
            Email_Status = True

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
video.release()
