#include <cstdlib>
#include <memory>
#include <map>
#include "../ncview/ui.h"
#pragma once

namespace draughts
{
    namespace nc_controller
    {

        class command
        {
            protected:
                static ncview::ui * view;

            public:

                command(void)
                {

                }

                virtual void operator()(void) = 0;
                virtual ~command(void){}
        };

        struct exit_command : public command
        {
            virtual void operator()(void) override
            {
                exit(EXIT_SUCCESS);
            }

            virtual ~exit_command(void){}
        };
        
        struct main_menu : public command
        {
            virtual void operator()(void) override
            {
                view->main_menu();
            }

            virtual ~main_menu(void){}
        };

        struct newgame_command : public command
        {          
            virtual void operator()(void) override
            {
                
                view->play_game();
                view->main_menu();
            }

            virtual ~newgame_command(void){}
        };

        struct addplayer_command : public command
        {
            virtual void operator()(void) override
            {
                view->add_player();
            }

            virtual ~addplayer_command(void){}
        };

        class select_player_command : public command
        {
            const std::map<int, std::string>& players_ref;
            std::map<int, std::string>& selected_ref;
            int index;
            public:
            select_player_command(
                    const std::map<int, std::string>& players, 
                    std::map<int, std::string>& selected, int ind)

                : players_ref(players), selected_ref(selected), index(ind)
                {
                }

            virtual void operator()(void) override
            {
                const std::map<int, std::string>::const_iterator needle 
                    = players_ref.find(index);
                if(needle == players_ref.cend())
                {
                    throw std::invalid_argument("Could not find the "
                        "selected player.");
                }
                selected_ref[index] = needle->second;
            }

            virtual ~select_player_command(void){}
        };
        
        struct demo_mode_command : public command
        {
            virtual void operator()(void) override
            {
                view->demo_menu();
            }

            virtual ~demo_mode_command(void){}
        };
        
        struct demo_basic_move_command : public command{
            virtual void operator()(void) override
            {
                view->demo(1);
                view->demo_menu();
            }
            virtual ~demo_basic_move_command(void){}
        };
        struct demo_jump_move_command : public command{
            virtual void operator()(void) override
            {
                view->demo(2);
                view->demo_menu();
            }
            virtual ~demo_jump_move_command(void){}
        };
        struct demo_normal_to_crown_command : public command{
            virtual void operator()(void) override
            {
                view->demo(3);
                view->demo_menu();
            }
            virtual ~demo_normal_to_crown_command(void){}
        };
        struct demo_game_finish_check_command : public command{
            virtual void operator()(void) override
            {
                view->demo(4);
                view->demo_menu();
            }
            virtual ~demo_game_finish_check_command(void){}
        };
    }
}
