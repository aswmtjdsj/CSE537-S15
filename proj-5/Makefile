CC=g++

INC=-I/usr/local/include/
CFLAGS=-Wall -W -g --std=c++0x 
LIB=-L/usr/local/lib/ -lopencv_core -lopencv_imgproc -lopencv_imgcodecs -lopencv_features2d -lopencv_ml
SRC=dtree.cpp

main: $(SRC)
	$(CC) $(CFLAGS) $^ -o $@ $(LIB) $(INC)

clean:
	-rm $(OBJ) main
