from copy import deepcopy

class Vector:
    def __init_list_of_list(self, args: list, first_elem=False):
        if not first_elem:
            if not isinstance(args, list):
                raise TypeError("Inconsistent type argument")
            if len(args) != self.cols:
                raise ValueError("Inconsistent argument dimension")
        else:
            if isinstance(args[0], list):
                if len(args) == 0:
                    return
            self.cols = len(args)
        self.rows = self.rows + 1
        row = []
        for f in args:
            if not isinstance(f, float):
                raise TypeError("Expected float. Got " + str(type(f)))
            row.append(f * 1.0)
        self.values.append(row)

    def __init_list(self, args: list):
        if len(args) == 0:
            return
        if not isinstance(args[0], list):
            self.rows = 1
            for f in args:
                if not isinstance(f, float):
                    raise TypeError("Expected float. Got " + str(type(f)))
                self.values.append(f * 1.0)
                self.cols = self.cols + 1
        else:
            for i in range(len(args)):
                self.__init_list_of_list(args[i], (i == 0))
        self.shape = (self.rows, self.cols)

    def __init__(self, args=None):
        self.values = []
        self.shape = (0, 0)
        self.rows = 0
        self.cols = 0
        if isinstance(args, list):
            self.__init_list(args)
        elif isinstance(args, int):
            if args == 0:
                return
            elif args < 0:
                raise ValueError("Negative size not supported")
            self.__init_tuple((0, args))
        elif isinstance(args, tuple):
            self.__init_tuple(args)
        elif isinstance(args, Vector):
            self.shape = args.shape
            self.rows = args.rows
            self.cols = args.cols
            self.values = deepcopy(args.values)
        elif args is None:
            return
        else:
            raise TypeError(str(type(args))
                            + " not supported by Vector __init__")
        if self.rows == 1 and isinstance(self.values[0], list):
            self.values = self.values[0]
        elif self.rows != 1 and self.cols != 1 and self.shape != (0, 0):
            raise ValueError("Sorry, your Matrix is in another module")

    def __init_tuple(self, args: tuple):
        if len(args) != 2:
            raise ValueError("Tuple must contains 2 numbers only")
        if not isinstance(args[0], int) or not isinstance(args[1], int):
            raise TypeError("Expected (int, int). Got ("
                            + str(type(args[0])) + ", "
                            + str(type(args[1])) + ")")
        elif args[0] == args[1]:
            return
        if args[1] > args[0]:
            a = args[0]
            b = args[1]
        else:
            b = args[0]
            a = args[1]
        self.rows = b - a
        self.cols = 1
        self.shape = (self.rows, self.cols)
        for i in range(args[0], args[1], 1 - 2 * (args[1] <= args[0])):
            self.values.append([i * 1.0])

    def __mul__(self, other):
        if not (isinstance(other, int) or isinstance(other, float)):
            raise TypeError("Expected float or int. Got " + str(type(other)))
        temp = Vector(self)
        if self.rows == 1:
            for i in range(len(temp.values)):
                temp.values[i] = temp.values[i] * other
        else:
            for i in range(len(temp.values)):
                for j in range(len(temp.values[i])):
                    temp.values[i][j] = temp.values[i][j] * other
        return temp

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Expected Vector. Got " + str(type(other)))
        if (self.rows != other.rows or self.cols != other.cols):
            raise ValueError("Expected same vector shape. Got "
                             + str(self.shape) + " != " + str(other.shape))
        v = Vector(self)
        if self.rows == 1:
            for j in range(0, self.cols):
                v.values[j] = v.values[j] + other.values[j]
        else:
            for i in range(0, self.rows):
                for j in range(0, self.cols):
                    v.values[i][j] = v.values[i][j] + other.values[i][j]
        return (v)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Expected Vector. Got " + str(type(other)))
        return self.__add__(-1 * other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __truediv__(self, other):
        if not (isinstance(other, int) or isinstance(other, float)):
            raise TypeError("Expected float or int. Got " + str(type(other)))
        if other == 0:
            raise ZeroDivisionError("illegal 0 divisor")
        other = 1 / other
        return self.__mul__(other)

    def dot(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Expected Vector. Got " + str(type(other)))
        if (self.rows != other.rows or self.cols != other.cols):
            raise ValueError("Expected same vector shape. Got "
                             + str(self.shape) + " != " + str(other.shape))
        temp = 0.0
        if self.rows == 1:
            for j in range(0, self.cols):
                temp = temp + self.values[j] * other.values[j]
        else:
            for i in range(0, self.rows):
                for j in range(0, self.cols):
                    temp = temp + self.values[i][j] * other.values[i][j]
        return temp

    def T(self):
        if self.rows == 0 and self.rows == 0:
            return Vector(self)
        if self.rows == 0 or self.rows == 0:
            return Vector()
        temp = Vector()
        if self.rows == 1:
            for j in range(0, self.cols):
                temp.values[0].append([self.values[j]])
        elif self.cols == 1:
            for i in range(0, self.rows):
                temp.values.append(self.values[i][0])
            # print(temp)
        else:
            for i in range(0, self.rows):
                temp.values[i].append([])
                for j in range(0, self.cols):
                    temp.values[i][j].append(self.values[i][j])
        temp.shape = (self.shape[1], self.shape[0])
        temp.rows = self.cols
        temp.cols = self.rows
        return temp

    def __rtruediv__(self, other):
        raise TypeError("Division by class Vector not supported")

    def __neg__(self):
        return self.__mul__(-1)

    def __str__(self):
        return (str(self.values))

    def __repr__(self):
        return (str(self))
