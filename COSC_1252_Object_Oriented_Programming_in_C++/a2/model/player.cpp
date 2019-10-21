//S3560808 Kai Zhang Assignment 2 C++
#include "player.h"
#include <stdlib.h>  
#include <vector>
#include <random>
#include <ctime>

int draughts::model::player::current_player = 0;
int draughts::model::player::component_player = 1;
std::vector<std::unique_ptr<draughts::model::player>> draughts::model::player::player_pool = 
std::vector<std::unique_ptr<draughts::model::player>>();
std::unique_ptr<draughts::model::player> draughts::model::player::instance = nullptr;

draughts::model::player& draughts::model::player::operator++() {
	++player_pool[current_player]->score;
    --player_pool[component_player]->token_number;
	return *this;
}

draughts::model::player draughts::model::player::operator++(int) { 
	player result = *this;
	++player_pool[current_player]->score;
    --player_pool[component_player]->token_number;
	return result;
} 

void draughts::model::player::set_players(int plr1, int plr2){
    draughts::model::player::player_pool.push_back(std::make_unique<player>(plr1));
    draughts::model::player::player_pool.push_back(std::make_unique<player>(plr2));
    set_player_token();
    return;
}

void draughts::model::player::set_demo_players(int plr1, int plr2, int mode){
    draughts::model::player::player_pool.push_back(std::make_unique<player>(plr1));
    draughts::model::player::player_pool.push_back(std::make_unique<player>(plr2));
    if(mode == 1){
        set_demo_basic_move_token();    
    }else if(mode == 2){
        set_demo_jump_move_token();    
    }else if(mode == 3){
        set_demo_normal_to_crown_token();    
    }else if(mode == 4){
        set_demo_game_finish_check_token();    
    }else{
        
    }
    return;
}

void draughts::model::player::get_winner(void){
    std::cout<<"PLAYER 1 \033[1;92m" <<player_pool[0]->player_name<< "\033[0m \'s score: \033[1;92m"<<player_pool[0]->score<<"\033[0m"<<std::endl;
    std::cout<<"PLAYER 2 \033[1;92m" <<player_pool[1]->player_name<< "\033[0m \'s score: \033[1;92m"<<player_pool[1]->score<<"\033[0m"<<std::endl;
    std::cout<<"\033[1;91m";
    if(player_pool[0]->score > player_pool[1]->score){
        std::cout<<"PLAYER 1 "<<player_pool[0]->player_name<<" WIN!";
    }else if(player_pool[0]->score < player_pool[1]->score){
        std::cout<<"PLAYER 2 "<<player_pool[1]->player_name<<" WIN!";
    }else{
        std::cout<<"DRAW!"<<std::endl;
    }
    std::cout<<"\033[0m"<<std::endl;
}

int draughts::model::player::get_current_player_id(void)
{
    return player_pool[current_player]->user_id;
}

std::string draughts::model::player::get_current_player_name(void)
{
    return player_pool[current_player]->player_name;
}

int draughts::model::player::get_current_player(void)
{
    return current_player;
}

int draughts::model::player::get_component_player(void)
{
    return component_player;
}

int draughts::model::player::get_current_player_score(void)
{
    return player_pool[current_player]->score;
}

std::vector<draughts::model::token> draughts::model::player::get_token_pool(void){
    return token_pool;
}

void  draughts::model::player::change_current_player(void)
{
    if(current_player==0){
        current_player=1;
        component_player = 0;
    }else{
        current_player=0;
        component_player = 1;
    }
    return;
}

bool draughts::model::player::still_continue_jump(int startx, int starty, int endx, int endy, bool check_mode)
{
    bool continue_jump = true;
    if(check_mode==true){
        return continue_jump;
    }
    if(instance->player_pool[instance->current_player]->jump_move_lock==true)
    {
        //Check last jump piece
        if(startx!=instance->player_pool[instance->current_player]->last_x||starty!=instance->player_pool[instance->current_player]->last_y)
        {
            continue_jump = false;
        }else{
            
        }
        //Check whether this is a jump move
        if(abs(startx-endx)!=2||abs(starty-endy)!=2)
        {
            continue_jump = false;
        }else{
            
        }
        
    }else{
        
    }
    if(continue_jump == false)
    {
        std::cout<<"\033[1;91m";
        std::cout<<"It is a continue jump move! Cannot move other pieces, or basic move";
        std::cout<<"\033[0m"<<std::endl;
            
    }
    return continue_jump;
}

bool draughts::model::player::in_bound(int startx, int starty, int endx, int endy, bool check_mode)
{
    if(startx<1||starty<1||startx>8||starty>8||endx<1||endy<1||endx>8||endy>8)
    {
        if(check_mode==false){
            if(startx<1||starty<1||startx>8||starty>8){
                std::cout<<"\033[1;91m";
                std::cout<<"Start piece out of bound";
                std::cout<<"\033[0m"<<std::endl;
            }
            if(endx<1||endy<1||endx>8||endy>8){
                std::cout<<"\033[1;91m";
                std::cout<<"End piece out of bound";
                std::cout<<"\033[0m"<<std::endl;
            }
        }else{
            
        }
        return false;
    }else{
        return true;
    }
}

bool draughts::model::player::check_current_user_start_piece(int startx, int starty, bool check_mode){
    draughts::model::player* instance = nullptr;
    for (std::vector<token>::iterator itr= instance->player_pool[instance->get_current_player()]->token_pool.begin(); itr != instance->player_pool[instance->get_current_player()]->token_pool.end(); ++itr) {
        if(itr->get_x_value()==startx&&itr->get_y_value()==starty)
        {
            return true;
        }
    }
    if(check_mode==false){
        std::cout<<"\033[1;91m";
        std::cout<<"Please choose your own start piece";
        std::cout<<"\033[0m"<<std::endl;
    }
    return false;
}

bool draughts::model::player::check_current_user_end_piece(int endx, int endy, bool check_mode){
    player* instance = nullptr;
    bool right_end_piece = true;
    for (std::vector<token>::iterator itr= instance->player_pool[instance->get_current_player()]->token_pool.begin(); itr != instance->player_pool[instance->get_current_player()]->token_pool.end(); ++itr) {
        if(itr->get_x_value()==endx&&itr->get_y_value()==endy)
        {
            right_end_piece = false;
        }
    }
    for (std::vector<token>::iterator itr= instance->player_pool[instance->get_component_player()]->token_pool.begin(); itr != instance->player_pool[instance->get_component_player()]->token_pool.end(); ++itr) {
        if(itr->get_x_value()==endx&&itr->get_y_value()==endy)
        {
            right_end_piece = false;
        }
    }
    if(right_end_piece == false){
        if(check_mode==false){
            std::cout<<"\033[1;91m";
            std::cout<<"Please choose a valid end place";
            std::cout<<"\033[0m"<<std::endl;
        }
        return right_end_piece;
    }
    return right_end_piece;
}

bool draughts::model::player::basic_checks(int startx, int starty, int endx, int endy, bool check_mode)
{
    if(
        !still_continue_jump(startx, starty,endx,endy, check_mode)||
        !in_bound(startx, starty,endx,endy, check_mode)||
        !check_current_user_start_piece(startx, starty, check_mode)||
        !check_current_user_end_piece(endx, endy, check_mode)
    )
    {
        return false;
    }
    return true;
}

bool draughts::model::player::make_move(int startx, int starty, int endx, int endy, bool check_mode)
{
    bool succ = false;
    //basic checks before moves
    if(!basic_checks(startx, starty,endx,endy,check_mode)){
        return succ;
    }
    //Start move
        //Basic move
    if(abs(startx-endx)==1&&abs(starty-endy)==1)
    {
        succ = basic_move(startx, starty,endx,endy);
    }
        //Jump move
    else if(abs(startx-endx)==2&&abs(starty-endy)==2)
    {
        succ = jump_move(startx, starty,endx,endy,check_mode);
    }
        //Invalid move
    else
    {
        std::cout<<"\033[1;91m";
        std::cout<<"Invalid move, this move does not follow the rules";
        std::cout<<"\033[0m"<<std::endl;
    }
    // test_function();
    return succ;
}

bool draughts::model::player::next_step_detector(int startx, int starty){
    token_type current_token_type = token_type::normal;
    player* instance = nullptr;
    bool jumped = false;
    for (std::vector<token>::iterator itr= instance->player_pool[instance->get_current_player()]->token_pool.begin(); itr != instance->player_pool[instance->get_current_player()]->token_pool.end(); ++itr) {
        if(itr->get_x_value()==startx&&itr->get_y_value()==starty)
        {
            current_token_type = itr->type;
        }
    }
    if(instance->get_current_player()==0){
        jumped = make_move(startx, starty, startx+2, starty+2,true);
        if(jumped==false){
            jumped = make_move(startx, starty, startx-2, starty+2,true);
        }
        if(current_token_type==token_type::crown){
            if(jumped==false){
                jumped = make_move(startx, starty, startx-2, starty-2,true);
            }
            
            if(jumped==false){
                jumped = make_move(startx, starty, startx+2, starty-2,true);
            }
            
        }
    }else{
        jumped = make_move(startx, starty, startx-2, starty-2,true);
        if(jumped==false){
            jumped = make_move(startx, starty, startx+2, starty-2,true);
        }
        if(current_token_type==token_type::crown){
            if(jumped==false){
                jumped = make_move(startx, starty, startx+2, starty+2,true);
            }
            
            if(jumped==false){
                jumped = make_move(startx, starty, startx-2, starty+2,true);
            }
        }
    }
    return jumped;
}

bool draughts::model::player::eliminate_middle_piece(int startx, int starty,int endx, int endy, bool check_mode){
    player* instance = nullptr;
    for (std::vector<token>::iterator itr= instance->player_pool[instance->get_component_player()]->token_pool.begin(); itr != instance->player_pool[instance->get_component_player()]->token_pool.end(); ++itr) {
        if(itr->get_x_value()==((startx+endx)/2)&&itr->get_y_value()==((starty+endy)/2))
        {
            if(check_mode==false){
                itr->x = 0;
                itr->y = 0;
                --instance->player_pool[instance->get_component_player()]->token_number;
            }
            return true;
        }
    }
    if(check_mode==false){
        std::cout<<"\033[1;91m";
        std::cout<<"No middle component piece cannot jump";
        std::cout<<"\033[0m"<<std::endl;
    }
    return false;
}

bool draughts::model::player::jump_move(int startx, int starty, int endx, int endy, bool check_mode)
{
    bool jumped = false;
    bool change_to_crown = false;
    draughts::model::token* middle_piece = nullptr;
    draughts::model::token* jump_piece = nullptr;
    for (std::vector<token>::iterator itr= player_pool[current_player]->token_pool.begin(); itr != player_pool[current_player]->token_pool.end(); ++itr)
    {
        if(itr->x==startx&&itr->y==starty)
        {
            jump_piece = &*itr;
        }
    }
    for(std::vector<token>::iterator itr= player_pool[component_player]->token_pool.begin(); itr != player_pool[component_player]->token_pool.end(); ++itr)
    {
        if(itr->x==((startx+endx)/2)&&itr->y==((starty+endy)/2))
        {
            middle_piece = &*itr;
        }
    }
    if(jump_piece==nullptr){
        if(check_mode==false)
        {
            std::cout<<"Invalid start jump piece"<<std::endl;
        }
        return jumped;
    }
    if(middle_piece==nullptr){
        if(check_mode==false)
        {
            std::cout<<"No component middle piece"<<std::endl;
        }
        return jumped;
    }
    if(jump_piece->type==token_type::crown)
    {
        jumped = true;
    }
    else
    {
        if(current_player==0)
        {
            if(starty<endy){
                jumped = true;
                if(endy == 8){
                    change_to_crown = true;
                }
            }
            else
            {
                std::cout<<"Cannot jump back"<<std::endl;
            }
        }
        else
        {
            if(starty>endy){
                jumped = true;
                if(endy == 1){
                    change_to_crown = true;
                }
            }
            else
            {
                std::cout<<"Cannot jump back"<<std::endl;
            }
        }
    }
    if(check_mode==true)
    {
        return jumped;
    }
    if(jumped==true)
    {
        jump_piece->x = endx;
        jump_piece->y = endy;
        middle_piece->x = 0;
        middle_piece->y = 0;
		++*draughts::model::player::get_instance();
        if(change_to_crown==true)
        {
            jump_piece->type = token_type::crown;
        }
        if(next_step_detector(endx, endy)==true)
        {
            player_pool[current_player]->jump_move_lock = true;
            player_pool[current_player]->last_x = endx;
            player_pool[current_player]->last_y = endy;
            return false;
        }else{
            
        }
    }
    else
    {
        
    }
    player_pool[current_player]->jump_move_lock = false;
    return jumped;
}

bool draughts::model::player::basic_move(int startx, int starty, int endx, int endy)
{
    player* instance = nullptr;
    
    if(starty<endy){
        if(instance->get_current_player()==0){
            for (std::vector<token>::iterator itr= instance->player_pool[instance->get_current_player()]->token_pool.begin(); itr != instance->player_pool[instance->get_current_player()]->token_pool.end(); ++itr) {
                if(itr->get_x_value()==startx&&itr->get_y_value()==starty)
                {
                    itr->x = endx;
                    itr->y = endy;
                    if(endy==8){
                        itr->type=token_type::crown;
                    }
                    return true;
                }
            }
        }else{
            for (std::vector<token>::iterator itr= instance->player_pool[instance->get_current_player()]->token_pool.begin(); itr != instance->player_pool[instance->get_current_player()]->token_pool.end(); ++itr) {
                if(itr->get_x_value()==startx&&itr->get_y_value()==starty&&itr->type==token_type::crown)
                {
                    itr->x = endx;
                    itr->y = endy;
                    return true;
                }
            }
        }
    }else{
        if(instance->get_current_player()==0){
            for (std::vector<token>::iterator itr= instance->player_pool[instance->get_current_player()]->token_pool.begin(); itr != instance->player_pool[instance->get_current_player()]->token_pool.end(); ++itr) {
                if(itr->get_x_value()==startx&&itr->get_y_value()==starty&&starty&&itr->type==token_type::crown)
                {
                    itr->x = endx;
                    itr->y = endy;
                    return true;
                }
            }
        }else{
            for (std::vector<token>::iterator itr= instance->player_pool[instance->get_current_player()]->token_pool.begin(); itr != instance->player_pool[instance->get_current_player()]->token_pool.end(); ++itr) {
                if(itr->get_x_value()==startx&&itr->get_y_value())
                {
                    itr->x = endx;
                    itr->y = endy;
                    if(endy==1){
                        itr->type=token_type::crown;
                    }
                    return true;
                }
            }
        }
    }
    return false;
}


void draughts::model::player::set_player_token(void){
    player_pool[0]->token_pool.clear();
    player_pool[1]->token_pool.clear();
    player_pool[0]->score = 0;
    player_pool[1]->score = 0;
    set_player_1_token();
    set_player_2_token();
    player_pool[0]->token_number = 12;
    player_pool[1]->token_number = 12;
}

void draughts::model::player::set_demo_basic_move_token(void)
{
    player_pool[0]->score = 0;
    player_pool[1]->score = 0;
    player_pool[0]->token_pool.clear();
    player_pool[1]->token_pool.clear();
    player_pool[0]->token_pool.push_back (draughts::model::token(2,1));
    player_pool[0]->token_pool.push_back (draughts::model::token(4,1));
    player_pool[0]->token_pool.push_back (draughts::model::token(6,1));
    player_pool[0]->token_pool.push_back (draughts::model::token(8,1));
    player_pool[0]->token_pool.push_back (draughts::model::token(1,2));
    player_pool[0]->token_pool.push_back (draughts::model::token(3,2));
    player_pool[0]->token_pool.push_back (draughts::model::token(5,2));
    player_pool[0]->token_pool.push_back (draughts::model::token(7,2));
    player_pool[0]->token_pool.push_back (draughts::model::token(2,3));
    player_pool[0]->token_pool.push_back (draughts::model::token(4,3));
    player_pool[0]->token_pool.push_back (draughts::model::token(6,3));
    player_pool[0]->token_pool.push_back (draughts::model::token(8,3));
    player_pool[1]->token_pool.push_back (draughts::model::token(1,6));
    player_pool[1]->token_pool.push_back (draughts::model::token(3,6));
    player_pool[1]->token_pool.push_back (draughts::model::token(5,6));
    player_pool[1]->token_pool.push_back (draughts::model::token(7,6));
    player_pool[1]->token_pool.push_back (draughts::model::token(2,7));
    player_pool[1]->token_pool.push_back (draughts::model::token(4,7));
    player_pool[1]->token_pool.push_back (draughts::model::token(6,7));
    player_pool[1]->token_pool.push_back (draughts::model::token(8,7));
    player_pool[1]->token_pool.push_back (draughts::model::token(1,8));
    player_pool[1]->token_pool.push_back (draughts::model::token(3,8));
    player_pool[1]->token_pool.push_back (draughts::model::token(5,8));
    player_pool[1]->token_pool.push_back (draughts::model::token(7,8));
    player_pool[0]->normal_token = "X";
    player_pool[0]->crown_token = "\033[1;32mX\033[0m";
    player_pool[1]->normal_token = "O";
    player_pool[1]->crown_token = "\033[1;32mO\033[0m";
    player_pool[0]->token_number = 12;
    player_pool[1]->token_number = 12;
    change_current_player();
}

void draughts::model::player::set_demo_jump_move_token(void)
{
    player_pool[0]->score = 0;
    player_pool[1]->score = 0;
    player_pool[0]->token_pool.clear();
    player_pool[1]->token_pool.clear();
    player_pool[0]->token_pool.push_back (draughts::model::token(1,1,token_type::crown));
    player_pool[0]->token_pool.push_back (draughts::model::token(2,4,token_type::crown));
    player_pool[0]->token_pool.push_back (draughts::model::token(4,4,token_type::crown));
    player_pool[0]->token_pool.push_back (draughts::model::token(6,4,token_type::crown));
    player_pool[0]->token_pool.push_back (draughts::model::token(8,4,token_type::crown));
    player_pool[1]->token_pool.push_back (draughts::model::token(1,3,token_type::crown));
    player_pool[1]->token_pool.push_back (draughts::model::token(2,2,token_type::crown));
    player_pool[1]->token_pool.push_back (draughts::model::token(4,2,token_type::crown));
    player_pool[1]->token_pool.push_back (draughts::model::token(6,2,token_type::crown));
    player_pool[1]->token_pool.push_back (draughts::model::token(8,2,token_type::crown));
    player_pool[0]->normal_token = "X";
    player_pool[0]->crown_token = "\033[1;32mX\033[0m";
    player_pool[1]->normal_token = "O";
    player_pool[1]->crown_token = "\033[1;32mO\033[0m";
    player_pool[0]->token_number = 5;
    player_pool[1]->token_number = 5;
    change_current_player();
}

void draughts::model::player::set_demo_normal_to_crown_token(void)
{
    player_pool[0]->score = 0;
    player_pool[1]->score = 0;
    player_pool[0]->token_pool.clear();
    player_pool[1]->token_pool.clear();
    player_pool[0]->token_pool.push_back (draughts::model::token(2,7));
    player_pool[0]->token_pool.push_back (draughts::model::token(6,6));
    player_pool[0]->token_pool.push_back (draughts::model::token(7,2));
    player_pool[1]->token_pool.push_back (draughts::model::token(3,2));
    player_pool[1]->token_pool.push_back (draughts::model::token(7,7));
    player_pool[1]->token_pool.push_back (draughts::model::token(6,3));
    player_pool[0]->normal_token = "X";
    player_pool[0]->crown_token = "\033[1;32mX\033[0m";
    player_pool[1]->normal_token = "O";
    player_pool[1]->crown_token = "\033[1;32mO\033[0m";
    player_pool[0]->token_number = 3;
    player_pool[1]->token_number = 3;
    change_current_player();
}

void draughts::model::player::set_demo_game_finish_check_token(void){
    player_pool[0]->score = 0;
    player_pool[1]->score = 0;
    player_pool[0]->token_pool.clear();
    player_pool[1]->token_pool.clear();
    player_pool[0]->token_pool.push_back (draughts::model::token(4,4,token_type::crown));
    player_pool[1]->token_pool.push_back (draughts::model::token(5,5,token_type::crown));
    player_pool[0]->normal_token = "X";
    player_pool[0]->crown_token = "\033[1;32mX\033[0m";
    player_pool[1]->normal_token = "O";
    player_pool[1]->crown_token = "\033[1;32mO\033[0m";
    player_pool[0]->token_number = 1;
    player_pool[1]->token_number = 1;
    change_current_player();
}

void draughts::model::player::set_player_1_token(){
    player_pool[0]->token_pool.push_back (draughts::model::token(2,1));
    player_pool[0]->token_pool.push_back (draughts::model::token(4,1));
    player_pool[0]->token_pool.push_back (draughts::model::token(6,1));
    player_pool[0]->token_pool.push_back (draughts::model::token(8,1));
    player_pool[0]->token_pool.push_back (draughts::model::token(1,2));
    player_pool[0]->token_pool.push_back (draughts::model::token(3,2));
    player_pool[0]->token_pool.push_back (draughts::model::token(5,2));
    player_pool[0]->token_pool.push_back (draughts::model::token(7,2));
    player_pool[0]->token_pool.push_back (draughts::model::token(2,3));
    player_pool[0]->token_pool.push_back (draughts::model::token(4,3));
    player_pool[0]->token_pool.push_back (draughts::model::token(6,3));
    player_pool[0]->token_pool.push_back (draughts::model::token(8,3));
    player_pool[0]->normal_token = "X";
    player_pool[0]->crown_token = "\033[1;32mX\033[0m";
    change_current_player();
}

void draughts::model::player::set_player_2_token(){
    player_pool[1]->token_pool.push_back (draughts::model::token(1,6));
    player_pool[1]->token_pool.push_back (draughts::model::token(3,6));
    player_pool[1]->token_pool.push_back (draughts::model::token(5,6));
    player_pool[1]->token_pool.push_back (draughts::model::token(7,6));
    player_pool[1]->token_pool.push_back (draughts::model::token(2,7));
    player_pool[1]->token_pool.push_back (draughts::model::token(4,7));
    player_pool[1]->token_pool.push_back (draughts::model::token(6,7));
    player_pool[1]->token_pool.push_back (draughts::model::token(8,7));
    player_pool[1]->token_pool.push_back (draughts::model::token(1,8));
    player_pool[1]->token_pool.push_back (draughts::model::token(3,8));
    player_pool[1]->token_pool.push_back (draughts::model::token(5,8));
    player_pool[1]->token_pool.push_back (draughts::model::token(7,8));
    player_pool[1]->normal_token = "O";
    player_pool[1]->crown_token = "\033[1;32mO\033[0m";
}

std::string draughts::model::player::get_token(int y, int x){
    for (std::vector<token>::iterator itr= player_pool[0]->token_pool.begin(); itr != player_pool[0]->token_pool.end(); ++itr) {
        if(itr->get_x_value()==x&&itr->get_y_value()==y)
        {
            if(itr->get_type()==draughts::model::token_type::normal){
                return player_pool[0]->normal_token;
            }else{
                return player_pool[0]->crown_token;
            }
            
        }
    }
    for (std::vector<token>::iterator itr= player_pool[1]->token_pool.begin(); itr != player_pool[1]->token_pool.end(); ++itr) {
        if(itr->get_x_value()==x&&itr->get_y_value()==y)
        {
            if(itr->get_type()==draughts::model::token_type::normal){
                return player_pool[1]->normal_token;
            }else{
                return player_pool[1]->crown_token;
            }
            
        }
    }
    return " ";
}

draughts::model::player * draughts::model::player::get_instance(void)
{
    if(instance == nullptr)
    {
        instance = std::unique_ptr<player>(new player);    
    }
    return instance.get();    
}

void draughts::model::player::delete_instance(void)
{
    instance.reset(nullptr);
}