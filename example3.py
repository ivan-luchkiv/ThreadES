#encoding: utf-8
"""Механізм логічного виведення "а-ля RETE" з правилами. Для пришвидшення алгоритму створюється дерево триплетів. З метою спрощення алгоритму це дерево містить тільки гілки з предикатами. Функції rule використовують це дерево."""

def kb2tree(F):
    """Cтворює дерево з множини триплетів"""
    k=[t[1] for t in F] # список предикатів (p)
    d={i:set() for i in k} # дерево: словник предикатів
    #print(d)

    for t in F: # для кожного факту
        for i in k: # для кожного предиката
            if t[1]==i: # якщо це предикат i
                d[i].add(t) # додати факт у гілку з цим предикатом
    return d

def tree2kb(d):
    """Cтворює множину триплетів з дерева"""
    F=set()
    for k in d:
        F.update(d[k])
    return F

def rule1(d, p):
    """Правило для транзитивної властивості p
    (x,p,y)&(y,p,z)->(x,p,z)
    d - дерево триплетів, створене за допомогою kb2tree"""
    l=len(d)
    с=d[p].copy() # копія гілки предикатів p
    for t in с: # для кожного факту t
        for r in с: # для кожного факту r
            if t[2]==r[0]:
                d[p].add((t[0], p, r[2]))
                # if (t[0], p, r[2]) not in d[p]: # уповільнює?
                #     d[p].add((t[0], p, r[2]))
                #     new=1
    return len(d)!=l # True, якщо були нові факти

def rule2(d, p):
    """Правило для реверсивної властивості p
    (x,p,y)->(y,p,x)
    d - дерево триплетів, створене за допомогою kb2tree"""
    l=len(d)
    for t in d[p].copy():
        d[p].add((t[2], p, t[0]))
    return len(d)!=l

def rule3(d, p):
    """Правило для асоціативної властивості p
    (x,p,y)&(x,p,z)->(y,p,z)
    d - дерево триплетів, створене за допомогою kb2tree"""
    l = len(d)
    с = d[p].copy()  # копія гілки предикатів p
    for t in с:  # для кожного факту t
        for r in с:  # для кожного факту r
            if t[0] == r[0]:  # перевірка, чи однакові x
                d[p].add((t[2], p, r[2]))  # додати новий факт
    return len(d) != l  # True, якщо були нові факти

def reasoner(F, rules, *args):
    """Виводить нові факти з множини триплетів F шляхом застосування правил rules. Цикл застосування усіх правил повторюється, поки виводяться нові факти. Повертає множину зі старими і новими фактами."""
    d=kb2tree(F)
    n=1
    while n: # цикл повторюється, поки виводяться нові факти
        n=0
        for r,a in zip(rules, args):
            n+=r(d, *a)
        #n+=rule1(d, p=2)
        #n+=rule2(d, p=0)
    return tree2kb(d)

if __name__=="__main__":
    # приклад:
    F={(1,2,3),(3,2,4),(5,2,6),(1,0,7),(8,0,9)} # факти-триплети (s,p,o)
    A=reasoner(F, [rule1, rule2], (2,), (0,))
    print(A)
    print(A-F)