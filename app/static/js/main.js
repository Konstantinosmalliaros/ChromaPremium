document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".site-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const expanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!expanded));
      nav.classList.toggle("open");
    });
  }

  // Lightbox functionality
  const lightbox = document.getElementById("lightbox");
  const lightboxImage = document.querySelector(".lightbox-image");
  const galleryItems = document.querySelectorAll(".gallery-item");
  const closeBtn = document.querySelector(".lightbox-close");
  const prevBtn = document.querySelector(".lightbox-prev");
  const nextBtn = document.querySelector(".lightbox-next");
  
  let currentIndex = 0;
  const photos = Array.from(galleryItems).map(item => {
    const img = item.querySelector("img");
    return img ? img.src : null;
  }).filter(Boolean);

  if (lightbox && galleryItems.length > 0 && lightboxImage) {
    // Navigation functions
    const openLightbox = () => {
      if (photos[currentIndex]) {
        lightboxImage.src = photos[currentIndex];
        lightbox.classList.add("active");
        document.body.style.overflow = "hidden";
      }
    };

    const closeLightbox = () => {
      lightbox.classList.remove("active");
      document.body.style.overflow = "";
    };

    const showPrev = () => {
      currentIndex = (currentIndex - 1 + photos.length) % photos.length;
      openLightbox();
    };

    const showNext = () => {
      currentIndex = (currentIndex + 1) % photos.length;
      openLightbox();
    };

    // Open lightbox on image click
    galleryItems.forEach((item, index) => {
      item.addEventListener("click", () => {
        currentIndex = index;
        openLightbox();
      });
    });

    // Close lightbox
    if (closeBtn) {
      closeBtn.addEventListener("click", closeLightbox);
    }

    // Close on background click
    lightbox.addEventListener("click", (e) => {
      if (e.target === lightbox) {
        closeLightbox();
      }
    });

    // Navigation buttons
    if (prevBtn) {
      prevBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        showPrev();
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        showNext();
      });
    }

    // Keyboard navigation
    document.addEventListener("keydown", (e) => {
      if (!lightbox.classList.contains("active")) return;

      if (e.key === "Escape") {
        closeLightbox();
      } else if (e.key === "ArrowLeft") {
        showPrev();
      } else if (e.key === "ArrowRight") {
        showNext();
      }
    });
  }
});

