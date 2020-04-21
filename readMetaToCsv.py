import Metashape
import csv

def readDJI():
    doc = Metashape.app.document
    chunk = doc.chunk

    csv_path = Metashape.app.getSaveFileName("Save Project As")

    header = False
    with open(csv_path, 'w') as f:
        
        for camera in chunk.cameras:
            # print(camera.photo.meta)
            metaData = dict(camera.photo.meta.items())
            metaData['PhotoName'] = camera.label
            if not header:
                writer = csv.DictWriter(f,metaData.keys())
                writer.writeheader()
                header = True
            writer.writerow(metaData)
    print("Done")

label = "Read and Save DJI metadata to csv"
Metashape.app.addMenuItem(label, readDJI)
print("To execute this script press {} on manu bar".format(label))
