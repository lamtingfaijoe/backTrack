from django.urls import path,re_path
from COMP3297 import views

urlpatterns = [
    path('<int:project>/inviteDeveloper/',
        views.inviteDeveloper
        , name='inviteDeveloper'),
    path('<int:project>/inviteManager/',
        views.inviteManager
        , name='inviteManager'),
	path('<int:project>/owner',
		views.OwnerView.as_view(),
		name='owner'),
	path('<int:project>/manager',
		views.ManagerView.as_view(),
		name='manager'),
	path('<int:project>/developer',
		views.DeveloperView.as_view(),
		name='developer'),
	path('unassigneddeveloper',
		views.UnassignedDeveloperView.as_view(),
		name='unassigneddeveloper'),
	path('managerhome/<str:username>',
		views.ManagerHomeView.as_view(),
		name='managerhome'),
	path('signup/',
		views.SignUpView,
		name='signup'),
	path('home/', 
		views.HomeView.as_view(), 
		name='home'),
    path('gotowork/',
         views.GoToWork,
         name='GoToWork'),
	path('newproject/',
		views.newproject,
		name='newproject'),
	path('newpbi/<int:project_id>/',
		views.newPBI
		, name='newPBI'),
	path('newtask/<int:project_id>/',
		views.newtask,
		name='newtask'),
    path('newSprint/<int:project>/',
    	views.newSprint,
    	name='newSprint'),
    path('editpbi/<int:id>/',
    	views.editpbi,
    	name='editpbi'),
    path('deleteProject/<int:id>/',
    	views.deleteProject,
    	name='deleteProject'),
    path('deletepbi/<int:id>/',
    	views.deletepbi,
    	name='deletepbi'),
    path('deletetask/<int:id>/',
    	views.deletetask,
    	name='deletetask'),
    path('deleteSprint/<int:project_id>',
    	views.deleteSprint,
    	name='deleteSprint'),
    path('nextSprint/<int:project_id>/',
    	views.nextSprint,
    	name='nextSprint'),
    path('email/',
    	views.sendEmail,
    	name='sendEmail'),
]		
