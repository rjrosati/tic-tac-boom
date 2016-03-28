CC=g++
DEBUG=-g -Wall -Wextra
CFLAGS=-c $(DEBUG)
LFLAGS= $(DEBUG)
OBJS= tic_tac_boom.o map.o lodepng.o

all: $(OBJS)
	$(CC) $(LFLAGS) $(OBJS) -o tic_tac_boom

.cpp.o:
	$(CC) $(CFLAGS) $*.cpp

tic_tac_boom.o: tic_tac_boom.cpp lodepng.h map.h

map.o: map.cpp map.h

lodepng.o: lodepng.cpp lodepng.h
