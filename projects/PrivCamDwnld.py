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