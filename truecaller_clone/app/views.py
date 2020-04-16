from django.http import HttpResponseServerError , HttpResponse , Http404 , JsonResponse
from django.shortcuts import render ,redirect
import pdb , re , json , jwt
from .models import *
from django.contrib import auth,messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from random import randint , choice
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django_reorder.reorder import reorder
from itertools import chain
from django.db import connection


def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]

def encode_data(data):
    if type(data) is dict:
        jwt_token = {'token':jwt.encode(data, 'industrybuying', algorithm='HS256').decode('utf-8')}
    else:
        jwt_token = {'token':jwt.encode({'data': data}, 'industrybuying', algorithm='HS256').decode('utf-8')}

    return jwt_token

def decode_token(token):
    data=jwt.decode(token, 'industrybuying', algorithms=['HS256'])
    return data




def index(request):
    payload = {
        "mobile":"95401502122",
        "password":"hehehehee"
    }
    token = encode_data(payload)
    print(token)
    data = decode_token(token['token'])
    print(data)
    # auth.logout(request)

    return HttpResponse(json.dumps(token,default=str),status=200,content_type="application/json")


######################################################
############ USER MANAGEMENT CODE ####################
######################################################



@csrf_exempt
@api_view(('POST',))
def register(request):
    # pdb.set_trace()

    data = json.loads(request.body.decode('utf-8'))
    mobile = data['mobile']
    email = data['email']
    password = data['password']
    name = data['name']
    user_existed = User.objects.filter(username=mobile)
    if user_existed:
        return JsonResponse({'status':'False','message':'Mobile Number Already Exist'}, status=400)
    else:
        User.objects.create_user(username=mobile,first_name=name,email=email,password=password)
        # user = auth.authenticate(username=mobile, password=password)
        # request.session['username'] = mobile
        # auth.login(request, user)
        return JsonResponse({'status':'True','message':'User Successfully Registered'}, status=200)



@csrf_exempt
@api_view(('POST',))
def login(request):
    pdb.set_trace()
    if request.user.is_authenticated:
        return JsonResponse({'status':'true','message':'Logged In'}, status=200)

    else:
        data = json.loads(request.body.decode('utf-8'))
        if not data:
            return JsonResponse({'status':'False','message':'No Data Received'}, status=400)
        login_data = decode_token(data['token'])
        print(login_data)
        username = login_data.get('mobile')
        print('user',username)
        password = login_data.get('password')
        print('pass',password)


        user_existed = User.objects.filter(username=username)
        if not user_existed:
            return JsonResponse({'status':'False','message':'Please Register First'}, status=400)


        user = auth.authenticate(username=username, password=password)
        if not user:
            return JsonResponse({'status':'false','message':'Incorrect Mobile number Or Password'}, status=400)
        else:
            username=user_existed[0].username
            request.session['username'] = username
            # pdb.set_trace()
            auth.login(request, user)
            return JsonResponse({'status':'true','message':'Logged In'}, status=200)



def logout(request):
    auth.logout(request)
    return JsonResponse({'status':'True','message':'Logged Out'}, status=200)



##################### MANAGEMENT CODE ENDS ####################



#####################################################################
#########################  DUMMY DATA ENTRY CODE  ###################
#####################################################################


def dummy_user_data(request):
    pdb.set_trace()
    x=['Abigail', 'Alexandra', 'Alison', 'Amanda', 'Amelia', 'Amy', 'Andrea', 'Angela', 'Anna', 'Anne', 'Audrey', 'Ava', 'Bella', 'Bernadette', 'Carol', 'Caroline', 'Carolyn', 'Chloe', 'Claire', 'Deirdre']
    for i in x:
        mobile=randint(9911277500,9999999999)
        name = i
        email = i + '@gmail.com'
        password = i.lower()
        User.objects.create_user(username=mobile,first_name=name,email=email,password=password)
        return HttpResponse('dummy user data added')


def dummy_contact_data(request):
    pdb.set_trace()
    x=[4,7,12,15,23,24]
    y=['Amelia', 'Amy', 'Andrea', 'Angela', 'Anna', 'Anne', 'Audrey', 'Ava', 'Bella', 'Bernadette', 'Carol', 'Caroline', 'Carolyn', 'Chloe', 'Claire', 'Deirdre', 'Diana', 'Diane', 'Donna', 'Dorothy', 'Elizabeth', 'Ella', 'Emily', 'Emma', 'Faith', 'Felicity', 'Fiona', 'Gabrielle', 'Grace', 'Hannah', 'Heather', 'Irene', 'Jan', 'Jan']

    for i in x:
        user_id = i
        range1=randint(3,10)
        for _ in range(range1):

            name = choice(y)
            mobile=randint(9911277500,9911277520)
            data = User.objects.filter(username=str(mobile))
            if data:
                registered='yes'
            else:
                registered='no'


            UserContacts.objects.create(user_id=user_id,mobile=mobile,name=name,registered=registered)
    return HttpResponse('dummy contacts added')


def dummy_mark_spam(request):
    pdb.set_trace()
    for _ in range(100):
        mobile=randint(9911277500,9911277520)

        data=Spam.objects.filter(mobile=mobile)
        if data:
            print("previous mobile number >>>>>>")
            data = data[0]
            data.count += 1
            data.save()

        else:
            print("new mobile no. >>>>")
            Spam.objects.create(mobile=mobile)
    return JsonResponse({'status':'True','message':'Mobile number marked as spam'}, status=200)
    

#########################  DUMMY DATA ENTRY CODE ENDS ###################


################################ MAIN FUNCTIONALITY STARTS ########################



@login_required          ## we can either login_required decorator or request.user.is_authenticated functionality
@api_view(('GET',))
def mark_spam(request,mobile=None):
    pdb.set_trace()
    print(mobile)
    print(type(mobile))
    data=Spam.objects.filter(mobile=mobile)
    if data:
        data = data[0]
        data.count += 1
        data.save()

    else:
        Spam.objects.create(mobile=mobile)
    return JsonResponse({'status':'True','message':'Mobile number marked as spam'}, status=200)


def user_search(request,term=None):
    pdb.set_trace()
    print(term)
    try:
        if term.isdigit():
            data = User.objects.filter(username=term).values('username','first_name')
            if data:
                person = data[0]
                token=encode_data(person)         ### fetched information is sent in the form of JWT token
                print(token)
                return JsonResponse(token, status=200)
            else:
                data=UserContacts.objects.filter(mobile=term).only('user_id','mobile','name')
                if data:
                    data = serialize('json',data)
                    print(data)
                    token = encode_data(data)
                    print(token)
                    return JsonResponse(token, status=200)
                else:
                    return JsonResponse({'status':'False','message':'search returned no results'}, status=200)  
        else:
            cursor = connection.cursor()
            query = f'''SELECT uc.mobile AS mobile,uc.name AS name,st.count FROM user_contacts uc LEFT JOIN spam_table st ON uc.mobile = st.mobile WHERE uc.registered LIKE 'no' AND (lower(uc.name) LIKE '{term}%' OR lower(uc.name) LIKE '%{term}%') UNION SELECT u.username AS mobile,u.first_name AS name,s.count FROM `auth_user` u LEFT JOIN spam_table s on u.username=s.mobile WHERE lower(u.first_name) LIKE '{term}%' OR lower(u.first_name) LIKE '%{term}%' ORDER BY CASE WHEN lower(name) LIKE 'am%' THEN 1 WHEN lower(name) LIKE '%am%' THEN 2 ELSE 3 END'''
            cursor.execute(query)
            data = dictfetchall(cursor)
            print(data)
            token = encode_data(data)
            print(token)
            return JsonResponse(token, status=200)

    except Exception as e:
        return JsonResponse({'status':'False','message':f'{e}'}, status=400)  

@csrf_exempt
# @login_required
@api_view(('POST',))
def user_details(request):

    '''
    Data can be posted from frontend in the form of JWT and decoded using decode_data() function
    '''
    pdb.set_trace()
    # user_id = request.user.id
    user_id = 19
    user = User.objects.get(id=user_id)   # data of person who is searching i.e user
    user_mobile = user.username
    data1 = json.loads(request.body.decode('utf-8'))
    print(data1)
    mobile = data1.get('mobile')
    name = data1.get('name')
    print(mobile,name)
    email = None
    final_dict = {}
    spam = Spam.objects.filter(mobile=mobile)
    if spam:
        spam_count = spam[0].count
    else:
        spam_count = 0
    x = User.objects.filter(username = mobile)   # check if searched person is user or not
    print(x)
    if x:
        final_dict['name']=x[0].first_name
        final_dict['mobile']=x[0].username
        print(x[0].id,user_mobile)
        data = UserContacts.objects.filter(user_id=x[0].id , mobile=user_mobile)
        print(data)
        if data:
            final_dict['email']=x[0].email
        else:
            final_dict['email']=email
    else:
        data = UserContacts.objects.filter(mobile = mobile , name=name)[0]
        final_dict['name'] = data.name
        final_dict['mobile'] = data.mobile
        final_dict['email'] = email
    final_dict['spam_count'] = spam_count
    print(final_dict)
    
    token = encode_data(final_dict)
    print(token)
    return JsonResponse(token, status=200)
        

