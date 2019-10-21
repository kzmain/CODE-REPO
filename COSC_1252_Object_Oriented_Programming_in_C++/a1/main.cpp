#include <iostream>
#include <list>
#include <set>
#include <vector>
#include <map>
#include <fstream>
#include <boost/tokenizer.hpp>
#include <boost/token_functions.hpp>
#include <boost/token_iterator.hpp>
/*****************************************************************\
*
*         Course code: COSC1252/1254
*         Student Number: s3560808
*         Date: 08.2017
*
*****************************************************************/
#include <string>
#include <sstream>
#include "./datastructure/dstru.h"
#include <time.h>
using namespace std;

//Process commands
int processCommand(int argc, char *argv[], int* mode, dstru* txtDstru, dstru* dictDstru, dstru* outDstru)
{
    int num=0;
    for(int i=0;i<argc;++i)
    {
        string temp="";
        stringstream ss;
        //Initial outstream
        if(strcmp(*(argv+i),"-o")==0)
        {
            ss<<(*(argv+i+1));
            ss>>temp;
            outDstru->outstream.open(temp);
            ++num;
        }
        //Initial input passage
        else if(strcmp(*(argv+i),"-t")==0)
        {
            ss<<(*(argv+i+1));
            ss>>temp;
            txtDstru->instream.open(temp);
            ++num;
        }
        //Initial input dict
        else if(strcmp(*(argv+i),"-d")==0)
        {
            ss<<(*(argv+i+1));
            ss>>temp;
            dictDstru->instream.open(temp);
            ++num;
        }
        //Initial modes
        else if(strcmp(*(argv+i),"-s")==0)
        {
            ss<<(*(argv+i+1));
            ss>>temp;
            if(temp.compare("list")==0){
                *mode=1;
            }
            else if(temp.compare("vector")==0){
                *mode=2;
            }
            else if(temp.compare("set")==0){
                *mode=3;
            }
            else if(temp.compare("custom_list")==0){
                *mode=4;
            }
            else if(temp.compare("custom_tree")==0){
                *mode=5;
            }
            else{
                
            }
            ++num;
        }
    }
    //If uncorrect commands return false
    if(num!=4){
        cout<<"Invalid input argument\n";
        return 1;
    }
    return 0;
}

int main(int argc, char *argv[])
{  

    //Input file & output files
    dstru outDstru;
    dstru txtDstru;
    dstru dictDstru;
    //Mode select
    int mode=0;
	clock_t startTime,afterInput, aftercompare;  
    startTime = clock(); 
    int checker = processCommand(argc, argv, &mode, &txtDstru, &dictDstru, &outDstru);
    if(checker==1){
        return EXIT_FAILURE;
    }
    checker = txtDstru.processInputFile(mode);
    if(checker==1){
        cout<<"Invalid input txt file\n";
        return EXIT_FAILURE;
    }
    checker = dictDstru.processInputFile(mode);
	afterInput = clock(); 
    if(checker==1){
        cout<<"Invalid dict txt file\n";
        return EXIT_FAILURE;
    }
    outDstru.stringCompare(mode, &txtDstru, &dictDstru, &outDstru);
	aftercompare = clock();
	cout<<"Input time is: "<<(double)(afterInput - startTime) / CLOCKS_PER_SEC << "s" << endl; 
	cout<<"Compare time is: "<<(double)(aftercompare - afterInput) / CLOCKS_PER_SEC << "s" << endl; 
    outDstru.outfile(0,"","");
    return EXIT_SUCCESS;
}



