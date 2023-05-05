NAME = corsair

INCLUDE = -I /goinfre/fballest/miniconda3/include/ 
LIBS = /goinfre/fballest/miniconda3/lib/libcrypto.a /goinfre/fballest/miniconda3/lib/libssl.a

CFLAGS = ${INCLUDE}

SRC = main.c 
OBJ = ${SRC:.c=.o}

all: ${NAME}

${NAME} : ${OBJ}
	${CC} ${LIBS} ${OBJ} -O3 -o ${NAME} 
re: clean all

clean:
	rm -rf ${OBJ}

fclean: clean
	rm -rf ${NAME}

.PHONY: all re clean fclean