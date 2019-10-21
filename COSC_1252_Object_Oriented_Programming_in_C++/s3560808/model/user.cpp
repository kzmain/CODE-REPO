#include "user.h"

std::unique_ptr<draughts::model::user> draughts::model::user::instance =
nullptr;
int draughts::model::user::user_number=0;
std::map<int, std::string> draughts::model::user::user_pool = std::map<int, std::string>();

draughts::model::user::user(void) 
{
}

draughts::model::user::~user(void)
{
}

bool draughts::model::user::add_user(const std::string& user_name)
{
    if(user_number!=0){
        std::map<int, std::string>::iterator itr;
        itr = user_pool.begin();
        while(itr!=user_pool.end()){
            if(itr->second==user_name)
            {
                return false;
            }
            itr++;
        }
    }
    ++user_number;
    user_pool.insert(std::pair<int, std::string>(user_number,user_name));
    return true;
}

int draughts::model::user::get_user_number()
{
    return user_number;
}

std::string draughts::model::user::get_user_name(int user_id){
    return user_pool[user_id];
}

std::map<int, std::string>& draughts::model::user::get_user_pool(void)
{
    return user_pool;
}

draughts::model::user * draughts::model::user::get_instance(void)
{
    if(instance == nullptr)
    {
        instance = std::unique_ptr<user>(new user);    
    }
    return instance.get();    
}

void draughts::model::user::delete_instance(void)
{
    instance.reset(nullptr);
}