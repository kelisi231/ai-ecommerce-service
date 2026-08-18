<script setup>
import { ref, onMounted } from "vue"
import { apiList, apiDelete, apiUpload } from "../api"

const docs = ref([])
const loading = ref(false)
const busy = ref(false)
const message = ref("")
const pending = ref([])
const fileInput = ref(null)

async function refresh() {
  loading.value = true
  try {
    docs.value = await apiList()
  } catch (err) {
    message.value = `加载失败：${err.message}`
  } finally {
    loading.value = false
  }
}

async function onFiles(files) {
  if (!files.length) return
  pending.value = files.map((f) => ({ name: f.name, status: "上传中" }))
  message.value = ""
  try {
    const results = await apiUpload(files)
    pending.value = results.map((r) => ({
      name: r.file_name,
      status: `已入库 · ${r.chunk_count} 个片段`,
    }))
    await refresh()
  } catch (err) {
    pending.value = pending.value.map((p) => ({ ...p, status: "失败" }))
    message.value = `上传失败：${err.message}`
  }
}

function onFileChange(e) {
  onFiles(Array.from(e.target.files ?? []))
  e.target.value = ""
}

function onDrop(e) {
  onFiles(Array.from(e.dataTransfer?.files ?? []))
}

async function remove(doc) {
  if (!confirm(`确定删除「${doc.file_name}」吗？相关片段会从检索中移除。`)) return
  busy.value = true
  message.value = ""
  try {
    await apiDelete(doc.doc_id)
    await refresh()
  } catch (err) {
    message.value = `删除失败：${err.message}`
  } finally {
    busy.value = false
  }
}

onMounted(refresh)
</script>

<template>
  <div class="know">
    <div class="know-head">
      <span class="know-title">知识库</span>
      <span class="know-count mono">
        {{ loading ? "同步中…" : `${docs.length} 份文档` }}
      </span>
      <span class="spacer"></span>
      <button class="refresh-btn" :disabled="loading" @click="refresh">
        {{ loading ? "刷新中…" : "刷新" }}
      </button>
    </div>

    <p v-if="message" class="know-msg err" role="alert">{{ message }}</p>

    <div
      class="dropzone"
      role="button"
      tabindex="0"
      @click="fileInput.click()"
      @keydown.enter="fileInput.click()"
      @dragover.prevent
      @drop.prevent="onDrop"
    >
      <div class="drop-mark mono">+</div>
      <div class="drop-title">拖拽文档到这里，或点击选择</div>
      <div class="drop-sub mono">支持 PDF / TXT / DOCX，多选上传</div>
      <input
        ref="fileInput"
        type="file"
        multiple
        accept=".pdf,.txt,.docx"
        hidden
        @change="onFileChange"
      />
    </div>

    <div v-if="pending.length" class="pending">
      <div v-for="p in pending" :key="p.name" class="pending-item">
        <span>{{ p.name }}</span>
        <span class="pending-status mono">{{ p.status }}</span>
      </div>
    </div>

    <section class="docs">
      <template v-if="loading">
        <div class="docs-empty">正在同步文档列表…</div>
      </template>
      <template v-else-if="!docs.length">
        <div class="docs-empty">
          <div class="docs-empty-title">知识库还是空的</div>
          <div class="docs-empty-sub">上传一份商品说明或政策文档，智能客服就能回答对应问题了。</div>
        </div>
      </template>
      <table v-else class="docs-table">
        <thead>
          <tr>
            <th>文档</th>
            <th>文档编号</th>
            <th>片段数</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="doc in docs" :key="doc.doc_id">
            <td class="file-name">{{ doc.file_name }}</td>
            <td class="doc-id mono">{{ doc.doc_id.slice(0, 12) }}…</td>
            <td class="chunk-count mono">{{ doc.chunk_count }}</td>
            <td class="td-right">
              <button class="delete-btn" :disabled="busy" @click="remove(doc)">
                删除
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<style scoped>
.know {
  max-width: 860px;
  margin: 0 auto;
  padding: 18px 16px 40px;
}

.know-head {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.know-title {
  font-weight: 700;
  color: var(--paper);
  font-size: 18px;
  letter-spacing: 0.03em;
}

.know-count {
  font-size: 12px;
  color: var(--muted);
}

.spacer {
  flex: 1;
}

.refresh-btn {
  background: transparent;
  border: 1px solid var(--line);
  color: var(--text-on-dark);
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 13px;
  cursor: pointer;
  font-family: inherit;
  transition: border-color 0.15s, color 0.15s;
}

.refresh-btn:hover:not(:disabled) {
  border-color: var(--amber);
  color: var(--amber);
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.know-msg {
  margin: 0 0 12px;
  font-size: 13px;
  color: #ff9c8a;
}

.dropzone {
  border: 1.5px dashed rgba(244, 239, 230, 0.25);
  border-radius: var(--radius);
  padding: 30px 20px;
  text-align: center;
  cursor: pointer;
  color: var(--muted);
  transition: border-color 0.15s, background 0.15s, color 0.15s;
  outline: none;
}

.dropzone:hover,
.dropzone:focus-visible {
  border-color: var(--amber);
  background: rgba(229, 160, 60, 0.06);
  color: var(--amber);
}

.drop-mark {
  font-size: 26px;
  color: var(--amber);
  line-height: 1;
}

.drop-title {
  margin: 8px 0 4px;
  font-size: 15px;
  color: var(--text-on-dark);
}

.drop-sub {
  font-size: 12px;
}

.pending {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.pending-item {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  font-size: 13px;
  background: var(--ink-raised);
  padding: 8px 12px;
  border-radius: 8px;
}

.pending-status {
  color: var(--amber);
  white-space: nowrap;
}

.docs {
  margin-top: 22px;
}

.docs-empty {
  text-align: center;
  color: var(--muted);
  padding: 34px 20px;
  border: 1px dashed var(--line);
  border-radius: var(--radius);
}

.docs-empty-title {
  color: var(--paper-dim);
  font-weight: 600;
  margin-bottom: 6px;
}

.docs-empty-sub {
  font-size: 13px;
}

.docs-table {
  width: 100%;
  border-collapse: collapse;
}

.docs-table th {
  text-align: left;
  font-size: 12px;
  color: var(--muted);
  font-weight: 500;
  padding: 8px 10px;
  border-bottom: 1px solid var(--line);
  letter-spacing: 0.05em;
}

.docs-table td {
  padding: 10px;
  border-bottom: 1px solid var(--line);
  font-size: 14px;
  color: var(--text-on-dark);
}

.file-name {
  font-weight: 600;
  max-width: 220px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.doc-id {
  font-size: 12px;
  color: var(--muted);
}

.chunk-count {
  color: var(--amber);
}

.td-right {
  text-align: right;
}

.delete-btn {
  background: transparent;
  border: 1px solid rgba(196, 85, 63, 0.5);
  color: #ff9c8a;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 12px;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.15s;
}

.delete-btn:hover:not(:disabled) {
  background: rgba(196, 85, 63, 0.15);
}

.delete-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .doc-id {
    display: none;
  }
}
</style>