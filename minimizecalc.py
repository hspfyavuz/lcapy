import os
import pathlib
from lcapy import *
from lcapy import circuit
from ordered_set import OrderedSet
import keyboard
from sys import *
import random 
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
        
    keyboard.wait('enter')
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
            check_key_press()
            print(give_result(i-1))
            col_net=colored_net(net,i)
            col_net.draw(style='european',filename='step'+str(i)+'.png',
                        draw_nodes=False,label_nodes=False,cpt_size=1,node_spacing=3.5)

        net=give_net(i)
        
        if i==0:
            net.draw(style='european',filename='Schaltung.png',
                        draw_nodes=False,label_nodes=False,cpt_size=1,node_spacing=3.5)
            
        if i==give_net_length()-1:
            net.draw(style='european',filename='Vereinfachte-Schaltung.png',
                        draw_nodes=False,label_nodes=False,cpt_size=1,node_spacing=3.5)
            
        print('_______________')
         

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
            strnethelptwo=(strnethelp[:findcomphelp])
            findcompheltwo=strnethelptwo.rfind(' ')
            one=(findcomp+findcompheltwo+1)
            two=(findcomp+findcomphelp)
            erg=(net.elements[netlist[i]].Z.jomega)
            strnet=(strnet[:one]) + '{'+str(erg)+'}' + (strnet[two:])
        if str(netlist[i][0])=='Z':
            strnet=strnet
        if str(netlist[i][0])=='W':
            strnet=strnet
    return circuit.Circuit(strnet)
