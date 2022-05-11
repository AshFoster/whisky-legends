// CREDIT - getStars function idea was found here:
// https://codereview.stackexchange.com/questions/177945/convert-rating-value-to-visible-stars-using-fontawesome-icons
// This function outputs stars to the nearest half based on a rating out of 10
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
// END CREDIT

let rating = document.getElementById("ratingValue").textContent
document.getElementById("stars").innerHTML = getStars(rating);

document.querySelectorAll('.review-stars').forEach(item => {
    reviewRating = item.getAttribute('data-rating')
    item.innerHTML = getStars(reviewRating);
});

// Add to cart and reload on click
// CREDIT - https://stackoverflow.com/questions/64612746/how-would-i-do-this-ajax-jquery-in-vanilla-js
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
// CREDIT - https://stackoverflow.com/questions/64612746/how-would-i-do-this-ajax-jquery-in-vanilla-js
document.querySelector('.wishlist-btn').addEventListener('click', function () {
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