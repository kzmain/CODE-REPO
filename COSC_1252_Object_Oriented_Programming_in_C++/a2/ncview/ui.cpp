//S3560808 Kai Zhang Assignment 2 C++
#include "ui.h"
#include "../nc_controller/controller.h"
#include "../model/model.h"
#include "../model/user.h"
std::unique_ptr<draughts::ncview::ui> draughts::ncview::ui::instance = 
    nullptr;

draughts::ncview::ui::ui(void)
    : thecontroller(draughts::nc_controller::controller::get_instance()),
        themodel(draughts::model::model::get_instance())
{
}

void draughts::ncview::ui::main_menu(void)
{
    draughts::ncview::main_menu menu;
    menu.activate();
}

void draughts::ncview::ui::add_player(void)
{
    draughts::ncview::add_player_window newwin;
    newwin.activate();
}

void draughts::ncview::ui::play_game(void)
{
    try
    { 
        player_selection_window newwin(draughts::model::user::get_user_pool());
        newwin.activate();
    }
    catch(std::exception& ex)
    {
        std::cerr << "Exception: " << std::endl;
    }
}

draughts::ncview::ui * draughts::ncview::ui::get_instance(void)
{
    if(instance == nullptr)
    {
        instance = std::unique_ptr<ui>(new ui());
    }
    return instance.get();
}

void draughts::ncview::ui::delete_instance(void)
{
    instance.reset(nullptr);
}


void draughts::ncview::ui::show_game_window(draughts::ncview::player_pair
    players)
{
    game_window newwin(players);
    newwin.activate();
}

void draughts::ncview::ui::demo_menu(void)
{
    draughts::ncview::demo_menu menu;
    menu.activate();
}

void draughts::ncview::ui::demo(int mode)
{
    draughts::model::user * user = draughts::model::user::get_instance();
    user->add_user("Demo Player 1");
    user->add_user("Demo Player 2");
    std::map<int,std::string> selected_list;
    selected_list.insert(std::make_pair(1,"Demo Player 1"));
    selected_list.insert(std::make_pair(2,"Demo Player 2"));
    if(mode == 1)
    {
        thecontroller->start_demo_game(selected_list, 1);
    }
    else if(mode ==2 )
    {
        thecontroller->start_demo_game(selected_list, 2);
    }
    else if(mode ==3)
    {
        thecontroller->start_demo_game(selected_list, 3);
    }
    else if(mode==4)
    {
        thecontroller->start_demo_game(selected_list, 4);
    }
    else
    {
        
    }
}


draughts::ncview::ui::~ui(void)
{
}

