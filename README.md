# STASiS

![STASiS design example](https://i.imgur.com/vxhF7ob.jpg)

## Use It Live
https://stasis-project.org

## Inspiration
Noticing dangerous situations and reacting to them can often lead to a difference between life and death. Often times, noticing these critical situations is hard for people since it might require looking at lots tiny details and putting them together. Our solution to this: computers!

With the increase in computational power in the last 5 years, computers have gotten exponentially faster, analyzing and moving heaps of data. With tools like Clarifai, TensorFlow and Caffe now open to the masses, it has become easier to combine these systems to build tools that are capable of collecting large amounts of data and processing them into usable data.

Our inspiration for this situational analysis system came from real-life projects such as DeepMind, as well as fictional icons such as Person of Interest. While in some fictitious shows the system is used as a tool for monitoring people, we want our tool to be used for potentially dangerous situations which could save lives without being intrusive and respecting privacy.

## How We Built It
We started building around the Clarifai API and playing with it. Another teammate developed a simple back-end web server capable of taking input from the webcam. We then linked these two up so that we could send pictures to the server and get back tags from Clarifai's API. We then built a statistical analysis tool for the data in a way that the more recent frames are given higher weightage when the system is trying to calculate the probability of a specific situation. We then brought it all together in a front-end that was written in Materialize. 

## Technical details
#### Front-end
With our front, we trying to achieve one simple goal: Make the UI as clean as possible while still displaying all the information to the user. Materialize, which implements Material Design by Google, seemed to be a natural fit for this. We use a grid layout that is responsive to the device's screen size, and we get all the data from the server asynchronously. This means that the user does not experience a slow browsing experience, but still has all the necessary information plus nice visualizations.

#### Statistical Analysis
The statistical analysis that we use is one of the core algorithms for the project. The idea behind it is fairly simple: If two frames are close together (i.e. the timestamps have some range), the tool should weigh in analysis tags from the old frames when getting the probablilities for the new frames. This is done to normalize outlying probablilty for tags, which means that if the API get a tag wrong in a single frame, it is unlikely to affect the entire probability outcome.


## Running the server
To build the required back-end, use the following commands:
```
mkvirtualenv --python=$(which python3) hackum
pip install -r requirements.txt
daphne -b 127.0.0.1 -p 9000 hackum.asgi:channel_layer
./manage.py runworker
```
