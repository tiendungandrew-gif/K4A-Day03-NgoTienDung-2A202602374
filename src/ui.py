"""
🖥️ VINFAST HR REACT AGENT - PREMIUM WEB UI
Giao diện Web chuyên nghiệp, hiện đại phục vụ tương tác trực quan với ReAct Agent & MCP Server.
Chạy thuần thư viện chuẩn Python (Standard Library), không cần cài đặt thêm thư viện ngoài.
"""

import os
import sys
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

# Thêm thư mục hiện tại vào sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from app import run_react_agent, save_waterfall_trace, load_test_cases
from providers import get_llm_provider
from mcp_server import MCPAcademicServer

# Khởi tạo Provider và MCP Server
provider = get_llm_provider()
mcp_server = MCPAcademicServer()

HTML_PAGE = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VinFast HR ReAct Agent - Enterprise Studio</title>
  <style>
    :root {
      --bg-main: #0b1329;
      --bg-sidebar: #070d1e;
      --bg-card: #131f37;
      --bg-card-hover: #1a2a4a;
      --border-subtle: #1e2f50;
      --border-focus: #3b82f6;
      
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      
      --vf-red: #e11b22;
      --vf-red-glow: rgba(225, 27, 34, 0.35);
      --vf-blue: #2563eb;
      
      --color-thought: #818cf8;
      --bg-thought: rgba(99, 102, 241, 0.08);
      --border-thought: #4f46e5;
      
      --color-action: #34d399;
      --bg-action: rgba(16, 185, 129, 0.08);
      --border-action: #059669;
      
      --color-final: #38bdf8;
      --bg-final: rgba(56, 189, 248, 0.08);
      --border-final: #0284c7;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; }
    body { background: var(--bg-main); color: var(--text-primary); display: flex; height: 100vh; overflow: hidden; }

    /* SIDEBAR */
    aside {
      width: 320px;
      background: var(--bg-sidebar);
      border-right: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }

    .brand-header {
      padding: 20px 24px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-logo {
      background: linear-gradient(135deg, #e11b22 0%, #b91c1c 100%);
      color: white;
      font-weight: 900;
      font-size: 16px;
      padding: 8px 12px;
      border-radius: 10px;
      letter-spacing: 1px;
      box-shadow: 0 4px 14px var(--vf-red-glow);
    }
    .brand-info h1 { font-size: 15px; font-weight: 700; color: #ffffff; letter-spacing: 0.3px; }
    .brand-info p { font-size: 11px; color: var(--text-muted); margin-top: 2px; }

    .server-status {
      margin: 16px 20px;
      padding: 12px 14px;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .status-row { display: flex; justify-content: space-between; align-items: center; font-size: 11px; }
    .status-badge { display: flex; align-items: center; gap: 6px; color: #4ade80; font-weight: 600; }
    .dot-pulse { width: 7px; height: 7px; background: #22c55e; border-radius: 50%; box-shadow: 0 0 10px #22c55e; animation: pulse 1.8s infinite; }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

    .sidebar-section {
      padding: 12px 20px;
      flex: 1;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .section-title {
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.8px;
    }

    .test-suite-list { display: flex; flex-direction: column; gap: 8px; }
    .test-item {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 10px 12px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .test-item:hover {
      background: var(--bg-card-hover);
      border-color: var(--border-focus);
      transform: translateX(3px);
    }
    .test-item-top { display: flex; justify-content: space-between; align-items: center; }
    .test-tag { font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px; }
    .tag-low { background: #064e3b; color: #34d399; }
    .tag-med { background: #1e3a8a; color: #60a5fa; }
    .tag-high { background: #701a75; color: #f472b6; }
    .test-name { font-size: 12px; font-weight: 600; color: #e2e8f0; }
    .test-desc { font-size: 11px; color: var(--text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

    /* MAIN CHAT */
    main {
      flex: 1;
      display: flex;
      flex-direction: column;
      background: radial-gradient(circle at 50% 0%, #152243 0%, var(--bg-main) 60%);
      overflow: hidden;
    }

    .top-toolbar {
      padding: 16px 28px;
      border-bottom: 1px solid var(--border-subtle);
      background: rgba(11, 19, 41, 0.7);
      backdrop-filter: blur(12px);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .top-title { display: flex; align-items: center; gap: 10px; }
    .agent-avatar {
      width: 34px;
      height: 34px;
      border-radius: 10px;
      background: linear-gradient(135deg, #2563eb, #38bdf8);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      box-shadow: 0 2px 8px rgba(37,99,235,0.4);
    }
    .toolbar-actions { display: flex; gap: 10px; }
    .btn-secondary {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      font-size: 12px;
      padding: 6px 14px;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .btn-secondary:hover { color: white; border-color: var(--text-secondary); }

    .chat-container {
      flex: 1;
      overflow-y: auto;
      padding: 28px;
      display: flex;
      flex-direction: column;
      gap: 24px;
      scroll-behavior: smooth;
    }

    .msg-wrapper {
      display: flex;
      flex-direction: column;
      max-width: 920px;
      width: 100%;
      margin: 0 auto;
      gap: 12px;
    }

    /* USER MESSAGE */
    .user-bubble {
      align-self: flex-end;
      background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
      color: #ffffff;
      padding: 14px 20px;
      border-radius: 18px 18px 4px 18px;
      font-size: 14.5px;
      line-height: 1.55;
      max-width: 82%;
      box-shadow: 0 4px 16px rgba(37, 99, 235, 0.35);
      letter-spacing: 0.1px;
    }

    /* REACT AGENT CARD */
    .agent-card {
      background: rgba(19, 31, 55, 0.75);
      border: 1px solid var(--border-subtle);
      border-radius: 18px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
      backdrop-filter: blur(10px);
      animation: fadeIn 0.3s ease;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }

    /* WATERFALL STEPS */
    .step-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }
    .step-badge::before {
      content: "";
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #38bdf8;
    }

    /* THOUGHT BOX */
    .thought-box {
      background: var(--bg-thought);
      border: 1px solid var(--border-thought);
      border-left: 4px solid var(--color-thought);
      border-radius: 6px 12px 12px 6px;
      padding: 12px 16px;
      color: #c7d2fe;
      font-size: 13.5px;
      line-height: 1.5;
    }
    .thought-header {
      display: flex;
      align-items: center;
      gap: 6px;
      font-weight: 700;
      font-size: 11.5px;
      color: var(--color-thought);
      margin-bottom: 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    /* ACTION BOX */
    .action-box {
      background: var(--bg-action);
      border: 1px solid var(--border-action);
      border-radius: 12px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .action-badge {
      align-self: flex-start;
      background: linear-gradient(135deg, #059669, #10b981);
      color: white;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 6px;
      letter-spacing: 0.4px;
    }
    .action-args {
      font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
      font-size: 12.5px;
      background: rgba(0, 0, 0, 0.4);
      border-radius: 8px;
      padding: 8px 12px;
      color: #6ee7b7;
      overflow-x: auto;
    }

    /* OBSERVATION BOX */
    .obs-box {
      background: #061e16;
      border-left: 3px solid #10b981;
      border-radius: 4px 8px 8px 4px;
      padding: 10px 14px;
      font-family: monospace;
      font-size: 12px;
      color: #a7f3d0;
      overflow-x: auto;
    }

    /* FINAL ANSWER CARD */
    .final-card {
      background: linear-gradient(135deg, rgba(6, 78, 59, 0.35) 0%, rgba(2, 44, 34, 0.4) 100%);
      border: 1px solid #059669;
      border-radius: 14px;
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      box-shadow: 0 4px 16px rgba(5, 150, 105, 0.15);
    }
    .final-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      font-weight: 700;
      color: #34d399;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .final-text {
      font-size: 14.5px;
      line-height: 1.6;
      color: #f0fdf4;
    }

    /* EMPLOYEE CARD OVERLAY */
    .employee-card {
      margin-top: 8px;
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 14px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 10px;
    }
    .emp-stat { display: flex; flex-direction: column; }
    .emp-stat-label { font-size: 10.5px; color: var(--text-muted); text-transform: uppercase; font-weight: 600; }
    .emp-stat-val { font-size: 14px; font-weight: 700; color: #f8fafc; margin-top: 2px; }
    .emp-stat-val.highlight { color: #38bdf8; }

    /* INPUT SECTION */
    .input-wrapper {
      padding: 20px 28px;
      background: rgba(11, 19, 41, 0.9);
      border-top: 1px solid var(--border-subtle);
      backdrop-filter: blur(12px);
    }
    .input-box-container {
      max-width: 920px;
      margin: 0 auto;
      display: flex;
      gap: 12px;
      position: relative;
    }
    input[type="text"] {
      flex: 1;
      background: rgba(19, 31, 55, 0.9);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 16px 20px;
      font-size: 14.5px;
      color: #ffffff;
      outline: none;
      transition: all 0.25s;
    }
    input[type="text"]:focus {
      border-color: #3b82f6;
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25);
      background: #14213d;
    }
    .btn-send {
      background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
      color: white;
      border: none;
      padding: 0 28px;
      border-radius: 14px;
      font-size: 14.5px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
      transition: all 0.2s;
    }
    .btn-send:hover {
      background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
      transform: translateY(-1px);
    }
    .btn-send:disabled {
      opacity: 0.6;
      cursor: not-allowed;
      transform: none;
    }

    .spinner {
      width: 16px;
      height: 16px;
      border: 2px solid rgba(255,255,255,0.3);
      border-top-color: white;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    /* SCROLLBAR */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #263859; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #3b5078; }
  </style>
</head>
<body>

  <!-- LEFT SIDEBAR -->
  <aside>
    <div class="brand-header">
      <div class="brand-logo">VF</div>
      <div class="brand-info">
        <h1>VINFAST HR STUDIO</h1>
        <p>ReAct Agent • MCP JSON-RPC 2.0</p>
      </div>
    </div>

    <div class="server-status">
      <div class="status-row">
        <span style="color: var(--text-secondary); font-weight:600;">HỆ THỐNG MCP</span>
        <div class="status-badge">
          <span class="dot-pulse"></span>
          <span>ONLINE</span>
        </div>
      </div>
      <div class="status-row" style="color: var(--text-muted);">
        <span>Server Name:</span>
        <span style="font-family: monospace; color:#cbd5e1;">vinfast-hr-server</span>
      </div>
      <div class="status-row" style="color: var(--text-muted);">
        <span>Tools công bố:</span>
        <span style="font-weight:700; color:#38bdf8;">3 Native Tools</span>
      </div>
    </div>

    <div class="sidebar-section">
      <div class="section-title">⚡ Bộ 5 Test Cases nghiệm thu</div>
      
      <div class="test-suite-list">
        <div class="test-item" onclick="selectCase('TC01')">
          <div class="test-item-top">
            <span class="test-name">TC01: Chính sách nhân sự</span>
            <span class="test-tag tag-low">Low</span>
          </div>
          <div class="test-desc">Hỏi FAQ chính sách chung không cần gọi Tool</div>
        </div>

        <div class="test-item" onclick="selectCase('TC02')">
          <div class="test-item-top">
            <span class="test-name">TC02: Tra cứu ngày phép</span>
            <span class="test-tag tag-med">Medium</span>
          </div>
          <div class="test-desc">Gọi Tool leave_balance_query mã NV2026001</div>
        </div>

        <div class="test-item" onclick="selectCase('TC03')">
          <div class="test-item-top">
            <span class="test-name">TC03: Tạo đơn xin nghỉ</span>
            <span class="test-tag tag-med">Medium</span>
          </div>
          <div class="test-desc">Tạo đơn nghỉ phép năm 2 ngày qua MCP Tool</div>
        </div>

        <div class="test-item" onclick="selectCase('TC04')">
          <div class="test-item-top">
            <span class="test-name">TC04: Suy luận đa bước</span>
            <span class="test-tag tag-high">High</span>
          </div>
          <div class="test-desc">Tra cứu số dư phép rồi điều hướng tạo đơn</div>
        </div>

        <div class="test-item" onclick="selectCase('TC05')">
          <div class="test-item-top">
            <span class="test-name">TC05: Xử lý ngoại lệ</span>
            <span class="test-tag tag-med">Medium</span>
          </div>
          <div class="test-desc">Xử lý NOT_FOUND khi mã nhân viên NV9999999</div>
        </div>
      </div>

      <div class="section-title" style="margin-top: 8px;">🛠️ Danh mục MCP Tools</div>
      <div style="font-size: 11px; color: var(--text-muted); display:flex; flex-direction:column; gap:6px;">
        <div style="display:flex; justify-content:space-between; background:rgba(255,255,255,0.02); padding:6px 8px; border-radius:6px;">
          <span style="color:#6ee7b7; font-family:monospace;">leave_balance_query</span>
          <span>Tra cứu</span>
        </div>
        <div style="display:flex; justify-content:space-between; background:rgba(255,255,255,0.02); padding:6px 8px; border-radius:6px;">
          <span style="color:#6ee7b7; font-family:monospace;">create_leave_request</span>
          <span>Tạo đơn</span>
        </div>
        <div style="display:flex; justify-content:space-between; background:rgba(255,255,255,0.02); padding:6px 8px; border-radius:6px;">
          <span style="color:#6ee7b7; font-family:monospace;">insurance_policy_query</span>
          <span>Bảo hiểm</span>
        </div>
      </div>
    </div>
  </aside>

  <!-- MAIN CHAT AREA -->
  <main>
    <div class="top-toolbar">
      <div class="top-title">
        <div class="agent-avatar">🤖</div>
        <div>
          <div style="font-weight: 700; font-size: 15px; color: white;">Trợ lý Tác tử Nhân sự VinFast (HR ReAct Agent)</div>
          <div style="font-size: 11px; color: var(--text-muted);">Mô hình kết nối MCP Server • Chu trình Thought ➔ Action ➔ Observation ➔ Answer</div>
        </div>
      </div>
      <div class="toolbar-actions">
        <button class="btn-secondary" onclick="clearChat()">🗑️ Xóa hội thoại</button>
      </div>
    </div>

    <div class="chat-container" id="chatArea">
      <!-- Welcome Message -->
      <div class="msg-wrapper">
        <div class="agent-card">
          <div class="final-card" style="background: rgba(30, 41, 59, 0.6); border-color: #334155;">
            <div class="final-header">
              <span>👋 Chào mừng bạn đến với Hệ thống VinFast HR Agentic Studio</span>
              <span style="font-size: 10px; background:#2563eb; color:white; padding:2px 8px; border-radius:4px;">Ready</span>
            </div>
            <div class="final-text" style="color: #cbd5e1; font-size: 14px;">
              Tôi là <strong>Trợ lý Tác tử Nhân sự ReAct Agent</strong> của VinFast. Tôi có thể trực tiếp thực thi các công cụ tra cứu và tạo đơn nhân sự thông qua máy chủ MCP Server.<br><br>
              👉 <em>Hãy nhấp vào các Test Case ở thanh bên trái hoặc tự do gõ câu hỏi vào ô nhập liệu bên dưới để bắt đầu trải nghiệm!</em>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- INPUT BAR -->
    <div class="input-wrapper">
      <div class="input-box-container">
        <input type="text" id="userInput" placeholder="Nhập yêu cầu nhân sự (ví dụ: tra cứu ngày phép của NV2026001, tạo đơn nghỉ phép...)" onkeypress="if(event.key === 'Enter') sendQuery()">
        <button class="btn-send" id="sendBtn" onclick="sendQuery()">
          <span>Gửi yêu cầu</span>
        </button>
      </div>
    </div>
  </main>

  <script>
    const TEST_CASES_DATA = {
      'TC01': 'Bạn có thể giới thiệu các chính sách nhân sự cơ bản của VinFast không?',
      'TC02': 'Hãy tra cứu số ngày phép còn lại của nhân viên có mã NV2026001.',
      'TC03': 'Tôi muốn tạo đơn xin nghỉ phép năm 2 ngày, từ ngày 20/09/2026 đến ngày 21/09/2026, lý do việc cá nhân.',
      'TC04': 'Tôi muốn nghỉ phép 3 ngày từ 20/09/2026 đến 22/09/2026. Hãy kiểm tra số ngày phép còn lại, nếu đủ thì hướng dẫn tôi tạo đơn xin nghỉ phép.',
      'TC05': 'Hãy tra cứu số ngày phép còn lại của nhân viên có mã NV9999999.'
    };

    function selectCase(tcId) {
      const q = TEST_CASES_DATA[tcId];
      if (!q) return;
      document.getElementById('userInput').value = q;
      sendQuery();
    }

    function clearChat() {
      const chat = document.getElementById('chatArea');
      chat.innerHTML = `
        <div class="msg-wrapper">
          <div class="agent-card">
            <div class="final-card" style="background: rgba(30, 41, 59, 0.6); border-color: #334155;">
              <div class="final-header">
                <span>Hội thoại đã được làm mới</span>
              </div>
              <div class="final-text" style="color: #cbd5e1; font-size: 14px;">
                Sẵn sàng tiếp nhận câu hỏi hoặc yêu cầu nhân sự mới từ bạn.
              </div>
            </div>
          </div>
        </div>
      `;
    }

    async function sendQuery() {
      const input = document.getElementById('userInput');
      const text = input.value.trim();
      if (!text) return;

      const chat = document.getElementById('chatArea');
      const sendBtn = document.getElementById('sendBtn');

      // Append user bubble
      const wrapper = document.createElement('div');
      wrapper.className = 'msg-wrapper';
      wrapper.innerHTML = `<div class="user-bubble">${escapeHtml(text)}</div>`;
      chat.appendChild(wrapper);

      input.value = '';
      sendBtn.disabled = true;
      sendBtn.innerHTML = `<div class="spinner"></div><span>Đang suy luận...</span>`;
      chat.scrollTop = chat.scrollHeight;

      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: text })
        });
        const data = await response.json();
        renderAgentTrace(wrapper, data);
      } catch (err) {
        renderErrorCard(wrapper, err.message);
      } finally {
        sendBtn.disabled = false;
        sendBtn.innerHTML = `<span>Gửi yêu cầu</span>`;
        chat.scrollTop = chat.scrollHeight;
      }
    }

    function renderAgentTrace(wrapper, data) {
      const card = document.createElement('div');
      card.className = 'agent-card';

      const traces = data.traces || [];
      traces.forEach(t => {
        // Thought
        if (t.thought) {
          card.innerHTML += `
            <div class="step-badge">BƯỚC ${t.step || 1}: SUY LUẬN LOGIC</div>
            <div class="thought-box">
              <div class="thought-header">🧠 Thought (Suy luận tác tử):</div>
              <div>${escapeHtml(t.thought)}</div>
            </div>
          `;
        }

        // Tool Execution
        if (t.action_type === 'TOOL_EXECUTION') {
          let obsJson = escapeHtml(JSON.stringify(t.observation || {}, null, 2));
          card.innerHTML += `
            <div class="action-box">
              <div class="action-badge">🛠️ ACTION ➔ GỌI MCP TOOL: ${escapeHtml(t.tool_name)}</div>
              <div class="action-args"><strong>Tham số:</strong> ${escapeHtml(JSON.stringify(t.arguments || {}))}</div>
              <div class="obs-box">
                <div style="font-weight:700; color:#34d399; margin-bottom:4px;">👁️ Observation (Kết quả trả về từ MCP Server):</div>
                <pre style="margin:0; white-space:pre-wrap;">${obsJson}</pre>
              </div>
            </div>
          `;
        }

        // Final Answer
        if (t.action_type === 'FINAL_ANSWER') {
          card.innerHTML += `
            <div class="final-card">
              <div class="final-header">
                <span>🏁 CÂU TRẢ LỜI CUỐI CÙNG (FINAL ANSWER)</span>
                <span style="font-size: 10px; color:#6ee7b7; text-transform:none;">⏱️ ${t.latency_ms || 10}ms</span>
              </div>
              <div class="final-text">${escapeHtml(t.output)}</div>
            </div>
          `;
        }
      });

      wrapper.appendChild(card);
    }

    function renderErrorCard(wrapper, msg) {
      const card = document.createElement('div');
      card.className = 'agent-card';
      card.innerHTML = `
        <div class="final-card" style="border-color:#ef4444; background:rgba(127,29,29,0.2);">
          <div class="final-header" style="color:#f87171;">❌ LỖI HỆ THỐNG</div>
          <div class="final-text" style="color:#fca5a5;">${escapeHtml(msg)}</div>
        </div>
      `;
      wrapper.appendChild(card);
    }

    function escapeHtml(t) {
      if (typeof t !== 'string') t = JSON.stringify(t);
      return t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }
  </script>
</body>
</html>
"""

class ReActAgentWebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif self.path == "/api/test_cases":
            cases = load_test_cases()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(cases, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode("utf-8"))
                query = payload.get("query", "").strip()
                if not query:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Empty query"}).encode("utf-8"))
                    return

                # Thực thi ReAct Loop
                trace_logs = run_react_agent(query, provider, mcp_server)
                save_waterfall_trace(trace_logs)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"traces": trace_logs}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


def run_ui_server(port: int = 8080):
    server_address = ("", port)
    httpd = HTTPServer(server_address, ReActAgentWebHandler)
    url = f"http://localhost:{port}"
    print("==========================================================")
    print("✨ KHỞI CHẠY GIAO DIỆN VINFAST HR AGENT STUDIO (PREMIUM)")
    print("==========================================================")
    print(f"🚀 UI Server đang lắng nghe tại: {url}")
    print(f"💡 Hãy mở trình duyệt web và truy cập: {url}")
    print("👉 Nhấn Ctrl + C tại terminal để dừng máy chủ.")
    print("==========================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Máy chủ Web UI đã dừng.")
        httpd.server_close()


if __name__ == "__main__":
    port = 8080
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_ui_server(port)
