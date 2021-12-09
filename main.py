import mysql.connector          # import library to read and insert into sql
from datetime import datetime   # import datetime library to get the timestamp
import serial.tools.list_ports  # import serial library to read serial value
import smtplib                  # import smtp library to send email
import getpass                  # import getpass to mask password input

lowerLimit = 600                # declare the lowerLimit of the reading to execute the sql insert statement
upperLimit = 650                # declare the upperLimit of the reading to execute the sql insert statement
status = ""                     #set the default status as an empty string
reading = 0                     # set the default reading as 0

database = mysql.connector.connect( # initialize the sql connector
  host="localhost",                 # the host name
  user="root",                      # the username
  password="1234",                  # the password
  database="sensor"                 # the db schema name
)
databaseCursor = database.cursor()  # assign databaseCursor as the sql cursor

def send_mail(low):                                         # function to send email when the water level is low
    sender_email = "kheeyaw2912@gmail.com"                  # specify the sender's email
    rec_email = "Lingkheeyaw@gmail.com"                     # specify the receiver's email
    password = getpass.getpass("Enter your password : ")    # prompt user to enter the password
    subject = "Abnormal Water Level Detected"               # subject of the email
    text = "The current water level threshold is LOW at {}. Please refill immediately".format(str(low)) # body of the email
    message = 'Subject: {}\n\n{}'.format(subject, text)     # combination of the subject and body
    server = smtplib.SMTP('smtp.gmail.com', 587)            # declare the smplib server host number
    server.starttls()                                       # establish the connection with the server
    server.login(sender_email, password)                    # login to the sender's email
    server.sendmail(sender_email, rec_email, message)       # send the email to the receiver using the sender's account
    server.quit()                                           # terminate the connection to the server
    print("Email has been sent to "+rec_email)              # print a text to validate that email has been sent successfully


ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = "COM9"
serialInst.open()
while True:
    databaseCursor.execute("SELECT * FROM sensor.sensordata order by timestamp desc limit 1")
    queryResult = databaseCursor.fetchall()
    if serialInst.in_waiting:
        packet = serialInst.readline()
        reading=packet.decode('utf')
        print(reading)
        if int(reading) > upperLimit:
            status = "High"
        elif lowerLimit > int(reading):
            status = "Low"
    if queryResult[0][2] != status and status != "" and queryResult[0][1] != reading and queryResult[0][0] != datetime.now().strftime("%Y-%m-%d %H:%M:%S") :
        sql = "INSERT INTO sensordata (TimeStamp, Value, Status) VALUES (%s, %s, %s)"
        val = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), reading, status)
        databaseCursor.execute(sql, val)
        database.commit()
        print(databaseCursor.rowcount, "record inserted.")
        if status == "Low":
            send_mail(reading)







