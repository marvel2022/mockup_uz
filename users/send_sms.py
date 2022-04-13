from django.conf import settings
import requests


def send_confirmation_code(token, phone_number, confirmation_code):
	endpoint = 'https://notify.eskiz.uz/api/message/sms/send'

	bt = 'Bearer '+str(token)
	header = {
		'Authorization': bt,
	}
	phone_number = str(phone_number)[1:]
	text="mockup.uz. \nYour confirmation code: " + str(confirmation_code)
	params = {
		'mobile_phone': phone_number,
		'message': text,
		'from': "4546",
	}
	try:
		response = requests.post(endpoint, headers=header, params=params)
	except Exception as e:
		print("Error has been accured while progress: ", e)		
	return response.json()

def send_sms(phone_number, confirmation_code):
	endpoint = 'https://notify.eskiz.uz/api/auth/login'
	params = {
		'email': settings.AUTHY_EMAIL, 
		'password': settings.AUTHY_KEY
	}
	response = requests.post(endpoint, params=params)
	token = response.json()['data'].get('token')
	print(response.text)

	result = send_confirmation_code(token, phone_number, confirmation_code)
	return result