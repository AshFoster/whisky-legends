/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

let stripePublicKey = document.getElementById('id_stripe_public_key').textContent.slice(1, -1);
let clientSecret = document.getElementById('id_client_secret').textContent.slice(1, -1)
let stripe = Stripe(stripePublicKey, {locale: 'en-GB'});
let elements = stripe.elements();
let style = {
    base: {
        color: '#000',
        fontFamily: "'Roboto Condensed', sans-serif",
        fontSmoothing: 'antialiased',
        fontSize: '16px',
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
let card = elements.create('card', {style: style});
card.mount('#card-element'); 

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    let errorDiv = document.getElementById('card-errors');
    if (event.error) {
        let html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        errorDiv.innerHTML = html;
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit
let form = document.getElementById('payment-form');
let submitButton = document.getElementById('submit-button');

form.addEventListener('submit', function(e) {
    e.preventDefault();
    card.update({ 'disabled': true });
    submitButton.setAttribute('disabled', true);
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        if (result.error) {
            let errorDiv = document.getElementById('card-errors');
            let html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>
            `;
            errorDiv.innerHTML = html;
            card.update({ 'disabled': false });
            submitButton.setAttribute('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});