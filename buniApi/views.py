# views.py
import requests
import base64
import json
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.shortcuts import render
import datetime
from requests.auth import HTTPBasicAuth


KCB_CONSUMER_KEY = getattr(settings, "KCB_CONSUMER_KEY", "XeFYLf421XWpKgzDxPnCdkh3nMMa")
KCB_CONSUMER_SECRET = getattr(settings, "KCB_CONSUMER_SECRET", "sgWv1yaj8bD4i1WRypef36F82NEa")
KCB_TOKEN_URL = getattr(settings, "KCB_TOKEN_URL", "https://uat.buni.kcbgroup.com/token?grant_type=client_credentials")


def generate_access_token():
    try:
        response = requests.post(
            KCB_TOKEN_URL,
            auth=HTTPBasicAuth(KCB_CONSUMER_KEY, KCB_CONSUMER_SECRET)
        )
        
        if response.status_code != 200:
            return None, f"Failed to get access token: {response.status_code} {response.text}"
        
        access_token_info = response.json()
        return access_token_info.get("access_token"), None
    except Exception as e:
        return None, str(e)

def stk_push(request):

    if request.method == 'POST':
        try:
            phone_number = request.POST.get('phoneNumber')
            amount = request.POST.get('amount')    
            
            if not all([phone_number, amount]):
                return JsonResponse({'error': 'Missing required parameters'}, status=400)

            access_token = generate_access_token()

            if not access_token:
                return JsonResponse({'error': 'Failed to generate access token'}, status=500)

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
            }

            payload = {
                'phoneNumber': phone_number,
                'amount': amount,
                'invoiceNumber': '123456',
                'sharedShortCode': True,
                "orgShortCode": "",
                "orgPassKey": "",
                'callbackUrl': settings.KCB_CALLBACK_URL,
                'transactionDescription': 'belfor Tech',
            }

            response = requests.post(settings.KCB_MPESA_EXPRESS_URL, headers=headers, data=json.dumps(payload))

            if response.status_code == 200:
                return JsonResponse(response.json())
            else:
                print(f'STK Push Error: {response.status_code}, {response.text}')
                return JsonResponse({'error': f'STK push failed: {response.status_code}, {response.text}'}, status=response.status_code)

        except requests.exceptions.RequestException as e:
            print(f"STK push failed: {e}")
            return JsonResponse({"error":f"STK push failed: {e}"}, status=500)

    return render(request, 'payment_form.html')

def stk_push_form(request):
    return render(request, 'payment_form.html')


# def display_token(request):
#     return render(request, 'token_display.html')