from imageai.Detection import VideoObjectDetection
import os
import cv2
import operator
from config import *

class object_detection:
  def __init__(self, video_file_name, crash_first_second, crash_duration_second):
    self.video_file_name = video_file_name
    self.crash_first_second = crash_first_second
    self.crash_duration_second = crash_duration_second
    self.current_path = os.getcwd()
    self.input_files_path = CRASH_DETECTION_ROOT + "/input_files/"
    self.output_files_path = CRASH_DETECTION_ROOT + "/output_files/"

    # basic video information
    self.cap = cv2.VideoCapture(self.input_files_path + self.video_file_name)
    self.fps = self.cap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
    self.duration = self.frame_count/self.fps

    # collision information
    self.collision_start_frame = self.crash_first_second / self.duration * self.frame_count
    self.collision_end_frame = (self.crash_first_second + self.crash_duration_second) / self.duration * self.frame_count
    self.objects_all = dict()

    # collision defination
    self.collision_pre_frame = self.fps


  def object_collision(self):
    #print("Detecting video file ('%s') from second %.3f to %.3f" %
    #  (self.video_file_name, self.crash_first_second, self.crash_first_second + self.crash_duration_second))

    def forFrame(frame_number, output_array, output_count):
      if(frame_number > self.collision_pre_frame and frame_number < self.collision_start_frame):
        #print("FOR FRAME " , frame_number)
        #print("Output for each object : ", output_array)
        #print("Output count for unique objects : ", output_count)
        for key in output_count.keys():
          if(key in self.objects_all.keys()):
            self.objects_all.update({key:self.objects_all[key]+output_count[key]})
          else:
            self.objects_all.update({key:output_count[key]})
        #print("All objects : ", self.objects_all)
        #print("------------END OF A FRAME --------------")
      return

    def forSeconds(second_number, output_arrays, count_arrays, average_output_count):
      #print("SECOND : ", second_number)
      #print("Array for the outputs of each frame ", output_arrays)
      #print("Array for output count for unique objects in each frame : ", count_arrays)
      #print("Output average count for unique objects in the last second: ", average_output_count)
      #print("------------END OF A SECOND --------------")
      return

    def forMinute(minute_number, output_arrays, count_arrays, average_output_count):
      #print("MINUTE : ", minute_number)
      #print("Array for the outputs of each frame ", output_arrays)
      #print("Array for output count for unique objects in each frame : ", count_arrays)
      #print("Output average count for unique objects in the last minute: ", average_output_count)
      #print("------------END OF A MINUTE --------------")
      return

    video_detector = VideoObjectDetection()
    video_detector.setModelTypeAsYOLOv3()
    video_detector.setModelPath(CRASH_DETECTION_ROOT + "/yolo.h5")
    video_detector.loadModel()
    custom_objects = video_detector.CustomObjects(person=True, bicycle=True, motorcycle=True, car=True, bus=True, truck=True)

    # print(self.output_files_path)

    video_detector.detectCustomObjectsFromVideo(custom_objects=custom_objects,
                                      input_file_path=os.path.join(self.current_path, self.input_files_path + self.video_file_name), 
                                      output_file_path=os.path.join(self.current_path, self.output_files_path + self.video_file_name.split('.')[0]) ,  
                                      frames_per_second=self.fps, per_second_function=forSeconds, 
                                      per_frame_function=forFrame, 
                                      per_minute_function=forMinute, 
                                      minimum_percentage_probability=30)

    
    # return object with maximal count
    if(bool(self.objects_all)==True):
      return max(self.objects_all.items(), key=operator.itemgetter(1))[0]
    else:
      return "None"
