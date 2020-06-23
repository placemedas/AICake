from imutils import paths
import pathlib
import argparse
import requests
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--urls", required=True,
	help="path to file containing image URLs")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory of images")
args = vars(ap.parse_args())
# grab the list of URLs from the input file, then initialize the
# total number of images downloaded thus far
rows = open(args["urls"]).read().strip().split("\n")
total = 0

# loop the URLs
for url in rows:
	try:
		# try to download the image
		r = requests.get(url, timeout=60)

		if r._content[0] == 0x89:
			p = os.path.sep.join([args["output"], "{}.png".format(str(total).zfill(8))])
		else:
			p = os.path.sep.join([args["output"], "{}.jpg".format(str(total).zfill(8))])

		# save the image to disk
		#p = os.path.sep.join([args["output"], "{}.jpg".format(
		#p = os.path.sep.join([os.getcwd(), "{}.jpg".format(
		#	str(total).zfill(8))])
		#p = "{}.jpg".format(str(total).zfill(8))
		print(p)
		f = open(p, "wb")
		f.write(r.content)
		f.close()
		# update the counter
		print("[INFO] downloaded: {}".format(p))
		total += 1
	# handle if any exceptions are thrown during the download process
	except:
		print("[INFO] error downloading {}...skipping".format(p))

#act_path = pathlib.PureWindowsPath(args["output"])
#print(act_path.as_posix())
#print(act_path)
for imagePath in paths.list_images(args["output"]):
	# initialize if the image should be deleted or not
	delete = False
	print(imagePath)
	#act_path = pathlib.PureWindowsPath(imagePath)
	#print(act_path.as_posix())
	#image = cv2.imread(act_path)
	# try to load the image
	try:
		image = cv2.imread(imagePath)
		print(image)
		# if the image is `None` then we could not properly load it
		# from disk, so delete it
		if image is None:
			delete = True
	# if OpenCV cannot load the image then the image is likely
	# corrupt so we should delete it
	except:
		print("Except")
		delete = True
	# check to see if the image should be deleted
	if delete:
		print("[INFO] deleting {}".format(imagePath))
		os.remove(imagePath)