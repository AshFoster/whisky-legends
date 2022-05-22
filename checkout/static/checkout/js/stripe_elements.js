/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

let stripePublicKey = document.getElementById('id_stripe_public_key').textContent.slice(1, -1);
let clientSecret = document.getElementById('id_client_secret').textContent.slice(1, -1);
let stripe = Stripe(stripePublicKey);
let elements = stripe.elements({
    fonts: [
        {
            cssSrc: "https://fonts.googleapis.com/css2?family=Lobster&family=Lato&family=Roboto+Condensed&display=swap",
        },
    ],
});
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

let card = elements.create('card', {
    style: style,
    hidePostalCode: true,
});
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
let loadingOverlay = document.getElementById('loading-overlay');

form.addEventListener('submit', function (e) {
    e.preventDefault();
    card.update({
        'disabled': true
    });
    submitButton.setAttribute('disabled', 'true');
    loadingOverlay.classList.remove('fadeout');
    loadingOverlay.classList.add('fadein', 'd-block');

    let saveInfo = document.getElementById('id-save-info');

    if (saveInfo == null) {
        saveInfo = false;
    } else {
        saveInfo = Boolean(saveInfo.checked);
    }

    let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    let url = '/checkout/cache_checkout_data/';
    let postData = 'csrfmiddlewaretoken=' + encodeURIComponent(csrfToken) + '&client_secret=' + clientSecret + '&save_info=' + saveInfo;
    let httpRequest = new XMLHttpRequest();

    httpRequest.open('POST', url);
    httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState == 4) {
            if (httpRequest.status == 200) {
                stripe.confirmCardPayment(clientSecret, {
                    payment_method: {
                        card: card,
                        billing_details: {
                            name: form.full_name.value.trim(),
                            email: form.email.value.trim(),
                            phone: form.phone_number.value.trim(),
                            address: {
                                line1: form.street_address1.value.trim(),
                                line2: form.street_address2.value.trim(),
                                city: form.town_or_city.value.trim(),
                                state: form.county.value.trim(),
                                country: form.country.value.trim(),
                            }
                        }
                    },
                    shipping: {
                        name: form.full_name.value.trim(),
                        phone: form.phone_number.value.trim(),
                        address: {
                            line1: form.street_address1.value.trim(),
                            line2: form.street_address2.value.trim(),
                            city: form.town_or_city.value.trim(),
                            state: form.county.value.trim(),
                            postal_code: form.postcode.value.trim(),
                            country: form.country.value.trim(),
                        }
                    }
                }).then(function (result) {
                    if (result.error) {
                        let errorDiv = document.getElementById('card-errors');
                        let html = `
                            <span class="icon" role="alert">
                            <i class="fas fa-times"></i>
                            </span>
                            <span>${result.error.message}</span>
                        `;
                        errorDiv.innerHTML = html;
                        loadingOverlay.classList.add('fadeout');
                        loadingOverlay.classList.remove('fadein', 'd-block');
                        card.update({
                            'disabled': false
                        });
                        submitButton.removeAttribute('disabled', 'true');
                    } else {
                        if (result.paymentIntent.status === 'succeeded') {
                            form.submit();
                        }
                    }
                });
            } else {
                location.reload();
            }
        }
    };
    httpRequest.send(postData);
});