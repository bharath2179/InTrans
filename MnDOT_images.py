import os, datetime, requests, schedule, time, logging

def download_camera_image():
    """
    Download the image for the given camera
    """
    cam_list = ['https://video.dot.state.mn.us/video/image/metro/C30163?1595339851498','https://video.dot.state.mn.us/video/image/metro/C30162?1595340465218','https://video.dot.state.mn.us/video/image/metro/C30161?1595340501406','https://video.dot.state.mn.us/video/image/metro/C30160?1595340529040','https://video.dot.state.mn.us/video/image/metro/C30159?1595340554309']
    cam_names = ['C30163','C30162','C30161','C30160','C30159']
    root_folder_path = "/lss/research/itrns-iwz/MnDOT_images"
    now = datetime.datetime.now()
    now = now.replace(minute=5 * int(now.minute / 5))
    logging.info('Downloading camera images at ' + str(now))
    today_folder_path = now.strftime('%Y%m%d')
    now_file_path = now.strftime('%Y-%m-%d-%H-%M')
    logging.debug('Downloading images at %s', now_file_path)
    try:
        folder_path = os.path.join(root_folder_path, today_folder_path)
        for i in range(len(cam_list)):
            print(cam_list[i])
            response = requests.get(cam_list[i], timeout=10)
            folder_path = os.path.join(root_folder_path, cam_names[i], today_folder_path)
            print(folder_path)
            os.makedirs(folder_path, exist_ok=True)
            i +=1
            if response.status_code == 200:
                with open(os.path.join(folder_path, now_file_path + '.jpg'), 'wb') as f:
                    f.write(response.content)
    except Exception as e:
        logging.error('Image download failed for camera %s \n error: %s', e)

if __name__ == '__main__':
    logging.debug('Started camera image downloader')
    download_camera_image()
    schedule.every(5).minutes.do(download_camera_image())
    while True:
        schedule.run_pending()
        time.sleep(1)
		