//S3560808 Kai Zhang Assignment 2 C++
#include "main_menu.h"
#include "../nc_controller/command.h"
#include "../nc_controller/controller.h"

const std::vector<std::string> draughts::ncview::main_menu::strings = {
    "Add Player to the system",  
    "Play Game","Assignment 2 Demo mode", "Exit Game"
};

draughts::ncview::main_menu::main_menu(void)
    : menu("English Draughts", strings, 
        draughts::nc_controller::controller::controller::get_instance()
            ->get_main_menu_commands())
{
}

draughts::ncview::main_menu::~main_menu(void)
{
}
