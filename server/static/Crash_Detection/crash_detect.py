# -*- coding: utf-8 -*-
import numpy as np
import cv2
import csv
class crash_detect_module:


    #parameter
    DARK_CAP_THRESHOLD = 5
    DAY_OR_NIGHT_THRESHOLD = 0.5
    DARK_PIXEL_THRESHOLD = 60
    PIX_DIFF_CRASH_THRESHOLD = 100
    DIFF_DIFF_CRASH_THRESHOLD = 40
    DISCARD_FRAME_NUM = 10


    #function
    #fpath is file address
    def __init__(self, fpath):
        #arguemnt
        self.fpath = fpath
        #print (self.fpath)
        #hidden variable
        self._fps = 0
        self._dark_arr = []
        self._pix_diff_arr = []

        #output
        self.org_dark_avg = 0
        self.capped_dark_avg = 0
        self.org_day_or_night = ''
        self.capped_day_or_night = ''

        self.pix_diff_crash_flag = False
        self.pix_first_time_th = 0
        self.argmax_in_pix_diff_arr = 0
        

    #procss all data
    def detect_process(self ):
        if not self.fpath:
            return
        self._process_video()
        self._process_data()
    #judge crash yes or no
    #return True False
    def get_crash_flag(self):
        return self.pix_diff_crash_flag
    #get time of  first time
    def get_crash_first_time(self):
        return  self.pix_first_time_th
    #get time of max crash change    
    def get_crash_max_time(self):
        return self.max_diff_time
    #judge moring and night
    def get_night_or_moring(self):
        return self.org_day_or_night
    def _process_video_frame(self, frame, fgbg):
        frame_size = frame.shape[0] * frame.shape[1]
        fgmask = fgbg.apply(frame)
        dark_pix_cnt = self.count_dark_pixel(frame, self.DARK_PIXEL_THRESHOLD) / frame_size
        avg_pix_diff = np.sum(fgmask) / frame_size
        return (dark_pix_cnt, avg_pix_diff)
        
    def _process_video(self):
        cap = cv2.VideoCapture(self.fpath)
        fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
        self._fps = cap.get(cv2.CAP_PROP_FPS)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                (dpc, avp) = self._process_video_frame(frame, fgbg)
                self._dark_arr.append(dpc)
                self._pix_diff_arr.append(avp)
            else:
                break
        cap.release()
        cv2.destroyAllWindows()


    

    def _process_data(self):
        fps = self._fps
        dark_arr = self._dark_arr
        pix_diff_arr = self._pix_diff_arr
        
        dark_arr = np.array(dark_arr)
        pix_diff_arr = np.array(pix_diff_arr)
        # discard few frame
        dark_arr[:self.DISCARD_FRAME_NUM] = 0
        pix_diff_arr[:self.DISCARD_FRAME_NUM] = 0
        diff_offset_arr_left = np.concatenate(([0.0], pix_diff_arr))[:-1]    
        diff_of_diff = np.abs(diff_offset_arr_left - pix_diff_arr)
        
        

        #process
        #night or moring process
        self.org_dark_avg = np.mean(dark_arr) #計算所有像素點的灰階值
        arg_where = np.argwhere(diff_of_diff < self.DARK_CAP_THRESHOLD).flatten() 
        self.capped_dark_avg = np.mean(dark_arr[arg_where]) #移除部分尖峰值
        capped_percent = (1 - (len(dark_arr[arg_where])/len(dark_arr))) * 100 # 再重新計算值的比例

        self.org_day_or_night = 'night' if self.org_dark_avg > self.DAY_OR_NIGHT_THRESHOLD else 'moring' #輸出
        self.capped_day_or_night = 'night' if self.capped_dark_avg > self.DAY_OR_NIGHT_THRESHOLD else 'moring' #輸出
        
        
        
        #crash  detect
        #使用畫面變動率來偵測碰撞
        max_in_pix_diff_arr = np.amax(pix_diff_arr) #取出最大值
        self.max_diff_time = np.argmax(pix_diff_arr) / fps #轉成秒了 #輸出
        #大於某個值判定為車禍(值為人設)
        if max_in_pix_diff_arr < self.PIX_DIFF_CRASH_THRESHOLD:
            self.pix_diff_crash_flag = False
            self.pix_first_time_th = -1
        else:
            arg_where = np.argwhere(pix_diff_arr >= self.PIX_DIFF_CRASH_THRESHOLD).flatten() 
            #filter variable > self.PIX_DIFF_CRASH_THRESHOLD, self.PIX_DIFF_CRASH_THRESHOLD(owd define)
            self.pix_first_time_th = arg_where[0] / fps #second of crashing in vidoe
            self.pix_diff_crash_flag = True #output, crash flag
        #crash  detect 2
        #使用變化率的畫面變化率來偵測碰種 (類似微分)
        max_in_diff_diff_arr = np.amax(diff_of_diff) #
        argmax_in_diff_diff_arr = np.argmax(diff_of_diff) / fps #轉成秒了 #輸出
        if max_in_diff_diff_arr < self.DIFF_DIFF_CRASH_THRESHOLD:
            diff_diff_crash_flag = False
            ddiff_first_time_th = -1
        else:
            arg_where = np.argwhere(diff_of_diff >= self.DIFF_DIFF_CRASH_THRESHOLD).flatten()
            ddiff_first_time_th = arg_where[0] / fps #轉成秒了 #輸出
            diff_diff_crash_flag = True #輸出

       
    def count_dark_pixel(self, frame, threshold):
        # RGB/3 and flatten and cast to uint8
        frame2 = np.mean(frame, axis=2).reshape((frame.shape[0] * frame.shape[1])).astype('uint8')
        extracted = frame2[frame2 < threshold]
        return extracted.shape[0]
