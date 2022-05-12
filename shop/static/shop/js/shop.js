// Global Variables
const params = new URLSearchParams(window.location.search);

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
        if (document.documentElement.clientWidth >= 576) {
            if (e.clientHeight > maxHeight) {
                maxHeight = e.clientHeight;
            }
        }
    });

    document.querySelectorAll(className).forEach(function (e) {
        if (document.documentElement.clientWidth >= 576) {
            e.style.minHeight = maxHeight + 'px';
        }
    });
}
// END CREDIT

function setSort() {
    let sortURL = params.get('sort');
    let directionURL = params.get('direction');
    let sortListItems = document.querySelectorAll('.sort-item');
    let sortClear = document.getElementById('sortClear');

    if (sortURL != null) {
        document.getElementById('sortDropdown').classList.add('active-filter');
    }

    for (let item of sortListItems) {
        item.addEventListener('click', function () {
            let sort = item.querySelector('.sort-name').value.split('_')[0]
            let direction = item.querySelector('.sort-name').value.split('_')[1]
            let currentURL = window.location.search
            if (sortURL != null) {
                currentURL = currentURL.replace(sortURL, sort);
                currentURL = currentURL.replace(directionURL, direction);
                window.location.search = currentURL
            } else {
                currentURL += '&sort=' + sort;
                currentURL += '&direction=' + direction;
                window.location.search = currentURL
            }
        });
    }

    if (sortClear != null) {
        sortClear.addEventListener('click', function () {
            let currentURL = window.location.search
            currentURL = currentURL.replace('&sort=' + sortURL, '');
            currentURL = currentURL.replace('&direction=' + directionURL, '');
            window.location.search = currentURL
        });
    }
}

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

function setPriceFilter() {
    let priceFilterURL = params.get('price');
    let minPrice = document.querySelector('.min-price');
    let maxPrice = document.querySelector('.max-price');
    let minPriceOriginal = minPrice.value;
    let maxPriceOriginal = maxPrice.value;
    let minPriceValue = 0;
    let maxPriceValue = 0;
    let priceApply = document.getElementById('priceApply');
    let priceClear = document.getElementById('priceClear');

    if (priceFilterURL != null) {
        document.getElementById('priceDropdown').classList.add('active-filter');
        minPrice.value = priceFilterURL.split(',')[0]
        maxPrice.value = priceFilterURL.split(',')[1]
        minPrice.max = Number(maxPrice.value) - 1
        maxPrice.min = Number(minPrice.value) + 1
    }

    priceApply.addEventListener('click', function () {
        if (Number(minPrice.value) >= Number(minPrice.min) && Number(minPrice.value) <= Number(minPrice.max)) {
            minPriceValue = Math.round(minPrice.value)
        } else if (Number(minPrice.value) <= Number(minPrice.max)) {
            minPriceValue = Math.round(minPrice.min)
        } else {
            minPriceValue = Math.round(minPrice.max)
        }

        if (Number(maxPrice.value) <= Number(maxPrice.max) && Number(maxPrice.value) >= Number(maxPrice.min)) {
            maxPriceValue = Math.round(maxPrice.value)
        } else if (Number(maxPrice.value) >= Number(maxPrice.min)) {
            maxPriceValue = Math.round(maxPrice.max)
        } else {
            maxPriceValue = Math.round(maxPrice.min)
        }

        if (minPriceValue >= maxPriceValue) {
            minPriceValue = minPriceOriginal;
            maxPriceValue = maxPriceOriginal;
        }

        if (priceFilterURL != null) {
            window.location.search = window.location.search.replace(priceFilterURL, minPriceValue + ',' + maxPriceValue);
        } else {
            window.location.search += '&price=' + minPriceValue + ',' + maxPriceValue;
        }
    });

    if (priceClear != null) {
        priceClear.addEventListener('click', function () {
            window.location.search = window.location.search.replace('&price=' + priceFilterURL, '');
        });
    }
}

function setAgeFilter() {
    let ageFilterURL = params.get('age');
    let ageListItems = document.querySelectorAll('.age-item');
    let ageClear = document.getElementById('ageClear');

    if (ageFilterURL != null) {
        document.getElementById('ageDropdown').classList.add('active-filter');
    }

    for (let item of ageListItems) {
        item.addEventListener('click', function () {
            if (ageFilterURL != null) {
                window.location.search = window.location.search.replace(ageFilterURL, item.querySelector('.age-name').textContent);
            } else {
                window.location.search += '&age=' + item.querySelector('.age-name').textContent;
            }
        });
    }

    if (ageClear != null) {
        ageClear.addEventListener('click', function () {
            window.location.search = window.location.search.replace('&age=' + ageFilterURL, '');
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

function setBttButton() {
    let bttButton = document.querySelector('.btt-button')

    window.addEventListener("scroll", function () {
        let y = window.scrollY;
        if (y > 0) {
            bttButton.style.display = 'block'
        } else {
            bttButton.style.display = 'none'
        }
    });

    bttButton.addEventListener('click', function () {
        window.scrollTo(0, 0);
    });
}

// Add to cart and reload on click
// CREDIT - https://stackoverflow.com/questions/64612746/how-would-i-do-this-ajax-jquery-in-vanilla-js
document.querySelectorAll('.add-cart-btn').forEach(item => {
    item.addEventListener('click', function () {
        let addCartForm = this.closest('.add-cart-form');
        let qtyInput = addCartForm.querySelector('.qty-input');
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
    });
})

// Delete product and reload on click
// CREDIT - https://stackoverflow.com/questions/64612746/how-would-i-do-this-ajax-jquery-in-vanilla-js
document.querySelectorAll('.delete-product-modal a').forEach(item => {
    item.addEventListener('click', function () {
        let productId = this.closest('.delete-product-modal').getAttribute('id').split('deleteProductModal')[1];
        let url = `/shop/delete_product/${productId}/`;
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


/* 
Once the DOM has finshed loading call all necessary functions
*/
document.addEventListener('DOMContentLoaded', function () {

    setMaxHeight('.product-card-title');

    setSort()

    setTypeFilter();

    setBrandFilter();

    setCountryFilter();

    setRegionFilter();

    setPriceFilter();

    setAgeFilter();

    setFlavourFilter();

    setBttButton()

});

/* 
Call setMaxHeight function on all elements with .product-card-title class when the window is resized
*/
window.addEventListener('resize', function () {

    setMaxHeight('.product-card-title');

}, false);