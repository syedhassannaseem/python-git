questions=[

    ["Who wrote the play \"Romeo and Juliet\"?","William Shakespeare","Sylvia Plath","Rudyard Kipling","Oscar Wilde"],
    [ "How many continents are there on Earth?","five","six","seven","eight"],
    ["Who discovered gravity?","Albert Einstein","Sir Isaac Newton","Abdul-Rahman Al-Khazini","Syed Hassan Naseem"],
    ["What is the largest ocean in the world?","Pacific Ocean","Indian Ocean","Southern Ocean","Arctic Ocean"],
    ["How many ocean in the world?","five","six","four","seven"]
]
level=[1000,2000,4000,10000,20000,40000,80000,160000,320000,640000,1280000,2560000,5120000,10000000]
for i in range(0,len(questions)):
 question=questions[i]
 print(f"Your Question is for {level[i]}")
 print(question[0])
 print(f"a-{question[1]}\tb-{question[2]}\n"
      f"c-{question[3]}\td-{question[4]}")
 quit=input("is you want to quit the game then enter \"yes\": ")
 if(quit=="yes"):
   break
 else:
  reply=input("Enter your answer: ")
 if(reply=="a" ):
    print("Congratulation!Your answer is correct")
    print(f"Congratulation!You won: {level[i]}\n")
 else:
   if(i==0):
     print(level[i]-i)
   else:
    print(f"Congratulation!You got: {level[i-1]}")
   print("your answer is false") 
   break
 
 
