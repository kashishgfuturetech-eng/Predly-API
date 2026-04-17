import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import PromptView from '../views/PromptView.vue'
import MainView from '../views/MainView.vue'
import LoginView from '../views/LoginView.vue'
import { isAuthenticated, setRedirectAfterLogin } from '../auth.js'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/prompt',
    name: 'Prompt',
    component: PromptView,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/main/:projectId',
    name: 'Main',
    component: MainView,
    props: true,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, _from, next) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    setRedirectAfterLogin(to.fullPath)
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router
