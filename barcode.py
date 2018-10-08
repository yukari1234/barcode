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

#初始化空块
class EmptyBlock(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def draw(self, ctx, xpos, ypos):
        ctx.rectangle(xpos, ypos, self.width, self.height)
        ctx.stroke()

#条形码类里的初始化、画条、分小格函数
class BarCode(object): 
    def __init__(self, number): 
        self.number = number 
    
    def draw(self, ctx, xpos=0, ypos=0): 
        blocks = self.make_blocks() 
        for b in blocks: 
            b.draw(ctx, xpos, ypos) 
            xpos += b.width 
            print (xpos) 
    
    def make_blocks(self):
        number_list = [0] + [ int(c) for c in self.number ]
        check1 = 3 * sum(number_list[::2]) + sum(number_list[1::2])
        check2 = 10 - check1 % 10
        if check2 == 10:
            check2 = 0
        number_list.append(check2)

        blocks = []
        blocks.append(LeftRightGuard())
        blocks.append(NumberBlock(number_list[0], isLeft=True))
        for i in number_list[1:6]:
            blocks.append(NumberBlockWithText(i, isLeft=True))
        blocks.append(CenterGuard())
        for i in number_list[6:-1]:
            blocks.append(NumberBlockWithText(i, isLeft=False))
        blocks.append(NumberBlock(number_list[-1], isLeft=False))
        blocks.append(LeftRightGuard())
        return blocks

class CodeBlock(EmptyBlock):
    Width_per_code = 5
    Height_per_code = 200

    def __init__(self, code="0"):
        self.code = code
        width = len(self.code) * CodeBlock.Width_per_code
        height = CodeBlock.Height_per_code
        super(CodeBlock, self).__init__(width, height)

    def draw(self, ctx, xpos, ypos):
        print ("draw code", self.code, "@", xpos, self.width)
        ctx.set_source_rgb(1, 0, 0)
        for i, c in enumerate(self.code):
            if c=="1":
                ctx.rectangle(xpos+CodeBlock.Width_per_code * i, ypos, CodeBlock.Width_per_code, CodeBlock.Height_per_code)
                ctx.fill()

class LeftRightGuard(CodeBlock):
    def __init__(self):
        super(LeftRightGuard, self).__init__(code="101")

class CenterGuard(CodeBlock):
    def __init__(self):
        super(CenterGuard, self).__init__(code="01010")

class NumberBlock(CodeBlock):
    Height_per_codeline = 170

    def __init__(self, number, isLeft=True):
        self.number = number
        if isLeft:
            code = dict_lcode[ number ]
        else:
            code = dict_rcode[ number ]
        super(NumberBlock, self).__init__(code=code)

    def draw(self, ctx, xpos, ypos):
        print ("draw code", self.code, "@", xpos, self.width)
        ctx.set_source_rgb(0, 0, 1)
        for i, c in enumerate(self.code):
            if c=="1":
                ctx.rectangle(xpos+CodeBlock.Width_per_code * i, ypos,CodeBlock.Width_per_code, NumberBlock.Height_per_codeline)
                ctx.fill()

class NumberBlockWithText(NumberBlock):
    def draw(self, ctx, xpos, ypos):
        super(NumberBlockWithText, self).draw(ctx, xpos, ypos)
        ctx.select_font_face("Times New Roman", cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(30)
        s = str(self.number)
        (x, y, width, height, dx, dy) = ctx.text_extents(s)
        xcenter = xpos + (CodeBlock.Width_per_code * len(self.code))/2.0 - width/2.0
        ycenter = ypos + (NumberBlock.Height_per_codeline + CodeBlock.Height_per_code)/2.0 + height/2.0
        ctx.move_to( xcenter, ycenter )
        ctx.show_text(s)

WIDTH, HEIGHT = 600, 300
surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context (surface)

barcode = BarCode("5100001251")
ctx.translate(50, 50)
ctx.set_source_rgb(0, 0, 0)
barcode.draw(ctx)
surface.write_to_png ("barcode3.png") # Output to PNG

'''
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

#最初版本
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


surface.write_to_png ("barcode2.png") # Output to PNG
'''