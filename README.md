# Real-Time-Water-Level-Alert-With-Arduino
A combination of Arduino, Python and SQL to trigger an email when the water level hits a certain limit by utilizing the serial port.

# Create the Schematics
<img src="Images/1.PNG" height="300" width="400">
Required Components:</br>
-Arduino Mega 2560 X 1</br>
-LCD 16X2 I2C X 1</br>
-Water Level Sensor X 1</br>
-LED X 3

# Construct the SQL Table Structure
<img src="Images/2.PNG" height="200" width="300">
Create a new schema called sensor with a table called sensordata with the following columns:</br>
-Timestamp (datetime)</br>
-Value (int)</br>
-Status (varchar) </br>

# Explanation of the Arduino Code
The code will continuously read the value of the water sensor and change the output of the LCD based on the input where 0 to 20 will be empty, 20 to lowerlimit 
will be low, lowerlimit to upperlimit will be normal, and more than upperlimit will be full. The LED will light up according to the values as well where RED will
be displayed when the water level is empty or low, yellow for normal and green for high. 

# Sample Output when the Water Level is Low
<img src="Images/4.jpeg" height="200" width="300">

# Sample Output when the Water Level is Normal
<img src="Images/5.jpeg" height="200" width="300">

# Explanation of the Python Code
The code will continuously read the value of the water sensor from the serial port and will insert a new row into the sql database if there is a change in the status
of the water level. If the water level changes from normal or high to low, an email will be triggered to a recipient to notify them that the current water level 
threshold is low. An input for the password to the sender's email will be prompted before the alert is being triggered. 

# Sample of Trigger for Alert
<img src="Images/3.PNG" height="100" width="300">

# Sample Email Output
<img src="Images/6.PNG" height="200" width="500">
