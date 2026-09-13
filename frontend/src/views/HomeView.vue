<template>
  <main class="home-page">
    <h1>RPI GPIO Simple Controller</h1>
  </main>
</template>

<style scoped>
.home-page {
  width: min(100%, 720px);
  margin: 0 auto;
  padding: 24px 16px 48px;
}

h1 {
  margin: 0;
  color: var(--text-primary);
  font-size: 20px;
  font-weight: 600;
  line-height: 1.3;
}

@media (min-width: 1024px) {
  .home-page {
    padding: 32px;
  }

  h1 {
    font-size: 24px;
  }
}
</style>
