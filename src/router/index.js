import { createRouter, createWebHistory } from 'vue-router'
import MenuView from '../views/menu.vue'
import CatalogueView from '../views/catalogue.vue'
import VolumeView from '../views/volume.vue'
import ReaderView from "../views/reader.vue"
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: MenuView,
      meta: { Transition: 'slide-right' },
    },
    {
      path: '/catalogue',
      name: 'catalogue',
      component: CatalogueView,
      meta: { Transition: 'slide-left' }
    },
    {
      path: '/volume/:vol_num',
      name: 'volume',
      component: VolumeView,
      meta: { Transition: 'slide-left' }
    },
    {
      path: '/volume/:vol_num/chap/:chap_num',
      name: 'reader',
      component : ReaderView,
      meta: { Transition: 'slide-left' }

    },
    { 
      path: "/:notFound", 
      component: MenuView 
    }
  ]
})

export default router
