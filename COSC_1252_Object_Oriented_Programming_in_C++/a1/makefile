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
main: main.cpp dstru.o slist.o bst.o
	$(CC) $(CPPFLAGS) -o test_datastructures main.cpp dstru.o slist.o

dstru.o: ./datastructure/dstru.cpp
	$(CC) $(CPPFLAGS) -c ./datastructure/dstru.cpp
    
slist.o: ./datastructure/slist.cpp
	$(CC) $(CPPFLAGS) -c ./datastructure/slist.cpp
    
bst.o: ./datastructure/bst.cpp
	$(CC) $(CPPFLAGS) -c ./datastructure/bst.cpp
clean:
	rm *.o test_datastructures