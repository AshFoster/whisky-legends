// CREDIT 
// Idea for this function came from:
// https://stackoverflow.com/questions/53384366/how-to-get-the-longest-height-of-the-div-from-pure-javascript
/* 
Finds maximum height of all divs with a particular class name and sets all of their heights to the maximum height
*/
function setMaxHeight(className) {
    let maxHeight = 0;

    document.querySelectorAll(className).forEach(function (e) {
        e.style.minHeight = null;
    });

    document.querySelectorAll(className).forEach(function (e) {
        if (e.clientHeight > maxHeight) {
            maxHeight = e.clientHeight;
        }
    });

    document.querySelectorAll(className).forEach(function (e) {
        e.style.minHeight = maxHeight + 'px';
    });
    console.log(maxHeight);
}
// END CREDIT

/* 
Once the DOM has finshed loading call setMaxHeight function on all elements with .product-card-title class
*/
document.addEventListener('DOMContentLoaded', function () {

    setMaxHeight('.product-card-title');

});

/* 
Call setMaxHeight function on all elements with .product-card-title class when the window is resized
*/
window.addEventListener('resize', function () {

    setMaxHeight('.product-card-title');

}, false);