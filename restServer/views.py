from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import base64
import datetime
from models import *

# View to register users
class registerView(TemplateView):
	template_name = 'index.html'
	
	# To generate a basic cipher text
	def gen_hash(self,msg_text):
		cipher = base64.b64encode(msg_text + 'qwasswaq')
		return cipher
	# To send verification e-mail to registered user	
	def send_mail(self,send_from, send_to, subject, text,login, password):
		assert isinstance(send_to, list)
		server='mail.smtp2go.com'
		msg = MIMEMultipart()
		msg= MIMEText(text)
		msg['Subject']=subject
		msg['To']=COMMASPACE.join(send_to)
		msg['Date']=formatdate(localtime=True)
		server = smtplib.SMTP_SSL(server,465)
		server.login(login,password)
		server.sendmail(send_from, send_to, msg.as_string())
		server.close()


	def post(self,req):
		try:
			post = User()
			post.name = req.POST['form-full-name']
			post.user_id = req.POST['form-id']
			post.password = req.POST['form-password']
			if req.POST['form-plan'] == 'Free' or req.POST['form-plan'] == 'Gold' or req.POST['form-plan'] == 'Platinum':
				post.plan = req.POST['form-plan']
			else:
				return HttpResponseRedirect(reverse('restServer:error',kwargs={'code':'4xe'}))	
			post.isVerified = False
			post.counter = 0
			post.save()
			self.send_mail(
				send_from = 'noreply@neuronme.com',
				send_to = [req.POST['form-id']],
				subject = 'E-Mail Verification',
				text = 'Welcome to rest-api-neuron\nPlease verify the email by clicking the link below\n\nhttp://localhost:8000/verify/%s' % self.gen_hash(req.POST['form-id']) ,
				login = 'halo_bla',
				password = 'bla_halo01'
				)
			print 'MAIL SENT!!!!!'
			return HttpResponseRedirect(reverse('restServer:success',kwargs={'code':'1xs'}))
		except NotUniqueError:	
			return HttpResponseRedirect(reverse('restServer:error',kwargs={'code':'1xe'}))


# View to post data by registered users
class postView(TemplateView):
	template_name = 'user_post.html'
	
	def post(self,req):
		try:
			# Check whether user exists
			user = User.objects.get(user_id = req.POST['form-id'], password = req.POST['form-password'])

			# Check whether user's e-mail has been verified or not
			if user.isVerified == True:

				# Flow for Free-plan users
				if user.plan == 'Free':
					if user.dateModified.date() == datetime.datetime.now().date():
						if user.counter < 100:
							data = Data()
							data.user_id = user.user_id
							data.content = req.POST['form-post-data']
							data.save()
							user.counter += 1
							user.save()
							return HttpResponseRedirect(reverse('restServer:success',kwargs={'code':'2xs1>1' + req.POST['form-post-data']}))
						else:
							return HttpResponseRedirect(reverse('restServer:error',kwargs={'code':'6xe'}))	
					else:
						data = Data()
						data.user_id = user.user_id
						data.content = req.POST['form-post-data']
						data.save()
						user.dateModified = datetime.datetime.now()
						user.counter = 1	
						user.save()	
						return HttpResponseRedirect(reverse('restServer:success',kwargs={'code':'2xs1>1' + req.POST['form-post-data']}))
				
				# Flow for Gold-plan users
				elif user.plan == 'Gold':
					if user.dateModified.date() == datetime.datetime.now().date():
						if user.counter < 1000:
							data = Data()
							data.user_id = user.user_id
							data.content = req.POST['form-post-data']
							data.save()
							user.counter += 1
							user.save()
							return HttpResponseRedirect(reverse('restServer:success',kwargs={'code':'2xs1>1' + req.POST['form-post-data']}))
						else:
							return HttpResponseRedirect(reverse('restServer:error',kwargs={'code':'6xe'}))	
					else:
						data = Data()
						data.user_id = user.user_id
						data.content = req.POST['form-post-data']
						data.save()
						user.dateModified = datetime.datetime.now()
						user.counter = 1	
						user.save()	
						return HttpResponseRedirect(reverse('restServer:success',kwargs={'code':'2xs1>1' + req.POST['form-post-data']}))	
				
				# Flow for Platinum-plan users
				elif user.plan == 'Platinum':
					data = Data()
					data.user_id = user.user_id
					data.content = req.POST['form-post-data']
					data.save()
					user.counter += 1
					user.save()
					return HttpResponseRedirect(reverse('restServer:success',kwargs={'code':'2xs1>1' + req.POST['form-post-data']}))
				
				else:
					return HttpResponseRedirect(reverse('restServer:error',kwargs={'code':'5xe'}))	
			
			else:
				return HttpResponseRedirect(reverse('restServer:error',kwargs={'code':'3xe'}))	
		
		except DoesNotExist:
			return HttpResponseRedirect(reverse('restServer:error',kwargs={'code':'2xe'}))

		
# View to display successful activity
class successView(TemplateView):
	template_name = 'success.html'

	def get_context_data(self, **kwargs):
		context = super(successView, self).get_context_data(**kwargs)
		if kwargs['code'] == '1xs':
			context['success_body'] = 'User created. Please verify your e-mail.'
		else:
			context['success_body'] = 'Data : <<' + kwargs['code'].split('1>1')[1] + '>> successfully posted.'	
		return context


# View to display erroneous activity
class errorView(TemplateView):
	template_name = 'error.html'

	def get_context_data(self, **kwargs):
		context = super(errorView, self).get_context_data(**kwargs)
		if kwargs['code'] == '1xe':
			context['error_body'] = 'User already exist. Please try again.'
		elif kwargs['code'] == '2xe':
			context['error_body'] = 'Invalid user credentials. Please try again.'	
		elif kwargs['code'] == '3xe':
			context['error_body'] = 'User not verified. Please verify your e-mail.'	
		elif kwargs['code'] == '4xe':
			context['error_body'] = 'Don\'t try to fiddle with the API ;P' 
		elif kwargs['code'] == '5xe':
			context['error_body'] = 'Some error occurred. Please try again.' 
		elif kwargs['code'] == '6xe':
			context['error_body'] = 'API rate limit exceeded for today!!!!!' 			
		return context

# View to display e-mail verification status
class verifyView(TemplateView):
	template_name = 'verify.html'

	def get_context_data(self, **kwargs):
		context = super(verifyView, self).get_context_data(**kwargs)
		try:
			user = User.objects.get(user_id = base64.b64decode(kwargs['code']).replace('qwasswaq',''))
			if user.isVerified == False:
				user.isVerified = True
				user.save()
				context['verify_body'] = 'Verification successful. Enjoy your API...'
			else:
				raise Exception	
		except Exception:
			context['verify_body'] = 'There was some problem with verification.'
		
		return context