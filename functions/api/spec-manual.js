// CF Pages Functions: GET/POST /api/spec-manual
// GET: 返回 { html, updatedAt } 或 { html: null } (还没存过)
// POST: 需 Authorization: Bearer <SPEC_TOKEN>, body 是 { html }, 存到 KV, 返回 { ok, updatedAt }

const KV_KEY = 'spec-manual-latest';

function cors(resp) {
  resp.headers.set('Access-Control-Allow-Origin', '*');
  resp.headers.set('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  resp.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization');
  return resp;
}

export async function onRequestOptions() {
  return cors(new Response(null, { status: 204 }));
}

export async function onRequestGet({ env }) {
  const raw = await env.SPEC_KV.get(KV_KEY);
  if (!raw) return cors(new Response(JSON.stringify({ html: null }), { headers: { 'Content-Type': 'application/json' } }));
  return cors(new Response(raw, { headers: { 'Content-Type': 'application/json' } }));
}

export async function onRequestPost({ request, env }) {
  const url = new URL(request.url);
  const queryToken = url.searchParams.get('token');
  const auth = request.headers.get('Authorization') || '';
  const headerToken = auth.replace(/^Bearer\s+/, '');
  const token = headerToken || queryToken;
  if (!token || token !== env.SPEC_TOKEN) {
    return cors(new Response(JSON.stringify({ error: 'unauthorized' }), { status: 401, headers: { 'Content-Type': 'application/json' } }));
  }
  let body;
  try { body = await request.json(); } catch { return cors(new Response(JSON.stringify({ error: 'bad json' }), { status: 400, headers: { 'Content-Type': 'application/json' } })); }
  const html = body && body.html;
  if (typeof html !== 'string' || html.length < 100 || html.length > 5_000_000) {
    return cors(new Response(JSON.stringify({ error: 'invalid html' }), { status: 400, headers: { 'Content-Type': 'application/json' } }));
  }
  const updatedAt = new Date().toISOString();
  const payload = JSON.stringify({ html, updatedAt });
  await env.SPEC_KV.put(KV_KEY, payload);
  return cors(new Response(JSON.stringify({ ok: true, updatedAt }), { headers: { 'Content-Type': 'application/json' } }));
}
