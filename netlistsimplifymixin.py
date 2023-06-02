"""This module provides the SubNetlistSimplifyMixin class.

Copyright 2022--2023 Michael Hayes, UCECE

"""


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


from .expr import expr
from warnings import warn
from collections import OrderedDict
from ordered_set import OrderedSet

class NetlistSimplifyMixin:
    
    def _do_simplify_combine(self, string, subset, net,
                             explain=False, add=False, series=False):
        
        if explain:
            print(string % subset)

        subset_list = list(subset)
        
        if add:
            total = expr(0)
            for name in subset_list[0:2]: #nur 2 komponenten
                total += expr(self.elements[name].cpt.args[0])
            
            if (subset_list[0])[0] == 'R' or (subset_list[0])[0] == 'C' or (subset_list[0])[0] == 'L':
                explain_dc_series_print(self,subset_list,
                        total,(save_new_component(subset_list[0:2],(give_net_length()+1))))
            if (subset_list[0])[0] == 'Z':
                explain_ac_series_print(self,subset_list,
                        total,(save_new_component(subset_list[0:2],(give_net_length()+1))))
                    
        else:
            if (subset_list[0])[0] == 'R' or (subset_list[0])[0] == 'C' or (subset_list[0])[0] == 'L':
                total = expr(0)
                total = ( (expr(self.elements[subset_list[0]].cpt.args[0]) * expr(self.elements[subset_list[1]].cpt.args[0])) 
                            / (expr(self.elements[subset_list[0]].cpt.args[0]) + expr(self.elements[subset_list[1]].cpt.args[0])))
                    
                explain_dc_parallel_print(self,subset_list,
                            total,(save_new_component(subset_list[0:2],(give_net_length()+1))))
            if (subset_list[0])[0]=='Z':
                total = expr(0)
                total = 1 / ( (1 / (expr(self.elements[subset_list[0]].cpt.args[0]))
                               + (1 / expr(self.elements[subset_list[1]].cpt.args[0]))))
                    
                explain_ac_parallel_print(self,subset_list,
                            total,(save_new_component(subset_list[0:2],(give_net_length()+1))))
                
                
                
        ic = None
        name = subset_list[0]
        name1 = subset_list[1]
        newname=save_new_component(subset_list[0:2],(give_net_length()+1))
        elt = self.elements[name]
        if elt.cpt.has_ic:
            ic = expr(0)
            for name1 in subset_list[0:2]: #nur 2 komponenten
                ic += expr(self.elements[name1].cpt.args[1])

            if explain:
                print('%s combined IC = %s' % (subset, ic))

        net1 = elt._new_value(total, ic)
        parts = net1.split(' ', 1)
        net1 = newname + ' ' + parts[1]
            
        net.add(net1)
        net.remove(name)
            
        for name1 in subset_list[1:2]: #nur 2 komponenten
            # Replace with wire or open-circuit.
            if series:
                net1 = self.elements[name1]._netmake_W()
            else:
                net1 = self.elements[name1]._netmake_O()

                # Avoid creating open-circuit components.
            if True and series:
                net.add(net1)
            #self._remove_dangling(skip=subset_list[1:2])
            save_net(self)
            net.remove(name1)
                
        return True

    def _check_ic(self, subset):

        subset = subset.copy()
        name = subset.pop()
        has_ic = self.elements[name].has_ic

        okay = True
        for name1 in subset:
            if self.elements[name1].has_ic != has_ic:
                warn('Incompatible initial conditions for %s and %s' %
                     (name, name1))
                okay = False
        if not has_ic:
            return okay
        ic = self.elements[name].cpt.args[1]
        for name1 in subset:
            if self.elements[name1].cpt.args[1] != ic:
                warn('Incompatible initial conditions for %s and %s' %
                     (name, name1))
                okay = False

        return okay

    def _simplify_combine_series(self, skip, explain=False):

        net = self.copy()
        changed = False

        for aset in net.in_series():
            aset -= skip
            subsets = net._find_combine_subsets(aset)
            for k, subset in subsets.items():
                if k == 'I':
                    #warn('Netlist has current sources in series: %s' % subset)
                    print()
                elif k in ('R', 'NR', 'L', 'V', 'Z'):
                    if k == 'L' and not self._check_ic(subset):
                        continue
                    changed |= self._do_simplify_combine('Can add in series: %s',
                                                         subset, net, explain, True, True)
                    save_components(subset)
                elif k in ('C', 'Y'):
                    changed |= self._do_simplify_combine('Can combine in series: %s',
                                                         subset, net, explain, False, True)
                    save_components(subset)
                else:
                    raise RuntimeError('Internal error')

        return net, changed

    def _simplify_combine_parallel(self, skip, explain=False):

        net = self.copy()
        changed = False

        for aset in net.in_parallel():
            aset -= skip
            subsets = net._find_combine_subsets(aset)
            for k, subset in subsets.items():
                if k == 'V':
                    #warn('Netlist has voltage sources in parallel: %s' % subset)
                    print()
                elif k in ('R', 'NR', 'L', 'Z'):
                    changed |= self._do_simplify_combine('Can combine in parallel: %s',
                                                         subset, net, explain, False, False)
                    save_components(subset)
                elif k in ('C', 'Y', 'I'):
                    if k == 'C' and not self._check_ic(subset):
                        continue
                    changed |= self._do_simplify_combine('Can add in parallel: %s',
                                                         subset, net, explain, True, False)
                    save_components(subset)
                else:
                    raise RuntimeError('Internal error')

        # TODO, remove dangling wires connected to the removed components.

        return net, changed

    def _simplify_redundant_series(self, skip, explain=False):

        net = self.copy()
        changed = False

        for aset in net.in_series():
            Iname = None
            for name in aset:
                cpt = self._elements[name]
                if cpt.type == 'I':
                    Iname = name
                    break
            if Iname is not None:
                for name in aset:
                    cpt = self._elements[name]
                    #if cpt.type != 'I':
                     #   warn('Have redundant %s in series with %s' %
                      #       (name, Iname))

        return net, False

    def _simplify_redundant_parallel(self, skip, explain=False):

        net = self.copy()
        changed = False

        for aset in net.in_parallel():
            Vname = None
            for name in aset:
                cpt = self._elements[name]
                if cpt.type == 'V':
                    Vname = name
                    break
            if Vname is not None:
                for name in aset:
                    cpt = self._elements[name]
                    #if cpt.type != 'V':
                     #   warn('Have redundant %s in parallel with %s' %
                      #       (name, Vname))

        return net, False

    def _keep_dangling(self, cpt, keep_nodes):

        for node in cpt.nodes:
            if node.is_dangling and node.name in keep_nodes:
                return True

        return False

    def _remove_dangling(self, skip, explain=False, keep_nodes=None):

        new = self._new()
        changed = False

        for cpt in self._elements.values():
            if (cpt.is_dangling and cpt.name not in skip
                    and not self._keep_dangling(cpt, keep_nodes)):
                if explain:
                    print('Removing dangling component %s' % cpt.name)
                changed = True
            else:
                new._add(cpt._copy())

        return new, changed

    def _remove_disconnected(self, skip, explain=False, keep_nodes=None):

        new = self._new()
        changed = False

        for cpt in self._elements.values():
            if (cpt.is_disconnected and cpt.name not in skip
                    and not self._keep_dangling(cpt, keep_nodes)):
                if explain:
                    print('Removing disconnected component %s' % cpt.name)
                changed = True
            else:
                new._add(cpt._copy())

        return new, changed

    def _simplify_series(self, skip, explain=False):

        net, changed = self._simplify_redundant_series(skip, explain)
        net, changed2 = net._simplify_combine_series(skip, explain)
        return net, changed or changed2

    def _simplify_parallel(self, skip, explain=False):

        net, changed = self._simplify_redundant_parallel(skip, explain)
        net, changed2 = net._simplify_combine_parallel(skip, explain)
        return net, changed or changed2

    def remove_dangling(self, select=None, ignore=None, passes=0, explain=False,
                        modify=True, keep_nodes=None):
        """Simplify a circuit by removing dangling components.

        This performs a number of passes specified by `passes`.  If zero,
        this iterates until no more simplifications can be performed.

        Note, if there are no circuits, e.g., a series network, then
        all the components will be removed.

        `select` is a list of component names to consider for simplification.
        If `None`, all components are considered.

        If `explain` is True, the reason for a simplification is printed.
        If `modify` is False, no modifications are performed.

        """

        return self.simplify(select=select, ignore=ignore, passes=passes,
                             explain=explain, modify=modify,
                             series=False, parallel=False, dangling=True,
                             keep_nodes=keep_nodes)

    def remove_dangling_wires(self, passes=0, explain=False,
                              modify=True, keep_nodes=None):
        """Simplify a circuit by removing dangling wires.

        This also removes disconnected open-circuit components
        after dangling wires have been removed.

        This performs a number of passes specified by `passes`.  If zero,
        this iterates until no more simplifications can be performed.

        If `explain` is True, the reason for a simplification is printed.
        If `modify` is False, no modifications are performed."""

        new = self.simplify(select=self.components.wires,
                            passes=passes, explain=explain,
                            modify=modify, series=False,
                            parallel=False, dangling=True, disconnected=False,
                            keep_nodes=keep_nodes)

        # Remove disconnected open-circuit components.
        return new.simplify(select=self.components.open_circuits,
                            passes=passes, explain=explain,
                            modify=modify, series=False,
                            parallel=False, dangling=False, disconnected=True,
                            keep_nodes=keep_nodes)

    def remove_disconnected(self, select=None, ignore=None, passes=0,
                            explain=False, modify=True, keep_nodes=None):
        """Simplify a circuit by removing disconnected components.

        This performs a number of passes specified by `passes`.  If zero,
        this iterates until no more simplifications can be performed.

        `select` is a list of component names to consider for simplification.
        If `None`, all components are considered.

        If `explain` is True, the reason for a simplification is printed.
        If `modify` is False, no modifications are performed."""

        return self.simplify(select=select, ignore=ignore, passes=passes,
                             explain=explain, modify=modify,
                             series=False, parallel=False, dangling=False,
                             disconnected=True, keep_nodes=keep_nodes)

    def simplify_series(self, select=None, ignore=None, passes=0,
                        explain=False, modify=True, keep_nodes=None):
        """Simplify a circuit by combining components in series.

        This performs a number of passes specified by `passes`.  If zero,
        this iterates until no more simplifications can be performed.

        `select` is a list of component names to consider for simplification.
        If `None`, all components are considered.

        If `None`, all components are considered.
        If `explain` is True, the reason for a simplification is printed.
        If `modify` is False, no modifications are performed."""

        return self.simplify(select=select, ignore=ignore, passes=passes,
                             explain=explain, modify=modify,
                             series=True, parallel=False, dangling=False,
                             keep_nodes=keep_nodes)

    def simplify_parallel(self, select=None, ignore=None, passes=0,
                          explain=False, modify=True, keep_nodes=None):
        """Simplify a circuit by combining components in parallel.

        This performs a number of passes specified by `passes`.  If zero,
        this iterates until no more simplifications can be performed.

        `select` is a list of component names to consider for simplification.
        If `None`, all components are considered.

        If `None`, all components are considered.
        If `explain` is True, the reason for a simplification is printed.
        If `modify` is False, no modifications are performed."""

        return self.simplify(select=select, ignore=ignore, passes=passes,
                             explain=explain, modify=modify,
                             series=False, parallel=True, dangling=False,
                             keep_nodes=keep_nodes)

    def simplify(self, select=None, ignore=None, passes=0, series=True,
                 parallel=True, dangling=False, disconnected=False,
                 explain=False, modify=True, keep_nodes=None):
        """Simplify a circuit by combining components in series and combining
        components in parallel.

        If `dangling` is True, then dangling components are removed.
        Dangling components are not in a circuit.

        If `disconnected` is True, then disconnected components are removed.
        Disconnected components are not connected to any other components.

        This performs a number of passes specified by `passes`.  If zero,
        this iterates until no more simplifications can be performed.

        `select` is a list of component names to consider for simplification.
        If `None`, all components are considered.

        If `explain` is True, the reason for a simplification is printed.
        If `modify` is False, no modifications are performed.

        See also `simplify_series`, `simplify_parallel`, `remove_dangling`,
        and `remove_dangling_wires`.

        """

        if keep_nodes is None:
            if '0' in self.nodes:
                keep_nodes = ['0']
            else:
                keep_nodes = []

        keep_nodes = [str(node) for node in keep_nodes]

        skip = OrderedSet()

        if select is not None:
            skip = OrderedSet(self._elements) - OrderedSet(select)

        if ignore is not None:
            skip = skip.union(OrderedSet(ignore))

        # Perhaps use num cpts?
        if passes == 0:
            passes = 100
        
        net = self
        
        for m in range(passes):
            changed = False
            if dangling:
                net, changed1 = net._remove_dangling(skip, explain, keep_nodes)
                changed = changed or changed1
            if disconnected:
                net, changed1 = net._remove_disconnected(
                    skip, explain, keep_nodes)
                changed = changed or changed1
            if series:
                net, changed1 = net._simplify_series(skip, explain)
                changed = changed or changed1
            if parallel:
                net, changed1 = net._simplify_parallel(skip, explain)
                changed = changed or changed1

            if not changed:
                break
        if not modify:
            return self
        
        save_net(net)
        
        return net
