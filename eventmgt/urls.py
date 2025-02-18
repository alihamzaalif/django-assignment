from django.urls import path
from eventmgt.views import home_view, sign_up, sign_in, sign_out, add_event, add_category, add_participant, update_event, delete_event, organizer_dashboard, event_detail
urlpatterns = [
    path('', home_view, name="home_view"),
    path('add-event/', add_event, name="add_event"),
    path('organizer-dashboard/', organizer_dashboard, name="organizer-dashboard"),
    path('add-category/', add_category, name="add_category"),
    path('add-participant/', add_participant, name="add_participant"),
    path('update-event/<int:id>/', update_event, name="update-event"),
    path('event-detail/<int:id>/', event_detail, name="event-detail"),
    path('delete-event/<int:id>/', delete_event, name="delete-event"),
    path('sign-up/', sign_up, name="sign-up"),
    path('log-in/', sign_in, name="log-in"),
    path('sign-out/', sign_out, name="logout"),
]