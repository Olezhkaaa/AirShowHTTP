document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".vehicle-card").forEach(card => {
      card.addEventListener("click", function () {
          const link = this.querySelector("a");
          if (link) {
              window.location.href = link.href;
          }
      });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  let slideIndex = 1;
  let timer;
  let remainingTime = 5000; // Оставшееся время
  let startTime;
  let paused = false; // Флаг паузы
  const slideDuration = 5000; // 5 секунд
  const progressIndicator = document.querySelector(".progress-indicator");
  const slider = document.querySelector(".slider");
  const prevButton = document.querySelector(".prev");
  const nextButton = document.querySelector(".next");

  function showSlides(n) {
    let slides = document.getElementsByClassName("item");
    let dots = document.getElementsByClassName("slider-dots_item");

    if (n > slides.length) slideIndex = 1;
    if (n < 1) slideIndex = slides.length;

    for (let i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
    }
    for (let i = 0; i < dots.length; i++) {
      dots[i].classList.remove("active");
    }

    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].classList.add("active");

    resetProgressIndicator();
    startTimer();
  }

  function resetProgressIndicator() {
    progressIndicator.style.transition = "none";
    progressIndicator.style.width = "0%";

    setTimeout(() => {
      progressIndicator.style.transition = `width ${remainingTime / 1000}s linear`;
      progressIndicator.style.width = "100%";
    }, 50);
  }

  function startTimer() {
    clearTimeout(timer);
    startTime = Date.now();
    timer = setTimeout(() => {
      plusSlide();
    }, remainingTime);
  }

  function plusSlide() {
    remainingTime = slideDuration;
    showSlides(slideIndex += 1);
  }

  function minusSlide() {
    remainingTime = slideDuration;
    showSlides(slideIndex -= 1);
  }

  // При наведении — ПАУЗА, но НЕ СБРОС!
  slider.addEventListener("mouseenter", () => {
    if (!paused) {
      clearTimeout(timer);
      let elapsedTime = Date.now() - startTime;
      remainingTime -= elapsedTime; // Корректируем оставшееся время

      let currentWidth = getComputedStyle(progressIndicator).width;
      progressIndicator.style.transition = "none";
      progressIndicator.style.width = currentWidth;
      paused = true;
    }
  });

  // Когда убираем курсор — ПРОДОЛЖАЕМ с того же места
  slider.addEventListener("mouseleave", () => {
    if (paused) {
      startTime = Date.now();
      progressIndicator.style.transition = `width ${remainingTime / 1000}s linear`;
      progressIndicator.style.width = "100%";
      startTimer();
      paused = false;
    }
  });

  // Привязываем стрелки к переключению слайдов
  prevButton.addEventListener("click", minusSlide);
  nextButton.addEventListener("click", plusSlide);

  // Запускаем слайдер
  showSlides(slideIndex);
});




// Показывать кнопку, когда прокручиваем страницу вниз
window.onscroll = function () {
  var button = document.querySelector(".scroll-to-top");
  if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
    button.classList.add("show");  // Добавляем класс .show для показа кнопки
    button.classList.remove("hide");  // Убираем класс .hide, чтобы не скрывать кнопку
  } else {
    button.classList.add("hide");  // Добавляем класс .hide для скрытия кнопки
    button.classList.remove("show");  // Убираем класс .show
  }
};

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}


// Весь код для карты теперь внутри колбека ymaps.ready()
ymaps.ready(function () {
  var map = new ymaps.Map("map", {
      center: [55.256341, 61.300496], // Укажите нужные координаты
      zoom: 12,
      controls: ['zoomControl', 'typeSelector']
  });

  var placemark = new ymaps.Placemark([55.256341, 61.300496], {
      balloonContent: 'Место проведения мероприятия'
  });

  map.geoObjects.add(placemark);
});


const modal = document.getElementById('ticket-modal');
const openModalButton = document.getElementById('open-ticket-modal');
const closeButton = document.querySelector('.close');

// Открытие модального окна
openModalButton.addEventListener('click', function() {
  modal.style.display = 'flex';
});

// Закрытие модального окна
closeButton.addEventListener('click', function() {
  modal.style.display = 'none';
});

// Закрытие модального окна, если пользователь кликает вне окна
window.addEventListener('click', function(event) {
  if (event.target === modal) {
    modal.style.display = 'none';
  }
});


