from django.views.generic import TemplateView

class Game1View(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MemoryGame1View(TemplateView):
    template_name = "memory_game.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context