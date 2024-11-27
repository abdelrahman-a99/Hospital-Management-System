// when the user scroll down, the header will be change the bg color
window.addEventListener('scroll', function () {
    const header = document.querySelector('header');
    if (window.scrollY > 0) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});


// Copyright Date
let time = document.querySelector(".time")
time.innerHTML = new Date().getFullYear() // 2024