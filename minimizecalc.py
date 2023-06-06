
import os
import pathlib
from lcapy import *
from lcapy import circuit
from ordered_set import OrderedSet
#import keyboard
from sys import *
import random 
import time
####################################
netarr=[]
subset_steps=[]
result=[]
combiningvar=[]
####################################

def clear_workspace():
    
    mydir=pathlib.Path().resolve()
    for f in os.listdir(mydir):
        if not f.endswith(".png"):
            continue
        os.remove(os.path.join(mydir, f))


def check_key_press():
        
    #keyboard.wait('enter')
    key='pressed'
    return key      

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

         
def explain_ac_parallel_print(net,sublist,total,newname):
    
    solution=( newname +' = ( 1 / (( 1 / '+(sublist[0])+ ') + ( 1 / ' +(sublist[1]) + ' )) )'
        + '\n' '≙ ( 1 / (( 1 / '+(net.elements[sublist[0]].cpt.args[0])+ ') + ( 1 / ' +(net.elements[sublist[1]].cpt.args[0]) + ' )) )' 
        +'\n'+ newname + ' = ' + str(total))
    result.append(solution)
    
        
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
    
    for i in range(give_net_length()):
        
        if i>0:
            #check_key_press()
            print(give_result(i-1))
            col_net=colored_net(net,i)
            col_net.draw(style='european',
                        draw_nodes=False,label_nodes=False,cpt_size=1,node_spacing=2.5)
            print('______________________________________________ step',i,'______________________________________________')

        net=give_net(i)
        
        if i==0:
            net.draw(style='european',
                        draw_nodes=False,label_nodes=False,cpt_size=1,node_spacing=2.5)
            print('______________________________________________ Originalschaltung ______________________________________________')
            
        if i==give_net_length()-1:
            time.sleep(10)
            net.draw(style='european',
                        draw_nodes=False,label_nodes=False,cpt_size=1,node_spacing=2.5)
            print('______________________________________________ Vereinfachte Schaltung ______________________________________________')
        time.sleep(10)

def colored_net(net,components):
    
    comps=(give_combined_components(components)).split(',')
    strnet=(str(net))
    strnet=strnet+('\n')
    
    for cnt in range(2):
    
        findcomp=(strnet.find(comps[cnt]))
        strnethelp=(strnet[findcomp+1:])
        findcomponent=strnethelp.find('\n')
        colnetstr=strnet[:findcomp+findcomponent+1]+', color=red!80 \n'+strnet[findcomp+findcomponent+2:]
        strnet=colnetstr
        
    return circuit.Circuit(colnetstr)


def change_elements(net):
    
    netlist=list(OrderedSet(net.elements))
    net=change_elements_of_ac_netlist(net,netlist)
    
    return net
             

def change_elements_of_ac_netlist(net,netlist):
    
    strnet=str(net)
    for i in range(len(netlist)-1):
        findcomp=strnet.find(netlist[i])
        if str(netlist[i][0])=='R' or str(netlist[i][0])=='C' or str(netlist[i][0])=='L':
            strnet=(strnet[:findcomp]) + 'Z'+netlist[i] + (strnet[findcomp+len(netlist[i]):])
            strnethelp=(strnet[findcomp:])
            findcomphelp=strnethelp.find(';')
            if net.elements[netlist[i]].cpt.args[0]==0 or net.elements[netlist[i]].cpt.args[0]=='L' or net.elements[netlist[i]].cpt.args[0]=='C' or net.elements[netlist[i]].cpt.args[0]=='R':
                one=(findcomp+findcomphelp)
                two=(findcomp+findcomphelp+1)
                erg=(net.elements[netlist[i]].Z.jomega)
                strnet=(strnet[:one]) + ' {'+str(erg)+'};' + (strnet[two:])
            else:
                strnethelptwo=(strnethelp[:findcomphelp])
                findcompheltwo=strnethelptwo.rfind(' ')
                one=(findcomp+findcompheltwo+1)
                two=(findcomp+findcomphelp)
                erg=(net.elements[netlist[i]].Z.jomega)
                strnet=(strnet[:one]) + '{'+str(erg)+'}' + (strnet[two:])
            if str(netlist[i][0])=='R':
                print_changed_elements(netlist[i],net.elements[netlist[i]].R,erg)
            if str(netlist[i][0])=='C':
                print_changed_elements(netlist[i],net.elements[netlist[i]].C,erg)
            if str(netlist[i][0])=='L':
                print_changed_elements(netlist[i],net.elements[netlist[i]].L,erg)
        if str(netlist[i][0])=='Z':
            strnet=strnet
        if str(netlist[i][0])=='W':
            strnet=strnet
    return circuit.Circuit(strnet)


def print_changed_elements(comp,value1,value2):
    
    strcomp=str(comp)
    strvalue1=str(value1)
    strvalue2=str(value2)
    print(strcomp+' = '+strvalue1+' |->| Z'+strcomp+' = '+strvalue2)
    if strcomp[0]=='R':
        if value2!=strcomp:
            print('yes')
    if strcomp[0]=='C':
        if strvalue2.find('-j')>=0:
            print('yes')
    if strcomp[0]=='L':
        if strvalue2.find('j')>=0:
            print('yes')
    
            
def resub():
    
    strerg=give_result(give_net_length()-2)
    print(strerg)
    strergold=strerg.find('\n')
    strergold2=strerg[strergold+1:]
    strergnew=strergold2.find('\n')
    strergnew2=strerg[strergnew+strergold+1:]
    print('________')
    print(strergnew2)
    print(strergnew2.find('j*'))
    print(strergnew2.find('- j'))


def choose_net(number):
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
    
    
def DC_R_Series():

    return(circuit.Circuit("""
        ...V 1 0 {10}; down
        ...R1 1 2 {10}; right
        ...R2 2 3 {20}; right
        ...R3 3 0_3 {10}; down
        ...W 0 0_3; right""")) 


def DC_R_Parallel():

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


def DC_R_Mixed():

    return(circuit.Circuit("""
        ...V1 1 0 ac {10}; down
        ...R1 1 2 {10}; right
        ...R2 2 3 {10}; right
        ...R3 2 0_2 {20}; down
        ...R4 3 0_3 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right""")) 


def DC_R_Mixed_long():

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


def DC_C_Series():

    return(circuit.Circuit("""
        ...V 1 0 {10}; down
        ...C1 1 2 {10}; right
        ...C2 2 3 {20}; right
        ...C3 3 0_3 {10}; down
        ...W 0 0_3; right""")) 


def DC_C_Parallel():

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


def DC_C_Mixed():

    return(circuit.Circuit("""
        ...V1 1 0 ac {10}; down
        ...C1 1 2 {10}; right
        ...C2 2 3 {10}; right
        ...C3 2 0_2 {20}; down
        ...C4 3 0_3 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right""")) 


def DC_C_Mixed_long():

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


def DC_L_Series():

    return(circuit.Circuit("""
        ...V 1 0 {10}; down
        ...L1 1 2 {10}; right
        ...L2 2 3 {20}; right
        ...L3 3 0_3 {10}; down
        ...W 0 0_3; right""")) 


def DC_L_Parallel():

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


def DC_L_Mixed():

    return(circuit.Circuit("""
        ...V1 1 0 ac {10}; down
        ...L1 1 2 {10}; right
        ...L2 2 3 {10}; right
        ...L3 2 0_2 {20}; down
        ...L4 3 0_3 {10}; down
        ...W 0 0_1; right
        ...W 0_1 0_2; right
        ...W 0_2 0_3; right""")) 


def DC_L_Mixed_long():

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

def show_notebooks():
   
    print('________________________________________________________1. DC R Series________________________________________________________')
    DC_R_Series().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________')
    
    print('_______________________________________________________2. DC R Parallel______________________________________________________')
    DC_R_Parallel().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________')
    
    print('________________________________________________________3. DC R Mixed________________________________________________________')
    DC_R_Mixed().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________')
    
    print('______________________________________________________4. DC R Mixed long______________________________________________________')
    DC_R_Mixed_long().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________')
    
    print('________________________________________________________5. DC C Series________________________________________________________')
    DC_C_Series().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________')
    
    print('_______________________________________________________6. DC C Parallel_______________________________________________________')
    DC_C_Parallel().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________')
    
    print('________________________________________________________7. DC C Mixed________________________________________________________')
    DC_C_Mixed().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________')
    
    print('______________________________________________________8. DC C Mixed long______________________________________________________')
    DC_C_Mixed_long().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________')
    
    print('________________________________________________________9. DC L Series________________________________________________________')
    DC_L_Series().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________')
    
    print('______________________________________________________10. DC L Parallel______________________________________________________')
    DC_L_Parallel().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________')
    
    print('_______________________________________________________11. DC L Mixed_______________________________________________________')
    DC_L_Mixed().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________')
    
    print('_____________________________________________________12. DC L Mixed long_____________________________________________________')
    DC_L_Mixed_long().draw(style='european', draw_nodes=False,label_nodes=False,cpt_size=0.5,node_spacing=2)
    print('_____________________________________________________________________________________________________________________________')
    
