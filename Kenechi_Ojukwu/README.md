# Player Recognition

This is the solution repository to the ParallelScore CV task.

# Breakdown of approach taken:
1) Identify Person(s) in video.
2) Track unique person(s).
3) Extract unique person(s) from video.
4) Seperate person(s) into two teams based on color of cloth.

### Identify Person(s) in Video:
The approach taken here was to use an object detecton model to detect all the objects that belong to the class "person" in the video. The detectron2 object detection framework was used. The pretrained version of the object detection model predicts for 80 classes per image. I retrained the pretrained model on just a dataset of people, hence reducing the classes from 80 to 1. The reason behind this is to improve the inferencing time, so if it takes 15 seconds to detect for 80 classes per image on a cpu only system, it reduces the time to around 3 seconds.

### Track unique Person(s):
The Simple Online Real Time (SORT) tracker algorithm was used to track all the unique persons(players) in the video, although the accuracy of the tracker wasn't high enough, it did a moderately fair job in tracking players.

### Extract Persons from Video:
After the unique players have been detected for each image frame in the video, the coordinates of the unique person(s) are used to crop the image of the player. The image of the player is then saved in a directory.

### Seperate persons into two teams:
The next stage is the seperation stage, here we seperate the the cropped images of the players into two teams using the color of their cloth. Two methods were used,
 Clustering and Color check. The clustering method was used to cluster the images based on the color present in the image ... This method worked well in clustering the yellow team but did poor on the blue. I then decided to use a color checking approach, which basically means that I check if the color blue is present in an image. This approach worked slightly well for the blue team.
 
### Optimizing for CPU inferencing:
The video in question contains 700+ frames, which would take a considerable amount of time to run on a cpu system, I decided to skip some frames inorder to increase overall speed. Two approaches were used. n_frames and n_seconds. 

1) n_seconds: The video is a 30 second video, 1 second contains 25 frames, this algorithm takes 1 frame from the 25 frames for every second, this reduces the overall frame from 700 to 30 frames ... The tradeoff for this approach is overall speed vs accuracy. Accuracy in this case means accurately identifying unique players in the video, this is because of the discontinuity that may occur in selecting just one frame per second.

2) n_frames: This approach selects key frames, then selects more frames in between these key frames. An example is, say for the video provided. There are 700 hundred plus frames. this algorithm takes keys frames, which will be the frames at position 0,100,200,300,400,500,600,700. Then proceeds to extract more frames between 0 to 100, 101 to 200 and so on. You can specify the number of frames to collect between key frames. This method is somewhat of an improvement of the n_seconds algorithm, tackling discontinuity but still trying to account for speed.


### Folder Structure of solution:
1) detector - Contains scripts for detecting the players in the video.
2) seperator -  Contains scripts for seperating the players into teams.
3) player - Folder where the cropped image of players are saved. This folder is cleared once the players have been seperated into teams
4) results - Folder where teams are saved.
3) Dockerfile -  Dockerfile
4) Main.py -  Main python script for running code



### How to Run code:
## simple run:
python main.py

## if you want to provide a path:
python main.py --output_path _path_to_directory_

## if you want to try out video skipping algorithms:
python main.py --output_path _path_to_directory_ --skip True --skip_type "n_frames"

The approach works well for a baseline, but is open to improvements.

### Possible Improvments for this approach :
1) Use deepsort for better tracking of unique players
2) Improve image quality with filters after cropping it.
3) Try out other feature extracting methods for the cropped images(images of players) to improve clustering performance.



### Set Back:
Due to a possible update of pytorch. There were so many dependency issues between pytorch and detectron2 when building a docker image. Attempting to successuly resolve this took time and alot of internet resource. Hence no successful docker image was built for this task. If interested, access to the working code on google colab can be made available. 
