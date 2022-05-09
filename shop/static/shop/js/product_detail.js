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