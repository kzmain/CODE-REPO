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
#include "bst.h"
#include <iostream>
using namespace std;

int bst::levenshtein(string word,string dict)
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

//Add nodes of bst
int bst::add(string input){
    node* current = nullptr;
    node* prev = nullptr;
    bool right = true;
    unique_ptr<node> temp = make_unique<node>(input);
    if(head==nullptr){
        head = temp.release();
        ++size;
        return 0;
    }
    current = head;
    while(current)
    {
        prev = current;
        if(levenshtein((current->word),input)<6)
        {
            current=current->right;
            right = true;
        }
        else{
            current=current->left;
            right = false;
        }
    }
    current = temp.release();
    if(right==true){
        prev->right = current;
        current->parent = prev;
    }else{
        prev->left = current;
        current->parent = prev;
    }
    ++size;
    return 0;
}

//Iterate bst
string bst::get(){
    //Initial search pivot
    if(pivot==nullptr){
        pivot = head;
        pivot->iterated = true;
        return pivot->word;
    }
    //Check left branch first
    if(pivot->left!=nullptr){
        //Left branch did not be iterated, go to left
        if(pivot->left->iterated==false){
            pivot = pivot->left;
            pivot->iterated = true;
            return pivot->word;
        }
        //Left branch was iterated, go to right
        else if(pivot->right!=nullptr){
            //Right branch did not be iterated, go to right
            if(pivot->right->iterated==false){
                pivot = pivot->right;
                pivot->iterated = true;
                return pivot->word;
            //Right branch was iterated, go upper node
            }else if(pivot->right->iterated==true){
                pivot = get(pivot);
            }
            else{
                
            }
        }
    //Check right branch
    }else if(pivot->right!=nullptr){
        //Right branch did not be iterated, go to right
        if(pivot->right->iterated==false){
            pivot = pivot->right;
            pivot->iterated = true;
            return pivot->word;
        }else{
            cout<<"problem 3  ";
        }
    //Get the end nodes of bst, go upper node
    }else if(pivot->left==nullptr&&pivot->right==nullptr){
        pivot = get(pivot);
    }else{
        return "";
    }
    pivot->iterated = true;
    return pivot->word;
}

//Got upper available node
bst::node* bst::get(node* pointer){
    if(pointer->right==nullptr){
        pointer = pointer->parent;
        pointer = get(pointer);
        return pointer;
    }
    else if(pointer->right->iterated==true){
        if(pointer==head){
            return head;
        }
        pointer = pointer->parent;
        pointer = get(pointer);
        return pointer;
    }else if(pointer->right->iterated==false){
        pointer = pointer->right;
        pointer->iterated=true;
        return pointer;
    }else{
        cout<<"problem 4  ";
    }
    return pointer;
}
//Initial pivot after iterated bst successfully in order to iterate next time

void bst::initialPivot(){
    pivot = head;
    head->iterated=false;
    initialPivot(head);
}
//Initial all node to not iterated status

void bst::initialPivot(node* initial){
    if(initial->left!=nullptr){
        initial->left->iterated = false;
        initialPivot(initial->left);
    }
    if(initial->right!=nullptr){
        initial->right->iterated = false;
        initialPivot(initial->right);
    }
}
