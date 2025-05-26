<template>
  <div class="home">
    <main class="main-content">
      <section class="hero-split">
        <div class="split-container">
          <!-- Girls Section -->
          <div class="split-section girls-section">
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
              <router-link to="/categories/girls" class="split-button">
                СМОТРЕТЬ КОЛЛЕКЦИЮ
              </router-link>
            </div>
          </div>
          
          <!-- Boys Section -->
          <div class="split-section boys-section">
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
              <router-link to="/categories/boys" class="split-button">
                СМОТРЕТЬ КОЛЛЕКЦИЮ
              </router-link>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
// import ProductCard from '@/components/ProductCart.vue';
</script>

<style scoped>
.main-content {
  padding-top: 120px;
}

/* Hero Split Section */
.hero-split {
  height: 80vh;
  min-height: 600px;
  position: relative;
  overflow: hidden;
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
}

/* Category Placeholders */
.category-placeholder {
  height: 200px;
}

.dresses-placeholder {
  background: linear-gradient(135deg, #FFB6C1, #FF69B4);
}

.shirts-placeholder {
  background: linear-gradient(135deg, #87CEEB, #4682B4);
}

.accessories-placeholder {
  background: linear-gradient(135deg, #DDA0DD, #9370DB);
}

.shoes-placeholder {
  background: linear-gradient(135deg, #F0E68C, #DAA520);
}

.category-placeholder .placeholder-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.category-placeholder .placeholder-content p {
  font-size: 0.9rem;
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
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 3rem 2rem;
  color: white;
  z-index: 10;
  text-align: center;
}

.split-title {
  font-size: 3rem;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 2rem;
  letter-spacing: 2px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.split-button {
  display: inline-block;
  background-color: #000;
  color: #fff;
  padding: 1rem 2rem;
  text-decoration: none;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1px;
  border-radius: 4px;
  transition: all 0.3s ease;
  border: 2px solid #000;
}

.split-button:hover {
  background-color: transparent;
  color: #fff;
  border-color: #fff;
  transform: translateY(-2px);
}

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
  .split-container {
    flex-direction: column;
  }
  
  .split-section {
    min-height: 50vh;
  }
  
  .split-title {
    font-size: 2rem;
  }
  
  .split-content {
    padding: 2rem 1rem;
  }
  
  .section {
    margin: 2rem 0;
  }
  
  .section-title {
    font-size: 1.5rem;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .product-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 1rem;
  }
  
  .categories-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 0 2rem;
  }
  
  .product-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .split-title {
    font-size: 4rem;
  }
}

@media (min-width: 1200px) {
  .split-title {
    font-size: 5rem;
  }
}
</style>