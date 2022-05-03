let defaultCountry = document.getElementById('id_default_country');

if (defaultCountry != null) {
    countrySelected = defaultCountry.value;
    if(!countrySelected) {
        defaultCountry.style.color = '#7e868d';
    };
    defaultCountry.addEventListener('change', function () {
        countrySelected = this.value;
        if(!countrySelected) {
            defaultCountry.style.color = '#7e868d';
        } else {
            defaultCountry.style.color = '#212529';
        }
    });
}