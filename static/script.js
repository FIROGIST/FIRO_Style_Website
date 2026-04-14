let currentSlide = 0;
function moveSlide(direction) {
    const slides = document.querySelector('.slides');
    const totalSlides = document.querySelectorAll('.slide').length;
    currentSlide = (currentSlide + direction + totalSlides) % totalSlides;
    slides.style.transform = `translateX(${currentSlide * 100}%)`;
}

const themeBtn = document.getElementById('dark-mode-toggle');
themeBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');
    const icon = themeBtn.querySelector('i');
    icon.classList.toggle('fa-moon');
    icon.classList.toggle('fa-sun');
});