//S3560808 Kai Zhang Assignment 2 C++
#include "model.h"
#include "player.h"
#include "user.h"
#include <math.h>

std::unique_ptr<draughts::model::model> draughts::model::model::instance =
nullptr;



draughts::model::model::model(void) 
{
}

draughts::model::model::~model(void)
{
}

void draughts::model::model::start_demo_game(int plr1, int plr2, int mode)
{
    player* instance = nullptr;
    instance->set_demo_players(plr1, plr2, mode);
}

draughts::model::model * draughts::model::model::get_instance(void)
{
    if(instance == nullptr)
    {
        instance = std::unique_ptr<model>(new model);    
    }
    return instance.get();    
}

void draughts::model::model::delete_instance(void)
{
    instance.reset(nullptr);
}