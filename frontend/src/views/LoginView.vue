<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { apiLogin } from "../api"
import { setUser } from "../stores/user"

const router = useRouter()
const username = ref("")
const password = ref("")
const error = ref("")
const busy = ref(false)

async function submit() {
  error.value = ""
  if (!username.value.trim() || !password.value) {
    error.value = "请输入用户名和密码"
    return
  }
  busy.value = true
  try {
    const res = await apiLogin(username.value.trim(), password.value)
    if (!res || !res.user_id) {
      error.value = "用户名或密码错误"
      return
    }
    setUser(res)
    router.push("/")
  } catch (err) {
    error.value = err.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="login-wrap">
    <form class="login-card" @submit.prevent="submit">
      <div class="login-brand">
        <div class="mark mono">台</div>
        <h1>登录客诉服务台</h1>
        <p>登录后即可在对话中查询订单</p>
      </div>

      <p class="form-error" role="alert">{{ error }}</p>

      <div class="field">
        <label for="username">用户名</label>
        <input
          id="username"
          v-model="username"
          type="text"
          maxlength="10"
          autocomplete="username"
          placeholder="请输入用户名"
        />
      </div>

      <div class="field">
        <label for="password">密码</label>
        <input
          id="password"
          v-model="password"
          type="password"
          maxlength="12"
          autocomplete="current-password"
          placeholder="请输入密码"
        />
      </div>

      <button class="submit-btn" type="submit" :disabled="busy">
        {{ busy ? "登录中…" : "登录" }}
      </button>

      <p class="login-hint mono">凭据仅用于标识身份，不会保存密码</p>
    </form>
  </div>
</template>

<style scoped>
.login-wrap {
  min-height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: var(--paper);
  color: #2b2a26;
  border-radius: 18px;
  padding: 32px 30px;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.35);
}

.login-brand {
  text-align: center;
  margin-bottom: 20px;
}

.login-brand .mark {
  font-size: 30px;
  color: var(--amber);
  letter-spacing: 0.2em;
}

.login-brand h1 {
  font-size: 20px;
  margin: 10px 0 4px;
  letter-spacing: 0.04em;
}

.login-brand p {
  margin: 0;
  color: #8a8577;
  font-size: 13px;
}

.form-error {
  color: var(--coral);
  font-size: 13px;
  margin: 0 0 12px;
  min-height: 18px;
}

.field {
  margin-bottom: 14px;
}

.field label {
  display: block;
  font-size: 13px;
  color: #5a564a;
  margin-bottom: 6px;
}

.field input {
  width: 100%;
  padding: 11px 12px;
  border: 1px solid #d8d0bd;
  border-radius: 10px;
  font-size: 15px;
  background: #fffdf8;
  color: #2b2a26;
  outline: none;
  font-family: inherit;
}

.field input:focus {
  border-color: var(--amber);
  box-shadow: 0 0 0 3px rgba(229, 160, 60, 0.18);
}

.submit-btn {
  width: 100%;
  padding: 12px;
  border: 0;
  border-radius: 10px;
  background: var(--ink);
  color: var(--paper);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  letter-spacing: 0.06em;
  font-family: inherit;
  transition: background 0.15s;
}

.submit-btn:hover {
  background: var(--ink-raised);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.login-hint {
  text-align: center;
  font-size: 12px;
  color: #8a8577;
  margin: 16px 0 0;
}
</style>