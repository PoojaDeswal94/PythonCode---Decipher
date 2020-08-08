import matplotlib.pyplot as plt

def order_fct(input_list):
    for j in range(len(input_list)-1):
        smallest=j
        for i in range(j+1 , len(input_list)):
            if input_list[i]<input_list[smallest]:
                smallest=i
                
        input_list[j],input_list[smallest]=input_list[smallest],input_list[j]

mylist= [100,20,45,36,72,1,12,7,33,61,93]
order_fct(mylist)
print(mylist)

class Reader:
    def __init__(self, filename ):
        self.file= open(filename, "r+")
    def create_dict(self):
        import string
        base=list(string.ascii_lowercase)
        self.dict1={}
        list1=[]
        for i in base:
            self.dict1[i]=0
        for line in self.file:
            for char in line:
                y = char.lower()
                list1.append(y)
        for i in list1:
            if i in self.dict1.keys():
                self.dict1[i]+=1
        
        return(self.dict1)  
class Decipher(Reader):
    def __init__(self,filename, codefile, format):
        Reader.__init__( self,filename)
        self.coded=  open(codefile, "r+")
        #self.string= string
        self.hist= list()
        self.ordered=list()
        self.deciphed= ""
        self.format= format
        self.entropy=  None
        # self.dict is already intialized in above parent class already inherited no need to initalize again
        
    def create_hist(self):
        for values in self.dict1.values():
            self.hist.append(values)
        return self.hist
    
    def create_ordered(self):
        order=sorted(self.dict1.items(), key=lambda t: t[1])
        for i in range(0,len(order)):
            self.ordered.append(order[i][0])
        #sorted(self.dict1.items(), key=lambda t: t[1], reverse = True)  for decending order
        return self.ordered
    def decipher(self):
        import string
        base1=list(string.ascii_lowercase)
        frequent_element= self.ordered[-1]
        vardict={}
        listf= []
        listx=[]
        given_key= 'z'
        #the given key should be updated here everytime for a new cipher
        for i in range(0, len(base1)):
            vardict[i]=base1[i]
        for i in range (0, len(vardict)):
            if vardict[i]== given_key :
                locationgiven = i
                break
        for i in range (0, len(vardict)):
            if vardict[i]== frequent_element:
                locationkey = i
                break
        if locationgiven>locationkey:location= locationgiven-locationkey
        elif locationgiven<locationkey:location= 26-locationkey + locationgiven
        else: location=0
        for line in self.coded:
            for char in line:
                listx.append(char)
        count=0
        for i in range(0,len(listx)):
            if (listx[i].isupper())==True:
                count=1
                listx[i]=listx[i].lower()
            else: count=0
            if listx[i] in vardict.values():
                for j in range(0, 26):
                    if vardict[j]==listx[i]:
                        final= location + j
                        if final>25:final= final-26
                        if count==1: 
                            listf.append(vardict[final].upper())
                        else:listf.append(vardict[final])
                        break    
            else: 
                listf.append(listx[i])
            
        self.deciphed=(''.join(listf))
            
        return(self.deciphed)
 
    
    def write_code(self):
        import csv
        if self.format=='txt':
            f=open("decoded.txt", "a+")
            n = f.write(self.deciphed)
            f.close()
        elif self.format=='csv':
            self.deciphed.replace('/n',"")
            li = list(self.deciphed.split(" ")) 
            with open('decoded.csv', 'w') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                wr.writerow(li)
 
    
    def plot_pie(self):
        import matplotlib.pyplot as plt
        import string

        labels = list(string.ascii_uppercase)

        fig1, ax1 = plt.subplots(figsize=(6, 5))
        fig1.subplots_adjust(0.3,0,1,1)


        theme = plt.get_cmap('bwr')
        ax1.set_prop_cycle("color", [theme(1. * i / len(self.hist)) for i in range(len(self.hist))])

        _, _ = ax1.pie(self.hist, startangle=90)

        ax1.axis('equal')

        total = sum(self.hist)
        plt.legend(
        loc='upper left',
        labels=['%s, %1.1f%%' % (
        l, (float(s) / total) * 100) for l, s in zip(labels, self.hist)],
        prop={'size': 11},
        bbox_to_anchor=(0.0, 1),
        bbox_transform=fig1.transFigure
        )
        plt.show()

    def compute_entropy(self):
        import collections
        import math
        import string
        base1=list(string.ascii_lowercase)
        s=[]
        for i in range(0,26):
            s.append(self.dict1[base1[i]])
        probabilities = [n_x/len(s) for x,n_x in collections.Counter(s).items()]
        e_x = [-p_x*math.log(p_x,2) for p_x in probabilities]    
        self.entropy= sum(e_x)
        return self.entropy
    
    
    
    
    def plot_hist(self):
        import matplotlib.pyplot as plt
        plt.bar(self.dict1.keys(), self.dict1.values())
        plt.show()
    
    
    
            
files=Decipher("text10.txt","text20.txt",'csv')
files.create_dict()
files.dict1
files.create_hist()
files.hist
files.create_ordered()
files.decipher()
files.write_code()
files.plot_pie()
print(files.compute_entropy())
files.plot_hist()
