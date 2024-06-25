import cv2
import requests
import os
import time

def send_frame(video_path, server_url, client_id):

    cap  = cv2.VideoCapture(video_path)
    cont = 0

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            print(f"[{client_id}] Finished processing the video.")
            break

        _, img_encoded = cv2.imencode('.jpg', frame)
        response       = requests.post(server_url, 
                                       files = {"file": img_encoded.tobytes()}, 
                                       data  = {"client_id": client_id})       

        time.sleep(0.1)  # Small delay to avoid overwhelming the server
        cont += 1

    cap.release()

    return response.json()

if __name__ == "__main__":

    time.sleep(2) # Waiting fpr server to start

    video_path = os.getenv("VIDEO_PATH")
    server_url = os.getenv("SERVER_URL")
    client_id  = os.getenv("CLIENT_ID") 

    print(f"[{client_id}] Starting to process the video: {video_path}")

    data = send_frame(video_path, server_url, client_id)

    print(f"[{client_id}] Total Number of People in the Video: {data['total_persons']}")
    print(f"[{client_id}] Exiting...")
