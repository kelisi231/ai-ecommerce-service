<script setup>
import { ref } from "vue"

const props = defineProps({
  role: { type: String, required: true },
  content: { type: String, default: "" },
  thinking: { type: Boolean, default: false },
  error: { type: Boolean, default: false },
  agent: { type: String, default: "" },
  sources: { type: Array, default: () => [] },
})

const AGENT_LABEL = {
  qa: "知识问答",
  order: "订单助手",
  general: "通用助理",
}

const openSources = ref(new Set())

function toggle(i) {
  const next = new Set(openSources.value)
  if (next.has(i)) next.delete(i)
  else next.add(i)
  openSources.value = next
}
</script>

<template>
  <div class="msg" :class="role">
    <div class="bubble" :class="{ error }">
      <template v-if="props.thinking">
        <span class="typing" aria-label="思考中">
          <i></i><i></i><i></i>
        </span>
      </template>
      <template v-else>
        <span v-if="agent && AGENT_LABEL[agent]" class="agent-tag mono">
          {{ AGENT_LABEL[agent] }}
        </span>
        <p class="text">{{ props.content }}</p>

        <div v-if="sources && sources.length" class="vouchers">
          <div class="voucher-head mono">引用凭证 · {{ sources.length }}</div>
          <button
            v-for="(s, i) in sources"
            :key="s.chunk_id"
            class="voucher"
            @click="toggle(i)"
          >
            <span class="voucher-no">{{ i + 1 }}</span>
            <span class="voucher-src">{{ s.source }} #{{ s.index }}</span>
            <span class="voucher-score">{{ (s.score ?? 0).toFixed(2) }}</span>
          </button>
          <div v-if="openSources.size" class="voucher-detail">
            <div
              v-for="(s, i) in sources"
              v-show="openSources.has(i)"
              :key="s.chunk_id"
              class="voucher-detail-item"
            >
              {{ s.content }}
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.msg {
  display: flex;
  animation: rise 0.22s ease-out;
}

@keyframes rise {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: none;
  }
}

.msg.user {
  justify-content: flex-end;
}

.bubble {
  max-width: 78%;
  border-radius: var(--radius);
  padding: 10px 14px;
  font-size: 15px;
  line-height: 1.7;
  white-space: pre-wrap;
  word-break: break-word;
}

.msg.user .bubble {
  background: var(--amber);
  color: var(--ink-deep);
  border-bottom-right-radius: 4px;
}

.msg.assistant .bubble {
  background: var(--paper);
  color: #2b2a26;
  border-bottom-left-radius: 4px;
}

.msg.error .bubble {
  background: rgba(196, 85, 63, 0.18);
  color: #ffb4a5;
  border: 1px solid rgba(196, 85, 63, 0.4);
}

.text {
  margin: 0;
}

.agent-tag {
  display: inline-block;
  font-size: 11px;
  letter-spacing: 0.08em;
  color: var(--mint);
  background: var(--ink);
  border-radius: 4px;
  padding: 1px 8px;
  margin-bottom: 6px;
}

.typing {
  display: inline-flex;
  gap: 5px;
  align-items: center;
  padding: 4px 2px;
}

.typing i {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--muted);
  animation: blink 1.2s infinite;
}

.typing i:nth-child(2) {
  animation-delay: 0.2s;
}

.typing i:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes blink {
  0%,
  80%,
  100% {
    opacity: 0.25;
    transform: translateY(0);
  }
  40% {
    opacity: 1;
    transform: translateY(-3px);
  }
}

.vouchers {
  margin-top: 10px;
  border-top: 1px dashed rgba(20, 25, 22, 0.18);
  padding-top: 8px;
}

.voucher-head {
  font-size: 11px;
  color: #8a8577;
  letter-spacing: 0.08em;
  margin-bottom: 6px;
}

.voucher {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  background: transparent;
  border: 1px solid rgba(20, 25, 22, 0.15);
  border-radius: 8px;
  padding: 5px 10px;
  margin-bottom: 4px;
  cursor: pointer;
  text-align: left;
  font-family: inherit;
  font-size: 12.5px;
  color: #3a382f;
  transition: border-color 0.15s, background 0.15s;
}

.voucher:hover {
  border-color: var(--amber);
  background: rgba(229, 160, 60, 0.08);
}

.voucher-no {
  font-family: var(--font-mono);
  font-weight: 700;
  color: var(--amber);
  font-size: 12px;
}

.voucher-src {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.voucher-score {
  font-family: var(--font-mono);
  color: #8a8577;
  font-size: 11px;
}

.voucher-detail {
  margin-top: 4px;
}

.voucher-detail-item {
  font-size: 12.5px;
  color: #5a564a;
  background: rgba(20, 25, 22, 0.05);
  border-radius: 8px;
  padding: 8px 10px;
  margin-bottom: 4px;
  line-height: 1.6;
  max-height: 120px;
  overflow-y: auto;
}

@media (max-width: 640px) {
  .bubble {
    max-width: 92%;
  }
}
</style>