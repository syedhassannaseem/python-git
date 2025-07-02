ques=str(input("enter message: "))
lst=ques.split()
coding=int(input("coding for '1' and decoding for '0'"))
coding==True if (coding==1) else False
if(coding):
 en=[]
 for word in lst:
   if(len(word)>=3):
     r1="Eerte"
     r2="dsfgs"
     st=r1+word[1:]+word[0]+r2
     en.append(st)
   else:
    en.append(word[::-1])
 print(" ".join(en))
else:
  en=[]
  for word in lst:
    if(len(word)>=3):
     st=word[5:-5]
     st=st[-1]+st[:-1]
     en.append(st)
    else:
     en.append(word[::-1])
  print(" ".join(en))

 
   