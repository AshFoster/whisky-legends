from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic.edit import FormView
from whiskylegends.settings import DEFAULT_FROM_EMAIL
from .forms import ContactForm


class Contact(FormView):
    """
    View used to process ContactForm form
    """
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = '/contact/'

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super().get_initial()

        if hasattr(self.request.user, 'userprofile'):
            if self.request.user.userprofile.default_full_name == '':
                initial['name'] = self.request.user.username
            else:
                initial['name'] = self.request.user.userprofile.default_full_name

            initial['email'] = self.request.user.email

        return initial

    def form_valid(self, form):
        """
        Sends contact form message as email if form is valid when submitted
        """
        name = self.request.POST.get('name')
        email = self.request.POST.get('email')
        message = self.request.POST.get('message')
        email_subject = ('From ' + name +
                         ': via Contact Us form - Whisky Legends')
        email_message = 'Reply to: ' + email + '\n\n' + message

        send_mail(
            email_subject,
            email_message,
            DEFAULT_FROM_EMAIL,
            [DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        messages.add_message(self.request,
                             messages.SUCCESS,
                             'Your message has been sent successfully.')
        return super().form_valid(form)
