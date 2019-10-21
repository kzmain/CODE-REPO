#include "controller.h"
#include "../ncview/ui.h"
#include "../model/model.h"
#include "../model/player.h"


std::unique_ptr<draughts::nc_controller::controller>
draughts::nc_controller::controller::instance=nullptr;

draughts::nc_controller::controller::controller(void) 
{

}

draughts::model::model * draughts::nc_controller::controller::get_model(
    void)
{
    return model::model::get_instance();
}

draughts::ncview::ui * draughts::nc_controller::controller::get_view(void)
{
    return ncview::ui::get_instance();
}

    draughts::nc_controller::controller*
draughts::nc_controller::controller::get_instance(void)
{
    if(instance == nullptr){
        instance = std::unique_ptr<controller>(new controller);
    }
    return instance.get();
}

    std::vector<std::unique_ptr<draughts::nc_controller::command>>
draughts::nc_controller::controller::get_main_menu_commands(void)
{
    std::vector<std::unique_ptr<command>> main_menu_commands;
    main_menu_commands.emplace_back(std::make_unique<addplayer_command>());
    main_menu_commands.emplace_back(std::make_unique<newgame_command>());
    main_menu_commands.emplace_back(std::make_unique<demo_mode_command>());
    main_menu_commands.emplace_back(std::make_unique<exit_command>());
    return std::move(main_menu_commands);
}

std::vector<std::unique_ptr<draughts::nc_controller::command>>
draughts::nc_controller::controller::get_demo_menu_commands(void)
{
    std::vector<std::unique_ptr<command>> demo_menu_commands;
    demo_menu_commands.emplace_back(std::make_unique<demo_basic_move_command>());
    demo_menu_commands.emplace_back(std::make_unique<demo_jump_move_command>());
    demo_menu_commands.emplace_back(std::make_unique<demo_normal_to_crown_command>());
    demo_menu_commands.emplace_back(std::make_unique<demo_game_finish_check_command>());
    demo_menu_commands.emplace_back(std::make_unique<main_menu>());
    return std::move(demo_menu_commands);
}

void draughts::nc_controller::controller::delete_instance(void)
{
    instance.reset(nullptr);
}

void draughts::nc_controller::controller::start_game(
    std::map<int, std::string> players)
{
    std::vector<int> ids;
    using player = std::pair<int, std::string>;
    player player1, player2;
    std::pair<player, player> theplayers; 
    int count = 0;
    for(auto & pair : players)
    {
        count++;
        ids.push_back(pair.first);
        if(count == 1)
        {
            player1 = pair;
        }
        else
        {
            player2 = pair;
        }
    }
    theplayers = std::make_pair(player1, player2);
    model::player::get_instance()->set_players(ids[0], ids[1]);
    get_view()->show_game_window(theplayers);
}

void draughts::nc_controller::controller::start_demo_game(
    std::map<int, std::string> players, int mode)
{
    std::vector<int> ids;
    using player = std::pair<int, std::string>;
    player player1, player2;
    std::pair<player, player> theplayers; 
    int count = 0;
    for(auto & pair : players)
    {
        count++;
        ids.push_back(pair.first);
        if(count == 1)
        {
            player1 = pair;
        }
        else
        {
            player2 = pair;
        }
    }
    theplayers = std::make_pair(player1, player2);
    get_model()->start_demo_game(ids[0], ids[1],mode);
    get_view()->show_game_window(theplayers);
}

draughts::nc_controller::controller::~controller(void)
{
}
