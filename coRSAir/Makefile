NAME = corsair

INCLUDE = -I /Users/fballest/.brew/opt/openssl@1.1/include 
LIBS = /Users/fballest/.brew/opt/openssl@1.1/lib/libcrypto.a /Users/fballest/.brew/opt/openssl@1.1/lib/libssl.a

CFLAGS = ${INCLUDE} ${SAN}

#SAN = -fsanitize=address -g3

SRC = corsair.c 
OBJ = ${SRC:.c=.o}

all: ${NAME}

${NAME} : ${OBJ}
	${CC} ${LIBS} ${OBJ} -O3 -o ${NAME} ${SAN}
re: clean all

clean:
	rm -rf ${OBJ}

fclean: clean
	rm -rf ${NAME}

.PHONY: all re clean fclean