//S3560808 Kai Zhang Assignment 2 C++
#include "game_window.h"
#include "../model/player.h"
#include "../model/board.h"
#include "../model/model.h"
#include <exception>

draughts::ncview::game_window::game_window(const player_pair & theplayers) 
    : players(theplayers), quit(false)
{
}

void draughts::ncview::game_window::activate(void) 
{
    draughts::model::player* theplayer=nullptr;
    while(!quit)
    {
        bool succ_move = false;
        while(!succ_move){
            if(theplayer->player_pool[0]->token_number==0||theplayer->player_pool[1]->token_number==0){
                quit = true;
                break;
            }
            try
            {
                display_board();
            }
            catch(std::exception & ex)
            {
                std::cerr << ex.what() << std::endl;
                return;
            }
            try
            {
                std::pair<std::pair<int,int>,std::pair<int,int>> move_coords;
                move_coords = get_move_input();
                if(move_coords.first.first==-1&&move_coords.first.second==-1){
                    quit = true;
					throw "Game exit!";
                }
				// if(move_coords.first.first==nullptr||move_coords.first.second==nullptr||move_coords.second.first==nullptr&&move_coords.second.second==nullptr){
					// throw input_cancelled();
				// }
                succ_move = theplayer->make_move(move_coords.first.first, 
                    move_coords.first.second, move_coords.second.first,
                    move_coords.second.second, false);
            }
            catch(char const* ex)
            {
                std::cerr <<ex<< std::endl;
            }
        }
        theplayer->change_current_player();
    }
    theplayer->get_winner();
    
}




std::pair<std::pair<int,int>, std::pair<int,int>> 
    draughts::ncview::game_window::get_move_input(void)
{
    std::string input;
    std::pair<std::pair<int,int>,std::pair<int,int>> move;
    std::pair<int,int> start;
    std::pair<int,int> end;
    std::getline(std::cin,input);
    std::vector<std::string> moves;
    std::vector<std::string> coords;
	
    if(input=="-1"){
        input="-1,-1 -1,-1";
    }
	try{
		boost::split(moves, input, boost::is_any_of(" "));
		if(moves.size()!=2){
			throw "Your input format is wrong";
		}
		start = strtocoord(moves[0]);    
		end = strtocoord(moves[1]);  
	}catch(char const* ex){
		std::cerr << ex << std::endl;
		start = strtocoord("-2,-2");    
		end = strtocoord("-2,-2");  
	}
	move = std::make_pair(start, end);
    return move;
}

void draughts::ncview::game_window::print_top_row(void)
{
    int xcount;
    std::cout << " |";
    for (xcount = 0; xcount < draughts::model::board::get_instance()->get_width(); ++xcount)
    {
        std::cout << " " << xcount + 1 << " |";
    }
    std::cout << std::endl;
}

std::pair<int,int> draughts::ncview::game_window::strtocoord(
    const std::string& input)
{
    int x, y;
	try{
		std::vector<std::string> parts;
		boost::split(parts, input, [](char ch){ return ch == ',';});
		if(parts.size()!=2){
			throw "Your input format is wrong";
		}
		x = stoi(parts[0]);
		y = stoi(parts[1]);
	}catch(char const* ex){
		std::cerr <<*ex<< std::endl;
		x = -2;
		y = -2;
	}
	return std::make_pair(x,y);
}

void draughts::ncview::game_window::print_row(int rownum)
{
    int xcount;
    std::cout << rownum + 1<< " |";
    for(xcount = 0; xcount < draughts::model::board::get_instance()->get_width(); ++xcount)
    {
        std::cout << " " << draughts::model::player::get_instance()->get_token(rownum + 1, xcount + 1)
            << " |";
    }
    if(rownum == 2){
        std::cout <<"        Current Player: "<<draughts::model::player::get_instance()->player_pool[draughts::model::player::get_instance()->current_player]->player_name;
    }else if(rownum == 3){
        std::cout <<"        Score: "<<draughts::model::player::get_instance()->player_pool[draughts::model::player::get_instance()->current_player]->score;
    }else if(rownum == 4){
        std::cout <<"        Your normal token is \""<<draughts::model::player::get_instance()->player_pool[draughts::model::player::get_instance()->current_player]->normal_token<<"\"";
    }else if(rownum == 5){
        std::cout <<"        Your normal token direction is : ";
        std::cout<<"\033[1;91m";
        if(draughts::model::player::get_instance()->current_player==1){
            std::cout <<"↑";
        }else{
            std::cout <<"↓";
        }
        std::cout<<"\033[0m";
    }else if(rownum == 6){
        std::cout <<"        Your crown token is \""<<draughts::model::player::get_instance()->player_pool[draughts::model::player::get_instance()->current_player]->crown_token<<"\"";
    }else
    {
        
    }
    std::cout << std::endl;
}

void draughts::ncview::game_window::print_line(int numdashes)
{
    int count;
    for(count = 0; count < numdashes; ++count)
    {
        std::cout << '-';
    }
}

void draughts::ncview::game_window::display_board(void)
{
    int ycount;

    print_top_row();
    print_line(draughts::model::board::get_instance()->get_width() * 4+3);
    std::cout << std::endl;

    for(ycount = 0; ycount < draughts::model::board::get_instance()->get_height(); ycount++)
    {
        print_row(ycount);
        print_line(draughts::model::board::get_instance()->get_width() * 4+3);
        std::cout << std::endl;
    }
    std::cout <<draughts::model::player::get_instance()->player_pool[0]->player_name<<"'s score: "<<draughts::model::player::get_instance()->player_pool[0]->score<<"      "<<draughts::model::player::get_instance()->player_pool[1]->player_name<<"'s score: "<<draughts::model::player::get_instance()->player_pool[1]->score<<std::endl;
    std::cout <<"\n- Please enter \"Start coordinate End coordinate\"    Example:\"3,2 4,3\""<<std::endl;
    std::cout <<"- Or enter \"-1\" to quit"<<std::endl;
}

