from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
import datetime
from app.models import *


# LOGIN PAGE

def login(request):
    return render(request,'index.html')

def login_post(request):
    name=request.POST['uname']
    password=request.POST['pass']
    if name and password: 
        try:
            user = login_table.objects.get(username=name, password=password)
            request.session['lid'] = user.id
            
            if user.type == 'admin':
                return HttpResponse('''<script> alert ('Admin Logged In');window.location='/admin_home_page';</script>''')
            elif user.type == 'coordinator':
                return HttpResponse('''<script> alert ('Camp Coordinator Logged In');window.location='/coordinator_home_page';</script>''')
            elif user.type == 'ERT':
                return HttpResponse('''<script> alert ('Emergency Response Team Logged In');window.location='/emergency_response_team_home_page';</script>''')
        except login_table.DoesNotExist:
            return HttpResponse('''<script> alert ('Invalid username or password');window.location='/';</script>''')
    else:
        return HttpResponse('''<script> alert ('Please enter both username and password');window.location='/';</script>''')


def register_emergency_response_team(request):
    return render (request,'EMERGENCY RESPONSE TEAM REGISTRATION.html')


def register_emergency_response_team_post(request):
    department=request.POST["department"]
    district=request.POST["district"]
    place=request.POST["place"]
    post=request.POST["post"]
    pin = request.POST["pin"]
    contactno=request.POST["contactno"]
    email = request.POST["email"]
    username=request.POST["username"]
    password=request.POST["password"]
    ob=login_table()
    ob.username=username
    ob.password=password
    ob.type="Pending"
    ob.save()
    obj=emergency_team_table()
    obj.LOGIN=ob
    obj.department=department
    obj.district=district
    obj.place=place
    obj.post=post
    obj.pin=pin
    obj.ContactNo=contactno
    obj.email=email
    obj.save()
    return HttpResponse('''<script> alert ('EMERGENCY RESPONSE TEAM REGISTERED');window.location='/'</script>''')


def ert_registration_status(request):
    ob=emergency_team_table.objects.all()
    return render(request,'ERT REGISTRATION STATUS.html', {'val': ob})


def search_emergency_team_status(request):
    district = request.POST['textfield']
    ob = emergency_team_table.objects.filter(district__icontains=district)
    return render(request,'ERT REGISTRATION STATUS.html', {'val': ob})






# ***** ADMIN *****

def admin_home_page(request):
    return  render(request,'ADMIN/index.html')


# ADD & MANAGE CAMP

def admin_add_camp(request):
    return render (request,'ADMIN/ADD CAMP.html')


def admin_add_camp_post(request):
    camp=request.POST["camp"]
    place=request.POST["place"]
    pin=request.POST["pin"]
    post=request.POST["post"]
    district=request.POST["district"]
    contactno=request.POST["contactno"]
    email=request.POST["email"]
    obj=camp_table()
    obj.campName=camp
    obj.place=place
    obj.pin=pin
    obj.post=post
    obj.district=district
    obj.contactno=contactno
    obj.email=email
    obj.save()
    return HttpResponse('''<script> alert ('CAMP ADDED');window.location='/admin_manage_camp'</script>''')


def admin_manage_camp(request):
    ob=camp_table.objects.all()
    return render (request,'ADMIN/MANAGE CAMP.html',{'val':ob})


def admin_search_camp(request):
    campName=request.POST['textfield']
    ob=camp_table.objects.filter(campName__icontains=campName)
    return render (request,'ADMIN/MANAGE CAMP.html',{'val':ob})


def admin_edit_camp(request,id):
    request.session["campid"]=id
    ob=camp_table.objects.get(id=id)
    return render(request, 'ADMIN/EDIT CAMP.html',{"ob":ob})


def admin_edit_camp_post(request):
    camp=request.POST["camp"]
    place=request.POST["place"]
    pin=request.POST["pin"]
    post=request.POST["post"]
    district=request.POST["district"]
    contactno=request.POST["contactno"]
    email=request.POST["email"]
    obj = camp_table.objects.get(id=request.session["campid"])
    obj.campName=camp
    obj.place=place
    obj.pin=pin
    obj.post=post
    obj.district=district
    obj.contactno=contactno
    obj.email=email
    obj.save()
    return HttpResponse('''<script> alert('CAMP EDITED');window.location='/admin_manage_camp';</script>''')


def admin_delete_camp(request,id):
    camp_table.objects.get(id=id).delete()
    return HttpResponse('''<script> alert('CAMP DELETED');window.location='/admin_manage_camp';</script>''')






# ADD & MANAGE CAMP COORDINATOR

def admin_add_camp_coordinator(request):
    ob=camp_table.objects.all()
    return render(request,'ADMIN/ADD CAMP COORDINATOR.html',{"data":ob})


def admin_add_camp_coordinator_post(request):
    camp=request.POST["camp"]
    name=request.POST["name"]
    gender=request.POST["gender"]
    dob=request.POST["dob"]
    contactno = request.POST["contactNo"]
    email=request.POST["email"]
    district = request.POST["district"]
    place=request.POST["place"]
    post=request.POST["post"]
    pin=request.POST["pin"]
    username=request.POST["username"]
    password=request.POST["password"]
    fs=FileSystemStorage( )
    photo = request.FILES["photo"]
    fsave = fs.save(photo.name, photo)
    ob=login_table()
    ob.username=username
    ob.password=password
    ob.type="coordinator"
    ob.save()
    obj=camp_coordinator_table()
    obj.LOGIN=ob
    obj.CAMP_id=camp
    obj.name=name
    obj.gender=gender
    obj.dob=dob
    obj.contactNo=contactno
    obj.email=email
    obj.district=district
    obj.place=place
    obj.post=post
    obj.pin=pin
    obj.photo = fsave
    obj.save()
    return HttpResponse('''<script> alert ('CAMP COORDINATOR ADDED');window.location='/admin_manage_camp_coordinator'</script>''')


def admin_manage_camp_coordinator(request):
    ob=camp_coordinator_table.objects.all()
    return render (request,'ADMIN/MANAGE CAMP COORDINATOR.html',{'val':ob})


def admin_search_camp_coordinator(request):
    name = request.POST['textfield']
    ob = camp_coordinator_table.objects.filter(name__icontains=name)
    return render(request, 'ADMIN/MANAGE CAMP COORDINATOR.html', {'val': ob})


def admin_edit_camp_coordinator(request,id):
    request.session["coordinatorid"]=id
    ob=camp_coordinator_table.objects.get(id=id)
    cam=camp_table.objects.all()
    return render(request, 'ADMIN/EDIT CAMP COORDINATOR.html', {"ob": ob,"camp":cam})


def admin_edit_camp_coordinator_post(request):
    camp=request.POST["camp"]
    name=request.POST["name"]
    gender=request.POST["gender"]
    dob=request.POST["dob"]
    contactno = request.POST["contactNo"]
    email=request.POST["email"]
    district = request.POST["district"]
    place=request.POST["place"]
    post=request.POST["post"]
    pin=request.POST["pin"]
    obj = camp_coordinator_table.objects.get(id=request.session["coordinatorid"])
    obj.CAMP_id = camp
    obj.name=name
    obj.gender=gender
    obj.dob=dob
    obj.contactNo=contactno
    obj.email=email
    obj.district=district
    obj.place=place
    obj.post=post
    obj.pin=pin
    obj.save()
    return HttpResponse('''<script> alert ('CAMP COORDINATOR EDITED');window.location='/admin_manage_camp_coordinator'</script>''')


def admin_delete_camp_coordinator(request,id):
    login_table.objects.get(id=id).delete()
    return HttpResponse('''<script> alert ('CAMP COORDINATOR DELETED');window.location='/admin_manage_camp_coordinator'</script>''')






# ADD & MANAGE GUIDELINES

def admin_add_guideline(request):
    ob = camp_coordinator_table.objects.all()
    return render (request,'ADMIN/ADD GUIDELINE.html',{"data":ob})


def admin_add_guideline_post(request):
    camp=request.POST["camp"]
    guideline=request.FILES["guideline"]
    fs=FileSystemStorage( )
    fsave=fs.save(guideline.name,guideline)
    obj=Guidelines_table()
    obj.CAMP_COORDINATOR=camp_coordinator_table.objects.get(id=camp)
    obj.guideline=fsave
    obj.date=datetime.datetime.now().date()
    obj.time=datetime.datetime.now().time()
    obj.save()
    return HttpResponse('''<script> alert ('GUIDELINE ADDED');window.location='/admin_manage_guideline'</script>''')


def admin_manage_guideline(request):
    ob = Guidelines_table.objects.all()
    return render (request,'ADMIN\MANAGE GUIDELINE.html',{"val":ob})


def admin_delete_guideline(request,id):
    Guidelines_table.objects.get(id=id).delete()
    return HttpResponse('''<script> alert('GUIDELINE DELETED');window.location='/admin_manage_guideline';</script>''')


def admin_search_guideline(request):
    name = request.POST['textfield']
    ob = Guidelines_table.objects.filter(CAMP_COORDINATOR__name__icontains=name)
    return render(request, 'ADMIN/MANAGE GUIDELINE.html', {'val': ob})



# VERIFY EMERGENCY TEAM

def admin_verify_emergency_team(request):
    ob=emergency_team_table.objects.filter(LOGIN__type='Pending')
    return render(request, 'ADMIN/VERIFY EMERGENCY TEAM.html', {'val': ob})


def admin_manage_emergency_team(request):
    ob1=emergency_team_table.objects.filter(LOGIN__type='ert')
    ob2=emergency_team_table.objects.filter(LOGIN__type='reject')
    return render(request, 'ADMIN/MANAGE EMERGENCY TEAM.html', {'val1': ob1 ,'val2':ob2})


def admin_search_verify_emergency_team(request):
    district = request.POST['textfield']
    ob = emergency_team_table.objects.filter(district__icontains=district,LOGIN__type='pending')
    return render(request, 'ADMIN/VERIFY EMERGENCY TEAM.html', {'val': ob})


def admin_search_accept_emergency_team(request):
    district = request.POST['textfield']
    ob = emergency_team_table.objects.filter(district__icontains=district,LOGIN__type='ert')
    return render(request, 'ADMIN/MANAGE EMERGENCY TEAM.html', {'val1': ob})


def admin_search_reject_emergency_team(request):
    district = request.POST['textfield']
    ob = emergency_team_table.objects.filter(district__icontains=district,LOGIN__type='reject')
    return render(request, 'ADMIN/MANAGE EMERGENCY TEAM.html', {'val2': ob})


def admin_accept_ERT(request,id):
    request.session["ERTid"]=id
    ob=login_table.objects.get(id=id)
    ob.type="ERT"
    ob.save()
    return HttpResponse('''<script> alert ('ACCEPTED');window.location='/admin_manage_emergency_team'</script>''')


def admin_reject_ERT(request,id):
    request.session["ERTid"]=id
    ob=login_table.objects.get(id=id)
    ob.type="Reject"
    ob.save()
    return HttpResponse('''<script> alert ('REJECTED');window.location='/admin_manage_emergency_team'</script>''')


# MANAGE COMPLAINT

def admin_manage_camplaint(request):
    ob=complaint_table.objects.all()
    return render (request,'ADMIN/VIEW COMPLAINT.html',{'val':ob})


def admin_reply_complaint(request,id):
    request.session["complaintid"]=id
    ob=complaint_table.objects.get(id=id)
    return render(request, 'ADMIN/REPLY COMPLAINT.html',{"ob":ob})


def admin_reply_complaint_post(request):
    status=request.POST["status"]
    reply=request.POST["reply"]
    obj = complaint_table.objects.get(id=request.session["complaintid"])
    obj.status=status
    obj.reply=reply
    obj.save()
    return HttpResponse('''<script> alert('COMPLAINT REPLIED');window.location='/admin_manage_camplaint';</script>''')


def search_complaint(request):
    status = request.POST['select'] 
    ob = complaint_table.objects.filter(status__icontains=status)
    return render(request, 'ADMIN/VIEW COMPLAINT.html', {'val': ob})




# MANAGE NOTIFICATION

def admin_add_notification(request):
    return render (request,'ADMIN/ADD NOTIFICATION.html')


def admin_add_notification_post(request):
   title=request.POST["title"]
   subject=request.POST["subject"]
   obj=notification_table()
   obj.title=title
   obj.subject=subject
   obj.date = datetime.datetime.now().date()
   obj.time = datetime.datetime.now().time()
   obj.save()
   return HttpResponse('''<script> alert ('NOTIFICATION ADDED');window.location='/admin_manage_notification'</script>''')


def admin_manage_notification(request):
    ob=notification_table.objects.all()
    return render (request,'ADMIN/MANAGE NOTIFICATION.html', {"val": ob})


def admin_delete_notification(request,id):
    notification_table.objects.get(id=id).delete()
    return HttpResponse('''<script> alert('NOTIFICATION DELETED');window.location='/admin_manage_notification';</script>''')


def admin_edit_notification(request,id):
    request.session["notificationid"]=id
    ob=notification_table.objects.get(id=id)
    return render(request, 'ADMIN/EDIT NOTIFICATION.html',{"ob":ob})


def admin_edit_notification_post(request):
    title=request.POST["title"]
    subject=request.POST["subject"]
    obj = notification_table.objects.get(id=request.session["notificationid"])
    obj.title=title
    obj.subject=subject
    obj.date = datetime.datetime.now().date()
    obj.time = datetime.datetime.now().time()
    obj.save()
    return HttpResponse('''<script> alert('NOTIFICATION EDITED');window.location='/admin_manage_notification';</script>''')


def admin_search_notification(request):
    fdate = request.POST['textfield1']
    tdate = request.POST['textfield2']
    ob = notification_table.objects.filter(date__range=(fdate, tdate))
    return render(request, 'ADMIN/MANAGE NOTIFICATION.html', {'val': ob})






# ***** CAMP COORDINATOR *****

def coordinator_home_page(request):
    return  render(request,'CAMP COORDINATOR/HOME PAGE.html')


# ADD & MANAGE STOCK

def coordinator_add_stock(request):
    return render(request, 'CAMP COORDINATOR/ADD STOCK.html')


def coordinator_add_stock_post(request):
    category = request.POST["category"]
    product = request.POST["product"]
    quantity = request.POST["quantity"]
    date = request.POST["date"]
    obj = stock_table()
    obj.category= category
    obj.product=product
    obj.quantity=quantity
    obj.date=date
    obj.save()
    return HttpResponse('''<script> alert ('STOCK ADDED');window.location='/coordinator_manage_stock'</script>''')


def coordinator_manage_stock(request):
    ob = stock_table.objects.all()
    return render(request, 'CAMP COORDINATOR/MANAGE STOCK.html', {"val": ob})


def coordinator_edit_stock(request,id):
    request.session["stockid"]=id
    ob=stock_table.objects.get(id=id)
    return render(request, 'CAMP COORDINATOR/EDIT STOCK.html',{"ob":ob})


def coordinator_edit_stock_post(request):
    category = request.POST["category"]
    product = request.POST["product"]
    quantity = request.POST["quantity"]
    date = request.POST["date"]
    obj = stock_table.objects.get(id=request.session["stockid"])
    obj.category= category
    obj.product=product
    obj.quantity=quantity
    obj.date=date
    obj.save()
    return HttpResponse('''<script> alert ('STOCK EDITED');window.location='/coordinator_manage_stock'</script>''')


def coordinator_delete_stock(request,id):
    stock_table.objects.get(id=id).delete()
    return HttpResponse('''<script> alert('STOCK DELETED');window.location='/coordinator_manage_stock';</script>''')


def coordinator_search_stock(request):
    category = request.POST['select']
    ob = stock_table.objects.filter(category__icontains=category)
    return render(request, 'CAMP COORDINATOR/MANAGE STOCK.html', {"val": ob})
    





# ADD & MANAGE MEMBER

def coordinator_add_member(request):
    return render (request,'CAMP COORDINATOR/ADD MEMBER.html')


def coordinator_add_member_post(request):
    name = request.POST["name"]
    gender = request.POST["gender"]
    dob = request.POST["dob"]
    district = request.POST["district"]
    place = request.POST["place"]
    post = request.POST["post"]
    pin = request.POST["pin"]
    contactNo = request.POST["contactNo"]
    email = request.POST["email"]
    photo = request.FILES["photo"]
    fs=FileSystemStorage( )
    fsave=fs.save(photo.name,photo)
    obj=member_table()
    obj.name = name
    obj.gender = gender
    obj.dob = dob
    obj.district = district
    obj.place = place
    obj.post = post
    obj.pin = pin
    obj.contactNo = contactNo
    obj.email = email
    obj.photo = fsave
    obj.COORDINATOR = camp_coordinator_table.objects.get(LOGIN__id=request.session['lid'])
    obj.save()
    return HttpResponse('''<script> alert ('MEMBER ADDED');window.location='/coordinator_manage_members'</script>''')


def coordinator_manage_members(request):
    ob = member_table.objects.all()
    return render (request,'CAMP COORDINATOR/MANAGE MEMBERS.html', {"val": ob})


def coordinator_delete_member(request,id):
    member_table.objects.get(id=id).delete()
    return HttpResponse('''<script> alert ('MEMBER DELETED');window.location='/coordinator_manage_members'</script>''')


def coordinator_edit_member(request,id):
    request.session["memberid"]=id
    ob=member_table.objects.get(id=id)
    return render(request,'CAMP COORDINATOR/EDIT MEMBER.html',{"ob":ob})


def coordinator_edit_member_post(request):
    name = request.POST["name"]
    gender = request.POST["gender"]
    dob = request.POST["dob"]
    district = request.POST["district"]
    place = request.POST["place"]
    post = request.POST["post"]
    pin = request.POST["pin"]
    contactNo = request.POST["contactNo"]
    email = request.POST["email"]
    obj = member_table.objects.get(id=request.session["memberid"])
    obj.name = name
    obj.gender = gender
    obj.dob = dob
    obj.district = district
    obj.place = place
    obj.post = post
    obj.pin = pin
    obj.contactNo = contactNo
    obj.email = email
    obj.save()
    return HttpResponse('''<script> alert ('MEMBER EDITED');window.location='/coordinator_manage_members'</script>''')


def coordinator_search_member(request):
    name=request.POST['name']
    ob=member_table.objects.filter(name__icontains=name)
    return render (request,'CAMP COORDINATOR/MANAGE MEMBERS.html',{'val':ob})




# MISSING ASSET

def coordinator_register_missing_asset(request):
    names=member_table.objects.filter(COORDINATOR__LOGIN_id=request.session['lid'])
    return render(request,'CAMP COORDINATOR/REGISTER MISSING ASSET.html',{'names':names})


def coordinator_register_missing_asset_post(request):
    membername = request.POST["membername"]
    category = request.POST["category"]
    assetname = request.POST["assetname"]
    assetdescription = request.POST["assetdescription"]
    date = request.POST["date"]
    status = 'pending'
    obj = asset_table()
    obj.MEMBER_id = membername
    obj.category = category
    obj.asset = assetname
    obj.description = assetdescription
    obj.date =date
    obj.status=status
    obj.save()
    return HttpResponse('''<script> alert (' MISSING ASSET REGISTERED');window.location='/coordinator_view_missing_asset_registration'</script>''')


def coordinator_view_missing_asset_registration(request):
    ob = asset_table.objects.all()
    return render(request, 'CAMP COORDINATOR/VIEW ASSET REGISTRATION.html', {'val': ob})


def coordinator_delete_asset_registration(request,id):
    asset_table.objects.get(id=id).delete()
    return HttpResponse('''<script> alert('ASSET REGISTRATION DELETED');window.location='/coordinator_view_missing_asset_registration';</script>''')


def coordinator_edit_asset_registration(request,id):
    request.session["assetid"] = id
    ob = asset_table.objects.get(id=id)
    return render(request, 'CAMP COORDINATOR/EDIT ASSET REGISTRATION.html', {"ob": ob})


def coordinator_edit_asset_registration_post(request):
    category = request.POST["category"]
    asset = request.POST["asset"]
    description = request.POST["description"]
    date = request.POST["date"]
    obj = asset_table.objects.get(id=request.session["assetid"])
    obj.category = category
    obj.asset = asset
    obj.description = description
    obj.date = date
    obj.save()
    return HttpResponse('''<script> alert('ASSET REGISTRATION EDITED');window.location='/coordinator_view_missing_asset_registration';</script>''')


def coordinator_search_asset_registration(request):
    name=request.POST['textfield']
    ob=asset_table.objects.filter(MEMBER__name__icontains=name)
    return render (request,'CAMP COORDINATOR/VIEW ASSET REGISTRATION.html', {'val': ob})



# ADD AND MANAGE NEEDS

def coordinator_add_needs(request):
    ob=camp_coordinator_table.objects.get(LOGIN=request.session["lid"])
    return render(request, 'CAMP COORDINATOR/ADD NEEDS.html',{"ob":ob})


def coordinator_add_needs_post(request):
    category = request.POST["category"]
    product = request.POST["product"]
    quantity = request.POST["quantity"]
    obj = needs_table()
    obj.COORDINATOR = camp_coordinator_table.objects.get(LOGIN=request.session["lid"])
    obj.category = category
    obj.product = product
    obj.quantity = quantity
    obj.date = datetime.datetime.now().date()
    obj.save()
    return HttpResponse( '''<script> alert('NEED ADDED');window.location='/coordinator_view_needs';</script>''')


def coordinator_view_needs(request):
    ob = needs_table.objects.all()
    return render(request, 'CAMP COORDINATOR/VIEW NEEDS.html', {"val": ob})


def coordinator_edit_needs(request,id):
    request.session["needsid"] = id
    ob = needs_table.objects.get(id=id)
    return render(request, 'CAMP COORDINATOR/EDIT NEEDS.html', {"ob": ob})


def coordinator_edit_needs_post(request):
    category = request.POST["category"]
    product = request.POST["product"]
    quantity = request.POST["quantity"]
    obj = needs_table.objects.get(id=request.session["needsid"])
    obj.category = category
    obj.product = product
    obj.quantity = quantity
    obj.date = datetime.datetime.now().date()
    obj.save()
    return HttpResponse('''<script> alert('NEEDS EDITED');window.location='/coordinator_view_needs';</script>''')


def coordinator_delete_needs(request,id):
    needs_table.objects.get(id=id).delete()
    return HttpResponse('''<script> alert('NEED DELETED');window.location='/coordinator_view_needs';</script>''')


def coordinator_search_needs(request):
    category = request.POST['select']
    ob = needs_table.objects.filter(category__icontains=category)
    return render(request, 'CAMP COORDINATOR/VIEW NEEDS.html', {"val": ob})



# MEDICAL SUPPORT REQUEST


def coordinator_manage_medical_request(request):
    ob = medical_request_table.objects.all()
    return render (request,'CAMP COORDINATOR/MANAGE MEDICAL REQUEST.html', {"val": ob})


def coordinator_search_medical_request(request):
    status = request.POST['status']
    ob = medical_request_table.objects.filter(status__icontains=status)
    return render(request, 'CAMP COORDINATOR/MANAGE MEDICAL REQUEST.html', {"val": ob})


def coordinator_edit_medical_request_status(request,id):
    request.session["medicalrequestid"] = id
    ob = medical_request_table.objects.get(id=id)
    return render(request, 'CAMP COORDINATOR/EDIT MEDICAL REQUEST STATUS.html', {"ob": ob})


def coordinator_edit_medical_request_status_post(request):
    status = request.POST["status"]
    obj = medical_request_table.objects.get(id=request.session["medicalrequestid"])
    obj.status = status
    obj.save()
    return HttpResponse('''<script> alert('STATUS UPDATED');window.location='/coordinator_manage_medical_request';</script>''')



# ADD AND MANAGE VOLUNTEER

def coordinator_volunteer_registration(request):
    return render(request,'CAMP COORDINATOR/REGISTER VOLUNTEER.html')


def coordinator_volunteer_registration_post(request):
    coid=camp_coordinator_table.objects.get(LOGIN=request.session['lid'])
    name=request.POST["name"]
    gender=request.POST["gender"]
    dob=request.POST["dob"]
    contactno = request.POST["contactNo"]
    email=request.POST["email"]
    district = request.POST["district"]
    place=request.POST["place"]
    post=request.POST["post"]
    pin=request.POST["pin"]
    username=request.POST["username"]
    password=request.POST["password"]
    fs=FileSystemStorage( )
    photo = request.FILES["photo"]
    fsave = fs.save(photo.name, photo)
    ob=login_table()
    ob.username=username
    ob.password=password
    ob.type="volunteer"
    ob.save()
    obj=volunteer_table()
    obj.LOGIN=ob
    obj.name=name
    obj.gender=gender
    obj.dob=dob
    obj.contactNo=contactno
    obj.email=email
    obj.district=district
    obj.place=place
    obj.post=post
    obj.pin=pin
    obj.photo = fsave
    obj.COORDINATOR=coid
    obj.save()
    return HttpResponse('''<script> alert ('VOLUNTEER ADDED');window.location='/coordinator_manage_volunteer'</script>''')


def coordinator_manage_volunteer(request):
    ob = volunteer_table.objects.all()
    return render (request,'CAMP COORDINATOR/MANAGE VOLUNTEER.html', {"val": ob})


def coordinator_search_volunteer(request):
    name = request.POST['name']
    ob = volunteer_table.objects.filter(name__icontains=name)
    return render(request, 'CAMP COORDINATOR/MANAGE VOLUNTEER.html', {"val": ob})


def coordinator_edit_volunteer(request,id):
    request.session["volunteerid"] = id
    ob = volunteer_table.objects.get(id=id)
    return render(request, 'CAMP COORDINATOR/EDIT VOLUNTEER.html', {"ob": ob})


def coordinator_edit_volunteer_post(request):
    name=request.POST["name"]
    gender=request.POST["gender"]
    dob=request.POST["dob"]
    contactno = request.POST["contactNo"]
    email=request.POST["email"]
    district = request.POST["district"]
    place=request.POST["place"]
    post=request.POST["post"]
    pin=request.POST["pin"]
    obj = volunteer_table.objects.get(id=request.session["volunteerid"])
    obj.name=name
    obj.gender=gender
    obj.dob=dob
    obj.contactNo=contactno
    obj.email=email
    obj.district=district
    obj.place=place
    obj.post=post
    obj.pin=pin
    obj.save()
    return HttpResponse('''<script> alert('VOLUNTEER EDITED');window.location='/coordinator_manage_volunteer';</script>''')

def coordinator_delete_volunteer(request,id):
    volunteer_table.objects.get(id=id).delete()
    return HttpResponse('''<script> alert('VOLUNTEER DELETED');window.location='/coordinator_manage_volunteer';</script>''')






# ***** EMERGENCY RESPONCE TEAM *****

# MANAGE EMERGENCY RESPONSE

def emergency_response_team_home_page(request):
    return render (request,'EMERGENCY RESPONSE TEAM/ERT HOME PAGE.html')


def emergency_response_tean_view_emergency_request(request):
    ob = emergency_request_table.objects.all()
    return render (request,'EMERGENCY RESPONSE TEAM/VIEW EMERGENCY REQUEST.html', {"val": ob})


def emergency_response_team_search_emergency_request(request):
    status = request.POST['status']
    ob = emergency_request_table.objects.filter(status__icontains=status)
    return render(request, 'EMERGENCY RESPONSE TEAM/VIEW EMERGENCY REQUEST.html', {"val": ob})


def emergency_response_edit_emergency_request_status(request,id):
    request.session["emergencyrequestid"] = id
    ob = emergency_request_table.objects.get(id=id)
    return render(request, 'EMERGENCY RESPONSE TEAM/EDIT EMERGENCY REQUEST STATUS.html', {"ob": ob})


def emergency_response_edit_emergency_request_status_post(request):
    status = request.POST["status"]
    obj = emergency_request_table.objects.get(id=request.session["emergencyrequestid"])
    obj.status = status
    obj.save()
    return HttpResponse('''<script> alert('STATUS UPDATED');window.location='/emergency_response_tean_view_emergency_request';</script>''')
