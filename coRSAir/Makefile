NAME = corsair

INCLUDE = -I /Users/fballest/42/miniconda3/include/ 
LIBS = /Users/fballest/42/miniconda3/lib/libcrypto.a /Users/fballest/42/miniconda3/lib/libssl.a

CFLAGS = ${INCLUDE}

SRC = main.c 
OBJ = ${SRC:.c=.o}

all: ${NAME}

${NAME} : ${OBJ}
	${CC} ${LIBS} ${OBJ} -fsanitize=address -g3 -O3 -o ${NAME} 
re: clean all

clean:
	rm -rf ${OBJ}

fclean: clean
	rm -rf ${NAME}

.PHONY: all re clean fclean