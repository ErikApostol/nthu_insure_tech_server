import os
import requests
import json
import crash_detect
import object_detection
import sys

input_files_path = "input_files/"
video_file_name = sys.argv[1]
severity_api = 'https://motor-crash.herokuapp.com/api'
object_type = {
	'bicycle': '腳踏車',
	'motorcycle': '機車',
	'car': '小型車',
	'bus': '巴士',
	'truck': '卡車'
}

def main():
	cd = crash_detect.crash_detect_module(video_file_name)
	cd.detect_process()
	print ('影片分析特徵:')
	print ('1.白天或黑夜: ', cd.get_night_or_moring() )
	if(cd.get_night_or_moring() == 'moring'):
		time = '白天'
	else:
		time = '夜晚'
	print ('2.是否發生碰撞: ', cd.get_crash_flag() )
	print ('3.碰撞發生時間點: ', cd.get_crash_first_time() )
	print ('4.碰撞持續時間點: ', cd.get_crash_max_time() )

	# collision object detection
	if(cd.get_crash_flag() == True):
		od = object_detection.object_detection(video_file_name, cd.get_crash_first_time(), cd.get_crash_max_time())
		collision_object = od.object_collision()
		print("5.碰撞物體: ",collision_object)
		object = collision_object
	else:
		print("5.碰撞物體: None")
		object = '自摔'
	for key in object_type:
		if(key == object):
			object = object_type.get(key)

	data = [[time, '晴天', object]]

	json_payload = json.dumps(data)
	severity_response = requests.post(severity_api, json={'input': json_payload})
	print("碰撞嚴重程度: ", severity_response.json()['Severity_Score'])

	return 0

if __name__ == "__main__":
    main()