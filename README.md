# Raspberry Pi project to monitor fridge door

The purpose of this project was to detect if a fridge door was in an open or closed position and report on openings. A Magnetic reed switch is attached to the Raspberry Pi and to the Fridge door to detect position. When door is open python code is implemented to take a picture and send to the firebase database which feeds a simple 
glitch web display. Notifications also sent to owners smartphone by mail via mailgun api and sms via Twilio API.

https://fridgedoor.glitch.me/
