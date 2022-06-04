print("\\Clear");

/*
MIT License

Copyright (c) 2021 Frederik Püffel f.puffel18@imperial.ac.uk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

//User interface
//Intro
#@ String (visibility=MESSAGE, value="<html><h1><font size=5 color=Green><i>Evolutionary Biomechanics Group</i></h1> <H2><font size=3>Imperial College London</H2><h1><font color=black>ImageJ Script Macro: Fibre seeds - Identifying muscle fibres from segmented image stacks</h1> <p1>Version: 1.0 (13/12/2021)</p1> <H2><font size=3>Created by Frederik Püffel</H2> <p1><font size=2> contact f.puffel18@imperial.ac.uk</p1> <br/> <br/> <p1><font size=3 \b i> This script uses tomographic image stacks of fibrous tissue and identifies the number and attachment points of individual fibres. <br/> It is initially designed for ant head muscles. </p1> <br/> <br/><html>") intro_msg1
#@ String (visibility=MESSAGE, value="<html> The identification process is divided into three steps: <br/> First, the attachment segmentation is dilated. <br/> Second, the interesections between the dilated structure and fibres are calculated. <br/> Third, after optional post-processing, a 3D particle analysis is run on the intersections. <br/> The resulting centre-of-masses of such intersections can be used to run fibre tracing algorithms. <br/> A random subset of the identified fibre seeds can be exported for manual tracking. <html>") intro_msg2

//File import
#@ String (visibility=MESSAGE, value="image stacks need to be imported:") file_msg
#@ File (label="1. Tomographic grayscale image", style="file") stackTomo
#@ File (label="2. Fibre segmentation(left)", style="file") stackFibre
#@ File (label="3. Fibre segmentation(right)", style="file") stackFibre_1
#@ File (label="4. The fibre attachment segmentation(head capsule)", style="file")stackCut
#@ File (label="5. The left apodeme tissue segmentation", style="file") Apodeme_left
#@ File (label="6. The right apodeme tissue segmentation", style="file")  Apodeme_right

//Parameters
//Dilation
#@ String (visibility=MESSAGE, value="First, the attachment segmentation will be dilated.") dil_msg1
#@ String (visibility=MESSAGE, value="Please select the number of dilation steps - (2/3) of the fibre diameter proved suitable.") dil_msg2
#@ Integer (label="Number of dilation steps", style="slider", min=0, max=50, stepSize=1) iter
//Erosion
#@ String (visibility=MESSAGE, value="Next, the intersection between dilated attachment and fibre tissue will be calculated.") ero_msg1
#@ String (visibility=MESSAGE, value="For some scans, an additional erosion step resulted in better fibre detection.") ero_msg2
#@ String (choices={"Yes", "No"}, style="radioButtonHorizontal") Erosion
//Erosion
#@ String (visibility=MESSAGE, value="For scans of lower quality, an additional thresholding step further improved the detection.") thr_msg1
#@ String (choices={"Yes", "No"}, style="radioButtonHorizontal") Thresholding

//Manual validation
#@ String (visibility=MESSAGE, value="A subset of the identified fibres can be exported for manual tracking.") val_msg1
#@ String (choices={"Yes", "No"}, style="radioButtonHorizontal") Export
#@ Integer (label="Number of fibres", style="slider", min=5, max=50, stepSize=5) sub


//Preview
#@ String (visibility=MESSAGE, value="To have a preview of the generated seeds in a slice of image of the stack.") pre_msg1
#@ String (choices={"Yes", "No"}, style="radioButtonHorizontal") Preview
#@ Integer (label="Slice number", style="slider", min=1, max=600, stepSize=1) sli

//Save data
#@ File (label="Select a directory for file saving", style="directory") saveDir




//Writes to log window script title and acknowledgement
scripttitle="Fibre seeds - Identifying muscle fibres from segmented image stacks";
version="1.0";
date="13/12/2021";

print("");
print("FIJI Macro: "+scripttitle);
print("Version: "+version+" Version Date: "+date);
print("Imperial College London: Evolutionary Biomechanics Group");
print("By Frederik Püffel (2021) f.puffel18@imperial.ac.uk")
print("");
getDateAndTime(year, month, week, day, hour, min, sec, msec);
time = newArray(hour, min, sec);
for (i=0; i<time.length; i++) {
	if (time[i] < 10) {
		time[i] = "0" + time[i];
	}
}
print("Script Run Date: "+day+"/"+(month+1)+"/"+year+"  Time:" +time[0]+":"+time[1]+":"+time[2]);
print("");

//Parameters
print("Number of dilation steps: " + iter);
print("");
print("Perform erosion? " + Erosion);
print("");
print("Perform thresholding? " + Thresholding);
print("");
print("Export subset of seeds for manual tracking? " + Export);
print("");
print("Files saved in: " + saveDir);
print("");
print("Preview:" + Preview + sli);
print("");


/*

//Fibre seed identification
//Open files
open(stackTomo);
open(stackFibre);
open(stackCut);


//Get image names
imT = File.getName(stackTomo);
imF = File.getName(stackFibre);
imC = File.getName(stackCut);



while(Preview == "Yes") {

	selectWindow(imC);
	run("Duplicate...", "duplicate range = sli");
	imCscreenshot = getTitle();

	selectWindow(imF);
	run("Duplicate...", "duplicate range = sli");
	imFscreenshot = getTitle();

	selectWindow(imCscreenshot);
	run("Options...", "iterations=" + iter + " count=1 black do=Dilate stack");
	imageCalculator("AND create stack", imCscreenshot, imFscreenshot);

	Dialog.create("Change dilation factor");
		Dialog.addMessage("Change the dilation factror:");
		Dialog.addCheckbox("Preview", true);
		Dialog.addSlider("Number of dilation steps", 0, 50, iter);
		Dialog.addSlider("Slice number",1, 600, sli);
	Dialog.show();

	Preview = Dialog.getCheckbox();
	if(Preview == 1){
		Preview = "Yes";
	}
	else{
		Preview = "False";
	}
	iter = Dialog.getNumber();
	sli = Dialog.getNumber();
	close();
	close();
	close();
	
}


//-----------------------------------------------------------------
//left
//Dilate attachment structure
selectWindow(imC);
print("Perform dilation...");
run("Options...", "iterations=" + iter + " count=1 black do=Dilate stack");
print("...done!");

//Calculate intersections
print("Calculate intersections...");
imageCalculator("AND create stack", imC, imF);
print("...done!");

//Perform erosion (optional)
minSize = 10;
if (Erosion == "Yes") {
	print("Perform erosion...");
	minSize = 1; //if an erosion was performed, small segmentation errors are most likely gone, so the minimun particle size can be set down
	run("Options...", "iterations=1 count=1 black do=Erode stack");	
	print("...done!");
}


//Perform thresholding (optional)
if (Thresholding == "Yes") {
	print("Perform thresholding...");
	imageCalculator("AND create stack", "Result of "+imC, imT);
	setAutoThreshold("Default dark");
	run("Convert to Mask", "method=Default background=Dark calculate black");
	print("...done!");
}


//3D particle analysis
saveAs(saveDir + "/cma_l.tif");
print("Perform 3D analysis...");
print("Exclude particles below: "+ minSize +" pixels");
run("3D Objects Counter", "min.="+ minSize +" exclude_objects_on_edges statistics summary");
fname = saveDir + "/fibreSeeds_l.csv";
tname = File.getName(fname);
saveAs("Results", fname);
run("Close");
print("...done!");




if (Export == "Yes") {
	print("Export subset of "+ sub + " fibres...");
	//Open data as results
	run("Table... ", "open="+fname);
	Table.rename(tname, "Results");
	//Extract lengths of results
	l = getValue("results.count");
	//Define array for indices
	set = newArray(sub);
	//Generate random set of indices
	Table.create("Subset");
	for (i = 0; i < sub; i++) {
		isUnique = false;
		while (isUnique == false) {
			//Create index
			r = random;
			s = round(r*l);
			//Subtract 1 in case the index just exceeds the length of the table
			if (s == l) {
				s = s-1;
			}
			set[i] = s;
			//Check if index is already used
			dif = newArray(i);
			for (j = 0; j < i; j++) {
				dif[j] = abs(set[j] - s);
			}
			if (i == 0) {
				isUnique = true;
			}
			if (i != 0) {
				Array.sort(dif);
				if (dif[0] > 0) {
					isUnique = true;
				}
			}
		}
	}
	for (i = 0; i < sub; i++) {
		Table.set("Index", i, set[i]);
		Table.set("XM", i, getResult("XM", set[i]));
		Table.set("YM", i, getResult("YM", set[i]));
		Table.set("ZM", i, getResult("ZM", set[i]));
	}
	Table.sort("Index");
	Table.save(saveDir + "/l_subSet_"+year+"_"+(month+1)+"_"+day+"_"+time[0]+"_"+time[1]+"_"+time[2]+".csv");
	print("...done!");
}
run("Close All");


//-----------------------------------------------------------------
//right


open(stackTomo);
open(stackFibre_1);
open(stackCut);


//Get image names
imT = File.getName(stackTomo);
imF = File.getName(stackFibre_1);
imC = File.getName(stackCut);

selectWindow(imC);
print("Perform dilation...");
run("Options...", "iterations=" + iter + " count=1 black do=Dilate stack");
print("...done!");

//Calculate intersections
print("Calculate intersections...");
imageCalculator("AND create stack", imC, imF);
print("...done!");

//Perform erosion (optional)
minSize = 10;
if (Erosion == "Yes") {
	print("Perform erosion...");
	minSize = 1; //if an erosion was performed, small segmentation errors are most likely gone, so the minimun particle size can be set down
	run("Options...", "iterations=1 count=1 black do=Erode stack");	
	print("...done!");
}


//Perform thresholding (optional)
if (Thresholding == "Yes") {
	print("Perform thresholding...");
	imageCalculator("AND create stack", "Result of "+imC, imT);
	setAutoThreshold("Default dark");
	run("Convert to Mask", "method=Default background=Dark calculate black");
	print("...done!");
}


//3D particle analysis
saveAs(saveDir + "/cma_r.tif");
print("Perform 3D analysis...");
print("Exclude particles below: "+ minSize +" pixels");
run("3D Objects Counter", "min.="+ minSize +" exclude_objects_on_edges statistics summary");
fname = saveDir + "/fibreSeeds_r.csv";
tname = File.getName(fname);
saveAs("Results", fname);
run("Close");
print("...done!");




if (Export == "Yes") {
	print("Export subset of "+ sub + " fibres...");
	//Open data as results
	run("Table... ", "open="+fname);
	Table.rename(tname, "Results");
	//Extract lengths of results
	l = getValue("results.count");
	//Define array for indices
	set = newArray(sub);
	//Generate random set of indices
	Table.create("Subset");
	for (i = 0; i < sub; i++) {
		isUnique = false;
		while (isUnique == false) {
			//Create index
			r = random;
			s = round(r*l);
			//Subtract 1 in case the index just exceeds the length of the table
			if (s == l) {
				s = s-1;
			}
			set[i] = s;
			//Check if index is already used
			dif = newArray(i);
			for (j = 0; j < i; j++) {
				dif[j] = abs(set[j] - s);
			}
			if (i == 0) {
				isUnique = true;
			}
			if (i != 0) {
				Array.sort(dif);
				if (dif[0] > 0) {
					isUnique = true;
				}
			}
		}
	}
	for (i = 0; i < sub; i++) {
		Table.set("Index", i, set[i]);
		Table.set("XM", i, getResult("XM", set[i]));
		Table.set("YM", i, getResult("YM", set[i]));
		Table.set("ZM", i, getResult("ZM", set[i]));
	}
	Table.sort("Index");
	Table.save(saveDir + "/l_subSet_"+year+"_"+(month+1)+"_"+day+"_"+time[0]+"_"+time[1]+"_"+time[2]+".csv");
	print("...done!");
}
run("Close All");


*/
//get text images of seeds and fibre
//left seed
folder = saveDir + "/im_s_l";
File.makeDirectory(folder);

open(saveDir + "/cma_l.tif")
open(stackTomo)
imT = File.getName(stackTomo);
selectWindow(imT);
imageCalculator("Subtract create stack", "cma_l.tif",imT);
selectWindow("Result of cma_l.tif");
a = getTitle();
for (i = 1; i <= nSlices; i++) {
	setSlice(i);
    saveAs("Text Image",  saveDir+"/im_s_l/im_s_"+i+".txt");
}
run("Close All");

//right seed
folder = saveDir + "/im_s_r";
File.makeDirectory(folder);

open(saveDir + "/cma_r.tif")
open(stackTomo)
imT = File.getName(stackTomo);
selectWindow(imT);
imageCalculator("Subtract create stack", "cma_r.tif",imT);
selectWindow("Result of cma_r.tif");
a = getTitle();
for (i = 1; i <= nSlices; i++) {
	setSlice(i);
    saveAs("Text Image",  saveDir+"/im_s_r/im_s_"+i+".txt");
}
run("Close All");

//left muscle
folder = saveDir + "/im_m_l";
File.makeDirectory(folder);

open(stackFibre)
open(stackTomo)
imT = File.getName(stackTomo);
imF =  File.getName(stackFibre);
imageCalculator("Subtract create stack", imF,imT);
selectWindow("Result of "+imF);
a = getTitle();
for (i = 1; i <= nSlices; i++) {
	setSlice(i);
    saveAs("Text Image",  saveDir+"/im_m_l/im_m_"+i+".txt");
}
run("Close All");

//right fibre

folder = saveDir + "/im_m_r";
File.makeDirectory(folder);

open(stackFibre_1)
open(stackTomo)
imT = File.getName(stackTomo);
imF =  File.getName(stackFibre_1);
imageCalculator("Subtract create stack", imF,imT);
selectWindow("Result of "+imF);
a = getTitle();
for (i = 1; i <= nSlices; i++) {
	setSlice(i);
    saveAs("Text Image",  saveDir+"/im_m_r/im_m_"+i+".txt");
}
run("Close All");

//get apodeme measurements
run("Set Measurements...", "area center perimeter fit stack redirect=None decimal=9");
open(Apodeme_left);
apo_l = File.getName(Apodeme_left);
run("Fill Holes", "stack");
run("Analyze Particles...", "display include stack");
saveAs("Results", saveDir + "/ca_l_stack.csv");
run("Clear Results");
run("3D Objects Counter", "min.=100 exclude_objects_on_edges statistics summary");
saveAs("Results", saveDir + "/ca_l_3D.csv");
close();
run("Clear Results");

open(Apodeme_right);
apo_r = File.getName(Apodeme_right);
run("Fill Holes", "stack");
run("Analyze Particles...", "display include stack");
saveAs("Results", saveDir + "/ca_r_stack.csv");
run("Clear Results");
run("3D Objects Counter", "min.=100 exclude_objects_on_edges statistics summary");
saveAs("Results", saveDir + "/ca_r_3D.csv");
close();
run("Clear Results");


