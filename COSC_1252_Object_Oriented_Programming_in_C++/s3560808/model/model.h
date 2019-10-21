#include <vector>
#include <memory>
#include <utility>
#include <iostream>
#include <sstream>
#include <map>
#include <thread>
#include <chrono>

#pragma once

namespace draughts
{
    namespace model
    {
        class model
        {
            static std::unique_ptr<model> instance;
        public:
            model(void);
            virtual ~model(void);
            void start_demo_game(int, int, int);
            
            static model * get_instance(void);
            static void delete_instance(void);
        };
    }
}
