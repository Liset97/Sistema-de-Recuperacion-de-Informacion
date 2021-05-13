import json
import numpy as np



inutiles=["","a","a's","able","about","acept","above","according","accordingly","across","actually","add","advance","after","afterwards",
          "again","against","ain't","all","allow","allows","almost","alone","along","already","also","although",
          "always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway",
          "anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","aside","ask",
          "asking","associated","at","available","away","awfully","b","be","became","because","become","becomes",
          "becoming","been","before","beforehand","behind","begin","being","believe","below","beside","besides","best",
          "better","between","beyond","both","break","brief","bring","but","buy","by","build","c","c'mon","c's","came","call","calm","can","can't","cannot","cant",
          "cancel","care","carry","catch","cause","causes","certain","certainly","change","changes","choose","check","clean","clearly","close","co","com","come","comes","concerning",
          "consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't",
          "course","currently","cut","d","dance","deal","declare","decorate","decide","definitely","demostrate","defend","depend","described","describe","despite","did","didn't","different","do","does","doesn't",
          "doing","don't","done","down","downwards","draw","drink","drive","during","e","eat","each","edu","eg","eight","either","else","elsewhere",
          "enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything",
          "everywhere","ex","exactly","example","except","explain","f","far","fall","feel","fill","few","fifth","find","finish","fit","fix","fly","first","five","followed","following",
          "follows","forget","for","former","formerly","forth","four","from","further","furthermore","g","get","gets","getting","give",
          "given","gives","go","goes","going","gone","got","gotten","greetings","h","had","hadn't","happen","happens","hardly",
          "has","hasn't","have","haven't","having","he","he's","hear","hello","help","hence","her","here","here's","hereafter",
          "hereby","herein","hereupon","hers","herself","hi","him","himself","his","hit","hither","hopefully","how","howbeit",
          "however","hurt","i","i'd","i'll","i'm","i've","ie","if","ignored","immediate","in","inasmuch","inc","indeed",
          "indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isn't","it","it'd","it'll",
          "it's","its","itself","j","just","k","keep","keeps","kept","know","known","knows","l","last","lately","later",
          "latter","latterly","least","learn","less","lest","let","let's","like","liked","likely","little","look","looking",
          "looks","ltd","m","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover",
          "most","mostly","much","must","my","myself","n","name","namely","nd","near","nearly","necessary","need","needs",
          "neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not",
          "nothing","novel","now","nowhere","o","obviously","of","off","often","oh","ok","okay","old","on","once","one",
          "ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over",
          "overall","own","p","particular","particularly","per","perhaps","placed","please","plus","possible","presumably",
          "probably","provides","q","que","quite","qv","r","rather","rd","re","really","reasonably","regarding","regardless",
          "regards","relatively","respectively","right","s","said","same","saw","say","saying","says","second","secondly",
          "see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously",
          "seven","several","shall","she","should","shouldn't","since","six","so","some","somebody","somehow","someone",
          "something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still",
          "sub","such","sup","sure","t","t's","take","taken","tell","tends","th","than","thank","thanks","thanx","that",
          "that's","thats","the","their","theirs","them","themselves","then","thence","there","there's","thereafter","thereby",
          "therefore","therein","theres","thereupon","these","they","they'd","they'll","they're","they've","think","third",
          "this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together",
          "too","took","toward","towards","tried","tries","truly","try","trying","twice","two","tupy","u","un","under",
          "unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using",
          "usually","uucp","v","value","various","very","via","visit","viz","vs","w","want","wants","was","wasn't","watch","way","we",
          "we'd","we'll","we're","we've","welcome","well","went","were","weren't","what","what's","whatever","when","whence",
          "whenever","where","where's","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which",
          "while","whither","who","who's","whoever","whole","whom","whose","why","will","willing","win","wish","with","within",
          "without","won't","wonder","would","wouldn't","write","work","x","y","yes","yet","you","you'd","you'll","you're","you've","your",
          "yours","yourself","yourselves","z","zero"]


#
#En ListDoc guardare tuplas con el formato: <id_doc,title,author,text>
#
ListDoc=[]

#
#En ListTerm guardare tuplas con el formato <term,[]>
#
ListTerm={}
ListTermAux=[]

ListMaxDoc=[]


def Cargar(set):
    with open('datasets/'+set+'.json') as file:
        data = json.load(file)
        
        #print(type(data))
        for i in data:
            if len(data[i]) < 2:
                tupla=(data[i]["id"],"","")
            else:
                try:
                    tupla=(data[i]["id"],data[i]["title"],data[i]["text"])
                except:
                    tupla=(data[i]["id"],data[i]["title"],data[i]["abstract"])

            #print(tupla)
            ListDoc.append(tupla)
            ListMaxDoc.append(0)
            #print(i)
            #print(data[i]["title"])
    
    
    for doc in ListDoc:
        id_doc=doc[0]
        title=doc[1].lower()
        text=doc[2].lower()
        new=title+" "+text
        cadena=new.split(' ')
        #print(cadena)
        #print(doc[0])
        maximo=0
        for term in cadena:
            t=term.split('.')
            t=t[0].split(',')
            if(t[0]!='' and not(inutiles.__contains__(t[0]))):
                if(not(ListTermAux.__contains__(t[0]))):
                    try:
                        num=int(t[0])
                        continue
                    except:
                        array=[0 for x in range(0,len(ListDoc))]
                        #array=np.zeros(len(ListDoc))
                        array[int(doc[0])-1]+=1
                        ListTerm[t[0]]=array
                        ListTermAux.append(t[0])
                else:
                    #print(int(doc[0])-1)
                    ListTerm[t[0]][int(doc[0])-1]+=1
                    if(ListTerm[t[0]][int(doc[0])-1]>maximo):
                        maximo=ListTerm[t[0]][int(doc[0])-1]
        ListMaxDoc[int(id_doc)-1]=maximo           
        #print(len(ListMaxDoc))

print(len(ListMaxDoc))




    
    

#print(" ")
#print(ListTerm["book"])
#for i in ListTerm["book"]:
#    print(i)

#print(len(ListTerm))
#data={}
#count=0
#for i in ListTerm:
 #   array=list(ListTerm[i])
 #   data[count]={
  #      'palabra':i,
 #       'frecuencia':array
 #   }
  #  count+=1


#with open('datasets/rel_ter_doc.json', 'w') as file:
#    json.dump(ListTerm, file, indent=32)



        
        
