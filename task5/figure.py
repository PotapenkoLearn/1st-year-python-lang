from abc import ABC, abstractmethod
from PIL import Image, ImageTk


class Figure(ABC):
    def __init__(self, x, y, type, rotation = 0):
        self.x = x
        self.y = y
        self.type = type
        # self.size = size
        # self.canvas = canvas

        # self.image_id = None
        self.rotation = rotation
        self.lighting = False

        # self.pil_image = Image.open(image).resize((self.size, self.size))
        # self.tk_image = ImageTk.PhotoImage(self.pil_image)

        # Сохраняем ссылку на изображение для того, что бы GC их не съел
        # self.canvas.image_refs = getattr(self.canvas, "image_refs", [])
        # self.canvas.image_refs.append(self.tk_image)

    def rotate(self):
        self.rotation = (self.rotation + 90) % 360

        # image_rotated = self.pil_image.rotate(-self.rotation, expand=True)
        #
        # self.tk_image = ImageTk.PhotoImage(image_rotated)
        #
        # self.canvas.itemconfig(self.image_id, image=self.tk_image)

    # def draw(self):
    # print(self.x, self.y, self.tk_image)
    # self.image_id = self.canvas.create_image(self.x, self.y, image=self.tk_image, anchor="nw")

    @abstractmethod
    def get_connections(self):
        pass


class LineFigure(Figure):
    def __init__(self, x, y, rotation):
        super().__init__(x, y, 'line', rotation)

    def get_connections(self):
        if self.rotation % 180 == 0:
            return {'left', 'right'}

        return {'up', 'down'}


class CornerFigure(Figure):
    def __init__(self, x, y, rotation):
        super().__init__(x, y, 'corner', rotation)

    def get_connections(self):
        match self.rotation:
            case 90:
                return {'right', 'down'}
            case 180:
                return {'down', 'left'}
            case 270:
                return {'left', 'up'}
            case _:
                return {'up', 'right'}
