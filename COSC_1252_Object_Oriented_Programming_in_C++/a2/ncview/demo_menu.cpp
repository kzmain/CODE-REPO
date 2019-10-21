//S3560808 Kai Zhang Assignment 2 C++
#include "main_menu.h"
#include "../nc_controller/command.h"
#include "../nc_controller/controller.h"

const std::vector<std::string> draughts::ncview::demo_menu::strings = {
    "Basic move","Jump move","Normal Token change to Crown Token","Game Finish Check" ,"Return to Main Menu" 
};

draughts::ncview::demo_menu::demo_menu(void)
    : menu("English Draughts (Demo mode)", strings, 
        draughts::nc_controller::controller::controller::get_instance()
            ->get_demo_menu_commands())
{
}

draughts::ncview::demo_menu::~demo_menu(void)
{
}
