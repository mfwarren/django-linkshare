
import datetime, time
from datetime import timedelta
import json
# Django imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.db.models import Sum
from django.http import HttpResponse

from linkshare.models import *


@login_required
def linkshare_stats(request):
    if not request.user.get_profile().linkshare_token:
        return HttpResponse("")
        
    reports = SalesReport.objects.filter(user=request.user, date=datetime.date.today())
    total = SalesReport.objects.filter(user=request.user, date=datetime.date.today()).aggregate(total=Sum('baseline_commissions'))['total']
    return render_to_response('linkshare_stats.html', locals(), context_instance=RequestContext(request))
