# E-Commerce Restful API By Django

[<img src="https://www.djangoproject.com/s/img/logos/django-logo-negative.png" width="200" title="Django Projects" >](https://github.com/OSAMAMOHAMED1234/django_projects)
[<img src="https://www.mysql.com/common/logos/logo-mysql-170x115.png" width="150" title="Django Projects" >](https://github.com/OSAMAMOHAMED1234/django_projects)

## E-commerce website containes:
* user registration 
* user login
* user logout 
* change password
* reset password
* user delete account
* send activation code when register
* order products
* add review to products
* calculate avg to every product
* contact us message



## Usage :
### Run project by :

``` python

# change database connection information in settings.py DATABASES default values with your info then run 

1. python manage.py migrate

2. python manage.py runserver

# if you want to manage to project just create super user account by :

3. python manage.py createsuperuser

```

That's it.

## Done :

Now the project is running at `http://localhost:8000` and your routes is:


| Route                                          | HTTP Method 	 | Description                           	      |
|:-----------------------------------------------|:--------------|:---------------------------------------------|
| {host}       	                                 | GET       	   | Home page     |
| {host}/admin/  	                               | GET      	     | Admin control panel                     	    |
| {host}/accounts/register/                      | POST      	     | user register           	    |
| {host}/accounts/activate/{code}/               | GET      	     | activate user account after register    |
| {host}/accounts/login/                         | POST      	     | user login           	    |
| {host}/accounts/logout/                        | GET      	     | user logout           	    |
| {host}/accounts/change_password/               | POST      	     | user change password           	    |
| {host}/accounts/profile/                       | GET      	     | user logout           	    |
| {host}/accounts/profile/update/{pk}/            | PUT      	     | user update checkout information           	    |
| {host}/accounts/profile/delete/                | POST      	     | user delete account           	    |
| {host}/accounts/reset_password/                | POST      	     | user email           	    |
| {host}/accounts/reset_password/done/           | POST      	     | send reset password email           	    |
| {host}/accounts/reset_password/confirm/{uidb64}/{token}/        | POST      	     | enter new password           	    |
| {host}/accounts/reset_password/complete/       | POST      	     | finish reset password           	    |
| {host}/products/                                | POST      	     | products page          	    |
| {host}/products/category/{category}/            | GET      	     | search products by category          	    |
| {host}/products/all/                            | GET      	     | all products           	    |
| {host}/products/{slug}/                         | GET      	     | product detail           	    |






| API Route                                     | HTTP Method 	 | Description                           	      |
|:----------------------------------------------|:--------------|:---------------------------------------------|
| {host}/api/accounts/register/                 | POST      	     | user register           	    |
| {host}/api/accounts/login/                    | POST      	     | user login           	    |
| {host}/api/accounts/change_password/              | PUT      	     | user change password           	    |
| {host}/api/accounts/profile/{id}/             | GET      	       | user logout           	    |
| {host}/api/accounts/profile/update/{id}/      | PUT      	     | user update profile information     |
| {host}/api/accounts/profile/delete/{id}/      | DELETE      	     | user delete account           	    |







For detailed explanation on how project work, read the [Django Docs](https://docs.djangoproject.com/en/1.11/) and [MySQLDB Docs](https://dev.mysql.com/doc/)

## Developer
This project made by [Osama Mohamed](https://www.facebook.com/osama.mohamed.ms)

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT)
