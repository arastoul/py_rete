# -*- coding: utf-8 -*-
from py_rete.production import Production
from py_rete.production import Cond
from py_rete.production import AndCond
from py_rete.production import Filter
from py_rete.production import Bind
from py_rete.network import Network
from py_rete.common import WME


def test_filter_compare():
    net = Network()
    c0 = Cond('spu:1', 'price', '$x')
    f0 = Filter('$x>100')
    f1 = Filter('$x<200')
    f2 = Filter('$x>200 and $x<400')
    f3 = Filter('$x>300')

    p0 = net.add_production(Production("test0", AndCond(c0, f0, f1)))
    p1 = net.add_production(Production("test1", AndCond(c0, f2)))
    p2 = net.add_production(Production("test2", AndCond(c0, f3)))
    net.add_wme(WME('spu:1', 'price', '100'))
    net.add_wme(WME('spu:1', 'price', '150'))
    net.add_wme(WME('spu:1', 'price', '300'))

    assert len(p0.items) == 1
    token = p0.items.pop()
    assert token.get_binding('$x') == '150'

    assert len(p1.items) == 1
    token = p1.items.pop()
    assert token.get_binding('$x') == '300'

    assert not p2.items


def test_bind():
    net = Network()
    c0 = Cond('spu:1', 'sales', '$x')
    b0 = Bind('len(set($x) & set(range(1, 100)))', '$num')
    f0 = Filter('$num > 0')
    p0 = net.add_production(Production('test0', AndCond(c0, b0, f0)))

    b1 = Bind('len(set($x) & set(range(100, 200)))', '$num')
    p1 = net.add_production(Production('test1', AndCond(c0, b1, f0)))

    b2 = Bind('len(set($x) & set(range(300, 400)))', '$num')
    p2 = net.add_production(Production('test2', AndCond(c0, b2, f0)))

    net.add_wme(WME('spu:1', 'sales', 'range(50, 110)'))

    assert len(p0.items) == 1
    assert len(p1.items) == 1
    assert len(p2.items) == 0
    t0 = p0.items[0]
    t1 = p1.items[0]
    assert t0.get_binding('$num') == 50
    assert t1.get_binding('$num') == 10
