"""
-*- coding: utf-8 -*-
========================
AWS Lambda
========================
Contributor: Bharath Chandra Anumukonda (Srce Cde)
========================
"""
import boto3


def lambda_handler(event, context):
    """Read file from s3 on trigger."""
    s3 = boto3.client("s3")
    if event:
        file_obj = event["Records"][0]
        bucketname = str(file_obj['s3']['bucket']['name'])
        filename = str(file_obj['s3']['object']['key'])
        print("Filename: ", filename)
        fileObj = s3.get_object(Bucket=bucketname, Key=filename)
        file_content = fileObj["Body"].read().decode('utf-8')
        print(file_content)
    return 'Thanks'
	
	--
	
	"""
-*- coding: utf-8 -*-
========================
AWS Lambda
========================
"""
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def lambda_handler(event, context):
    
    ses = boto3.client("ses")
    s3 = boto3.client("s3")

    for i in event["Records"]:
        action = i["eventName"]
        ip = i["requestParameters"]["sourceIPAddress"]
        bucket_name = i["s3"]["bucket"]["name"]
        object = i["s3"]["object"]["key"]

    fileObj = s3.get_object(Bucket = bucket_name, Key = object)
    file_content = fileObj["Body"].read()

    sender = "bharathc@iastate.edu"
    to = "bharathc@iastate.edu"
    subject = str(action) + 'Event from ' + bucket_name
    body = """
        <br>
        This email is to notify you regarding {} event.
        The object {} is uploaded.
        Source IP: {}
    """.format(action, object, ip)

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to

    body_txt = MIMEText(body, "html")

    attachment = MIMEApplication(file_content)
    attachment.add_header("Content-Disposition", "attachment", filename=object)

    msg.attach(body_txt)
    msg.attach(attachment)

    response = ses.send_raw_email(Source = sender, Destinations = [to], RawMessage = {"Data": msg.as_string()})
    
    return "Thanks"
	
	---
	
	
	
	import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def lambda_handler(event, context):
    
    ses = boto3.client("ses")
    s3 = boto3.client("s3")

    for i in event["Records"]:
        action = i["eventName"]
        ip = i["requestParameters"]["sourceIPAddress"]
        bucket_name = i["s3"]["bucket"]["name"]
        object = i["s3"]["object"]["key"]

    fileObj = s3.get_object(Bucket = bucket_name, Key = object)
    file_content = fileObj["Body"].read()
	recipients = ['bharathc@iastate.edu', 'aravindk@iastate.edu']
    sender = "bharathc@iastate.edu"
    to = "bharathc@iastate.edu"
    subject = str(action) + 'Event from ' + bucket_name
    body = """
        <br>
        This email is to notify you regarding {} event.
        The object {} is uploaded.
        Source IP: {}
    """.format(action, object, ip)

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender
    msg['To'] = ', '.join(recipients)

    body_txt = MIMEText(body, "html")

    attachment = MIMEApplication(file_content)
    attachment.add_header("Content-Disposition", "attachment", filename="monitoring.html")

    msg.attach(body_txt)
    msg.attach(attachment)

    response = ses.send_raw_email(Source = sender, Destinations = [recipients], RawMessage = {"Data": msg.as_string()})
    
    return "Thanks"