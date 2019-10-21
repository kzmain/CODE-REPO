//S3560808 Kai Zhang Assignment 2 C++
#include "board.h"
std::unique_ptr<draughts::model::board> draughts::model::board::instance = nullptr;


draughts::model::board * draughts::model::board::get_instance(void)
{
    if(instance == nullptr)
    {
        instance = std::unique_ptr<board>(new board(8,8));    
    }
    return instance.get();    
}

int draughts::model::board::get_width(void)noexcept 
{
    return 8;
}

int draughts::model::board::get_height(void)noexcept
{
    return 8;
}

void draughts::model::board::delete_instance(void)
{
    instance.reset(nullptr);
}
