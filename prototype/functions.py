import boto3
from boto3.dynamodb.conditions import Key, Attr

def upload_post(file_name, id, BUCKET, TABLE):
	s3 = boto3.client('s3')
	s3.upload_file(file_name, BUCKET, file_name)
	url = f"https://s3.ap-northeast-2.amazonaws.com/{BUCKET}/{file_name}"
	class_name="crash"
	dynamo = boto3.resource('dynamodb')
	dtable = dynamo.Table(TABLE)
	dtable.put_item(Item = {
		'file_name':file_name,
		'id':id,
		'url':url,
		'class_name':class_name
	})


def get_items(file_name, id, TABLE):
	dynamo = boto3.resource('dynamodb')
	dtable = dynamo.Table(TABLE)
	response = dtable.scan(
		FilterExpression=Attr('file_name').eq(file_name) & Attr('id').eq(id)
	)['Items']
	url - response[0]['url']
	class_name = response[0]['class_name']
	return url, class_name