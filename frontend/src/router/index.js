import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import MainView from '../views/MainView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    // ✅ Must match router.push({ name: 'Main', params: { projectId } }) in Home.vue
    path: '/main/:projectId',
    name: 'Main',
    component: MainView,
    props: true,   // passes :projectId as a prop automatically
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router