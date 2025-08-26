from django.http import JsonResponse
from django.db.models import Sum
from .models import Class, EnrollClass, Payment
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from datetime import timedelta,datetime,date
from django.utils.timezone import now, timedelta
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

def classR(request):
    if request.method == 'POST':
        form = ClassR(request.POST, request.FILES)
        if form.is_valid():
            class_instance = form.save(commit=False)   # don't save yet
            class_instance.teacher = request.user      # assign teacher
            class_instance.save()                      # now save
            messages.success(request, 'Class Registered')
            return redirect('homepage')
        else:
            print(form.errors)
            messages.error(request, "There were errors in your form. Please fix them.")
    else:
        form = ClassR()

    return render(request, 'classr.html', {'form': form})

def viewClass(request):
    if request.user.role == 'teacher':
        print(request.user)
        classes = Class.objects.filter(teacher = request.user)
    else:
        classes = Class.objects.all()
    paid_classes = []

    if request.user.role == 'student':
        paid_classes = Payment.objects.filter(userid=request.user).values_list('classid_id', flat=True)

    class_data = []
    for c in classes:
        status = ""
        if c.date > now():
            status = "Upcoming"
        elif c.date <= now() <= c.date + timedelta(minutes=c.duration):
            status = "Ongoing"
        else:
            status = "Completed"

        # Registration closes 24h before class start
        registration_close = c.date - timedelta(hours=24)
        payment_open = now() < registration_close

        class_data.append({
            "obj": c,
            "status": status,
            "payment_open": payment_open,
            "registration_close": registration_close
        })

    return render(request, 'view_class.html', {
        'class_data': class_data,
        'paid_classes': paid_classes
    })

def event(request):
    if request.method == 'POST':
        form = EventR(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            messages.success(request,'Event Registered')
            return redirect('homepage')
        else:
            print(form.errors)
            messages.error(request,form.errors)
    form = EventR()
    return render(request,'events.html',{'form':form})

def viewEvent(request):
    events = Events.objects.all()
    paid_events = []
    if request.user.role == 'student':
        paid_events = Payment.objects.filter(userid=request.user).values_list('eventid_id', flat=True)

    event_data = []
    now = timezone.now()

    for e in events:
        # If Events.date is DateField → convert to datetime for comparison
        event_date = (
            datetime.combine(e.date, datetime.min.time())
            if isinstance(e.date, date) and not isinstance(e.date, datetime)
            else e.date
        )

        # Ensure event_date is timezone-aware
        if timezone.is_naive(event_date):
            event_date = timezone.make_aware(event_date)

        # Decide event status
        if event_date > now:
            status = "Upcoming"
        elif event_date.date() == now.date():
            status = "Ongoing"
        else:
            status = "Completed"

        # Registration closes 24 hours before start
        registration_close = event_date - timedelta(hours=24)
        registration_open = now < registration_close

        event_data.append({
            "obj": e,
            "status": status,
            "registration_close": registration_close,
            "registration_open": registration_open,
        })

    return render(request, 'view_event.html', {
        'event_data': event_data,
        'paid_events': paid_events
    })







@login_required
def update_event(request, id):
    event = get_object_or_404(Events, id=id)

    # Only admin or event creator (teacher) can update
    if not (request.user.is_superuser or (request.user == event.user and request.user.role == "teacher")):
        return HttpResponseForbidden("You are not allowed to update this event.")

    if request.method == "POST":
        form = EventR(request.POST, request.FILES, instance=event)  # <-- added request.FILES
        if form.is_valid():
            form.save()
            return redirect('view_event')  # redirect to event list page
    else:
        form = EventR(instance=event)

    return render(request, 'update_event.html', {'form': form, 'event': event})


@login_required
def delete_event(request, id):
    event = get_object_or_404(Events, id=id)

    # Only admin or event creator (instructor) can delete
    if not (request.user.is_superuser or (request.user == event.user and request.user.usertype == "instructor")):
        return HttpResponseForbidden("You are not allowed to delete this event.")

    event.delete()
    return redirect('view_event')



# List Trainings
@login_required
def training_list(request):
    trainings = Training.objects.filter(user=request.user)
    return render(request, 'training_list.html', {'trainings': trainings})

@login_required
def training_lists(request):
    trainings = Training.objects.all()
    return render(request, 'training_list.html', {'trainings': trainings})



# Add Training
@login_required
def add_training(request):
    if request.method == 'POST':
        form = TrainingForm(request.POST, request.FILES)
        if form.is_valid():
            training = form.save(commit=False)
            training.user = request.user
            training.save()
            messages.success(request, "Training material added successfully.")
            return redirect('training_list')
    else:
        form = TrainingForm()
    return render(request, 'add_training.html', {'form': form})


# Update Training
@login_required
def update_training(request, training_id):
    training = get_object_or_404(Training, id=training_id, user=request.user)
    if request.method == 'POST':
        form = TrainingForm(request.POST, request.FILES, instance=training)
        if form.is_valid():
            form.save()
            messages.success(request, "Training material updated successfully.")
            return redirect('training_list')
    else:
        form = TrainingForm(instance=training)
    return render(request, 'update_training.html', {'form': form})


# Delete Training
@login_required
def delete_training(request, training_id):
    training = get_object_or_404(Training, id=training_id, user=request.user)
    if request.method == "POST":
        training.delete()
        messages.success(request, "Training material deleted successfully.")
    return redirect('training_list')




# Update a Class
def updateClass(request, class_id):
    cls = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        form = ClassR(request.POST, request.FILES, instance=cls)
        if form.is_valid():
            form.save()
            messages.success(request, "Class updated successfully.")
            return redirect('view_class')
        else:
            messages.error(request, form.errors)
    else:
        form = ClassR(instance=cls)
    return render(request, 'update_class.html', {'form': form})


# Delete a Class (inline, no extra confirm page)
def deleteClass(request, class_id):
    cls = get_object_or_404(Class, id=class_id)
    if request.method == "POST":
        cls.delete()
        messages.success(request, "Class deleted successfully.")
        return redirect('view_class')
    # If accessed by GET, just delete directly (optional)
    cls.delete()
    messages.success(request, "Class deleted successfully.")
    return redirect('view_class')

def feedback(request):
    classes = EnrollClass.objects.filter(userid=request.user,attend='Present')

    
    # Get IDs of classes the user already submitted feedback for
    submitted_classes = Feedback.objects.filter(userid=request.user).values_list('class_attended_id', flat=True)

    if request.method == 'POST':
        class_id = request.POST.get("class_name")
    
        rating = request.POST.get("rating")
        comment = request.POST.get("comments")

        if not (class_id  and rating and comment):
            messages.error(request, "All fields are required!")
        else:
            selected_class = get_object_or_404(EnrollClass, id=class_id)

            if int(class_id) in submitted_classes:
                messages.error(request, "You have already submitted feedback for this class.")
            else:
                Feedback.objects.create(
                    userid=request.user,
                    class_attended=selected_class,
                   
                    rating=rating,
                    comment=comment
                )
                messages.success(request, "Feedback submitted successfully!")
                return redirect('view_feedback')

    return render(request, "feedback.html", {
        "classes": classes,
        "submitted_classes": submitted_classes
    })


def view_feedback(request):
    feedbacks = Feedback.objects.filter(userid=request.user)
    return render(request, "view_feedback.html", {"feedbacks": feedbacks})



def view_feedbacks(request):
    feedbacks = Feedback.objects.all()
    return render(request, "view_feedback.html", {"feedbacks": feedbacks})


def reply_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)

    if request.method == "POST":
        reply_text = request.POST.get("reply")
        if reply_text:
            feedback.reply = reply_text
            feedback.reply_at = timezone.now()
            feedback.save()
            messages.success(request, "Reply added successfully!")
            return redirect('view_feedback')
        else:
            messages.error(request, "Reply cannot be empty.")

    return render(request, "reply_feedback.html", {"feedback": feedback})



def payment(request, id):
    product = Class.objects.get(id=id)
    
    return render(request, 'payment.html', {
        'product': product
    })
    


def payments(request, id):
    product = Events.objects.get(id=id)
    
    return render(request, 'payments.html', {
        'event': product
    })

def order(request, id):
    cls = Class.objects.get(id=id)

    # Check if the user already enrolled in this class
    existing_enroll = EnrollClass.objects.filter(userid=request.user, classid=cls).first()

    if existing_enroll:
        od = existing_enroll
        messages.warning(request, 'You have already enrolled in this class.')
    else:
        # Create new enrollment if not exists
        od = EnrollClass.objects.create(userid=request.user, classid=cls)
        messages.success(request, 'Enrollment successful!')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        # Check if payment already exists for this enrollment and method
        payment_exists = Payment.objects.filter(
            classid=od.classid, userid=request.user, method=payment_method
        ).exists()
        if payment_exists:
            messages.warning(request, f'Payment already exists for {payment_method}!')
            return redirect('orderdone')

        # Create payment
        if payment_method == 'card':
            return redirect('card', id=od.id, value=2)
        elif payment_method == 'upi':
            return redirect('upi', id=od.id, value=2)
        elif payment_method == 'cod':
            Payment.objects.create(method='cod', classid=od.classid, userid=request.user)
            messages.success(request, 'Payment successfull !')
            return redirect('orderdone')
        else:
            messages.error(request, 'Invalid payment method')
            return redirect('payment', id=cls.id)


def registerEvent(request, id):
    cls = Events.objects.get(id=id)

    # Check if the user already enrolled in this event
    existing_enroll = EnrollEvent.objects.filter(userid=request.user, eventid=cls).first()

    if existing_enroll:
        od = existing_enroll
        messages.warning(request, 'You have already enrolled in this Event.')
    else:
        # Create new enrollment if not exists
        od = EnrollEvent.objects.create(userid=request.user, eventid=cls)
        messages.success(request, 'Enrollment successful!')
    print("out of re")
    if request.method == 'POST':
        print("in of re")
        payment_method = request.POST.get('payment_method')

        # Check if payment already exists for this enrollment and method
        payment_exists = Payment.objects.filter(
            eventid=od.eventid, userid=request.user, method=payment_method
        ).exists()
        if payment_exists:
            print("fi ")
            messages.warning(request, f'Payment already exists for {payment_method}!')
            return redirect('orderdone')

        # Create payment
        print("out if of upi")
        if payment_method == 'card':
            return redirect('card', id=od.id, value=1)
        elif payment_method == 'upi':
            print("in re upi")
            return redirect('upi', id=od.id, value=1)
        elif payment_method == 'cod':
            Payment.objects.create(method='cod', eventid=od.classid, userid=request.user)
            od.pid = Payment
            messages.success(request, 'Payment successfull !')
            return redirect('orderdone')
        else:
            messages.error(request, 'Invalid payment method')
            return redirect('payments', id=cls.id)

def card(request, id, value):
    try:
        if value == 1:  # Event enrollment
            od = get_object_or_404(EnrollEvent, id=id)
            related_event = od.eventid   # ✅ fix here
            related_class = None
            amount = related_event.amount
        else:  # Class enrollment
            od = get_object_or_404(EnrollClass, id=id)
            related_class = od.classid
            related_event = None
            amount = related_class.amount
    except:
        od = None
        related_class = None
        related_event = None
        amount = 0

    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('number')
        cvv = request.POST.get('cvv')
        date = request.POST.get('expiry')

        k = Payment.objects.create(
            name=name,
            method='card',
            classid=related_class,
            eventid=related_event,
            userid=request.user,
            amount=amount   # ✅ save amount
        )
        od.pid = k
        od.save()
        messages.success(request, 'Payment successful!')
        return redirect('orderdone')

    return render(request, 'card.html', {'order': od})


def upi(request, id, value):
    try:
        if value == 1:  # Event enrollment
            od = get_object_or_404(EnrollEvent, id=id)
            related_event = od.eventid
            related_class = None
            amount = related_event.amount
        else:  # Class enrollment
            od = get_object_or_404(EnrollClass, id=id)
            related_class = od.classid
            related_event = None
            amount = related_class.amount
    except:
        od = None
        related_class = None
        related_event = None
        amount = 0

    if request.method == 'POST':
        name = request.POST.get('upi_id')

        k = Payment.objects.create(
            name=name,
            method="upi",
            classid=related_class,
            eventid=related_event,
            userid=request.user,
            amount=amount   # ✅ save amount
        )
        od.pid = k
        od.save()
        messages.success(request, 'Payment successful!')
        return redirect('orderdone')

    return render(request, 'upi.html', {'order': od})
# def cod(request,id):
#     try:
#         od=EnrollClass.objects.get(id=id)
#     except:
#         od=None
#     Payment.objects.create(method='cod',classid=od.classid)
#     messages.success(request, ' Payment successfull !')
#     return redirect('orderdone')


def orderdone(request):
    return render(request,'paymentdone.html')




@login_required
def my_classes(request):
    enrollments = EnrollClass.objects.filter(userid=request.user)
    return render(request, "enroll_class.html", {"enrollments": enrollments})


@login_required
def my_class(request):
    enrollments = EnrollClass.objects.all()
    return render(request, "enroll_class.html", {"enrollments": enrollments})
@login_required
def toggle_attendance(request, enroll_id):
    enrollment = get_object_or_404(EnrollClass, id=enroll_id)

    # Only teachers should be allowed to change attendance
    if request.user.role != "teacher":
        return redirect("my_classes")

    if enrollment.attend == "Not Started":
        # If first time, teacher decides what to set based on GET param
        status = request.GET.get("status")
        if status in ["Present", "Absent"]:
            enrollment.attend = status
    else:
        # Already marked once → allow toggling between Present / Absent
        if enrollment.attend == "Present":
            enrollment.attend = "Absent"
        else:
            enrollment.attend = "Present"

    enrollment.save()
    return redirect("my_class")



@login_required
def my_events(request):
    enrollments = EnrollEvent.objects.filter(userid=request.user).select_related("eventid")
    return render(request, "enroll_event.html", {"enrollments": enrollments})


@login_required
def my_event(request):
    enrollments = EnrollEvent.objects.all()
    return render(request, "enroll_event.html", {"enrollments": enrollments})






# Global Report (All Classes)
def enroll_report_chart(request):
    classes = Class.objects.all()

    # ✅ Global Attendance Summary
    attendance_data = {
        "Present": EnrollClass.objects.filter(attend="Present").count(),
        "Absent": EnrollClass.objects.filter(attend="Absent").count(),
        "Not Started": EnrollClass.objects.filter(attend="Not Started").count(),
    }

    # ✅ Enrollments per Class
    class_data = {
        "labels": [c.name for c in classes],
        "counts": [EnrollClass.objects.filter(classid=c).count() for c in classes]
    }

    # ✅ Enrollments Over Time (All Classes)
    time_data = {"labels": [], "counts": []}
    enrollments = EnrollClass.objects.dates("date", "month", order="ASC")
    for d in enrollments:
        time_data["labels"].append(d.strftime("%b %Y"))
        time_data["counts"].append(
            EnrollClass.objects.filter(date__month=d.month, date__year=d.year).count()
        )

    # ✅ Global Finance Summary
    total_revenue = Payment.objects.aggregate(total=Sum("amount"))["total"] or 0
    total_payments = Payment.objects.count()
    finance_data = {"total": total_revenue, "enrollments": total_payments}

    return render(request, "report.html", {
        "classes": classes,
        "attendance_data": attendance_data,
        "class_data": class_data,
        "time_data": time_data,
        "finance_data": finance_data,
    })


# Class-Specific Report (AJAX)
def class_report(request, class_id):
    cls = get_object_or_404(Class, id=class_id)

    # ✅ Attendance for selected class
    attendance = {
        "Present": EnrollClass.objects.filter(classid=cls, attend="Present").count(),
        "Absent": EnrollClass.objects.filter(classid=cls, attend="Absent").count(),
        "Not Started": EnrollClass.objects.filter(classid=cls, attend="Not Started").count(),
    }

    # ✅ Enrollment count for this class
    class_data = {
        "labels": [cls.name],
        "counts": [EnrollClass.objects.filter(classid=cls).count()]
    }

    # ✅ Enrollments Over Time (per class)
    time_data = {"labels": [], "counts": []}
    enrollments = EnrollClass.objects.filter(classid=cls).dates("date", "month", order="ASC")
    for d in enrollments:
        time_data["labels"].append(d.strftime("%b %Y"))
        time_data["counts"].append(
            EnrollClass.objects.filter(classid=cls, date__month=d.month, date__year=d.year).count()
        )

    # ✅ Finance for this class (directly linked via classid in Payment model)
    total_revenue = Payment.objects.filter(classid=cls).aggregate(total=Sum("amount"))["total"] or 0
    total_payments = Payment.objects.filter(classid=cls).count()

    return JsonResponse({
        "attendance": attendance,
        "class": class_data,
        "time": time_data,
        "finance": {
            "total": total_revenue,
            "enrollments": total_payments
        }
    })



@login_required
def class_chat(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    messages = ChatMessage.objects.filter(classid=class_obj).order_by('timestamp')
    
    if request.method == "POST":
        message_text = request.POST.get("message")
        if message_text:
            ChatMessage.objects.create(
                classid=class_obj,
                sender=request.user,
                message=message_text
            )

    return render(request, "chat.html", {
        "class_obj": class_obj,
        "messages": messages
    })



@login_required
def clear_chat(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    
    # Only allow teachers to clear chat
    if request.user.role != 'teacher':
        return redirect('class_chat', class_id=class_id)
    
    if request.method == 'POST':
        ChatMessage.objects.filter(classid=class_obj).delete()
    
    return redirect('class_chat', class_id=class_id)