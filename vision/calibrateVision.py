#Para modificar los parametros del color
file = open("colorVal.txt","r")
lowVal=[]
uppVal=[]
i=0
for line in file:
	print line
	if(i<3):
		lowVal.append(int(line))
	else:
		uppVal.append(int(line))
	i+=1
file.close()