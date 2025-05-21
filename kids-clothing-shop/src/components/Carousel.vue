<template>
  <div class="carousel-container">
    <div 
      class="carousel" 
      :style="{ transform: `translateX(-${activeIndex * 100}%)` }"
    >
      <div 
        v-for="slide in slides" 
        :key="slide.id" 
        class="carousel-slide"
      >
        <img :src="slide.image" :alt="slide.alt" class="carousel-image">
        <div class="carousel-content" v-if="slide.title || slide.subtitle || slide.buttonText">
          <h2 v-if="slide.title" class="carousel-title">{{ slide.title }}</h2>
          <p v-if="slide.subtitle" class="carousel-subtitle">{{ slide.subtitle }}</p>
          <router-link 
            v-if="slide.buttonText && slide.buttonLink" 
            :to="slide.buttonLink" 
            class="carousel-button"
          >
            {{ slide.buttonText }}
          </router-link>
        </div>
      </div>
    </div>
    
    <div class="carousel-controls" v-if="slides.length > 1">
      <button 
        class="carousel-arrow prev"
        aria-label="Previous slide"
        @click="prevSlide"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </button>
      
      <div class="carousel-dots">
        <button 
          v-for="(slide, index) in slides" 
          :key="slide.id"
          class="carousel-dot"
          :class="{ active: index === activeIndex }"
          @click="goToSlide(index)"
          :aria-label="`Go to slide ${index + 1}`"
        ></button>
      </div>
      
      <button 
        class="carousel-arrow next"
        aria-label="Next slide"
        @click="nextSlide"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps({
  slides: {
    type: Array,
    required: true,
    default: () => []
  },
  autoplay: {
    type: Boolean,
    default: true
  },
  interval: {
    type: Number,
    default: 5000
  }
});

const activeIndex = ref(0);
let autoplayInterval = null;

const nextSlide = () => {
  activeIndex.value = (activeIndex.value + 1) % props.slides.length;
};

const prevSlide = () => {
  activeIndex.value = (activeIndex.value - 1 + props.slides.length) % props.slides.length;
};

const goToSlide = (index) => {
  activeIndex.value = index;
};

const startAutoplay = () => {
  if (props.autoplay && props.slides.length > 1) {
    autoplayInterval = setInterval(() => {
      nextSlide();
    }, props.interval);
  }
};

const stopAutoplay = () => {
  if (autoplayInterval) {
    clearInterval(autoplayInterval);
  }
};

// Мобильная адаптация поворотов карусели
let touchStartX = 0;
let touchEndX = 0;

const handleTouchStart = (e) => {
  touchStartX = e.changedTouches[0].screenX;
};

const handleTouchEnd = (e) => {
  touchEndX = e.changedTouches[0].screenX;
  handleSwipe();
};

// функционал влево и вправо
const handleSwipe = () => {
  const swipeThreshold = 50;
  if (touchEndX < touchStartX - swipeThreshold) {
    nextSlide();
  } else if (touchEndX > touchStartX + swipeThreshold) {
    prevSlide();
  }
};

onMounted(() => {
  startAutoplay();
  
  // Add touch event listeners
  const carouselElement = document.querySelector('.carousel-container');
  if (carouselElement) {
    carouselElement.addEventListener('touchstart', handleTouchStart, { passive: true });
    carouselElement.addEventListener('touchend', handleTouchEnd, { passive: true });
  }
});

onUnmounted(() => {
  stopAutoplay();
  
  // Remove touch event listeners
  const carouselElement = document.querySelector('.carousel-container');
  if (carouselElement) {
    carouselElement.removeEventListener('touchstart', handleTouchStart);
    carouselElement.removeEventListener('touchend', handleTouchEnd);
  }
});

watch(() => props.slides, () => {
  // Ресет карусели, когда слайды кончаются
  activeIndex.value = 0;
  stopAutoplay();
  startAutoplay();
}, { deep: true });
</script>

<style scoped>
.carousel-container {
  position: relative;
  width: 100%;
  overflow: hidden;
}

.carousel {
  display: flex;
  transition: transform 0.5s ease;
}

.carousel-slide {
  flex: 0 0 100%;
  position: relative;
}

.carousel-image {
  width: 100%;
  height: auto;
  display: block;
}

.carousel-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #fff;
  width: 80%;
}

.carousel-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-transform: uppercase;
}

.carousel-subtitle {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
}

.carousel-button {
  display: inline-block;
  background-color: #000;
  color: #fff;
  padding: 0.75rem 1.5rem;
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.carousel-button:hover {
  background-color: #333;
}

.carousel-controls {
  position: absolute;
  bottom: 20px;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.carousel-arrow {
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.carousel-arrow:hover {
  background: rgba(0, 0, 0, 0.8);
}

.carousel-dots {
  display: flex;
  gap: 8px;
}

.carousel-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  border: none;
  padding: 0;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.carousel-dot.active {
  background: #fff;
}

/* Responsive adjustments */
@media (min-width: 768px) {
  .carousel-title {
    font-size: 3rem;
  }
  
  .carousel-subtitle {
    font-size: 1.5rem;
  }
}
</style>