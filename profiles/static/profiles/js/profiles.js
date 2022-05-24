// CREDIT - The functions here were inspired by Code Institute's walkthrough
// project 'Boutique Ado', and the method on how to use AJAX without jQuery
// was found here: https://stackoverflow.com/questions/64612746/how-would-i-do-this-ajax-jquery-in-vanilla-js

// Set colour of country field to look muted if none selected
let defaultCountry = document.getElementById('id_default_country');

if (defaultCountry != null) {
    let countrySelected = defaultCountry.value;
    if(!countrySelected) {
        defaultCountry.style.color = '#7e868d';
    }
    defaultCountry.addEventListener('change', function () {
        countrySelected = this.value;
        if(!countrySelected) {
            defaultCountry.style.color = '#7e868d';
        } else {
            defaultCountry.style.color = '#212529';
        }
    });
}

// Remove from wishlist and reload on click
document.querySelectorAll('.remove-btn').forEach(item => {
    item.addEventListener('click', function () {
        let wishlistForm = this.closest('.wishlist-form');
        let formData = new FormData(wishlistForm);
        let productId = this.getAttribute('data-id').split('wishlist-')[1];
        let url = `/profile/wishlist/update/${productId}/`;
        let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        let httpRequest = new XMLHttpRequest();
        httpRequest.open('POST', url);
        httpRequest.setRequestHeader('X-CSRF-Token', csrfToken);
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState == 4 && httpRequest.status == 200) {
                location.reload();
            }
        };
        httpRequest.send(formData);
    });
});