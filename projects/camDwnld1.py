import os,datetime,csv, requests,schedule,time, logging,pytz
from xml.etree import ElementTree
from ftplib import FTP
from multiprocessing import Pool
import pysftp

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
camera_inventories,camera_exclusions,valid_cameras = [[]]*3
root_folder_path = '/itrns-iwz/camera_images'
private_root_folder_path = '/itrns-iwz/private_camera_images'
url_string = 'https://atms.iowadot.gov/Iowa.Sims.C2C/IADOT_SIMS_C2C.asmx/OP_ShareCCTVInventoryInformation?MSG_CCTVInventoryRequest=Intrans'


class CameraInventory:
    """
    Class to hold the camera inventory details.
    """
    def __init__(self,device_id,device_name,latitude,longitude,imageURL,videoURL):
        self.device_id = device_id
        self.device_name = device_name
        self.latitude = latitude
        self.longitude = longitude
        self.imageURL = imageURL
        self.videoURL =videoURL

    def __iter__(self):
        return iter([self.device_id,self.device_name,self.latitude,self.longitude])

    def __hash__(self):
        return hash((self.device_id,self.device_name))

    def __eq__(self, other):
        return (self.device_id,self.device_name) == (other.device_id,other.device_name)

    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        return '[{},{}]'.format(self.device_id,self.device_name)


def update_camera_inventory():
    """
    Downloads the camera inventory and creates in-memory objects
    :return:
    """
    logging.debug('Downloading the camera inventory')


    # Create in memory object of the camera feed
    try:
        global camera_inventories
        # Download Camera Invenotry Feed
        content = requests.get(url_string).content
        xml_root = ElementTree.fromstring(content)
        ns = {'tcore': 'http://www.tcoreAddOns.com'}
        temp = [[device.find('./device-inventory-header'), device.find("./tcore:cctv-data-url-list", ns)]
                for device in xml_root.findall('cctv-inventory-item')]
        camera_inventories = []
        for header, dataurl in temp:
            device_id, device_name,latitude, longitude = header.findtext('device-id'),header.findtext('device-name')\
                                        , header.findtext('./device-location/latitude'), header.findtext('./device-location/longitude')

            imageURL, videoURL =dataurl.find('./tcore:static-image-url',ns).text, \
                                dataurl.find('./tcore:live-video-url',ns).text if dataurl.find('./tcore:live-video-url',ns) else None
            camera_inventories.append(CameraInventory(device_id,device_name,latitude,longitude,imageURL,videoURL))

        logging.info('Total number of cameras downloaded: %s', len(camera_inventories))

        # Remove exclusions from the inventory
        global valid_cameras
        valid_cameras = list(set(camera_inventories) - set(camera_exclusions))

        logging.info('Total valid cameras: %s', len(valid_cameras))

        #Finally, Update the camera mapping - Append only the changes
        update_camera_mapping()
    except:
        logging.error('Erorr updating the camera inventory')


def update_camera_mapping():
    """
    Append new Cameras to the camera mapping CSV file. This file is only for the reference.
    :return:
    """
    logging.debug('Updating the camera mapping CSV file.')
    saved_inventories = set()
    file_name = os.path.join(root_folder_path,'camera_mapping.csv')

    # Write header at begining.
    if not os.path.isfile(file_name):
        with open(file_name,'w') as f:
            writer = csv.writer(f)
            headers = ['Id', 'Name', 'Latitude', 'Longitude','ImageURL', 'DateAdded']
            writer.writerow(headers)

    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        # Skip Header
        next(reader)
        for row in reader:
            saved_inventories.add(CameraInventory(row[0],row[1],row[2],row[3],row[4],None))

    diff = set(camera_inventories) - saved_inventories

    if len(diff) > 0 :
        logging.info('New camera identified. Appending them into the CSV file.')
        today =  datetime.date.today().strftime('%Y-%m-%d')
        with open(file_name,'a',newline='') as f:
            writer = csv.writer(f)
            writer.writerows(map(lambda x: list(x)+[today] , diff))


def update_camera_exclusions():
    logging.debug('Updating the camera exclusions list')
    global camera_exclusions
    camera_exclusions = []
    with open(os.path.join(root_folder_path, 'CameraExclusion.csv'), newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            camera_exclusions.append(CameraInventory(row[0], row[1], row[2], row[3], row[4], None))
    logging.info('Total number of excluded cameras: %s', len(camera_exclusions) )



def downloadCameraImages():
    """
    Download images for all cameras
    :return:
    """

    now = datetime.datetime.now()
    logging.info('Stating image download batch at ' + str(now))
	
    with Pool(4) as pool
	
        pool.map(download_camera_image,valid_cameras)

    now = datetime.datetime.now()
    logging.info('Completed image download batch at ' + str(now))

def download_camera_image(camera):
    """
    Download the image for the given camera
    """
    now = datetime.datetime.now()
    now = now.replace(minute=5 * int(now.minute / 5))
    logging.info('Downloading camera images at ' + str(now))
    today_folder_path = now.strftime('%Y%m%d')
    now_file_path = now.strftime('%Y-%m-%d-%H-%M')
    logging.debug('Downloading images at %s', now_file_path)
    logging.debug('Downloading images for camera %s', camera)
    try:
        folder_path = os.path.join(root_folder_path,camera.device_id,today_folder_path)
        os.makedirs(folder_path,exist_ok=True)
        response = requests.get(camera.imageURL, timeout=10)
        if response.status_code == 200:
            with open(os.path.join(folder_path,now_file_path+'.jpg'),'wb') as f:
                f.write(response.content)
    except Exception as e:
        logging.error('Image download failed for camera %s \n error: %s', camera, e)


def download_private_truck_stops():
    """
    Download truck stops from the FTP server
    """
    try:
        now = datetime.datetime.now()
        now = now.replace(minute=5 * int(now.minute / 5))
        logging.info('Downloading truck images at ' + str(now))
        today_folder_path = now.strftime('%Y%m%d')
        now_file_path = now.strftime('%Y-%m-%d-%H-%M')
        ftp = FTP('atms.iowadot.gov')
        ftp.login('ctreisu','ctre123')
        ftp.cwd('/TrkStop')
        all_files = ftp.nlst()
        all_files = [x for x in all_files if x != 'IDOT-logo.jpg']
        for file in all_files:
            try:
                device_id = file.split('.')[0]
                # Get the file modified date (returns in UTC)
                mt = ftp.sendcmd('MDTM '+ file)[4:]
                mod_time = datetime.datetime.strptime(mt,'%Y%m%d%H%M%S').replace(tzinfo = datetime.timezone.utc).astimezone(tz=None)
                latest_file = abs(pytz.timezone('US/Central').localize(now)-mod_time) < datetime.timedelta(seconds = 300)
                folder_path = os.path.join(private_root_folder_path,device_id,today_folder_path)
                os.makedirs(folder_path,exist_ok=True)
                if latest_file:
                    logging.info('Downloading truck image for camera %s', device_id)
                    filename = os.path.join(folder_path,now_file_path+'.jpg')
                    ftp.retrbinary('RETR '+file, open(filename,'wb').write)
                else:
                     logging.info('No latest image available for camera %s', device_id)
            except Exception as e:
                logging.error('Image download failed for camera %s \n error: %s', file, e)

    except Exception as e:
        logging.error('Failed to download truck stops: %s',e)


def download_private_truck_stops_sftp():
    """
    Download truck stops from the sFTP server
    """
    try:
        now = datetime.datetime.now()
        now = now.replace(minute=5 * int(now.minute / 5))
        logging.info('Downloading truck images at ' + str(now))
        today_folder_path = now.strftime('%Y%m%d')
        now_file_path = now.strftime('%Y-%m-%d-%H-%M')
        # Connect sftp
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(host="atms.iowadot.gov", username="ctreisu", password="ctre123", cnopts=cnopts) as sftp:
            sftp.cwd('/TrkStop')
            all_files = sftp.listdir()
            all_files = [x for x in all_files if x != 'IDOT-logo.jpg']
            for file in all_files:
                try:
                    device_id = file.split('.')[0]
                    # Get the file modified date (returns in UTC)
                    mt = sftp.lstat(file).st_mtime
                    mod_time = datetime.datetime.utcfromtimestamp(mt).replace(tzinfo = datetime.timezone.utc).astimezone(tz=None)
                    latest_file = abs(pytz.timezone('US/Central').localize(now)-mod_time) < datetime.timedelta(seconds = 300)
                    folder_path = os.path.join(private_root_folder_path,device_id,today_folder_path)
                    os.makedirs(folder_path,exist_ok=True)
                    if latest_file:
                        logging.info('Downloading truck image for camera %s', device_id)
                        filename = os.path.join(folder_path,now_file_path+'.jpg')
                        sftp.getfo(file, open(filename, 'wb'), callback=None)
                        logging.info('Downloaded truck image for camera %s!', device_id)
                    else:
                         logging.info('No latest image available for camera %s', device_id)
                except Exception as e:
                    logging.error('Image download failed for camera %s \n error: %s', file, e)

    except Exception as e:
        logging.error('Failed to download truck stops: %s',e)


if __name__ == '__main__':
    logging.debug('Started camera image downloader')
    update_camera_exclusions()
    update_camera_inventory()
    logging.info("Initialization completed.")
    downloadCameraImages()
    download_private_truck_stops_sftp()
    schedule.every().day.at("00:02").do(update_camera_inventory)
    schedule.every(5).minutes.do(downloadCameraImages)
    schedule.every(5).minutes.do(download_private_truck_stops_sftp)
    while True:
        schedule.run_pending()
        time.sleep(1)

    # downloadCameraImages()