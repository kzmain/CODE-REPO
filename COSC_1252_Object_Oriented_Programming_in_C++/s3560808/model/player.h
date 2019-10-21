#include <vector>
#include <memory>
#include <utility>
#include <iostream>
#include <sstream>
#include <vector>
#include <thread>
#include <chrono>
#include "user.h"
#include "token.h"
namespace draughts
{
    namespace model
    {
        class player : public user
        {
        public:
            int user_id;
            std::string player_name;
            int score;
            
            std::string normal_token;
            std::string crown_token;
            int token_number;
            
            bool jump_move_lock;
            int last_x;
            int last_y;
            //Static int
            static int component_player;
            static int current_player;
            //Player Instance
            static std::unique_ptr<player> instance;
        public:
            std::vector<token> token_pool;
            static std::vector<std::unique_ptr<player>> player_pool;
            player(void):
                user_id(0),
                player_name(""),
                score(0),
                normal_token(""),
                crown_token(""),
                token_number()
            {}
            player(int player_id):
                user_id(player_id),
                player_name(get_user_name(player_id)),
                score(0),
                normal_token(""),
                crown_token(""),
                token_number(0),
                jump_move_lock(false),
                last_x(0),
                last_y(0)
            {
                //Set user name
                get_user_name(player_id);
                //Random current user
                srand(time(0));
                current_player = rand()%2;
                change_current_player();
            }
            virtual ~player(void){};
			player&  operator++();
            player operator++(int);
			
			void set_players(int, int);
            void set_demo_players(int, int, int);
            
            void get_winner(void);
            
            int get_current_player_id(void);
            int get_current_player(void);
            int get_component_player(void);
            std::string get_current_player_name(void);
            int get_current_player_score(void);
            std::vector<std::unique_ptr<draughts::model::player>> get_player_pool(void);
            std::vector<token> get_token_pool(void);
            void change_current_player(void);
            bool still_continue_jump(int, int, int, int, bool);
            bool in_bound(int, int, int, int,bool);
            bool basic_checks(int, int, int, int, bool);
            bool make_move(int, int, int, int, bool);
            bool jump_move(int, int, int, int,bool);
            bool next_step_detector(int, int);
            bool basic_move(int, int, int, int);
            bool check_current_user_start_piece(int, int, bool);
            bool check_current_user_end_piece(int, int, bool);
            bool eliminate_middle_piece(int, int, int, int,bool);
            void set_player_token(void);
            void set_demo_basic_move_token(void);
            void set_demo_jump_move_token(void);
            void set_demo_normal_to_crown_token(void);
            void set_demo_game_finish_check_token(void);
            void set_player_1_token(void);
            void set_player_2_token(void);
            std::string get_token(int, int);
            static player * get_instance(void);
            static void delete_instance(void);
            // void test_function(void);
        };
        
        

    }
}