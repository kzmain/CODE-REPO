//S3560808 Kai Zhang Assignment 2 C++
#include "menu.h"

#pragma once

namespace draughts
{
    namespace ncview
    {
        class demo_menu : public menu
        {
            static const std::vector<std::string> strings;
            public:
                demo_menu(void);
                virtual ~demo_menu(void);
        };
    }
}
