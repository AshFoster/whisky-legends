// Global Variables
const params = new URLSearchParams(window.location.search);
let searchHiddenInput = document.querySelector('#search-shop');
let searchInput = document.querySelector('.search-bar');

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
}
// END CREDIT

function setTypeFilter() {
    let typeFilterURL = params.get('type');
    let typeListItems = document.querySelectorAll('.type-item');
    let typeClear = document.getElementById('typeClear');

    if (typeFilterURL != null) {
        document.getElementById('typeDropdown').classList.add('active-filter');
    }

    for (let item of typeListItems) {
        item.addEventListener('click', function () {
            if (typeFilterURL != null) {
                window.location.search = window.location.search.replace(typeFilterURL, item.querySelector('.type-name').value);
            } else {
                window.location.search += '&type=' + item.querySelector('.type-name').value;
            }
            document.getElementById('typeDropdown').classList.add('active-filter');
        });
    }

    if (typeClear != null) {
        typeClear.addEventListener('click', function () {
            window.location.search = window.location.search.replace('&type=' + typeFilterURL, '');
        });
    }
}

function setBrandFilter() {
    let brandFilterURL = params.get('brand');
    let brandListItems = document.querySelectorAll('.brand-item');
    let brandClear = document.getElementById('brandClear');

    if (brandFilterURL != null) {
        document.getElementById('brandDropdown').classList.add('active-filter');
    }

    for (let item of brandListItems) {
        item.addEventListener('click', function () {
            if (brandFilterURL != null) {
                window.location.search = window.location.search.replace(brandFilterURL, item.querySelector('.brand-name').value);
            } else {
                window.location.search += '&brand=' + item.querySelector('.brand-name').value;
            }
        });
    }

    if (brandClear != null) {
        brandClear.addEventListener('click', function () {
            window.location.search = window.location.search.replace('&brand=' + brandFilterURL, '');
        });
    }
}

function setCountryFilter() {
    let countryFilterURL = params.get('country');
    let countryListItems = document.querySelectorAll('.country-item');
    let countryClear = document.getElementById('countryClear');

    if (countryFilterURL != null) {
        document.getElementById('countryDropdown').classList.add('active-filter');
    }

    for (let item of countryListItems) {
        item.addEventListener('click', function () {
            if (countryFilterURL != null) {
                window.location.search = window.location.search.replace(countryFilterURL, item.querySelector('.country-name').value);
            } else {
                window.location.search += '&country=' + item.querySelector('.country-name').value;
            }
        });
    }

    if (countryClear != null) {
        countryClear.addEventListener('click', function () {
            window.location.search = window.location.search.replace('&country=' + countryFilterURL, '');
        });
    }
}

function setRegionFilter() {
    let regionFilterURL = params.get('region');
    let regionListItems = document.querySelectorAll('.region-item');
    let regionClear = document.getElementById('regionClear');

    if (regionFilterURL != null) {
        document.getElementById('regionDropdown').classList.add('active-filter');
    }

    for (let item of regionListItems) {
        item.addEventListener('click', function () {
            if (regionFilterURL != null) {
                window.location.search = window.location.search.replace(regionFilterURL, item.querySelector('.region-name').value);
            } else {
                window.location.search += '&region=' + item.querySelector('.region-name').value;
            }
        });
    }

    if (regionClear != null) {
        regionClear.addEventListener('click', function () {
            window.location.search = window.location.search.replace('&region=' + regionFilterURL, '');
        });
    }
}

function setFlavourFilter() {
    let flavourFilterURL = params.get('flavour');
    let flavourListItems = document.querySelectorAll('.flavour-item');
    let flavourClear = document.getElementById('flavourClear');

    if (flavourFilterURL != null) {
        document.getElementById('flavourDropdown').classList.add('active-filter');
    }

    for (let item of flavourListItems) {
        item.addEventListener('click', function () {
            if (flavourFilterURL != null) {
                window.location.search = window.location.search.replace(flavourFilterURL, item.querySelector('.flavour-name').value);
            } else {
                window.location.search += '&flavour=' + item.querySelector('.flavour-name').value;
            }
        });
    }

    if (flavourClear != null) {
        flavourClear.addEventListener('click', function () {
            window.location.search = window.location.search.replace('&flavour=' + flavourFilterURL, '');
        });
    }
}


/* 
Once the DOM has finshed loading call setMaxHeight function on all elements with .product-card-title class
*/
document.addEventListener('DOMContentLoaded', function () {

    setMaxHeight('.product-card-title');

    setTypeFilter();

    setBrandFilter();

    setCountryFilter();

    setRegionFilter();

    setFlavourFilter();

});

/* 
Call setMaxHeight function on all elements with .product-card-title class when the window is resized
*/
window.addEventListener('resize', function () {

    setMaxHeight('.product-card-title');

}, false);