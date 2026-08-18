import { createRouter, createWebHistory } from "vue-router"

const routes = [
  { path: "/", name: "chat", component: () => import("../views/ChatView.vue") },
  { path: "/login", name: "login", component: () => import("../views/LoginView.vue") },
  { path: "/knowledge", name: "knowledge", component: () => import("../views/KnowledgeView.vue") },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})