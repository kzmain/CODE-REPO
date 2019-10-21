/*****************************************************************\
*
*         Course code: COSC1252/1254
*         Student Number: s3560808
*         Date: 08.2017
*
*****************************************************************/
#include <iostream>
#include <list>
#include <set>
#include <vector>
#include <map>
#include <fstream>
#include <boost/tokenizer.hpp>
#include <boost/token_functions.hpp>
#include <boost/token_iterator.hpp>
#include <string>
#include <sstream>
#include "bst.h"
#include "slist.h"
using namespace std;
class dstru{
    public:
        list<string> alist;
            vector<string> avector;
            multiset<string> aset;
            slist aslist;
            bst abst;
            ifstream instream;
            ofstream outstream;
        dstru(){}
        virtual ~dstru(){}
    public:
        int processInputFile(int mode);
        int outfile(int mode,string word,string relatedWord);
        int levenshtein(string str1,string str2);
        int stringCompare(int mode, dstru* txtDstru, dstru* dictDstru, dstru* outDstru);
};