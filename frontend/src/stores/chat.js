import { reactive, watch } from "vue"

const KEY = "ai_cs_chat"

function load() {
  try {
    const raw = localStorage.getItem(KEY)
    if (raw) return JSON.parse(raw)
  } catch {
    /* ignore */
  }
  return []
}

export const chatStore = reactive({ messages: load() })

watch(
  () => chatStore.messages,
  (val) => {
    localStorage.setItem(KEY, JSON.stringify(val))
  },
  { deep: true }
)

export function resetChat() {
  chatStore.messages = []
}