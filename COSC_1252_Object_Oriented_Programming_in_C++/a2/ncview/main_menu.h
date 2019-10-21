//S3560808 Kai Zhang Assignment 2 C++
#include "menu.h"

#pragma once

namespace draughts
{
    namespace ncview
    {
        class main_menu : public menu
        {
            static const std::vector<std::string> strings;
            public:
                main_menu(void);
                virtual ~main_menu(void);
        };
    }
}
