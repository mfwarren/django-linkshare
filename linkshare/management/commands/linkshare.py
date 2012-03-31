from AppControl.linkshare.models import SalesReport

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from settings import *
import datetime, time
import urllib2, urllib
import csv

class Command(BaseCommand):
    help = "Download sales data from Admob"

    def handle(self, *args, **options):
        users = User.objects.filter(is_active=True)

        for user in users:
            profile = user.get_profile()
            if not profile.linkshare_token:  #THIS IS IN THE MAIN APP
                continue

            url = 'https://reportws.linksynergy.com/downloadreport.php'

            #storing month to date because attribution can take a while to show up.  ie. yesterday will always show $0
            today = datetime.datetime.now()
            start_date = today + datetime.timedelta(days=-today.day+1)
            end_date = today

            data = {'reportid':4,
                    'bdate':start_date.strftime("%Y%m%d"),
                    'edate':end_date.strftime("%Y%m%d"),
                    'token':profile.linkshare_token,
                    }

            url = url + '?' + urllib.urlencode(data)
            request = urllib2.urlopen(url)
            csv_reader = csv.DictReader(request)

            for row in csv_reader:
                if 'Advertiser ID' not in row:
                    print 'empty row?', row
                    continue
                if not row['Advertiser ID']:
                    print 'empty row?', row
                    continue

                try:
                    report = SalesReport.objects.get(user=user, date=end_date, advertiser_id=row['Advertiser ID'])
                except SalesReport.DoesNotExist:
                    report = SalesReport(user=user, date=end_date)

                report.advertiser_id = row['Advertiser ID']
                report.advertiser = row['Advertiser']
                report.impressions = float(row['Impressions'])
                report.clicks = float(row['Clicks'])
                report.ctr = float(row['CTR'])
                report.orders = float(row['Orders'])
                report.orders_per_click = float(row['Orders/Click'])
                report.epc = float(row['EPC'])
                report.items = float(row['Items'])
                report.cancelled_items = float(row['Cancelled Items'])
                report.sales = float(row['Sales'])
                report.baseline_commissions = float(row['Baseline Commissions'])
                report.adjusted_commissions = float(row['Adjusted Commissions'])
                report.actual_commissions = float(row['Actual Commissions'])
                report.save()

