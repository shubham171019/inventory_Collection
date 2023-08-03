import re
import http
import json
import csv
from django.shortcuts import render,redirect


from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse, response
from netmiko import ConnectHandler
from pprint import pprint
from django.contrib import messages


# import logging
# logger = logging.getLogger('django')

def get_switch_spanning_1():
        with open("Allfiles/spanning_tree/spanning.txt") as f:
            output_list= f.read().splitlines()
            return output_list

def get_switch_spanning_2():
        with open("Allfiles/spanning_tree/sw2.txt") as f:
            output_list= f.read().splitlines()
            return output_list

def get_switch_spanning_3():
        with open("Allfiles/spanning_tree/tor_sw.txt") as f:
            data_to_send= f.read().splitlines()
            return data_to_send

# Files should be added in All Files SFP
def get_data_sfp(): 
    with open("Allfiles/SFP/mysfp.txt") as f:
        get_output_data = f.read() 
        return get_output_data 

def get_data_inv():
    with open("Allfiles/INV/myInv.txt") as f:
        get_output_data = f.read() 
        return get_output_data 

###Inventory collection




class HomePageView(TemplateView):
    def get(self,request):
        data_resp ={}
        # logger.info("$$$$  LOGGER IS WORKING  $$$$$$")
        print("get====================")
        return render(request,'demo.html',data_resp)

    def post(self,request):
        data_resp ={}
        print("post")

        if request.POST.get("hiddenJson")!= '{"": {}}':
            print("yes")
            if 'exportExcel' in request.POST:
                myact = request.POST.get("myact")
                new_dict = json.loads(request.POST.get("hiddenJson"))
                

                if myact == "Spanning Tree Protocol":
                    new_dict,lspl =  self.mydataspanning(request,myact,new_dict)
                    return export_download_spanning(new_dict,lspl)
                    
                elif myact == "SFP":
                    new_dict =  self.mydataSFP(request,myact,new_dict)
                    return export_download_sfp(new_dict)

                elif myact == "Inventory Collection":
                    new_dict,sfp_speed =  self.mydataInventory(request,myact,new_dict)
                    return export_download_INV(new_dict)

            if 'exportJson' in request.POST:
                
                myact = request.POST.get("myact")
                print(myact,'=========================myact === json')
                new_dict =  json.loads(request.POST.get("hiddenJson"))

                if myact == "Spanning Tree Protocol":
                    new_dict,lspl =  self.mydataspanning(request,myact,new_dict)
                    return export_json(new_dict,myact)
                elif myact == "SFP":
                    new_dict =  self.mydataSFP(request,myact,new_dict)
                    return export_json(new_dict,myact )
                elif myact == "Inventory Collection":
                    new_dict =  self.mydataInventory(request,myact,new_dict)
                    return export_json(new_dict,myact )

            if 'display' in request.POST:    

                myact = request.POST.get("myact")
                print(myact,'=========================myact === display')
                new_dict =  json.loads(request.POST.get("hiddenJson"))

                if myact == "Spanning Tree Protocol":
                    new_dict,lspl =  self.mydataspanning(request,myact,new_dict)
                    return render(request,'demo.html',{
                        'new_dict': new_dict,
                        'lspl' :lspl
                    })
                elif myact == "SFP":
                    spf_dict =  self.mydataSFP(request,myact,new_dict)
                    return render(request,'demo.html',{
                        'spf_dict': spf_dict
                    })
                elif myact == "Inventory Collection":
                    INV_dict,sfp_speed =  self.mydataInventory(request,myact,new_dict)
                    return render(request,'demo.html',{
                        'INV_dict': INV_dict,
                        'sfp_speed':sfp_speed
                    })

            return render(request,'demo.html',data_resp)
        else:
            print("no")
            return render(request,'demo.html',messages.success(request, 'Please provide Input.', 'alert-danger'))


    def mydataspanning(self,request,myact,new_dict):
        print(myact,'===============myexportExcelfunc==============')


        for k,v in new_dict.items(): 
            if new_dict[k]['device_make'] == "Cisco": 
                device = ConnectHandler(device_type='cisco_nxos', ip=k, username=new_dict[k]["username"], password=new_dict[k]["password"]) 
                print(device,'=========device')
                chk = device.send_command("show spanning-tree")

                print('chk==========',type(chk))

                new_list = list(chk.split("\n"))

                my_list = [] 
                for item in chk: 
                    my_list.append([m for m in item.split(" ") if m.strip()]) 

                pprint(my_list)

                lspl = []
                Vlan_list = []

                for item in my_list:
                    for i in item:        
                        if i.startswith("VLAN"):
                            Vlan_list.append(i)
                            lspl.append([])
                            get_vlan = i                   
                        else:
                            lspl[-1].append(get_vlan)
                            lspl[-1].append(i)
                            get_vlan = ""

                print(Vlan_list)

                for terms in lspl:
                    new_dict[k][terms[0]]= {}


                for terms in lspl:
                    new_dict[k][terms[0]]['Root_Bridge'] = False
                    new_dict[k][terms[0]]['Cost'] =""
                    new_dict[k][terms[0]]['Root_ID'] = ""
                    new_dict[k][terms[0]]['Bridge_ID'] = ""
                    new_dict[k][terms[0]]['Root_MAC_address'] = ""
                    new_dict[k][terms[0]]['Bridge_MAC_address'] = ""

                    new_dict[k][terms[0]]['Root_Ports']= ""
                    new_dict[k][terms[0]]['Desg_Ports']= ""
                    new_dict[k][terms[0]]['Forwarding_Ports'] = ""
                    new_dict[k][terms[0]]['Blocking_Ports'] = ""

                    new_dict[k][terms[0]]['No_of_Root_Ports']= ""
                    new_dict[k][terms[0]]['Desginated_Ports']= ""
                    new_dict[k][terms[0]]['No_of_Forwarding_Ports'] = "" 
                    new_dict[k][terms[0]]['No_of_Blocking_Ports'] = "" 

                    new_dict[k][terms[0]]['Total_ports'] = "" 

                for terms in lspl: 
                    Cost = [i for i,x in enumerate(terms) if x == "Cost"]
                    if len(Cost) == 1:
                        new_dict[k][terms[0]]['Cost'] = "Root"
                        new_dict[k][terms[0]]['Root_Bridge'] = True
                    else:
                        cost_of = [i for i,x in enumerate(terms) if x == "Cost"][0]
                        new_dict[k][terms[0]]['Cost'] = terms[cost_of+2]


                    Root_ID = terms.index("Root")
                    if Root_ID:
                        new_dict[k][terms[0]]['Root_ID']= terms[Root_ID+6]

                    Bridge_ID = terms.index("Bridge")
                    if Bridge_ID:
                        new_dict[k][terms[0]]['Bridge_ID']= terms[Bridge_ID+6]



                    MAC_address = [i for i,x in enumerate(terms) if x == "Address"]
                    if MAC_address:
                        new_dict[k][terms[0]]['Root_MAC_address']= terms[MAC_address[0]+2]
                        new_dict[k][terms[0]]['Bridge_MAC_address']= terms[MAC_address[1]+2]


                    root_port = [i for i,x in enumerate(terms) if x == "Root"]
                    if root_port:
                        root = []
                        for index in root_port:
                            root.append(terms[index-2])
                        new_dict[k][terms[0]]['Root_Ports'] = str(root[1:])
                        new_dict[k][terms[0]]['No_of_Root_Ports'] = str(len(root)-1)


                    forwarding_indices = [i for i,x in enumerate(terms) if x == "FWD"]
                    forwarding_ports = []
                    for index in forwarding_indices:
                        forwarding_ports.append(terms[index-4])
                    new_dict[k][terms[0]]['Forwarding_Ports'] = str(forwarding_ports)
                    new_dict[k][terms[0]]['No_of_Forwarding_Ports'] = str(len(forwarding_ports))


                    blocking_indices = [i for i,x in enumerate(terms) if x == "BLK"]
                    blocking_ports = []
                    for index in blocking_indices:
                        blocking_ports.append(terms[index-4])
                    new_dict[k][terms[0]]['Blocking_Ports'] = str(blocking_ports)
                    new_dict[k][terms[0]]['No_of_Blocking_Ports'] = str(len(blocking_ports))


                    desg_indices = [i for i,x in enumerate(terms) if x == "Desg"]
                    desg = []
                    for index in desg_indices:
                        desg.append(terms[index-2])
                    new_dict[k][terms[0]]['Desg_Ports']= str(desg)
                    new_dict[k][terms[0]]['Desginated_Ports'] = len(desg_indices)

                    new_dict[k][terms[0]]['Total_ports'] = str(len(forwarding_ports)+len(blocking_ports)) 

        # print(new_dict)  

        return  new_dict,lspl 
        
       
    def mydataSFP(self,request,myact,new_dict):

        for k,v in new_dict.items():
            new_dict[k]['SPF_connected_status'] =""
            new_dict[k]['speed'] =""
            new_dict[k]['ports_successfully'] =""
            new_dict[k]['SPF_unconnected_status'] =""
            new_dict[k]['ports_unsuccessfully'] =""
            new_dict[k]['Total'] =""

        
        for key,v in new_dict.items(): 
            if new_dict[key]['device_make'] == "Cisco": 
                device = ConnectHandler(device_type='cisco_nxos', ip=key, username=new_dict[key]["username"], password=new_dict[key]["password"]) 
                output_list = device.send_command("sh interface status") 
                # output_list = get_data_sfp() 
                
                
                chk = [j for j in output_list.split('\n') if len(j)>0] 
        

                my_list = [] 
                for item in chk: 
                    my_list.append([m for m in item.split(" ") if m.strip()]) 

                first_list = [] 
                second_list =[] 
                unconnected_list = [] 
                connected_list = [] 
                for i in my_list: 
                    for o,j in enumerate(i): 
                        unconnected_list = [] 
                        connected_list = [] 
                        if j.startswith("Gi") or j.startswith("Eth") : 
                            if "connected" in i[len(i)-5] and ("10Gbase-SR" in i[len(i)-1] or "1000base-T" in i[len(i)-1] or "QSFP-40G-SR-BD" in i[len(i)-1]): 
                                connected_list.append(i[0]) 
                                connected_list.append(i[len(i)-5]) 
                                connected_list.append(i[len(i)-2]) 
                                connected_list.append(i[len(i)-1]) 
                                first_list.append(connected_list) 
                            else: 
                                unconnected_list.append(i[0]) 
                                unconnected_list.append(i[len(i)-5]) 
                                unconnected_list.append(i[len(i)-2]) 
                                unconnected_list.append(i[len(i)-1]) 
                                second_list.append(unconnected_list) 

                speed_list = [] 
                for items in first_list: 
                    speed_list.append(items[-2]) 

                res = {} 
                for i in speed_list: 
                    res[i] = speed_list.count(i) 

                disabled_list = [] 
                for items in second_list: 
                    if items[-1] != "--": 
                        disabled_list.append(items[-1]) 

                port_list = [] 
                for items in first_list: 
                    port_list.append(items[0]) 


                unport_list = [] 
                for items in second_list: 
                    unport_list.append(items[0]) 

                new_dict[key]['SPF_connected_status'] = str(port_list) 
                new_dict[key]['ports_successfully'] = str(len(first_list))+"/"+str(len(first_list)+len(second_list)) 
                new_dict[key]['SPF_unconnected_status'] = str(len(disabled_list))+"/"+str(len(second_list)) 
                new_dict[key]['ports_unsuccessfully'] = str(unport_list) 
                new_dict[key]['speed'] = str(res) 
                new_dict[key]['Total'] = str(len(first_list)+len(second_list))

            else: 
                pass 

            pprint(new_dict)
            print("===============sfp")

            return new_dict

           
            
            

    def mydataInventory(self,request,myact,new_dict):

        print(new_dict,'============inv')

        sfp_speed = ['GE T','GE LX','10GBASE-SR/SW','SFP+ 10GBASE-LR'
            ,'10Gbase-SR','1000base-T','40GBASE-BXSR','100GBASE-BXSR',
            '1000base-SX','GLC-TE','GLC-LH-SMD','GLC-SX-MMD',
            'SFP-10G-LR-S','SFP-10G-SR','SFP-10G-SR-S','SFP28-25G-BASE-SR',
            'SFP+-10G-USR','SFP+-10G-SR','XFP-10G-MM-SR','QSFP-40G-SR-BD',
            'SFP-H25GB-SR','JUNIPER SFP-H25GB-SR','JUNIPER 10G BXSR','JUNIPER 40G BXSR']



        for k,v in new_dict.items(): 
           
            new_dict[k]['Device_Model']= ""
            new_dict[k]['S_No']= ""
            new_dict[k]['used']= {}
            new_dict[k]['unused']= {}

        for k,v in new_dict.items():     
            for speed in sfp_speed:
                new_dict[k]['used'][speed]= 0
                new_dict[k]['unused'][speed]= 0
                
        for k,v in new_dict.items():  
            new_dict[k]['used']['Total_used'] = 0
            new_dict[k]['unused']['Total_unused']= 0


        for k,v in new_dict.items(): 
            # try:
            if new_dict[k]['device_make'] == "Cisco": 
                device = ConnectHandler(device_type='cisco_nxos', ip=k ,username=new_dict[k]["username"], password=new_dict[k]["password"]) 
                output_list = device.send_command("show inventory")


                # output_list = get_data_inv() 
                
                chk  =[ele for ele in output_list.split("\n") if len(ele)>0]
                print(chk,'====================chk',type(chk))



                mydevice = re.findall(r'"(.+?)"',chk[0])[-1]
                serial_no = [x for x in chk[1].split(":")][-1]

                new_dict[k]['Device_Model'] = mydevice
                new_dict[k]['S_No'] = serial_no.strip()

                output_cisco = device.send_command("show interface status") 


                # output_cisco = get_data_sfp() 

                chk_cisco= [j for j in output_cisco.split('\n') if len(j)>0] 

                print(chk_cisco,'chk_cisco',type(chk_cisco))


                my_list_cisco = [] 
                for item in chk_cisco: 
                    my_list_cisco.append([m for m in item.split(" ") if m.strip()]) 

                first_list = [] 
                second_list =[] 
                unconnected_list = [] 
                connected_list = [] 
                for i in my_list_cisco: 
                    for o,j in enumerate(i): 
                        unconnected_list = [] 
                        connected_list = [] 
                        if j.startswith("Gi") or j.startswith("Eth") : 
                            if ("connected" in i[len(i)-5] or "channelDo" in i[len(i)-5]) and ("--" not in i[len(i)-1]): 
                            # if ("connected" in i[len(i)-5] or "channelDo" in i[len(i)-5]) and ("10Gbase-SR" in i[len(i)-1] or "1000base-T" in i[len(i)-1] or "QSFP-40G-SR-BD" in i[len(i)-1]): 
                                connected_list.append(i[0]) 
                                connected_list.append(i[len(i)-5]) 
                                connected_list.append(i[len(i)-2]) 
                                connected_list.append(i[len(i)-1]) 
                                first_list.append(connected_list) 
                            else: 
                                unconnected_list.append(i[0]) 
                                unconnected_list.append(i[len(i)-5]) 
                                unconnected_list.append(i[len(i)-2]) 
                                unconnected_list.append(i[len(i)-1]) 
                                second_list.append(unconnected_list) 

                speed_list = []     
                for items in first_list: 
                    speed_list.append(items[-1]) 

                for speed in speed_list:
                    new_dict[k]['used'][speed]= speed_list.count(speed) 

                disables_speed = []
                for item in second_list:
                    if item[-1]!= "--":
                        disables_speed.append(item[-1])

                for speed in disables_speed:
                    new_dict[k]['unused'][speed] = disables_speed.count(speed) 

                new_dict[k]['used']['Total_used'] = len(speed_list)
                new_dict[k]['unused']['Total_unused']= len(disables_speed)

            pprint(new_dict)
            print("IM HERE====================")

            return new_dict,sfp_speed


            # except:
            #     pass

        # ++++++++++++++++++
        
     
def export_download_sfp(new_dict):
    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment;filename="SFP_tree.csv"'

    all_data = ['Ip_address','Ports working with SFP','Speed','Number of Ports working successfully with SFP',
    'Number of ports not working successfully with SFP','Ports Status unconnected/disabled/xcrv absent','Total']

    writer = csv.writer(response)

    writer.writerow(all_data)
    for key,value in new_dict.items(): 
        SPF_connected_status = new_dict[key]["SPF_connected_status"] 
        speed = new_dict[key]["speed"] 
        ports_successfully = new_dict[key]["ports_successfully"] 
        SPF_unconnected_status = new_dict[key]["SPF_unconnected_status"] 
        ports_unsuccessfully = new_dict[key]["ports_unsuccessfully"] 
        Total = new_dict[key]["Total"] 
        
        writer.writerow([key]+[SPF_connected_status]+[speed]+[ports_successfully]+ 
            [SPF_unconnected_status]+[ports_unsuccessfully]+[Total]) 

    return response


#spanning tree 
def export_download_spanning(new_dict,lspl):
    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment;filename="spanning_tree.csv"'

    all_data = ["Ip address","Vlan","Root Bridge","Cost","Root Priority","Bridge Priority",
        "Root Mac Address","Bridge Mac Address",
        "Root ports","Desg Ports","Forwarding Ports","Blocking Ports",
        "No of Root ports","No of Desg ports","No. of Forwarding Ports","No of Blocking ports",
        "Total Ports"] 
    writer = csv.writer(response)

    writer.writerow(all_data)

    for k,v in new_dict.items():
        for terms in lspl:
            writer.writerow([k]+[terms[0]]+
            [new_dict[k][terms[0]]['Root_Bridge']]+
            [new_dict[k][terms[0]]['Cost']]+
            [new_dict[k][terms[0]]['Root_ID']]+
            [new_dict[k][terms[0]]['Bridge_ID']]+
            [new_dict[k][terms[0]]['Root_MAC_address']]+
            [new_dict[k][terms[0]]['Bridge_MAC_address']]+

            [new_dict[k][terms[0]]['Root_Ports']]+
            [new_dict[k][terms[0]]['Desg_Ports']]+       
            [new_dict[k][terms[0]]['Forwarding_Ports']]+
            [new_dict[k][terms[0]]['Blocking_Ports']]+

            [new_dict[k][terms[0]]['No_of_Root_Ports']]+
            [new_dict[k][terms[0]]['Desginated_Ports']]+
            [new_dict[k][terms[0]]['No_of_Forwarding_Ports']]+
            [new_dict[k][terms[0]]['No_of_Blocking_Ports']]+
            
            [new_dict[k][terms[0]]['Total_ports']])
    return response

def export_download_INV(new_dict):
    response = HttpResponse(content_type='text/csv')
    response['content-Disposition'] = 'attachment;filename="inv_collection.csv"'
    all_data = ['Make','Device Model','S.No','Ip address','Port used',
            'GE T','GE LX','10GBASE-SR/SW','SFP+ 10GBASE-LR',
            '10Gbase-SR','1000base-T','40GBASE-BXSR','100GBASE-BXSR',
            '1000base-SX','GLC-TE','GLC-LH-SMD','GLC-SX-MMD',
            'SFP-10G-LR-S','SFP-10G-SR','SFP-10G-SR-S','SFP28-25G-BASE-SR',
            'SFP+-10G-USR','SFP+-10G-SR','XFP-10G-MM-SR','QSFP-40G-SR-BD',
            'SFP-H25GB-SR','JUNIPER SFP-H25GB-SR','JUNIPER 10G BXSR','JUNIPER 40G BXSR',
            'Total']

    writer = csv.writer(response)
    writer.writerow(all_data)

    for key,value in new_dict.items(): 
        Make = new_dict[key]['device_make'] 
        Device_Model = new_dict[key]['Device_Model']
        S_no = new_dict[key]['S_No'] 
        Total_portused = "Connected"

        sfp1used = new_dict[key]['used']['GE T']
        sfp2used = new_dict[key]['used']['GE LX']
        sfp3used= new_dict[key]['used']['10GBASE-SR/SW']
        sfp4used = new_dict[key]['used']['SFP+ 10GBASE-LR']

        sfp6used = new_dict[key]['used']['10Gbase-SR']
        sfp7used = new_dict[key]['used']['1000base-T']
        sfp8used= new_dict[key]['used']['40GBASE-BXSR']
        sfp9used = new_dict[key]['used']['100GBASE-BXSR']
        sfp10used = new_dict[key]['used']['1000base-SX'] 

        sfp11used = new_dict[key]['used']['GLC-TE']
        sfp12used = new_dict[key]['used']['GLC-LH-SMD']
        sfp13used= new_dict[key]['used']['GLC-SX-MMD']
        sfp14used = new_dict[key]['used']['SFP-10G-LR-S'] 
        sfp15used = new_dict[key]['used']['SFP-10G-SR'] 

        sfp16used = new_dict[key]['used']['SFP-10G-SR-S']
        sfp17used = new_dict[key]['used']['SFP28-25G-BASE-SR']
        sfp18used= new_dict[key]['used']['SFP+-10G-USR']
        sfp19used = new_dict[key]['used']['SFP+-10G-SR']
        sfp20used = new_dict[key]['used']['XFP-10G-MM-SR'] 

        sfp21used = new_dict[key]['used']['QSFP-40G-SR-BD'] 
        sfp22used = new_dict[key]['used']['SFP-H25GB-SR'] 
        sfp23used = new_dict[key]['used']['JUNIPER SFP-H25GB-SR'] 
        sfp24used = new_dict[key]['used']['JUNIPER 10G BXSR'] 
        sfp25used = new_dict[key]['used']['JUNIPER 40G BXSR'] 

        sfp26used = new_dict[key]['used']['Total_used'] 

        writer.writerow([Make]+
            [Device_Model]+[S_no]+[key]+[Total_portused]+
            [sfp1used]+[sfp2used]+
            [sfp3used]+[sfp4used]+
            [sfp6used]+
            [sfp7used]+[sfp8used]+
            [sfp9used]+[sfp10used]+
            [sfp11used]+[sfp12used]+
            [sfp13used]+[sfp14used]+
            [sfp15used]+[sfp16used]+
            [sfp17used]+[sfp18used]+
            [sfp19used]+[sfp20used]+
            [sfp21used]+[sfp22used]+
            [sfp23used]+[sfp24used]+
            [sfp25used]+[sfp26used]
        )

        Make = new_dict[key]['device_make']
        Device_Model = new_dict[key]['Device_Model']
        S_no = new_dict[key]['S_No'] 
        Total_portused = "Unconnected"

        sfp1unused= new_dict[key]['unused']['GE T']
        sfp2unused = new_dict[key]['unused']['GE LX']
        sfp3unused =new_dict[key]['unused']['10GBASE-SR/SW']
        sfp4unused= new_dict[key]['unused']['SFP+ 10GBASE-LR']

        sfp6unused= new_dict[key]['unused']['10Gbase-SR']
        sfp7unused = new_dict[key]['unused']['1000base-T']
        sfp8unused =new_dict[key]['unused']['40GBASE-BXSR']
        sfp9unused= new_dict[key]['unused']['100GBASE-BXSR']
        sfp10unused = new_dict[key]['unused']['1000base-SX']

        sfp11unused= new_dict[key]['unused']['GLC-TE']
        sfp12unused = new_dict[key]['unused']['GLC-LH-SMD']
        sfp13unused =new_dict[key]['unused']['GLC-SX-MMD']
        sfp14unused= new_dict[key]['unused']['SFP-10G-LR-S']
        sfp15unused = new_dict[key]['unused']['SFP-10G-SR']

        sfp16unused= new_dict[key]['unused']['SFP-10G-SR-S']
        sfp17unused = new_dict[key]['unused']['SFP28-25G-BASE-SR']
        sfp18unused =new_dict[key]['unused']['SFP+-10G-USR']
        sfp19unused= new_dict[key]['unused']['SFP+-10G-SR']
        sfp20unused = new_dict[key]['unused']['XFP-10G-MM-SR']

        sfp21unused = new_dict[key]['unused']['QSFP-40G-SR-BD']
        sfp22unused = new_dict[key]['unused']['SFP-H25GB-SR']
        sfp23unused = new_dict[key]['unused']['JUNIPER SFP-H25GB-SR']
        sfp24unused = new_dict[key]['unused']['JUNIPER 10G BXSR']
        sfp25unused = new_dict[key]['unused']['JUNIPER 40G BXSR']
        sfp26unused = new_dict[key]['unused']['Total_unused']

        writer.writerow([Make]+[Device_Model]+[S_no]+[key]+[Total_portused]+
            [sfp1unused]+[sfp2unused]+
            [sfp3unused]+[sfp4unused]+
            [sfp6unused]+
            [sfp7unused]+[sfp8unused]+
            [sfp9unused]+[sfp10unused]+
            [sfp11unused]+[sfp12unused]+
            [sfp13unused]+[sfp14unused]+
            [sfp15unused]+[sfp16unused]+
            [sfp17unused]+[sfp18unused]+
            [sfp19unused]+[sfp20unused]+
            [sfp21unused]+[sfp22unused]+
            [sfp23unused]+[sfp24unused]+
            [sfp25unused]+[sfp26unused])

    print(new_dict,'============atexcel')
    return response


def export_json(new_dict,myact):
    json_object = json.dumps(new_dict, indent = 4) 
    content=json_object
    # print(content)
    response = HttpResponse(content, content_type='text/json')
    response['content-Disposition'] = 'attachment;filename="{}.json";'.format(myact)
    return response


def Ip_and_device_type(request):   
    mydata = request.POST.get("valuedict") 
    mydict = json.loads(mydata)
    Activity_type = request.POST.get("Activity_type")
    jsondata = json.dumps(mydict)

    return JsonResponse({'jsondata':jsondata,'Activity_type':Activity_type},safe=False)
