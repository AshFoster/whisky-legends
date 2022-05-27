// CREDIT - The method on how to use AJAX without jQuery was found here:
// https://stackoverflow.com/questions/64612746/how-would-i-do-this-ajax-jquery-in-vanilla-js

// Update quantity of item in cart and reload on click
document.querySelectorAll('.update-btn').forEach(item => {
    item.addEventListener('click', function () {
        let updateForm = this.closest('.update-form');
        let qtyInput = updateForm.querySelector('.qty-input');

        if (parseInt(qtyInput.value) >= parseInt(qtyInput.min) && parseInt(qtyInput.value) <= parseInt(qtyInput.max)) {
            let formData = new FormData(updateForm);
            let productId = qtyInput.getAttribute('id').split('id-qty-')[1];
            let url = `/cart/update/${productId}/`;
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
            updateForm.submit.click();
        }
    });
});

// Remove item from cart and reload on click
document.querySelectorAll('.remove-btn').forEach(item => {
    item.addEventListener('click', function () {
        let productId = this.getAttribute('id').split('remove-')[1];
        let url = `/cart/remove/${productId}/`;
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

// Add/Remove from wishlist and reload on click
let wishlistBtns = document.querySelectorAll('.wishlist-btn');
if (wishlistBtns != null) {
    wishlistBtns.forEach(item => {
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
}