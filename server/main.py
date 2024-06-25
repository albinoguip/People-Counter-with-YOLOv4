from fastapi import FastAPI, UploadFile, File, Form
import cv2
import numpy as np
from typing import List, Dict
from pydantic import BaseModel

app = FastAPI()

# Carregar modelo YOLO
net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Dicionário de trackers por cliente
person_counts  : Dict[str, int ] = {}
person_posicoes: Dict[str, list] = {}
person_centros : Dict[str, list] = {}

@app.post("/detect/")
async def detect_persons(file     : UploadFile = File(...), 
                         client_id: str        = Form(...)
                         ):
    
    contents = await file.read()
    nparr    = np.frombuffer(contents, np.uint8)
    img      = cv2.imdecode(nparr, cv2.IMREAD_COLOR)


    if client_id not in person_counts:
        person_counts[client_id]   = 0
        person_posicoes[client_id] = []
        person_centros[client_id]  = []

    height, width, channels = img.shape
    blob = cv2.dnn.blobFromImage(img, 0.00392, (608, 608), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)

            if class_id == 0:   # Classe 0 é a pessoa
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    try:
        result_boxes = [boxes[i] for i in indexes.flatten()]
    except:
        result_boxes = []


    if len(result_boxes) > len(person_posicoes[client_id]):
        n_novas                  =  len(result_boxes) - len(person_posicoes[client_id])
        person_counts[client_id] += n_novas

    person_posicoes[client_id] = result_boxes

    return {"boxes": result_boxes, "total_persons": person_counts[client_id]}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
