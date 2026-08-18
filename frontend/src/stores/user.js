import { reactive, watch } from "vue"

const KEY = "ai_cs_user"

function load() {
  try {
    const raw = localStorage.getItem(KEY)
    if (raw) return JSON.parse(raw)
  } catch {
    /* ignore */
  }
  return { user_id: null, user_name: "" }
}

export const userStore = reactive(load())

watch(
  userStore,
  (val) => {
    localStorage.setItem(KEY, JSON.stringify(val))
  },
  { deep: true }
)

export function setUser(user) {
  userStore.user_id = user.user_id
  userStore.user_name = user.user_name
}

export function clearUser() {
  userStore.user_id = null
  userStore.user_name = ""
}