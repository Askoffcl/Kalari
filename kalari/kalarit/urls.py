from django.urls import path
from . import views



urlpatterns = [
    path('classr/',views.classR),
    path('view_class/',views.viewClass,name = 'view_class'),
    path('event/',views.event),
    path('view_event/',views.viewEvent,name = 'view_event'),
    path('events/<int:id>/update/', views.update_event, name='update_event'),
    path('events/<int:id>/delete/', views.delete_event, name='delete_event'),
    path('trainings/', views.training_list, name='training_list'),
    path('training/', views.training_lists, name='training_lists'),
    path('trainings_add/', views.add_training, name='add_training'),
    path('trainings_update/<int:training_id>/', views.update_training, name='update_training'),
    path('trainings_delete/<int:training_id>/', views.delete_training, name='delete_training'),
    path('class_update/<int:class_id>/', views.updateClass, name='update_class'),
    path('class_delete/<int:class_id>/', views.deleteClass, name='delete_class'),
    path('feedback/', views.feedback, name='feedback'),
    path('view_feedback/', views.view_feedback, name='view_feedback'),
    path('view_feedbacks/', views.view_feedbacks, name='view_feedback'),
    path('feedback/reply/<int:feedback_id>/', views.reply_feedback, name='reply_feedback'),
    path('payment/<int:id>/',views.payment,name = 'payment'),
      path('payments/<int:id>/',views.payments,name = 'payments'),
    path('card/<int:id>/<int:value>',views.card,name='card'),
    path('upi/<int:id>/<int:value>',views.upi,name='upi'),
    
    path('orderdone',views.orderdone,name='orderdone'),
    path('order/<int:id>/',views.order,name='order'),
    path('registerEvent/<int:id>/',views.registerEvent,name='registerEvent'),
     path("my_classes/", views.my_classes, name="my_classes"),
     path("my_class/", views.my_class, name="my_class"),
    path("toggle-attendance/<int:enroll_id>/", views.toggle_attendance, name="toggle_attendance"),
       path("my_events/", views.my_events, name="my_events"),
             path("my_event/", views.my_event, name="my_event"),
             path("enroll_report/", views.enroll_report_chart, name="enroll_report"),
             
path("reports/class/<int:class_id>/", views.class_report, name="class_report"),
path('chat/<int:class_id>/', views.class_chat, name='class_chat'),
  path('chat/clear/<int:class_id>/', views.clear_chat, name='clear_chat'),

]