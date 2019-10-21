//S3560808 Kai Zhang Assignment 2 C++
#include "token.h"

draughts::model::token_type draughts::model::token::get_type(void)
{
    return type;
}

int draughts::model::token::get_y_value(void){
    return y;
}

int draughts::model::token::get_x_value(void){
    return x;
}