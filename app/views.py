from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from app.models import *
from django.contrib.auth.models import User

# LOGIN PAGE

def login(request):
    return render(request, 'index.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def login_post(request):
    if request.method == "POST":
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        if username and password:
            try:
                user = login_table.objects.get(username=username, password=password)
                if user.type == 'admin':
                    auth.login(request, User.objects.get(username='admin'))
                    request.session['lid'] = user.id
                    return HttpResponse(
                        '''<script>alert('Admin Logged In');window.location='/admin_home_page';</script>'''
                    )
                elif user.type == 'coordinator':
                    auth.login(request, User.objects.get(username='admin'))
                    request.session['lid'] = user.id
                    return HttpResponse(
                        '''<script>alert('Camp Coordinator Logged In');window.location='/coordinator_home_page';</script>'''
                    )
                elif user.type == 'ERT':
                    auth.login(request, User.objects.get(username='admin'))
                    request.session['lid'] = user.id
                    return HttpResponse(
                        '''<script>alert('Emergency Response Team Logged In');window.location='/emergency_response_team_home_page';</script>'''
                    )
                else:
                    return HttpResponse(
                        '''<script>alert('User type not authorized.');window.location='/';</script>'''
                    )
            except login_table.DoesNotExist:
                return HttpResponse(
                    '''<script>alert('Invalid username or password.');window.location='/';</script>'''
                )
        return HttpResponse(
            '''<script>alert('Please enter both username and password.');window.location='/';</script>'''
        )
    return redirect('/')


# EMERGENCY RESPONSE TEAM REGISTRATION

def register_emergency_response_team(request):
    return render(request, 'EMERGENCY RESPONSE TEAM REGISTRATION.html')

def register_emergency_response_team_post(request):
    if request.method == "POST":
        department = request.POST.get("department")
        district = request.POST.get("district")
        place = request.POST.get("place")
        post = request.POST.get("post")
        pin = request.POST.get("pin")
        contactno = request.POST.get("contactno")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Create login instance
        login_instance = login_table(username=username, password=password, type="Pending")
        login_instance.save()

        # Create emergency team instance
        emergency_team = emergency_team_table(
            LOGIN=login_instance,
            department=department,
            district=district,
            place=place,
            post=post,
            pin=pin,
            ContactNo=contactno,
            email=email
        )
        emergency_team.save()
        
        return HttpResponse(
            '''<script>alert('Emergency Response Team Registered');window.location='/';</script>'''
        )
    return redirect('/')


def ert_registration_status(request):
    teams = emergency_team_table.objects.all()
    return render(request, 'ERT REGISTRATION STATUS.html', {'val': teams})

def search_emergency_team_status(request):
    if request.method == "POST":
        district = request.POST.get('textfield', '')
        teams = emergency_team_table.objects.filter(district__icontains=district)
        return render(request, 'ERT REGISTRATION STATUS.html', {'val': teams})
    return redirect('/ert_registration_status')


# ADMIN DASHBOARD

@login_required(login_url='/')
def admin_home_page(request):
    user_id = request.session.get('lid')
    logged_in_user = login_table.objects.get(id=user_id).username
    context = {
        'total_camp': camp_table.objects.count(),
        'total_coordinator': camp_coordinator_table.objects.count(),
        'total_ert': login_table.objects.filter(type='ERT').count(),
        'total_user': public_table.objects.count(),
        'total_volunteer': volunteer_table.objects.count(),
        'total_member': member_table.objects.count(),
        'logged_in_user': logged_in_user,
    }
    return render(request, 'ADMIN/index.html', context)


# CAMP MANAGEMENT

@login_required(login_url='/')
def admin_add_camp(request):
    return render(request, 'ADMIN/ADD CAMP.html')

@login_required(login_url='/')
def admin_add_camp_post(request):
    if request.method == "POST":
        camp = request.POST.get("camp")
        place = request.POST.get("place")
        pin = request.POST.get("pin")
        post = request.POST.get("post")
        district = request.POST.get("district")
        contactno = request.POST.get("contactno")
        email = request.POST.get("email")

        camp_instance = camp_table(
            campName=camp, place=place, pin=pin, post=post, district=district, contactno=contactno, email=email
        )
        camp_instance.save()

        return HttpResponse(
            '''<script>alert('Camp Added');window.location='/admin_manage_camp';</script>'''
        )
    return redirect('/admin_add_camp')

@login_required(login_url='/')
def admin_manage_camp(request):
    camps = camp_table.objects.all()
    return render(request, 'ADMIN/MANAGE CAMP.html', {'val': camps})

@login_required(login_url='/')
def admin_search_camp(request):
    if request.method == "POST":
        campName = request.POST.get('textfield', '')
        camps = camp_table.objects.filter(campName__icontains=campName)
        return render(request, 'ADMIN/MANAGE CAMP.html', {'val': camps})
    return redirect('/admin_manage_camp')

@login_required(login_url='/')
def admin_edit_camp(request, id):
    camp = get_object_or_404(camp_table, id=id)
    return render(request, 'ADMIN/EDIT CAMP.html', {"ob": camp})

@login_required(login_url='/')
def admin_edit_camp_post(request):
    if request.method == "POST":
        camp_id = request.session.get("campid")
        camp = get_object_or_404(camp_table, id=camp_id)
        
        camp.campName = request.POST.get("camp")
        camp.place = request.POST.get("place")
        camp.pin = request.POST.get("pin")
        camp.post = request.POST.get("post")
        camp.district = request.POST.get("district")
        camp.contactno = request.POST.get("contactno")
        camp.email = request.POST.get("email")
        camp.save()

        return HttpResponse(
            '''<script>alert('Camp Edited');window.location='/admin_manage_camp';</script>'''
        )
    return redirect('/admin_manage_camp')

@login_required(login_url='/')
def admin_delete_camp(request, id):
    camp = get_object_or_404(camp_table, id=id)
    camp.delete()
    return HttpResponse(
        '''<script>alert('Camp Deleted');window.location='/admin_manage_camp';</script>'''
    )





# ADD & MANAGE CAMP COORDINATOR
@login_required(login_url='/')
def admin_add_camp_coordinator(request):
    ob=camp_table.objects.all()
    return render(request,'ADMIN/ADD CAMP COORDINATOR.html',{"data":ob})

@login_required(login_url='/')
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

@login_required(login_url='/')
def admin_manage_camp_coordinator(request):
    ob=camp_coordinator_table.objects.all()
    return render (request,'ADMIN/MANAGE CAMP COORDINATOR.html',{'val':ob})

@login_required(login_url='/')
def admin_search_camp_coordinator(request):
    name = request.POST['textfield']
    ob = camp_coordinator_table.objects.filter(name__icontains=name)
    return render(request, 'ADMIN/MANAGE CAMP COORDINATOR.html', {'val': ob})

@login_required(login_url='/')
def admin_edit_camp_coordinator(request,id):
    request.session["coordinatorid"]=id
    ob=camp_coordinator_table.objects.get(id=id)
    cam=camp_table.objects.all()
    return render(request, 'ADMIN/EDIT CAMP COORDINATOR.html', {"ob": ob,"camp":cam})

@login_required(login_url='/')
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

@login_required(login_url='/')
def admin_delete_camp_coordinator(request,id):
    login_table.objects.get(id=id).delete()
    return HttpResponse('''<script> alert ('CAMP COORDINATOR DELETED');window.location='/admin_manage_camp_coordinator'</script>''')






# ADD & MANAGE GUIDELINES
@login_required(login_url='/')
def admin_add_guideline(request):
    ob = camp_coordinator_table.objects.all()
    return render (request,'ADMIN/ADD GUIDELINE.html',{"data":ob})

@login_required(login_url='/')
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

@login_required(login_url='/')
def admin_manage_guideline(request):
    ob = Guidelines_table.objects.all()
    return render (request,'ADMIN\MANAGE GUIDELINE.html',{"val":ob})

@login_required(login_url='/')
def admin_delete_guideline(request,id):
    Guidelines_table.objects.get(id=id).delete()
    return HttpResponse('''<script> alert('GUIDELINE DELETED');window.location='/admin_manage_guideline';</script>''')

@login_required(login_url='/')
def admin_search_guideline(request):
    name = request.POST['textfield']
    ob = Guidelines_table.objects.filter(CAMP_COORDINATOR__name__icontains=name)
    return render(request, 'ADMIN/MANAGE GUIDELINE.html', {'val': ob})



# VERIFY EMERGENCY TEAM
@login_required(login_url='/')
def admin_verify_emergency_team(request):
    ob=emergency_team_table.objects.filter(LOGIN__type='Pending')
    return render(request, 'ADMIN/VERIFY EMERGENCY TEAM.html', {'val': ob})

@login_required(login_url='/')
def admin_manage_emergency_team(request):
    ob1=emergency_team_table.objects.filter(LOGIN__type='ert')
    ob2=emergency_team_table.objects.filter(LOGIN__type='reject')
    return render(request, 'ADMIN/MANAGE EMERGENCY TEAM.html', {'val1': ob1 ,'val2':ob2})

@login_required(login_url='/')
def admin_search_verify_emergency_team(request):
    district = request.POST['textfield']
    ob = emergency_team_table.objects.filter(district__icontains=district,LOGIN__type='pending')
    return render(request, 'ADMIN/VERIFY EMERGENCY TEAM.html', {'val': ob})

@login_required(login_url='/')
def admin_search_accept_emergency_team(request):
    district = request.POST['textfield']
    ob = emergency_team_table.objects.filter(district__icontains=district,LOGIN__type='ert')
    return render(request, 'ADMIN/MANAGE EMERGENCY TEAM.html', {'val1': ob})

@login_required(login_url='/')
def admin_search_reject_emergency_team(request):
    district = request.POST['textfield']
    ob = emergency_team_table.objects.filter(district__icontains=district,LOGIN__type='reject')
    return render(request, 'ADMIN/MANAGE EMERGENCY TEAM.html', {'val2': ob})

@login_required(login_url='/')
def admin_accept_ERT(request,id):
    request.session["ERTid"]=id
    ob=login_table.objects.get(id=id)
    ob.type="ERT"
    ob.save()
    return HttpResponse('''<script> alert ('ACCEPTED');window.location='/admin_manage_emergency_team'</script>''')

@login_required(login_url='/')
def admin_reject_ERT(request,id):
    request.session["ERTid"]=id
    ob=login_table.objects.get(id=id)
    ob.type="Reject"
    ob.save()
    return HttpResponse('''<script> alert ('REJECTED');window.location='/admin_manage_emergency_team'</script>''')


# MANAGE COMPLAINT
@login_required(login_url='/')
def admin_manage_camplaint(request):
    ob=complaint_table.objects.all()
    return render (request,'ADMIN/VIEW COMPLAINT.html',{'val':ob})

@login_required(login_url='/')
def admin_reply_complaint(request,id):
    request.session["complaintid"]=id
    ob=complaint_table.objects.get(id=id)
    return render(request, 'ADMIN/REPLY COMPLAINT.html',{"ob":ob})

@login_required(login_url='/')
def admin_reply_complaint_post(request):
    status=request.POST["status"]
    reply=request.POST["reply"]
    obj = complaint_table.objects.get(id=request.session["complaintid"])
    obj.status=status
    obj.reply=reply
    obj.save()
    return HttpResponse('''<script> alert('COMPLAINT REPLIED');window.location='/admin_manage_camplaint';</script>''')

@login_required(login_url='/')
def search_complaint(request):
    status = request.POST['select'] 
    ob = complaint_table.objects.filter(status__icontains=status)
    return render(request, 'ADMIN/VIEW COMPLAINT.html', {'val': ob})




# MANAGE NOTIFICATION
@login_required(login_url='/')
def admin_add_notification(request):
    return render (request,'ADMIN/ADD NOTIFICATION.html')

@login_required(login_url='/')
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

@login_required(login_url='/')
def admin_manage_notification(request):
    ob=notification_table.objects.all()
    return render (request,'ADMIN/MANAGE NOTIFICATION.html', {"val": ob})

@login_required(login_url='/')
def admin_delete_notification(request,id):
    notification_table.objects.get(id=id).delete()
    return HttpResponse('''<script> alert('NOTIFICATION DELETED');window.location='/admin_manage_notification';</script>''')

@login_required(login_url='/')
def admin_edit_notification(request,id):
    request.session["notificationid"]=id
    ob=notification_table.objects.get(id=id)
    return render(request, 'ADMIN/EDIT NOTIFICATION.html',{"ob":ob})

@login_required(login_url='/')
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

@login_required(login_url='/')
def admin_search_notification(request):
    fdate = request.POST['textfield1']
    tdate = request.POST['textfield2']
    ob = notification_table.objects.filter(date__range=(fdate, tdate))
    return render(request, 'ADMIN/MANAGE NOTIFICATION.html', {'val': ob})






# ***** CAMP COORDINATOR *****
@login_required(login_url='/')
def coordinator_home_page(request):
    return  render(request,'CAMP COORDINATOR/index.html')


# ADD & MANAGE STOCK
@login_required(login_url='/')
def coordinator_add_stock(request):
    return render(request, 'CAMP COORDINATOR/ADD STOCK.html')

@login_required(login_url='/')
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

@login_required(login_url='/')
def coordinator_manage_stock(request):
    ob = stock_table.objects.all()
    return render(request, 'CAMP COORDINATOR/MANAGE STOCK.html', {"val": ob})

@login_required(login_url='/')
def coordinator_edit_stock(request,id):
    request.session["stockid"]=id
    ob=stock_table.objects.get(id=id)
    return render(request, 'CAMP COORDINATOR/EDIT STOCK.html',{"ob":ob})

@login_required(login_url='/')
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

@login_required(login_url='/')
def coordinator_delete_stock(request,id):
    stock_table.objects.get(id=id).delete()
    return HttpResponse('''<script> alert('STOCK DELETED');window.location='/coordinator_manage_stock';</script>''')

@login_required(login_url='/')
def coordinator_search_stock(request):
    category = request.POST['select']
    ob = stock_table.objects.filter(category__icontains=category)
    return render(request, 'CAMP COORDINATOR/MANAGE STOCK.html', {"val": ob})
    





# ADD & MANAGE MEMBER
@login_required(login_url='/')
def coordinator_add_member(request):
    return render (request,'CAMP COORDINATOR/ADD MEMBER.html')

@login_required(login_url='/')
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

@login_required(login_url='/')
def coordinator_manage_members(request):
    ob = member_table.objects.all()
    return render (request,'CAMP COORDINATOR/MANAGE MEMBERS.html', {"val": ob})

@login_required(login_url='/')
def coordinator_delete_member(request,id):
    member_table.objects.get(id=id).delete()
    return HttpResponse('''<script> alert ('MEMBER DELETED');window.location='/coordinator_manage_members'</script>''')

@login_required(login_url='/')
def coordinator_edit_member(request,id):
    request.session["memberid"]=id
    ob=member_table.objects.get(id=id)
    return render(request,'CAMP COORDINATOR/EDIT MEMBER.html',{"ob":ob})

@login_required(login_url='/')
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

@login_required(login_url='/')
def coordinator_search_member(request):
    name=request.POST['name']
    ob=member_table.objects.filter(name__icontains=name)
    return render (request,'CAMP COORDINATOR/MANAGE MEMBERS.html',{'val':ob})




# MISSING ASSET
@login_required(login_url='/')
def coordinator_register_missing_asset(request):
    names=member_table.objects.filter(COORDINATOR__LOGIN_id=request.session['lid'])
    return render(request,'CAMP COORDINATOR/REGISTER MISSING ASSET.html',{'names':names})

@login_required(login_url='/')
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

@login_required(login_url='/')
def coordinator_view_missing_asset_registration(request):
    ob = asset_table.objects.all()
    return render(request, 'CAMP COORDINATOR/VIEW ASSET REGISTRATION.html', {'val': ob})

@login_required(login_url='/')
def coordinator_delete_asset_registration(request,id):
    asset_table.objects.get(id=id).delete()
    return HttpResponse('''<script> alert('ASSET REGISTRATION DELETED');window.location='/coordinator_view_missing_asset_registration';</script>''')

@login_required(login_url='/')
def coordinator_edit_asset_registration(request,id):
    request.session["assetid"] = id
    ob = asset_table.objects.get(id=id)
    return render(request, 'CAMP COORDINATOR/EDIT ASSET REGISTRATION.html', {"ob": ob})

@login_required(login_url='/')
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

@login_required(login_url='/')
def coordinator_search_asset_registration(request):
    name=request.POST['textfield']
    ob=asset_table.objects.filter(MEMBER__name__icontains=name)
    return render (request,'CAMP COORDINATOR/VIEW ASSET REGISTRATION.html', {'val': ob})



# ADD AND MANAGE NEEDS
@login_required(login_url='/')
def coordinator_add_needs(request):
    ob=camp_coordinator_table.objects.get(LOGIN=request.session["lid"])
    return render(request, 'CAMP COORDINATOR/ADD NEEDS.html',{"ob":ob})

@login_required(login_url='/')
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

@login_required(login_url='/')
def coordinator_view_needs(request):
    ob = needs_table.objects.all()
    return render(request, 'CAMP COORDINATOR/VIEW NEEDS.html', {"val": ob})

@login_required(login_url='/')
def coordinator_edit_needs(request,id):
    request.session["needsid"] = id
    ob = needs_table.objects.get(id=id)
    return render(request, 'CAMP COORDINATOR/EDIT NEEDS.html', {"ob": ob})

@login_required(login_url='/')
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

@login_required(login_url='/')
def coordinator_delete_needs(request,id):
    needs_table.objects.get(id=id).delete()
    return HttpResponse('''<script> alert('NEED DELETED');window.location='/coordinator_view_needs';</script>''')

@login_required(login_url='/')
def coordinator_search_needs(request):
    category = request.POST['select']
    ob = needs_table.objects.filter(category__icontains=category)
    return render(request, 'CAMP COORDINATOR/VIEW NEEDS.html', {"val": ob})



# MEDICAL SUPPORT REQUEST

@login_required(login_url='/')
def coordinator_manage_medical_request(request):
    ob = medical_request_table.objects.all()
    return render (request,'CAMP COORDINATOR/MANAGE MEDICAL REQUEST.html', {"val": ob})

@login_required(login_url='/')
def coordinator_search_medical_request(request):
    status = request.POST['status']
    ob = medical_request_table.objects.filter(status__icontains=status)
    return render(request, 'CAMP COORDINATOR/MANAGE MEDICAL REQUEST.html', {"val": ob})

@login_required(login_url='/')
def coordinator_edit_medical_request_status(request,id):
    request.session["medicalrequestid"] = id
    ob = medical_request_table.objects.get(id=id)
    return render(request, 'CAMP COORDINATOR/EDIT MEDICAL REQUEST STATUS.html', {"ob": ob})

@login_required(login_url='/')
def coordinator_edit_medical_request_status_post(request):
    status = request.POST["status"]
    obj = medical_request_table.objects.get(id=request.session["medicalrequestid"])
    obj.status = status
    obj.save()
    return HttpResponse('''<script> alert('STATUS UPDATED');window.location='/coordinator_manage_medical_request';</script>''')



# ADD AND MANAGE VOLUNTEER
@login_required(login_url='/')
def coordinator_volunteer_registration(request):
    return render(request,'CAMP COORDINATOR/REGISTER VOLUNTEER.html')

@login_required(login_url='/')
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

@login_required(login_url='/')
def coordinator_manage_volunteer(request):
    ob = volunteer_table.objects.all()
    return render (request,'CAMP COORDINATOR/MANAGE VOLUNTEER.html', {"val": ob})

@login_required(login_url='/')
def coordinator_search_volunteer(request):
    name = request.POST['name']
    ob = volunteer_table.objects.filter(name__icontains=name)
    return render(request, 'CAMP COORDINATOR/MANAGE VOLUNTEER.html', {"val": ob})

@login_required(login_url='/')
def coordinator_edit_volunteer(request,id):
    request.session["volunteerid"] = id
    ob = volunteer_table.objects.get(id=id)
    return render(request, 'CAMP COORDINATOR/EDIT VOLUNTEER.html', {"ob": ob})

@login_required(login_url='/')
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

@login_required(login_url='/')
def coordinator_delete_volunteer(request,id):
    volunteer_table.objects.get(id=id).delete()
    return HttpResponse('''<script> alert('VOLUNTEER DELETED');window.location='/coordinator_manage_volunteer';</script>''')






# ***** EMERGENCY RESPONCE TEAM *****

# MANAGE EMERGENCY RESPONSE
@login_required(login_url='/')
def emergency_response_team_home_page(request):
    return render (request,'EMERGENCY RESPONSE TEAM/index.html')

@login_required(login_url='/')
def emergency_response_tean_view_emergency_request(request):
    ob = emergency_request_table.objects.all()
    return render (request,'EMERGENCY RESPONSE TEAM/VIEW EMERGENCY REQUEST.html', {"val": ob})

@login_required(login_url='/')
def emergency_response_team_search_emergency_request(request):
    status = request.POST['status']
    ob = emergency_request_table.objects.filter(status__icontains=status)
    return render(request, 'EMERGENCY RESPONSE TEAM/VIEW EMERGENCY REQUEST.html', {"val": ob})

@login_required(login_url='/')
def emergency_response_edit_emergency_request_status(request,id):
    request.session["emergencyrequestid"] = id
    ob = emergency_request_table.objects.get(id=id)
    return render(request, 'EMERGENCY RESPONSE TEAM/EDIT EMERGENCY REQUEST STATUS.html', {"ob": ob})

@login_required(login_url='/')
def emergency_response_edit_emergency_request_status_post(request):
    status = request.POST["status"]
    obj = emergency_request_table.objects.get(id=request.session["emergencyrequestid"])
    obj.status = status
    obj.save()
    return HttpResponse('''<script> alert('STATUS UPDATED');window.location='/emergency_response_tean_view_emergency_request';</script>''')
