<template>
  <div class="home">
    <main class="main-content">
      <section class="hero-split">
        <div class="split-container">
          <!-- Girls Section -->
          <router-link to="/categories/girls" class="split-section girls-section">
            <div class="split-image">
              <div class="image-placeholder girls-placeholder">
                <div class="placeholder-content">
                  <div class="placeholder-icon">👗</div>
                  <p>Коллекция для девочек</p>
                </div>
              </div>
              <div class="split-overlay"></div>
            </div>
            <div class="split-content">
              <h2 class="split-title">ДЕВОЧКИ</h2>
            </div>
          </router-link>
          
          <!-- Boys Section -->
          <router-link to="/categories/boys" class="split-section boys-section">
            <div class="split-image">
              <div class="image-placeholder boys-placeholder">
                <div class="placeholder-content">
                  <div class="placeholder-icon">👕</div>
                  <p>Коллекция для мальчиков</p>
                </div>
              </div>
              <div class="split-overlay"></div>
            </div>
            <div class="split-content">
              <h2 class="split-title">МАЛЬЧИКИ</h2>
            </div>
          </router-link>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
</script>

<style scoped>
.home {
  /* Remove any margins/padding that might cause white space */
  margin: 0;
  padding: 0;
}

.main-content {
  /* Reduce padding-top or remove it completely if header overlaps */
  padding-top: 0;
  margin: 0;
}

/* Hero Split Section */
.hero-split {
  height: 100vh; /* Use full viewport height */
  min-height: 600px;
  position: relative;
  overflow: hidden;
  margin: 0;
  padding: 0;
}

.split-container {
  display: flex;
  height: 100%;
  width: 100%;
}

.split-section {
  flex: 1;
  position: relative;
  overflow: hidden;
  transition: flex 0.3s ease;
  text-decoration: none;
  color: inherit;
  display: block;
  cursor: pointer;
}

.split-section:hover {
  flex: 1.1;
}

.split-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.split-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

/* Image Placeholders */
.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  transition: transform 0.5s ease;
}

.girls-placeholder {
  background: linear-gradient(
    135deg,
    #FFB6C1 0%,
    #FFC0CB 50%,
    #FFE4E1 100%
  );
}

.boys-placeholder {
  background: linear-gradient(
    135deg,
    #87CEEB 0%,
    #4682B4 50%,
    #B0C4DE 100%
  );
}

.placeholder-content {
  text-align: center;
  color: rgba(255, 255, 255, 0.9);
  z-index: 2;
}

.placeholder-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.placeholder-content p {
  font-size: 1.2rem;
  font-weight: 500;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  margin: 0;
}

.split-section:hover .split-image img,
.split-section:hover .image-placeholder {
  transform: scale(1.05);
}

.split-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    45deg, 
    rgba(0, 0, 0, 0.3) 0%, 
    rgba(0, 0, 0, 0.1) 100%
  );
}

.split-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  z-index: 10;
  text-align: center;
  width: 100%;
}

.split-title {
  font-size: 4rem;
  font-weight: 700;
  text-transform: uppercase;
  margin: 0;
  letter-spacing: 3px;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
}

/* Remove split button styles as they're no longer needed */

/* Girls Section Styling */
.girls-section .split-overlay {
  background: linear-gradient(
    135deg, 
    rgba(255, 182, 193, 0.3) 0%, 
    rgba(255, 105, 180, 0.2) 100%
  );
}

/* Boys Section Styling */
.boys-section .split-overlay {
  background: linear-gradient(
    135deg, 
    rgba(70, 130, 180, 0.3) 0%, 
    rgba(25, 25, 112, 0.2) 100%
  );
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-split {
    height: 100vh; /* Keep full height on mobile */
  }
  
  .split-container {
    flex-direction: row; /* Keep horizontal layout on mobile */
  }
  
  .split-section {
    min-height: 100vh; /* Full height for each section */
  }
  
  .split-title {
    font-size: 2rem;
    letter-spacing: 1px;
  }
  
  .placeholder-icon {
    font-size: 2.5rem;
  }
  
  .placeholder-content p {
    font-size: 0.9rem;
  }
}

@media (min-width: 1024px) {
  .split-title {
    font-size: 5rem;
  }
}

@media (min-width: 1200px) {
  .split-title {
    font-size: 6rem;
  }
}

/* Sections */
.section {
  margin: 4rem 0;
  padding: 2rem 0;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1rem;
}
</style>