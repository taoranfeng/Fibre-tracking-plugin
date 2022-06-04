from ij import IJ
from ij.gui import GenericDialog
from ij.io import Opener
import os, csv, math, random
import glob
import codecs
from ij.gui import WaitForUserDialog


IJ.run("FibreSeeds ")
mywit = WaitForUserDialog("Please select the folder where all data files are saved (including the im_m and im_s folder)")
mywit.show()
DIR = IJ.getDirectory("Choose the directory ")

csv_image_notes = DIR + "pca.csv"
csv_apos_r = DIR + "/ca_r_3D.csv"
csv_apos_l = DIR + "/ca_l_3D.csv"


#parameters
iterations= 1000
res = 6.5428
dia = 5
apos = ["ca_l","ca_r"]
muscles = ["cm_l","cm_r"]
muscle_seeds = ["cma_l","cma_r"]
muscle = ["l","r"]
pw =1


#read csv function
def openCSV(filepath, header_length =1):
	with open(filepath,'r') as csvfile:
		reader = csv.reader(csvfile, delimiter=',' , quotechar="\"")
		header_rows = [reader.next() for i in xrange(header_length)]
		rows = [columns for columns in reader]
		return header_rows, rows


#functions 
#1.start_pos get alternative starting position within the bounding box of the respective particle

def start_pos(seed):
	start_alt = []
	x_range = int(seed[7]/2)
	y_range = int(seed[8]/2)
	z_range = int(seed[9]/2)

	for x in range(int(seed[7])):
		for y in range(int(seed[8])):
			for z in range(int(seed[9])):
				x_sh = x - x_range
				y_sh = y - y_range
				z_sh = z - z_range
				s_alt = [z_sh, y_sh, x_sh]
				start_alt.append(s_alt)
	
	random. shuffle(start_alt)
	start_alt.append([0,0,0])
	start_alt[::-1]

	return start_alt



##	Find the appropriate search cone
def what_a(it):
	a = 10 - it/iterations*10
	if a < 0.1:
		a = 0.1
	return a

def rotx(points, angles):
	 mrot = [[1,0,0],[0, math.cos(angles), -math.sin(angles)], [0,math.sin(angles), math.cos(angles)]]
	 result = []
	 for j in range(3):
	 	res = mrot[j][0]*points[0]+mrot[j][1]*points[1]+mrot[j][2]*points[2]
	 	result.append(res)
	 return result

def roty(points, angles):
    mrot =[[math.cos(angles),0, -math.sin(angles)],[0,1,0], [math.sin(angles),0, math.cos(angles)]]
    result = []
    for j in range(3):
    	res = mrot[j][0]*points[0]+mrot[j][1]*points[1]+mrot[j][2]*points[2]
    	result.append(res)
    return result

def rotz(points, angles):
    mrot = [[math.cos(angles), math.sin(angles), 0], [-math.sin(angles), math.cos(angles), 0],[0,0,1]]
    result = []
    for j in range(3):
    	res = mrot[j][0]*points[0]+mrot[j][1]*points[1]+mrot[j][2]*points[2]
    	result.append(res)
    return result

	 

def d_gaus_a(dir_b,a):
	angle1=random.normalvariate(0, a)*(math.pi)/180
	angle2=random.normalvariate(0, a)*(math.pi)/180
	angle3=random.normalvariate(0, a)*(math.pi)/180
	dir_b = rotx(dir_b, angle1)
	dir_b = rotx(dir_b, angle2)
	dir_b = rotz(dir_b, angle3)
	return(dir_b)


def getvalue(m,x,y,z):
	count = 0 
	with open(DIR + 'im_m_'+m+'/im_m_'+z+'.txt') as f:
		for line in f:
			if count == x:
				inner_list = [elt.strip('u\n') for elt in line.split('\t')]
				px = inner_list[y]
				return px
			else:
				count+=1

def getvalue_seed(m,x,y,z):
	count = 0 
	with open(DIR + 'im_s_'+m+'/im_s_'+z+'.txt') as f:
		for line in f:
			if count == x:
				inner_list = [elt.strip('u\n') for elt in line.split('\t')]
				px = inner_list[y]
				return px
			else:
				count+=1
	

#----------------------------------------------------------------------------------------------------
#apopdeme - PCA
#----------------------------------------------------------------------------------------------------
#if os.path.exists(csv_image_notes):
#	header_rows,ad = openCSV(csv_image_notes, header_length =1)
#	header = header_rows[0]
#else:
#	print('failed to open file')


#for i in range(len(ad[0])):
#	for j in range(len(ad)):
#		ad[j][i] = float(ad[j][i])
	
#for c in ad:
	#delete columns of Perim., Major, Minor, Angle
#	del c[4:8]
#	del c[0]
	# subtract 1 from slice number as it starts with 1 , unlike z)
#	c[3]= int(c[3])-1
	#convert slice number to mm
#	c[3]= int(c[3])*res/1000
	
#ad_o = ad
#row_count = len(ad)
#i = 0

#while i < row_count -1:
#	r1 =ad[i][3]
#	r2 =ad[i+1][3]
#	if r1 == r2:
#		#getting the coordinates of both COMs
#		x_1 = float(ad[i][1])
#		x_2 = float(ad[i+1][1])
#		y_1 = float(ad[i][2])
#		y_2 = float(ad[i+1][2])
#		#the area(weight)
#		w_1 = float(ad[i][0])
#		w_2 = float(ad[i+1][0])
#		#recalculate COM
#		xm = (x_1*w_1 + x_2*w_2)/(w_1+w_2)
#		ym = (y_1*w_1 + y_2*w_2)/(w_1+w_2)
#		#change the coordinates in the table to the combined COM
#		ad[i][0] = w_1+w_2
#		ad[i][1] = xm
#		ad[i][2] = ym
#		#delete the previous coordinate
#		ad.pop(i+1)
#		row_count = len(ad)
#		i -= 1
#	i+=1
#
#extract cyz coordinates
#data = ad
#for c in data:
#	del c[0]

#datamean = [sum(x)/len(x) for x in zip(*data)]

#Transpose data to origin to perform PCA - TBC
#for i in range(len(data[0])):
#	for j in range(len(data)):
#		data[j][i] = data[j][i] - datamean[i]




pca=[[0.01145384,-0.0983256, 0.99508838],[0.01764476,-0.09052018,0.9957383]]
#------------------------------------------------------------------------------------------
#apodeme
#------------------------------------------------------------------------------------------

apo_3D = []
for a in apos:
	#Combine individual apodeme 3D particles and extract centre-of-mass
	#open excel file
	if os.path.exists(csv_apos_l):
		apos_rows, apos_ad = openCSV(csv_apos_l, header_length =1)
		#change it from a list of  list to list
		aposheader = apos_rows[0]
	else:
		print('failed to open file')

#change all content to float

	for i in range(len(apos_ad[0])):
		for j in range(len(apos_ad)):
			apos_ad[j][i] = float(apos_ad[j][i])



#remove junk content
	list_of_apos = []
	for i in range(len(apos_ad)+1):
		list_of_apos.append([' ',' ',' ',' ',' '])

	for i in range(len(aposheader)):
		if aposheader[i] == "XM":
			list_of_apos[0][0] = "XM"
			for j in range(len(apos_ad)):
				list_of_apos[j+1][0] = apos_ad[0][i]
		elif aposheader[i] == "YM":
			list_of_apos[0][1] = "YM"
			for j in range(len(apos_ad)):
				list_of_apos[j+1][1] = apos_ad[0][i]
		elif aposheader[i] == "ZM":
			list_of_apos[0][2] = "ZM"
			for j in range(len(apos_ad)):
				list_of_apos[j+1][2] = apos_ad[0][i]
		elif aposheader[i] == 'Volume (mm^3)':
			list_of_apos[0][3] = 'Volume (mm^3)'
			for j in range(len(apos_ad)):
				list_of_apos[j+1][3] = apos_ad[0][i]
		elif aposheader[i] == 'Surface (mm^2)':
			list_of_apos[0][4] = 'Surface (mm^2)'
			for j in range(len(apos_ad)):
				list_of_apos[j+1][4] = apos_ad[0][i]

#check if there is more than 1 apodeme
#combine apodemes together if more than 1
	if len(apos_ad) > 1:
		print("The no. of apodeme is: {} ".format(len(apos_ad)))
	#combine apodemes - to be done
	elif len(apos_ad)==1 :
		print("There is only one apodeme existed")

	apo_3D.append(list_of_apos[1])



#------------------------------------------------------------------------------------------
#seed
#------------------------------------------------------------------------------------------

#for nr,v in enumerate(muscles):
for count, m in enumerate(muscle):
	fname = DIR + 'fibreSeeds_'+m+'.csv'
	if os.path.exists(fname):
		seed_header, seedlist = openCSV(fname, header_length =1)
		#change it from a list of  list to list
		seedheader = seed_header[0]
	else:
		print('failed to open file:{}'.format(fname))

	#select contend in col [0,16,17,18,19,20,21,22,23,24]
	for row in seedlist:
		del row[1:16]
		row.append(0)

	##change all content to float

	for i in range(len(seedlist[0])):
		for j in range(len(seedlist)):
			seedlist[j][i] = float(seedlist[j][i])

	s_mins = []
	for fbr in range(len(seedlist)):
		empty_list= []
		for nbr in range(len(seedlist)):
			if fbr != nbr:
				x_s = seedlist[fbr][1] - seedlist[nbr][1]		
				y_s = seedlist[fbr][2] - seedlist[nbr][2]
				z_s = seedlist[fbr][3] - seedlist[nbr][3]
				s_s = x_s**2+y_s**2+z_s**2
				s_s = math.sqrt(s_s)
				empty_list.append(s_s)
        	seed_min = min(empty_list)
        	s_mins.append(seed_min)

	print("for the left part:")
	print("--------------------------------------------------------")
	print('Minimum seed distance:{} '.format(str(sum(s_mins)/len(s_mins))))

	##set cancel criterion
	cc = int(round((sum(s_mins)/len(s_mins)-dia)/4))
	print('Cancel criterion (numer of pixels allowed to be unsegmented):{} '.format(cc))

	#convert seed and apos to rounded number
	for i in range(len(seedlist[0])):
		for j in range(len(seedlist)):
			seedlist[j][i] = int(round(seedlist[j][i]))
	for i in range(len(apo_3D[0])):
		for j in range(len(apo_3D)):
			apo_3D[j][i] = int(round(apo_3D[j][i]))
	
	


	#estimate pennation angle and initial directions by connecting seeds to apodeme COM
	#get initial direction and fibres lengths
	pca_temp = pca[count]
	pA = []
	direc = []
	lengths = []

	apo_temp = apo_3D[1][0:3]
	for seed_nr, seed in enumerate(seedlist):
		seed_temp = seed[1:4]	
		vec = [a - b for a, b in zip(apo_temp, seed_temp)]
		vec_pca_dot = sum(x*y for x,y in zip(vec,pca_temp))
		vec_norm = math.sqrt(vec[0]*vec[0]+vec[1]*vec[1]+vec[2]*vec[2])
		angle = (math.acos(vec_pca_dot/vec_norm))*180/(math.pi)
		e_dir = [v/vec_norm for v in vec]
		pA.append(angle)
		lengths.append(vec_norm)
		direc.append(e_dir)
		seedlist[seed_nr][-1] = seed_nr




	#calculate fibre orientations

	dir_bs = []
	penAs = []
	flengths = []
	heights = []
	cross_as = []
	d_cycles =[]
	
	list_of_list_of_list = []
	#for temp in range(99,300):
	# 	temp+=1
	#	print(temp)
	#	list_of_lists = []
	#	with open(DIR + 'im_m_l/im_m_'+str(temp)+'.txt') as f:
	#		for line in f:
	#			inner_list = [elt.strip('u\n') for elt in line.split('\t')]
	#			list_of_lists.append(inner_list)
	#	f.close()
	#	list_of_list_of_list.append(list_of_lists)


	z_list  = []
	for fbr in range (len(seedlist)):
		start_opt = start_pos(seedlist[fbr])

		for st_opt in start_opt:
			
			pxs_b = []
			qc_b = 0
			it = 0
			flength = []
			dir_r = direc[fbr]
			

			while it <iterations:
				pxs = []

				for i in range(int(round(lengths[fbr]))):
					step = [int(i * dir_r_temp) for dir_r_temp in dir_r]
					z = str( seedlist[fbr][3]+step[2]+st_opt[2])
					x = seedlist[fbr][2]+step[1]+st_opt[1]
					y = seedlist[fbr][1]+step[0]+st_opt[0]

					#if z>=100 and z<=300:
					#	px = list_of_list_of_list[z-100][x][y]
					#else:
					#list_of_lists = []
					#with open(DIR + 'im_m_l/im_m_'+z+'.txt') as f:
					#	for line in f:
					#		inner_list = [elt.strip('u\n') for elt in line.split('\t')]
					#		list_of_lists.append(inner_list)
					#imp = Opener().openImage(DIR+"/im_m.tif",z)
					#v= imp.getPixel(x,y)
					#imp.close()
					#px = int(v[0])
					px = getvalue(m,x,y,z)

					pxs.append(int(px))
					
					pxs_cc = pxs[-cc:]
					if sum(pxs_cc)/len(pxs_cc) == 0:
						break
					
				mean = sum(pxs) / len(pxs)
				var = sum((l-mean)**2 for l in pxs) / len(pxs)
				st_dev = math.sqrt(var)
				if st_dev == 0:
					qc = 0
				else:
					qc = len(pxs)/(st_dev**pw)

				if qc >= qc_b: #if a better fibre is found, we use the current direction as the new best
					dir_b = dir_r
					pxs_b = pxs
					qc_b = qc

				a = what_a(it)
				dir_r = d_gaus_a(dir_b,a)
				it += 1

			height_i = [] #part of the muscle cylinder that goes inside from its COM
			height_o = [] #part of the muscle cylinder that goes outside from its COM - This part needs to be added to the total fibre length
			bound_d = ((seedlist[fbr][7]**2+seedlist[fbr][8]**2+seedlist[fbr][9]**2)**(1/2))
			vol = seedlist[fbr][0]

			for i in range(int(round((bound_d)))):
				step = [int(i * dir_r_temp) for dir_r_temp in dir_r]
				z = str(seedlist[fbr][3]+step[2]+st_opt[2])
				x = seedlist[fbr][2]+step[1]+st_opt[1]
				y = seedlist[fbr][1]+step[0]+st_opt[0]
				#imp = Opener().openImage(DIR+"/im_s.tif",z)
				#v= imp.getPixel(x,y)
				#imp.close()
				#px = int(v[0])

				px = getvalue_seed(m,x,y,z)
				if px == 0:
					break
				else:
					height_o.append(px)
			
			height = (len(height_i) + len(height_o)-1)*res
			
			
			if height < res:
					height = res

			
			cross_a = vol/height
			d_cyl = (cross_a/math.pi)**(1/2)*2
			dir_pca_dot = sum(x*y for x,y in zip(dir_b,pca_temp))
			penA = math.acos(dir_pca_dot)*180/math.pi
			flength = len(pxs_b)-cc+len(height_o)-1

			if flength < 0:
				flength = 0
			if flength > dia*2:
				break

			
		pxsmean = sum(pxs) / len(pxs)
		print('Fibre nr: ' + str(fbr+1) + '/' +str(len(seedlist)) + '; Quality criterion: ' + str(qc_b) + '; Fibre length: ' + str(flength) + '; Mean gray value: ' + str(pxsmean))
		flengths.append(flength)
		heights.append(height)
		cross_as.append(cross_a)
		d_cycles.append(d_cyl)
		penAs.append(penA)
		dir_bs.append(dir_b)
		print("next")		
			
			

	#flip angles
	pamean = sum(pA) / len(pA)
	if pamean > 90:
		for angle_nr, angle in enumerate(penAs):
			angle = 180 - angle
			penAs[angle_nr] = angle
		for angle_nr, angle in enumerate(pA):
			angle = 180 - angle
			pA[angle_nr] = angle

	#nonZ = 0
	#for fl in flengths:
	#	if fl > 0:
	#		nonZ +=1
	#if len(flengths) > 0:
	#	print("Fraction of non zero-length fibres: " + str(nonZ/len(flengths)))

	print('Average fibre length: ' + str((sum(flengths)*int(res))/ len(flengths)) + ' µm')
	print('Average pennation angle: ' + str(sum(penAs) / len(penAs))  + ' °')
	print('Number of fibres: ' + str(len(penAs)))



	#summerise data
	
		
		
	 
	
	
	

	