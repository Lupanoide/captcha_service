from captcha_validation.business.ConfigBusiness import ConfigBusiness
from random import randint, uniform
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from captcha_validation.dao.ManageCaptcha import ManageCaptcha
from captcha_validation.model.Protocolz import Outcome

class CaptchaBusiness(ConfigBusiness):
    def __init__(self):
        ConfigBusiness.__init__(self)
        self.dao = ManageCaptcha()


    def get_random_color(self):
        # random color rgb
        return randint(120, 200), randint(120, 200), randint(120, 200)


    def get_random_char(self):
        """
        # random characters
        # list of list [['0','1',2','3','4','5','6','7','8','9'],
        #                ['A','B','C','D','E','F','G','H','I','J','K','L','M','N',[...]],
        #                ['a','b','c','d','e',f','g',[...]]
        #                   ]
        #
        :return:
        """

        codes = [[chr(i) for i in range(48, 58)], [chr(i) for i in range(65, 91)], [chr(i) for i in range(97, 123)]]
        codes = codes[randint(0, 2)]
        faith = randint(0, len(codes) - 1)
        return codes[faith]


    def generate_captcha(self, address):
        # generate verification code
        length = randint(self.min_char_len, self.max_char_len)
        k_offset = self.width / (length + 1)
        number_of_lines = randint(self.min_num_lines,self.max_num_lines)
        number_of_points = randint(self.min_num_points,self.max_num_points)

        img = Image.new("RGB", (self.width, self.height), (250, 250, 250))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(self.ttf_file, size=self.font_size)
        # captcha_validation text
        text = ""
        for i in range(length):
            char = self.get_random_char()

            text += char
            shift_len = uniform(self.min_shift_len, self.max_shift_len)
            draw.text(( k_offset * (i + 1) - (k_offset*shift_len) , shift_len * self.height ), char, font=font, fill=self.get_random_color())

        # add interference line
        for i in range(number_of_lines):
            x1 = randint(0, self.width)
            y1 = randint(0, self.height)
            x2 = randint(0, self.width)
            y2 = randint(0, self.height)
            draw.line((x1, y1, x2, y2), fill=self.get_random_color())
        # add interference point
        for i in range(number_of_points):
            draw.point((randint(0, self.width), randint(0, self.height)), fill=self.get_random_color())
        # save the picture
        #img.save(r"../resources/" + text + ".jpg")
        img_io = BytesIO()
        img.save(img_io,'JPEG', quality=70)
        self.log.debug("Captcha created. Prepare to load into db")
        self.dao.ingest(address,text.lower())
        return Outcome(img_io, True)
        #return text + ".jpg"

    def validate_captcha(self, solution, address):
        if not self.stringValidator.exec_validation(solution):
            self.log.error(f"The provided argument solution is not a string. Found: {type(solution)}")
            return Outcome(f"The provided argument solution is not a string. Found: {type(solution)}", False)
        return self.dao.query_for_validation(solution.lower(), address)