from django.http import HttpResponse


class StripeWH_Handler:
    """
    Handle Stripe webhooks
    """
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle generic/unknown/unexpected webhook events
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}', status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle payment_intent.succeeded webhook events
        """
        intent = event.data.object
        print(intent)
        return HttpResponse(
            content=f'Webhook received: {event["type"]}', status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle payment_intent.payment_failed webhook events
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}', status=200)
