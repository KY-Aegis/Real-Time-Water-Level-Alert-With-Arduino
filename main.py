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
    sender_email = "sender@gmail.com"                  # specify the sender's email
    rec_email = "receiver@gmail.com"                     # specify the receiver's email
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


ports = serial.tools.list_ports.comports()  # get the list of ports
serialInst = serial.Serial()                # initialize the serial port
serialInst.baudrate = 9600                  # specify the max bits per second to 9600bits
serialInst.port = "COM9"                    # specify the port used
serialInst.open()                           # open the serial port
while True:                                 # while the arduino is connected to the com port
    databaseCursor.execute("SELECT * FROM sensor.sensordata order by timestamp desc limit 1")   # query the last value from the sql database
    queryResult = databaseCursor.fetchall()                                                     # assign the value fetched to an array
    if serialInst.in_waiting:                                                                   # if the compiler is waiting for the data
        packet = serialInst.readline()                                                          # read the current value from the serial port
        reading=packet.decode('utf')                                                            # decode the value
        print(reading)                                                                          # print the value
        if int(reading) > upperLimit:                                                           # if the value is above the upper limit
            status = "High"                                                                     # set the status to high
        elif lowerLimit > int(reading):                                                         # if the status is below the lower limit
            status = "Low"                                                                      # set the status to low
    if queryResult[0][2] != status and status != "" and queryResult[0][1] != reading and queryResult[0][0] != datetime.now().strftime("%Y-%m-%d %H:%M:%S"): # if the status from the sql different from the status collected from the serial port, status is not an empty string and the value and timestamp of the sql data and serial port is different
        sql = "INSERT INTO sensordata (TimeStamp, Value, Status) VALUES (%s, %s, %s)"   # construct the insert statement to be inserted into the sql database
        val = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), reading, status)           # get the current timestamp, reading and status from the serial port
        databaseCursor.execute(sql, val)                                                # insert the data into the sql database
        database.commit()                                                               # commit the statement
        print(databaseCursor.rowcount, "record inserted.")                              # print record inserted to indicate a successful insert into statement
        if status == "Low":                                                             # if the status is low
            send_mail(reading)                                                          # send an email to the user to alert them to refil the tank







