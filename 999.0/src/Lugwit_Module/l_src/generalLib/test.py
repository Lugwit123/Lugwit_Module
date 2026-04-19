file=r'e:\BUG_Project\B003_S78\Asset_work\sets\shot16_A\work\B003_S78_sets_ZL_preview.ma'
with open(file,'rb') as f:
    f.seek(100000000000, )
    print (f.read())
    
print(len(''))