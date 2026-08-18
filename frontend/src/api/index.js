async function request(path, options = {}) {
  const resp = await fetch(path, options)
  if (!resp.ok) {
    let detail = `请求失败 (${resp.status})`
    try {
      const body = await resp.json()
      if (body && body.detail) {
        detail = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail)
      }
    } catch {
      /* ignore */
    }
    throw new Error(detail)
  }
  const text = await resp.text()
  return text ? JSON.parse(text) : null
}

function json(method, body) {
  return {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  }
}

export function apiLogin(username, password) {
  return request("/login/login", json("POST", { username, password }))
}

export function apiChat(payload) {
  return request("/agent/chat", json("POST", payload))
}

export function apiUpload(files) {
  const form = new FormData()
  for (const f of files) form.append("files", f)
  return request("/knowledge/upload", { method: "POST", body: form })
}

export function apiList() {
  return request("/knowledge/list")
}

export function apiDelete(docId) {
  return request(`/knowledge/delete?doc_id=${encodeURIComponent(docId)}`, {
    method: "DELETE",
  })
}