from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login,logout
from datetime import date as date
from django.db.models import Q, Min, Max
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date as date, datetime as dt
from django.db.models import Q, Min, Max


# Create your views here.
def index(request):
    return render(request, 'index.html')

def user_logout(request):
    logout(request)
    return redirect('index')


def admin(request):
    adm=Login.objects.create_superuser(username='admin',email='admin@gmail.com',viewpassword='1234',password='1234',usertype='Admin')
    adm.save()
    return redirect('/')

def view_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']       
        
        user = authenticate(request, username=username, password=password) 
        if user is not None:
            if user.is_active:
                auth_login(request, user)  

                if user.usertype == "Admin":
                    return redirect('admin_dashboard')

                elif user.usertype == "Investigator":
                    request.session['uid'] = user.id  
                    return redirect('investigator_dashboard')

                elif user.usertype == "Court":
                    request.session['uid'] = user.id
                    return redirect('Court_dashboard')

                else:
                    return redirect('login')  
            else:
                messages.error(request, 'Your account is inactive')
                return render(request, 'login.html')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

    return render(request, 'login.html')

def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html')

def investigator_dashboard(request):
    return render(request,'investigator/investigator_dashboard.html')

def Court_dashboard(request):
    return render(request,'Court/victim_dashboard.html')



def investigator_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        image = request.FILES.get('image')

        if Login.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('investigator_register')

        if Login.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return redirect('investigator_register')

        if Investigator.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number is already registered.')
            return redirect('investigator_register')

        login_user = Login.objects.create(
            username=username,
            usertype="Investigator",
            email=email,
            viewpassword=password,
            is_active=False  
        )
        login_user.set_password(password)
        login_user.save()

        investigator = Investigator.objects.create(
            investigator_id=login_user,
            username=username,
            name=name,
            email=email,
            phone=phone,
            address=address,
            image=image
        )
        investigator.save()

        messages.success(request, 'Investigator registered successfully! Waiting for admin approval.')
        return redirect('view_login')  

    return render(request, 'investigator_register.html')

def victim_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        image = request.FILES.get('image')

        if Login.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('victim_register')
        if Login.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return redirect('victim_register')
        if Victim.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number is already registered.')
            return redirect('victim_register')

        login_user = Login.objects.create(
            username=username,
            usertype="Victim",
            email=email,
            viewpassword=password,
            is_active=False  
        )
        login_user.set_password(password)
        login_user.save()

        victim = Victim.objects.create(
            victim_id=login_user,
            username=username,
            name=name,
            email=email,
            phone=phone,
            address=address,
            image=image
        )
        victim.save()

        messages.success(request, 'Victim registered successfully! Waiting for admin approval.')
        return redirect('view_login')

    return render(request, 'victim_register.html')


def display_all_investigators(request):
    investigators = Investigator.objects.all()
    return render(request, 'admin/display_all_investigators.html', {'investigators': investigators})

def accept_investigator(request, investigator_id):
    login_user = get_object_or_404(Login, id=investigator_id)
    login_user.is_active = True
    login_user.save()
    messages.success(request, 'Investigator accepted successfully.')
    return redirect('display_all_investigators')

def reject_investigator(request, investigator_id):
    login_user = get_object_or_404(Login, id=investigator_id)
    investigator = Investigator.objects.filter(investigator_id=login_user).first()
    
    if investigator:
        investigator.delete()
    
    login_user.delete()
    messages.success(request, 'Investigator rejected successfully.')
    return redirect('display_all_investigators')


def display_all_victims(request):
    victims = Victim.objects.all()
    return render(request, 'admin/display_all_victims.html', {'victims': victims})

def accept_victim(request, victim_id):
    login_user = get_object_or_404(Login, id=victim_id)
    login_user.is_active = True
    login_user.save()
    messages.success(request, 'Victim accepted successfully.')
    return redirect('display_all_victims')

def reject_victim(request, victim_id):
    login_user = get_object_or_404(Login, id=victim_id)
    victim = Victim.objects.filter(victim_id=login_user).first()
    
    if victim:
        victim.delete()
    
    login_user.delete()
    messages.success(request, 'Victim rejected successfully.')
    return redirect('display_all_victims')


def investigator_profile(request):
    investigator = get_object_or_404(Investigator, investigator_id=request.user)
    return render(request, 'investigator/investigator_profile.html', {'investigator': investigator})

def edit_investigator_profile(request):
    investigator = get_object_or_404(Investigator, investigator_id=request.user)
    login_user = investigator.investigator_id  # Get the associated Login instance
    
    if request.method == "POST":
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_name = request.POST.get('name')
        new_phone = request.POST.get('phone')
        new_address = request.POST.get('address')

        # Update Investigator model
        investigator.username = new_username
        investigator.name = new_name
        investigator.email = new_email
        investigator.phone = new_phone
        investigator.address = new_address

        # Update Login (AbstractUser) model
        login_user.username = new_username
        login_user.email = new_email

        if 'image' in request.FILES:
            investigator.image = request.FILES['image']
        
        # Save both models
        login_user.save()
        investigator.save()

        return redirect('investigator_profile')

    return render(request, 'investigator/edit_investigator_profile.html', {'investigator': investigator})


def victim_profile(request):
    victim = get_object_or_404(Victim, victim_id=request.user)
    return render(request, 'victim/victim_profile.html', {'victim': victim})

def edit_victim_profile(request):
    victim = get_object_or_404(Victim, victim_id=request.user)

    if request.method == "POST":
        username = request.POST["username"]
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        image = request.FILES.get("image")

        # Update the victim model
        victim.username = username
        victim.name = name
        victim.email = email
        victim.phone = phone
        victim.address = address

        if image:
            victim.image = image

        victim.save()

        # Also update the Login model (AbstractUser)
        login_user = Login.objects.get(id=victim.victim_id.id)
        login_user.username = username
        login_user.email = email
        login_user.save()

        return redirect("victim_profile")

    return render(request, "victim/edit_victim_profile.html", {"victim": victim})




def apply_case(request):
    if request.method == "POST":
        case_title = request.POST.get("case_title")
        case_description = request.POST.get("case_description")
        incident_place = request.POST.get("incident_place")  # New field
        investigator_id = request.POST.get("investigator")
        
        try:
            victim = Victim.objects.get(victim_id=request.user)
        except Victim.DoesNotExist:
            return render(request, 'apply_case.html', {"error": "Victim profile not found"})

        investigator = Investigator.objects.get(id=investigator_id) if investigator_id else None

        # Handle Image Uploads
        image1 = request.FILES.get("image1")
        image2 = request.FILES.get("image2")
        image3 = request.FILES.get("image3")

        Case.objects.create(
            case_title=case_title,
            case_description=case_description,
            incident_place=incident_place,
            victim=victim,
            investigator=investigator,
            image1=image1,
            image2=image2,
            image3=image3
        )

        return redirect("apply_case")  
    investigators = Investigator.objects.all()
    return render(request, "victim/apply_case.html", {"investigators": investigators})



def victim_cases(request):
    try:
        victim = Victim.objects.get(victim_id=request.user)  
    except Victim.DoesNotExist:
        return render(request, 'victim_cases.html', {"error": "Victim profile not found"})

    cases = Case.objects.filter(victim=victim)  

    return render(request, 'victim/victim_cases.html', {"cases": cases})



def edit_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    investigators = Investigator.objects.all()

    if request.method == "POST":
        case.case_title = request.POST.get("case_title")
        case.case_description = request.POST.get("case_description")
        case.incident_place = request.POST.get("incident_place")
        case.status = request.POST.get("status")  # Hidden field submission
        
        investigator_id = request.POST.get("investigator")
        if investigator_id:
            case.investigator = Investigator.objects.get(id=investigator_id)

        # Handling Image Uploads
        if "image1" in request.FILES:
            case.image1 = request.FILES["image1"]
        if "image2" in request.FILES:
            case.image2 = request.FILES["image2"]
        if "image3" in request.FILES:
            case.image3 = request.FILES["image3"]

        case.save()
        return redirect('victim_cases')  # Redirect to victim cases page after saving

    return render(request, "victim/edit_case.html", {"case": case, "investigators": investigators})
def delete_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    case.delete()
    return redirect('victim_cases')


def investigator_cases(request):
    if request.user.usertype == "Investigator":
        cases = Case.objects.filter(investigator__investigator_id=request.user)
        return render(request, 'investigator/investigator_cases.html', {'cases': cases})
    else:
        return render(request, 'investigator_dashboard.html', {'message': 'Unauthorized access'})

@csrf_exempt
def update_case_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            case_id = data.get("case_id")
            new_status = data.get("status")
            case = get_object_or_404(Case, id=case_id)
            case.status = new_status
            case.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})



# def evidence_collection(request, case_id):
#     case = get_object_or_404(Case, id=case_id)

#     if request.method == 'POST':
#         case.evidence_description = request.POST.get('evidence_description')
#         case.witness_statements = request.POST.get('witness_statements')
#         case.forensic_report = request.POST.get('forensic_report')
#         case.suspect_details = request.POST.get('suspect_details')

#         if 'evidence_image1' in request.FILES:
#             case.evidence_image1 = request.FILES['evidence_image1']
#         if 'evidence_image2' in request.FILES:
#             case.evidence_image2 = request.FILES['evidence_image2']
#         if 'evidence_image3' in request.FILES:
#             case.evidence_image3 = request.FILES['evidence_image3']

#         case.save()
#         return redirect('investigator_cases')  

#     return render(request, 'investigator/evidence_collection.html', {'case': case})
# ===================================================================================================







# cybercrime_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Case
import cv2
import numpy as np

def detect_fake_video(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return ("Error: cannot open", 0.0)

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps if fps > 0 else 0
        avg_brightness = 0
        sample_frames = min(10, frame_count)
        for i in np.linspace(0, frame_count-1, sample_frames, dtype=int):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                avg_brightness += np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        avg_brightness /= sample_frames if sample_frames > 0 else 1

        # 🔍 Simple heuristic
        if frame_count < 60 or duration < 2 or avg_brightness < 30:
            verdict, confidence = "Fake", 0.95
        else:
            verdict, confidence = "Real", 0.9

        cap.release()
        return (verdict, confidence)
    except Exception as e:
        print("Detection error:", e)
        return ("Error", 0.0)


def evidence_collection(request, case_id):
    case = get_object_or_404(Case, id=case_id)

    if request.method == 'POST':
        case.evidence_description = request.POST.get('evidence_description')
        case.witness_statements = request.POST.get('witness_statements')
        case.forensic_report = request.POST.get('forensic_report')
        case.suspect_details = request.POST.get('suspect_details')

        for i in range(1, 4):
            fkey = f"evidence_image{i}"
            if fkey in request.FILES:
                setattr(case, f"evidence_image{i}", request.FILES[fkey])

        if 'evidence_video' in request.FILES:
            case.evidence_video = request.FILES['evidence_video']
            case.save()
            verdict, confidence = detect_fake_video(case.evidence_video.path)
            case.video_verdict = verdict
            case.video_confidence = confidence

        case.save()
        return redirect('investigator_cases')

    return render(request, 'investigator/evidence_collection.html', {'case': case})



def display_evidence_collection(request):
    investigator = request.user
    # ✅ Corrected variable name ('cases' instead of 'case')
    cases = Case.objects.filter(investigator=investigator)
    return render(request, 'investigator/display_evidence_collection.html', {'cases': cases})
















# ===================================================================================================

def add_suspect(request):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        address = request.POST.get("address")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        status = request.POST.get("status")

        Suspect.objects.create(
            name=name,
            age=age,
            address=address,
            description=description,
            image=image,
            status=status,
        )
        return redirect("display_suspects")  # Redirect to suspects list

    return render(request, "admin/add_suspect.html")



def display_suspects(request):
    suspects = Suspect.objects.all()
    return render(request, "admin/display_suspects.html", {"suspects": suspects})

def edit_suspect(request, suspect_id):
    suspect = get_object_or_404(Suspect, id=suspect_id)

    if request.method == "POST":
        suspect.name = request.POST["name"]
        suspect.age = request.POST["age"]
        suspect.address = request.POST["address"]
        suspect.description = request.POST["description"]
        suspect.status = request.POST["status"]

        if "image" in request.FILES:
            suspect.image = request.FILES["image"]

        suspect.save()
        return redirect("display_suspects")

    return render(request, "admin/edit_suspect.html", {"suspect": suspect})


def delete_suspect(request, suspect_id):
    suspect = get_object_or_404(Suspect, id=suspect_id)
    suspect.delete()
    return redirect("display_suspects")


def view_evidence(request, case_id):
    case = Case.objects.get(id=case_id)
    return render(request, 'victim/view_evidence.html', {'case': case})


def chat(request):
    uid = request.session["uid"]
    name = ""
    artistData = Victim.objects.all()
    id = request.GET.get("id")
    getChatData = Chat.objects.filter(
        Q(sellerid__investigator_id=uid) & Q(customerid=id))
    current_time = dt.now().time()
    formatted_time = current_time.strftime("%H:%M")
    userid = Investigator.objects.get(investigator_id=uid)
    if id:
        customerid = Victim.objects.get(id=id)
        name = customerid.username
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(
            sellerid=userid, message=message, customerid=customerid, time=formatted_time, utype="SELLER")
        sendMsg.save()
    return render(request, "investigator/RECIEVER.html", {"artistData": artistData, "getChatData": getChatData, "customerid": name, "id": id})


def reply(request):
    uid = request.session["uid"]
    name = ""
    userData = Investigator.objects.all()
    id = request.GET.get("id")
    getChatData = Chat.objects.filter(
        Q(customerid__victim_id=uid) & Q(sellerid=id))
    current_time = dt.now().time()
    formatted_time = current_time.strftime("%H:%M")
    customerid = Victim.objects.get(victim_id=uid)
    if id:
        userid = Investigator.objects.get(id=id)
        name = userid.username
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(
            sellerid=userid, message=message, customerid=customerid, time=formatted_time, utype="CUSTOMER")
        sendMsg.save()
    return render(request, "victim/SENDER.html", {"userData": userData, "getChatData": getChatData, "userid": name, "id": id})



def request_investigator(request):
    victim_cases = Case.objects.filter(victim__victim_id=request.user)

    if request.method == "POST":
        case_id = request.POST.get('case_id')
        new_investigator_id = request.POST.get('investigator')

        if case_id and new_investigator_id:
            case = Case.objects.get(id=case_id)
            if not case.requested_investigator:  # Prevent duplicate requests
                new_investigator = Investigator.objects.get(id=new_investigator_id)
                case.requested_investigator = new_investigator
                case.save()
            return redirect('/request-investigator/')  # Redirect after submission

    investigators = Investigator.objects.all()

    return render(request, "victim/request_investigator.html", {
        "victim_cases": victim_cases.filter(requested_investigator__isnull=True),  # Show only cases without requests
        "investigators": investigators
    })


def requested_investigators_list(request):
    requested_cases = Case.objects.filter(requested_investigator__isnull=False)

    return render(request, "admin/requested_investigators.html", {
        "requested_cases": requested_cases
    })



def approve_investigator_change(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if case.requested_investigator:
        case.investigator = case.requested_investigator
        case.requested_investigator = None
        case.save()
        messages.success(request, "Investigator change approved successfully.")
    return redirect('requested_investigators_list')

def reject_investigator_change(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    case.requested_investigator = None
    case.save()
    messages.warning(request, "Investigator change request rejected.")
    return redirect('requested_investigators_list')


def suspect_list(request):
    if request.user.is_authenticated:
        suspects = Suspect.objects.all()  
        return render(request, 'investigator/suspect_list.html', {'suspects': suspects})
    else:
        return redirect('view_login')  


def display_evidence_collection(request):
    investigator = request.user
    cases = Case.objects.filter(investigator__investigator_id=investigator)  
    suspects = Suspect.objects.all() 
    return render(request, 'investigator/display_evidence_collection.html', {'case': cases, 'suspects': suspects})


def submit_final_report(request, case_id):
    if request.method == "POST":
       
        case = get_object_or_404(Case, id=case_id)

        identified_suspect_id = request.POST.get("identified_suspect")
        analysis_summary = request.POST.get("analysis_summary")
        final_conclusion = request.POST.get("final_conclusion")

        # identified_suspect = get_object_or_404(Suspect, id=identified_suspect_id)

        CaseAnalysis.objects.create(
            case=case,
            investigator=case.investigator,
            identified_suspect1=identified_suspect_id,
            analysis_summary=analysis_summary,
            final_conclusion=final_conclusion,
        )    
        case.status = 'Closed'
        case.save()       
        messages.success(request, "Final report submitted successfully!")
      
        return redirect("display_evidence_collection")
    return redirect("display_evidence_collection")


def victim_case_analysis(request):
    victim = Victim.objects.get(victim_id=request.user) 
    cases = Case.objects.filter(victim=victim)  
    case_analysis = CaseAnalysis.objects.filter(case__in=cases)  

    return render(request, 'victim/victim_case_analysis.html', {'case_analysis': case_analysis})


def investigator_case_analysis(request):
    investigator = Investigator.objects.get(investigator_id=request.user)
    case_analysis = CaseAnalysis.objects.filter(investigator=investigator)

    return render(request, 'investigator/investigator_case_analysis.html', {'case_analysis': case_analysis})


def view_case_analysis_admin(request):


    case_id = request.GET.get('id')  # ✅ get id from URL like ?id=3
    case = get_object_or_404(Case, id=case_id)  # ✅ safely fetch case

    case_analyses = CaseAnalysis.objects.filter(case=case).select_related('investigator', 'case')

    return render(request, 'admin/admin_case_analysis.html', {
        'case': case,
        'case_analyses': case_analyses
    })

def admin_view_cases(request):
    """
    Admin page to list all cases with summary info and link to details.
    """
    cases = Case.objects.all().order_by('-id')
    return render(request, 'admin/view_all_cases.html', {'cases': cases})

def case_analysis_view(request):
    
    
    case_summary = {
        'Open': CaseAnalysis.objects.filter(final_conclusion='Open').count(),
        'Solved': CaseAnalysis.objects.filter(final_conclusion='Solved').count(),
        'Closed': CaseAnalysis.objects.filter(final_conclusion='Closed').count()
    }

    return render(request, 'admin/case_analysis.html', {
        'case_data_json': json.dumps(case_summary)
    })









def admin_view_case_detail(request, case_id):
    """
    Admin view to see complete case details, including evidence and video verdict.
    """
    case = get_object_or_404(Case, id=case_id)
    return render(request, 'admin/view_case_detail.html', {'case': case})


def add_court(request):
    if request.method == 'POST':
        court_name = request.POST.get('court_name')
        court_type = request.POST.get('court_type')
        judge_name = request.POST.get('judge_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')  # Add password field to your form
        court_image = request.FILES.get('court_image')

        # ✅ Validation checks
        if Login.objects.filter(username=court_name).exists():
            messages.error(request, 'A court with this name already exists as a username.')
            return redirect('add_court')

        if Login.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered with another account.')
            return redirect('add_court')

        if Court1.objects.filter(phone=phone).exists():
            messages.error(request, 'This phone number is already registered with another court.')
            return redirect('add_court')

        # ✅ Create Login entry first
        login_user = Login.objects.create(
            username=court_name,
            usertype="Court",
            email=email,
            viewpassword=password,
            is_active=True  # You can set False if you want admin approval
        )
        login_user.set_password(password)
        login_user.save()

        # ✅ Now create the Court record linked to Login
        court = Court1.objects.create(
            court_idd=login_user,   # ForeignKey to Login
            court_name=court_name,
            court_type=court_type,
            judge_name=judge_name,
            email=email,
            phone=phone,
            address=address,
            court_image=court_image
        )

        messages.success(request, 'Court added successfully!')
        return redirect('admin_view_courts')  # Page to view all courts

    return render(request, 'admin/add_court.html')


def admin_view_courts(request):
    courts = Court1.objects.all()
    return render(request, 'admin/admin_view_courts.html', {'courts': courts})


def court_cases(request):
  
    cases = Case.objects.all()
    return render(request, 'Court/investigator_cases.html', {'cases': cases})

    
    
    
def court_display_evidence_collection(request):
    case_id = request.GET.get('id')  # get the case ID from the URL query
    if not case_id:
        return render(request, 'Court/display_evidence_collection.html', {'error': 'No case ID provided.'})

    # ✅ Fetch the specific case or show 404 if not found
    case = get_object_or_404(Case, id=case_id)

    # Since all evidence fields are stored within the Case model itself,
    # no need to query a separate Evidence table.
    # Pass the single case object to the template.
    context = {
        'case': case
    }
    return render(request, 'Court/display_evidence_collection.html', context)






from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Case, Investigator

def add_case(request):
    try:
        investigator = Investigator.objects.get(username=request.user)
    except Investigator.DoesNotExist:
        messages.error(request, "Investigator not found.")
        return redirect('login')  # Or any appropriate page
    vict=Victim.objects.get(id=3)
    if request.method == "POST":
        case_title = request.POST.get("case_title")
        case_description = request.POST.get("case_description")
        incident_place = request.POST.get("incident_place")
        status = request.POST.get("status", "Open")
        victim_details = request.POST.get("victim")  # Text entered by investigator

        # ✅ Create new case
        new_case = Case.objects.create(
            case_title=case_title,
            case_description=case_description,
            victim_details=victim_details,
            investigator=investigator,
            incident_place=incident_place,
            status=status,
            victim=vict

        )

        # ✅ Handle optional image uploads
        if "image1" in request.FILES:
            new_case.image1 = request.FILES["image1"]
        if "image2" in request.FILES:
            new_case.image2 = request.FILES["image2"]
        if "image3" in request.FILES:
            new_case.image3 = request.FILES["image3"]

        new_case.save()

        messages.success(request, "Case added successfully! Proceed to add evidence.")
        return redirect('investigator_cases')  # Step 2: add evidence

    return render(request, "investigator/add_case.html")

def dell(request):
    Case.objects.filter(id=8).delete()