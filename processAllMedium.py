import time
import os
import Metashape


def process():

	# get path
	path = Metashape.app.getExistingDirectory("Provide folder with photos")
	
	### processing parameters
	accuracy = Metashape.Accuracy.MediumAccuracy  #align photos accuracy
	reference_preselection = False
	generic_preselection = True
	keypoints = 40000 #align photos key point limit
	tiepoints = 4000 #align photos tie point limit
	source = Metashape.DataSource.DenseCloudData #build mesh/DEM source
	surface = Metashape.SurfaceType.Arbitrary #build mesh surface type
	quality = Metashape.Quality.MediumQuality #build dense cloud quality
	filtering = Metashape.FilterMode.MildFiltering #depth filtering
	interpolation = Metashape.Interpolation.EnabledInterpolation #build mesh interpolation
	# blending = Metashape.BlendingMode.MosaicBlending #blending mode
	face_num = Metashape.FaceCount.MediumFaceCount #build mesh polygon count
	# mapping = Metashape.MappingMode.GenericMapping #build texture mapping
	atlas_size = 4096
	TYPES = ["jpg", "jpeg", "tif", "tiff"]
	###end of processing parameters definition

	print("Processing " + path)
	list_files = os.listdir(path)
	list_photos = list()
	for entry in list_files: #finding image files
		file = path + "/" + entry
		if os.path.isfile(file):
			if file[-3:].lower() in TYPES:
				list_photos.append(file)
	if not(len(list_photos)):
		print("No images in " + path)
		return False

	print(list_photos)

	# Create project
	doc = Metashape.app.document
	doc_path = Metashape.app.getSaveFileName("Save Project As")
	try:
		doc.save(doc_path + '.psx')
	except RuntimeError:
		Metashape.app.messageBox("Can't save project")

	# Add chunk
	chunk = doc.addChunk()
	print(doc_path)
	chunk.label = doc_path.rsplit("/", 1)[1]

	###align photos
	chunk.addPhotos(list_photos)
	chunk.matchPhotos(accuracy = accuracy, generic_preselection = generic_preselection, reference_preselection = reference_preselection, filter_mask = False, keypoint_limit = keypoints, tiepoint_limit = tiepoints)
	chunk.alignCameras()
	chunk.optimizeCameras()
	chunk.resetRegion()
	doc.save()

		
	###building dense cloud
	chunk.buildDepthMaps(quality = quality, filter = filtering)
	chunk.buildDenseCloud(point_colors = True, keep_depth = False)
	doc.save()

	###building mesh
	chunk.buildModel(surface = surface, source = source, interpolation = interpolation, face_count = face_num)
	doc.save()

	## building DEM
	chunk.buildDem(source = source, interpolation = interpolation, flip_x=False, flip_y=False, flip_z=False)
	doc.save()

	## building Orthomosaic
	surface_data = Metashape.DataSource.ElevationData
	chunk.buildOrthomosaic(surface = surface_data)


def main():


	t0 = time.time()
	print("Script started...")
	
	process()

	t1 = time.time()
	t1 -= t0
	t1 = float(t1)	

	print("Script finished in " + "{:.2f}".format(t1) + " seconds.\n")
	return

main()