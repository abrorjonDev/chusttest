from datetime import datetime
from django.shortcuts import get_object_or_404
import pandas as pd
import numpy as np
from django.contrib.auth import get_user_model

from celery import shared_task

from users.models import UserFileModel

User = get_user_model()
@shared_task
def summa(a, b):

    return a + b

def names(full_name):
    first_name = None
    last_name = None
    father_name = None
    name = full_name.split(" ")
    if len(name)>3:
        first_name = name[1]
        last_name = name[0]
        father_name = name[2]+ ' '+ name[3] 
    elif len(name)==3:
        first_name = name[1]
        last_name = name[0]
        father_name = name[2]
    else:
        first_name = name[1]
        last_name = name[0]
    return first_name, last_name, father_name

@shared_task
def create_students(id, created_by=None):
    data = pd.read_excel(get_object_or_404(UserFileModel, id=id).file).to_numpy()
    users = User.objects.all()
    created_by = get_object_or_404(User, id=created_by)
    created_users = []
    modified_users = []
    users = User.objects.all()
    for dt in data:
        print(dt[0])
        username =dt[4] #ID
        last_name = dt[1]
        first_name = dt[2]
        parent_name = dt[3]
        # full_name = names(dt[1]) #full_name
        school = dt[6]
        klass = dt[7]
        try:
           user = User(
                username=username, 
                first_name=first_name, 
                last_name=last_name,
                father_name=parent_name,
                school=school,
                klass=klass
                )
           user.set_password("1")
           user.save()
            # if user not in modified_users and user not in created_users:
           created_users.append(user) 
        except Exception as e:
           user = User.objects.get(username=username)
           if user.first_name != first_name:
               user.first_name = first_name
           if user.last_name != last_name:
               user.last_name = last_name
           if user.father_name != parent_name:
               user.father_name = parent_name
           if user.school != school:
               user.school = school
           if user.klass != klass:
               user.klass = klass
           user.set_password("1")
           if user not in modified_users or user not in created_users:
               modified_users.append(user)
           user.save() 
#if exception, it means that the user must be created
        #except:
#            user = User(
#                username=username, 
#                first_name=first_name, 
#                last_name=last_name,
#                father_name=parent_name,
#                school=school,
#                klass=klass
#                )
#            user.set_password("1")
#            user.save()
            # if user not in modified_users and user not in created_users:
#            created_users.append(user)
        
    # bulk_create and bulk_update only create, modify objects till 1600
    #start_index = 0
    #end_index = 1600
    #print("created users length(): ", len(created_users))
    #for i in range(len(created_users)//1600):
        #User.objects.bulk_create(created_users[start_index:end_index], ignore_conflicts=True)
        #print("Bulk_create : ", start_index, end_index)
        #start_index = end_index
        #end_index = end_index + 1600
        #if end_index > len(created_users):
        #    end_index = len(created_users)

    #print("modified users length(): ", len(modified_users))
    #for i in range(len(created_users)//1600):
     #   User.objects.bulk_update(modified_users[start_index:end_index], ['first_name','last_name','father_name', 'school', 'klass'])
     #   print("Bulk update:   ", start_index, end_index)
     #   start_index = end_index
     #   end_index = end_index + 1600
     #   if end_index > len(modified_users):
     #       end_index = len(modified_users)
    return #{
        #'created':len(created_users),
        #'modified': len(modified_users)
        #}
