

from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse, response
from pyparsing import null_debug_action
from pprint import pprint
from django.core.files.storage import FileSystemStorage
from ttp import ttp
from ipaddress import IPv4Address , IPv4Network
from colorama import Fore, Back, Style
import re
import csv
import datetime
import shlex
import ipaddress
import time
from tqdm import tqdm


def get_test_template():
    with open('Allfiles/template/ttp_test_template.txt') as template1:
        b = template1.read()
        template1.close()
        return b
def get_test1_template():
    with open('Allfiles/template/ttp_test1_template.txt') as template2:
        c = template2.read()
        template2.close()
        return c
def get_test2_template():
    with open('Allfiles/template/ttp_test2_template.txt') as template3:
        d = template3.read()
        template3.close()
        return d
def get_test3_template():
    with open('Allfiles/template/ttp_test3_template.txt') as template4:
        e = template4.read()
        template4.close()
        return e
def get_test4_template():
    with open('Allfiles/template/ttp_test4_template.txt') as template1:
        c = template1.read()
        template1.close()
        return c


class extraction_policy(TemplateView):
    def get(self,request):
        print("=========GET===========")
        return render(request,'Firewall/home.html')
    def post(self,request):
        print("=========post==========")
        print(request.POST.get("ipaddress")," ====++++++++++++=======")

        if request.method == "POST" and request.FILES['customFile']:
            if request.POST.get("ipaddress") == '':
                print(request.POST.get("ipaddress"),'==============================================')
                IP_ADDRESS = "all"
                sheet = request.FILES.get('customFile')
                a = str(sheet.read(),'UTF-8')
                # pprint(Data)

                b= get_test_template()
                c= get_test1_template()
                d= get_test2_template()
                e= get_test3_template()
                f= get_test4_template()
                
                #### EXTRACTING POLICY FROM CONFIG FILE #######
                results = {}

                parser = ttp(data=a, template=b)
                parser.parse()

                results['facts'] = parser.result()[0][0]

                # pprint(results)

                #### EXTRACTING IP OBJ FROM CONFIG FILE #######
                results1 = {}

                parser1 = ttp(data=a, template=c)
                parser1.parse()

                results1['facts'] = parser1.result()[0][0]

                #### EXTRACTING IP GRP FROM CONFIG FILE #######
                results2 = {}

                parser2 = ttp(data=a, template=d)
                parser2.parse()

                results2['facts'] = parser2.result()[0][0]

                #### EXTRACTING SERVICE OBJ FROM CONFIG FILE #######
                results3 = {}

                parser3 = ttp(data=a, template=e)
                parser3.parse()

                results3['facts'] = parser3.result()[0][0]

                #### EXTRACTING SERVICE GRP FROM CONFIG FILE #######
                results4 = {}

                parser4 = ttp(data=a, template=f)
                parser4.parse()

                results4['facts'] = parser4.result()[0][0]


                def Get_IP (): 
                    while True:
                        try:
                            # IP_ADDRESS= '192.168.0.6'
                            # IP_ADDRESS= input("PLEASE ENTER A VALID PRIVATE IP ADDRESS [eg: 192.168.0.1]: ")
                            if IP_ADDRESS == 'all':
                                return(IP_ADDRESS) 
                            elif IPv4Address(IP_ADDRESS).is_private:
                                return(IP_ADDRESS) 
                            else:
                                print("OOPS! That wasn't a VALID Private IP Address. Try Again...")    
                        except ValueError:
                            print("OOPS! That wasn't a VALID Private IP Address. Try Again...")   
                    
                IP_ADDRESS = Get_IP()

                obj = []
                obj_grp = []
                matched_obj_initial = []
                custom_obj = []
                ALL_Policies = []
                matched_Policies = []

                print("\nInitiating Process To Find Matching Policies....")

                if IP_ADDRESS == 'all':
                    for policy in results['facts']: 
                        ALL_Policies.append(results['facts'][policy]['abcd'])
                else:    
                    print("\n1)CHECKING FOR MATCHING IP OBJECTS\n")
                    for ip in tqdm(range(len(results1['facts']['ipmask']['def']))):
                        if IP_ADDRESS == results1['facts']['ipmask']['def'][ip]['IP']:
                            obj.append(results1['facts']['ipmask']['def'][ip]['ADDRESS_NAME'])
                            matched_obj_initial.append(results1['facts']['ipmask']['def'][ip])

                    def find_IPs_range(range1):
                        range_IPs = []
                        for r1 in range(len(results1['facts']['iprange']['def'])):
                            if range1 == results1['facts']['iprange']['def'][r1]['ADDRESS_NAME']:
                                import ipaddress
                                start_ip = int(ipaddress.IPv4Address(results1['facts']['iprange']['def'][r1]['START_IP']))
                                end_ip = int(ipaddress.IPv4Address(results1['facts']['iprange']['def'][r1]['END_IP']))
                                for ip_int in range(int(start_ip), int(end_ip)+1):
                                    range_IPs.append(str(ipaddress.IPv4Address(ip_int)))
                        # pprint(range_IPs)
                        # print('===============range_IPs=======')
                        return(range_IPs)

                    rn = re.compile(f'^{IP_ADDRESS}$')
                    
                    for ip10 in tqdm(range(len(results1['facts']['iprange']['def']))):   
                        ip11 = find_IPs_range(results1['facts']['iprange']['def'][ip10]['ADDRESS_NAME'])
                        if list(filter(rn.match,ip11)):
                            obj.append(results1['facts']['iprange']['def'][ip10]['ADDRESS_NAME'])   

                    obj = obj + custom_obj

                    if not obj:
                        print(Fore.RED +"\nNO MATCHING OBJECTS FOUND") 
                        print("\nNO MATCHING POLICIES FOUND") 
                        print(Style.RESET_ALL)
                    else:
                        print(Fore.GREEN +f"\nFOUND {len(obj)} MATCHING IP OBJECTS {obj}")
                        print(Style.RESET_ALL)

                        print("\n2)CHECKING FOR MATCHING IP GROUP\n")
                        for obj_grp1 in tqdm(list(results2['facts'].keys())):
                            for obj_grp2 in range(len(shlex.split(results2['facts'][obj_grp1]['xyz']['MEMBER_OBJ'][0],posix=False))):
                                for obj_grp3 in obj:
                                    if obj_grp3 == shlex.split(results2['facts'][obj_grp1]['xyz']['MEMBER_OBJ'][0],posix=False)[obj_grp2]:
                                        obj_grp.append(obj_grp1)
                        if not obj_grp:
                            print(Fore.RED +"\nNO MATCHING OBJECT GROUP FOUND") 
                            print(Style.RESET_ALL)  
                        else:
                            print(Fore.GREEN +f"\nFOUND {len(obj_grp)} MATCHING IP OBJECT GROUPS {obj_grp}")
                            print(Style.RESET_ALL)
                        obj_list = obj + obj_grp    

                        print("\n3)CHECKING FOR MATCHING POLICIES\n")
                        
                        for each_obj in tqdm(obj_list):
                            for policy in results['facts']:
                                r = re.compile(f'^{each_obj}$')
                                if (list(filter(r.match,shlex.split(results['facts'][policy]['abcd']['DSTADDR'][0],posix=False)))):
                                    matched_Policies.append(results['facts'][policy]['abcd'])
                                elif (list(filter(r.match,shlex.split(results['facts'][policy]['abcd']['SRCADDR'][0],posix=False)))):
                                    matched_Policies.append(results['facts'][policy]['abcd'])
                                else:
                                    pass
                        # pprint(obj_list) 
                if ALL_Policies:
                    matched_Policies = []
                    matched_Policies = matched_Policies + ALL_Policies

                #import ipdb;ipdb.set_trace()

                print(Fore.GREEN +f"\nFOUND {len(matched_Policies)} MATCHING POLICIES")
                print(Style.RESET_ALL)

                print("\n4)CHECKING FOR MATCHING OBJECTS AND GROUPS IN POLICIES\n")

                def Split_Obj_Grp(lists):
                    grps = []
                    objects1 = []
                    grp_names = []
                    grp_names = list(results2['facts'].keys())
                    for m in lists:
                        r = re.compile(f'^{m}$')
                        if (list(filter(r.match,grp_names))):
                            grps.append(m)
                        else:
                            objects1.append(m)    
                    return(grps,objects1)   

                def find_obj(lists):
                    objs = []
                    objsonly = []
                    for m in lists: 
                        for no in results2['facts']:
                            if m == no:
                                for o in range(len(shlex.split(results2['facts'][no]['xyz']['MEMBER_OBJ'][0],posix=False))):
                                    objs.append(shlex.split(results2['facts'][no]['xyz']['MEMBER_OBJ'][0],posix=False)[o])
                    return(objs)    

                def Extracting_IPs_From_Objs(list1):
                    groups,objects = Split_Obj_Grp(list1)
                    while len(groups) != 0:
                        list2 = find_obj(groups)
                        groups1,objects1 = Split_Obj_Grp(list2)
                        groups = groups1
                        if type(objects1) == list:
                            for j in objects1:
                                objects.append(j)
                        else:
                            objects.append(objects1)
                    IPs = find_IPs_obj(objects)     
                    return(IPs)        

                def find_IPs_obj(lists):
                    obj_IPs = []
                    for e in lists:
                        for f in results1['facts']:
                            for g in range(len(results1['facts'][f]['def'])):
                                if results1['facts'][f]['def'][g]['ADDRESS_NAME'] == e:
                                    if f == 'ipmask':
                                        mask = results1['facts'][f]['def'][g]['MASK']
                                        CIDR = IPv4Network('0.0.0.0/'+mask).prefixlen
                                        obj_IPs.append(results1['facts'][f]['def'][g]['IP']+'/'+str(CIDR))
                                    if f == 'iprange':
                                        start_ip = results1['facts']['iprange']['def'][g]['START_IP']
                                        end_ip = results1['facts']['iprange']['def'][g]['END_IP']
                                        obj_IPs.append(start_ip+'-'+end_ip)
                    return(obj_IPs)

                final_src = []
                for f in range(len(matched_Policies)):
                    IPs1 = Extracting_IPs_From_Objs(shlex.split(matched_Policies[f]['SRCADDR'][0],posix=False))
                    matched_Policies[f]['SRCADDR_IP'] = IPs1
                    
                final_dst = []
                for g1 in range(len(matched_Policies)):
                    IPs2 = Extracting_IPs_From_Objs(shlex.split(matched_Policies[g1]['DSTADDR'][0],posix=False))
                    matched_Policies[g1]['DSTADDR_IP'] = IPs2
                        
                def Split_Serv_Grps_Objs(lists):
                    ser_grps1 = []
                    service1_objs = []
                    grp_names1 = []
                    grp_names1 = list(results4['facts'].keys())
                    for m in lists:
                        r = re.compile(f'^{m}$')
                        if (list(filter(r.match,grp_names1))):
                            ser_grps1.append(m)
                        else:
                            service1_objs.append(m)    
                    return(ser_grps1,service1_objs)   

                def Get_Objs_From_Grps(lists):
                    ser_objs = []
                    for m in lists:
                        for n in results4['facts']:
                            if m == n:
                                for o in range(len(shlex.split(results4['facts'][n]['DEF']['SER_OBJ_MEMBERS'][0],posix=False))):
                                    ser_objs.append(shlex.split(results4['facts'][n]['DEF']['SER_OBJ_MEMBERS'][0],posix=False)[o])
                    return(ser_objs)

                def Get_Ports_From_Objs(lists):
                    ports_list = []
                    for e in lists:
                        for f in results3['facts']:
                            if e == f:
                                ser_obj_keys = list(results3['facts'][f]['RST'].keys())
                                r1 = re.compile('^TCP_PORTRANGE$')
                                r2 = re.compile('^UDP_PORTRANGE$')
                                if (list(filter(r1.match,ser_obj_keys))):
                                    ports_list.append("tcp-"+results3['facts'][f]['RST']['TCP_PORTRANGE'][0])
                                elif (list(filter(r2.match,ser_obj_keys))):
                                    ports_list.append("udp-"+results3['facts'][f]['RST']['UDP_PORTRANGE'][0])
                                else:
                                    pass
                    return(ports_list)

                def Extracting_IPs_From_Objs(list1):
                    ser_groups,ser_objects = Split_Serv_Grps_Objs(list1)
                    while len(ser_groups) != 0:
                        list3 = Get_Objs_From_Grps(ser_groups)
                        ser_groups1,ser_objects1 = Split_Serv_Grps_Objs(list3)
                        ser_groups = ser_groups1
                        if type(ser_objects1) == list:
                            for j1 in ser_objects1:
                                ser_objects.append(j1)
                        else:
                            ser_objects.append(ser_objects1)
                    ser_objects2 = Get_Ports_From_Objs(ser_objects)
                    return(ser_objects2)   

                final_objs = []
                for h1 in range(len(matched_Policies)):
                    objs1 = Extracting_IPs_From_Objs(shlex.split(matched_Policies[h1]['SERVICE'][0],posix=False))
                    matched_Policies[h1]['SERVICE_PORTS'] = objs1     

                print(Fore.GREEN +f"Starting to Export Matched Policies to CSV")
                print(Style.RESET_ALL)
             
                
                # pprint(matched_Policies)
                print("=====================done=================")

                if matched_Policies:
                    keys = matched_Policies[0].keys()     
                    basename = "policies_"+IP_ADDRESS+"_"
                    middlename = datetime.datetime.now().strftime("%y%m%d")
                    suffix = ".csv"  
                    filename = basename+middlename+suffix
                    
                    response = HttpResponse(content_type='text/csv')
                    response['content-Disposition'] = 'attachment;filename="'+filename +'"'

                    
                    dict_writer = csv.DictWriter(response, keys)
                    dict_writer.writeheader()
                    dict_writer.writerows(matched_Policies)
                    print(Fore.GREEN +f"Completed Exporting Policies to CSV {filename}")
                    print(Style.RESET_ALL)
                    
                    return response
                else:
                    print(Fore.GREEN +f"NO POLICIES TO EXPORT")
                    print(Style.RESET_ALL)  
                    return render(request,'Firewall/home.html')


                # return  export_download_firewall(matched_Policies,IP_ADDRESS)



                # return render(request,'Firewall/home.html')
            
            
            else:
                My_IP_ADDRESS = request.POST.get("ipaddress")
                print(My_IP_ADDRESS,'=========My_IP_ADDRESS=========')
                sheet = request.FILES.get('customFile')
                a = str(sheet.read(),'UTF-8')
                # pprint(Data)

                b= get_test_template()
                c= get_test1_template()
                d= get_test2_template()
                e= get_test3_template()
                f= get_test4_template()
                
                #### EXTRACTING POLICY FROM CONFIG FILE #######
                results = {}

                parser = ttp(data=a, template=b)
                parser.parse()

                results['facts'] = parser.result()[0][0]

                # pprint(results)

                #### EXTRACTING IP OBJ FROM CONFIG FILE #######
                results1 = {}

                parser1 = ttp(data=a, template=c)
                parser1.parse()

                results1['facts'] = parser1.result()[0][0]

                #### EXTRACTING IP GRP FROM CONFIG FILE #######
                results2 = {}

                parser2 = ttp(data=a, template=d)
                parser2.parse()

                results2['facts'] = parser2.result()[0][0]

                #### EXTRACTING SERVICE OBJ FROM CONFIG FILE #######
                results3 = {}

                parser3 = ttp(data=a, template=e)
                parser3.parse()

                results3['facts'] = parser3.result()[0][0]

                #### EXTRACTING SERVICE GRP FROM CONFIG FILE #######
                results4 = {}

                parser4 = ttp(data=a, template=f)
                parser4.parse()

                results4['facts'] = parser4.result()[0][0]

                def Get_IP (): 
                    while True:
                        try:
                            IP_ADDRESS = My_IP_ADDRESS
                            # IP_ADDRESS= input("PLEASE ENTER A VALID PRIVATE IP ADDRESS [eg: 192.168.0.1]: ") '192.168.0.6'
                            if IP_ADDRESS == 'all':
                                return(IP_ADDRESS) 
                            elif IPv4Address(IP_ADDRESS).is_private:
                                return(IP_ADDRESS) 
                            else:
                                print("OOPS! That wasn't a VALID Private IP Address. Try Again...")    
                        except ValueError:
                            print("OOPS! That wasn't a VALID Private IP Address. Try Again...")   
                    
                IP_ADDRESS = Get_IP()

                obj = []
                obj_grp = []
                matched_obj_initial = []
                custom_obj = []
                ALL_Policies = []
                matched_Policies = []

                print("\nInitiating Process To Find Matching Policies....")

                if IP_ADDRESS == 'all':
                    for policy in results['facts']: 
                        ALL_Policies.append(results['facts'][policy]['abcd'])
                else:    
                    print("\n1)CHECKING FOR MATCHING IP OBJECTS\n")
                    for ip in tqdm(range(len(results1['facts']['ipmask']['def']))):
                        if IP_ADDRESS == results1['facts']['ipmask']['def'][ip]['IP']:
                            obj.append(results1['facts']['ipmask']['def'][ip]['ADDRESS_NAME'])
                            matched_obj_initial.append(results1['facts']['ipmask']['def'][ip])

                    def find_IPs_range(range1):
                        range_IPs = []
                        for r1 in range(len(results1['facts']['iprange']['def'])):
                            if range1 == results1['facts']['iprange']['def'][r1]['ADDRESS_NAME']:
                                import ipaddress
                                start_ip = int(ipaddress.IPv4Address(results1['facts']['iprange']['def'][r1]['START_IP']))
                                end_ip = int(ipaddress.IPv4Address(results1['facts']['iprange']['def'][r1]['END_IP']))
                                for ip_int in range(int(start_ip), int(end_ip)+1):
                                    range_IPs.append(str(ipaddress.IPv4Address(ip_int)))
                        # pprint(range_IPs)
                        # print('===============range_IPs=======')
                        return(range_IPs)

                    rn = re.compile(f'^{IP_ADDRESS}$')

                    for ip10 in tqdm(range(len(results1['facts']['iprange']['def']))):   
                        ip11 = find_IPs_range(results1['facts']['iprange']['def'][ip10]['ADDRESS_NAME'])
                        if list(filter(rn.match,ip11)):
                            obj.append(results1['facts']['iprange']['def'][ip10]['ADDRESS_NAME'])   

                    obj = obj + custom_obj

                    if not obj:
                        print(Fore.RED +"\nNO MATCHING OBJECTS FOUND") 
                        print("\nNO MATCHING POLICIES FOUND") 
                        print(Style.RESET_ALL)
                    else:
                        print(Fore.GREEN +f"\nFOUND {len(obj)} MATCHING IP OBJECTS {obj}")
                        print(Style.RESET_ALL)

                        print("\n2)CHECKING FOR MATCHING IP GROUP\n")
                        for obj_grp1 in tqdm(list(results2['facts'].keys())):
                            for obj_grp2 in range(len(shlex.split(results2['facts'][obj_grp1]['xyz']['MEMBER_OBJ'][0],posix=False))):
                                for obj_grp3 in obj:
                                    if obj_grp3 == shlex.split(results2['facts'][obj_grp1]['xyz']['MEMBER_OBJ'][0],posix=False)[obj_grp2]:
                                        obj_grp.append(obj_grp1)
                        if not obj_grp:
                            print(Fore.RED +"\nNO MATCHING OBJECT GROUP FOUND") 
                            print(Style.RESET_ALL)  
                        else:
                            print(Fore.GREEN +f"\nFOUND {len(obj_grp)} MATCHING IP OBJECT GROUPS {obj_grp}")
                            print(Style.RESET_ALL)
                        obj_list = obj + obj_grp    

                        print("\n3)CHECKING FOR MATCHING POLICIES\n")

                        for each_obj in tqdm(obj_list):
                            for policy in results['facts']:
                                r = re.compile(f'^{each_obj}$')
                                if (list(filter(r.match,shlex.split(results['facts'][policy]['abcd']['DSTADDR'][0],posix=False)))):
                                    matched_Policies.append(results['facts'][policy]['abcd'])
                                elif (list(filter(r.match,shlex.split(results['facts'][policy]['abcd']['SRCADDR'][0],posix=False)))):
                                    matched_Policies.append(results['facts'][policy]['abcd'])
                                else:
                                    pass
                        # pprint(obj_list) 
                if ALL_Policies:
                    matched_Policies = []
                    matched_Policies = matched_Policies + ALL_Policies
                
                print(Fore.GREEN +f"\nFOUND {len(matched_Policies)} MATCHING POLICIES")
                print(Style.RESET_ALL)

                print("\n4)CHECKING FOR MATCHING OBJECTS AND GROUPS IN POLICIES\n")

                def Split_Obj_Grp(lists):
                    grps = []
                    objects1 = []
                    grp_names = []
                    grp_names = list(results2['facts'].keys())
                    for m in lists:
                        r = re.compile(f'^{m}$')
                        if (list(filter(r.match,grp_names))):
                            grps.append(m)
                        else:
                            objects1.append(m)    
                    return(grps,objects1)   

                def find_obj(lists):
                    objs = []
                    objsonly = []
                    for m in lists: 
                        for no in results2['facts']:
                            if m == no:
                                for o in range(len(shlex.split(results2['facts'][no]['xyz']['MEMBER_OBJ'][0],posix=False))):
                                    objs.append(shlex.split(results2['facts'][no]['xyz']['MEMBER_OBJ'][0],posix=False)[o])
                    return(objs)    

                def Extracting_IPs_From_Objs(list1):
                    groups,objects = Split_Obj_Grp(list1)
                    while len(groups) != 0:
                        list2 = find_obj(groups)
                        groups1,objects1 = Split_Obj_Grp(list2)
                        groups = groups1
                        if type(objects1) == list:
                            for j in objects1:
                                objects.append(j)
                        else:
                            objects.append(objects1)
                    IPs = find_IPs_obj(objects)     
                    return(IPs) 

                def find_IPs_obj(lists):
                    obj_IPs = []
                    for e in lists:
                        for f in results1['facts']:
                            for g in range(len(results1['facts'][f]['def'])):
                                if results1['facts'][f]['def'][g]['ADDRESS_NAME'] == e:
                                    if f == 'ipmask':
                                        mask = results1['facts'][f]['def'][g]['MASK']
                                        CIDR = IPv4Network('0.0.0.0/'+mask).prefixlen
                                        obj_IPs.append(results1['facts'][f]['def'][g]['IP']+'/'+str(CIDR))
                                    if f == 'iprange':
                                        start_ip = results1['facts']['iprange']['def'][g]['START_IP']
                                        end_ip = results1['facts']['iprange']['def'][g]['END_IP']
                                        obj_IPs.append(start_ip+'-'+end_ip)
                    return(obj_IPs)

                final_src = []
                for f in range(len(matched_Policies)):
                    IPs1 = Extracting_IPs_From_Objs(shlex.split(matched_Policies[f]['SRCADDR'][0],posix=False))
                    matched_Policies[f]['SRCADDR_IP'] = IPs1
                    
                final_dst = []
                for g1 in range(len(matched_Policies)):
                    IPs2 = Extracting_IPs_From_Objs(shlex.split(matched_Policies[g1]['DSTADDR'][0],posix=False))
                    matched_Policies[g1]['DSTADDR_IP'] = IPs2
                        
                def Split_Serv_Grps_Objs(lists):
                    ser_grps1 = []
                    service1_objs = []
                    grp_names1 = []
                    grp_names1 = list(results4['facts'].keys())
                    for m in lists:
                        r = re.compile(f'^{m}$')
                        if (list(filter(r.match,grp_names1))):
                            ser_grps1.append(m)
                        else:
                            service1_objs.append(m)    
                    return(ser_grps1,service1_objs)  

                def Get_Objs_From_Grps(lists):
                    ser_objs = []
                    for m in lists:
                        for n in results4['facts']:
                            if m == n:
                                for o in range(len(shlex.split(results4['facts'][n]['DEF']['SER_OBJ_MEMBERS'][0],posix=False))):
                                    ser_objs.append(shlex.split(results4['facts'][n]['DEF']['SER_OBJ_MEMBERS'][0],posix=False)[o])
                    return(ser_objs)

                def Get_Ports_From_Objs(lists):
                    ports_list = []
                    for e in lists:
                        for f in results3['facts']:
                            if e == f:
                                ser_obj_keys = list(results3['facts'][f]['RST'].keys())
                                r1 = re.compile('^TCP_PORTRANGE$')
                                r2 = re.compile('^UDP_PORTRANGE$')
                                if (list(filter(r1.match,ser_obj_keys))):
                                    ports_list.append("tcp-"+results3['facts'][f]['RST']['TCP_PORTRANGE'][0])
                                elif (list(filter(r2.match,ser_obj_keys))):
                                    ports_list.append("udp-"+results3['facts'][f]['RST']['UDP_PORTRANGE'][0])
                                else:
                                    pass
                    return(ports_list)  

                def Extracting_IPs_From_Objs(list1):
                    ser_groups,ser_objects = Split_Serv_Grps_Objs(list1)
                    while len(ser_groups) != 0:
                        list3 = Get_Objs_From_Grps(ser_groups)
                        ser_groups1,ser_objects1 = Split_Serv_Grps_Objs(list3)
                        ser_groups = ser_groups1
                        if type(ser_objects1) == list:
                            for j1 in ser_objects1:
                                ser_objects.append(j1)
                        else:
                            ser_objects.append(ser_objects1)
                    ser_objects2 = Get_Ports_From_Objs(ser_objects)
                    return(ser_objects2)   

                final_objs = []
                for h1 in range(len(matched_Policies)):
                    objs1 = Extracting_IPs_From_Objs(shlex.split(matched_Policies[h1]['SERVICE'][0],posix=False))
                    matched_Policies[h1]['SERVICE_PORTS'] = objs1     

                print(Fore.GREEN +f"Starting to Export Matched Policies to CSV")
                print(Style.RESET_ALL) 

                print("=====================done=================")

                if matched_Policies:
                    keys = matched_Policies[0].keys()     
                    basename = "policies_"+IP_ADDRESS+"_"
                    middlename = datetime.datetime.now().strftime("%y%m%d")
                    suffix = ".csv"  
                    filename = basename+middlename+suffix
                    
                    response = HttpResponse(content_type='text/csv')
                    response['content-Disposition'] = 'attachment;filename="'+filename +'"'

                    
                    dict_writer = csv.DictWriter(response, keys)
                    dict_writer.writeheader()
                    dict_writer.writerows(matched_Policies)
                    print(Fore.GREEN +f"Completed Exporting Policies to CSV {filename}")
                    print(Style.RESET_ALL)
                    
                    return response
                else:
                    print(Fore.GREEN +f"NO POLICIES TO EXPORT")
                    print(Style.RESET_ALL)  
                    return render(request,'Firewall/home.html')

                return render(request,'Firewall/home.html')

