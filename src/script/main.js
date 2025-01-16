import Alpine from "alpinejs";
import htmx from "htmx.org";
import zxcvbn from "zxcvbn";
window.zxcvbn = zxcvbn;
Alpine.start();
document.addEventListener("DOMContentLoaded", () => {
  const carousel = document.getElementById("carousel");
  const dots = document.querySelectorAll(".dot");
  let currentIndex = 0;
  const imageCount = dots.length;

  function updateCarousel() {
    const offset = -currentIndex * 100;
    carousel.style.transform = `translateX(${offset}%)`;

    // 更新導航點狀態
    dots.forEach((dot, index) => {
      dot.classList.toggle("bg-white", index === currentIndex);
      dot.classList.toggle("bg-gray-400", index !== currentIndex);
    });
  }

  // 自動輪播
  function autoSlide() {
    currentIndex = (currentIndex + 1) % imageCount;
    updateCarousel();
  }

  // 點擊導航點切換圖片
  dots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
      currentIndex = index;
      updateCarousel();
    });
  });

  // 設置自動輪播間隔
  let timerId = setTimeout(function tick() {
    autoSlide();
    timerId = setTimeout(tick, 3000);
  }, 3000);
});
