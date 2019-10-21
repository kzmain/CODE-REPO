//S3560808 Kai Zhang Assignment 2 C++
#include <memory>
#include <vector>
#include "command.h"
#include <chrono>
#include <thread>

#pragma once

namespace draughts
{
    namespace ncview
    {
        class ui;
    }
    namespace model
    {
        class model;
    }
    namespace nc_controller
    {
        class command;

        class controller
        {
            static std::unique_ptr<controller>instance;

            model::model * get_model(void);
            ncview::ui * get_view(void);
            controller(void);

            public:
            static controller* get_instance(void);
            std::vector<std::unique_ptr<command>> 
                get_main_menu_commands(void);
            std::vector<std::unique_ptr<command>> 
                get_demo_menu_commands(void);
            void start_game(std::map<int, std::string>);
            void start_demo_game(std::map<int, std::string>, int);
            static void delete_instance(void);
            virtual ~controller(void);

        };
    }
}
