import re
aa='W:\BKC_TL6\EP01\maya\TL6_01_01_sc001_an(101-245).ma'
aa=aa.replace('\\','/')
bb=re.search(r'TL6_(\d+)_01',aa).group(1)
print (bb)