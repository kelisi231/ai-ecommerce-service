<script setup>
import { userStore, clearUser } from "./stores/user"
import { useRouter } from "vue-router"

const router = useRouter()

function logout() {
  clearUser()
  router.push("/login")
}
</script>

<template>
  <div class="shell">
    <header class="desk-bar">
      <div class="brand">
        <span class="brand-dot" aria-hidden="true"></span>
        <span class="brand-name">客诉服务台</span>
        <span class="brand-duty">值班中</span>
      </div>
      <nav class="nav">
        <RouterLink to="/" class="nav-link">对话</RouterLink>
        <RouterLink to="/knowledge" class="nav-link">知识库</RouterLink>
      </nav>
      <div class="user-area">
        <template v-if="userStore.user_id">
          <span class="user-chip mono">{{ userStore.user_name }}</span>
          <button class="ghost-btn" @click="logout">退出</button>
        </template>
        <RouterLink v-else to="/login" class="ghost-btn">登录</RouterLink>
      </div>
    </header>

    <main class="shell-main">
      <RouterView />
    </main>

    <footer class="desk-foot mono">
      <span>服务台号 · AI-CS-001</span>
      <span>上下文保存在当前浏览器 · 会话保留 3 分钟</span>
    </footer>
  </div>
</template>

<style scoped>
.shell {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.desk-bar {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 0 20px;
  height: 56px;
  background: var(--ink);
  border-bottom: 1px solid var(--line);
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.brand-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--mint);
  box-shadow: 0 0 0 0 rgba(127, 196, 164, 0.5);
  animation: pulse 2.4s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(127, 196, 164, 0.5);
  }
  70% {
    box-shadow: 0 0 0 8px rgba(127, 196, 164, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(127, 196, 164, 0);
  }
}

.brand-name {
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--paper);
}

.brand-duty {
  font-size: 12px;
  color: var(--mint);
  border: 1px solid rgba(127, 196, 164, 0.35);
  padding: 2px 8px;
  border-radius: 999px;
}

.nav {
  display: flex;
  gap: 4px;
  margin-left: 8px;
}

.nav-link {
  padding: 6px 14px;
  border-radius: 999px;
  color: var(--muted);
  text-decoration: none;
  font-size: 14px;
  transition: color 0.15s, background 0.15s;
}

.nav-link:hover {
  color: var(--text-on-dark);
}

.nav-link.router-link-exact-active {
  color: var(--paper);
  background: var(--ink-raised);
}

.user-area {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-chip {
  color: var(--amber);
  font-size: 13px;
  letter-spacing: 0.04em;
}

.ghost-btn {
  background: transparent;
  border: 1px solid var(--line);
  color: var(--text-on-dark);
  padding: 5px 12px;
  border-radius: 999px;
  font-size: 13px;
  cursor: pointer;
  text-decoration: none;
  font-family: inherit;
}

.ghost-btn:hover {
  border-color: var(--amber);
  color: var(--amber);
}

.shell-main {
  flex: 1;
  min-height: 0;
}

.desk-foot {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding: 8px 20px;
  font-size: 11px;
  color: var(--muted);
  border-top: 1px solid var(--line);
  background: var(--ink);
  letter-spacing: 0.04em;
}

@media (max-width: 640px) {
  .brand-name {
    display: none;
  }
  .desk-foot span:last-child {
    display: none;
  }
}
</style>