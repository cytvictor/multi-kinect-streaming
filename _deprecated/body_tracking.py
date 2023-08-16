import sys
import cv2
import numpy as np
import time

import pykinect_azure as pykinect

if __name__ == "__main__":

	# Initialize the library, if the library is not found, add the library path as argument
	pykinect.initialize_libraries(track_body=True)

	# Modify camera configuration
	device_config = pykinect.default_configuration
	device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
	device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED

	# Start device
	device = pykinect.start_device(config=device_config)

	# Start body tracker
	bodyTracker = pykinect.start_body_tracker()

	cv2.namedWindow('Depth image with skeleton',cv2.WINDOW_NORMAL)
	i = 0
	while True:

		ts1 = time.time()
		# Get capture
		capture = device.update()
		# print(ts1)

		# Get body tracker frame
		ts2 = time.time()
		body_frame = bodyTracker.update()
		print(ts2)

		#print(body_frame)

		# Get the color depth image from the capture
		# ret, depth_color_image = capture.get_colored_depth_image()

		# Get the colored body segmentation
		# ret, body_image_color = body_frame.get_segmentation_image()

		#num_bodies = body_frame.get_num_bodies()
		#print(num_bodies)
		try:
			skeleton = body_frame.get_body_skeleton()
			# print(np.asarray(skeleton))

		except:
			continue

		# if not ret:
		# 	continue
			
		# Combine both images
		# combined_image = cv2.addWeighted(depth_color_image, 0.6, body_image_color, 0.4, 0)

		# Draw the skeletons
		# combined_image = body_frame.draw_bodies(combined_image)

		# Overlay body segmentation on depth image
		# cv2.imshow('Depth image with skeleton',combined_image)

		# Press q key to stop
		# if cv2.waitKey(1) == ord('q'):  
		# 	break
