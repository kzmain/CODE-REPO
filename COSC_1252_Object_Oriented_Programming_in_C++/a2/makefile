#****************************************************************
#
#         Course code: COSC1252/1254
#         Student Number: s3560808
#         Date: 08.2017
#
#****************************************************************\
VAL=valgrind --leak-check=full
CC = g++
CPPFLAGS = -Wall -pedantic -std=c++14

main: main_noncurses.cpp ./ncview/ui.o ./nc_controller/controller.o ./model/model.o ./ncview/main_menu.o ./ncview/demo_menu.o ./ncview/menu.o ./ncview/add_player_window.o ./ncview/game_window.o ./ncview/player_selection_window.o ./ncview/window.o ./model/user.o ./model/player.o ./model/board.o ./model/token.o ./nc_controller/command.o 
	$(CC) $(CPPFLAGS) -o main main_noncurses.cpp ./ncview/ui.o ./nc_controller/controller.o ./model/model.o ./ncview/main_menu.o ./ncview/demo_menu.o ./ncview/menu.o ./ncview/add_player_window.o ./ncview/game_window.o ./ncview/player_selection_window.o ./ncview/window.o ./model/user.o ./model/player.o ./model/board.o ./model/token.o ./nc_controller/command.o 

#model
./model/model.o: ./model/model.cpp
	$(CC) $(CPPFLAGS) -c -o ./model/model.o ./model/model.cpp
	
./model/user.o: ./model/user.cpp
	$(CC) $(CPPFLAGS) -c -o ./model/user.o ./model/user.cpp
	
./model/player.o: ./model/player.cpp
	$(CC) $(CPPFLAGS) -c -o ./model/player.o ./model/player.cpp
	
./model/board.o: ./model/board.cpp
	$(CC) $(CPPFLAGS) -c -o ./model/board.o ./model/board.cpp
	
./model/token.o: ./model/token.cpp
	$(CC) $(CPPFLAGS) -c -o ./model/token.o ./model/token.cpp
#nc_controller
./nc_controller/controller.o:./nc_controller/controller.cpp
	$(CC) $(CPPFLAGS) -c -o ./nc_controller/controller.o ./nc_controller/controller.cpp
	
./nc_controller/command.o:./nc_controller/command.cpp
	$(CC) $(CPPFLAGS) -c -o ./nc_controller/command.o ./nc_controller/command.cpp
#ncview
./ncview/add_player_window.o:./ncview/add_player_window.cpp
	$(CC) $(CPPFLAGS) -c -o ./ncview/add_player_window.o ./ncview/add_player_window.cpp

./ncview/game_window.o:./ncview/game_window.cpp
	$(CC) $(CPPFLAGS) -c -o ./ncview/game_window.o ./ncview/game_window.cpp

./ncview/main_menu.o:./ncview/main_menu.cpp
	$(CC) $(CPPFLAGS) -c -o ./ncview/main_menu.o ./ncview/main_menu.cpp
	
./ncview/demo_menu.o:./ncview/demo_menu.cpp
	$(CC) $(CPPFLAGS) -c -o ./ncview/demo_menu.o ./ncview/demo_menu.cpp
	
./ncview/menu.o:./ncview/menu.cpp
	$(CC) $(CPPFLAGS) -c -o ./ncview/menu.o ./ncview/menu.cpp
	
./ncview/player_selection_window.o:./ncview/player_selection_window.cpp
	$(CC) $(CPPFLAGS) -c -o ./ncview/player_selection_window.o ./ncview/player_selection_window.cpp

./ncview/ui.o:./ncview/ui.cpp
	$(CC) $(CPPFLAGS) -c -o ./ncview/ui.o ./ncview/ui.cpp

./ncview/window.o:./ncview/window.cpp
	$(CC) $(CPPFLAGS) -c -o ./ncview/window.o ./ncview/window.cpp
	
clean:
	rm main ./model/*.o ./nc_controller/*.o ./ncview/*.o