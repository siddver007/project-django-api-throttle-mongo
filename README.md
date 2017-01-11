# throttlr
A simple project in Django using MongoDB to show API rate limiting by simple throttling process and completely using Mongo as the rate-limiting-backend. It shows a daily rate-limit scenario. There are 3 plans:-  
1.Free - a rate limit of 100 per day.  
2.Gold - a rate limit of 1000 per day.  
3.Platinum - unlimited API calls.  

** This project uses MongoEngine as the MongoDB driver for Django.


## HOW TO RUN

1. Clone the project or download the zip.
2. Install virtual environment for your convenience.
3. Install the dependencies/requirements using command "pip install -r requirements.txt"
4. Install MongoDB server and start the server.(Preferred Mongo version is v2.6.11)
5. Now fire up the Django project using command "python manage.py runserver 0.0.0.0:8000"


## HOW TO USE

1. Go to URL "http://localhost:8000"  -- this is the homepage and is used to register new users.  
	1.1 Enter name, id, password and choose the desired plan by clicking it.  
	1.2 Click on "Sign Me Up" button to register a user.  
	1.3 A verification e-mail would be sent to provided E-Mail ID.  
	1.4 Now a new view/page "post" to post data would open. -- you can't post anything without verification  
	
	Already registered users can go to the "post" page directly by clicking the "Already registered hyperlink above".

2. You can post the data by going to the URL "http://localhost:8000/post" -- although you would be automatically redirected there when you register  	
	2.1 Here just put the E-Mail ID and password with which you registered and enter the data to be posted. --this is only to show the API so no sessions are created  
	2.2 Click on the "Post" button to post the data.  



## SOME OTHER NOTES

1. This is a very basic implementation to show rate-limiting using django.  
2. This shows rate-limiting on a daily basis and not 24 hrs from the date and time of registration.  	
3. It completely uses MongoDB though MongoDB is not the most preferred DB to be used with Django.  
4. It's only to show basic working so many security flaws like the saved passwords are not hashed ,.etc are not taken into account.  
5. A much better rate-limiting implementation could be done using a Middleware and a faster caching backend like Redis.  
6. No sessions are created since it is only to show API.  
7. There might be some issues/errors/problems and would be rectified by more rigorous testing.  
