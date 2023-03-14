import boto3
import time
from boto3.dynamodb.conditions import Key, Attr

def id_duplication_check(uid, TABLE):
	dynamo = boto3.resource('dynamodb')
	dtable = dynamo.Table(TABLE)
	response = dtable.scan(
		FilterExpression=Attr('id').eq(uid)
	)['Items']
	if response:
		return True
	else:
		return False

def register_member(uid, pw, TABLE):
	dynamo = boto3.resource('dynamodb')
	dtable = dynamo.Table(TABLE)
	dtable.put_item(Item = {
		'id':uid,
		'pw':pw
	})

def login_check(uid, pw, TABLE):
	dynamo = boto3.resource('dynamodb')
	dtable = dynamo.Table(TABLE)
	response = dtable.scan(
		FilterExpression=Attr('pw').eq(pw) & Attr('id').eq(uid)
	)['Items']
	if response:
		return True
	else:
		return False

def upload_video(file_name, uid, BUCKET, TABLE):
	s3 = boto3.client('s3')
	s3.upload_file(file_name, BUCKET, file_name)
	url = f"https://s3.ap-northeast-2.amazonaws.com/{BUCKET}/{file_name}"
	class_name="crash"
	upload_time = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))

	dynamo = boto3.resource('dynamodb')
	dtable = dynamo.Table(TABLE)
	dtable.put_item(Item = {
		'file_name':file_name,
		'id':uid,
		'file_url':url,
		'class_name':class_name,
		'upload_time':upload_time
	})


def get_result(file_name, uid, TABLE):
	dynamo = boto3.resource('dynamodb')
	dtable = dynamo.Table(TABLE)
	response = dtable.scan(
		FilterExpression=Attr('file_name').eq(file_name) & Attr('id').eq(uid)
	)['Items']
	url = response[0]['file_url']
	class_name = response[0]['class_name']
	return url, class_name



def get_all_video(uid, TABLE):
	dynamo = boto3.resource('dynamodb')
	dtable = dynamo.Table(TABLE)
	response = dtable.scan(
		FilterExpression= Attr('id').eq(uid)
	)['Items']
	if response:
		file_names = dtable.scan(
			FilterExpression=Attr('id').eq(uid), 
			ProjectionExpression='file_name'
		)['Items']

		for i in range(len(file_names)):
			file_names[i] = file_names[i]['file_name']
			file_names[i] = file_names[i][8:]

		class_names = dtable.scan(
			FilterExpression=Attr('id').eq(uid), 
			ProjectionExpression='class_name'
		)['Items']

		for i in range(len(class_names)):
			class_names[i] = class_names[i]['class_name']

		urls = dtable.scan(
			FilterExpression=Attr('id').eq(uid), 
			ProjectionExpression='file_url'
		)['Items']

		for i in range(len(urls)):
			urls[i] = urls[i]['file_url']

		upload_times = dtable.scan(
			FilterExpression=Attr('id').eq(uid), 
			ProjectionExpression='upload_time'
		)['Items']

		for i in range(len(upload_times)):
			upload_times[i] = upload_times[i]['upload_time']
		
	else:
		file_names = []
		urls = []
		class_names = []
		upload_times = []
	return file_names, urls, class_names, upload_times

def delete_video(key, uid, BUCKET, TABLE):
	dynamo = boto3.resource('dynamodb')
	dtable = dynamo.Table(TABLE)
	file_name = "uploads/"+key
	
	response = dtable.delete_item(
		Key={
		'file_name': file_name,
		'id': uid
		}
	)
	s3 = boto3.client('s3') 
	s3.delete_object(Bucket=BUCKET, Key=file_name)


def admin_get_all_mem(TABLE):
	dynamo = boto3.resource('dynamodb')
	dtable = dynamo.Table(TABLE)
	response = dtable.scan()['Items']
	if response:
		uids = dtable.scan(
			ProjectionExpression='id'
		)['Items']

		for i in range(len(uids)):
			uids[i] = uids[i]['id']

	else:
		uids = []
	
	return uids
