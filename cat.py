def concat_datasets(datasets):
    ds0 = [[datasets[0]]]
    print("ds0:",type(ds0))
    for ds1 in datasets[1:]:
        ds0.append([ds1])
    return ds0
def p(l):
    for i,e in enumerate(l):
        print(i,e)
def flatten(l):
    f=[]
    for x in l:
        for y in x:
            f.append(y)
    return f
l1=[[1,2],[3]]
l3=[[4,5,6]]
l4=[[7,9,9,0]]
all=[l1,l3,l4]
print('all:',all)
p(all)
#flattened_list = [y for x in all for y in x]
print('flattened:',flatten(all))
flatall=flatten(all)
p(flatall)
print('-------')

#zip(tuple(datasets)).flat_map(lambda *args: concat_datasets(args)

z = list(zip(tuple(concat_datasets(all))))
print('tuple concat '+'z',type(z),z)
p(z)
print('-------')
flatz=flatten(z)
print('flatten z:',flatz)
p(flatz)
print('-------')
z2 = list(zip((concat_datasets(tuple(all)))))
print('concat tuple '+'z2',type(z2),z2)
p(z2)
print('-------')
flatz2=flatten(z2)
print('flatten z2:',flatz2)
p(flatz2)
print('-------')
print(z==z2)
print(flatz==flatz2)
print(flatz==all)
print(flatz2==all)