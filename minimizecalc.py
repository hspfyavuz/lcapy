import os
from PyPDF2 import PdfMerger
from ordered_set import OrderedSet
from lcapy import *
from lcapy import randomnetwork
from lcapy import circuit
from sys import *
import random

####################################
netarr=[]
subset_steps=[]
result=[]
combiningvar=[]
resultcompl=[]
####################################
 
def explain_dc_series_print(net,sublist,total,newname):
    
    solution=( newname +' = '+(sublist[0])+ ' + ' +(sublist[1])
          +'\n'+ '≙ ' + ((net.elements[sublist[0]].cpt.args[0]))+ ' + '+ ((net.elements[sublist[1]].cpt.args[0]))
          +'\n'+ newname + ' = ' + str(total))
           
    result.append(solution)

    
def explain_dc_parallel_print(net,sublist,total,newname):
    
    solution=( newname +' = ( '+(sublist[0])+ ' ⋅ ' +(sublist[1]) + ' ) / ( ' 
                      + (sublist[0])+ ' + ' +(sublist[1])+ ' )'
        + '\n' '≙ ( '+(net.elements[sublist[0]].cpt.args[0])+ ' ⋅ ' +(net.elements[sublist[1]].cpt.args[0]) + ' ) / ( ' 
                      + (net.elements[sublist[0]].cpt.args[0])+ ' + ' +(net.elements[sublist[1]].cpt.args[0])+ ' )'
        +'\n'+ newname + ' = ' + str(total))
    result.append(solution)
         

def explain_ac_series_print(net,sublist,total,newname):
    
    solution=( newname +' = '+(sublist[0])+ ' + ' +(sublist[1])
          +'\n'+ '≙ ( ' + ((net.elements[sublist[0]].cpt.args[0]))+ ' ) + ( '+ ((net.elements[sublist[1]].cpt.args[0])) +' )'
          +'\n'+ newname + ' = ' + str(total))
           
    result.append(solution)
    resultcompl.append(total)

         
def explain_ac_parallel_print(net,sublist,total,newname):
    
    solution=( newname +' = ( 1 / (( 1 / '+(sublist[0])+ ') + ( 1 / ' +(sublist[1]) + ' )) )'
        + '\n' '≙ ( 1 / (( 1 / '+(net.elements[sublist[0]].cpt.args[0])+ ') + ( 1 / ' +(net.elements[sublist[1]].cpt.args[0]) + ' )) )' 
        +'\n'+ newname + ' = ' + str(total))
    result.append(solution)
    resultcompl.append(total)
    
        
def result_print(name, result):
    
    #noch nicht funktionsfähig
    if name[0]=='R' or name[0]=='Z':
        print('≙ %s = %s Ω' % (name,result))
        print('__________')
    if name[0]=='C':
        print('≙ %s = %s F' % (name,result))
        print('__________')
    if name[0]=='L':
        print('≙ %s = %s H' % (name,result))
        print('__________')
    

def give_result(step):
    
    return result[step]

####################################
    
def save_net(net):
    
    netarr.append(net)


def give_net(netnumber):
    
    net=netarr[netnumber]
    return net
    

def give_net_length():
    
    return len(netarr)

####################################

def save_components(components):
    
    componentlist=list(components)
    component1=componentlist[0]
    component2=componentlist[1]
    component3=save_new_component(components,give_net_length())
    combine_components(component1,component2,component3)
    give_combined_components(give_net_length())
    

def save_new_component(components,netlength):
    
    componentspecification=((list(components))[0])
    componentname=(str((componentspecification)[0]))+('step')+(str(netlength))
    return componentname


def combine_components(component1,component2,component3):
    
    combinedcomponents=str(str(component1)+','+str(component2)+','+str(component3))
    subset_steps.append(combinedcomponents)
    

def give_combined_components(step):

    return (subset_steps[step-1])
    

def save_combining_process(kind):
    
    #noch nicht funktionsfähig
    combiningvar.append(kind)


def give_combining_process(netnumber):
    
    #noch nicht funktionsfähig
    return combiningvar[netnumber]
    
####################################

    
def mainprogram():
 
    merger = PdfMerger()
 
    for i in range(give_net_length()):
        
        if i>0:
            #check_key_press()
            print('________________________________________________________________________________________________________________________________________________________')
            print(give_result(i-1))
            col_net=colored_net(net,i)
            col_net.draw(style='european',filename="step"+str(i)+".pdf",
                        draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
            col_net.draw(style='european',
                        draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
            print('____________________________________________________________________ Step',i,'____________________________________________________________________')
            print('\n\n')
         
            merger.append(("step"+str(i)+".pdf"))
            os.remove(("step"+str(i)+".pdf"))

        net=give_net(i)
        
        if i==0:
            net.draw(style='european',filename="one.pdf",
                        draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
            net.draw(style='european',
                        draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
            if net.has_ac:
                print('_______________________________________________________________________ AC Schaltung ______________________________________________________________________')
            if net.has_dc:
                print('____________________________________________________________________ Originalschaltung ____________________________________________________________________')
            print('\n\n')
            merger.append("one.pdf")
            os.remove("one.pdf")
            
        if i==give_net_length()-1:
            net.draw(style='european',filename="end.pdf",
                        draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
            net.draw(style='european',
                        draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
            print('____________________________________________________________________ Vereinfachte Schaltung ____________________________________________________________________')
            print('\n\n')
            merger.append("end.pdf")
            os.remove("end.pdf")
            if net.has_ac:
                lastnet=resub()
                print('________________________________________________________________________________________________________________________________________________________')
                lastnet.draw(style='european',filename="lastnet.pdf",
                        draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
                lastnet.draw(style='european',
                        draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
                
                print('_______________________________________________________________ Rücksubstituierte Schaltung _______________________________________________________________')
                merger.append("lastnet.pdf")
                os.remove("lastnet.pdf")
            merger.write("result.pdf")
            merger.close()
        

def colored_net(net,components):
    
    comps=(give_combined_components(components)).split(',')
    colnet=net.annotate((comps[0],comps[1]), color='red')
    
    return(colnet)


def change_elements(net):
    
    netlist=list(OrderedSet(net.elements))
    net=change_elements_of_ac_netlist(net,netlist)
    
    return net
             

def change_elements_of_ac_netlist(net,netlist):
    
    for i in range(len(netlist)-1):
        if (netlist[i][0])=='R' or (netlist[i][0])=='C' or (netlist[i][0])=='L':
            
            elt = net.elements[netlist[i]]
            name=(netlist[i])
            net1 = elt._new_value(net.elements[netlist[i]].Z.jomega, )
            parts = net1.split(' ', 1)
            if (netlist[i][0])=='R':
                try:
                    newname='ZR'+ (netlist[i][1])
                except:
                    newname='ZR'
                print_changed_elements(netlist[i],net.elements[netlist[i]].R,net.elements[netlist[i]].Z.jomega)
            if (netlist[i][0])=='C':
                try:
                    newname='ZC'+ (netlist[i][1])
                except:
                    newname='ZC'
                print_changed_elements(netlist[i],net.elements[netlist[i]].C,net.elements[netlist[i]].Z.jomega)
            if (netlist[i][0])=='L':
                try:
                    newname='ZL'+ (netlist[i][1])
                except:
                    newname='ZL'
                print_changed_elements(netlist[i],net.elements[netlist[i]].L,net.elements[netlist[i]].Z.jomega)
                
            net1 = newname + ' ' + parts[1]
            net.add(net1)
            net.remove(name)
            
        if str(netlist[i][0])=='Z':
            net=net
            
        if str(netlist[i][0])=='W':
            net=net
            
    return net


def print_changed_elements(comp,value1,value2):
    
    strcomp=str(comp)
    strvalue1=str(value1)
    strvalue2=str(value2)
    print(strcomp+' = '+strvalue1+' \t\t\t->\t\t\tZ'+strcomp+' = '+strvalue2)
    
            
def resub():
    
    a=(resultcompl[give_net_length()-2])
    b=(resultcompl[give_net_length()-2])
    resultof_acnetlist=a.real_imag
    realteil=resultof_acnetlist.real
    imaginärteil=resultof_acnetlist.imag
    if imaginärteil==0 and realteil==0:
        print('No result')
    if imaginärteil==0:
        strrealteil=str(realteil)
        a='R = ' + strrealteil
        print('\nResubstituting element to:\n')
        print('Zstep'+str((give_net_length()-1))+' = '+str(b)+' \t\t\t->\t\t\tZ'+a)
    if imaginärteil!=0:
        strimaginärteil=str(imaginärteil)
        stra=str(a)
        cnt=0
        #if imag=none
        #newname= oldname[1:]
        #else
        for i in range(10):
            if stra.find('j')>=0:
                ergfind=stra.find('j')
                cnt=cnt+1
                stra=stra[ergfind+1:]
          
        if cnt>1:
            print('No resub')
            return 0
        if cnt==1:
            if strimaginärteil.find('-')>=0:
                strimaginärteil=str(imaginärteil).find('/')
                strimaginärteil2=str(imaginärteil).find('*omega')
                if (str(imaginärteil))[:strimaginärteil] == '-1':
                    strimaginärteilnew=(str(imaginärteil))[strimaginärteil+2:strimaginärteil2]   
                else:
                    strimaginärteilnew=(str(imaginärteil))[strimaginärteil+2:strimaginärteil2]+'/'+(str(imaginärteil))[1:strimaginärteil]
                a='C = ' + strimaginärteilnew
                print('\nResubstituting element to:\n')
                print('Zstep'+str((give_net_length()-1))+' = '+str(b)+' \t\t\t->\t\t\tZ'+a)
            else:
                strimaginärteil=str(imaginärteil).find('*omega')
                strimaginärteilnew=(str(imaginärteil))[:strimaginärteil]+(str(imaginärteil))[strimaginärteil+6:]
                a='L = ' + strimaginärteilnew
                print('\nResubstituting element to:\n')
                print('Zstep'+str((give_net_length()-1))+' = '+str(b)+' \t\t\t->\t\t\tZ'+a)
                

    net=(circuit.Circuit("""
        ...V 1 0 ac; down
        ...R 1 2; right
        ...W 2 0_2; down
        ...W 0 0_2; right"""))
 
    elt = net.elements['R']
    name= 'R'
    net1 = elt._new_value(strimaginärteilnew, )
    parts = net1.split(' ', 1)

    net1 = a[0] + ' ' + parts[1]
    net.add(net1) 
    net.remove('R')
 
    return net


    
def show_changing_elements(net):
    
    net.draw(style='european',draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('____________________________________________________________________ Originalschaltung ____________________________________________________________________')
    print('\nSubstituting elements to:\n')
    newnet=change_elements(net)
    newnet.draw(style='european',draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_______________________________________________________________________ AC Schaltung ______________________________________________________________________')
    return(newnet)


def choose_net(number):

###################################################################################################
#following Notebook numbers without values
###################################################################################################
    if number==1:
        return(DC_R_Series())
    if number==2:
        return(DC_R_Parallel())
    if number==3:
        return(DC_R_Mixed())
    if number==4:
        return(DC_R_Mixed_long())
    if number==5:
        return(DC_C_Series())
    if number==6:
        return(DC_C_Parallel())
    if number==7:
        return(DC_C_Mixed())
    if number==8:
        return(DC_C_Mixed_long())
    if number==9:
        return(DC_L_Series())
    if number==10:
        return(DC_L_Parallel())
    if number==11:
        return(DC_L_Mixed())
    if number==12:
        return(DC_L_Mixed_long())
    if number==13:
        return(DC_R_Random())
    if number==14:
        return(DC_C_Random())
    if number==15:
        return(DC_L_Random())
    if number==16:
        return(AC_R_Series())
    if number==17:
        return(AC_R_Parallel())
    if number==18:
        return(AC_R_Mixed())
    if number==19:
        return(AC_R_Mixed_long())
    if number==20:
        return(AC_C_Series())
    if number==21:
        return(AC_C_Parallel())
    if number==22:
        return(AC_C_Mixed())
    if number==23:
        return(AC_C_Mixed_long())
    if number==24:
        return(AC_L_Series())
    if number==25:
        return(AC_L_Parallel())
    if number==26:
        return(AC_L_Mixed())
    if number==27:
        return(AC_L_Mixed_long())
    if number==28:
        return(AC_Mixed_Series())
    if number==29:
        return(AC_Mixed_Parallel())
    if number==30:
        return(AC_Mixed_long())
    if number==31:
        return(AC_R_Random())
    if number==32:
        return(AC_C_Random())
    if number==33:
        return(AC_L_Random())
    if number==34:
        return(AC_Mixed_Random())

###################################################################################################
#following Notebook numbers with values
###################################################################################################
     
    if number==35:
        return(DC_R_Series_v())
    if number==36:
        return(DC_R_Parallel_v())
    if number==37:
        return(DC_R_Mixed_v())
    if number==38:
        return(DC_R_Mixed_long_v())
    if number==39:
        return(DC_C_Series_v())
    if number==40:
        return(DC_C_Parallel_v())
    if number==41:
        return(DC_C_Mixed_v())
    if number==42:
        return(DC_C_Mixed_long_v())
    if number==43:
        return(DC_L_Series_v())
    if number==44:
        return(DC_L_Parallel_v())
    if number==45:
        return(DC_L_Mixed_v())
    if number==46:
        return(DC_L_Mixed_long_v())
    if number==47:
        return(DC_R_Random_v())
    if number==48:
        return(DC_C_Random_v())
    if number==49:
        return(DC_L_Random_v())
    if number==50:
        return(AC_R_Series_v())
    if number==51:
        return(AC_R_Parallel_v())
    if number==52:
        return(AC_R_Mixed_v())
    if number==53:
        return(AC_R_Mixed_long_v())
    if number==54:
        return(AC_C_Series_v())
    if number==55:
        return(AC_C_Parallel_v())
    if number==56:
        return(AC_C_Mixed_v())
    if number==57:
        return(AC_C_Mixed_long_v())
    if number==58:
        return(AC_L_Series_v())
    if number==59:
        return(AC_L_Parallel_v())
    if number==60:
         return(AC_L_Mixed_v())
    if number==61:
        return(AC_L_Mixed_long_v())
    if number==62:
        return(AC_Mixed_Series_v())
    if number==63:
        return(AC_Mixed_Parallel_v())
    if number==64:
        return(AC_Mixed_long_v())
    if number==65:
        return(AC_R_Random_v())
    if number==66:
        return(AC_C_Random_v())
    if number==67:
        return(AC_L_Random_v())
    if number==68:
        return(AC_Mixed_Random_v())


###################################################################################################
#following Notebooks without values
###################################################################################################
def DC_R_Series():

    return(circuit.Circuit("""
        ...V 1 0; down
        ...R1 1 2; right
        ...R2 2 3; right
        ...R3 3 0_3; down
        ...W 0 0_3; right""")) 


def DC_R_Parallel():

    return(circuit.Circuit("""
        ...V1 1 0 dc; down
        ...W 1 2; right
        ...R1 2 0_2; down
        ...W 2 3 ; right
        ...R2 3 0_3; down
        ...W 3 4 ; right
        ...R3 4 0_4; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right""")) 


def DC_R_Mixed():

    return(circuit.Circuit("""
        ...V1 1 0; down
        ...R1 1 2; right
        ...R2 2 3; right
        ...R3 2 0_2; down
        ...R4 3 0_3; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right""")) 


def DC_R_Mixed_long():

    return(circuit.Circuit("""
        ...V1 1 0; down
        ...R1 1 2; right
        ...R2 2 3; right
        ...R3 3 4; right
        ...R4 2 0_2; down
        ...R5 3 0_3; down
        ...R6 4 0_4; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right"""))


def DC_C_Series():

    return(circuit.Circuit("""
        ...V 1 0; down
        ...C1 1 2; right
        ...C2 2 3; right
        ...C3 3 0_3; down
        ...W 0 0_3; right""")) 


def DC_C_Parallel():

    return(circuit.Circuit("""
        ...V1 1 0; down
        ...W 1 2; right
        ...C1 2 0_2; down
        ...W 2 3 ; right
        ...C2 3 0_3; down
        ...W 3 4 ; right
        ...C3 4 0_4; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right""")) 


def DC_C_Mixed():

    return(circuit.Circuit("""
        ...V1 1 0; down
        ...C1 1 2; right
        ...C2 2 3; right
        ...C3 2 0_2; down
        ...C4 3 0_3; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right""")) 


def DC_C_Mixed_long():

    return(circuit.Circuit("""
        ...V1 1 0; down
        ...C1 1 2; right
        ...C2 2 3; right
        ...C3 3 4; right
        ...C4 2 0_2; down
        ...C5 3 0_3; down
        ...C6 4 0_4; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right"""))


def DC_L_Series():

    return(circuit.Circuit("""
        ...V 1 0; down
        ...L1 1 2; right
        ...L2 2 3; right
        ...L3 3 0_3; down
        ...W 0 0_3; right""")) 


def DC_L_Parallel():

    return(circuit.Circuit("""
        ...V1 1 0; down
        ...W 1 2; right
        ...L1 2 0_2; down
        ...W 2 3 ; right
        ...L2 3 0_3; down
        ...W 3 4 ; right
        ...L3 4 0_4; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right""")) 


def DC_L_Mixed():

    return(circuit.Circuit("""
        ...V1 1 0; down
        ...L1 1 2; right
        ...L2 2 3; right
        ...L3 2 0_2; down
        ...L4 3 0_3; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right""")) 


def DC_L_Mixed_long():

    return(circuit.Circuit("""
        ...V1 1 0; down
        ...L1 1 2; right
        ...L2 2 3; right
        ...L3 3 4; right
        ...L4 2 0_2; down
        ...L5 3 0_3; down
        ...L6 4 0_4; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right"""))

def DC_R_Random():

    res=random.randrange(3,6)
    cap=0
    ind=0
    
    k=res+cap+ind
    
    par=random.randrange(1,k)

    net = randomnetwork.random_network(num_resistors=res, num_capacitors=cap, num_inductors=ind,
                        num_voltage_sources=1, kind='dc', num_parallel=par, numeric_values=False)
    net=circuit.Circuit(net.netlist())
    
    return(net)

def DC_C_Random():

    cap=random.randrange(3,6)
    res=0
    ind=0
    
    k=res+cap+ind
    
    par=random.randrange(1,k)

    net = randomnetwork.random_network(num_resistors=res, num_capacitors=cap, num_inductors=ind,
                        num_voltage_sources=1, kind='dc', num_parallel=par, numeric_values=False)
    net=circuit.Circuit(net.netlist())
    
    return(net)


def DC_L_Random():

    ind=random.randrange(3,6)
    cap=0
    res=0
    
    k=res+cap+ind
    
    par=random.randrange(1,k)

    net = randomnetwork.random_network(num_resistors=res, num_capacitors=cap, num_inductors=ind,
                        num_voltage_sources=1, kind='dc', num_parallel=par, numeric_values=False)
    net=circuit.Circuit(net.netlist())
    
    return(net)
 

def AC_R_Series():

    return(circuit.Circuit("""
        ...V 1 0 ac; down
        ...R1 1 2; right
        ...R2 2 3; right
        ...R3 3 0_3; down
        ...W 0 0_3; right""")) 


def AC_R_Parallel():

    return(circuit.Circuit("""
        ...V1 1 0 ac; down
        ...W 1 2; right
        ...R1 2 0_2; down
        ...W 2 3 ; right
        ...R2 3 0_3; down
        ...W 3 4 ; right
        ...R3 4 0_4; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right""")) 


def AC_R_Mixed():

    return(circuit.Circuit("""
        ...V1 1 0 ac; down
        ...R1 1 2; right
        ...R2 2 3; right
        ...R3 2 0_2; down
        ...R4 3 0_3; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right""")) 


def AC_R_Mixed_long():

    return(circuit.Circuit("""
        ...V1 1 0 ac; down
        ...R1 1 2; right
        ...R2 2 3; right
        ...R3 3 4; right
        ...R4 2 0_2; down
        ...R5 3 0_3; down
        ...R6 4 0_4; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right"""))


def AC_C_Series():

    return(circuit.Circuit("""
        ...V 1 0 ac; down
        ...C1 1 2; right
        ...C2 2 3; right
        ...C3 3 0_3; down
        ...W 0 0_3; right""")) 


def AC_C_Parallel():

    return(circuit.Circuit("""
        ...V1 1 0 ac; down
        ...W 1 2; right
        ...C1 2 0_2; down
        ...W 2 3 ; right
        ...C2 3 0_3; down
        ...W 3 4 ; right
        ...C3 4 0_4; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right""")) 


def AC_C_Mixed():

    return(circuit.Circuit("""
        ...V1 1 0 ac; down
        ...C1 1 2; right
        ...C2 2 3; right
        ...C3 2 0_2; down
        ...C4 3 0_3; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right""")) 


def AC_C_Mixed_long():

    return(circuit.Circuit("""
        ...V1 1 0 ac; down
        ...C1 1 2; right
        ...C2 2 3; right
        ...C3 3 4; right
        ...C4 2 0_2; down
        ...C5 3 0_3; down
        ...C6 4 0_4; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right"""))


def AC_L_Series():

    return(circuit.Circuit("""
        ...V 1 0 ac; down
        ...L1 1 2; right
        ...L2 2 3; right
        ...L3 3 0_3; down
        ...W 0 0_3; right""")) 


def AC_L_Parallel():

    return(circuit.Circuit("""
        ...V1 1 0 ac; down
        ...W 1 2; right
        ...L1 2 0_2; down
        ...W 2 3 ; right
        ...L2 3 0_3; down
        ...W 3 4 ; right
        ...L3 4 0_4; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right""")) 


def AC_L_Mixed():

    return(circuit.Circuit("""
        ...V1 1 0 ac; down
        ...L1 1 2; right
        ...L2 2 3; right
        ...L3 2 0_2; down
        ...L4 3 0_3; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right""")) 


def AC_L_Mixed_long():

    return(circuit.Circuit("""
        ...V1 1 0 ac; down
        ...L1 1 2; right
        ...L2 2 3; right
        ...L3 3 4; right
        ...L4 2 0_2; down
        ...L5 3 0_3; down
        ...L6 4 0_4; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right"""))

def AC_Mixed_Series():
    
    return(circuit.Circuit("""
        ...V1 1 0 ac; down
        ...R 1 2; right
        ...L 2 3; right
        ...C 3 0_3; down
        ...W 0 0_3; right"""))


def AC_Mixed_Parallel():
    
    return(circuit.Circuit("""
        ...V1 1 0 ac; down
        ...W 1 2; right
        ...R 2 0_2; down
        ...W 2 3 ; right
        ...C 3 0_3; down
        ...W 3 4 ; right
        ...L 4 0_4; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right"""))

def AC_Mixed_long():
    
    return(circuit.Circuit("""
        ...V 1 0 ac; down
        ...R1 1 2; right
        ...L1 2 3; right
        ...L2 3 0_3; down
        ...C1 3 4; right
        ...R2 4 5; right
        ...C2 5 0_5; down
        ...W 0 0_3; right
        ...W 0 0_5; right"""))

def AC_R_Random():

    res=random.randrange(3,6)
    cap=0
    ind=0
    
    k=res+cap+ind
    
    par=random.randrange(1,k)

    net = randomnetwork.random_network(num_resistors=res, num_capacitors=cap, num_inductors=ind,
                        num_voltage_sources=1, kind='ac', num_parallel=par, numeric_values=False)
    net=circuit.Circuit(net.netlist())
    
    return(net)

def AC_C_Random():

    cap=random.randrange(3,6)
    res=0
    ind=0
    
    k=res+cap+ind
    
    par=random.randrange(1,k)

    net = randomnetwork.random_network(num_resistors=res, num_capacitors=cap, num_inductors=ind,
                        num_voltage_sources=1, kind='ac', num_parallel=par, numeric_values=False)
    net=circuit.Circuit(net.netlist())
    
    return(net)

def AC_L_Random():

    ind=random.randrange(3,6)
    cap=0
    res=0
    
    k=res+cap+ind
    
    par=random.randrange(1,k)

    net = randomnetwork.random_network(num_resistors=res, num_capacitors=cap, num_inductors=ind,
                        num_voltage_sources=1, kind='ac', num_parallel=par, numeric_values=False)
    net=circuit.Circuit(net.netlist())
    
    return(net)

def AC_Mixed_Random():

    ind=random.randrange(1,3)
    cap=random.randrange(1,3)
    res=random.randrange(1,3)
  
    k=res+cap+ind
    
    par=random.randrange(1,k)

    net = randomnetwork.random_network(num_resistors=res, num_capacitors=cap, num_inductors=ind,
                        num_voltage_sources=1, kind='ac', num_parallel=par, numeric_values=False)
    net=circuit.Circuit(net.netlist())
    
    return(net)


###################################################################################################
#following Notebooks with values
###################################################################################################

def DC_R_Series_v():

    return(circuit.Circuit("""
        ...V 1 0 {10}; down
        ...R1 1 2 {10}; right
        ...R2 2 3 {20}; right
        ...R3 3 0_3 {10}; down
        ...W 0 0_3; right""")) 


def DC_R_Parallel_v():

    return(circuit.Circuit("""
        ...V1 1 0 {10}; down
        ...W 1 2; right
        ...R1 2 0_2 {10}; down
        ...W 2 3 ; right
        ...R2 3 0_3 {10}; down
        ...W 3 4 ; right
        ...R3 4 0_4 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right""")) 


def DC_R_Mixed_v():

    return(circuit.Circuit("""
        ...V1 1 0 {10}; down
        ...R1 1 2 {10}; right
        ...R2 2 3 {10}; right
        ...R3 2 0_2 {20}; down
        ...R4 3 0_3 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right""")) 


def DC_R_Mixed_long_v():

    return(circuit.Circuit("""
        ...V1 1 0 {10}; down
        ...R1 1 2 {10}; right
        ...R2 2 3 {20}; right
        ...R3 3 4 {10}; right
        ...R4 2 0_2 {20}; down
        ...R5 3 0_3 {20}; down
        ...R6 4 0_4 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right"""))


def DC_C_Series_v():

    return(circuit.Circuit("""
        ...V 1 0 {10}; down
        ...C1 1 2 {10}; right
        ...C2 2 3 {20}; right
        ...C3 3 0_3 {10}; down
        ...W 0 0_3; right""")) 


def DC_C_Parallel_v():

    return(circuit.Circuit("""
        ...V1 1 0 {10}; down
        ...W 1 2; right
        ...C1 2 0_2 {10}; down
        ...W 2 3 ; right
        ...C2 3 0_3 {10}; down
        ...W 3 4 ; right
        ...C3 4 0_4 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right""")) 


def DC_C_Mixed_v():

    return(circuit.Circuit("""
        ...V1 1 0 {10}; down
        ...C1 1 2 {10}; right
        ...C2 2 3 {10}; right
        ...C3 2 0_2 {20}; down
        ...C4 3 0_3 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right""")) 


def DC_C_Mixed_long_v():

    return(circuit.Circuit("""
        ...V1 1 0 {10}; down
        ...C1 1 2 {10}; right
        ...C2 2 3 {20}; right
        ...C3 3 4 {10}; right
        ...C4 2 0_2 {20}; down
        ...C5 3 0_3 {20}; down
        ...C6 4 0_4 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right"""))


def DC_L_Series_v():

    return(circuit.Circuit("""
        ...V 1 0 {10}; down
        ...L1 1 2 {10}; right
        ...L2 2 3 {20}; right
        ...L3 3 0_3 {10}; down
        ...W 0 0_3; right""")) 


def DC_L_Parallel_v():

    return(circuit.Circuit("""
        ...V1 1 0 {10}; down
        ...W 1 2; right
        ...L1 2 0_2 {10}; down
        ...W 2 3 ; right
        ...L2 3 0_3 {10}; down
        ...W 3 4 ; right
        ...L3 4 0_4 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right""")) 


def DC_L_Mixed_v():

    return(circuit.Circuit("""
        ...V1 1 0 {10}; down
        ...L1 1 2 {10}; right
        ...L2 2 3 {10}; right
        ...L3 2 0_2 {20}; down
        ...L4 3 0_3 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right""")) 


def DC_L_Mixed_long_v():

    return(circuit.Circuit("""
        ...V1 1 0 {10}; down
        ...L1 1 2 {10}; right
        ...L2 2 3 {20}; right
        ...L3 3 4 {10}; right
        ...L4 2 0_2 {20}; down
        ...L5 3 0_3 {20}; down
        ...L6 4 0_4 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right"""))

def DC_R_Random_v():

    res=random.randrange(3,6)
    cap=0
    ind=0
    
    k=res+cap+ind
    
    par=random.randrange(1,k)

    net = randomnetwork.random_network(num_resistors=res, num_capacitors=cap, num_inductors=ind,
                        num_voltage_sources=1, kind='dc', num_parallel=par, numeric_values=True)
    net=circuit.Circuit(net.netlist())
    
    return(net)

def DC_C_Random_v():

    cap=random.randrange(3,6)
    res=0
    ind=0
    
    k=res+cap+ind
    
    par=random.randrange(1,k)

    net = randomnetwork.random_network(num_resistors=res, num_capacitors=cap, num_inductors=ind,
                        num_voltage_sources=1, kind='dc', num_parallel=par, numeric_values=True)
    net=circuit.Circuit(net.netlist())
    
    return(net)


def DC_L_Random_v():

    ind=random.randrange(3,6)
    cap=0
    res=0
    
    k=res+cap+ind
    
    par=random.randrange(1,k)

    net = randomnetwork.random_network(num_resistors=res, num_capacitors=cap, num_inductors=ind,
                        num_voltage_sources=1, kind='dc', num_parallel=par, numeric_values=True)
    net=circuit.Circuit(net.netlist())
    
    return(net)


def AC_R_Series_v():

    return(circuit.Circuit("""
        ...V 1 0 ac {10}; down
        ...R1 1 2 {10}; right
        ...R2 2 3 {20}; right
        ...R3 3 0_3 {10}; down
        ...W 0 0_3; right""")) 


def AC_R_Parallel_v():

    return(circuit.Circuit("""
        ...V1 1 0 ac {10}; down
        ...W 1 2; right
        ...R1 2 0_2 {10}; down
        ...W 2 3 ; right
        ...R2 3 0_3 {10}; down
        ...W 3 4 ; right
        ...R3 4 0_4 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right""")) 


def AC_R_Mixed_v():

    return(circuit.Circuit("""
        ...V1 1 0 ac {10}; down
        ...R1 1 2 {10}; right
        ...R2 2 3 {10}; right
        ...R3 2 0_2 {20}; down
        ...R4 3 0_3 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right""")) 


def AC_R_Mixed_long_v():

    return(circuit.Circuit("""
        ...V1 1 0 ac {10}; down
        ...R1 1 2 {10}; right
        ...R2 2 3 {20}; right
        ...R3 3 4 {10}; right
        ...R4 2 0_2 {20}; down
        ...R5 3 0_3 {20}; down
        ...R6 4 0_4 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right"""))


def AC_C_Series_v():

    return(circuit.Circuit("""
        ...V 1 0 ac {10}; down
        ...C1 1 2 {10}; right
        ...C2 2 3 {20}; right
        ...C3 3 0_3 {10}; down
        ...W 0 0_3; right""")) 


def AC_C_Parallel_v():

    return(circuit.Circuit("""
        ...V1 1 0 ac {10}; down
        ...W 1 2; right
        ...C1 2 0_2 {10}; down
        ...W 2 3 ; right
        ...C2 3 0_3 {10}; down
        ...W 3 4 ; right
        ...C3 4 0_4 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right""")) 


def AC_C_Mixed_v():

    return(circuit.Circuit("""
        ...V1 1 0 ac {10}; down
        ...C1 1 2 {10}; right
        ...C2 2 3 {10}; right
        ...C3 2 0_2 {20}; down
        ...C4 3 0_3 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right""")) 


def AC_C_Mixed_long_v():

    return(circuit.Circuit("""
        ...V1 1 0 ac {10}; down
        ...C1 1 2 {10}; right
        ...C2 2 3 {20}; right
        ...C3 3 4 {10}; right
        ...C4 2 0_2 {20}; down
        ...C5 3 0_3 {20}; down
        ...C6 4 0_4 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right"""))


def AC_L_Series_v():

    return(circuit.Circuit("""
        ...V 1 0 ac {10}; down
        ...L1 1 2 {10}; right
        ...L2 2 3 {20}; right
        ...L3 3 0_3 {10}; down
        ...W 0 0_3; right""")) 


def AC_L_Parallel_v():

    return(circuit.Circuit("""
        ...V1 1 0 ac {10}; down
        ...W 1 2; right
        ...L1 2 0_2 {10}; down
        ...W 2 3 ; right
        ...L2 3 0_3 {10}; down
        ...W 3 4 ; right
        ...L3 4 0_4 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right""")) 


def AC_L_Mixed_v():

    return(circuit.Circuit("""
        ...V1 1 0 ac {10}; down
        ...L1 1 2 {10}; right
        ...L2 2 3 {10}; right
        ...L3 2 0_2 {20}; down
        ...L4 3 0_3 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right""")) 


def AC_L_Mixed_long_v():

    return(circuit.Circuit("""
        ...V1 1 0 ac {10}; down
        ...L1 1 2 {10}; right
        ...L2 2 3 {20}; right
        ...L3 3 4 {10}; right
        ...L4 2 0_2 {20}; down
        ...L5 3 0_3 {20}; down
        ...L6 4 0_4 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right"""))

def AC_Mixed_Series_v():
    
    return(circuit.Circuit("""
        ...V1 1 0 ac 10; down
        ...R 1 2 20; right
        ...L 2 3 10; right
        ...C 3 0_3 10; down
        ...W 0 0_3; right"""))


def AC_Mixed_Parallel_v():
    
    return(circuit.Circuit("""
        ...V1 1 0 ac 10; down
        ...W 1 2; right
        ...R 2 0_2 20; down
        ...W 2 3 ; right
        ...C 3 0_3 10; down
        ...W 3 4 ; right
        ...L 4 0_4 10; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right
        ...W 0_3 0_4; right"""))

def AC_Mixed_long_v():
    
    return(circuit.Circuit("""
        ...V 1 0 ac 10; down
        ...R1 1 2 10; right
        ...L1 2 3 10; right
        ...L2 3 0_3 5; down
        ...C1 3 4 10; right
        ...R2 4 5 20; right
        ...C2 5 0_5 10; down
        ...W 0 0_3; right
        ...W 0 0_5; right"""))

def AC_R_Random_v():

    res=random.randrange(3,6)
    cap=0
    ind=0
    
    k=res+cap+ind
    
    par=random.randrange(1,k)

    net = randomnetwork.random_network(num_resistors=res, num_capacitors=cap, num_inductors=ind,
                        num_voltage_sources=1, kind='ac', num_parallel=par, numeric_values=True)
    net=circuit.Circuit(net.netlist())
    
    return(net)

def AC_C_Random_v():

    cap=random.randrange(3,6)
    res=0
    ind=0
    
    k=res+cap+ind
    
    par=random.randrange(1,k)

    net = randomnetwork.random_network(num_resistors=res, num_capacitors=cap, num_inductors=ind,
                        num_voltage_sources=1, kind='ac', num_parallel=par, numeric_values=True)
    net=circuit.Circuit(net.netlist())
    
    return(net)

def AC_L_Random_v():

    ind=random.randrange(3,6)
    cap=0
    res=0
    
    k=res+cap+ind
    
    par=random.randrange(1,k)

    net = randomnetwork.random_network(num_resistors=res, num_capacitors=cap, num_inductors=ind,
                        num_voltage_sources=1, kind='ac', num_parallel=par, numeric_values=True)
    net=circuit.Circuit(net.netlist())
    
    return(net)

def AC_Mixed_Random_v():

    ind=random.randrange(1,3)
    cap=random.randrange(1,3)
    res=random.randrange(1,3)
  
    k=res+cap+ind
    
    par=random.randrange(1,k)

    net = randomnetwork.random_network(num_resistors=res, num_capacitors=cap, num_inductors=ind,
                        num_voltage_sources=1, kind='ac', num_parallel=par, numeric_values=True)
    net=circuit.Circuit(net.netlist())
    
    return(net)
###################################################################################################
#end of Notebooks
###################################################################################################

def show_notebooks():
   
    print('______________________________________________________________________ 1. DC R Series _______________________________________________________________________')
    DC_R_Series().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('______________________________________________________________________ 2. DC R Parallel _____________________________________________________________________')
    DC_R_Parallel().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('_______________________________________________________________________ 3. DC R Mixed _______________________________________________________________________')
    DC_R_Mixed().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('____________________________________________________________________ 4. DC R Mixed long _____________________________________________________________________')
    DC_R_Mixed_long().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('______________________________________________________________________ 5. DC C Series _______________________________________________________________________')
    DC_C_Series().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('_____________________________________________________________________ 6. DC C Parallel ______________________________________________________________________')
    DC_C_Parallel().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('_______________________________________________________________________ 7. DC C Mixed _______________________________________________________________________')
    DC_C_Mixed().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('____________________________________________________________________ 8. DC C Mixed long _____________________________________________________________________')
    DC_C_Mixed_long().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('______________________________________________________________________ 9. DC L Series _______________________________________________________________________')
    DC_L_Series().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('_____________________________________________________________________ 10. DC L Parallel _____________________________________________________________________')
    DC_L_Parallel().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('______________________________________________________________________ 11. DC L Mixed _______________________________________________________________________')
    DC_L_Mixed().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('____________________________________________________________________ 12. DC L Mixed long ____________________________________________________________________')
    DC_L_Mixed_long().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('______________________________________________________________________ 13. DC R Random ______________________________________________________________________')
    print('\n -> Random DC R Network \n')
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('______________________________________________________________________ 14. DC C Random ______________________________________________________________________')
    print('\n -> Random DC C Network \n')
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('______________________________________________________________________ 15. DC L Random ______________________________________________________________________')
    print('\n -> Random DC L Network \n')
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('______________________________________________________________________ 16. AC R Series ______________________________________________________________________')
    AC_R_Series().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('_____________________________________________________________________ 17. AC R Parallel _____________________________________________________________________')
    AC_R_Parallel().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('______________________________________________________________________ 18. AC R Mixed _______________________________________________________________________')
    AC_R_Mixed().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('____________________________________________________________________ 19. AC R Mixed long ____________________________________________________________________')
    AC_R_Mixed_long().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('______________________________________________________________________ 20. AC C Series ______________________________________________________________________')
    AC_C_Series().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('_____________________________________________________________________ 21. AC C Parallel _____________________________________________________________________')
    AC_C_Parallel().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('______________________________________________________________________ 22. AC C Mixed ______________________________________________________________________')
    AC_C_Mixed().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('____________________________________________________________________ 23. AC C Mixed long ____________________________________________________________________')
    AC_C_Mixed_long().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('______________________________________________________________________ 24. AC L Series ______________________________________________________________________')
    AC_L_Series().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('_____________________________________________________________________ 25. AC L Parallel _____________________________________________________________________')
    AC_L_Parallel().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('______________________________________________________________________ 26. AC L Mixed ______________________________________________________________________')
    AC_L_Mixed().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('____________________________________________________________________ 27. AC L Mixed long ____________________________________________________________________')
    AC_L_Mixed_long().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('____________________________________________________________________ 28. AC Mixed Series ____________________________________________________________________')
    AC_Mixed_Series().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('___________________________________________________________________ 29. AC Mixed Parallel ___________________________________________________________________')
    AC_Mixed_Parallel().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('_____________________________________________________________________ 30. AC Mixed long _____________________________________________________________________')
    AC_Mixed_long().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('______________________________________________________________________ 31. AC R Random ______________________________________________________________________')
    print('\n -> Random AC R Network \n')
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('______________________________________________________________________ 32. AC C Random ______________________________________________________________________')
    print('\n -> Random AC C Network \n')
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('______________________________________________________________________ 33. AC L Random ______________________________________________________________________')
    print('\n -> Random AC L Network \n')
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    print('____________________________________________________________________ 34. AC Mixed Random _____________________________________________________________________')
    print('\n -> Random AC Mixed Network \n')
    print('_____________________________________________________________________________________________________________________________________________________________')
    print('\n\n')
    
    
    
    print('Available Nets:\n\t  DC\t\t\t AC \n\t  1. DC R Series \t 16. AC R Series \n\t  2. DC R Parallel \t 17. AC R Parallel \n\t  3. DC R Mixed \t 18. AC R Mixed \n\t  4. DC R Mixed long \t 19. AC R Mixed long \n\t  5. DC C Series \t 20. AC C Series \n\t  6. DC C Parallel \t 21. AC C Parallel \n\t  7. DC C Mixed \t 22. AC C Mixed \n\t  8. DC C Mixed long \t 23. AC C Mixed long \n\t  9. DC L Series \t 24. AC L Series \n\t 10. DC L Parallel \t 25. AC L Parallel \n\t 11. DC L Mixed \t 26. AC L Mixed \n\t 12. DC L Mixed long \t 27. AC L Mixed long \n\t 13. DC R Random \t 28. AC Mixed Series \n\t 14. DC C Random \t 29. AC Mixed Parallel \n\t 15. DC L Random \t 30. AC Mixed long \n\t \t \t \t 31. AC R Random \n\t \t \t \t 32. AC C Random \n\t \t \t \t 33. AC L Random \n\t \t \t \t 34. AC Mixed Random')
    
