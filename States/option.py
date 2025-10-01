import pygame
import config

pygame.font.init()
font_large = pygame.font.SysFont("consolas", 50)
font_small = pygame.font.SysFont("consolas", 28)

BLACK = config.BLACK
GREEN = config.GREEN
WHITE = config.WHITE

class Option:
    def __init__(self, width, height, start_points=50):
        self.width = width
        self.height = height

        # Current number of data points (default = 50)
        self.num_points = start_points

        # Slider settings
        self.min_val = 5
        self.max_val = 70
        self.slider_x = 200
        self.slider_y = height // 2
        self.slider_w = 600
        self.slider_h = 6
        self.knob_radius = 12
        self.dragging = False

        # Back button
        self.back_rect = pygame.Rect(50, height - 80, 120, 40)

    def _clamp_knob_x(self, mx):
        return max(self.slider_x, min(mx, self.slider_x + self.slider_w))

    def _set_value_from_x(self, mx):
        mx = self._clamp_knob_x(mx)
        ratio = (mx - self.slider_x) / self.slider_w
        new_val = int(round(self.min_val + ratio * (self.max_val - self.min_val)))
        self.num_points = max(self.min_val, min(new_val, self.max_val))

    def get_knob_x(self):
        ratio = (self.num_points - self.min_val) / (self.max_val - self.min_val)
        return int(self.slider_x + ratio * self.slider_w)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Back button check
            if self.back_rect.collidepoint(mx, my):
                return "menu"

            # Slider knob check
            knob_x = self.get_knob_x()
            on_knob = (abs(mx - knob_x) <= self.knob_radius and abs(my - self.slider_y) <= 20)
            on_track = (self.slider_x <= mx <= self.slider_x + self.slider_w and
                        self.slider_y - 10 <= my <= self.slider_y + 10)
            if on_knob or on_track:
                self.dragging = True
                self._set_value_from_x(mx)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._set_value_from_x(event.pos[0])

        return None

    def draw(self, screen):
        screen.fill(BLACK)

        header = font_large.render("OPTIONS", True, GREEN)
        screen.blit(header, header.get_rect(center=(self.width // 2, 100)))

        label = font_small.render(f"Number of Data Points: {self.num_points}", True, WHITE)
        screen.blit(label, label.get_rect(center=(self.width // 2, self.slider_y - 40)))

        # Slider track
        pygame.draw.line(screen, GREEN,
                         (self.slider_x, self.slider_y),
                         (self.slider_x + self.slider_w, self.slider_y),
                         self.slider_h)

        # Slider knob
        pygame.draw.circle(screen, GREEN, (self.get_knob_x(), self.slider_y), self.knob_radius)

        # Back button
        pygame.draw.rect(screen, GREEN, self.back_rect, 2, border_radius=5)
        back_text = font_small.render("BACK", True, GREEN)
        screen.blit(back_text, back_text.get_rect(center=self.back_rect.center))