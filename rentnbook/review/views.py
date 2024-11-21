from django.urls import reverse
from django.views.generic import CreateView

from accommodation.models import Accommodation
from review.forms import ReviewForm
from review.models import Review


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/review_create.html'

    def form_valid(self, form):
        accommodation = Accommodation.objects.get(uuid=self.kwargs['uuid'])
        renter = self.request.user.renter_profile

        # Створення виведення повідомлення про помилку
        if Review.objects.filter(accommodation=accommodation, renter=renter).exists():
            form.add_error("rating", "Ви вже залишали відгук для цього житла.")
            return self.form_invalid(form)

        form.instance.renter = renter
        form.instance.accommodation = accommodation

        return super().form_valid(form)

    def get_success_url(self):
        # Перенаправляє на сторінку деталі житла після успішного створення відгуку
        return reverse('accommodation_detail', kwargs={'uuid': self.kwargs['uuid']})
