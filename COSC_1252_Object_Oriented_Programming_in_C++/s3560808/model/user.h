#include <vector>
#include <memory>
#include <utility>
#include <iostream>
#include <sstream>
#include <map>
#include <thread>
#include <chrono>
#include "model.h"

#pragma once
namespace draughts
{
    namespace model
    {
        class user : public model
        {
            static std::unique_ptr<user> instance;
            static int user_number;
            static std::map<int, std::string> user_pool;
        public:
            user(void);
            virtual ~user(void);
            bool add_user(const std::string&);
            int get_user_number();
            std::string get_user_name(int);
            static std::map<int, std::string>& get_user_pool(void);
            static user * get_instance(void);
            static void delete_instance(void);
        };
    }
}