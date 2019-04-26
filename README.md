# Pi in the Sky
This will contain all of my planning and documentation for the Pi in the Sky project.

## Planning
This is the planning section of my documentation.

### General Idea
I plan on creating a simple wooden launching device for the pi that will fucntion somewhat like a crossbow, with a bungie cord or exercise band as a string and a rail for the pi to keep it straight for the start of the flight.
[Here](https://github.com/aralsto/Pi_in_the_Sky/blob/master/Planning_Images/mockup.png) is a mock-up of this design. As far as the pi side of things, I will simply utilize the code I made for the previous accelerometer assignments and modify it to predict the peak of the flight and turn on an LED when
it reaches this point. This isn't too difficult to code as you can simply use a Reimann sum to find vertical velocity, and then divide by G to get the number of seconds until that velocity should become 0. As I will
elaborate on in the challenges section, however, it is imperative that the accelerometer remain parallel to the ground during the acceleration, otherwise the data gathered will be practically useless. As a final note, I 
want to keep the payload as minimal as possible, so it will likely just be a small piece of foam board with slots for the pi, accelerometer, LED, and perhaps a small circuit board if that seems necessary.

### Challenges
There are a number of potential challenges and issues with this project. First and foremost, the accelerometer MUST be parallel to the groud (or in some other fixed orientation) for the entirety of the acceleration.
If it isn't, the Reimann sum used to calculate velocity will be entirely innacurate, and the main idea behind the project (finding the peak of the flight) will be impossible. This is why I wanted the pi to be on a rail
for the launch, because this would keep it well enough oriented to allow for the proper accelerometer data to be gathered.
Another potential challenge will be finding a proper cord to use for propulsion. I don't want to make the launcher particularly large, and I want the cord to be taught even at its resting position,
meaning I'll need quite a short cord that still has enough power to launch the pi some feet in the air. If I end up using something else like an exercise band this issue would be eliminated, but it would also make the design
slightly more complicated as I might no be able to just use metal hooks to attach the propulsion mechanism.

### Schedule
Feb 6 - Planning

Feb 7 to 13 - Code

Feb 13 to 15 (less if I don't do a circuit board) - Wiring

Feb 15 to 19 (due to President's day) - Payload design and creation

Feb 20 to 22 - Launcher design

Feb 25 to 28 - Launcher creation

Mar 1 to 4 (due to weekend) - Fixing issues, likely testing and refining code, finishing project!

## Finished Project
This is the documentation of the actual finished project with explanations about the wiring, code, solidworks, and changes to the design from the planning phase.

### Changes
The project changed quite a bit from the planning phase. I settled on simply making a compact package that one can flip a switch to automatically start up, and once it is "armed" throw it in the air to have it
blink an LED at the peak of the flight. [Here](https://github.com/aralsto/Pi_in_the_Sky/blob/master/Images/Overview.jpg) is an images of it from the top, and [here](https://github.com/aralsto/Pi_in_the_Sky/blob/master/Images/Underview.jpg) is an image of it from the bottom. The green LED indicates when it is ready to be thrown, blinking off once when the accelerometer has been calibrated. The blue LED turns on at the peak of the flight
for a second, then both turn off and the program ends. The switch simply closes the circuit of the battery to The accelerometer is attached somewhat interestingly as seen in the view of the underside, and this choice will be
expanded on in the Solidworks section. The basic gist is that when I used the mounts I made for the accelerometer, it spun too much and gave innacurate readings because of it. The final change in the project was that I was
initially going to have it record the data from each flight, but I decided against that as in testing I had already seen the data and it really isn't interesting. If I ever wish to have the data, it's an easy addition,
but I don't see value in using processing power to record it every time.
