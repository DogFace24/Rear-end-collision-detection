from ultralytics import YOLO

model = YOLO("yolov8s.pt")
#model.train(data="coco128.yaml", epochs = 10)

results = model.predict("crash.mp4", save = True)
#print(results)

'''
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    #result.show()  # display to screen
    result.save(filename="result.mp4")  # save to disk
'''