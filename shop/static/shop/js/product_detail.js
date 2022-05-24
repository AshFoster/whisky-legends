// CREDIT - getStars function idea was found here:
// https://codereview.stackexchange.com/questions/177945/convert-rating-value-to-visible-stars-using-fontawesome-icons
/*
This function outputs stars to the nearest half based on a rating out of 10
*/
function getStars(rating) {

    // Round to nearest half
    rating = Math.round(rating * 2) / 2;
    let output = [];

    // Append all the filled whole stars
    for (var i = rating; i >= 1; i--) {
        output.push('<i class="fas fa-star" aria-hidden="true"></i>');
    }

    // If there is a half a star, append it
    if (i == 0.5) output.push('<i class="fas fa-star-half-alt" aria-hidden="true"></i>');

    // Fill the empty stars
    for (let i = (10 - rating); i >= 1; i--) {
        output.push('<i class="far fa-star" aria-hidden="true"></i>');
    }

    return output.join('');
}

// Set stars shown on product detail page by calling getStars
let rating = document.getElementById("ratingValue").textContent;
document.getElementById("stars").innerHTML = getStars(rating);

// Set stars shown on reviews by calling getStars
document.querySelectorAll('.review-stars').forEach(item => {
    let reviewRating = item.getAttribute('data-rating');
    item.innerHTML = getStars(reviewRating);
});

// CREDIT - The following functions here were inspired by Code Institute's walkthrough
// project 'Boutique Ado', and the method on how to use AJAX without jQuery
// was found here: https://stackoverflow.com/questions/64612746/how-would-i-do-this-ajax-jquery-in-vanilla-js

// Add to cart and reload on click
document.querySelector('.add-cart-btn').addEventListener('click', function () {
    let addCartForm = this.closest('.add-cart-form');
    let qtyInput = addCartForm.querySelector('.qty-input');

    if (parseInt(qtyInput.value) >= parseInt(qtyInput.min) && parseInt(qtyInput.value) <= parseInt(qtyInput.max)) {
        let formData = new FormData(addCartForm);
        let productId = qtyInput.getAttribute('id').split('id-qty-')[1];
        let url = `/cart/add/${productId}/`;
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
    } else {
        addCartForm.submit.click();
    }
});

// Add/Remove from wishlist and reload on click
let wishlistBtn = document.querySelector('.wishlist-btn');
if (wishlistBtn != null) {
    wishlistBtn.addEventListener('click', function () {
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
}

// Submit review and reload on click
let submitBtn = document.querySelector('#submit-button');
if (submitBtn != null) {
    submitBtn.addEventListener('click', function () {
        let reviewForm = document.querySelector('#review-form');
        let formData = new FormData(reviewForm);
        if (document.querySelector('#review-form-content').value != '' && document.querySelector('input[name="rating"]:checked') != null) {
            let productId = this.getAttribute('data-id').split('review-')[1];
            let url = `/shop/${productId}/`;
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
        } else {
            reviewForm.submit.click();
        }
    });
}

// Delete review and reload on click
document.querySelectorAll('.delete-review-modal a').forEach(item => {
    item.addEventListener('click', function () {
        let reviewId = this.closest('.delete-review-modal').getAttribute('id').split('deleteReviewModal')[1];
        let url = `/shop/delete_review/${reviewId}/`;
        let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        let params = 'csrfmiddlewaretoken=' + encodeURIComponent(csrfToken);
        let httpRequest = new XMLHttpRequest();
        httpRequest.open('POST', url);
        httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState == 4 && httpRequest.status == 200) {
                location.reload();
            }
        };
        httpRequest.send(params);
    });
});