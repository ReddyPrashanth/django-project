from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from botocore.exceptions import ClientError
import re
import boto3
import json

# Create your views here.

aws_session = boto3.Session(profile_name='sns')

def home(request):
    return render(request, 'core/home.html')

def portfolio(request):
    return render(request, 'core/portfolio.html')

def download_resume(request):
    try:
        s3 = aws_session.client('s3')
        url = s3.generate_presigned_url(
            ClientMethod='get_object', 
            Params={'Bucket': 'psreepathi-portfolio', 'Key': 'psreepathi-resume.pdf'},
            ExpiresIn=3600
        )
        return HttpResponseRedirect(url)
    except ClientError as e:
        JsonResponse({'error', 'Cannot download file. Please try again'}, status=404)

def contact(request):
    data = json.loads(request.body)
    if not (bool(data.get('name', False)) and bool(data.get('email', False)) and bool(data.get('message', False))):
        return JsonResponse({'error': 'All fields are required.'}, status=400)
    email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if(not email.match(data['email'])):
        return JsonResponse({'error': 'Email is not valid. Provide a valid email address.'}, status=400)
    try:
        sns = aws_session.client('sns')
        sns.publish(
            TopicArn = settings.SNS_ARN,
            Message='{message}. Email: {sender}'.format(message=data['message'], sender=data['email']),
            Subject='Message from {sender}'.format(sender=data['name'])
        )
    except Exception:
        return JsonResponse({'error': 'Unable to send message. Please try again.'}, status=400)
    return JsonResponse(data, status=200)