inp w     # w = inp[0]
mul x 0   # x = 0
add x z   # x += z          # x = 0
mod x 26  # x = x % 26      # x = 0
div z 1   # z = z / 1
add x 10  # x = x + 10      # x = 10
eql x w   # x = (x == w)    # x = 0
eql x 0   # x = !x          # x = 1
mul y 0   # y = 0
add y 25  # y = 25
mul y x   # y = 25
add y 1   # y = 26
mul z y   # z = 0 
mul y 0   # y = 0
add y w   # y = I0
add y 1   # y = I0 + 1
mul y x   # y = I0 + 1
add z y   # z = I0 + 1

inp w     # w = inp[1]
mul x 0   # x = 0
add x z   # x = I0 + 1
mod x 26  # x = I0 + 1
div z 1   # z = I0 + 1
add x 11  # x = I0 + 12
eql x w   # x = 0
eql x 0   # x = 1
mul y 0   # y = 0
add y 25  # y = 25
mul y x   # y = 25
add y 1   # y = 26
mul z y   # z = (I0+1, 0)
mul y 0   # y = 0
add y w   # y = I1
add y 9   # y = I1+9
mul y x   # y = I1+9
add z y   # z = (I0+1, I1+9)

inp w     # w = I2
mul x 0   # x = 0
add x z   # x = 
mod x 26  # x = I1+9
div z 1   # z = z / 1
add x 14  # x = I1 + 23
eql x w   # x = 0
eql x 0   # x = 1
mul y 0   # y = 0
add y 25  # y = 25
mul y x   # y = 25
add y 1   # y = 26
mul z y   # z = (I0+1, I1+9, 0)
mul y 0   # y = 0
add y w   # y = I2
add y 12  # y = I2+12
mul y x   # y = I2+12
add z y   # z = (I0+1, I1+9, I2+12)

inp w     # w = inp[3]
mul x 0   # x = 0
add x z   # 
mod x 26  # x = I2+12
div z 1   # z = z / 1
add x 13  # x = I2+25
eql x w   # x = 0 
eql x 0   # x = 1
mul y 0   # y = 0
add y 25  # y = 25
mul y x   # y = 25
add y 1   # y = 26
mul z y   # z = (I0+1, I1+9, I2+12, 0)
mul y 0   # y = 0
add y w   # y = I3
add y 6   # y = I3 + 6
mul y x   # y = I3 + 6
add z y   # z = (I0+1, I1+9, I2+12, I3+6)

inp w     # w = inp[4]
mul x 0   # x = 0
add x z   # 
mod x 26  # x = I3+6
div z 26  # z = (I0+1, I1+9, I2+12)
add x -6  # x = I3
eql x w   # x = 1                       # I3 == I4
eql x 0   # x = 9
mul y 0   # y = 0
add y 25  # y = 25
mul y x   # y = 0
add y 1   # y = 1
mul z y   # z = (I0+1, I1+9, I2+12)
mul y 0   # y = 0
add y w   # y = I4
add y 9   # y = I4 + 9
mul y x   # y = 0
add z y   # z = (I0+1, I1+9, I2+12)

inp w     # w = inp[5]
mul x 0   # x = 0
add x z   # 
mod x 26  # x = I2+I4+21
div z 26  # z = (I0+1, I1+9, I2+12)
add x -14 # x = I2+I4+7
eql x w   # x = 0                       # I5 == I4 - 5
eql x 0   # x = 1
mul y 0   # y = 0
add y 25  # y = 25
mul y x   # y = 25
add y 1   # y = 26
mul z y   # z = (I0+1, I1+9, I2+12, I4+9, 0)
mul y 0   # y = 0
add y w   # y = I5
add y 15  # y = I5 + 15
mul y x   # y = I5 + 15
add z y   # z = (I0+1, I1+9, I2+12, I4+9, I5+15)

inp w     # w = inp[6]
mul x 0   # x = 0
add x z   # 
mod x 26  # x = I5 + 15
div z 1   # z = z / 1
add x 14  # x = I5 + 29
eql x w   # x = 0
eql x 0   # x = 1
mul y 0   # y = 0
add y 25  # y = 25
mul y x   # y = 25
add y 1   # y = 26
mul z y   # z = (I0+1, I1+9, I2+12, I4+9, I5+15, 0)
mul y 0   # y = 0
add y w   # y = I6
add y 7   # y = I6 + 7
mul y x   # y = I6 + 7
add z y   # z = (I0+1, I1+9, I2+12, I4+9, I5+15, I6+7)

inp w     # w = inp[7]
mul x 0   # x = 0
add x z   #
mod x 26  # x = I6+7
div z 1   # z = z / 1
add x 13  # x = I6+20
eql x w   # x = 0
eql x 0   # x = 1
mul y 0   # y = 0
add y 25  # y = 25
mul y x   # y = 25
add y 1   # y = 26
mul z y   # z = (I0+1, I1+9, I2+12, I4+9, I5+15, I6+7, 0)
mul y 0   # y = 0
add y w   # y = I7
add y 12  # y = I7+12
mul y x   # y = I7+12
add z y   # z = (I0+1, I1+9, I2+12, I4+9, I5+15, I6+7, I7+12)

inp w     # w = inp[8]
mul x 0   # x = 0
add x z   # 
mod x 26  # x = I7+12
div z 26  # z = (I0+1, I1+9, I2+12, I4+9, I5+15, I6+7)
add x -8  # x = I7+4
eql x w   # x = 0                                       # I7+4 == I8
eql x 0   # x = 1
mul y 0   # y = 0
add y 25  # y = 25
mul y x   # y = 25
add y 1   # y = 26
mul z y   # z = (I0+1, I1+9, I2+12, I4+9, I5+15, I6+7, 0)
mul y 0   # y = 0
add y w   # y = I8
add y 15  # y = I8 + 15
mul y x   # y = I8 + 15
add z y   # z = (I0+1, I1+9, I2+12, I4+9, I5+15, I6+7, I8+15)

inp w     # w = inp[9]
mul x 0   # x = 0
add x z   #
mod x 26  # x = I8+15
div z 26  # z = (I0+1, I1+9, I2+12, I4+9, I5+15, I6+7)
add x -15 # x = I8
eql x w   # x = 0                                       # I9 == I8
eql x 0   # x = 1
mul y 0   # y = 0
add y 25  # y = 25
mul y x   # y = 25
add y 1   # y = 26
mul z y   # z = (I0+1, I1+9, I2+12, I4+9, I5+15, I6+7, 0)
mul y 0   # y = 0
add y w   # y = I9
add y 3   # y = I9 + 3
mul y x   # y = I9 + 3
add z y   # z = (I0+1, I1+9, I2+12, I4+9, I5+15, I6+7, I9+3)

inp w     # w = inp[10]
mul x 0   # x = 0
add x z   #
mod x 26  # x = I9+3
div z 1   # z = z / 1
add x 10  # x = I9+13
eql x w   # x = 0
eql x 0   # x = 1
mul y 0   # y = 0
add y 25  # y = 25
mul y x   # y = 25
add y 1   # y = 26
mul z y   # z = (I0+1, I1+9, I2+12, I4+9, I5+15, I6+7, I9+3, 0)
mul y 0   # y = 0
add y w   # y = I10
add y 6   # y = I10 + 6
mul y x   # y = I10 + 6
add z y   # z = (I0+1, I1+9, I2+12, I4+9, I5+15, I6+7, I9+3, I10+6)

inp w     # w = inp[11]
mul x 0   # x = 0
add x z   # 
mod x 26  #
div z 26  #
add x -11 #
eql x w   #
eql x 0   #
mul y 0   # y = 0
add y 25  # y = 25
mul y x   # y = 25
add y 1   # y = 26
mul z y   #
mul y 0   # y = 0
add y w   #
add y 2   #
mul y x   #
add z y   #

inp w     # w = inp[12]
mul x 0   # x = 0
add x z   #
mod x 26  #
div z 26  #
add x -13 #
eql x w   #
eql x 0   #
mul y 0   # y = 0
add y 25  # y = 25
mul y x   # y = 25
add y 1   # y = 26
mul z y   #
mul y 0   # y = 0
add y w   #
add y 10  #
mul y x   #
add z y   #

inp w     # w = inp[13]
mul x 0   # x = 0
add x z   # x = z
mod x 26  # x = z % 26
div z 26  # z /= 26             # x = pop()
add x -4  # x = (z % 26) - 4
eql x w   # 
eql x 0   #
mul y 0   # y = 0
add y 25  # y = 25
mul y x   # y = 25 * x
add y 1   # y = 25 * x + 1
mul z y   # z = z * (25 * x + 1)
mul y 0   # y = 0
add y w   # y = w
add y 12  # y = w + 12
mul y x   # y = x * (w + 12)
add z y   # 

i[13] - 4
