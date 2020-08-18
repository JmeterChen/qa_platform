from django.urls import path,re_path
from testcase.views import modelformviews,formviews,study



urlpatterns = [

	path('add_case/', modelformviews.CaseAdd.as_view()),
	path('get_case/', modelformviews.CaseGet.as_view()),
	path('update_case/', modelformviews.CaseUpdate.as_view()),
	path('del_case/', modelformviews.CaseDel.as_view()),


	path('case/', study.CaseModelView.as_view()),

	path('formcase/', formviews.CaseView.as_view()),


	re_path(r'detail/(\d+)', study.detail),


	# re_path(r'edit-(\d+)/', modelformviews.detail),

	path('case_list/', study.case_list,),

	re_path(r'case/(?P<pk>\d+)/', study.CaseDetailModelView.as_view()),

	re_path(r'formcase/(?P<pk>\d+)/', formviews.CaseDetailView.as_view())
]