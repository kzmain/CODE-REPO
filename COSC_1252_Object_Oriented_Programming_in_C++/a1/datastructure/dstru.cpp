/*****************************************************************\
*
*         Course code: COSC1252/1254
*         Student Number: s3560808
*         Date: 08.2017
*
*****************************************************************/
#include <memory>
#include <string>
#include <cstring>
#include <vector>
#include <set>
#include <fstream>
#include <map>
#include <boost/tokenizer.hpp>
#include <boost/token_functions.hpp>
#include <boost/token_iterator.hpp>
#include "dstru.h"
using namespace std;
int dstru::processInputFile(int mode){
    if(instream.is_open())
    {
        //Read files from input txt file
        stringstream strStream;
        strStream<<instream.rdbuf();
        string str=strStream.str();
        //Tokenization initial
        typedef boost::tokenizer<boost::char_separator<char> > tokenizer;
        boost::char_separator<char> sep(" 1234567890!@#$%^&*()_+=[{}]\\|;:'\"<>,./?\n\r");
        tokenizer tokens(str, sep);
        //Tokenize start
        for (tokenizer::iterator tok_iter = tokens.begin();tok_iter != tokens.end(); ++tok_iter)
        {    
            string temp=*tok_iter;
            transform(temp.begin(), temp.end(), temp.begin(), ::tolower);
            if(mode==1){
                alist.push_back(temp);
            }else if(mode==2){
                avector.push_back(temp);
            }else if(mode==3){
                aset.insert(temp);
            }else if(mode==4){
                aslist.add(temp);
            }else if(mode==5){
                abst.add(temp);
            }else{
                
            }
        }
        //Success process files! Close instream!
        instream.close();
        return 0;
    }else{
        cout<<"Invalid Passage File\n";
        return 1;
    }
}
    
int dstru::outfile(int mode,string word,string relatedWord){
    //Initialize two maps to store outputs after levenshtein calculation
    static std::map<string,int> indict;
    static std::map<string,set<string>> notdict;
    //Store words in dict
    if(mode==1){
        if(indict.count(word)==0){
            indict[word]=1;
        }else{
            indict[word]=indict[word]+1;
        }
    //Store words not in dict
    }else if(mode==2){
        multimap<string,set<string>>::iterator it;
        set<string> relatedWordSet;
        bool inmap = false;
        for(it = notdict.begin(); it != notdict.end(); it++)  
        {  
            if(it->first==word){
                inmap = true;
            }
        }  
        if(inmap==false){
            relatedWordSet.insert(relatedWord);
            notdict.insert(pair<string,set<string>>(word,relatedWordSet));
        }else{
            notdict[word].insert(relatedWord);
        }
    //Output files
    }else if(mode==0){
        std::map<string,int>::iterator itrInDict = indict.begin();
        std::multimap<string,set<string>>::iterator itrNotIn = notdict.begin();
        std::set<string>::iterator itrRelatedWords;
        //Output results files in dict first
        while(itrInDict!=indict.end()){
            outstream<<itrInDict->first<<":"<<itrInDict->second<<"\n";
            itrInDict++;
        }
        //Output results files not in dict
        while(itrNotIn!=notdict.end()){
            itrRelatedWords = itrNotIn->second.begin();
            while(itrRelatedWords!=itrNotIn->second.end()){
                outstream<<itrNotIn->first<<" was not found in the dictionary. The closest matches were: "<<*itrRelatedWords<<"\n";
                itrRelatedWords++;
            }
            itrNotIn++;
        }
        outstream.close();
    }else{
        return 1;
    }
    return 0;
}

int dstru::levenshtein(string word,string dict)
{
    //Initial arry
    int n = word.size();
    int m = dict.size();
    if ( n == 0)
        return m;
    if ( m == 0)
        return n;
    int stringArr[21][21];
    for(int i = 0;i<=m;++i){
        stringArr[0][i]=i;
    }
    for(int i = 0;i<=n;++i){
        stringArr[i][0]=i;
    }
    //Levenshtein implementation
    for(int i = 1;i<=m;++i){
        for(int j=1;j<=n;++j){
            
            if(dict.at(i-1)==word.at(j-1)){
                stringArr[j][i]=stringArr[j-1][i-1];
            }else{
                stringArr[j][i]=stringArr[j-1][i-1]+1;
            }
        }
    }
    return stringArr[n][m];
}

int dstru::stringCompare(int mode, dstru* txtDstru, dstru* dictDstru, dstru* outDstru){
    multimap<string,string> store;
    //List mode
    if(mode==1){
        list<string>::iterator passageitr;
        list<string>::iterator dictitr;
        for(passageitr=txtDstru->alist.begin();passageitr!=txtDstru->alist.end();++passageitr){
            int min = 100;
            int check = 100;
            for(dictitr=dictDstru->alist.begin();dictitr!=dictDstru->alist.end();++dictitr){
                check=levenshtein(*passageitr,*dictitr);
                
                if(check<min){
                    min=check;
                    store.clear();
                    store.insert(pair<string,string>(*passageitr,*dictitr));
                }
                if(min==0){
                    outfile(1,*passageitr,*dictitr);
                    break;
                }
                if(check==min){
                    store.insert(pair<string,string>(*passageitr,*dictitr));
                }
            }
            if(min==0){
                
            }else{
                map<string,string>::iterator itr;
                itr=store.begin();
                while(itr!=store.end()){
                    outfile(2,itr->first,itr->second);
                    itr++;
                }
            }
        }
    }
    //Vector mode
    else if(mode==2){
        vector<string>::iterator passageitr;
        vector<string>::iterator dictitr;
        for(passageitr=txtDstru->avector.begin();passageitr!=txtDstru->avector.end();++passageitr){
            int min = 100;
            int check = 100;
            for(dictitr=dictDstru->avector.begin();dictitr!=dictDstru->avector.end();++dictitr){
                check=levenshtein(*passageitr,*dictitr);
                if(check<min){
                    min=check;
                    store.clear();
                    store.insert(pair<string,string>(*passageitr,*dictitr));
                }
                if(min==0){
                    outfile(1,*passageitr,*dictitr);
                    break;
                }
                if(check==min){
                    store.insert(pair<string,string>(*passageitr,*dictitr));
                }
            }
            if(min==0){
                
            }else{
                map<string,string>::iterator itr;
                itr=store.begin();
                while(itr!=store.end()){
                    outfile(2,itr->first,itr->second);
                    itr++;
                }
            }
        }
    }
    //multiset mode
    else if(mode==3){
        multiset<string>::iterator passageitr;
        multiset<string>::iterator dictitr;
        for(passageitr=txtDstru->aset.begin();passageitr!=txtDstru->aset.end();++passageitr){
            int min = 100;
            int check = 100;
            for(dictitr=dictDstru->aset.begin();dictitr!=dictDstru->aset.end();++dictitr){
                check=levenshtein(*passageitr,*dictitr);
                if(check<min){
                    min=check;
                    store.clear();
                    store.insert(pair<string,string>(*passageitr,*dictitr));
                }
                if(min==0){
                    outfile(1,*passageitr,*dictitr);
                    break;
                }
                if(check==min){
                    store.insert(pair<string,string>(*passageitr,*dictitr));
                }
            }
            if(min==0){
                
            }else{
                map<string,string>::iterator itr;
                itr=store.begin();
                while(itr!=store.end()){
                    outfile(2,itr->first,itr->second);
                    itr++;
                }
            }
        }
    }
    //Single list mode
    else if(mode==4){
        for(int i=0;i<txtDstru->aslist.size;++i){
            int min = 100;
            int check = 100;
            string passagetxt = txtDstru->aslist.get();
            string dicttxt="";
            for(int j=0;j<dictDstru->aslist.size;++j){
                dicttxt = dictDstru->aslist.get();
                check=levenshtein(passagetxt,dicttxt);
                if(check<min){
                    min=check;
                    store.clear();
                    store.insert(pair<string,string>(passagetxt,dicttxt));
                }
                if(min==0){
                    outfile(1,passagetxt,passagetxt);
                    break;
                }
                if(check==min){
                    store.insert(pair<string,string>(passagetxt,dicttxt));
                }
            }
            if(min==0){
                
            }else{
                map<string,string>::iterator itr;
                itr=store.begin();
                while(itr!=store.end()){
                    outfile(2,itr->first,itr->second);
                    itr++;
                }
            }
        }
    }
    //Binary search mode
    else if(mode==5){
        for(int i=0;i<txtDstru->abst.size;++i){
            int min = 100;
            int check = 100;
            string passagetxt = txtDstru->abst.get();
            string dicttxt="";
            for(int j=0;j<dictDstru->abst.size;++j){
                dicttxt = dictDstru->abst.get();
                check=levenshtein(passagetxt,dicttxt);
                if(check<min){
                    min=check;
                    store.clear();
                    store.insert(pair<string,string>(passagetxt,dicttxt));
                }
                if(min==0){
                    outfile(1,passagetxt,passagetxt);
                    break;
                }
                if(check==min){
                    store.insert(pair<string,string>(passagetxt,dicttxt));
                }
            }
            if(min==0){
                
            }else{
                map<string,string>::iterator itr;
                itr=store.begin();
                for(itr=store.begin();itr!=store.end();++itr){
                    
                    outfile(2,itr->first,itr->second);
                }
            }
            dictDstru->abst.initialPivot();
        }
    }else{
        return 1;    
    }
    return 0;
}