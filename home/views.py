from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
import whois

def home(request):
    context = {}
    if request.method == 'POST':
        domainName = request.POST.get('domainName')
        try:
            w = whois.whois(domainName)
            print(w)
            doms = {}        
            doms['Domain Name'] = w['domain_name']
            doms['Registrar'] = w['registrar']
            doms['Whois Server'] = w['whois_server']
            try:
                udate = []
                for i in list(w['updated_date']):
                    udate.append(i.strftime("%Y-%m-%d %H:%M:%S"))        
                cdate = []
                for i in list(w['creation_date']):
                    cdate.append(i.strftime("%Y-%m-%d %H:%M:%S"))
                edate = []
                edate.append(w['expiration_date'].strftime("%Y-%m-%d %H:%M:%S"))            
                doms['Updated Date'] = udate[0]
                doms['Created Date'] = cdate[0]
                doms['Expiration Date'] = edate[0]
            except:
                pass
            doms['Name Servers'] = "{}, {}, {}, {}".format(w['name_servers'][0],w['name_servers'][1],w['name_servers'][2],w['name_servers'][3])
            doms['Status'] = w['status']
            doms['Emails'] = "{},{}".format(w['emails'][0],w['emails'][1])
            doms['Name'] = w['name']
            doms['Organization'] = w['org']
            doms['Address'] = w['address']
            doms['City'] = w['city']
            doms['State'] = w['state']
            doms['Zip Code'] = w['zipcode']
            doms['Country'] = w['country']
            print(doms)
            context = {'data': doms}
        except (whois.parser.PywhoisError, RuntimeError):
            context = {'data': {'Error': 'Not found!'}}
        except Exception as e:
            context = {'data': {'Error': 'Error'}}
    return render(request, 'home/index.html', context)