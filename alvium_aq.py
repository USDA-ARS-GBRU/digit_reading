import vmbpy


# Example 1 check cameras
# vmb = vmbpy.VmbSystem.get_instance()
# with vmb:
#	cams = vmb.get_all_cameras()
#	for cam in cams:
#	print(cam)
# Camera(id=DEV_1AB22C06995C)

#
import cv2
from vmbpy import *

with VmbSystem.get_instance() as vmb:
    cams = vmb.get_all_cameras()
    with cams[0] as cam:
        frame = cam.get_frame()
        frame.convert_pixel_format(PixelFormat.Mono8)
        cv2.imwrite('frame.jpg', frame.as_opencv_image())


