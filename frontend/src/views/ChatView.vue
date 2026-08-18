<script setup>
import { ref, nextTick, onMounted } from "vue"
import { apiChat } from "../api"
import { userStore } from "../stores/user"
import { chatStore } from "../stores/chat"
import MessageBubble from "../components/MessageBubble.vue"

const listRef = ref(null)
const messages = chatStore.messages
const input = ref("")
const busy = ref(false)

const suggestions = [
  "你们支持七天无理由退换货吗",
  "帮我查一下我的订单",
  "发货后一般多久能到",
]

function sessionKey() {
  const key = "ai_cs_session_id"
  let id = localStorage.getItem(key)
  if (!id) {
    id = crypto.randomUUID()
    localStorage.setItem(key, id)
  }
  return id
}

const sid = sessionKey()

function scroll() {
  nextTick(() => {
    const box = listRef.value
    if (box) box.scrollTop = box.scrollHeight
  })
}

async function send(text) {
  const question = (text ?? input.value).trim()
  if (!question || busy.value) return

  messages.push({ role: "user", content: question })
  input.value = ""
  messages.push({ role: "assistant", content: "", thinking: true })
  busy.value = true
  scroll()

  try {
    const res = await apiChat({
      session_id: sid,
      question,
      user_id: userStore.user_id ?? null,
    })
    const last = messages[messages.length - 1]
    last.thinking = false
    last.content = res.answer
    last.agent = res.agent
    last.sources = res.sources ?? []
  } catch (err) {
    const last = messages[messages.length - 1]
    last.thinking = false
    last.content = `服务台暂时无法接通：${err.message}`
    last.error = true
  } finally {
    busy.value = false
    scroll()
  }
}

function onKeydown(e) {
  if (e.key === "Enter" && !e.shiftKey && !e.isComposing) {
    e.preventDefault()
    send()
  }
}

onMounted(() => {
  const last = messages[messages.length - 1]
  if (last && last.thinking) {
    last.thinking = false
    last.error = true
    last.content = "上一条回复因页面切换未完成，请重新发送。"
  }
  if (!messages.length) {
    messages.push({
      role: "assistant",
      agent: "general",
      content:
        "您好，欢迎光临。我是客诉服务台的智能客服，可以帮您查询订单、解答商品与退换货政策问题。请问有什么可以帮您？",
      sources: [],
    })
  }
})
</script>

<template>
  <div class="chat">
    <div class="chat-head">
      <span class="chat-title">智能对话</span>
      <span class="chat-meta mono">会话 {{ sid.slice(0, 8) }}</span>
      <span v-if="userStore.user_id" class="chat-user mono">
        {{ userStore.user_name }} · 已登录
      </span>
      <span v-else class="chat-user mono">未登录 · 订单查询需先登录</span>
    </div>

    <div ref="listRef" class="chat-list">
      <div v-if="!messages.length" class="empty">
        <div class="empty-mark mono">台</div>
        <div class="empty-title">深夜服务台，静候您来</div>
        <div class="empty-sub">
          询问商品与政策，或登录后查询订单。所有回答都会附上引用凭证，方便您核对。
        </div>
        <div class="suggestions">
          <button
            v-for="s in suggestions"
            :key="s"
            class="suggestion"
            @click="send(s)"
          >
            {{ s }}
          </button>
        </div>
      </div>

      <MessageBubble
        v-for="(m, i) in messages"
        :key="i"
        :role="m.role"
        :content="m.content"
        :thinking="m.thinking"
        :error="m.error"
        :agent="m.agent"
        :sources="m.sources"
      />
    </div>

    <div class="chat-input">
      <div class="input-box">
        <textarea
          v-model="input"
          rows="1"
          placeholder="输入您的问题，Enter 发送，Shift+Enter 换行"
          @keydown="onKeydown"
        ></textarea>
        <button class="send-btn" :disabled="busy || !input.trim()" aria-label="发送" @click="send()">
          ➤
        </button>
      </div>
      <div class="input-hint mono">AI 生成内容仅供参考，订单数据以系统记录为准</div>
    </div>
  </div>
</template>

<style scoped>
.chat {
  height: 100%;
  display: flex;
  flex-direction: column;
  max-width: 860px;
  margin: 0 auto;
  width: 100%;
  padding: 0 16px;
}

.chat-head {
  display: flex;
  align-items: baseline;
  gap: 12px;
  padding: 14px 2px 8px;
  flex-wrap: wrap;
}

.chat-title {
  font-weight: 700;
  color: var(--paper);
  letter-spacing: 0.04em;
}

.chat-meta,
.chat-user {
  font-size: 12px;
  color: var(--muted);
}

.chat-user {
  margin-left: auto;
}

.chat-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px 4px 16px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.empty {
  margin: auto;
  text-align: center;
  max-width: 460px;
  padding: 32px;
}

.empty-mark {
  font-size: 42px;
  color: var(--amber);
  letter-spacing: 0.2em;
}

.empty-title {
  font-weight: 700;
  color: var(--paper);
  margin: 14px 0 6px;
  letter-spacing: 0.04em;
}

.empty-sub {
  color: var(--muted);
  font-size: 14px;
  line-height: 1.7;
}

.suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-top: 20px;
}

.suggestion {
  background: var(--ink-raised);
  color: var(--paper-dim);
  border: 1px solid var(--line);
  padding: 8px 14px;
  border-radius: 999px;
  font-size: 13px;
  cursor: pointer;
  font-family: inherit;
  transition: border-color 0.15s, color 0.15s;
}

.suggestion:hover {
  border-color: var(--amber);
  color: var(--amber);
}

.chat-input {
  padding: 12px 0 16px;
}

.input-box {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  background: var(--ink-raised);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 10px 10px 10px 14px;
  transition: border-color 0.15s;
}

.input-box:focus-within {
  border-color: var(--amber);
}

textarea {
  flex: 1;
  resize: none;
  border: 0;
  outline: 0;
  background: transparent;
  color: var(--paper);
  font-family: inherit;
  font-size: 15px;
  line-height: 1.6;
  max-height: 120px;
  padding: 4px 0;
}

textarea::placeholder {
  color: var(--muted);
}

.send-btn {
  background: var(--amber);
  color: var(--ink-deep);
  border: 0;
  border-radius: 10px;
  width: 42px;
  height: 42px;
  font-size: 18px;
  cursor: pointer;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: filter 0.15s, transform 0.05s;
}

.send-btn:hover {
  filter: brightness(1.08);
}

.send-btn:active {
  transform: scale(0.96);
}

.send-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.input-hint {
  font-size: 11px;
  color: var(--muted);
  padding: 6px 4px 0;
}

@media (max-width: 640px) {
  .chat {
    padding: 0 10px;
  }
  .chat-user {
    margin-left: 0;
    width: 100%;
  }
}
</style>