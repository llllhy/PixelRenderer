from renderer.abstract_effectors.abstract_threading_effector import AbstractThreadingEffector
from renderer.color import *


class Effector(AbstractThreadingEffector):
    _name_ = 'Fade'
    _func_ = ['show', 'hide','switch']

    def get_frame_sum(self):
        return 5

    def show(self, frame_id, frame_sum):
        render_layer = np.zeros(self.element_shape, dtype='uint32')
        it = np.nditer(self.element_style, flags=['multi_index'])
        while not it.finished:
            pixel_color = it[0]
            pixel_opacity = get_color_opacity(pixel_color)
            if pixel_opacity == 0:
                it.iternext()
                continue
            opacity = self.opacity_transition(0, pixel_opacity, frame_sum, frame_id + 1)
            render_layer[it.multi_index[0]][it.multi_index[1]] = set_color_opacity(pixel_color, opacity)
            it.iternext()

        # for i in range(0, self.element_shape[0]):
        #     for j in range(0, self.element_shape[1]):
        #         pixel_color = self.element_style[i][j]
        #         pixel_opacity = get_color_opacity(pixel_color)
        #         if pixel_opacity == 0:
        #             continue
        #         opacity = self.opacity_transition(0, pixel_opacity, frame_sum, frame_id + 1)
        #         render_layer[i][j] = set_color_opacity(pixel_color, opacity)
        return self.position, render_layer

    def hide(self, frame_id, frame_sum):
        render_layer = np.zeros(self.element_shape, dtype='uint32')
        # for i in range(0, self.element_shape[0]):
        #     for j in range(0, self.element_shape[1]):
        #         pixel_color = self.element_style[i][j]
        #         pixel_opacity = get_color_opacity(pixel_color)
        #         if pixel_opacity == 0:
        #             continue
        #         opacity = self.opacity_transition(pixel_opacity, 0, frame_sum, frame_id + 1)
        #         render_layer[i][j] = set_color_opacity(pixel_color, opacity)
        it = np.nditer(self.element_style, flags=['multi_index'])
        while not it.finished:
            pixel_color = it[0]
            pixel_opacity = get_color_opacity(pixel_color)
            if pixel_opacity == 0:
                it.iternext()
                continue
            opacity = self.opacity_transition(pixel_opacity, 0, frame_sum, frame_id + 1)
            render_layer[it.multi_index[0]][it.multi_index[1]] = set_color_opacity(pixel_color, opacity)
            it.iternext()
        return self.position, render_layer

    def move(self, frame_id, frame_sum):
        return None

    def switch_element_style(self, element_after, frame_id, frame_sum):
        if frame_id < frame_sum / 2:
            return self.hide(frame_id, frame_sum / 2)
        else:
            render_layer = np.zeros(self.element_shape, dtype='uint32')
            it = np.nditer(self.element_style, flags=['multi_index'])
            while not it.finished:
                pixel_color = it[0]
                pixel_opacity = get_color_opacity(pixel_color)
                if pixel_opacity == 0:
                    it.iternext()
                    continue
                opacity = self.opacity_transition(0, pixel_opacity, frame_sum, frame_id + 1)
                render_layer[it.multi_index[0]][it.multi_index[1]] = set_color_opacity(pixel_color, opacity)
                it.iternext()
            return self.position, render_layer
