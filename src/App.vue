<script setup>
import { RouterView} from 'vue-router'
import navbar from './components/nav.vue'
</script>

<template>
  <header>
    <navbar/>
  </header>

  <RouterView v-slot="{Component, route}">
    <transition :name="route.meta.Transition" mode="out-in">
      <component class="component" :is="Component" />
    </transition>
  </RouterView>
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.slide-left-enter-active,
.slide-right-leave-active {
  transition: transform 0.5s;
}

.slide-left-enter,
.slide-right-leave-to {
  transform: translateX(100%); /* Sortie vers la droite */
}

.slide-left-leave-active,
.slide-right-enter-active {
  transition: transform 0.5s;
}

.slide-left-leave-to,
.slide-right-enter {
  transform: translateX(-100%); /* Sortie vers la gauche */
}

.component{
  
  padding: 20px;
  
}



</style>
