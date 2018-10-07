import cairo

left_guard = "101"
right_guard = "101"
center_guard = "01010"
dict_lcode = {
    0: "0001101",
    1: "0011001",
    2: "0010011",
    3: "0111101",
    4: "0100011",
    5: "0110001",
    6: "0101111",
    7: "0111011",
    8: "0110111",
    9: "0001011"
}

dict_rcode = {
    0: "1110010",
    1: "1100110",
    2: "1101100",
    3: "1000010",
    4: "1011100",
    5: "1001110",
    6: "1010000",
    7: "1000100",
    8: "1001000",
    9: "1110100"
}

WIDTH, HEIGHT = 600, 300
surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context (surface)

number = "5100001251"
number_list = [0] + [ int(c) for c in number ]

check1 = 3 * sum(number_list[::2]) + sum(number_list[1::2])
check2 = 10 - check1 % 10
if check2 == 10:
    check2 = 0
number_list.append(check2)

code = left_guard
for i in range(6):
    code += dict_lcode[number_list[i]]
code += center_guard
for i in range(6, 12):
    code += dict_rcode[number_list[i]]
code += right_guard

def draw_code(ctx, code):
    Width_per_code = 5
    Height_per_code = 200
    ctx.translate(50, 50)
    ctx.set_source_rgb(0, 0, 0)
    for i, c in enumerate(code):
        xpos = Width_per_code * i
        if c=="1":
            ctx.rectangle(xpos, 0, Width_per_code, Height_per_code)
            ctx.fill()

draw_code(ctx,code)

'''
ctx.translate(50, 50)
code = [0,1,0,1,1,1]

Width_per_code = 10
Height_per_code = 200

ctx.set_source_rgb(0, 0, 0)
for i, c in enumerate(code):
    xpos = Width_per_code * i
    if c:
        ctx.rectangle(xpos, 0, Width_per_code, Height_per_code)
        ctx.fill()
'''

surface.write_to_png ("barcode2.png") # Output to PNG