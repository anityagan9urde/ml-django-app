import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class LoanFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name="date_created", lookup_expr='gte')
	end_date = DateFilter(field_name="date_created", lookup_expr='lte')
	note = CharFilter(field_name='note', lookup_expr='icontains')
	status = CharFilter(field_name='status', lookup_expr=None)

	class Meta:
		model = LoanApplication
		fields = '__all__'
		exclude = ['applicant', 'date_created']