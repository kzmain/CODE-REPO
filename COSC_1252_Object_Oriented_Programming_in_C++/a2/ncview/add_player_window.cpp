//S3560808 Kai Zhang Assignment 2 C++
#include "add_player_window.h"
#include "ui.h"
#include "../model/user.h"
#include "../nc_controller/command.h"

void draughts::ncview::add_player_window::activate(void)
{
    std::string name;
    bool success = false;
    std::string recv;

    while(!success){
        try {
            name = window::get_input(
               "\n- Please enter the name for the \033[1;32mNew Player.\033[0m, \n- Or press \"\033[1;32mEnter\033[0m\" to \033[1;32mskip\033[0m"  
            );
            draughts::model::user * user = draughts::model::user::get_instance();
            success = user->add_user(name);
            if(success==false){
                std::cout << "\033[1;31mUser \""<<name<< "\" is already in system, plean try another user name.\033[0m"<<std::endl;
            }
        }
        catch(std::exception& ex)
        {
            std::cerr << ex.what() << std::endl;
            view->main_menu();
        }
    }
    std::cout <<"User: \033[1;32m\""<<name<< "\"\033[0m is \033[1;32mSuccessfully\033[0m added to the player roster."
    << std::endl;
    std::cout << "Press <enter> to continue: " << std::endl;
    std::cin.get();
    view->main_menu();
}
