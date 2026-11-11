# assemble_cms.py

import json

from pathlib import Path

ROOT = Path(__file__).resolve().parent

with open(ROOT / 'telemetry_html.txt', 'r', encoding='utf-8') as f:

    TELEMETRY_HTML = f.read()

with open(ROOT / 'telemetry_js.txt', 'r', encoding='utf-8') as f:

    TELEMETRY_JS = f.read()

with open(ROOT / 'article_editor_js.txt', 'r', encoding='utf-8') as f:

    ARTICLE_EDITOR_JS = f.read()

def run():

    print("Generating complete unified Academic CMS...")

    

    html = """<!DOCTYPE html>

<html lang="en" data-theme="dark">

<head>

  <meta charset="UTF-8">

  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Academic CMS & Editorial Studio (Secured) | Dr. Zaid Amin</title>

  <link rel="preconnect" href="https://fonts.googleapis.com">

  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,400;1,600&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="assets/css/style.css?v=4.0">

  <link rel="icon" type="image/x-icon" href="/favicon.ico">

  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">

  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">

  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

  <style>

    :root {

      --bg-dark: #020b14;

      --bg-surface: rgba(8, 20, 36, 0.85);

      --bg-card: rgba(10, 24, 42, 0.70);

      --border-subtle: rgba(186, 230, 253, 0.12);

      --border-focus: rgba(56, 189, 248, 0.45);

      --border-gold: rgba(212, 175, 55, 0.45);

      --cyan-accent: #38bdf8;

      --gold-accent: #facc15;

      --text-main: #f1f5f9;

      --text-muted: #94a3b8;

    }

    html {
      overflow-x: clip !important;
    }

    body {
      background: var(--bg-dark);
      color: var(--text-main);
      font-family: var(--font-sans);
      margin: 0;
      padding: 0;
      min-height: 100vh;
      line-height: 1.5;
      overflow-x: clip !important;
    }

    /* 1. Master Security Lock Screen */

    #cms-lock-screen {

      position: fixed;

      inset: 0;

      background: radial-gradient(circle at 50% 30%, #0d2238 0%, #020b14 80%);

      z-index: 999999;

      display: flex;

      align-items: center;

      justify-content: center;

      padding: 24px;

    }

    .lock-vault-card {

      width: 100%;

      max-width: 440px;

      background: rgba(10, 22, 38, 0.90);

      border: 1px solid var(--border-gold);

      border-radius: 20px;

      padding: 40px 32px;

      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.8), 0 0 30px rgba(212, 175, 55, 0.15);

      backdrop-filter: blur(20px);

      text-align: center;

      animation: vaultFadeIn 0.35s ease;

    }

    @keyframes vaultFadeIn {

      from { transform: scale(0.96) translateY(10px); opacity: 0; }

      to { transform: scale(1) translateY(0); opacity: 1; }

    }

    .vault-icon-circle {

      width: 64px;

      height: 64px;

      margin: 0 auto 20px auto;

      border-radius: 50%;

      background: rgba(212, 175, 55, 0.12);

      border: 1px solid rgba(212, 175, 55, 0.4);

      display: flex;

      align-items: center;

      justify-content: center;

      color: var(--gold-accent);

      box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);

    }

    .vault-title {

      font-family: var(--font-cinzel);

      font-size: 1.35rem;

      font-weight: 700;

      letter-spacing: 0.05em;

      color: #ffffff;

      margin-bottom: 6px;

    }

    .vault-subtitle {

      font-size: 0.82rem;

      color: var(--text-muted);

      margin-bottom: 24px;

    }

    .vault-input {

      width: 100%;

      background: rgba(2, 11, 20, 0.85);

      border: 1px solid var(--border-subtle);

      border-radius: 10px;

      padding: 13px 16px;

      color: #ffffff;

      font-size: 0.95rem;

      outline: none;

      transition: all 0.2s ease;

      box-sizing: border-box;

      margin-bottom: 16px;

      text-align: center;

      letter-spacing: 0.1em;

    }

    .vault-input:focus {

      border-color: var(--cyan-accent);

      box-shadow: 0 0 16px rgba(56, 189, 248, 0.25);

    }

    .vault-btn {

      width: 100%;

      background: linear-gradient(135deg, #d4af37, #aa8c2c);

      color: #031220;

      border: none;

      border-radius: 10px;

      padding: 13px;

      font-family: var(--font-cinzel);

      font-size: 0.88rem;

      font-weight: 800;

      letter-spacing: 0.08em;

      text-transform: uppercase;

      cursor: pointer;

      transition: all 0.2s ease;

    }

    .vault-btn:hover {

      background: linear-gradient(135deg, #facc15, #d4af37);

      box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4);

      transform: translateY(-1px);

    }

    .vault-error {

      color: #f87171;

      font-size: 0.82rem;

      margin-top: 14px;

      display: none;

    }

    /* 2. CMS Executive Header (Clean Single-Row Non-Overlapping Grid) */

    .cms-navbar {

      background: rgba(2, 11, 20, 0.95);

      border-bottom: 1px solid var(--border-subtle);

      backdrop-filter: blur(16px);

      -webkit-backdrop-filter: blur(16px);

      position: sticky;

      top: 0;

      z-index: 999;

      height: 52px;

      padding: 0 20px;

      display: flex;

      align-items: center;

      justify-content: space-between;

      gap: 12px;

      flex-wrap: nowrap;

      box-sizing: border-box;

    }

    .cms-brand-group {

      display: flex;

      align-items: center;

      gap: 10px;

      min-width: 0;

      flex: 1 1 auto;

    }

    .cms-brand-title {

      font-family: var(--font-cinzel);

      font-size: 0.95rem;

      font-weight: 700;

      letter-spacing: 0.05em;

      color: #ffffff;

      margin: 0;

      display: flex;

      align-items: center;

      gap: 8px;

      white-space: nowrap;

      flex-shrink: 0;

    }

    .cms-brand-badge {

      font-family: var(--font-sans);

      font-size: 0.60rem;

      letter-spacing: 0.08em;

      text-transform: uppercase;

      background: rgba(212, 175, 55, 0.12);

      color: var(--gold-accent);

      border: 1px solid rgba(212, 175, 55, 0.30);

      padding: 2px 7px;

      border-radius: 999px;

      font-weight: 700;

      white-space: nowrap;

    }

    /* Spotlight Status Chip */

    .cms-spotlight-status {

      display: inline-flex;

      align-items: center;

      gap: 6px;

      background: rgba(10, 24, 42, 0.75);

      border: 1px solid rgba(56, 189, 248, 0.20);

      border-radius: 999px;

      padding: 3px 10px;

      font-size: 0.72rem;

      color: #bae6fd;

      cursor: pointer;

      transition: all 0.2s ease;

      max-width: 320px;

      overflow: hidden;

      white-space: nowrap;

      text-overflow: ellipsis;

      flex-shrink: 1;

    }

    .cms-spotlight-status:hover {

      border-color: var(--gold-accent);

      background: rgba(212, 175, 55, 0.12);

      color: var(--gold-accent);

    }

    .cms-spotlight-source-pill {

      background: rgba(56, 189, 248, 0.18);

      color: var(--cyan-accent);

      padding: 1px 5px;

      border-radius: 4px;

      font-size: 0.60rem;

      font-weight: 700;

      text-transform: uppercase;

      flex-shrink: 0;

    }

    .cms-nav-actions {

      display: flex;

      align-items: center;

      gap: 8px;

      flex-shrink: 0;

    }

    .cms-btn {

      display: inline-flex;

      align-items: center;

      gap: 6px;

      height: 32px;

      padding: 0 12px;

      border-radius: 7px;

      font-family: var(--font-sans);

      font-size: 0.76rem;

      font-weight: 700;

      cursor: pointer;

      border: 1px solid transparent;

      transition: all 0.2s ease;

      white-space: nowrap;

      text-decoration: none;

      box-sizing: border-box;

    }

    .cms-btn-primary {

      background: linear-gradient(135deg, #d4af37, #b8972e);

      color: #031220;

    }

    .cms-btn-primary:hover {

      background: linear-gradient(135deg, #facc15, #d4af37);

      box-shadow: 0 4px 14px rgba(212, 175, 55, 0.35);

      transform: translateY(-1px);

    }

    .cms-btn-cyan {

      background: rgba(56, 189, 248, 0.15);

      color: var(--cyan-accent);

      border-color: rgba(56, 189, 248, 0.35);

    }

    .cms-btn-cyan:hover {

      background: rgba(56, 189, 248, 0.25);

      border-color: var(--cyan-accent);

      box-shadow: 0 4px 14px rgba(56, 189, 248, 0.25);

      transform: translateY(-1px);

    }

    .cms-btn-ghost {

      background: rgba(255, 255, 255, 0.06);

      color: #e2e8f0;

      border-color: var(--border-subtle);

    }

    .cms-btn-ghost:hover {

      background: rgba(255, 255, 255, 0.12);

      border-color: rgba(255, 255, 255, 0.25);

      color: #ffffff;

    }

    .cms-btn-danger {

      background: rgba(239, 68, 68, 0.15);

      color: #f87171;

      border-color: rgba(239, 68, 68, 0.3);

    }

    .cms-btn-danger:hover {

      background: rgba(239, 68, 68, 0.25);

      border-color: #ef4444;

      color: #ffffff;

    }

    
    /* =============================================================
       TELEMETRY & AUDIT STUDIO STYLES (Golden Ratio & Dark Luxury)
       ============================================================= */
    .cms-timeframe-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 7px 16px;
      font-family: var(--font-inter, 'Inter', sans-serif);
      font-size: 0.78rem;
      font-weight: 600;
      letter-spacing: 0.02em;
      color: #94a3b8;
      background: rgba(10, 24, 42, 0.75);
      border: 1px solid rgba(186, 230, 253, 0.16);
      border-radius: 999px;
      cursor: pointer;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      text-decoration: none;
      white-space: nowrap;
      user-select: none;
    }

    .cms-timeframe-btn:hover {
      background: rgba(56, 189, 248, 0.15);
      border-color: rgba(56, 189, 248, 0.45);
      color: #ffffff;
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(56, 189, 248, 0.15);
    }

    .cms-timeframe-btn.active {
      background: linear-gradient(135deg, rgba(212, 175, 55, 0.28) 0%, rgba(212, 175, 55, 0.12) 100%);
      border-color: rgba(212, 175, 55, 0.75);
      color: #fef08a;
      box-shadow: 0 0 16px rgba(212, 175, 55, 0.22);
      font-weight: 700;
    }

    .cms-trace-chip {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 5px 12px;
      font-family: var(--font-inter, 'Inter', sans-serif);
      font-size: 0.75rem;
      font-weight: 600;
      color: #94a3b8;
      background: rgba(10, 24, 42, 0.65);
      border: 1px solid rgba(186, 230, 253, 0.14);
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s ease;
      white-space: nowrap;
      user-select: none;
    }

    .cms-trace-chip:hover {
      background: rgba(56, 189, 248, 0.14);
      border-color: rgba(56, 189, 248, 0.35);
      color: #ffffff;
    }

    .cms-trace-chip.active {
      background: rgba(56, 189, 248, 0.22);
      border-color: #38bdf8;
      color: #38bdf8;
      font-weight: 700;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
    }

    .chart-node {
      transition: r 0.2s cubic-bezier(0.16, 1, 0.3, 1), fill 0.2s ease, stroke 0.2s ease;
    }

    .chart-node:hover {
      r: 7.5;
      fill: #ffffff;
      stroke: #38bdf8;
      stroke-width: 3;
    }

    .chart-node-glow {
      animation: pulseGlow 2.5s infinite ease-in-out;
    }

    @keyframes pulseGlow {
      0%, 100% { r: 6; opacity: 0.25; }
      50% { r: 10; opacity: 0.55; }
    }

    /* 3. Global Module Tabs Bar (Gestalt Segmented Control Dock) */

    .cms-module-tabs {

      display: flex;

      gap: 4px;

      padding: 8px 20px 0 20px;

      border-bottom: 1px solid var(--border-subtle);

      background: rgba(2, 11, 20, 0.90);

      overflow-x: auto;

      scrollbar-width: thin;

      scrollbar-color: rgba(56, 189, 248, 0.20) transparent;

      box-sizing: border-box;

    }

    .cms-module-tabs::-webkit-scrollbar {

      height: 3px;

    }

    .cms-module-tabs::-webkit-scrollbar-thumb {

      background: rgba(56, 189, 248, 0.20);

      border-radius: 999px;

    }

    .cms-module-btn {

      display: inline-flex;

      align-items: center;

      gap: 6px;

      padding: 7px 12px;

      background: rgba(10, 24, 42, 0.50);

      border: 1px solid rgba(186, 230, 253, 0.10);

      border-bottom: none;

      border-radius: 8px 8px 0 0;

      color: var(--text-muted);

      font-family: var(--font-sans);

      font-size: 0.76rem;

      font-weight: 600;

      letter-spacing: 0.01em;

      cursor: pointer;

      transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);

      white-space: nowrap;

      flex-shrink: 0;

    }

    .cms-module-btn:hover {

      color: #ffffff;

      background: rgba(34, 166, 200, 0.10);

      border-color: rgba(56, 189, 248, 0.25);

    }

    .cms-module-btn.active {

      color: #ffffff;

      background: rgba(10, 24, 42, 0.95);

      border-color: rgba(56, 189, 248, 0.35);

      border-bottom: 1px solid rgba(10, 24, 42, 0.95);

      position: relative;

      font-weight: 700;

      box-shadow: 0 -2px 10px rgba(56, 189, 248, 0.10);

    }

    .cms-module-btn.active::after {

      content: '';

      position: absolute;

      top: 0;

      left: 0;

      right: 0;

      height: 2px;

      background: linear-gradient(90deg, #38bdf8, #d4af37);

      border-radius: 8px 8px 0 0;

    }

    .cms-count-chip {

      background: rgba(255, 255, 255, 0.07);

      color: var(--cyan-accent);

      font-family: var(--font-mono), monospace;

      font-size: 0.68rem;

      font-weight: 700;

      padding: 1px 6px;

      border-radius: 999px;

      line-height: 1.2;

    }

    .cms-module-btn.active .cms-count-chip {

      background: rgba(56, 189, 248, 0.18);

      color: #38bdf8;

    }

    /* 4. Main Stage Layout */

    .cms-main {

      padding: 24px;

      max-width: 1440px;

      margin: 0 auto;

    }

    .module-panel {

      display: none;

      animation: panelFade 0.25s ease;

    }

    .module-panel.active {

      display: block;

    }

    @keyframes panelFade {

      from { opacity: 0; transform: translateY(6px); }

      to { opacity: 1; transform: translateY(0); }

    }

    /* Sub-Navigation Pills (Gestalt Proximity & Golden Ratio) */

    .cms-sub-pills-bar {

      display: flex;

      gap: 6px;

      margin-bottom: 18px;

      border-bottom: 1px solid var(--border-subtle);

      padding-bottom: 10px;

      flex-wrap: wrap;

    }

    .cms-sub-pill {

      display: inline-flex;

      align-items: center;

      gap: 6px;

      padding: 5px 12px;

      border-radius: 999px;

      background: rgba(10, 24, 42, 0.50);

      border: 1px solid rgba(186, 230, 253, 0.10);

      color: var(--text-muted);

      font-family: var(--font-sans);

      font-size: 0.74rem;

      font-weight: 600;

      letter-spacing: 0.01em;

      cursor: pointer;

      transition: all 0.18s ease;

      white-space: nowrap;

    }

    .cms-sub-pill:hover {

      color: #ffffff;

      border-color: rgba(56, 189, 248, 0.30);

      background: rgba(56, 189, 248, 0.08);

    }

    .cms-sub-pill.active {

      background: rgba(34, 166, 200, 0.15);

      border-color: rgba(56, 189, 248, 0.40);

      color: #38bdf8;

      font-weight: 700;

      box-shadow: 0 2px 10px rgba(56, 189, 248, 0.15);

    }

    .cms-sub-pill span[id^="count-"] {

      background: rgba(255, 255, 255, 0.07);

      color: var(--cyan-accent);

      font-family: var(--font-mono), monospace;

      font-size: 0.68rem;

      font-weight: 700;

      padding: 1px 6px;

      border-radius: 999px;

    }

    .cms-sub-pill.active span[id^="count-"] {

      background: rgba(56, 189, 248, 0.20);

      color: #38bdf8;

    }

    /* Toolbar / Filter Row */

    .cms-filter-row {

      display: flex;

      justify-content: space-between;

      align-items: center;

      gap: 12px;

      margin-bottom: 18px;

      flex-wrap: wrap;

    }

    .cms-search-box {

      flex: 1 1 320px;

      position: relative;

    }

    .cms-input, .cms-select, .cms-textarea {

      width: 100%;

      background: rgba(8, 20, 36, 0.85);

      border: 1px solid var(--border-subtle);

      border-radius: 8px;

      padding: 10px 14px;

      color: #ffffff;

      font-size: 0.88rem;

      outline: none;

      box-sizing: border-box;

      transition: all 0.2s ease;

    }

    .cms-input:focus, .cms-select:focus, .cms-textarea:focus {

      border-color: var(--cyan-accent);

      box-shadow: 0 0 12px rgba(56, 189, 248, 0.2);

    }

    .cms-select {

      width: auto;

      min-width: 180px;

      cursor: pointer;

    }

    /* Table Cards */

    .cms-table-card {

      background: var(--bg-surface);

      border: 1px solid var(--border-subtle);

      border-radius: 14px;

      overflow: hidden;

      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);

    }

    .cms-table {

      width: 100%;

      border-collapse: collapse;

      text-align: left;

    }

    .cms-table th {

      background: rgba(3, 15, 28, 0.9);

      padding: 14px 18px;

      font-family: var(--font-cinzel);

      font-size: 0.74rem;

      font-weight: 700;

      letter-spacing: 0.08em;

      text-transform: uppercase;

      color: var(--text-muted);

      border-bottom: 1px solid var(--border-subtle);

    }

    .cms-table td {

      padding: 14px 18px;

      font-size: 0.86rem;

      border-bottom: 1px solid rgba(186, 230, 253, 0.06);

      vertical-align: middle;

    }

    .cms-table tr:last-child td {

      border-bottom: none;

    }

    .cms-table tr:hover td {

      background: rgba(34, 166, 200, 0.05);

    }

    .btn-set-spotlight {

      background: rgba(212, 175, 55, 0.12);

      border: 1px solid rgba(212, 175, 55, 0.3);

      color: var(--gold-accent);

      padding: 3px 8px;

      border-radius: 999px;

      font-size: 0.70rem;

      font-weight: 700;

      cursor: pointer;

      transition: all 0.2s ease;

      display: inline-flex;

      align-items: center;

      gap: 4px;

    }

    .btn-set-spotlight:hover {

      background: rgba(212, 175, 55, 0.25);

      border-color: var(--gold-accent);

      box-shadow: 0 0 10px rgba(212, 175, 55, 0.3);

    }

    .spotlight-active-badge {

      background: linear-gradient(135deg, rgba(212, 175, 55, 0.3), rgba(212, 175, 55, 0.15));

      border: 1px solid var(--gold-accent);

      color: #fef08a;

      padding: 3px 9px;

      border-radius: 999px;

      font-size: 0.68rem;

      font-weight: 800;

      letter-spacing: 0.04em;

      text-transform: uppercase;

      box-shadow: 0 0 12px rgba(212, 175, 55, 0.3);

      display: inline-flex;

      align-items: center;

      gap: 4px;

    }

    /* Modal Backdrop & Dialog */

    .cms-modal-backdrop {

      position: fixed;

      inset: 0;

      background: rgba(2, 11, 20, 0.82);

      backdrop-filter: blur(12px);

      z-index: 10000;

      display: none;

      align-items: center;

      justify-content: center;

      padding: 24px;

    }

    .cms-modal-backdrop.active {

      display: flex;

      animation: modalFade 0.22s ease;

    }

    @keyframes modalFade {

      from { opacity: 0; transform: scale(0.97); }

      to { opacity: 1; transform: scale(1); }

    }

    .cms-modal-dialog {

      width: 100%;

      max-width: 760px;

      max-height: 90vh;

      background: rgba(8, 20, 36, 0.95);

      border: 1px solid var(--border-gold);

      border-radius: 18px;

      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.85);

      overflow-y: auto;

      display: flex;

      flex-direction: column;

    }

    .cms-modal-header {

      padding: 18px 24px;

      border-bottom: 1px solid var(--border-subtle);

      display: flex;

      align-items: center;

      justify-content: space-between;

    }

    .cms-modal-title {

      font-family: var(--font-cinzel);

      font-size: 1.2rem;

      font-weight: 700;

      color: #ffffff;

      margin: 0;

    }

    .cms-modal-body {

      padding: 24px;

      flex: 1 1 auto;

      overflow-y: auto;

    }

    .cms-modal-footer {

      padding: 16px 24px;

      border-top: 1px solid var(--border-subtle);

      display: flex;

      justify-content: flex-end;

      gap: 10px;

      background: rgba(3, 14, 26, 0.8);

    }

    .form-group {

      margin-bottom: 18px;

    }

    .form-label {

      display: block;

      font-size: 0.78rem;

      font-weight: 700;

      color: #bae6fd;

      margin-bottom: 6px;

      letter-spacing: 0.02em;

    }

    .form-row-2 {

      display: grid;

      grid-template-columns: 1fr 1fr;

      gap: 16px;

    }

    .form-row-3 {

      display: grid;

      grid-template-columns: 1fr 1fr 1fr;

      gap: 14px;

    }

    /* Article & Essay Focus Studio (Full-Screen Golden Ratio Editor) */

    .article-studio-container {
      width: 100%;
      margin: 0 auto;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Fullscreen Focus Mode */
    .article-studio-container.is-fullscreen {
      position: fixed;
      inset: 0;
      z-index: 2500;
      background: #020b14;
      padding: 20px 32px 32px;
      overflow-y: auto;
      max-width: 100vw;
      height: 100vh;
      border-radius: 0;
      box-sizing: border-box;
    }

    /* Top Sticky Control Bridge (Never scrolls away) */
    .art-sticky-control-bridge {
      position: sticky !important;
      top: 0 !important;
      z-index: 1000 !important;
      background: rgba(2, 9, 18, 0.98) !important;
      backdrop-filter: blur(16px) !important;
      -webkit-backdrop-filter: blur(16px) !important;
      border-bottom: 2px solid #d4af37 !important;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.85), 0 0 18px rgba(212, 175, 55, 0.25) !important;
      transition: box-shadow 0.2s ease;
    }

    .art-studio-topbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 18px;
      border-bottom: 1px solid rgba(56, 189, 248, 0.20);
      flex-wrap: wrap;
      gap: 12px;
    }

    .art-studio-topbar-left {
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
    }

    .art-studio-title-badge {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .art-studio-mode-pill {
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      background: rgba(212, 175, 55, 0.15);
      border: 1px solid rgba(212, 175, 55, 0.45);
      color: #fef08a;
      padding: 3px 10px;
      border-radius: 9999px;
    }

    .art-studio-active-title {
      font-family: var(--font-cinzel), serif;
      font-size: 1.05rem;
      font-weight: 700;
      color: #ffffff;
      max-width: 500px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .art-studio-topbar-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .art-studio-btn-expand {
      background: rgba(14, 28, 48, 0.85);
      border: 1px solid rgba(56, 189, 248, 0.35);
      color: #7dd3fc;
      transition: all 0.2s ease;
    }

    .art-studio-btn-expand:hover {
      background: rgba(56, 189, 248, 0.20);
      border-color: rgba(56, 189, 248, 0.65);
      color: #ffffff;
    }

    /* Metadata Card (Harmonious Golden Ratio Grid) */
    .art-studio-meta-card {
      background: linear-gradient(160deg, rgba(8, 26, 48, 0.85) 0%, rgba(3, 12, 24, 0.95) 100%);
      border: 1px solid rgba(212, 175, 55, 0.28);
      border-radius: 16px;
      padding: 20px 24px;
      margin-bottom: 20px;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
      display: flex;
      flex-direction: column;
      gap: 16px;
      transition: all 0.25s ease;
    }

    .art-title-input {
      font-family: var(--font-cinzel), serif !important;
      font-size: 1.12rem !important;
      font-weight: 700 !important;
      color: #ffffff !important;
      border-color: rgba(212, 175, 55, 0.40) !important;
      background: rgba(3, 10, 20, 0.85) !important;
    }

    .art-title-input:focus {
      border-color: #fef08a !important;
      box-shadow: 0 0 14px rgba(212, 175, 55, 0.35) !important;
    }

    .art-meta-row-1 {
      display: flex;
      gap: 16px;
      align-items: flex-end;
    }

    .art-meta-row-4 {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
    }

    .art-meta-row-2 {
      display: grid;
      grid-template-columns: 1.618fr 1fr;
      gap: 20px;
    }

    .art-thumb-preview-box {
      width: 44px;
      height: 32px;
      border-radius: 4px;
      background: rgba(0, 0, 0, 0.5);
      border: 1px solid rgba(56, 189, 248, 0.3);
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .art-thumb-preview-box img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    /* Content Editor Stage */
    .art-studio-editor-stage {
      background: linear-gradient(175deg, rgba(6, 18, 34, 0.95) 0%, rgba(2, 9, 18, 0.98) 100%);
      border: 1.5px solid rgba(56, 189, 248, 0.35);
      border-radius: 18px;
      overflow: hidden;
      box-shadow: 0 16px 44px rgba(0, 0, 0, 0.65), 0 0 24px rgba(56, 189, 248, 0.12);
      display: flex;
      flex-direction: column;
    }

    /* Advanced Rich Formatting Toolbar */
    .art-advanced-toolbar {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 18px;
      background: linear-gradient(180deg, rgba(6, 18, 34, 0.98) 0%, rgba(3, 11, 22, 0.98) 100%);
      border-bottom: none;
      flex-wrap: wrap;
    }

    .art-toolbar-group {
      display: flex;
      align-items: center;
      gap: 4px;
      background: rgba(2, 8, 16, 0.65);
      border: 1px solid rgba(56, 189, 248, 0.18);
      border-radius: 8px;
      padding: 3px 6px;
      position: relative;
    }

    .art-toolbar-group-label {
      font-size: 0.55rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      color: #64748b;
      margin-right: 4px;
      user-select: none;
    }

    .art-tool-btn {
      background: transparent;
      border: 1px solid transparent;
      color: #cbd5e1;
      padding: 4px 7px;
      border-radius: 5px;
      font-size: 0.78rem;
      cursor: pointer;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transition: all 0.15s ease;
      line-height: 1;
    }

    .art-tool-btn:hover {
      background: rgba(56, 189, 248, 0.18);
      color: #38bdf8;
      border-color: rgba(56, 189, 248, 0.40);
      transform: translateY(-1px);
    }

    .art-tool-btn:active {
      transform: translateY(1px);
    }

    .art-mode-switch {
      display: flex;
      gap: 4px;
      background: rgba(3, 10, 20, 0.85);
      padding: 2px;
      border-radius: 6px;
      border: 1px solid rgba(212, 175, 55, 0.35);
    }

    /* Writing Desk Wrapper (Gestalt Figure-Ground Elevation) */
    .art-visual-wrapper {
      position: relative;
      background: radial-gradient(circle at 50% 12%, rgba(10, 32, 60, 0.45) 0%, rgba(1, 6, 14, 0.98) 100%), #01060e;
      padding: 32px 24px 64px 24px;
      overflow-y: visible !important;
      min-height: 600px;
      max-height: none !important;
      border-radius: 0 0 14px 14px;
    }

    .is-fullscreen .art-visual-wrapper {
      min-height: 600px;
      max-height: none !important;
      overflow-y: visible !important;
      padding: 36px 32px 100px;
    }

    /* Manuscript Canvas (Golden Ratio 860px Column Measure) */
    .art-visual-canvas {
      max-width: 860px;
      margin: 0 auto;
      min-height: 520px;
      padding: 46px 56px;
      background: rgba(3, 11, 22, 0.98);
      border: 1px solid rgba(56, 189, 248, 0.22);
      border-radius: 12px;
      box-shadow: 0 16px 45px rgba(0, 0, 0, 0.65), 0 0 0 1px rgba(212, 175, 55, 0.14);
      color: #e2e8f0;
      font-family: 'Inter', system-ui, sans-serif;
      font-size: 1.05rem;
      line-height: 1.82;
      outline: none;
      word-break: break-word;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .art-visual-canvas:focus {
      border-color: rgba(212, 175, 55, 0.55);
      box-shadow: 0 18px 50px rgba(0, 0, 0, 0.75), 0 0 0 1px rgba(212, 175, 55, 0.45), 0 0 24px rgba(212, 175, 55, 0.18);
    }

    /* Constrained Golden Ratio Images in Editor (Never chaotic or oversized) */
    .art-visual-canvas img {
      max-width: 100% !important;
      max-height: 420px !important; /* Cap to Golden Ratio height so it never overwhelms */
      width: auto !important;
      height: auto !important;
      object-fit: contain !important;
      display: block !important;
      margin: 22px auto !important;
      border-radius: 10px !important;
      border: 1px solid rgba(56, 189, 248, 0.28) !important;
      box-shadow: 0 10px 32px rgba(0, 0, 0, 0.55) !important;
      background: rgba(2, 9, 18, 0.8) !important;
      cursor: pointer !important;
      transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    .art-visual-canvas img:hover {
      border-color: #fce09b !important;
      box-shadow: 0 14px 40px rgba(212, 175, 55, 0.25) !important;
      transform: translateY(-2px);
    }

    .art-visual-canvas img.art-img-selected {
      outline: 2px solid #d4af37 !important;
      outline-offset: 4px !important;
      border-color: #fce09b !important;
      box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.25), 0 16px 44px rgba(0, 0, 0, 0.7) !important;
    }

    .art-visual-canvas figure {
      margin: 28px auto !important;
      max-width: 100% !important;
      text-align: center !important;
      position: relative !important;
      clear: both !important;
    }

    .art-visual-canvas figcaption,
    .art-visual-canvas .figure-caption,
    .art-visual-canvas p.figure-caption {
      font-family: 'Cormorant Garamond', Georgia, serif !important;
      font-size: 0.88rem !important;
      font-style: italic !important;
      color: #94a3b8 !important;
      margin: 8px auto 16px auto !important;
      line-height: 1.5 !important;
      display: block !important;
      letter-spacing: 0.02em !important;
      text-align: center !important;
    }

    /* Figure size presets */
    .art-visual-canvas figure.fig-compact,
    .art-visual-canvas img.fig-compact {
      max-width: 60% !important;
      max-height: 290px !important;
    }

    .art-visual-canvas figure.fig-standard,
    .art-visual-canvas img.fig-standard {
      max-width: 82% !important;
      max-height: 400px !important;
    }

    .art-visual-canvas figure.fig-full,
    .art-visual-canvas img.fig-full {
      max-width: 100% !important;
      max-height: 500px !important;
    }

    .art-visual-canvas figure.fig-left,
    .art-visual-canvas img.fig-left {
      float: left !important;
      max-width: 48% !important;
      margin: 10px 24px 18px 0 !important;
      clear: left !important;
    }

    .art-visual-canvas figure.fig-right,
    .art-visual-canvas img.fig-right {
      float: right !important;
      max-width: 48% !important;
      margin: 10px 0 18px 24px !important;
      clear: right !important;
    }

    /* Floating Image Format Bar */
    .art-img-floating-toolbar {
      position: fixed;
      display: none;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      background: rgba(3, 14, 28, 0.96);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid rgba(212, 175, 55, 0.5);
      border-radius: 9999px;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.7), 0 0 16px rgba(212, 175, 55, 0.25);
      z-index: 60;
      transform: translateX(-50%);
      white-space: nowrap;
      transition: opacity 0.2s ease;
    }

    .art-img-floating-toolbar.active {
      display: flex;
    }

    .art-img-pill-btn {
      background: rgba(255, 255, 255, 0.07);
      border: 1px solid rgba(56, 189, 248, 0.25);
      color: #cbd5e1;
      padding: 3px 9px;
      border-radius: 9999px;
      font-size: 0.72rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
      line-height: 1.2;
    }

    .art-img-pill-btn:hover {
      background: rgba(212, 175, 55, 0.22);
      color: #fef08a;
      border-color: rgba(212, 175, 55, 0.55);
    }

    .art-img-pill-btn.danger {
      color: #f87171;
      border-color: rgba(239, 68, 68, 0.35);
    }
    .art-img-pill-btn.danger:hover {
      background: rgba(239, 68, 68, 0.25);
      color: #ffffff;
      border-color: #ef4444;
    }

    /* Color Swatch & Native Color Picker (Gestalt Proximity & Visual Feedback) */
    .art-color-picker-wrap {
      position: relative;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 22px;
      height: 22px;
      margin-right: 4px;
      flex-shrink: 0;
    }

    .art-tool-color-native {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      opacity: 0;
      cursor: pointer;
      z-index: 2;
    }

    .art-color-swatch-badge {
      display: block;
      width: 18px;
      height: 18px;
      border-radius: 4px;
      border: 1.5px solid rgba(212, 175, 55, 0.7);
      box-shadow: 0 0 6px rgba(0, 0, 0, 0.75);
      cursor: pointer;
      transition: transform 0.16s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.16s ease, box-shadow 0.16s ease;
    }

    .art-color-swatch-badge:hover {
      transform: scale(1.18);
      border-color: #fef08a;
      box-shadow: 0 0 10px rgba(212, 175, 55, 0.9);
    }

    .art-visual-canvas mark {
      border-radius: 4px;
      padding: 2px 6px;
      box-decoration-break: clone;
      -webkit-box-decoration-break: clone;
    }

    /* Toolbar Select Dropdowns */
    .art-tool-select {
      background: rgba(6, 20, 36, 0.92);
      border: 1px solid rgba(56, 189, 248, 0.32);
      color: #f1f5f9;
      font-size: 0.78rem;
      font-weight: 600;
      padding: 4px 8px;
      border-radius: 6px;
      outline: none;
      cursor: pointer;
      transition: all 0.2s ease;
      line-height: 1.2;
      height: 28px;
    }

    .art-tool-select:hover, .art-tool-select:focus {
      border-color: #d4af37;
      box-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
      background: rgba(8, 28, 50, 0.98);
      color: #ffffff;
    }

    .art-tool-select option {
      background: #041220;
      color: #e2e8f0;
      padding: 6px 10px;
    }

    .art-tool-btn-highlight {
      background: rgba(212, 175, 55, 0.15) !important;
      border-color: rgba(212, 175, 55, 0.4) !important;
      color: #fce09b !important;
    }
    .art-tool-btn-highlight:hover {
      background: rgba(212, 175, 55, 0.3) !important;
      border-color: #fef08a !important;
      color: #ffffff !important;
      box-shadow: 0 0 10px rgba(212, 175, 55, 0.4);
    }
    .art-tool-btn-clear {
      color: #cbd5e1;
      border-color: rgba(255, 255, 255, 0.14);
    }
    .art-tool-btn-clear:hover {
      background: rgba(239, 68, 68, 0.18) !important;
      color: #fca5a5 !important;
      border-color: rgba(239, 68, 68, 0.45) !important;
    }

    /* Inside Canvas Editorial Styling */
    .art-visual-canvas h1,
    .art-visual-canvas h2,
    .art-visual-canvas h3 {
      font-family: var(--font-cinzel), serif;
      color: #ffffff;
      line-height: 1.35;
      margin: 1.6em 0 0.6em;
      letter-spacing: 0.02em;
    }

    .art-visual-canvas h2 {
      font-size: 1.55rem;
      border-bottom: 1px solid rgba(212, 175, 55, 0.25);
      padding-bottom: 8px;
    }

    .art-visual-canvas h3 {
      font-size: 1.25rem;
      color: #fef08a;
    }

    .art-visual-canvas p {
      margin-bottom: 1.3em;
    }

    .art-visual-canvas p.lead-para {
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 1.32rem;
      line-height: 1.85;
      color: #fce09b;
      font-style: italic;
      border-left: 3px solid #d4af37;
      padding-left: 18px;
      margin: 1.8em 0;
    }

    .art-visual-canvas blockquote {
      border-left: 3px solid #d4af37;
      background: rgba(212, 175, 55, 0.06);
      margin: 1.8em 0;
      padding: 18px 24px;
      border-radius: 0 10px 10px 0;
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 1.18rem;
      font-style: italic;
      color: #f8fafc;
      line-height: 1.8;
    }

    .art-visual-canvas .callout-box {
      background: linear-gradient(135deg, rgba(8, 28, 50, 0.85) 0%, rgba(3, 14, 28, 0.95) 100%);
      border: 1px solid rgba(56, 189, 248, 0.35);
      border-left: 4px solid #38bdf8;
      border-radius: 8px;
      padding: 16px 20px;
      margin: 1.8em 0;
      color: #bae6fd;
      font-size: 0.95rem;
      line-height: 1.7;
    }

    .art-visual-canvas .callout-warning {
      border-left-color: #f59e0b;
      background: linear-gradient(135deg, rgba(38, 24, 8, 0.85) 0%, rgba(20, 12, 3, 0.95) 100%);
      border-color: rgba(245, 158, 11, 0.35);
      color: #fef3c7;
    }

    .art-visual-canvas mark.scholar-highlight {
      background: rgba(212, 175, 55, 0.25);
      color: #fef08a;
      padding: 2px 5px;
      border-radius: 3px;
    }

    .art-visual-canvas hr.section-divider {
      border: none;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.6) 50%, transparent);
      margin: 2.4em 0;
    }

    .art-visual-canvas table.scholar-table {
      width: 100%;
      border-collapse: collapse;
      margin: 1.8em 0;
      font-size: 0.92rem;
    }

    .art-visual-canvas table.scholar-table th,
    .art-visual-canvas table.scholar-table td {
      border: 1px solid rgba(56, 189, 248, 0.25);
      padding: 10px 14px;
      text-align: left;
    }

    .art-visual-canvas table.scholar-table th {
      background: rgba(8, 28, 50, 0.9);
      color: #fce09b;
      font-family: var(--font-cinzel), serif;
      font-size: 0.85rem;
    }

    .art-visual-canvas table.scholar-table tr:nth-child(even) td {
      background: rgba(4, 16, 30, 0.4);
    }

    .art-visual-canvas .latex-math-block {
      background: #030d1a;
      border: 1px solid rgba(212, 175, 55, 0.35);
      border-radius: 8px;
      padding: 14px 20px;
      margin: 1.6em 0;
      font-family: 'JetBrains Mono', monospace;
      color: #fef08a;
      text-align: center;
      font-size: 1.05rem;
    }

    .art-visual-canvas .inline-latex {
      font-family: 'JetBrains Mono', monospace;
      color: #fef08a;
      background: rgba(212, 175, 55, 0.12);
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid rgba(212, 175, 55, 0.25);
    }

    .art-visual-canvas pre.code-block {
      background: #020810 !important;
      border: 1px solid rgba(56, 189, 248, 0.25) !important;
      border-radius: 8px !important;
      padding: 14px 18px !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 0.88rem !important;
      color: #bae6fd !important;
      overflow-x: auto !important;
      margin: 1.6rem 0 !important;
      line-height: 1.6 !important;
    }

    /* Raw HTML Canvas */
    .art-code-canvas {
      min-height: 520px;
      max-height: 720px;
      padding: 24px;
      background: #020810;
      color: #38bdf8;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.88rem;
      line-height: 1.7;
      border: none;
      outline: none;
      resize: vertical;
      width: 100%;
      box-sizing: border-box;
    }

    .is-fullscreen .art-code-canvas {
      min-height: calc(100vh - 280px);
      max-height: calc(100vh - 280px);
    }

    /* Status Bar */
    .art-editor-statusbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 20px;
      background: rgba(3, 10, 20, 0.95);
      border-top: 1px solid rgba(56, 189, 248, 0.18);
      font-size: 0.78rem;
      color: #94a3b8;
    }

    .art-status-metrics {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .art-status-sep {
      color: #475569;
    }

    .art-status-pulse {
      display: inline-block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
      margin-right: 6px;
    }

    @media (max-width: 900px) {
      .art-meta-row-1 { flex-direction: column; }
      .art-meta-row-1 .art-cat-group { width: 100% !important; }
      .art-meta-row-4 { grid-template-columns: 1fr 1fr; }
      .art-meta-row-2 { grid-template-columns: 1fr; }
    }

    .preview-tab-pill {

      background: transparent;

      border: none;

      color: #94a3b8;

      font-size: 0.78rem;

      font-weight: 700;

      cursor: pointer;

      padding: 4px 10px;

      border-radius: 6px;

    }

    .preview-tab-pill.active {

      background: rgba(56, 189, 248, 0.2);

      color: #ffffff;

    }

    /* Live Card Previews in Modals */

    .live-preview-box {

      margin-top: 18px;

      padding: 16px;

      background: rgba(2, 11, 20, 0.6);

      border: 1px dashed rgba(56, 189, 248, 0.25);

      border-radius: 12px;

    }

    /* Grid of Cards for Pillars & Supervision */

    .cms-cards-grid {

      display: grid;

      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));

      gap: 18px;

    }

    .cms-feature-card {

      background: rgba(8, 20, 36, 0.85);

      border: 1px solid var(--border-subtle);

      border-radius: 14px;

      padding: 20px;

      position: relative;

      transition: all 0.2s ease;

    }

    .cms-feature-card:hover {

      border-color: var(--border-focus);

      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);

    }

    /* Toast Notification */

    #cms-toast {

      position: fixed;

      bottom: 24px;

      right: 24px;

      background: #020b14;

      border: 1px solid var(--border-gold);

      color: #ffffff;

      padding: 12px 20px;

      border-radius: 10px;

      font-size: 0.86rem;

      font-weight: 600;

      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8), 0 0 20px rgba(212, 175, 55, 0.2);

      display: none;

      z-index: 9999999;

      animation: toastIn 0.3s ease;

    }

    @keyframes toastIn {

      from { transform: translateY(20px); opacity: 0; }

      to { transform: translateY(0); opacity: 1; }

    }


    /* Universal Golden Scroll-To-Top Button for CMS (All Modules & Article Editor) */
    .scroll-to-top-btn {
      position: fixed;
      bottom: 28px;
      right: 28px;
      width: 46px;
      height: 46px;
      border-radius: 50%;
      background: linear-gradient(135deg, rgba(14, 28, 48, 0.95) 0%, rgba(4, 11, 22, 0.98) 100%);
      border: 2px solid #d4af37;
      color: #fce09b;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      z-index: 9999;
      box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.75), 0 0 16px rgba(212, 175, 55, 0.35);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      opacity: 0;
      pointer-events: none;
      transform: translateY(14px) scale(0.92);
      transition: opacity 0.28s cubic-bezier(0.16, 1, 0.3, 1),
                  transform 0.28s cubic-bezier(0.16, 1, 0.3, 1),
                  background 0.2s ease,
                  border-color 0.2s ease,
                  box-shadow 0.2s ease,
                  color 0.2s ease;
    }

    .scroll-to-top-btn.visible {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0) scale(1);
    }

    .scroll-to-top-btn:hover {
      background: linear-gradient(135deg, rgba(22, 46, 78, 0.98) 0%, rgba(8, 20, 38, 0.98) 100%);
      border-color: #fef08a;
      color: #ffffff;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.85), 0 0 24px rgba(212, 175, 55, 0.6);
      transform: translateY(-2px) scale(1.06);
    }

    .scroll-to-top-btn:active {
      transform: translateY(1px) scale(0.98);
    }

    @media (max-width: 768px) {
      .scroll-to-top-btn {
        bottom: 20px;
        right: 20px;
        width: 42px;
        height: 42px;
      }
    }
  </style>

</head>

<body>

  <!-- =============================================================

       1. IMPENETRABLE MASTER SECURITY VAULT LOCK SCREEN

       ============================================================= -->

  <div id="cms-lock-screen">

    <div class="lock-vault-card">

      <div class="vault-icon-circle">

        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">

          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>

          <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>

        </svg>

      </div>

      <div class="vault-title">SECURED CMS STUDIO</div>

      <div class="vault-subtitle">dr. zaid amin &bull; institutional editorial gateway</div>

      <form onsubmit="handleAdminLogin(event)">

        <input type="password" id="vault-key-input" class="vault-input" placeholder="Enter Master Admin Passkey" autofocus autocomplete="current-password">

        <button type="submit" class="vault-btn">Unlock Studio &rarr;</button>

        <div id="vault-error-msg" class="vault-error">Invalid passkey. Unauthorized access logged.</div>

      </form>

    </div>

  </div>

  <!-- Toast Container -->

  <div id="cms-toast">Notification message</div>

  <!-- =============================================================

       2. CMS EXECUTIVE NAVBAR

       ============================================================= -->

  <header class="cms-navbar">

    <div class="cms-brand-group">

      <h1 class="cms-brand-title">

        <span>DR. ZAID AMIN</span>

        <span class="cms-brand-badge">CMS STUDIO</span>

      </h1>

      

      <!-- Live Spotlight Indicator -->

      <div class="cms-spotlight-status" id="header-spotlight-widget" onclick="switchModule('profile')" title="Click to manage Homepage Spotlight">

        <span>★ SPOTLIGHT:</span>

        <span id="spotlight-title-display" style="font-weight: 700; color: #ffffff;">Loading active spotlight...</span>

        <span class="cms-spotlight-source-pill" id="spotlight-source-display">PUBLICATION</span>

      </div>

    </div>

    <div class="cms-nav-actions">

      <button class="cms-btn cms-btn-ghost" onclick="switchModule('telemetry')" title="View Edge Telemetry & Real-Time Visitor Metrics">

        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>

        Audit Telemetry

      </button>

      <button class="cms-btn cms-btn-cyan" id="btn-deploy-live" onclick="deployLiveSite()" title="Compile website via build.py and sync to GitHub Pages & zaidamin.org">

        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 2L11 13"></path><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>

        Publish Live

      </button>

      <button class="cms-btn cms-btn-ghost" onclick="lockStudio()" title="Lock CMS Studio">

        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>

        Lock

      </button>

    </div>

  </header>

  <!-- =============================================================

       3. GLOBAL MODULE NAVIGATION TABS (All 7 Website Areas)

       ============================================================= -->

  <nav class="cms-module-tabs">

    <button class="cms-module-btn active" id="btn-mod-articles" onclick="switchModule('articles')">

      <span>📑 Activity &amp; Projects</span> <span id="count-articles" class="cms-count-chip">80</span>

    </button>

    <button class="cms-module-btn" id="btn-mod-pubs" onclick="switchModule('pubs')">

      <span>📚 Publications</span> <span id="count-pubs" class="cms-count-chip">24</span>

    </button>

    <button class="cms-module-btn" id="btn-mod-talks" onclick="switchModule('talks')">

      <span>🎤 Media &amp; Talks</span> <span id="count-talks" class="cms-count-chip">19</span>

    </button>

    <button class="cms-module-btn" id="btn-mod-cv" onclick="switchModule('cv')">

      <span>🏆 Achievements &amp; CV</span> <span id="count-cv" class="cms-count-chip">46</span>

    </button>

    <button class="cms-module-btn" id="btn-mod-supervision" onclick="switchModule('supervision')">

      <span>🎓 Supervision</span> <span id="count-supervision" class="cms-count-chip">4</span>

    </button>

    <button class="cms-module-btn" id="btn-mod-profile" onclick="switchModule('profile')">

      <span>🏛️ Site Profile</span>

    </button>

    <button class="cms-module-btn" id="btn-mod-telemetry" onclick="switchModule('telemetry')">

      <span>🛡️ Audit &amp; Analytics</span>

    </button>

  </nav>

  <!-- =============================================================

       4. MAIN CONTENT STAGE

       ============================================================= -->

  <main class="cms-main">

    <!-- =============================================================

         PANEL 1: ACTIVITY & PROJECT (Articles & Essays + Research Pillars)

         ============================================================= -->

    <section class="module-panel active" id="panel-articles">

      

      <!-- Sub-tabs: Articles & Essays vs Research Pillars & Grants -->

      <div class="cms-sub-pills-bar">

        <button class="cms-sub-pill active" id="subtab-btn-art-essays" onclick="switchArticlesSubTab('essays')">

          📑 Scholarly Articles &amp; Essays <span id="count-art-essays">80</span>

        </button>

        <button class="cms-sub-pill" id="subtab-btn-art-pillars" onclick="switchArticlesSubTab('pillars')">

          🏛️ Research Pillars &amp; Active Grants <span id="count-art-pillars">5</span>

        </button>

      </div>

      <!-- Section 1A: Articles List View -->

      <div id="articles-subpane-essays">

        <div id="articles-list-view">

          <div class="cms-filter-row">

            <div class="cms-search-box">

              <input type="text" id="articles-search-input" class="cms-input" placeholder="Search across 80+ articles by title, topic, or keyword..." oninput="filterArticlesTable()">

            </div>

            <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">

              <select id="articles-cat-filter" class="cms-select" onchange="filterArticlesTable()">

                <option value="">All Categories</option>

                <option value="AI & Cybernetics">AI &amp; Cybernetics</option>

                <option value="Essays & Perspectives">Essays &amp; Perspectives</option>

                <option value="Pedagogy & Education">Pedagogy &amp; Education</option>

                <option value="Digital Ethics & HCI">Digital Ethics &amp; HCI</option>

                <option value="Philosophy & Society">Philosophy &amp; Society</option>

                <option value="Epistemic & Media">Epistemic &amp; Media</option>

              </select>

              <button class="cms-btn cms-btn-primary" onclick="openNewArticleEditor()">+ New Article</button>

              <button class="cms-btn cms-btn-ghost" onclick="downloadJSON('articles.json', articlesData)">📥 Backup Articles JSON</button>

            </div>

          </div>

          <div class="cms-table-card">

            <table class="cms-table">

              <thead>

                <tr>

                  <th style="width: 44px;">#</th>

                  <th>Article Title</th>

                  <th>Category</th>

                  <th>Date</th>

                  <th>Read Time</th>

                  <th style="text-align: right;">Actions</th>

                </tr>

              </thead>

              <tbody id="articles-tbody"></tbody>

            </table>

          </div>

        </div>

        <!-- Section 1B: Optimized Full-Screen Article Content Editor (Golden Ratio & Advanced Scholarly Features) -->

        <div id="articles-editor-view" class="article-studio-container" style="display: none;">

          <!-- Sticky Control Header Bridge (Always Pinned at Top When Scrolling) -->
          <div class="art-sticky-control-bridge" id="art-sticky-control-bridge">
            <div class="art-studio-topbar">
            <div class="art-studio-topbar-left">
              <button type="button" class="cms-btn cms-btn-ghost art-studio-btn-back" onclick="closeArticleEditor()" title="Return to articles list">
                &larr; Back to Articles List
              </button>
              <div class="art-studio-title-badge">
                <span class="art-studio-mode-pill" id="art-studio-mode-indicator">✏️ Article Editor</span>
                <span class="art-studio-active-title" id="art-studio-header-title">Create / Edit Scholarly Essay</span>
                <span class="art-studio-save-status" id="art-studio-save-status" style="display:none; margin-left: 10px; font-size: 0.72rem; color: #38bdf8; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.35); padding: 3px 10px; border-radius: 9999px; font-weight: 600; letter-spacing: 0.03em;">✓ Saved &amp; Live</span>
              </div>
            </div>
            <div class="art-studio-topbar-actions">
              <!-- Fullscreen Toggle -->
              <button type="button" class="cms-btn cms-btn-ghost art-studio-btn-expand" id="btn-article-fullscreen" onclick="toggleArticleFullscreen()" title="Toggle Fullscreen Focus Mode (Esc to exit)">
                <span id="article-fullscreen-icon">⛶</span> <span id="article-fullscreen-label">Fullscreen</span>
              </button>
              <!-- Metadata Drawer Toggle -->
              <button type="button" class="cms-btn cms-btn-ghost" id="btn-toggle-art-meta" onclick="toggleArticleMetadataDrawer()" title="Expand or collapse metadata card">
                ⚙️ Metadata
              </button>
              <!-- Primary: Save & Deploy Live (DOES NOT CLOSE EDITOR SESSION) -->
              <button type="button" class="cms-btn cms-btn-primary" id="btn-art-save-deploy" onclick="saveArticleAction({ deploy: true, close: false })" title="Save changes, rebuild website, and deploy live to zaidamin.org (editor session stays open)">
                🚀 Save &amp; Deploy Live
              </button>
              <!-- Secondary: Save Locally (DOES NOT CLOSE EDITOR SESSION) -->
              <button type="button" class="cms-btn cms-btn-cyan" id="btn-art-save-local" onclick="saveArticleAction({ deploy: false, close: false })" title="Save changes locally &amp; rebuild HTML without pushing to GitHub (editor session stays open)">
                💾 Save (Local Only)
              </button>
              <!-- Save & Exit -->
              <button type="button" class="cms-btn cms-btn-ghost" id="btn-art-save-close" onclick="saveArticleAction({ deploy: true, close: true })" title="Save, deploy live, and return to articles list">
                ✓ Save &amp; Exit
              </button>
            </div>
          </div>

          <!-- Harmonized Metadata Card (Golden Ratio Proportions & Proximity) -->

            <div class="art-advanced-toolbar" id="art-visual-toolbar">
              
              <!-- Font Family & Typography Group -->
              <div class="art-toolbar-group">
                <span class="art-toolbar-group-label">FONT TYPE</span>
                <select id="art-tool-font" class="art-tool-select" onchange="applyArticleFontFamily(this.value)" title="Choose Typography Font Family">
                  <option value="">Font: Inter (Academic Sans)</option>
                  <option value="Inter, system-ui, sans-serif">Inter (Clean Modern Sans)</option>
                  <option value="'Cormorant Garamond', Georgia, serif">Cormorant Garamond (Editorial Serif)</option>
                  <option value="'Cinzel', Georgia, serif">Cinzel (Classical Display Serif)</option>
                  <option value="'Newsreader', Georgia, serif">Newsreader (Academic Literature)</option>
                  <option value="Georgia, serif">Georgia (Warm Editorial Serif)</option>
                  <option value="'Merriweather', Georgia, serif">Merriweather (Attentive Reading)</option>
                  <option value="'JetBrains Mono', monospace">JetBrains Mono (Code &amp; Systems)</option>
                </select>
              </div>

              <!-- Hierarchy / Scholarly Presets Group -->
              <div class="art-toolbar-group">
                <span class="art-toolbar-group-label">FORMAT</span>
                <select id="art-tool-heading" class="art-tool-select" onchange="applyArticleHeading(this.value)" title="Scholarly Format Preset &amp; Typography Hierarchy">
                  <option value="" disabled selected>✦ Format Preset...</option>
                  <optgroup label="── 1. Reading &amp; Captions ──">
                    <option value="p">1. ¶ Normal Text (Standard Body)</option>
                    <option value="caption">2. 💬 Figure &amp; Table Caption (Italic Slate 0.85rem)</option>
                    <option value="lead">★ Lead Intro Paragraph (Editorial Serif 1.25rem)</option>
                    <option value="detail">📌 Footnote / Scholarly Observation (0.82rem)</option>
                  </optgroup>
                  <optgroup label="── 2. Headings &amp; Hierarchy ──">
                    <option value="h2">3. H2 Header Title (Section - Cinzel Gold 1.75rem)</option>
                    <option value="h3">4. H3 Sub Header Title (Subsection - Soft Gold 1.35rem)</option>
                    <option value="h4">H4 Minor Heading (Inter Bold Cyan 1.15rem)</option>
                  </optgroup>
                  <optgroup label="── 3. Image &amp; Media Wrapping ──">
                    <option value="wrap_left">5. ⫷ Image Float Left (Text Wraps Right)</option>
                    <option value="wrap_right">5. ⫸ Image Float Right (Text Wraps Left)</option>
                    <option value="wrap_center">5. ≡ Image Centered (Clear Float)</option>
                    <option value="wrap_full">5. ⬛ Image Full Column Width (100%)</option>
                  </optgroup>
                  <optgroup label="── 4. Formulas, Code &amp; Data ──">
                    <option value="code_block">6. ⌨️ Code Block (JetBrains Mono)</option>
                    <option value="code_inline">6. &lt;/&gt; Inline Code Token</option>
                    <option value="math_block">7. ∑ Equation Style (LaTeX Display Block)</option>
                    <option value="math_inline">7. √ Inline Math Equation</option>
                    <option value="table">📊 Scholarly Matrix Table</option>
                  </optgroup>
                  <optgroup label="── 5. Scholarly Quotes &amp; Callouts ──">
                    <option value="quote">8. ❝ Quote (Scholarly Epigraph / Axiom)</option>
                    <option value="callout">9. 💡 Key Finding Callout Box</option>
                    <option value="warning">9. ⚠️ Policy &amp; Operational Alert Box</option>
                    <option value="divider">― Golden Ratio Section Divider</option>
                  </optgroup>
                </select>
              </div>

              <!-- Typographic Scale / Size Group -->
              <div class="art-toolbar-group">
                <span class="art-toolbar-group-label">SIZE</span>
                <select id="art-tool-size" class="art-tool-select" onchange="applyArticleFontSize(this.value)" title="Choose Font Size Scale">
                  <option value="">Size: Normal (1.05rem)</option>
                  <option value="0.85rem">Footnote (0.85rem / 14px)</option>
                  <option value="0.95rem">Compact (0.95rem / 15px)</option>
                  <option value="1.05rem">Regular (1.05rem / 17px)</option>
                  <option value="1.18rem">Medium (1.18rem / 19px)</option>
                  <option value="1.32rem">Large Lead (1.32rem / 21px)</option>
                  <option value="1.618rem">Golden Title (1.618rem / 26px)</option>
                </select>
              </div>

              <!-- Text Font Color Group (Golden Ratio & Academic Palette) -->
              <div class="art-toolbar-group" title="Typography Font Color">
                <span class="art-toolbar-group-label">COLOR</span>
                <div class="art-color-picker-wrap">
                  <input type="color" id="art-tool-color-native" class="art-tool-color-native" value="#fce09b" oninput="applyArticleFontColor(this.value)" title="Choose Custom Hex Color">
                  <label for="art-tool-color-native" class="art-color-swatch-badge" id="art-color-swatch-indicator" style="background-color: #fce09b;" title="Custom Font Color Swatch"></label>
                </div>
                <select id="art-tool-color" class="art-tool-select" onchange="applyArticleFontColor(this.value)" title="Choose Typography Font Color">
                  <option value="">Color: Default</option>
                  <option value="#fce09b" style="color:#fce09b; background:#040d18;">★ Luxe Gold (#fce09b)</option>
                  <option value="#facc15" style="color:#facc15; background:#040d18;">✦ Bright Gold (#facc15)</option>
                  <option value="#d4af37" style="color:#d4af37; background:#040d18;">⚜ Antique Gold (#d4af37)</option>
                  <option value="#ffffff" style="color:#ffffff; background:#040d18;">⚪ Pure White (#ffffff)</option>
                  <option value="#f1f5f9" style="color:#f1f5f9; background:#040d18;">◻ Soft Slate (#f1f5f9)</option>
                  <option value="#94a3b8" style="color:#94a3b8; background:#040d18;">◽ Muted Silver (#94a3b8)</option>
                  <option value="#38bdf8" style="color:#38bdf8; background:#040d18;">💎 Academic Cyan (#38bdf8)</option>
                  <option value="#34d399" style="color:#34d399; background:#040d18;">🍃 Emerald Green (#34d399)</option>
                  <option value="#f87171" style="color:#f87171; background:#040d18;">🌹 Coral Crimson (#f87171)</option>
                  <option value="#c084fc" style="color:#c084fc; background:#040d18;">🔮 Royal Amethyst (#c084fc)</option>
                  <option value="#fb923c" style="color:#fb923c; background:#040d18;">🍂 Amber Ochre (#fb923c)</option>
                  <option value="inherit" style="color:#cbd5e1; background:#040d18;">↺ Reset Color</option>
                </select>
              </div>

              <!-- Color Highlight Group (Academic Highlighter Markers) -->
              <div class="art-toolbar-group" title="Text & Block Highlight Marker">
                <span class="art-toolbar-group-label">HIGHLIGHT</span>
                <div class="art-color-picker-wrap">
                  <input type="color" id="art-tool-highlight-native" class="art-tool-color-native" value="#d4af37" oninput="applyArticleHighlight(this.value)" title="Choose Custom Highlight Color">
                  <label for="art-tool-highlight-native" class="art-color-swatch-badge" id="art-highlight-swatch-indicator" style="background-color: #d4af37;" title="Custom Highlight Swatch"></label>
                </div>
                <select id="art-tool-highlight" class="art-tool-select" onchange="applyArticleHighlight(this.value)" title="Choose Background Highlight Marker">
                  <option value="">Highlight: None</option>
                  <option value="rgba(212, 175, 55, 0.35)" style="background:#040d18; color:#fce09b;">✨ Golden Amber (35%)</option>
                  <option value="rgba(250, 204, 21, 0.35)" style="background:#040d18; color:#facc15;">🌟 Solar Gold (35%)</option>
                  <option value="rgba(56, 189, 248, 0.30)" style="background:#040d18; color:#38bdf8;">💎 Cyber Cyan (30%)</option>
                  <option value="rgba(52, 211, 153, 0.30)" style="background:#040d18; color:#34d399;">🍃 Emerald Sage (30%)</option>
                  <option value="rgba(244, 63, 94, 0.30)" style="background:#040d18; color:#f87171;">🌹 Crimson Rose (30%)</option>
                  <option value="rgba(192, 132, 252, 0.30)" style="background:#040d18; color:#c084fc;">🔮 Amethyst Purple (30%)</option>
                  <option value="rgba(15, 23, 42, 0.85)" style="background:#040d18; color:#e2e8f0;">🌑 Dark Velvet Slate (85%)</option>
                  <option value="transparent" style="background:#040d18; color:#94a3b8;">🧹 Clear Highlight</option>
                </select>
              </div>

              <!-- Margin & Block Spacing Group (Golden Ratio Spacing Scale) -->
              <div class="art-toolbar-group" title="Paragraph & Block Margin Spacing">
                <span class="art-toolbar-group-label">MARGIN</span>
                <select id="art-tool-margin" class="art-tool-select" onchange="applyArticleMargin(this.value)" title="Choose Block Margin / Spacing Scale">
                  <option value="">Margin: Standard (1.618rem)</option>
                  <option value="0.618rem 0">Compact Spacing (0.618rem / 10px)</option>
                  <option value="1.0rem 0">Standard Spacing (1.0rem / 16px)</option>
                  <option value="1.618rem 0">★ Golden Ratio Spacing (1.618rem / 26px)</option>
                  <option value="2.618rem 0">Relaxed Spacing (2.618rem / 42px)</option>
                  <option value="1.618rem 2.618rem">❝ Indented Inset (Both Sides)</option>
                  <option value="1.618rem 4.236rem">❝ Deep Scholarly Indent</option>
                  <option value="2.618rem -1.618rem">↔ Outset Bleed (-1.618rem)</option>
                  <option value="0 0 0.5rem 0">Tight Paragraph Bottom (0.5rem)</option>
                  <option value="0">Zero Margin (Flush)</option>
                  <option value="reset">↺ Reset Block Margin</option>
                </select>
                <button type="button" class="art-tool-btn" onclick="adjustBlockMargin('increase')" title="Increase Block Indent Margin (+16px)">+ Indent</button>
                <button type="button" class="art-tool-btn" onclick="adjustBlockMargin('decrease')" title="Decrease Block Indent Margin (-16px)">- Indent</button>
              </div>

              <!-- Inline Styling Group -->
              <div class="art-toolbar-group">
                <span class="art-toolbar-group-label">STYLE</span>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('bold')" title="Bold (Ctrl+B)"><b>B</b></button>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('italic')" title="Italic (Ctrl+I)"><i>I</i></button>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('underline')" title="Underline (Ctrl+U)"><u>U</u></button>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('strikethrough')" title="Strikethrough"><s>S</s></button>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('code')" title="Inline Code">&lt;/&gt;</button>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('highlight')" title="Gold Highlight Marker">🖌️ Mark</button>
                <button type="button" class="art-tool-btn art-tool-btn-clear" onclick="clearArticleElementFormat()" title="Clear Format: Strip all styles, spans, marks &amp; reset element to clean normal paragraph">🧹 Clear Format</button>
              </div>

              <!-- Alignment Group -->
              <div class="art-toolbar-group">
                <span class="art-toolbar-group-label">ALIGN</span>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('align', 'left')" title="Align Left">⫷ Left</button>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('align', 'center')" title="Center">≡ Center</button>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('align', 'right')" title="Align Right">⫸ Right</button>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('align', 'justify')" title="Justify Full">≣ Justify</button>
              </div>

              <!-- Scholarly Elements Group -->
              <div class="art-toolbar-group">
                <span class="art-toolbar-group-label">BLOCKS</span>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('math')" title="LaTeX / Math Formula Block">∑ Math</button>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('table')" title="Scholarly Table Generator">📊 Table</button>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('hr')" title="Section Divider (Golden Ratio Line)">― Divider</button>
              </div>

              <!-- Lists & Indent Group -->
              <div class="art-toolbar-group">
                <span class="art-toolbar-group-label">LISTS</span>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('ul')" title="Bullet List">• List</button>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('ol')" title="Numbered List">1. List</button>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('indent')" title="Indent In">⇥</button>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('outdent')" title="Outdent">⇤</button>
              </div>

              <!-- Media & Figure Group -->
              <div class="art-toolbar-group">
                <span class="art-toolbar-group-label">FIGURE &amp; MEDIA</span>
                <button type="button" class="art-tool-btn art-tool-btn-highlight" onclick="openArticleFigureModal()" title="Insert / Upload Academic Figure with Caption &amp; Size">🖼️ Figure</button>
                <label class="art-tool-btn" title="Quick Upload Image File from Computer" style="cursor: pointer; display: inline-flex; align-items: center; margin: 0; font-weight: 600;">
                  📁 Upload <input type="file" id="art-figure-quick-file" accept="image/*" style="display: none;" onchange="handleDirectArticleImageUpload(event)">
                </label>
                <button type="button" class="art-tool-btn art-tool-btn-highlight" onclick="applyArticleHeading('caption')" title="Format Selected Text as Figure/Table Caption (0.85rem Italic Slate) or Add Caption to Image">💬 Caption</button>
                <button type="button" class="art-tool-btn" onclick="formatSelectedArticleImage('compact')" title="Resize Figure: 60% Compact">60%</button>
                <button type="button" class="art-tool-btn" onclick="formatSelectedArticleImage('standard')" title="Resize Figure: 82% Standard">82%</button>
                <button type="button" class="art-tool-btn" onclick="formatSelectedArticleImage('full')" title="Resize Figure: 100% Full Column">100%</button>
                <button type="button" class="art-tool-btn" onclick="formatSelectedArticleImage('center')" title="Center Figure (Clear Floats)">⏺️ Center</button>
                <button type="button" class="art-tool-btn" onclick="formatSelectedArticleImage('left')" title="Float Figure Left (Text Wraps Right)">⫷ Wrap L</button>
                <button type="button" class="art-tool-btn" onclick="formatSelectedArticleImage('right')" title="Float Figure Right (Text Wraps Left)">Wrap R ⫸</button>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('link')" title="Insert Hyperlink">🔗 Link</button>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('unlink')" title="Remove Hyperlink">Unlink</button>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('video')" title="Embed YouTube Video">▶️ Video</button>
              </div>

              <!-- History & Mode Toggle -->
              <div class="art-toolbar-group art-toolbar-right" style="margin-left: auto;">
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('undo')" title="Undo (Ctrl+Z)">↺</button>
                <button type="button" class="art-tool-btn" onclick="applyArticleVisualFormat('redo')" title="Redo (Ctrl+Y)">↻</button>
                <div class="art-mode-switch">
                  <button type="button" id="btn-art-mode-visual" class="preview-tab-pill active" onclick="setArticleEditorMode('visual')">👁️ Visual Text</button>
                  <button type="button" id="btn-art-mode-code" class="preview-tab-pill" onclick="setArticleEditorMode('code')">&lt;/&gt; HTML Source</button>
                </div>
              </div>

            </div>

            <!-- Visual Contenteditable Container (High-Elevation Scholarly Desk & Canvas) -->
          </div>

          <!-- Harmonized Metadata Card (Collapsible) -->
          <div class="art-studio-meta-card" id="art-studio-meta-drawer">
            <!-- Row 1: Title & Category -->
            <div class="art-meta-row-1">
              <div class="form-group" style="flex: 1; margin: 0;">
                <label class="form-label" style="display: flex; justify-content: space-between;">
                  <span>Article Title *</span>
                  <span style="font-size: 0.72rem; color: #94a3b8; font-weight: normal;">Main publication &amp; essay headline</span>
                </label>
                <input type="text" id="art-form-title" class="cms-input art-title-input" placeholder="Enter Scholarly Article Title..." oninput="autoUpdateArticleTitle()">
              </div>
              <div class="form-group art-cat-group" style="width: 280px; margin: 0;">
                <label class="form-label">Category *</label>
                <select id="art-form-cat" class="cms-select" style="width: 100%;">
                  <option value="AI & Cybernetics">AI &amp; Cybernetics</option>
                  <option value="Essays & Perspectives">Essays &amp; Perspectives</option>
                  <option value="Pedagogy & Education">Pedagogy &amp; Education</option>
                  <option value="Digital Ethics & HCI">Digital Ethics &amp; HCI</option>
                  <option value="Philosophy & Society">Philosophy &amp; Society</option>
                  <option value="Epistemic & Media">Epistemic &amp; Media</option>
                </select>
              </div>
            </div>

            <!-- Row 2: 4-Column Golden Ratio Parameters -->
            <div class="art-meta-row-4">
              <div class="form-group" style="margin: 0;">
                <label class="form-label">Slug (URL ID) *</label>
                <input type="text" id="art-form-slug" class="cms-input" placeholder="e.g. harmony-human-trusted-ai" oninput="this.dataset.manuallyEdited='true'">
              </div>
              <div class="form-group" style="margin: 0;">
                <label class="form-label">Publication Date</label>
                <input type="date" id="art-form-date" class="cms-input">
              </div>
              <div class="form-group" style="margin: 0;">
                <label class="form-label">Estimated Read Time</label>
                <input type="text" id="art-form-readtime" class="cms-input" placeholder="e.g. 4 min read">
              </div>
              <div class="form-group" style="margin: 0;">
                <label class="form-label">Tags (comma-separated)</label>
                <input type="text" id="art-form-tags" class="cms-input" placeholder="e.g. AI, Cybernetics, Trust">
              </div>
            </div>

            <!-- Row 3: Excerpt & Featured Media / Spotlight (Golden Ratio Split 61.8% / 38.2%) -->
            <div class="art-meta-row-2">
              <div class="form-group" style="margin: 0;">
                <label class="form-label">Short Excerpt / Teaser</label>
                <textarea id="art-form-excerpt" class="cms-textarea" rows="2" placeholder="Summary statement or abstract shown in cards and teasers..."></textarea>
              </div>
              <div class="form-group" style="margin: 0;">
                <label class="form-label">Featured Image URL &amp; Spotlight Status</label>
                <div style="display: flex; gap: 8px; margin-bottom: 8px;">
                  <input type="text" id="art-form-image" class="cms-input" placeholder="assets/images/spotlight-smart-cities.jpg" oninput="updateImageThumbnail()">
                  <label class="cms-btn cms-btn-ghost" style="cursor: pointer; margin: 0; white-space: nowrap;">
                    📁 Upload <input type="file" id="art-image-uploader" accept="image/*" style="display: none;" onchange="handleImageUpload(event, 'art-form-image')">
                  </label>
                </div>
                <div style="display: flex; align-items: center; justify-content: space-between;">
                  <label style="display: flex; align-items: center; gap: 8px; cursor: pointer; margin: 0;">
                    <input type="checkbox" id="art-form-featured">
                    <span style="font-size: 0.82rem; font-weight: 700; color: #fef08a;">★ Feature as Active Homepage Spotlight</span>
                  </label>
                  <div id="art-image-thumbnail-preview" class="art-thumb-preview-box"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Main Article Content Editor Stage (Maximized, Advanced Features) -->
          <div class="art-studio-editor-stage">
            <div class="art-visual-wrapper" id="art-visual-desk-wrapper">
              <div id="art-img-floating-toolbar" class="art-img-floating-toolbar" role="toolbar" aria-label="Image Format Controls">
                <span style="font-size: 0.72rem; color: #fce09b; font-weight: 700; margin-right: 4px;">🖼️ FIGURE:</span>
                <button type="button" class="art-img-pill-btn" onclick="formatSelectedArticleImage('compact')" title="Compact (52% width, 260px max-height)">52% Compact</button>
                <button type="button" class="art-img-pill-btn" onclick="formatSelectedArticleImage('standard')" title="Standard (78% width, 380px max-height - Golden Ratio)">78% Golden</button>
                <button type="button" class="art-img-pill-btn" onclick="formatSelectedArticleImage('full')" title="Full Width (100% width, 480px max-height)">100% Full</button>
                <button type="button" class="art-img-pill-btn" onclick="formatSelectedArticleImage('left')" title="Float Left">⬅️ Left</button>
                <button type="button" class="art-img-pill-btn" onclick="formatSelectedArticleImage('center')" title="Center Align">⏺️ Center</button>
                <button type="button" class="art-img-pill-btn" onclick="formatSelectedArticleImage('right')" title="Float Right">➡️ Right</button>
                <button type="button" class="art-img-pill-btn" onclick="formatSelectedArticleImage('matting')" title="Toggle Dark Contrast Matting for white-backed technical figures">🌓 Matting</button>
                <button type="button" class="art-img-pill-btn" onclick="formatSelectedArticleImage('caption')" title="Edit Caption">✏️ Caption</button>
                <button type="button" class="art-img-pill-btn danger" onclick="formatSelectedArticleImage('delete')" title="Delete Figure">🗑️ Delete</button>
              </div>
              <div id="art-form-visual-editor" contenteditable="true" class="art-visual-canvas" oninput="onVisualArticleInput()"></div>
            </div>

            <!-- Raw HTML Code Container -->
            <textarea id="art-form-code-editor" class="art-code-canvas" style="display: none;" oninput="onCodeArticleInput()"></textarea>

            <!-- Editor Status & Live Telemetry Bar -->
            <div class="art-editor-statusbar">
              <div class="art-status-metrics">
                <span id="art-stat-words"><strong>0</strong> words</span>
                <span class="art-stat-sep">•</span>
                <span id="art-stat-chars"><strong>0</strong> characters</span>
                <span class="art-stat-sep">•</span>
                <span id="art-stat-readtime"><strong>1 min</strong> estimated read</span>
                <span class="art-stat-sep">•</span>
                <span id="art-stat-paragraphs"><strong>0</strong> paragraphs</span>
              </div>
              <div class="art-status-right">
                <span class="art-status-pulse"></span>
                <span style="font-size: 0.74rem; color: #94a3b8;">Scholarly Composition Engine • Golden Ratio Active</span>
              </div>
            </div>

          </div>

        </div>

      </div>

      <!-- Section 1C: Research Pillars & Active Grants View -->

      <div id="articles-subpane-pillars" style="display: none;">

        <!-- Research Vision Statement -->

        <div class="cms-feature-card" style="margin-bottom: 24px;">

          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">

            <h3 style="font-family: var(--font-cinzel); font-size: 1.05rem; color: #ffffff; margin: 0;">Institutional Research Vision Statement</h3>

            <button class="cms-btn cms-btn-cyan" onclick="saveResearchVision()">💾 Save Vision</button>

          </div>

          <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 10px;">This statement appears prominently on the Activity &amp; Project subpage (research.html).</p>

          <textarea id="research-vision-input" class="cms-textarea" rows="3" placeholder="Enter academic vision statement..."></textarea>

        </div>

        <!-- 3 Research Pillars -->

        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">

          <h3 style="font-family: var(--font-cinzel); font-size: 1.15rem; color: #ffffff; margin: 0;">Core Research Pillars (3)</h3>

          <button class="cms-btn cms-btn-ghost" onclick="openPillarModal(null)">+ Add Research Pillar</button>

        </div>

        <div class="cms-cards-grid" id="pillars-container" style="margin-bottom: 32px;"></div>

        <!-- Active Funded Grant Themes -->

        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">

          <h3 style="font-family: var(--font-cinzel); font-size: 1.15rem; color: #ffffff; margin: 0;">Active Funded Grant Themes (2)</h3>

          <button class="cms-btn cms-btn-ghost" onclick="openGrantModal(null)">+ Add Grant Theme</button>

        </div>

        <div class="cms-cards-grid" id="grants-container"></div>

      </div>

    </section>

    <!-- =============================================================

         PANEL 2: RESEARCH & PUBLICATION (publications.html)

         ============================================================= -->

    <section class="module-panel" id="panel-pubs">

      <div class="cms-filter-row">

        <div class="cms-search-box">

          <input type="text" id="pubs-search-input" class="cms-input" placeholder="Search publications by title, venue, or year..." oninput="filterPubsTable()">

        </div>

        <select id="pubs-cat-filter" class="cms-select" onchange="filterPubsTable()">

          <option value="">All Categories</option>

          <option value="Journal">Peer-Reviewed Journals</option>

          <option value="Conference">Conference Proceedings</option>

          <option value="Book Chapter">Book Chapters</option>

          <option value="Preprint">Preprints / SSRN</option>

        </select>

        <button class="cms-btn cms-btn-primary" onclick="openModal('modal-pub'); resetPubModal();">+ Add Publication</button>

        <button class="cms-btn cms-btn-ghost" onclick="openBooksHeroModal()" style="border-color: rgba(212,175,55,0.45); color: #fef08a;">📖 Monograph Hero Stage</button>

        <button class="cms-btn cms-btn-ghost" onclick="downloadJSON('publications.json', pubsData)">📥 Backup Pubs JSON</button>

      </div>

      <div class="cms-table-card">

        <table class="cms-table">

          <thead>

            <tr>

              <th style="width: 44px;">#</th>

              <th>Publication Title</th>

              <th>Category</th>

              <th>Venue / Journal</th>

              <th>Year</th>

              <th style="text-align: right;">Actions</th>

            </tr>

          </thead>

          <tbody id="pubs-tbody"></tbody>

        </table>

      </div>

    </section>

    <!-- =============================================================

         PANEL 3: MEDIA & TALKS (talks.html - 3 Categories 100% Matched)

         ============================================================= -->

    <section class="module-panel" id="panel-talks">

      <!-- 3 Sub-tabs matching talks.html -->

      <div class="cms-sub-pills-bar">

        <button class="cms-sub-pill active" id="subtab-btn-talkshows" onclick="switchTalksCategory('talkshows')">

          📺 01. Talkshows (Video Gallery) <span id="count-talkshows">7</span>

        </button>

        <button class="cms-sub-pill" id="subtab-btn-keynotes" onclick="switchTalksCategory('keynotes')">

          🎙️ 02. Keynote &amp; Visiting Speeches <span id="count-keynotes">6</span>

        </button>

        <button class="cms-sub-pill" id="subtab-btn-opinions" onclick="switchTalksCategory('opinions')">

          ✍️ 03. Opinion Essays &amp; Columns <span id="count-opinions">6</span>

        </button>

      </div>

      <div class="cms-filter-row">

        <div class="cms-search-box">

          <input type="text" id="talks-search-input" class="cms-input" placeholder="Search across all media, televised talkshows, keynotes, or opinions..." oninput="filterMediaTalksTable()">

        </div>

        <button class="cms-btn cms-btn-primary" id="btn-add-media-talk" onclick="openActiveTalkCategoryModal()">+ Add Item</button>

        <button class="cms-btn cms-btn-ghost" onclick="downloadJSON('media_talks.json', mediaTalksData)">📥 Backup Media JSON</button>

      </div>

      <!-- Category 1 Table: Talkshows -->

      <div id="media-table-talkshows" class="cms-table-card">

        <table class="cms-table">

          <thead>

            <tr>

              <th style="width: 44px;">Ep</th>

              <th>Talkshow Title &amp; Channel</th>

              <th>Category Tag</th>

              <th>Duration</th>

              <th>Air Date</th>

              <th style="text-align: right;">Actions</th>

            </tr>

          </thead>

          <tbody id="talkshows-tbody"></tbody>

        </table>

      </div>

      <!-- Category 2 Table: Keynotes -->

      <div id="media-table-keynotes" class="cms-table-card" style="display: none;">

        <table class="cms-table">

          <thead>

            <tr>

              <th style="width: 44px;">#</th>

              <th>Keynote Title &amp; Event</th>

              <th>Role / Plenary</th>

              <th>Venue / Host</th>

              <th>Year</th>

              <th style="text-align: right;">Actions</th>

            </tr>

          </thead>

          <tbody id="keynotes-tbody"></tbody>

        </table>

      </div>

      <!-- Category 3 Table: Opinions -->

      <div id="media-table-opinions" class="cms-table-card" style="display: none;">

        <table class="cms-table">

          <thead>

            <tr>

              <th style="width: 44px;">#</th>

              <th>Opinion Essay Title</th>

              <th>Type</th>

              <th>Publication Venue</th>

              <th>Year</th>

              <th style="text-align: right;">Actions</th>

            </tr>

          </thead>

          <tbody id="opinions-tbody"></tbody>

        </table>

      </div>

    </section>

    <!-- =============================================================

         PANEL 4: ACHIEVEMENT & CV (cv.html - 7 Sections 100% Matched)

         ============================================================= -->

    <section class="module-panel" id="panel-cv">

      <!-- 7 Sub-tabs matching cv.html -->

      <div class="cms-sub-pills-bar">

        <button class="cms-sub-pill active" id="subtab-btn-cv-honors" onclick="switchCvSection('achievements_and_grants')">

          🏆 Honors &amp; Grants <span id="count-cv-honors">16</span>

        </button>

        <button class="cms-sub-pill" id="subtab-btn-cv-profile" onclick="switchCvSection('executive_profile')">

          👤 Executive Profile

        </button>

        <button class="cms-sub-pill" id="subtab-btn-cv-leadership" onclick="switchCvSection('academic_leadership')">

          🏛️ Leadership (<span id="count-cv-leadership">5</span>

        </button>

        <button class="cms-sub-pill" id="subtab-btn-cv-education" onclick="switchCvSection('education')">

          🎓 Education (<span id="count-cv-education">5</span>

        </button>

        <button class="cms-sub-pill" id="subtab-btn-cv-experience" onclick="switchCvSection('work_experience')">

          💼 Experience (<span id="count-cv-experience">5</span>

        </button>

        <button class="cms-sub-pill" id="subtab-btn-cv-certs" onclick="switchCvSection('professional_certifications')">

          📜 Certifications (<span id="count-cv-certs">5</span>

        </button>

        <button class="cms-sub-pill" id="subtab-btn-cv-refs" onclick="switchCvSection('academic_references')">

          👥 References (<span id="count-cv-refs">4</span>

        </button>

      </div>

      <!-- Filter Row (for list sections) -->

      <div class="cms-filter-row" id="cv-filter-row">

        <div class="cms-search-box">

          <input type="text" id="cv-search-input" class="cms-input" placeholder="Search across honors, degrees, roles, or organizations..." oninput="filterCvCurrentTable()">

        </div>

        <button class="cms-btn cms-btn-primary" id="btn-add-cv-item" onclick="openActiveCvModal()">+ Add CV Item</button>

        <button class="cms-btn cms-btn-ghost" onclick="downloadJSON('cv_data.json', cvData)">📥 Backup CV JSON</button>

      </div>

      <!-- CV Section A: Honors & Grants Table -->

      <div id="cv-table-container-honors" class="cms-table-card">

        <table class="cms-table">

          <thead>

            <tr>

              <th style="width: 44px;">#</th>

              <th>Honor / Achievement Title</th>

              <th>Organization / Agency</th>

              <th>Badge</th>

              <th>Year</th>

              <th style="text-align: right;">Actions</th>

            </tr>

          </thead>

          <tbody id="cv-honors-tbody"></tbody>

        </table>

      </div>

      <!-- CV Section B: Executive Profile Form Editor -->

      <div id="cv-form-container-profile" class="cms-feature-card" style="display: none;">

        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">

          <div>

            <h3 style="font-family: var(--font-cinzel); font-size: 1.15rem; color: #ffffff; margin: 0 0 4px 0;">Executive Profile &amp; Official Identifiers</h3>

            <p style="font-size: 0.82rem; color: var(--text-muted); margin: 0;">Renders directly on the hero card of cv.html.</p>

          </div>

          <button class="cms-btn cms-btn-cyan" onclick="saveCvExecutiveProfile()">💾 Save Executive Profile</button>

        </div>

        <h4 style="font-family: var(--font-cinzel); font-size: 0.92rem; color: #fef08a; margin: 0 0 12px 0;">Executive Portrait &amp; CV Document Actions</h4>

        <div class="form-row-2">

          <div class="form-group">

            <label class="form-label">Executive Portrait Photo URL / Path</label>

            <div style="display: flex; gap: 8px; align-items: center;">

              <input type="text" id="cv-prof-photo" class="cms-input" style="flex: 1;" placeholder="assets/images/portraits/portrait-1.webp" oninput="updateCvPortraitPreview()">

              <label class="cms-btn cms-btn-ghost" style="cursor: pointer; margin: 0; white-space: nowrap; padding: 7px 12px; font-size: 0.78rem;">

                📁 Upload Photo <input type="file" id="cv-photo-uploader" accept="image/*" style="display: none;" onchange="handleImageUpload(event, 'cv-prof-photo').then(() => updateCvPortraitPreview())">

              </label>

              <div id="cv-portrait-preview-box" style="width: 44px; height: 54px; border: 1px solid rgba(212,175,55,0.4); border-radius: 6px; overflow: hidden; background: #030d1a; display: flex; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 4px 10px rgba(0,0,0,0.5);">

                <img id="cv-portrait-preview-img" src="" alt="Portrait" style="width: 100%; height: 100%; object-fit: cover; display: none;">

                <span id="cv-portrait-preview-empty" style="font-size: 0.65rem; color: #64748b;">No Img</span>

              </div>

            </div>

          </div>

          <div class="form-group">

            <label class="form-label">Portrait Kicker / Badge Label</label>

            <input type="text" id="cv-prof-kicker" class="cms-input" placeholder="Ph.D. • UKM 2024">

          </div>

        </div>

        <div class="form-row-2">

          <div class="form-group">

            <label class="form-label">Official CV PDF File (Download Button Target)</label>

            <div style="display: flex; gap: 8px; align-items: center;">

              <input type="text" id="cv-prof-cv-url" class="cms-input" style="flex: 1;" placeholder="assets/docs/dr-zaid-amin-cv-july-2026.pdf">

              <label class="cms-btn cms-btn-ghost" style="cursor: pointer; margin: 0; white-space: nowrap; padding: 7px 12px; font-size: 0.78rem;">

                📁 Upload PDF <input type="file" id="cv-pdf-uploader" accept=".pdf" style="display: none;" onchange="handleCvPdfUpload(event, 'cv-prof-cv-url')">

              </label>

            </div>

            <span class="cms-field-hint" style="font-size: 0.72rem; color: #94a3b8; margin-top: 4px; display: block;">Local files live in <code>assets/docs/</code> or use external cloud link.</span>

          </div>

          <div class="form-group">

            <label class="form-label">CV Edition &amp; Verification Label</label>

            <input type="text" id="cv-prof-edition" class="cms-input" placeholder="July 2026 Academic Edition • 1.1 MB">

          </div>

        </div>

        <h4 style="font-family: var(--font-cinzel); font-size: 0.92rem; color: var(--cyan-accent); margin: 24px 0 12px 0;">Academic Credentials &amp; Titles</h4>

        <div class="form-row-2">

          <div class="form-group">

            <label class="form-label">Full Name &amp; Degrees *</label>

            <input type="text" id="cv-prof-name" class="cms-input">

          </div>

          <div class="form-group">

            <label class="form-label">Role Title *</label>

            <input type="text" id="cv-prof-role" class="cms-input">

          </div>

        </div>

        <div class="form-row-2">

          <div class="form-group">

            <label class="form-label">Institution Affiliation *</label>

            <input type="text" id="cv-prof-institution" class="cms-input">

          </div>

          <div class="form-group">

            <label class="form-label">Primary Distinction Badge (Gold) *</label>

            <input type="text" id="cv-prof-distinction" class="cms-input">

          </div>

        </div>

        <div class="form-group">

          <label class="form-label">Executive Bio / Academic Summary</label>

          <textarea id="cv-prof-summary" class="cms-textarea" rows="4"></textarea>

        </div>

        <h4 style="font-family: var(--font-cinzel); font-size: 0.92rem; color: var(--cyan-accent); margin: 24px 0 12px 0;">Official Academic &amp; Regulatory Identifiers</h4>

        <div class="form-row-3">

          <div class="form-group">

            <label class="form-label">ORCID iD</label>

            <input type="text" id="cv-prof-orcid" class="cms-input">

          </div>

          <div class="form-group">

            <label class="form-label">Scopus Author ID</label>

            <input type="text" id="cv-prof-scopus" class="cms-input">

          </div>

          <div class="form-group">

            <label class="form-label">WoS ResearcherID</label>

            <input type="text" id="cv-prof-wos" class="cms-input">

          </div>

        </div>

        <div class="form-row" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px;">

          <div class="form-group">

            <label class="form-label">Institutional Email</label>

            <input type="email" id="cv-prof-email" class="cms-input">

          </div>

          <div class="form-group">

            <label class="form-label">Teaching Permit URL</label>

            <input type="text" id="cv-prof-permit" class="cms-input">

          </div>

          <div class="form-group">

            <label class="form-label">MQA Official CV URL</label>

            <input type="text" id="cv-prof-mqa" class="cms-input">

          </div>

          <div class="form-group">

            <label class="form-label">Teaching Portfolio URL</label>

            <input type="text" id="cv-prof-portfolio" class="cms-input">

          </div>

        </div>

      </div>

      <!-- CV Section C: Academic Leadership Table -->

      <div id="cv-table-container-leadership" class="cms-table-card" style="display: none;">

        <table class="cms-table">

          <thead>

            <tr>

              <th style="width: 44px;">#</th>

              <th>Leadership Role / Title</th>

              <th>Institution / Faculty</th>

              <th>Period</th>

              <th>Key Contributions</th>

              <th style="text-align: right;">Actions</th>

            </tr>

          </thead>

          <tbody id="cv-leadership-tbody"></tbody>

        </table>

      </div>

      <!-- CV Section D: Education Table -->

      <div id="cv-table-container-education" class="cms-table-card" style="display: none;">

        <table class="cms-table">

          <thead>

            <tr>

              <th style="width: 44px;">#</th>

              <th>Degree &amp; Field</th>

              <th>University / Institution</th>

              <th>Period</th>

              <th>Distinction / Honors</th>

              <th style="text-align: right;">Actions</th>

            </tr>

          </thead>

          <tbody id="cv-education-tbody"></tbody>

        </table>

      </div>

      <!-- CV Section E: Work Experience Table -->

      <div id="cv-table-container-experience" class="cms-table-card" style="display: none;">

        <table class="cms-table">

          <thead>

            <tr>

              <th style="width: 44px;">#</th>

              <th>Position / Title</th>

              <th>Organization / Institution</th>

              <th>Period</th>

              <th>Description</th>

              <th style="text-align: right;">Actions</th>

            </tr>

          </thead>

          <tbody id="cv-experience-tbody"></tbody>

        </table>

      </div>

      <!-- CV Section F: Professional Certifications Table -->

      <div id="cv-table-container-certs" class="cms-table-card" style="display: none;">

        <table class="cms-table">

          <thead>

            <tr>

              <th style="width: 44px;">#</th>

              <th>Certification Name</th>

              <th>Issuing Organization</th>

              <th>Year / Period</th>

              <th>Details / ID</th>

              <th style="text-align: right;">Actions</th>

            </tr>

          </thead>

          <tbody id="cv-certs-tbody"></tbody>

        </table>

      </div>

      <!-- CV Section G: Academic References Table -->

      <div id="cv-table-container-refs" class="cms-table-card" style="display: none;">

        <table class="cms-table">

          <thead>

            <tr>

              <th style="width: 44px;">#</th>

              <th>Referee Name</th>

              <th>Designation &amp; Title</th>

              <th>Institution</th>

              <th>Contact Coordinates</th>

              <th style="text-align: right;">Actions</th>

            </tr>

          </thead>

          <tbody id="cv-refs-tbody"></tbody>

        </table>

      </div>

    </section>

    <!-- =============================================================

         PANEL 5: SUPERVISION / PH.D. (prospective-students.html)

         ============================================================= -->

    <section class="module-panel" id="panel-supervision">

      <div class="cms-feature-card" style="margin-bottom: 24px;">

        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">

          <div>

            <h3 style="font-family: var(--font-cinzel); font-size: 1.15rem; color: #ffffff; margin: 0 0 4px 0;">Postgraduate Research &amp; Supervisory Statement</h3>

            <p style="font-size: 0.82rem; color: var(--text-muted); margin: 0;">Configures prospective-students.html invitation to Ph.D. and Master's candidates.</p>

          </div>

          <button class="cms-btn cms-btn-cyan" onclick="saveSupervisionStatement()">💾 Save Statement</button>

        </div>

        <div class="form-group">

          <label class="form-label">Page Headline *</label>

          <input type="text" id="sup-form-heading" class="cms-input">

        </div>

        <div class="form-group">

          <label class="form-label">Subheading / Initiative *</label>

          <input type="text" id="sup-form-subheading" class="cms-input">

        </div>

        <div class="form-group">

          <label class="form-label">Official Supervisory Statement</label>

          <textarea id="sup-form-statement" class="cms-textarea" rows="4"></textarea>

        </div>

      </div>

      <!-- Open Research Topics -->

      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">

        <h3 style="font-family: var(--font-cinzel); font-size: 1.15rem; color: #ffffff; margin: 0;">Open Supervised Research Directions (4)</h3>

        <button class="cms-btn cms-btn-ghost" onclick="openSupervisionTopicModal(null)">+ Add Research Direction</button>

      </div>

      <div class="cms-cards-grid" id="supervision-topics-container"></div>

    </section>

    <!-- =============================================================

         PANEL 6: HOME & GLOBAL PROFILE (index.html & profile.json)

         ============================================================= -->

    <section class="module-panel" id="panel-profile">

      <div class="cms-feature-card" style="margin-bottom: 24px;">

        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">

          <div>

            <h3 style="font-family: var(--font-cinzel); font-size: 1.15rem; color: #ffffff; margin: 0 0 4px 0;">Executive Identity &amp; Epigraph</h3>

            <p style="font-size: 0.82rem; color: var(--text-muted); margin: 0;">Controls index.html epigraph, philosophical motto, and global scholarly identifiers.</p>

          </div>

          <button class="cms-btn cms-btn-cyan" onclick="saveGlobalProfile()">💾 Save Profile</button>

        </div>

        <div class="form-row-2">

          <div class="form-group">

            <label class="form-label">Scholar Name</label>

            <input type="text" id="prof-form-name" class="cms-input">

          </div>

          <div class="form-group">

            <label class="form-label">Academic Degree</label>

            <input type="text" id="prof-form-degree" class="cms-input">

          </div>

        </div>

        <div class="form-row-2">

          <div class="form-group">

            <label class="form-label">Top Epigraph Title</label>

            <input type="text" id="prof-form-epigraph" class="cms-input" value="Das Sein, Das Sollen.">

          </div>

          <div class="form-group">

            <label class="form-label">Philosophical Motto</label>

            <input type="text" id="prof-form-motto" class="cms-input">

          </div>

        </div>

        <div class="form-group">

          <label class="form-label">Short Academic Bio</label>

          <textarea id="prof-form-bio" class="cms-textarea" rows="3"></textarea>

        </div>

        <h4 style="font-family: var(--font-cinzel); font-size: 0.92rem; color: var(--cyan-accent); margin: 24px 0 12px 0;">Social &amp; Scholarly Identifiers (Star of David Cluster)</h4>

        <div class="form-row-3">

          <div class="form-group">

            <label class="form-label">Google Scholar URL</label>

            <input type="text" id="prof-form-scholar" class="cms-input">

          </div>

          <div class="form-group">

            <label class="form-label">ORCID URL</label>

            <input type="text" id="prof-form-orcid" class="cms-input">

          </div>

          <div class="form-group">

            <label class="form-label">GitHub URL</label>

            <input type="text" id="prof-form-github" class="cms-input">

          </div>

        </div>

        <div class="form-row-3">

          <div class="form-group">

            <label class="form-label">LinkedIn URL</label>

            <input type="text" id="prof-form-linkedin" class="cms-input">

          </div>

          <div class="form-group">

            <label class="form-label">SciProfiles URL</label>

            <input type="text" id="prof-form-sciprofiles" class="cms-input">

          </div>

          <div class="form-group">

            <label class="form-label">ResearchGate URL</label>

            <input type="text" id="prof-form-rg" class="cms-input">

          </div>

        </div>

      </div>

      <!-- Universal Homepage Spotlight Configuration -->

      <div class="cms-feature-card">

        <h3 style="font-family: var(--font-cinzel); font-size: 1.15rem; color: #ffffff; margin: 0 0 6px 0;">Universal Homepage Spotlight Configuration</h3>

        <p style="font-size: 0.82rem; color: var(--text-muted); margin: 0 0 16px 0;">Select any article, publication, talk, or honor to highlight on the homepage split section (spotlight.json).</p>

        <div style="background: rgba(3, 14, 26, 0.7); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 18px; margin-bottom: 16px;">

          <div style="font-size: 0.76rem; color: var(--cyan-accent); font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">Current Active Spotlight</div>

          <div id="prof-spotlight-active-title" style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-bottom: 6px;">Loading...</div>

          <span class="spotlight-active-badge" id="prof-spotlight-active-source">PUBLICATION</span>

        </div>

      </div>

    </section>

    <!-- =============================================================

         PANEL 7: READERSHIP TELEMETRY & GA4 AUDIT STUDIO

         ============================================================= -->

""" + TELEMETRY_HTML + """

  </main>

  <!-- =============================================================

       5. COMPREHENSIVE EDITORIAL MODALS

       ============================================================= -->

  <!-- Modal: Insert Academic Figure / Diagram -->
  <div class="cms-modal-backdrop" id="modal-figure-insert">
    <div class="cms-modal-dialog" style="max-width: 620px;">
      <div class="cms-modal-header">
        <h3 class="cms-modal-title">🖼️ Insert Academic Figure / Diagram</h3>
        <button type="button" class="cms-btn cms-btn-ghost" onclick="closeModal('modal-figure-insert')">&times;</button>
      </div>
      <div class="cms-modal-body">
        
        <!-- Upload or Choose File from Computer -->
        <div class="form-group">
          <label class="form-label" style="display: flex; justify-content: space-between; align-items: center;">
            <span>📁 Upload Image from Computer</span>
            <span style="font-size: 0.72rem; color: #94a3b8;">PNG, JPG, WEBP, SVG</span>
          </label>
          <div style="display: flex; gap: 10px; align-items: center;">
            <button type="button" class="cms-btn cms-btn-primary" style="padding: 7px 16px; font-size: 0.82rem;" onclick="document.getElementById('modal-fig-file-picker').click()">
              📁 Choose File from Computer...
            </button>
            <input type="file" id="modal-fig-file-picker" accept="image/*" style="display: none;" onchange="handleModalFigureUpload(event)">
            <span style="font-size: 0.75rem; color: #94a3b8;">or enter web / asset URL below</span>
          </div>
        </div>

        <!-- Image URL or Asset Path -->
        <div class="form-group">
          <label class="form-label">Image URL / Asset Path *</label>
          <input type="text" id="modal-fig-url" class="cms-input" placeholder="assets/images/... or https://..." oninput="updateModalFigPreview(this.value)">
        </div>

        <!-- Live Thumbnail Preview -->
        <div id="modal-fig-preview-box" style="display: none; margin-bottom: 16px; padding: 12px; background: rgba(3, 10, 20, 0.75); border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 8px; text-align: center;">
          <div style="font-size: 0.70rem; color: #d4af37; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">Image Preview</div>
          <img id="modal-fig-preview-img" src="" alt="Figure Preview" style="max-height: 180px; max-width: 100%; border-radius: 6px; box-shadow: 0 4px 14px rgba(0,0,0,0.5);">
        </div>

        <!-- Caption -->
        <div class="form-group">
          <label class="form-label" style="display: flex; justify-content: space-between;">
            <span>Figure Caption (Optional)</span>
            <span style="font-size: 0.72rem; color: #94a3b8;">Rendered neatly beneath the image</span>
          </label>
          <input type="text" id="modal-fig-caption" class="cms-input" placeholder="Figure: Architectural diagram of cybernetic urban interaction">
        </div>

        <!-- Size & Alignment (Golden Ratio Grid) -->
        <div class="form-row-2">
          <div class="form-group">
            <label class="form-label">Layout Size (Golden Ratio)</label>
            <select id="modal-fig-size" class="cms-select" style="width: 100%;">
              <option value="standard" selected>★ Standard Golden Ratio (82% Column)</option>
              <option value="compact">Compact Diagram (60% Column)</option>
              <option value="full">Full Bleed (100% Column)</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Alignment</label>
            <select id="modal-fig-align" class="cms-select" style="width: 100%;">
              <option value="center" selected>Center (Harmonized)</option>
              <option value="left">Left Aligned</option>
              <option value="right">Right Aligned</option>
            </select>
          </div>
        </div>

        <!-- Action Footer -->
        <div class="cms-modal-footer" style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; padding-top: 14px; border-top: 1px solid rgba(186, 230, 253, 0.12);">
          <button type="button" class="cms-btn cms-btn-ghost" onclick="closeModal('modal-figure-insert')">Cancel</button>
          <button type="button" class="cms-btn cms-btn-primary" onclick="confirmInsertArticleFigure()" style="background: linear-gradient(135deg, #d4af37 0%, #b89628 100%); color: #020b14; font-weight: 700;">
            🖼️ Insert Figure into Article
          </button>
        </div>

      </div>
    </div>
  </div>

  <!-- Modal: Publication -->

  <div class="cms-modal-backdrop" id="modal-pub">

    <div class="cms-modal-dialog">

      <div class="cms-modal-header">

        <h3 class="cms-modal-title" id="modal-pub-heading">Edit Publication</h3>

        <button class="cms-btn cms-btn-ghost" onclick="closeModal('modal-pub')">&times;</button>

      </div>

      <div class="cms-modal-body">

        <form id="form-pub" onsubmit="savePublicationAction(event)">

          <div class="form-group">

            <label class="form-label">Publication Title *</label>

            <input type="text" id="pub-form-title" class="cms-input" required>

          </div>

          <div class="form-row-2">

            <div class="form-group">

              <label class="form-label">Publication ID (BibTeX Key) *</label>

              <input type="text" id="pub-form-id" class="cms-input" required>

            </div>

            <div class="form-group">

              <label class="form-label">Category *</label>

              <select id="pub-form-cat" class="cms-select" style="width: 100%;">

                <option value="Journal">Peer-Reviewed Journal</option>

                <option value="Conference">Conference Proceedings</option>

                <option value="Book Chapter">Book Chapter / Volume</option>

                <option value="Preprint">Preprint / Working Paper</option>

              </select>

            </div>

          </div>

          <div class="form-row-2">

            <div class="form-group">

              <label class="form-label">Venue / Journal / Publisher *</label>

              <input type="text" id="pub-form-venue" class="cms-input" required>

            </div>

            <div class="form-group">

              <label class="form-label">Publication Year *</label>

              <input type="text" id="pub-form-year" class="cms-input" value="2026" required>

            </div>

          </div>

          <div class="form-row-2">

            <div class="form-group">

              <label class="form-label">DOI / External Link</label>

              <input type="text" id="pub-form-doi" class="cms-input" placeholder="https://doi.org/10.xxxx">

            </div>

            <div class="form-group">

              <label class="form-label">Citation Metrics (Optional)</label>

              <input type="text" id="pub-form-citations" class="cms-input" placeholder="e.g. Scopus Q1, Impact Factor 4.2">

            </div>

          </div>

          <div class="form-group">

            <label class="form-label">Authors List</label>

            <input type="text" id="pub-form-authors" class="cms-input" placeholder="e.g. Zaid Amin, et al.">

          </div>

          <div class="form-group">

            <label class="form-label">Abstract / Summary</label>

            <textarea id="pub-form-abstract" class="cms-textarea" rows="3"></textarea>

          </div>

          <div class="form-group">

            <label class="form-label">Cover Image / 3D Book Thumbnail URL or Path</label>

            <div style="display: flex; gap: 8px; align-items: center;">

              <input type="text" id="pub-form-image" class="cms-input" style="flex: 1;" placeholder="assets/images/books/book_name.webp or https://..." oninput="updatePubCoverPreview()">

              <label class="cms-btn cms-btn-ghost" style="cursor: pointer; margin: 0; white-space: nowrap; padding: 7px 12px; font-size: 0.78rem;">

                📁 Upload <input type="file" id="pub-image-uploader" accept="image/*" style="display: none;" onchange="handleImageUpload(event, 'pub-form-image').then(() => updatePubCoverPreview())">

              </label>

              <div id="pub-cover-preview-box" style="width: 48px; height: 68px; border: 1px solid rgba(212,175,55,0.3); border-radius: 4px; overflow: hidden; background: #030a14; display: flex; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 4px 10px rgba(0,0,0,0.5);">

                <img id="pub-cover-preview-img" src="" alt="Cover" style="width: 100%; height: 100%; object-fit: cover; display: none;">

                <span id="pub-cover-preview-empty" style="font-size: 0.65rem; color: #64748b;">No Img</span>

              </div>

            </div>

            <span class="cms-field-hint" style="font-size: 0.72rem; color: #94a3b8; margin-top: 4px; display: block;">For Book Chapters / Primary Monograph: Recommended 2:3 ratio (~600x900px). Standard covers live in <code>assets/images/books/</code>.</span>

          </div>

          <div class="form-group">

            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;">

              <input type="checkbox" id="pub-form-featured">

              <span style="font-size: 0.84rem; font-weight: 700; color: #fef08a;">★ Set as Primary Monograph (Bokify Showcase) / Active Homepage Spotlight</span>

            </label>

          </div>

          <div class="cms-modal-footer">

            <button type="button" class="cms-btn cms-btn-ghost" onclick="closeModal('modal-pub')">Cancel</button>

            <button type="submit" class="cms-btn cms-btn-primary">Save Publication</button>

          </div>

        </form>

      </div>

    </div>

  </div>

  <!-- Modal: Monograph Hero Stage Settings -->

  <div class="cms-modal-backdrop" id="modal-books-hero">

    <div class="cms-modal-dialog" style="max-width: 680px;">

      <div class="cms-modal-header">

        <h3 class="cms-modal-title">📖 Edit Monograph Hero Stage</h3>

        <button class="cms-btn cms-btn-ghost" onclick="closeModal('modal-books-hero')">&times;</button>

      </div>

      <div class="cms-modal-body">

        <form id="form-books-hero" onsubmit="saveBooksHero(event)">

          <div class="form-group">

            <label class="form-label">Category Kicker / Stage Subtitle</label>

            <input type="text" id="hero-form-kicker" class="cms-input" placeholder="01 / 04 • MONOGRAPHS & CHAPTERS">

          </div>

          <div class="form-row-2">

            <div class="form-group">

              <label class="form-label">Headline Prefix</label>

              <input type="text" id="hero-form-prefix" class="cms-input" placeholder="Explore Research">

            </div>

            <div class="form-group">

              <label class="form-label">Headline Highlight (Gold Gradient)</label>

              <input type="text" id="hero-form-highlight" class="cms-input" placeholder="Monographs & Chapters">

            </div>

          </div>

          <div class="form-group">

            <label class="form-label">Overview Description Paragraph</label>

            <textarea id="hero-form-desc" class="cms-textarea" rows="4" placeholder="Comprehensive academic monographs..."></textarea>

          </div>

          <div class="form-group">

            <label class="form-label">Publisher Verification Pills (Comma-Separated)</label>

            <input type="text" id="hero-form-badges" class="cms-input" placeholder="Springer Nature, LNCS Series, Atlantis Press, Scopus Indexed, Gold Open Access">

            <span class="cms-field-hint" style="font-size: 0.72rem; color: #94a3b8; margin-top: 4px; display: block;">Enter badges separated by commas.</span>

          </div>

          <div class="cms-modal-footer">

            <button type="button" class="cms-btn cms-btn-ghost" onclick="closeModal('modal-books-hero')">Cancel</button>

            <button type="submit" class="cms-btn cms-btn-primary">Save Hero Stage</button>

          </div>

        </form>

      </div>

    </div>

  </div>

  <!-- Modal: Talkshow Video -->

  <div class="cms-modal-backdrop" id="modal-talkshow">

    <div class="cms-modal-dialog">

      <div class="cms-modal-header">

        <h3 class="cms-modal-title" id="modal-talkshow-heading">Edit Talkshow Video</h3>

        <button class="cms-btn cms-btn-ghost" onclick="closeModal('modal-talkshow')">&times;</button>

      </div>

      <div class="cms-modal-body">

        <form id="form-talkshow" onsubmit="saveTalkshowAction(event)">

          <div class="form-row-2">

            <div class="form-group">

              <label class="form-label">Episode Number *</label>

              <input type="text" id="ts-form-ep" class="cms-input" placeholder="01" required>

            </div>

            <div class="form-group">

              <label class="form-label">Broadcast Channel *</label>

              <input type="text" id="ts-form-channel" class="cms-input" placeholder="TVRI Sumatera Selatan" required>

            </div>

          </div>

          <div class="form-group">

            <label class="form-label">Talkshow Title *</label>

            <input type="text" id="ts-form-title" class="cms-input" required>

          </div>

          <div class="form-row-3">

            <div class="form-group">

              <label class="form-label">Category Tag</label>

              <input type="text" id="ts-form-tag" class="cms-input" placeholder="Televised Talkshow">

            </div>

            <div class="form-group">

              <label class="form-label">Air Date</label>

              <input type="text" id="ts-form-date" class="cms-input" placeholder="Mei 2015">

            </div>

            <div class="form-group">

              <label class="form-label">Duration</label>

              <input type="text" id="ts-form-duration" class="cms-input" placeholder="24:30">

            </div>

          </div>

          <div class="form-group">

            <label class="form-label">Video URL (YouTube or Google Drive View Link)</label>

            <input type="text" id="ts-form-video-url" class="cms-input">

          </div>

          <div class="form-group">

            <label class="form-label">Embed URL (Google Drive /preview or YouTube /embed)</label>

            <input type="text" id="ts-form-embed-url" class="cms-input">

          </div>

          <div class="form-group">

            <label class="form-label">Poster Thumbnail URL</label>

            <div style="display: flex; gap: 8px; align-items: center;">

              <input type="text" id="ts-form-poster" class="cms-input" style="flex: 1;" placeholder="assets/images/talks/tvri-virtual-machine.jpg" oninput="updateTsCoverPreview()">

              <label class="cms-btn cms-btn-ghost" style="cursor: pointer; margin: 0; white-space: nowrap; padding: 7px 12px; font-size: 0.78rem;">

                📁 Upload <input type="file" id="ts-image-uploader" accept="image/*" style="display: none;" onchange="handleImageUpload(event, 'ts-form-poster').then(() => updateTsCoverPreview())">

              </label>

              <div id="ts-cover-preview-box" style="width: 64px; height: 44px; border: 1px solid rgba(212,175,55,0.3); border-radius: 4px; overflow: hidden; background: #030a14; display: flex; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 4px 10px rgba(0,0,0,0.5);">

                <img id="ts-cover-preview-img" src="" alt="Poster" style="width: 100%; height: 100%; object-fit: cover; display: none;">

                <span id="ts-cover-preview-empty" style="font-size: 0.65rem; color: #64748b;">No Img</span>

              </div>

            </div>

          </div>

          <div class="form-group">

            <label class="form-label">Broadcast Description</label>

            <textarea id="ts-form-desc" class="cms-textarea" rows="3"></textarea>

          </div>

          <div class="cms-modal-footer">

            <button type="button" class="cms-btn cms-btn-ghost" onclick="closeModal('modal-talkshow')">Cancel</button>

            <button type="submit" class="cms-btn cms-btn-primary">Save Talkshow Video</button>

          </div>

        </form>

      </div>

    </div>

  </div>

  <!-- Modal: Keynote / Visiting Speech -->

  <div class="cms-modal-backdrop" id="modal-keynote">

    <div class="cms-modal-dialog">

      <div class="cms-modal-header">

        <h3 class="cms-modal-title" id="modal-keynote-heading">Edit Keynote Address</h3>

        <button class="cms-btn cms-btn-ghost" onclick="closeModal('modal-keynote')">&times;</button>

      </div>

      <div class="cms-modal-body">

        <form id="form-keynote" onsubmit="saveKeynoteAction(event)">

          <div class="form-group">

            <label class="form-label">Speech / Lecture Title *</label>

            <input type="text" id="kn-form-title" class="cms-input" required>

          </div>

          <div class="form-row-2">

            <div class="form-group">

              <label class="form-label">Role / Keynote Type *</label>

              <input type="text" id="kn-form-role" class="cms-input" placeholder="Plenary Keynote Address" required>

            </div>

            <div class="form-group">

              <label class="form-label">Badge Label</label>

              <input type="text" id="kn-form-badge" class="cms-input" placeholder="01 • PLENARY">

            </div>

          </div>

          <div class="form-group">

            <label class="form-label">Conference / Forum Name *</label>

            <input type="text" id="kn-form-event" class="cms-input" required>

          </div>

          <div class="form-row-2">

            <div class="form-group">

              <label class="form-label">Venue / Host University</label>

              <input type="text" id="kn-form-venue" class="cms-input">

            </div>

            <div class="form-group">

              <label class="form-label">Display Date (e.g. MARCH | 2026)</label>

              <input type="text" id="kn-form-date" class="cms-input">

            </div>

          </div>

          <div class="form-group">

            <label class="form-label">Abstract / Lecture Summary</label>

            <textarea id="kn-form-abstract" class="cms-textarea" rows="3"></textarea>

          </div>

          <div class="form-group">

            <label class="form-label">Conference Slides / Video Link</label>

            <input type="text" id="kn-form-url" class="cms-input" placeholder="https://...">

          </div>

          <div class="form-group">

            <label class="form-label">Background Artwork / Portrait Image URL or Path</label>

            <div style="display: flex; gap: 8px; align-items: center;">

              <input type="text" id="kn-form-image" class="cms-input" style="flex: 1;" placeholder="assets/images/spotlight-smart-cities.jpg or https://..." oninput="updateKnCoverPreview()">

              <label class="cms-btn cms-btn-ghost" style="cursor: pointer; margin: 0; white-space: nowrap; padding: 7px 12px; font-size: 0.78rem;">

                📁 Upload <input type="file" id="kn-image-uploader" accept="image/*" style="display: none;" onchange="handleImageUpload(event, 'kn-form-image').then(() => updateKnCoverPreview())">

              </label>

              <div id="kn-cover-preview-box" style="width: 52px; height: 70px; border: 1px solid rgba(212,175,55,0.3); border-radius: 6px; overflow: hidden; background: #030a14; display: flex; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 4px 10px rgba(0,0,0,0.5);">

                <img id="kn-cover-preview-img" src="" alt="Cover" style="width: 100%; height: 100%; object-fit: cover; display: none;">

                <span id="kn-cover-preview-empty" style="font-size: 0.65rem; color: #64748b;">No Img</span>

              </div>

            </div>

            <span class="cms-field-hint" style="font-size: 0.72rem; color: #94a3b8; margin-top: 4px; display: block;">Keynote card background artwork (recommended ~3:4 or 4:5 portrait ratio, e.g. <code>assets/images/spotlight-smart-cities.jpg</code>).</span>

          </div>

          <div class="cms-modal-footer">

            <button type="button" class="cms-btn cms-btn-ghost" onclick="closeModal('modal-keynote')">Cancel</button>

            <button type="submit" class="cms-btn cms-btn-primary">Save Keynote Address</button>

          </div>

        </form>

      </div>

    </div>

  </div>

  <!-- Modal: Opinion Article -->

  <div class="cms-modal-backdrop" id="modal-opinion">

    <div class="cms-modal-dialog">

      <div class="cms-modal-header">

        <h3 class="cms-modal-title" id="modal-opinion-heading">Edit Opinion Column</h3>

        <button class="cms-btn cms-btn-ghost" onclick="closeModal('modal-opinion')">&times;</button>

      </div>

      <div class="cms-modal-body">

        <form id="form-opinion" onsubmit="saveOpinionAction(event)">

          <div class="form-group">

            <label class="form-label">Opinion Essay Title *</label>

            <input type="text" id="op-form-title" class="cms-input" required>

          </div>

          <div class="form-row-2">

            <div class="form-group">

              <label class="form-label">Opinion Type</label>

              <input type="text" id="op-form-type" class="cms-input" placeholder="Philosophical Opinion">

            </div>

            <div class="form-group">

              <label class="form-label">Badge Label</label>

              <input type="text" id="op-form-badge" class="cms-input" placeholder="ESSAY 01">

            </div>

          </div>

          <div class="form-row-2">

            <div class="form-group">

              <label class="form-label">Publication / Venue *</label>

              <input type="text" id="op-form-pub" class="cms-input" placeholder="Philosophical Treatises" required>

            </div>

            <div class="form-group">

              <label class="form-label">Date Display (e.g. SEPTEMBER | 2026)</label>

              <input type="text" id="op-form-date" class="cms-input">

            </div>

          </div>

          <div class="form-group">

            <label class="form-label">Abstract / Critical Thesis</label>

            <textarea id="op-form-abstract" class="cms-textarea" rows="3"></textarea>

          </div>

          <div class="form-group">

            <label class="form-label">Full Article Link / Slug (e.g. article.html?id=...)</label>

            <input type="text" id="op-form-url" class="cms-input">

          </div>

          <div class="form-group">

            <label class="form-label">Background Artwork / Thumbnail Image URL or Path</label>

            <div style="display: flex; gap: 8px; align-items: center;">

              <input type="text" id="op-form-image" class="cms-input" style="flex: 1;" placeholder="assets/images/thumb-attention.jpg or https://..." oninput="updateOpCoverPreview()">

              <label class="cms-btn cms-btn-ghost" style="cursor: pointer; margin: 0; white-space: nowrap; padding: 7px 12px; font-size: 0.78rem;">

                📁 Upload <input type="file" id="op-image-uploader" accept="image/*" style="display: none;" onchange="handleImageUpload(event, 'op-form-image').then(() => updateOpCoverPreview())">

              </label>

              <div id="op-cover-preview-box" style="width: 52px; height: 70px; border: 1px solid rgba(212,175,55,0.3); border-radius: 6px; overflow: hidden; background: #030a14; display: flex; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 4px 10px rgba(0,0,0,0.5);">

                <img id="op-cover-preview-img" src="" alt="Cover" style="width: 100%; height: 100%; object-fit: cover; display: none;">

                <span id="op-cover-preview-empty" style="font-size: 0.65rem; color: #64748b;">No Img</span>

              </div>

            </div>

            <span class="cms-field-hint" style="font-size: 0.72rem; color: #94a3b8; margin-top: 4px; display: block;">Card background art for opinion treatise.</span>

          </div>

          <div class="cms-modal-footer">

            <button type="button" class="cms-btn cms-btn-ghost" onclick="closeModal('modal-opinion')">Cancel</button>

            <button type="submit" class="cms-btn cms-btn-primary">Save Opinion</button>

          </div>

        </form>

      </div>

    </div>

  </div>

  <!-- Modal: CV Honor / Grant -->

  <div class="cms-modal-backdrop" id="modal-cv-honor">

    <div class="cms-modal-dialog">

      <div class="cms-modal-header">

        <h3 class="cms-modal-title" id="modal-cv-honor-heading">Edit Honor / Achievement</h3>

        <button class="cms-btn cms-btn-ghost" onclick="closeModal('modal-cv-honor')">&times;</button>

      </div>

      <div class="cms-modal-body">

        <form id="form-cv-honor" onsubmit="saveCvHonorAction(event)">

          <div class="form-group">

            <label class="form-label">Honor / Distinction Title *</label>

            <input type="text" id="cv-h-title" class="cms-input" required>

          </div>

          <div class="form-row-2">

            <div class="form-group">

              <label class="form-label">Organization / Awarding Body *</label>

              <input type="text" id="cv-h-org" class="cms-input" required>

            </div>

            <div class="form-group">

              <label class="form-label">Award Year *</label>

              <input type="text" id="cv-h-year" class="cms-input" value="2026" required>

            </div>

          </div>

          <div class="form-row-2">

            <div class="form-group">

              <label class="form-label">Badge Tag (e.g. National Competitive, Provincial)</label>

              <input type="text" id="cv-h-badge" class="cms-input" placeholder="National Competitive">

            </div>

            <div class="form-group">

              <label class="form-label">Verification / News Link</label>

              <input type="text" id="cv-h-url" class="cms-input" placeholder="https://...">

            </div>

          </div>

          <div class="form-group">

            <label class="form-label">Achievement Summary / Impact</label>

            <textarea id="cv-h-details" class="cms-textarea" rows="3"></textarea>

          </div>

          <div class="form-group">

            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;">

              <input type="checkbox" id="cv-h-featured">

              <span style="font-size: 0.84rem; font-weight: 700; color: #fef08a;">★ Set as Active Homepage Spotlight</span>

            </label>

          </div>

          <div class="cms-modal-footer">

            <button type="button" class="cms-btn cms-btn-ghost" onclick="closeModal('modal-cv-honor')">Cancel</button>

            <button type="submit" class="cms-btn cms-btn-primary">Save Honor / Award</button>

          </div>

        </form>

      </div>

    </div>

  </div>

  <!-- Modal: Generic CV Item (Leadership, Education, Experience, Certification, Reference) -->

  <div class="cms-modal-backdrop" id="modal-cv-generic">

    <div class="cms-modal-dialog">

      <div class="cms-modal-header">

        <h3 class="cms-modal-title" id="modal-cv-generic-heading">Edit CV Item</h3>

        <button class="cms-btn cms-btn-ghost" onclick="closeModal('modal-cv-generic')">&times;</button>

      </div>

      <div class="cms-modal-body">

        <form id="form-cv-generic" onsubmit="saveCvGenericAction(event)">

          <div class="form-group">

            <label class="form-label" id="cv-gen-lbl-1">Title / Role / Degree *</label>

            <input type="text" id="cv-gen-field-1" class="cms-input" required>

          </div>

          <div class="form-row-2">

            <div class="form-group">

              <label class="form-label" id="cv-gen-lbl-2">Institution / Organization *</label>

              <input type="text" id="cv-gen-field-2" class="cms-input" required>

            </div>

            <div class="form-group">

              <label class="form-label" id="cv-gen-lbl-3">Period / Year *</label>

              <input type="text" id="cv-gen-field-3" class="cms-input" required>

            </div>

          </div>

          <div class="form-group">

            <label class="form-label" id="cv-gen-lbl-4">Details / Distinction / Responsibilities</label>

            <textarea id="cv-gen-field-4" class="cms-textarea" rows="3"></textarea>

          </div>

          <div class="form-group" id="cv-gen-extra-group" style="display: none;">

            <label class="form-label" id="cv-gen-lbl-5">Extra Info (e.g. Email / Phone)</label>

            <input type="text" id="cv-gen-field-5" class="cms-input">

          </div>

          <div class="cms-modal-footer">

            <button type="button" class="cms-btn cms-btn-ghost" onclick="closeModal('modal-cv-generic')">Cancel</button>

            <button type="submit" class="cms-btn cms-btn-primary">Save Item</button>

          </div>

        </form>

      </div>

    </div>

  </div>
  <!-- Modal: CV Academic Referee -->
  <div class="cms-modal-backdrop" id="modal-cv-referee">
    <div class="cms-modal-dialog">
      <div class="cms-modal-header">
        <h3 class="cms-modal-title" id="modal-cv-referee-heading">Edit Academic Reference</h3>
        <button class="cms-btn cms-btn-ghost" onclick="closeModal('modal-cv-referee')">&times;</button>
      </div>
      <div class="cms-modal-body">
        <form id="form-cv-referee" onsubmit="saveCvRefereeAction(event)">
          <div class="form-group">
            <label class="form-label">Referee Full Name &amp; Academic Title *</label>
            <input type="text" id="ref-form-name" class="cms-input" placeholder="e.g. Assoc. Prof. Dr. Nazlena Mohamad Ali" required>
          </div>
          <div class="form-row-2">
            <div class="form-group">
              <label class="form-label">Designation &amp; Academic Role *</label>
              <input type="text" id="ref-form-role" class="cms-input" placeholder="e.g. Head of Research &amp; Innovation" required>
            </div>
            <div class="form-group">
              <label class="form-label">Institution &amp; Department / Faculty *</label>
              <input type="text" id="ref-form-institution" class="cms-input" placeholder="e.g. Universiti Kebangsaan Malaysia (UKM)" required>
            </div>
          </div>
          <div class="form-row-2">
            <div class="form-group">
              <label class="form-label">Official Email Address *</label>
              <input type="email" id="ref-form-email" class="cms-input" placeholder="e.g. nazlena.ali@ukm.edu.my" required>
            </div>
            <div class="form-group">
              <label class="form-label">Telephone / Phone Coordinates</label>
              <input type="text" id="ref-form-phone" class="cms-input" placeholder="e.g. +603-8927 2413">
            </div>
          </div>
          <div class="cms-modal-footer">
            <button type="button" class="cms-btn cms-btn-ghost" onclick="closeModal('modal-cv-referee')">Cancel</button>
            <button type="submit" class="cms-btn cms-btn-primary">Save Academic Reference</button>
          </div>
        </form>
      </div>
    </div>
  </div>


  <!-- =============================================================

       6. JAVASCRIPT ENGINE (100% Connected to All Data Stores)

       ============================================================= -->

  <script>

    // Global Studio State

    let activeModule = 'articles';

    let activeArticlesSubTab = 'essays';

    let activeTalksCategory = 'talkshows';

    let activeCvSection = 'achievements_and_grants';

    let articlesData = [];

    let pubsData = [];

    let mediaTalksData = { talkshows: [], keynotes: [], opinions: [] };

    let cvData = {};

    let researchData = { vision: '', pillars: [], active_grant_themes: [] };

    let supervisionData = { heading: '', subheading: '', statement: '', open_topics: [] };

    let profileData = {};

    let currentSpotlight = { source: 'publication', id: '', title: '' };

    let editingArticleId = null;

    let editingPubId = null;

    let editingTalkshowId = null;

    let editingKeynoteId = null;

    let editingOpinionId = null;

    let editingCvHonorKey = null;

    let editingCvGenericKey = null;

    // Password & Auth Configuration

    const MASTER_PASSKEY = "ZaidAmin@Academic2026!";
    window.currentAdminKey = MASTER_PASSKEY;

    window.addEventListener('DOMContentLoaded', () => {

      checkAdminSession();

    });

    function checkAdminSession() {

      const auth = sessionStorage.getItem('zaidamin_admin_auth');

      if (auth === 'true') {

        document.getElementById('cms-lock-screen').style.display = 'none';

        initStudio();

      } else {

        document.getElementById('cms-lock-screen').style.display = 'flex';

      }

    }

    function handleAdminLogin(e) {

      e.preventDefault();

      const val = document.getElementById('vault-key-input').value;

      if (val === MASTER_PASSKEY) {

        sessionStorage.setItem('zaidamin_admin_auth', 'true');

        document.getElementById('cms-lock-screen').style.display = 'none';

        showToast('Vault Unlocked. Welcome, Dr. Zaid Amin.');

        initStudio();

      } else {

        const err = document.getElementById('vault-error-msg');

        err.style.display = 'block';

        err.textContent = 'Invalid Master Passkey. Access Denied.';

      }

    }

    function lockStudio() {

      sessionStorage.removeItem('zaidamin_admin_auth');

      document.getElementById('cms-lock-screen').style.display = 'flex';

      document.getElementById('vault-key-input').value = '';

      showToast('Studio Locked.');

    }

    // Modal Helpers

    function openModal(id) {

      const m = document.getElementById(id);

      if (m) m.classList.add('active');

    }

    function closeModal(id) {

      const m = document.getElementById(id);

      if (m) m.classList.remove('active');

    }

    function showToast(msg) {

      const t = document.getElementById('cms-toast');

      if (t) {

        t.textContent = msg;

        t.style.display = 'block';

        setTimeout(() => { t.style.display = 'none'; }, 3500);

      }

    }

    // Module Switcher

    function switchModule(mod) {

      activeModule = mod;

      document.querySelectorAll('.cms-module-btn').forEach(b => b.classList.remove('active'));

      document.querySelectorAll('.module-panel').forEach(p => p.classList.remove('active'));

      const btn = document.getElementById('btn-mod-' + mod);

      const panel = document.getElementById('panel-' + mod);

      if (btn) btn.classList.add('active');

      if (panel) panel.classList.add('active');

      updateCreateButtonLabel();

      if (mod === 'telemetry') {

        loadTelemetryData();

      }

    }

    function updateCreateButtonLabel() {

      const lbl = document.getElementById('nav-btn-create-label');

      if (!lbl) return;

      if (activeModule === 'articles') {

        lbl.textContent = activeArticlesSubTab === 'essays' ? 'New Article' : 'New Pillar';

      } else if (activeModule === 'pubs') {

        lbl.textContent = 'New Publication';

      } else if (activeModule === 'talks') {

        if (activeTalksCategory === 'talkshows') lbl.textContent = 'New Video';

        else if (activeTalksCategory === 'keynotes') lbl.textContent = 'New Keynote';

        else lbl.textContent = 'New Opinion';

      } else if (activeModule === 'cv') {

        lbl.textContent = activeCvSection === 'achievements_and_grants' ? 'New Honor' : 'New CV Item';

      } else if (activeModule === 'supervision') {

        lbl.textContent = 'New Research Topic';

      } else if (activeModule === 'profile') {

        lbl.textContent = 'Save Profile';

      } else if (activeModule === 'telemetry') {

        lbl.textContent = 'Save Telemetry';

      }

    }

    function openCreateModalForActiveModule() {

      if (activeModule === 'articles') {

        if (activeArticlesSubTab === 'essays') openNewArticleEditor();

        else openPillarModal(null);

      } else if (activeModule === 'pubs') {

        resetPubModal();

        openModal('modal-pub');

      } else if (activeModule === 'talks') {

        openActiveTalkCategoryModal();

      } else if (activeModule === 'cv') {

        openActiveCvModal();

      } else if (activeModule === 'supervision') {

        openSupervisionTopicModal(null);

      } else if (activeModule === 'profile') {

        saveGlobalProfile();

      } else if (activeModule === 'telemetry') {

        saveAnalyticsCalibration();

      }

    }

    // -------------------------------------------------------------

    // DATA INITIALIZATION ENGINE

    // -------------------------------------------------------------

    async function initStudio() {

      try {

        await Promise.all([

          loadSpotlightData(),

          loadArticlesData(),

          loadPubsData(),

          loadMediaTalksData(),

          loadCvData(),

          loadResearchData(),

          loadSupervisionData(),

          loadProfileData()

        ]);

        updateAllCounts();

      } catch (e) {

        console.error("Init Studio Error:", e);

      }

    }

    function updateAllCounts() {

      document.getElementById('count-articles').textContent = (articlesData.length + 5);

      document.getElementById('count-art-essays').textContent = articlesData.length;

      document.getElementById('count-art-pillars').textContent = 5;

      document.getElementById('count-pubs').textContent = pubsData.length;

      const tsCount = (mediaTalksData.talkshows || []).length;

      const knCount = (mediaTalksData.keynotes || []).length;

      const opCount = (mediaTalksData.opinions || []).length;

      document.getElementById('count-talks').textContent = (tsCount + knCount + opCount);

      document.getElementById('count-talkshows').textContent = tsCount;

      document.getElementById('count-keynotes').textContent = knCount;

      document.getElementById('count-opinions').textContent = opCount;

      const hCount = (cvData.achievements_and_grants || []).length;

      const lCount = (cvData.academic_leadership || []).length;

      const eCount = (cvData.education || []).length;

      const wCount = (cvData.work_experience || []).length;

      const cCount = (cvData.professional_certifications || []).length;

      const rCount = (cvData.academic_references || []).length;

      const totalCv = hCount + lCount + eCount + wCount + cCount + rCount;

      document.getElementById('count-cv').textContent = totalCv;

      document.getElementById('count-cv-honors').textContent = hCount;

      document.getElementById('count-cv-leadership').textContent = lCount;

      document.getElementById('count-cv-education').textContent = eCount;

      document.getElementById('count-cv-experience').textContent = wCount;

      document.getElementById('count-cv-certs').textContent = cCount;

      document.getElementById('count-cv-refs').textContent = rCount;

      const sCount = (supervisionData.open_topics || []).length;

      document.getElementById('count-supervision').textContent = sCount;

    }

    // -------------------------------------------------------------

    // SPOTLIGHT ENGINE

    // -------------------------------------------------------------

    async function loadSpotlightData() {

      try {

        const res = await fetch('data/spotlight.json?t=' + Date.now());

        if (res.ok) {

          currentSpotlight = await res.json();

          document.getElementById('spotlight-title-display').textContent = currentSpotlight.title || 'Trustworthy AI for Sustainable Cities...';

          document.getElementById('spotlight-source-display').textContent = (currentSpotlight.source || 'PUBLICATION').toUpperCase();

          const pTitle = document.getElementById('prof-spotlight-active-title');

          const pSrc = document.getElementById('prof-spotlight-active-source');

          if (pTitle) pTitle.textContent = currentSpotlight.title || '';

          if (pSrc) pSrc.textContent = (currentSpotlight.source || 'PUBLICATION').toUpperCase();

        }

      } catch (e) {}

    }

    async function setHomepageSpotlight(source, id, title) {

      if (!confirm(`Set this item as the active Universal Homepage Spotlight?`)) return;

      try {

        const res = await fetch('/api/set-homepage-spotlight', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY },

          body: JSON.stringify({ source, id, title, deploy: false })

        });

        if (res.ok) {

          showToast(`Homepage Spotlight updated to: ${title}`);

          await loadSpotlightData();

          renderArticlesTable(articlesData);

          renderPubsTable(pubsData);

          renderCvHonorsTable(cvData.achievements_and_grants || []);

        } else {

          showToast('Failed to update spotlight.', true);

        }

      } catch (e) {

        showToast('Spotlight update error: ' + e, true);

      }

    }

    // -------------------------------------------------------------

    // 1. ARTICLES & ESSAYS (Activity & Project)

    // -------------------------------------------------------------

    async function loadArticlesData() {

      const res = await fetch('data/articles.json?t=' + Date.now());

      if (res.ok) {

        articlesData = await res.json();

        renderArticlesTable(articlesData);

      }

    }

    function switchArticlesSubTab(sub) {

      activeArticlesSubTab = sub;

      document.getElementById('subtab-btn-art-essays').classList.toggle('active', sub === 'essays');

      document.getElementById('subtab-btn-art-pillars').classList.toggle('active', sub === 'pillars');

      document.getElementById('articles-subpane-essays').style.display = sub === 'essays' ? 'block' : 'none';

      document.getElementById('articles-subpane-pillars').style.display = sub === 'pillars' ? 'block' : 'none';

      updateCreateButtonLabel();

    }

    function renderArticlesTable(list) {

      const tbody = document.getElementById('articles-tbody');

      tbody.innerHTML = list.map((a, i) => {

        const isSpotlight = (currentSpotlight.source === 'article' && (currentSpotlight.id === a.id || currentSpotlight.title === a.title)) || a.featured;

        const spotlightHtml = isSpotlight

          ? '<span class="spotlight-active-badge">★ ACTIVE SPOTLIGHT</span>'

          : `<button type="button" class="btn-set-spotlight" onclick="setHomepageSpotlight('article', '${a.id}', '${escapeQuotes(a.title)}')">★ Spotlight</button>`;

        return `

        <tr>

          <td style="color: #64748b; font-weight: 700;">${i + 1}</td>

          <td>

            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">

              <span style="font-weight: 700; color: #ffffff;">${escapeHTML(a.title)}</span>

              ${spotlightHtml}

            </div>

            <div style="font-size: 0.75rem; color: #64748b; font-family: monospace; margin-top: 3px;">${escapeHTML(a.id)}</div>

          </td>

          <td><span style="background: rgba(56, 189, 248, 0.12); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.25); padding: 3px 8px; border-radius: 999px; font-size: 0.72rem; font-weight: 700;">${escapeHTML(a.category || 'General')}</span></td>

          <td style="color: #94a3b8; font-size: 0.82rem; white-space: nowrap;">${escapeHTML(a.date || '2026')}</td>

          <td style="color: #94a3b8; font-size: 0.82rem; white-space: nowrap;">${escapeHTML(a.reading_time || '3 min')}</td>

          <td style="text-align: right; white-space: nowrap;">

            <button class="cms-btn cms-btn-ghost" style="padding: 4px 10px; font-size: 0.75rem;" onclick="editArticle('${a.id}')">Edit</button>

            <a href="article.html?id=${a.id}" target="_blank" class="cms-btn cms-btn-ghost" style="padding: 4px 10px; font-size: 0.75rem;">View</a>

            <button class="cms-btn cms-btn-danger" style="padding: 4px 8px; font-size: 0.75rem;" onclick="deleteArticle('${a.id}')">&times;</button>

          </td>

        </tr>`;

      }).join('');

    }

    function filterArticlesTable() {

      const q = document.getElementById('articles-search-input').value.toLowerCase();

      const cat = document.getElementById('articles-cat-filter').value;

      const filtered = articlesData.filter(a => {

        const mQ = !q || (a.title && a.title.toLowerCase().includes(q)) || (a.excerpt && a.excerpt.toLowerCase().includes(q));

        const mCat = !cat || a.category === cat;

        return mQ && mCat;

      });

      renderArticlesTable(filtered);

    }

    // -------------------------------------------------------------

    // RESEARCH PILLARS & ACTIVE GRANTS

    // -------------------------------------------------------------

    async function loadResearchData() {

      try {

        const res = await fetch('data/research.json?t=' + Date.now());

        if (res.ok) {

          researchData = await res.json();

          document.getElementById('research-vision-input').value = researchData.vision || '';

          renderPillarsCards(researchData.pillars || []);

          renderGrantsCards(researchData.active_grant_themes || []);

        }

      } catch (e) {}

    }

    function renderPillarsCards(pillars) {

      const c = document.getElementById('pillars-container');

      c.innerHTML = pillars.map((p, i) => `

        <div class="cms-feature-card" style="display: flex; flex-direction: column; justify-content: space-between;">

          <div>

            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">

              <div style="font-size: 1.5rem;">${p.icon || '🏛️'}</div>

              <div style="display: flex; gap: 6px;">

                <button class="cms-btn cms-btn-ghost" style="padding: 3px 8px; font-size: 0.74rem;" onclick="openPillarModal(${i})">Edit</button>

                <button class="cms-btn cms-btn-ghost" style="padding: 3px 8px; font-size: 0.74rem; color: #f87171;" onclick="deletePillar(${i})">Del</button>

              </div>

            </div>

            <h4 style="font-family: var(--font-cinzel); font-size: 1rem; color: #ffffff; margin: 0 0 6px 0;">${escapeHTML(p.title)}</h4>

            <p style="font-size: 0.82rem; color: #bae6fd; font-weight: 600; margin: 0 0 8px 0;">${escapeHTML(p.short_desc || '')}</p>

            <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.5; margin: 0 0 12px 0;">${escapeHTML(p.full_desc || '')}</p>

            <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 8px;">

              ${(p.key_topics || []).map(t => `<span style="background: rgba(255,255,255,0.06); font-size: 0.70rem; padding: 2px 6px; border-radius: 4px; color: #94a3b8;">${escapeHTML(t)}</span>`).join('')}

            </div>

          </div>

          ${p.grant_alignment ? `<div style="font-size: 0.72rem; color: var(--gold-accent); margin-top: 8px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 6px;">Target: ${escapeHTML(p.grant_alignment)}</div>` : ''}

        </div>

      `).join('');

    }

    function renderGrantsCards(grants) {

      const c = document.getElementById('grants-container');

      c.innerHTML = grants.map((g, i) => `

        <div class="cms-feature-card" style="display: flex; flex-direction: column; justify-content: space-between;">

          <div>

            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">

              <h4 style="font-family: var(--font-cinzel); font-size: 1rem; color: #ffffff; margin: 0;">${escapeHTML(g.title)}</h4>

              <div style="display: flex; gap: 6px; align-items: center;">

                <span style="background: rgba(56, 189, 248, 0.15); color: var(--cyan-accent); font-size: 0.70rem; font-weight: 700; padding: 2px 7px; border-radius: 999px;">${escapeHTML(g.period || '')}</span>

                <button class="cms-btn cms-btn-ghost" style="padding: 3px 8px; font-size: 0.74rem;" onclick="openGrantModal(${i})">Edit</button>

                <button class="cms-btn cms-btn-ghost" style="padding: 3px 8px; font-size: 0.74rem; color: #f87171;" onclick="deleteGrant(${i})">Del</button>

              </div>

            </div>

            <div style="font-size: 0.82rem; color: var(--gold-accent); font-weight: 700; margin-bottom: 8px;">${escapeHTML(g.role || '')} &bull; ${escapeHTML(g.agency || '')}</div>

            <p style="font-size: 0.84rem; color: var(--text-muted); line-height: 1.5; margin: 0;">${escapeHTML(g.objective || '')}</p>

          </div>

        </div>

      `).join('');

    }

    async function saveResearchVision() {

      const v = document.getElementById('research-vision-input').value;

      researchData.vision = v;

      try {

        const res = await fetch('/api/save-research', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY },

          body: JSON.stringify({ research: researchData, deploy: false })

        });

        if (res.ok) showToast('Research vision saved successfully.');

        else showToast('Failed to save vision', true);

      } catch (e) { showToast('Error: ' + e, true); }

    }

    // -------------------------------------------------------------

    // 2. PUBLICATIONS (Research & Publication)

    // -------------------------------------------------------------

    async function loadPubsData() {

      const res = await fetch('data/publications.json?t=' + Date.now());

      if (res.ok) {

        pubsData = await res.json();

        renderPubsTable(pubsData);

      }

    }

    function updatePubCoverPreview() {

      const val = document.getElementById('pub-form-image').value.trim();

      const imgEl = document.getElementById('pub-cover-preview-img');

      const emptyEl = document.getElementById('pub-cover-preview-empty');

      if (val) {

        imgEl.src = val;

        imgEl.style.display = 'block';

        emptyEl.style.display = 'none';

      } else {

        imgEl.src = '';

        imgEl.style.display = 'none';

        emptyEl.style.display = 'block';

      }

    }

    function updateKnCoverPreview() {
      const val = (document.getElementById('kn-form-image') ? document.getElementById('kn-form-image').value : '').trim();
      const img = document.getElementById('kn-cover-preview-img');
      const empty = document.getElementById('kn-cover-preview-empty');
      if (!img || !empty) return;
      if (val) {
        img.src = val;
        img.style.display = 'block';
        empty.style.display = 'none';
      } else {
        img.src = '';
        img.style.display = 'none';
        empty.style.display = 'block';
      }
    }

    function updateOpCoverPreview() {

      const val = (document.getElementById('op-form-image') ? document.getElementById('op-form-image').value : '').trim();

      const img = document.getElementById('op-cover-preview-img');

      const empty = document.getElementById('op-cover-preview-empty');

      if (!img || !empty) return;

      if (val) {

        img.src = val;

        img.style.display = 'block';

        empty.style.display = 'none';

      } else {

        img.src = '';

        img.style.display = 'none';

        empty.style.display = 'block';

      }

    }

    function updateTsCoverPreview() {

      const val = (document.getElementById('ts-form-poster') ? document.getElementById('ts-form-poster').value : '').trim();

      const img = document.getElementById('ts-cover-preview-img');

      const empty = document.getElementById('ts-cover-preview-empty');

      if (!img || !empty) return;

      if (val) {

        img.src = val;

        img.style.display = 'block';

        empty.style.display = 'none';

      } else {

        img.src = '';

        img.style.display = 'none';

        empty.style.display = 'block';

      }

    }

    

    async function openBooksHeroModal() {

      try {

        const res = await fetch('/api/books-hero');

        let hero = {};

        if (res.ok) hero = await res.json();

        document.getElementById('hero-form-kicker').value = hero.kicker || '01 / 04 • MONOGRAPHS & CHAPTERS';

        document.getElementById('hero-form-prefix').value = hero.headline_prefix || 'Explore Research';

        document.getElementById('hero-form-highlight').value = hero.headline_highlight || 'Monographs & Chapters';

        document.getElementById('hero-form-desc').value = hero.description || '';

        document.getElementById('hero-form-badges').value = (hero.publisher_badges || []).join(', ');

        openModal('modal-books-hero');

      } catch (err) {

        showToast('Error loading hero settings: ' + err.message, 'error');

      }

    }

    async function saveBooksHero(e) {

      e.preventDefault();

      const hero = {

        kicker: document.getElementById('hero-form-kicker').value.trim(),

        headline_prefix: document.getElementById('hero-form-prefix').value.trim(),

        headline_highlight: document.getElementById('hero-form-highlight').value.trim(),

        description: document.getElementById('hero-form-desc').value.trim(),

        publisher_badges: document.getElementById('hero-form-badges').value.split(',').map(s => s.trim()).filter(Boolean)

      };

      try {

        const res = await fetch('/api/save-books-hero', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json' },

          body: JSON.stringify({ hero: hero })

        });

        const data = await res.json();

        if (data.status === 'ok') {

          showToast('Monograph Hero Stage updated and site rebuilt!');

          closeModal('modal-books-hero');

        } else {

          showToast('Error: ' + (data.error || 'Failed to save'), 'error');

        }

      } catch (err) {

        showToast('Save failed: ' + err.message, 'error');

      }

    }

    function renderPubsTable(list) {

      const tbody = document.getElementById('pubs-tbody');

      tbody.innerHTML = list.map((p, i) => {

        const isBook = p.category === 'Book Chapter';

        const isSpotlight = (currentSpotlight.source === 'publication' && (currentSpotlight.id === p.id || currentSpotlight.title === p.title)) || p.featured;

        

        let badgeHtml = '';

        if (isBook && p.featured) {

          badgeHtml = '<span class="spotlight-active-badge" style="background: rgba(212,175,55,0.22); color: #fef08a; border-color: #d4af37;">★ PRIMARY MONOGRAPH</span>';

        } else if (isSpotlight) {

          badgeHtml = '<span class="spotlight-active-badge">★ ACTIVE SPOTLIGHT</span>';

        } else if (isBook) {

          badgeHtml = `<button type="button" class="btn-set-spotlight" style="border-color: rgba(212,175,55,0.4); color: #fef08a;" onclick="setPrimaryMonograph('${p.id}')">★ Set Primary</button>`;

        } else {

          badgeHtml = `<button type="button" class="btn-set-spotlight" onclick="setHomepageSpotlight('publication', '${p.id}', '${escapeQuotes(p.title)}')">★ Spotlight</button>`;

        }

        const thumbHtml = p.image ? `<img src="${escapeHTML(p.image)}" style="width: 28px; height: 38px; object-fit: cover; border-radius: 3px; border: 1px solid rgba(212,175,55,0.4); flex-shrink: 0;" onerror="this.style.display='none'">` : '';

        return `

        <tr>

          <td style="color: #64748b; font-weight: 700;">${i + 1}</td>

          <td>

            <div style="display: flex; align-items: center; gap: 10px;">

              ${thumbHtml}

              <div style="flex: 1; min-width: 0;">

                <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">

                  <span style="font-weight: 700; color: #ffffff;">${escapeHTML(p.title)}</span>

                  ${badgeHtml}

                </div>

                <div style="font-size: 0.75rem; color: #64748b; font-family: monospace; margin-top: 3px;">${escapeHTML(p.id)}</div>

              </div>

            </div>

          </td>

          <td><span style="background: rgba(56, 189, 248, 0.12); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.25); padding: 3px 8px; border-radius: 999px; font-size: 0.72rem; font-weight: 700;">${escapeHTML(p.category || 'Journal')}</span></td>

          <td style="color: #bae6fd; font-size: 0.82rem;">${escapeHTML(p.venue || '')}</td>

          <td style="color: #94a3b8; font-size: 0.82rem; white-space: nowrap;">${escapeHTML(p.year || '2026')}</td>

          <td style="text-align: right; white-space: nowrap;">

            <button class="cms-btn cms-btn-ghost" style="padding: 4px 10px; font-size: 0.75rem;" onclick="editPublication('${p.id}')">Edit</button>

            <button class="cms-btn cms-btn-danger" style="padding: 4px 8px; font-size: 0.75rem;" onclick="deletePublication('${p.id}')">&times;</button>

          </td>

        </tr>`;

      }).join('');

    }

    async function setPrimaryMonograph(pubId) {

      const pub = pubsData.find(p => p.id === pubId);

      if (!pub) return;

      pubsData.forEach(p => {

        if (p.category === 'Book Chapter') p.featured = (p.id === pubId);

      });

      pub.featured = true;

      try {

        const res = await fetch('/api/save-publication', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY },

          body: JSON.stringify({ publication: pub, deploy: false })

        });

        if (res.ok) {

          showToast(`Set "${pub.title.substring(0, 30)}..." as Primary Monograph.`);

          renderPubsTable(pubsData);

        }

      } catch (e) {

        showToast('Error setting primary monograph: ' + e, true);

      }

    }

    function filterPubsTable() {

      const q = document.getElementById('pubs-search-input').value.toLowerCase();

      const cat = document.getElementById('pubs-cat-filter').value;

      const filtered = pubsData.filter(p => {

        const mQ = !q || (p.title && p.title.toLowerCase().includes(q)) || (p.venue && p.venue.toLowerCase().includes(q));

        const mCat = !cat || (p.category && p.category.toLowerCase().includes(cat.toLowerCase()));

        return mQ && mCat;

      });

      renderPubsTable(filtered);

    }

    function resetPubModal() {

      editingPubId = null;

      document.getElementById('modal-pub-heading').textContent = 'Add Publication';

      document.getElementById('pub-form-title').value = '';

      document.getElementById('pub-form-id').value = 'amin' + new Date().getFullYear() + 'pub';

      document.getElementById('pub-form-venue').value = '';

      document.getElementById('pub-form-year').value = '2026';

      document.getElementById('pub-form-doi').value = '';

      document.getElementById('pub-form-citations').value = '';

      document.getElementById('pub-form-authors').value = 'Zaid Amin';

      document.getElementById('pub-form-abstract').value = '';

      document.getElementById('pub-form-image').value = '';

      document.getElementById('pub-form-featured').checked = false;

      updatePubCoverPreview();

    }

    function editPublication(id) {

      const pub = pubsData.find(p => p.id === id);

      if (!pub) return;

      editingPubId = id;

      document.getElementById('modal-pub-heading').textContent = 'Edit Publication';

      document.getElementById('pub-form-title').value = pub.title || '';

      document.getElementById('pub-form-id').value = pub.id || '';

      document.getElementById('pub-form-cat').value = pub.category || 'Journal';

      document.getElementById('pub-form-venue').value = pub.venue || '';

      document.getElementById('pub-form-year').value = pub.year || '2026';

      document.getElementById('pub-form-doi').value = pub.doi || pub.url || '';

      document.getElementById('pub-form-citations').value = pub.citations || '';

      document.getElementById('pub-form-authors').value = pub.authors || '';

      document.getElementById('pub-form-abstract').value = pub.abstract || '';

      document.getElementById('pub-form-image').value = pub.image || '';

      document.getElementById('pub-form-featured').checked = !!pub.featured;

      updatePubCoverPreview();

      openModal('modal-pub');

    }

    async function savePublicationAction(e) {

      e.preventDefault();

      const existing = pubsData.find(p => p.id === (editingPubId || document.getElementById('pub-form-id').value.trim())) || {};

      const isBook = document.getElementById('pub-form-cat').value === 'Book Chapter';

      const isFeatured = document.getElementById('pub-form-featured').checked;

      if (isBook && isFeatured) {

        pubsData.forEach(p => {

          if (p.category === 'Book Chapter' && p.id !== document.getElementById('pub-form-id').value.trim()) {

            p.featured = false;

          }

        });

      }

      const item = {

        id: document.getElementById('pub-form-id').value.trim(),

        title: document.getElementById('pub-form-title').value.trim(),

        category: document.getElementById('pub-form-cat').value,

        venue: document.getElementById('pub-form-venue').value.trim(),

        year: parseInt(document.getElementById('pub-form-year').value.trim(), 10) || 2026,

        doi: document.getElementById('pub-form-doi').value.trim(),

        citations: document.getElementById('pub-form-citations').value.trim(),

        authors: document.getElementById('pub-form-authors').value.trim(),

        abstract: document.getElementById('pub-form-abstract').value.trim(),

        image: document.getElementById('pub-form-image').value.trim() || existing.image || '',

        featured: isFeatured,

        bibtex: existing.bibtex || ''

      };

      try {

        const res = await fetch('/api/save-publication', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY },

          body: JSON.stringify({ publication: item, deploy: false })

        });

        if (res.ok) {

          showToast('Publication saved successfully.');

          closeModal('modal-pub');

          await loadPubsData();

          updateAllCounts();

        } else {

          showToast('Failed to save publication.', true);

        }

      } catch (err) {

        showToast('Error: ' + err, true);

      }

    }

    async function deletePublication(id) {

      if (!confirm(`Delete publication '${id}'?`)) return;

      try {

        const res = await fetch('/api/delete-publication', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY },

          body: JSON.stringify({ id })

        });

        if (res.ok) {

          showToast('Publication deleted.');

          await loadPubsData();

          updateAllCounts();

        }

      } catch (e) { showToast('Error: ' + e, true); }

    }

    // -------------------------------------------------------------

    // 3. MEDIA & TALKS (talks.html - 3 Categories)

    // -------------------------------------------------------------

    async function loadMediaTalksData() {

      const res = await fetch('data/media_talks.json?t=' + Date.now());

      if (res.ok) {

        mediaTalksData = await res.json();

        renderTalkshowsTable(mediaTalksData.talkshows || []);

        renderKeynotesTable(mediaTalksData.keynotes || []);

        renderOpinionsTable(mediaTalksData.opinions || []);

      }

    }

    function switchTalksCategory(cat) {

      activeTalksCategory = cat;

      document.getElementById('subtab-btn-talkshows').classList.toggle('active', cat === 'talkshows');

      document.getElementById('subtab-btn-keynotes').classList.toggle('active', cat === 'keynotes');

      document.getElementById('subtab-btn-opinions').classList.toggle('active', cat === 'opinions');

      document.getElementById('media-table-talkshows').style.display = cat === 'talkshows' ? 'block' : 'none';

      document.getElementById('media-table-keynotes').style.display = cat === 'keynotes' ? 'block' : 'none';

      document.getElementById('media-table-opinions').style.display = cat === 'opinions' ? 'block' : 'none';

      updateCreateButtonLabel();

    }

    function renderTalkshowsTable(list) {

      const tbody = document.getElementById('talkshows-tbody');

      tbody.innerHTML = list.map((t, i) => `

        <tr>

          <td style="color: var(--cyan-accent); font-weight: 800; font-family: monospace;">${escapeHTML(t.episode_num || ('0' + (i + 1)))}</td>

          <td>

            <div style="font-weight: 700; color: #ffffff;">${escapeHTML(t.title)}</div>

            <div style="font-size: 0.75rem; color: #94a3b8;">${escapeHTML(t.channel || 'Broadcast')} &bull; ${escapeHTML(t.author_name || 'Dr. Zaid Amin')}</div>

          </td>

          <td><span style="background: rgba(56, 189, 248, 0.12); color: #38bdf8; padding: 2px 8px; border-radius: 999px; font-size: 0.70rem; font-weight: 700;">${escapeHTML(t.category_tag || 'Talkshow')}</span></td>

          <td style="color: var(--gold-accent); font-family: monospace; font-size: 0.80rem;">${escapeHTML(t.duration || '20:00')}</td>

          <td style="color: #94a3b8; font-size: 0.82rem;">${escapeHTML(t.date || '')}</td>

          <td style="text-align: right; white-space: nowrap;">

            <button class="cms-btn cms-btn-ghost" style="padding: 4px 10px; font-size: 0.75rem;" onclick="editTalkshow('${t.id}')">Edit</button>

            <a href="${t.video_url || '#'}" target="_blank" class="cms-btn cms-btn-ghost" style="padding: 4px 10px; font-size: 0.75rem;">Watch</a>

            <button class="cms-btn cms-btn-danger" style="padding: 4px 8px; font-size: 0.75rem;" onclick="deleteMediaTalk('talkshows', '${t.id}')">&times;</button>

          </td>

        </tr>

      `).join('');

    }

    function renderKeynotesTable(list) {

      const tbody = document.getElementById('keynotes-tbody');

      tbody.innerHTML = list.map((k, i) => `

        <tr>

          <td style="color: #64748b; font-weight: 700;">${i + 1}</td>

          <td>

            <div style="font-weight: 700; color: #ffffff;">${escapeHTML(k.title)}</div>

            <div style="font-size: 0.75rem; color: #bae6fd;">${escapeHTML(k.event || '')}</div>

          </td>

          <td><span style="background: rgba(212, 175, 55, 0.15); color: var(--gold-accent); padding: 2px 8px; border-radius: 999px; font-size: 0.70rem; font-weight: 700;">${escapeHTML(k.role || 'Keynote')}</span></td>

          <td style="color: #94a3b8; font-size: 0.82rem;">${escapeHTML(k.venue || '')}</td>

          <td style="color: #94a3b8; font-size: 0.82rem;">${escapeHTML(k.year || '2026')}</td>

          <td style="text-align: right; white-space: nowrap;">

            <button class="cms-btn cms-btn-ghost" style="padding: 4px 10px; font-size: 0.75rem;" onclick="editKeynote('${k.id}')">Edit</button>

            <button class="cms-btn cms-btn-danger" style="padding: 4px 8px; font-size: 0.75rem;" onclick="deleteMediaTalk('keynotes', '${k.id}')">&times;</button>

          </td>

        </tr>

      `).join('');

    }

    function renderOpinionsTable(list) {

      const tbody = document.getElementById('opinions-tbody');

      tbody.innerHTML = list.map((o, i) => `

        <tr>

          <td style="color: #64748b; font-weight: 700;">${i + 1}</td>

          <td>

            <div style="font-weight: 700; color: #ffffff;">${escapeHTML(o.title)}</div>

            <div style="font-size: 0.75rem; color: #94a3b8;">${escapeHTML(o.abstract ? o.abstract.substring(0, 80) + '...' : '')}</div>

          </td>

          <td><span style="background: rgba(56, 189, 248, 0.12); color: #38bdf8; padding: 2px 8px; border-radius: 999px; font-size: 0.70rem; font-weight: 700;">${escapeHTML(o.type || 'Opinion')}</span></td>

          <td style="color: #bae6fd; font-size: 0.82rem;">${escapeHTML(o.publication || '')}</td>

          <td style="color: #94a3b8; font-size: 0.82rem;">${escapeHTML(o.year || '2026')}</td>

          <td style="text-align: right; white-space: nowrap;">

            <button class="cms-btn cms-btn-ghost" style="padding: 4px 10px; font-size: 0.75rem;" onclick="editOpinion('${o.id}')">Edit</button>

            <button class="cms-btn cms-btn-danger" style="padding: 4px 8px; font-size: 0.75rem;" onclick="deleteMediaTalk('opinions', '${o.id}')">&times;</button>

          </td>

        </tr>

      `).join('');

    }

    function filterMediaTalksTable() {

      const q = document.getElementById('talks-search-input').value.toLowerCase();

      if (activeTalksCategory === 'talkshows') {

        const filtered = (mediaTalksData.talkshows || []).filter(t => !q || (t.title && t.title.toLowerCase().includes(q)) || (t.channel && t.channel.toLowerCase().includes(q)));

        renderTalkshowsTable(filtered);

      } else if (activeTalksCategory === 'keynotes') {

        const filtered = (mediaTalksData.keynotes || []).filter(k => !q || (k.title && k.title.toLowerCase().includes(q)) || (k.event && k.event.toLowerCase().includes(q)));

        renderKeynotesTable(filtered);

      } else {

        const filtered = (mediaTalksData.opinions || []).filter(o => !q || (o.title && o.title.toLowerCase().includes(q)) || (o.publication && o.publication.toLowerCase().includes(q)));

        renderOpinionsTable(filtered);

      }

    }

    function openActiveTalkCategoryModal() {

      if (activeTalksCategory === 'talkshows') {

        editingTalkshowId = null;

        document.getElementById('modal-talkshow-heading').textContent = 'Add Talkshow Video';

        document.getElementById('form-talkshow').reset();

        document.getElementById('ts-form-ep').value = '0' + ((mediaTalksData.talkshows || []).length + 1);

        updateTsCoverPreview();

        openModal('modal-talkshow');

      } else if (activeTalksCategory === 'keynotes') {

        editingKeynoteId = null;

        document.getElementById('modal-keynote-heading').textContent = 'Add Keynote Address';

        document.getElementById('form-keynote').reset();

        document.getElementById('kn-form-image').value = 'assets/images/spotlight-smart-cities.jpg';

        updateKnCoverPreview();

        openModal('modal-keynote');

      } else {

        editingOpinionId = null;

        document.getElementById('modal-opinion-heading').textContent = 'Add Opinion Essay';

        document.getElementById('form-opinion').reset();

        document.getElementById('op-form-image').value = 'assets/images/thumb-attention.jpg';

        updateOpCoverPreview();

        openModal('modal-opinion');

      }

    }

    function editTalkshow(id) {

      const t = (mediaTalksData.talkshows || []).find(x => x.id === id);

      if (!t) return;

      editingTalkshowId = id;

      document.getElementById('modal-talkshow-heading').textContent = 'Edit Talkshow Video';

      document.getElementById('ts-form-ep').value = t.episode_num || '';

      document.getElementById('ts-form-channel').value = t.channel || '';

      document.getElementById('ts-form-title').value = t.title || '';

      document.getElementById('ts-form-tag').value = t.category_tag || '';

      document.getElementById('ts-form-date').value = t.date || '';

      document.getElementById('ts-form-duration').value = t.duration || '';

      document.getElementById('ts-form-video-url').value = t.video_url || '';

      document.getElementById('ts-form-embed-url').value = t.embed_url || '';

      document.getElementById('ts-form-poster').value = t.poster || '';

      updateTsCoverPreview();

      document.getElementById('ts-form-desc').value = t.description || '';

      openModal('modal-talkshow');

    }

    async function saveTalkshowAction(e) {

      e.preventDefault();

      const item = {

        id: editingTalkshowId || ('talkshow-' + Date.now()),

        episode_num: document.getElementById('ts-form-ep').value.trim(),

        channel: document.getElementById('ts-form-channel').value.trim(),

        title: document.getElementById('ts-form-title').value.trim(),

        category_tag: document.getElementById('ts-form-tag').value.trim(),

        date: document.getElementById('ts-form-date').value.trim(),

        duration: document.getElementById('ts-form-duration').value.trim(),

        video_url: document.getElementById('ts-form-video-url').value.trim(),

        embed_url: document.getElementById('ts-form-embed-url').value.trim(),

        poster: document.getElementById('ts-form-poster').value.trim(),

        description: document.getElementById('ts-form-desc').value.trim(),

        author_name: "Dr. Zaid Amin",

        author_avatar: "assets/images/portraits/portrait-1.webp"

      };

      try {

        const res = await fetch('/api/save-media-talk', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY },

          body: JSON.stringify({ category: 'talkshows', item, deploy: false })

        });

        if (res.ok) {

          showToast('Talkshow saved.');

          closeModal('modal-talkshow');

          await loadMediaTalksData();

          updateAllCounts();

        }

      } catch (err) { showToast('Error: ' + err, true); }

    }

    function editKeynote(id) {

      const k = (mediaTalksData.keynotes || []).find(x => x.id === id);

      if (!k) return;

      editingKeynoteId = id;

      document.getElementById('modal-keynote-heading').textContent = 'Edit Keynote Address';

      document.getElementById('kn-form-title').value = k.title || '';

      document.getElementById('kn-form-role').value = k.role || '';

      document.getElementById('kn-form-badge').value = k.badge || '';

      document.getElementById('kn-form-event').value = k.event || '';

      document.getElementById('kn-form-venue').value = k.venue || '';

      document.getElementById('kn-form-date').value = k.date_display || '';

      document.getElementById('kn-form-abstract').value = k.abstract || '';

      document.getElementById('kn-form-url').value = k.url || '';

      document.getElementById('kn-form-image').value = k.image || 'assets/images/spotlight-smart-cities.jpg';

      updateKnCoverPreview();

      openModal('modal-keynote');

    }

    async function saveKeynoteAction(e) {

      e.preventDefault();

      const existingK = (mediaTalksData.keynotes || []).find(x => x.id === editingKeynoteId) || {};

      const item = {

        id: editingKeynoteId || ('keynote-' + Date.now()),

        title: document.getElementById('kn-form-title').value.trim(),

        role: document.getElementById('kn-form-role').value.trim(),

        badge: document.getElementById('kn-form-badge').value.trim(),

        event: document.getElementById('kn-form-event').value.trim(),

        venue: document.getElementById('kn-form-venue').value.trim(),

        year: (document.getElementById('kn-form-date').value.match(/\\d{4}/) || ['2026'])[0],

        date_display: document.getElementById('kn-form-date').value.trim(),

        abstract: document.getElementById('kn-form-abstract').value.trim(),

        url: document.getElementById('kn-form-url').value.trim(),

        palette: existingK.palette || "ivory",

        arch_style: existingK.arch_style || "arch-cathedral",

        image: document.getElementById('kn-form-image').value.trim() || existingK.image || "assets/images/spotlight-smart-cities.jpg"

      };

      try {

        const res = await fetch('/api/save-media-talk', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY },

          body: JSON.stringify({ category: 'keynotes', item, deploy: false })

        });

        if (res.ok) {

          showToast('Keynote saved.');

          closeModal('modal-keynote');

          await loadMediaTalksData();

          updateAllCounts();

        }

      } catch (err) { showToast('Error: ' + err, true); }

    }

    function editOpinion(id) {

      const o = (mediaTalksData.opinions || []).find(x => x.id === id);

      if (!o) return;

      editingOpinionId = id;

      document.getElementById('modal-opinion-heading').textContent = 'Edit Opinion Column';

      document.getElementById('op-form-title').value = o.title || '';

      document.getElementById('op-form-type').value = o.type || '';

      document.getElementById('op-form-badge').value = o.badge || '';

      document.getElementById('op-form-pub').value = o.publication || '';

      document.getElementById('op-form-date').value = o.date_display || '';

      document.getElementById('op-form-abstract').value = o.abstract || '';

      document.getElementById('op-form-url').value = o.url || '';

      document.getElementById('op-form-image').value = o.image || 'assets/images/thumb-attention.jpg';

      updateOpCoverPreview();

      openModal('modal-opinion');

    }

    async function saveOpinionAction(e) {

      e.preventDefault();

      const existingO = (mediaTalksData.opinions || []).find(x => x.id === editingOpinionId) || {};

      const item = {

        id: editingOpinionId || ('opinion-' + Date.now()),

        title: document.getElementById('op-form-title').value.trim(),

        type: document.getElementById('op-form-type').value.trim(),

        badge: document.getElementById('op-form-badge').value.trim(),

        publication: document.getElementById('op-form-pub').value.trim(),

        year: (document.getElementById('op-form-date').value.match(/\\d{4}/) || ['2026'])[0],

        date_display: document.getElementById('op-form-date').value.trim(),

        abstract: document.getElementById('op-form-abstract').value.trim(),

        url: document.getElementById('op-form-url').value.trim(),

        palette: existingO.palette || "ivory",

        arch_style: existingO.arch_style || "arch-cathedral",

        image: document.getElementById('op-form-image').value.trim() || existingO.image || "assets/images/thumb-attention.jpg"

      };

      try {

        const res = await fetch('/api/save-media-talk', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY },

          body: JSON.stringify({ category: 'opinions', item, deploy: false })

        });

        if (res.ok) {

          showToast('Opinion saved.');

          closeModal('modal-opinion');

          await loadMediaTalksData();

          updateAllCounts();

        }

      } catch (err) { showToast('Error: ' + err, true); }

    }

    async function deleteMediaTalk(category, id) {

      if (!confirm(`Delete ${category} item?`)) return;

      try {

        const res = await fetch('/api/delete-media-talk', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY },

          body: JSON.stringify({ category, id })

        });

        if (res.ok) {

          showToast('Item deleted.');

          await loadMediaTalksData();

          updateAllCounts();

        }

      } catch (e) { showToast('Error: ' + e, true); }

    }

    // -------------------------------------------------------------

    // 4. ACHIEVEMENT & CV (cv.html - 7 Sections)

    // -------------------------------------------------------------

    async function loadCvData() {

      const res = await fetch('data/cv_data.json?t=' + Date.now());

      if (res.ok) {

        cvData = await res.json();

        renderCvHonorsTable(cvData.achievements_and_grants || []);

        populateCvProfileForm(cvData.executive_profile || {});

        renderCvLeadershipTable(cvData.academic_leadership || []);

        renderCvEducationTable(cvData.education || []);

        renderCvExperienceTable(cvData.work_experience || []);

        renderCvCertsTable(cvData.professional_certifications || []);

        renderCvRefsTable(cvData.academic_references || []);

      }

    }

    function switchCvSection(sec) {

      activeCvSection = sec;

      const allSecs = ['achievements_and_grants', 'executive_profile', 'academic_leadership', 'education', 'work_experience', 'professional_certifications', 'academic_references'];

      allSecs.forEach(s => {

        const btnId = s === 'achievements_and_grants' ? 'cv-honors' : (s === 'executive_profile' ? 'cv-profile' : (s === 'academic_leadership' ? 'cv-leadership' : (s === 'education' ? 'cv-education' : (s === 'work_experience' ? 'cv-experience' : (s === 'professional_certifications' ? 'cv-certs' : 'cv-refs')))));

        const btn = document.getElementById('subtab-btn-' + btnId);

        if (btn) btn.classList.toggle('active', s === sec);

        const tableId = s === 'achievements_and_grants' ? 'cv-table-container-honors' : (s === 'executive_profile' ? 'cv-form-container-profile' : (s === 'academic_leadership' ? 'cv-table-container-leadership' : (s === 'education' ? 'cv-table-container-education' : (s === 'work_experience' ? 'cv-table-container-experience' : (s === 'professional_certifications' ? 'cv-table-container-certs' : 'cv-table-container-refs')))));

        const el = document.getElementById(tableId);

        if (el) el.style.display = s === sec ? 'block' : 'none';

      });

      const filterRow = document.getElementById('cv-filter-row');

      if (filterRow) filterRow.style.display = sec === 'executive_profile' ? 'none' : 'flex';

      updateCreateButtonLabel();

    }

    function renderCvHonorsTable(list) {

      const tbody = document.getElementById('cv-honors-tbody');

      tbody.innerHTML = list.map((a, i) => {

        const isSpotlight = (currentSpotlight.source === 'cv' && (currentSpotlight.id === a.title || currentSpotlight.title === a.title)) || a.featured;

        const spotlightHtml = isSpotlight

          ? '<span class="spotlight-active-badge">★ ACTIVE SPOTLIGHT</span>'

          : `<button type="button" class="btn-set-spotlight" onclick="setHomepageSpotlight('cv', '${escapeQuotes(a.title)}', '${escapeQuotes(a.title)}')">★ Spotlight</button>`;

        return `

        <tr>

          <td style="color: #64748b; font-weight: 700;">${i + 1}</td>

          <td>

            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">

              <span style="font-weight: 700; color: #ffffff;">${escapeHTML(a.title)}</span>

              ${spotlightHtml}

            </div>

            <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 3px;">${escapeHTML((typeof a.details === 'string' ? a.details : (typeof a.highlight === 'string' ? a.highlight : '')).substring(0, 75) + '...')}</div>

          </td>

          <td style="color: #bae6fd;">${escapeHTML(a.organization || '')}</td>

          <td><span style="background: rgba(212, 175, 55, 0.15); color: var(--gold-accent); padding: 2px 8px; border-radius: 999px; font-size: 0.70rem; font-weight: 700;">${escapeHTML(a.badge || 'Distinction')}</span></td>

          <td style="color: #94a3b8; font-size: 0.82rem;">${escapeHTML(a.year || '2026')}</td>

          <td style="text-align: right; white-space: nowrap;">

            <button class="cms-btn cms-btn-ghost" style="padding: 4px 10px; font-size: 0.75rem;" onclick="editCvHonor('${escapeQuotes(a.title)}')">Edit</button>

            <button class="cms-btn cms-btn-danger" style="padding: 4px 8px; font-size: 0.75rem;" onclick="deleteCvItem('achievements_and_grants', '${escapeQuotes(a.title)}')">&times;</button>

          </td>

        </tr>`;

      }).join('');

    }

    function updateCvPortraitPreview() {

      const val = document.getElementById('cv-prof-photo').value.trim();

      const imgEl = document.getElementById('cv-portrait-preview-img');

      const emptyEl = document.getElementById('cv-portrait-preview-empty');

      if (val) {

        imgEl.src = val;

        imgEl.style.display = 'block';

        emptyEl.style.display = 'none';

      } else {

        imgEl.src = '';

        imgEl.style.display = 'none';

        emptyEl.style.display = 'block';

      }

    }

    async function handleCvPdfUpload(e, targetInputId) {

      const file = e.target.files[0];

      if (!file) return;

      const reader = new FileReader();

      reader.onload = async function(evt) {

        try {

          const res = await fetch('/api/upload-image', {

            method: 'POST',

            headers: { 'Content-Type': 'application/json' },

            body: JSON.stringify({ filename: file.name, data: evt.target.result })

          });

          const json = await res.json();

          if (json.status === 'ok') {

            document.getElementById(targetInputId).value = json.url;

            showToast('PDF uploaded successfully: ' + json.filename);

          } else {

            showToast('PDF upload failed: ' + (json.error || 'Server error'), true);

          }

        } catch (err) {

          showToast('Upload error: ' + err, true);

        }

      };

      reader.readAsDataURL(file);

    }

    function populateCvProfileForm(p) {

      p = p || cvData.executive_profile || {};

      document.getElementById('cv-prof-photo').value = p.photo || 'assets/images/portraits/portrait-1.webp';

      updateCvPortraitPreview();

      document.getElementById('cv-prof-kicker').value = p.kicker || 'Ph.D. • UKM 2024';

      document.getElementById('cv-prof-cv-url').value = p.cv_pdf_url || 'assets/docs/dr-zaid-amin-cv-july-2026.pdf';

      document.getElementById('cv-prof-edition').value = p.edition_label || 'July 2026 Academic Edition • 1.1 MB';

      document.getElementById('cv-prof-name').value = p.name || 'Dr. Zaid Amin';

      document.getElementById('cv-prof-role').value = p.role_title || '';

      document.getElementById('cv-prof-institution').value = p.institution || '';

      document.getElementById('cv-prof-distinction').value = p.distinction || '';

      document.getElementById('cv-prof-summary').value = p.summary || '';

      const rIds = p.researcher_ids || {};

      document.getElementById('cv-prof-orcid').value = (typeof rIds.orcid === 'object' ? rIds.orcid.id : rIds.orcid) || '';

      document.getElementById('cv-prof-scopus').value = (typeof rIds.scopus === 'object' ? rIds.scopus.id : rIds.scopus_id) || '';

      document.getElementById('cv-prof-wos').value = (typeof rIds.wos === 'object' ? rIds.wos.id : rIds.wos_id) || '';

      const cont = p.contact || {};

      document.getElementById('cv-prof-email').value = cont.email || '';

      const docs = p.official_docs || {};

      document.getElementById('cv-prof-permit').value = (typeof docs.teaching_permit === 'object' ? docs.teaching_permit.url : docs.teaching_permit) || '';

      document.getElementById('cv-prof-mqa').value = (typeof docs.mqa_cv === 'object' ? docs.mqa_cv.url : docs.mqa_cv) || '';

      document.getElementById('cv-prof-portfolio').value = (typeof docs.teaching_portfolio === 'object' ? docs.teaching_portfolio.url : docs.teaching_portfolio) || '';

    }

    async function saveCvExecutiveProfile() {

      const p = cvData.executive_profile || {};

      p.photo = document.getElementById('cv-prof-photo').value.trim();

      p.kicker = document.getElementById('cv-prof-kicker').value.trim();

      p.cv_pdf_url = document.getElementById('cv-prof-cv-url').value.trim();

      p.edition_label = document.getElementById('cv-prof-edition').value.trim();

      p.name = document.getElementById('cv-prof-name').value.trim();

      p.role_title = document.getElementById('cv-prof-role').value.trim();

      p.institution = document.getElementById('cv-prof-institution').value.trim();

      p.distinction = document.getElementById('cv-prof-distinction').value.trim();

      p.summary = document.getElementById('cv-prof-summary').value.trim();

      p.researcher_ids = p.researcher_ids || {};

      const orcidVal = document.getElementById('cv-prof-orcid').value.trim();

      p.researcher_ids.orcid = { id: orcidVal, url: `https://orcid.org/${orcidVal}` };

      const scopusVal = document.getElementById('cv-prof-scopus').value.trim();

      p.researcher_ids.scopus = { id: scopusVal, url: `https://www.scopus.com/authid/detail.uri?authorId=${scopusVal}` };

      const wosVal = document.getElementById('cv-prof-wos').value.trim();

      p.researcher_ids.wos = { id: wosVal, url: `https://www.webofscience.com/wos/author/record/${wosVal}` };

      p.contact = p.contact || {};

      p.contact.email = document.getElementById('cv-prof-email').value.trim();

      p.official_docs = p.official_docs || {};

      const permitVal = document.getElementById('cv-prof-permit').value.trim();

      p.official_docs.teaching_permit = { title: "Higher Education Teaching Permit", url: permitVal };

      const mqaVal = document.getElementById('cv-prof-mqa').value.trim();

      p.official_docs.mqa_cv = { title: "MQA CV for Higher Education Accreditation", url: mqaVal };

      const portVal = document.getElementById('cv-prof-portfolio').value.trim();

      p.official_docs.teaching_portfolio = { title: "Teaching, Supervision & Examination Portfolio", url: portVal };

      try {

        const res = await fetch('/api/save-cv-profile', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY },

          body: JSON.stringify({ executive_profile: p, deploy: false })

        });

        if (res.ok) showToast('Executive profile & CV hero updated and site re-compiled!');

        else showToast('Failed to save profile.', true);

      } catch (e) { showToast('Error: ' + e, true); }

    }

    function renderCvLeadershipTable(list) {

      const tbody = document.getElementById('cv-leadership-tbody');

      tbody.innerHTML = list.map((item, i) => `

        <tr>

          <td style="color: #64748b; font-weight: 700;">${i + 1}</td>

          <td style="font-weight: 700; color: #ffffff;">${escapeHTML(item.role)}</td>

          <td style="color: #bae6fd;">${escapeHTML(item.institution || '')}</td>

          <td style="color: var(--cyan-accent); font-family: monospace;">${escapeHTML(item.period || '')}</td>

          <td style="color: var(--text-muted); font-size: 0.80rem;">${escapeHTML(item.responsibilities ? item.responsibilities.substring(0, 75) + '...' : '')}</td>

          <td style="text-align: right; white-space: nowrap;">

            <button class="cms-btn cms-btn-ghost" style="padding: 4px 10px; font-size: 0.75rem;" onclick="editCvGeneric('academic_leadership', '${escapeQuotes(item.role)}')">Edit</button>

            <button class="cms-btn cms-btn-danger" style="padding: 4px 8px; font-size: 0.75rem;" onclick="deleteCvItem('academic_leadership', '${escapeQuotes(item.role)}')">&times;</button>

          </td>

        </tr>

      `).join('');

    }

    function renderCvEducationTable(list) {

      const tbody = document.getElementById('cv-education-tbody');

      tbody.innerHTML = list.map((item, i) => `

        <tr>

          <td style="color: #64748b; font-weight: 700;">${i + 1}</td>

          <td style="font-weight: 700; color: #ffffff;">${escapeHTML(item.degree)}</td>

          <td style="color: #bae6fd;">${escapeHTML(item.institution || '')}</td>

          <td style="color: var(--cyan-accent); font-family: monospace;">${escapeHTML(item.period || '')}</td>

          <td style="color: var(--gold-accent); font-size: 0.80rem;">${escapeHTML(item.distinction || item.focus || '')}</td>

          <td style="text-align: right; white-space: nowrap;">

            <button class="cms-btn cms-btn-ghost" style="padding: 4px 10px; font-size: 0.75rem;" onclick="editCvGeneric('education', '${escapeQuotes(item.degree)}')">Edit</button>

            <button class="cms-btn cms-btn-danger" style="padding: 4px 8px; font-size: 0.75rem;" onclick="deleteCvItem('education', '${escapeQuotes(item.degree)}')">&times;</button>

          </td>

        </tr>

      `).join('');

    }

    function renderCvExperienceTable(list) {

      const tbody = document.getElementById('cv-experience-tbody');

      tbody.innerHTML = list.map((item, i) => `

        <tr>

          <td style="color: #64748b; font-weight: 700;">${i + 1}</td>

          <td style="font-weight: 700; color: #ffffff;">${escapeHTML(item.role)}</td>

          <td style="color: #bae6fd;">${escapeHTML(item.institution || '')}</td>

          <td style="color: var(--cyan-accent); font-family: monospace;">${escapeHTML(item.period || '')}</td>

          <td style="color: var(--text-muted); font-size: 0.80rem;">${escapeHTML(item.description ? item.description.substring(0, 75) + '...' : '')}</td>

          <td style="text-align: right; white-space: nowrap;">

            <button class="cms-btn cms-btn-ghost" style="padding: 4px 10px; font-size: 0.75rem;" onclick="editCvGeneric('work_experience', '${escapeQuotes(item.role)}')">Edit</button>

            <button class="cms-btn cms-btn-danger" style="padding: 4px 8px; font-size: 0.75rem;" onclick="deleteCvItem('work_experience', '${escapeQuotes(item.role)}')">&times;</button>

          </td>

        </tr>

      `).join('');

    }

    function renderCvCertsTable(list) {

      const tbody = document.getElementById('cv-certs-tbody');

      tbody.innerHTML = list.map((item, i) => `

        <tr>

          <td style="color: #64748b; font-weight: 700;">${i + 1}</td>

          <td style="font-weight: 700; color: #ffffff;">${escapeHTML(item.name)}</td>

          <td style="color: #bae6fd;">${escapeHTML(item.issuer || '')}</td>

          <td style="color: var(--cyan-accent); font-family: monospace;">${escapeHTML(item.period || '')}</td>

          <td style="color: var(--text-muted); font-size: 0.80rem;">${escapeHTML(item.details || '')}</td>

          <td style="text-align: right; white-space: nowrap;">

            <button class="cms-btn cms-btn-ghost" style="padding: 4px 10px; font-size: 0.75rem;" onclick="editCvGeneric('professional_certifications', '${escapeQuotes(item.name)}')">Edit</button>

            <button class="cms-btn cms-btn-danger" style="padding: 4px 8px; font-size: 0.75rem;" onclick="deleteCvItem('professional_certifications', '${escapeQuotes(item.name)}')">&times;</button>

          </td>

        </tr>

      `).join('');

    }

    function renderCvRefsTable(list) {

      const tbody = document.getElementById('cv-refs-tbody');

      tbody.innerHTML = list.map((item, i) => `

        <tr>

          <td style="color: #64748b; font-weight: 700;">${i + 1}</td>

          <td style="font-weight: 700; color: #ffffff;">${escapeHTML(item.name)}</td>

          <td style="color: #bae6fd;">${escapeHTML(item.role || '')}</td>

          <td style="color: var(--text-muted);">${escapeHTML(item.institution || '')}</td>

          <td style="color: var(--cyan-accent); font-size: 0.80rem; font-family: monospace;">${escapeHTML(item.email || '')} ${item.phone ? ' &bull; ' + escapeHTML(item.phone) : ''}</td>

          <td style="text-align: right; white-space: nowrap;">

            <button class="cms-btn cms-btn-ghost" style="padding: 4px 10px; font-size: 0.75rem;" onclick="editCvReferee('${escapeQuotes(item.name)}')">Edit</button>

            <button class="cms-btn cms-btn-danger" style="padding: 4px 8px; font-size: 0.75rem;" onclick="deleteCvItem('academic_references', '${escapeQuotes(item.name)}')">&times;</button>

          </td>

        </tr>

      `).join('');

    }

    function filterCvCurrentTable() {

      const q = document.getElementById('cv-search-input').value.toLowerCase();

      if (activeCvSection === 'achievements_and_grants') {

        const filtered = (cvData.achievements_and_grants || []).filter(a => !q || (a.title && a.title.toLowerCase().includes(q)) || (a.organization && a.organization.toLowerCase().includes(q)));

        renderCvHonorsTable(filtered);

      }

    }

    function openActiveCvModal() {
      if (activeCvSection === 'achievements_and_grants') {
        editingCvHonorKey = null;
        document.getElementById('modal-cv-honor-heading').textContent = 'Add Honor / Grant';
        document.getElementById('form-cv-honor').reset();
        openModal('modal-cv-honor');
      } else if (activeCvSection === 'academic_references') {
        openAddRefereeModal();
      } else {
        openCvGenericModal(activeCvSection, null);
      }
    }

    function editCvHonor(title) {

      const h = (cvData.achievements_and_grants || []).find(x => x.title === title);

      if (!h) return;

      editingCvHonorKey = title;

      document.getElementById('modal-cv-honor-heading').textContent = 'Edit Honor / Grant';

      document.getElementById('cv-h-title').value = h.title || '';

      document.getElementById('cv-h-org').value = h.organization || '';

      document.getElementById('cv-h-year').value = h.year || '2026';

      document.getElementById('cv-h-badge').value = h.badge || '';

      document.getElementById('cv-h-url').value = h.url || '';

      document.getElementById('cv-h-details').value = h.details || h.highlight || '';

      document.getElementById('cv-h-featured').checked = !!h.featured;

      openModal('modal-cv-honor');

    }

    async function saveCvHonorAction(e) {

      e.preventDefault();

      const item = {

        title: document.getElementById('cv-h-title').value.trim(),

        organization: document.getElementById('cv-h-org').value.trim(),

        year: document.getElementById('cv-h-year').value.trim(),

        badge: document.getElementById('cv-h-badge').value.trim() || 'Distinction',

        url: document.getElementById('cv-h-url').value.trim(),

        details: document.getElementById('cv-h-details').value.trim(),

        featured: document.getElementById('cv-h-featured').checked

      };

      try {

        const res = await fetch('/api/save-cv-section', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY },

          body: JSON.stringify({ section: 'achievements_and_grants', item, deploy: false })

        });

        if (res.ok) {

          showToast('Honor saved.');

          closeModal('modal-cv-honor');

          await loadCvData();

          updateAllCounts();

        }

      } catch (err) { showToast('Error: ' + err, true); }

    }

    function openCvGenericModal(section, existingKey) {

      editingCvGenericKey = existingKey;

      const modal = document.getElementById('modal-cv-generic');

      const head = document.getElementById('modal-cv-generic-heading');

      const l1 = document.getElementById('cv-gen-lbl-1');

      const l2 = document.getElementById('cv-gen-lbl-2');

      const l3 = document.getElementById('cv-gen-lbl-3');

      const l4 = document.getElementById('cv-gen-lbl-4');

      const extraG = document.getElementById('cv-gen-extra-group');

      const l5 = document.getElementById('cv-gen-lbl-5');

      extraG.style.display = 'none';

      if (section === 'academic_leadership') {

        head.textContent = existingKey ? 'Edit Leadership Role' : 'Add Leadership Role';

        l1.textContent = 'Leadership Role / Title *';

        l2.textContent = 'Institution / Department *';

        l3.textContent = 'Period *';

        l4.textContent = 'Key Responsibilities / Scope';

      } else if (section === 'education') {

        head.textContent = existingKey ? 'Edit Education Credential' : 'Add Education Credential';

        l1.textContent = 'Degree & Field *';

        l2.textContent = 'University / Institution *';

        l3.textContent = 'Period / Year *';

        l4.textContent = 'Distinction / Honors (e.g. GOT)';

      } else if (section === 'work_experience') {

        head.textContent = existingKey ? 'Edit Work Experience' : 'Add Work Experience';

        l1.textContent = 'Position Title *';

        l2.textContent = 'Organization / Institution *';

        l3.textContent = 'Period *';

        l4.textContent = 'Responsibilities / Summary';

      } else if (section === 'professional_certifications') {

        head.textContent = existingKey ? 'Edit Certification' : 'Add Certification';

        l1.textContent = 'Certification Name *';

        l2.textContent = 'Issuing Body *';

        l3.textContent = 'Period / Year *';

        l4.textContent = 'Details / Credential ID';

      } else if (section === 'academic_references') {

        head.textContent = existingKey ? 'Edit Academic Reference' : 'Add Academic Reference';

        l1.textContent = 'Referee Name *';

        l2.textContent = 'Designation & Title *';

        l3.textContent = 'Institution *';

        l4.textContent = 'Endorsement / Notes';

        extraG.style.display = 'block';

        l5.textContent = 'Email & Phone Contact Coordinates';

      }

      const list = cvData[section] || [];

      const item = existingKey ? list.find(x => (x.role || x.degree || x.name) === existingKey) : null;

      document.getElementById('cv-gen-field-1').value = item ? (item.role || item.degree || item.name || '') : '';

      document.getElementById('cv-gen-field-2').value = item ? (item.institution || item.issuer || item.role || '') : '';

      document.getElementById('cv-gen-field-3').value = item ? (item.period || item.year || '') : '';

      document.getElementById('cv-gen-field-4').value = item ? (item.responsibilities || item.distinction || item.description || item.details || '') : '';

      document.getElementById('cv-gen-field-5').value = item ? (item.email || item.phone || '') : '';

      openModal('modal-cv-generic');

    }

    function editCvGeneric(section, key) {

      openCvGenericModal(section, key);

    }

    async function saveCvGenericAction(e) {

      e.preventDefault();

      const sec = activeCvSection;

      let item = {};

      const f1 = document.getElementById('cv-gen-field-1').value.trim();

      const f2 = document.getElementById('cv-gen-field-2').value.trim();

      const f3 = document.getElementById('cv-gen-field-3').value.trim();

      const f4 = document.getElementById('cv-gen-field-4').value.trim();

      const f5 = document.getElementById('cv-gen-field-5').value.trim();

      if (sec === 'academic_leadership') {

        item = { role: f1, institution: f2, period: f3, responsibilities: f4 };

      } else if (sec === 'education') {

        item = { degree: f1, institution: f2, period: f3, distinction: f4 };

      } else if (sec === 'work_experience') {

        item = { role: f1, institution: f2, period: f3, description: f4 };

      } else if (sec === 'professional_certifications') {

        item = { name: f1, issuer: f2, period: f3, details: f4 };

      } else if (sec === 'academic_references') {

        item = { name: f1, role: f2, institution: f3, email: f5, phone: '' };

      }

      try {

        const res = await fetch('/api/save-cv-section', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY },

          body: JSON.stringify({ section: sec, item, deploy: false })

        });

        if (res.ok) {

          showToast('CV item saved.');

          closeModal('modal-cv-generic');

          await loadCvData();

          updateAllCounts();

        }

      } catch (err) { showToast('Error: ' + err, true); }

    }

    
    let editingCvRefereeKey = null;

    function openAddRefereeModal() {
      editingCvRefereeKey = null;
      document.getElementById('modal-cv-referee-heading').textContent = 'Add Academic Reference';
      document.getElementById('form-cv-referee').reset();
      openModal('modal-cv-referee');
    }

    function editCvReferee(name) {
      const list = cvData.academic_references || [];
      const item = list.find(x => x.name === name);
      if (!item) {
        showToast('Referee not found: ' + name, true);
        return;
      }
      editingCvRefereeKey = name;
      document.getElementById('modal-cv-referee-heading').textContent = 'Edit Academic Reference';
      document.getElementById('ref-form-name').value = item.name || '';
      document.getElementById('ref-form-role').value = item.role || '';
      document.getElementById('ref-form-institution').value = item.institution || '';
      document.getElementById('ref-form-email').value = item.email || '';
      document.getElementById('ref-form-phone').value = item.phone || '';
      openModal('modal-cv-referee');
    }

    async function saveCvRefereeAction(e) {
      e.preventDefault();
      const item = {
        name: document.getElementById('ref-form-name').value.trim(),
        role: document.getElementById('ref-form-role').value.trim(),
        institution: document.getElementById('ref-form-institution').value.trim(),
        email: document.getElementById('ref-form-email').value.trim(),
        phone: document.getElementById('ref-form-phone').value.trim()
      };

      try {
        const res = await fetch('/api/save-cv-section', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY },
          body: JSON.stringify({ section: 'academic_references', item, old_key: editingCvRefereeKey, deploy: false })
        });
        if (res.ok) {
          showToast('Academic Reference saved.');
          closeModal('modal-cv-referee');
          await loadCvData();
          updateAllCounts();
        } else {
          const err = await res.json();
          showToast('Error saving: ' + (err.error || res.statusText), true);
        }
      } catch (err) { showToast('Error: ' + err, true); }
    }


    async function deleteCvItem(section, key) {

      if (!confirm(`Delete item '${key}' from ${section}?`)) return;

      try {

        const res = await fetch('/api/delete-cv-section', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY },

          body: JSON.stringify({ section, key })

        });

        if (res.ok) {

          showToast('Item deleted.');

          await loadCvData();

          updateAllCounts();

        }

      } catch (e) { showToast('Error: ' + e, true); }

    }

    // -------------------------------------------------------------

    // 5. SUPERVISION / PH.D. (prospective-students.html)

    // -------------------------------------------------------------

    async function loadSupervisionData() {

      try {

        const res = await fetch('data/supervision.json?t=' + Date.now());

        if (res.ok) {

          supervisionData = await res.json();

          document.getElementById('sup-form-heading').value = supervisionData.heading || '';

          document.getElementById('sup-form-subheading').value = supervisionData.subheading || '';

          document.getElementById('sup-form-statement').value = supervisionData.statement || '';

          renderSupervisionTopics(supervisionData.open_topics || []);

        }

      } catch (e) {}

    }

    function renderSupervisionTopics(topics) {

      const c = document.getElementById('supervision-topics-container');

      c.innerHTML = topics.map((t, i) => `

        <div class="cms-feature-card" style="display: flex; flex-direction: column; justify-content: space-between;">

          <div>

            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">

              <span style="font-size: 0.72rem; color: var(--cyan-accent); font-weight: 700; text-transform: uppercase;">TOPIC 0${i + 1}</span>

              <div style="display: flex; gap: 6px;">

                <button class="cms-btn cms-btn-ghost" style="padding: 3px 8px; font-size: 0.74rem;" onclick="openSupervisionTopicModal(${i})">Edit</button>

                <button class="cms-btn cms-btn-ghost" style="padding: 3px 8px; font-size: 0.74rem; color: #f87171;" onclick="deleteSupervisionTopic(${i})">Del</button>

              </div>

            </div>

            <h4 style="font-family: var(--font-cinzel); font-size: 1.05rem; color: #ffffff; margin: 0 0 6px 0;">${escapeHTML(t.title)}</h4>

            <p style="font-size: 0.82rem; color: #bae6fd; font-weight: 600; margin: 0 0 8px 0;">Target: ${Array.isArray(t.degree_levels) ? t.degree_levels.join(', ') : (t.degree_levels || '')}</p>

            <p style="font-size: 0.84rem; color: var(--text-muted); line-height: 1.5; margin: 0 0 10px 0;">${escapeHTML(t.description || '')}</p>

            <div style="font-size: 0.75rem; color: var(--gold-accent); font-weight: 600;">Recommended Background: ${Array.isArray(t.skills_required) ? t.skills_required.join(', ') : (t.skills_required || '')}</div>

          </div>

        </div>

      `).join('');

    }

    async function saveSupervisionStatement() {

      supervisionData.heading = document.getElementById('sup-form-heading').value.trim();

      supervisionData.subheading = document.getElementById('sup-form-subheading').value.trim();

      supervisionData.statement = document.getElementById('sup-form-statement').value.trim();

      try {

        const res = await fetch('/api/save-supervision', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY },

          body: JSON.stringify({ supervision: supervisionData, deploy: false })

        });

        if (res.ok) showToast('Supervision statement saved.');

        else showToast('Failed to save statement.', true);

      } catch (e) { showToast('Error: ' + e, true); }

    }

    // -------------------------------------------------------------

    // 6. HOME & GLOBAL PROFILE (profile.json)

    // -------------------------------------------------------------

    async function loadProfileData() {

      try {

        const res = await fetch('data/profile.json?t=' + Date.now());

        if (res.ok) {

          profileData = await res.json();

          document.getElementById('prof-form-name').value = profileData.name || 'Dr. Zaid Amin';

          document.getElementById('prof-form-degree').value = profileData.degree || '';

          document.getElementById('prof-form-motto').value = profileData.motto || '';

          document.getElementById('prof-form-bio').value = profileData.short_bio || '';

          const sl = profileData.social_links || {};

          document.getElementById('prof-form-scholar').value = sl.scholar || '';

          document.getElementById('prof-form-orcid').value = sl.orcid || '';

          document.getElementById('prof-form-github').value = sl.github || '';

          document.getElementById('prof-form-linkedin').value = sl.linkedin || '';

          document.getElementById('prof-form-sciprofiles').value = sl.sciprofiles || '';

          document.getElementById('prof-form-rg').value = sl.researchgate || '';

        }

      } catch (e) {}

    }

    async function saveGlobalProfile() {

      profileData.name = document.getElementById('prof-form-name').value.trim();

      profileData.degree = document.getElementById('prof-form-degree').value.trim();

      profileData.motto = document.getElementById('prof-form-motto').value.trim();

      profileData.short_bio = document.getElementById('prof-form-bio').value.trim();

      profileData.social_links = profileData.social_links || {};

      profileData.social_links.scholar = document.getElementById('prof-form-scholar').value.trim();

      profileData.social_links.orcid = document.getElementById('prof-form-orcid').value.trim();

      profileData.social_links.github = document.getElementById('prof-form-github').value.trim();

      profileData.social_links.linkedin = document.getElementById('prof-form-linkedin').value.trim();

      profileData.social_links.sciprofiles = document.getElementById('prof-form-sciprofiles').value.trim();

      profileData.social_links.researchgate = document.getElementById('prof-form-rg').value.trim();

      try {

        const res = await fetch('/api/save-profile', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY },

          body: JSON.stringify({ profile: profileData, deploy: false })

        });

        if (res.ok) showToast('Global Profile saved and rebuilt.');

        else showToast('Failed to save profile.', true);

      } catch (e) { showToast('Error: ' + e, true); }

    }

    // -------------------------------------------------------------

    // UTILITIES, UPLOADER & BACKUP

    // -------------------------------------------------------------

    function escapeHTML(str) {

      if (!str) return '';

      return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

    }

    function escapeQuotes(str) {

      if (!str) return '';

      return String(str).replace(/'/g, "\\\\'");

    }

    function downloadJSON(filename, data) {

      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });

      const url = URL.createObjectURL(blob);

      const a = document.createElement('a');

      a.href = url;

      a.download = filename;

      a.click();

      URL.revokeObjectURL(url);

      showToast(`Downloaded backup: ${filename}`);

    }

    async function handleImageUpload(e, targetInputId) {

      const file = e.target.files[0];

      if (!file) return;

      const reader = new FileReader();

      reader.onload = async () => {

        try {

          const res = await fetch('/api/upload-image', {

            method: 'POST',

            headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY },

            body: JSON.stringify({ filename: file.name, data: reader.result })

          });

          const json = await res.json();

          if (json.url) {

            document.getElementById(targetInputId).value = json.url;

            showToast('Image uploaded successfully: ' + json.filename);

            autoUpdateArticlePreview();

          }

        } catch (err) { showToast('Upload failed: ' + err, true); }

      };

      reader.readAsDataURL(file);

    }

    async function deployLiveSite() {

      if (!confirm("Initiate real-time compilation and cloud deployment to zaidamin.org via deploy.py?")) return;

      const btn = document.getElementById('btn-deploy-live');

      btn.innerHTML = '⏳ Deploying live...';

      btn.disabled = true;

      try {

        const res = await fetch('/api/deploy', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json', 'X-Admin-Key': MASTER_PASSKEY }

        });

        if (res.ok) {

          showToast('Deployment initiated in background! Check terminal or live site in ~40s.');

        } else {

          showToast('Deployment trigger failed.', true);

        }

      } catch (e) {

        showToast('Deploy error: ' + e, true);

      } finally {

        setTimeout(() => {

          btn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 2L11 13"></path><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg> Publish to zaidamin.org';

          btn.disabled = false;

        }, 3000);

      }

    }

    """ + ARTICLE_EDITOR_JS + """

    """ + TELEMETRY_JS + """

  </script>


  <!-- Universal Golden Scroll-to-Top Button for CMS (All Menus & Article Editor) -->
  <button class="scroll-to-top-btn" id="cms-scroll-to-top" aria-label="Scroll directly to top" title="Scroll to Top" type="button" onclick="scrollCmsToTop()">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="18 15 12 9 6 15"></polyline>
    </svg>
  </button>

  <script>
    function initCmsScrollToTop() {
      const btn = document.getElementById('cms-scroll-to-top');
      if (!btn) return;

      function checkScroll() {
        const winScroll = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop;
        const desk = document.getElementById('art-visual-desk-wrapper');
        const deskScroll = desk ? desk.scrollTop : 0;
        const fullScreenModal = document.querySelector('.article-studio-container.is-fullscreen');
        const fullScroll = fullScreenModal ? fullScreenModal.scrollTop : 0;

        if (winScroll > 160 || deskScroll > 160 || fullScroll > 160) {
          btn.classList.add('visible');
        } else {
          btn.classList.remove('visible');
        }
      }

      window.addEventListener('scroll', checkScroll, { passive: true });
      document.addEventListener('scroll', checkScroll, { passive: true });

      const desk = document.getElementById('art-visual-desk-wrapper');
      if (desk) desk.addEventListener('scroll', checkScroll, { passive: true });
    }

    function scrollCmsToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      document.documentElement.scrollTo({ top: 0, behavior: 'smooth' });
      document.body.scrollTo({ top: 0, behavior: 'smooth' });

      const desk = document.getElementById('art-visual-desk-wrapper');
      if (desk && desk.scrollTop > 0) {
        desk.scrollTo({ top: 0, behavior: 'smooth' });
      }

      const fullScreenModal = document.querySelector('.article-studio-container.is-fullscreen');
      if (fullScreenModal && fullScreenModal.scrollTop > 0) {
        fullScreenModal.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initCmsScrollToTop);
    } else {
      initCmsScrollToTop();
    }
  </script>
</body>

</html>

"""

    with open(ROOT / 'cms.html', 'w', encoding='utf-8') as f:

        f.write(html)

    print("Successfully built new comprehensive cms.html! Size:", len(html))

if __name__ == '__main__':

    run()

