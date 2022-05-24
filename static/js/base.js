// Show Bootstrap toasts
document.querySelectorAll('.toast').forEach(item => {
    toast = new bootstrap.Toast(item);
    toast.show();
});

/* 
Adds event listeners to the 'bttButton' element so it only appears when
page is scrolled below the top, and returns the user to the top of the
page when clicked.
*/
function setBttButton() {
    let bttButton = document.querySelector('.btt-button');

    window.addEventListener("scroll", function () {
        let y = window.scrollY;
        if (y > 0) {
            bttButton.style.display = 'block';
        } else {
            bttButton.style.display = 'none';
        }
    });

    bttButton.addEventListener('click', function () {
        window.scrollTo(0, 0);
    });
}

// Call setBttButton() fucntion
setBttButton();