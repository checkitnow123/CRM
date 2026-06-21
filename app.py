"""
CheckItNow — Client & Service CRM
Streamlit · session_state · English production UI (zh/zh_cn dictionaries retained)
"""

from __future__ import annotations

import json
import re
import uuid
from datetime import date, timedelta
from typing import Any
from urllib.parse import quote, urlencode

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

URGENT_DAYS = 30
CRITICAL_DAYS = 14

MODE_SINGLE = "single"
MODE_MILESTONE = "milestone"

CHANNEL_SMS = "sms"
CHANNEL_EMAIL = "email"
ALL_CHANNELS = (CHANNEL_SMS, CHANNEL_EMAIL)
_LEGACY_IM_CHANNELS = frozenset({"whatsapp", "line", "wechat"})

PAYMENT_ROUTINE = "routine"
PAYMENT_COLLECTION = "collection"

LANG_CODES = ("zh", "zh_cn", "en")
LANG_SHORT = {"zh": "繁", "zh_cn": "简", "en": "EN"}

# Brand palette — Apple minimalist light
C_BG = "#F5F5F7"
C_CARD = "#FFFFFF"
C_COMPOSE = "#FFFFFF"
C_PRIMARY = "#007AFF"
C_PRIMARY_LIGHT = "rgba(0, 122, 255, 0.1)"
C_SIDEBAR = "#FBFBFD"
C_AMBER = "#FF9500"
C_RED = "#FF3B30"
C_GREEN = "#34C759"
C_TEXT = "#1D1D1F"
C_MUTED = "#86868B"
C_BORDER = "rgba(0, 0, 0, 0.06)"
C_SHADOW = "0 1px 2px rgba(0, 0, 0, 0.04), 0 4px 18px rgba(0, 0, 0, 0.08)"
C_SHADOW_HOVER = "0 12px 32px rgba(0, 0, 0, 0.14), 0 4px 12px rgba(0, 122, 255, 0.1)"

LANG = {
    "en": {
        "page_title": "CheckItNow",
        "title": "CheckItNow",
        "tagline": "Client & Service CRM",
        "subtitle": "Track clients, sessions, and renewals — tutors, coaches, technicians, therapists, and service businesses.",
        "today": "Today",
        "mode_single": "Single Expiry",
        "mode_milestone": "Milestone Plan",
        "badge_single": "EXPIRY",
        "badge_milestone": "MILESTONE",
        "sidebar_add": "Add Client",
        "sidebar_add_cap": "Add a contract end date or a multi-session plan.",
        "tracker_mode": "Tracker type",
        "client_name": "Client / company name",
        "client_ph": "e.g., Acme Corp, Student Mary, Gym Client Alex",
        "contact_person": "Contact person",
        "contact_ph": "Name on WhatsApp, LINE, WeChat, or email",
        "client_email": "Client email",
        "email_ph": "contact@client.com",
        "edit_client": "Edit details",
        "save_edit": "Save changes",
        "close_btn": "Close",
        "dialog_dismiss_hint": "Tip: click outside the window or press Esc to close.",
        "saved_edit": "Saved {name}.",
        "service_label": "Service / program name",
        "service_ph": "e.g., 10-Session Yoga, English Tutoring, CCTV Maintenance",
        "end_date": "Program end date",
        "milestone_hdr": "Session milestones",
        "total_ms": "Total milestones",
        "total_ms_help": "Any count — lessons, visits, coaching sessions, check-ins.",
        "done_ms": "Completed so far",
        "progress_tracker": "Progress tracker",
        "progress_tracker_cap": "Check each visit in order — today's date is saved automatically.",
        "progress_empty": "No milestones configured for this client.",
        "ms_service": "{n}{suffix} Session / Milestone",
        "ms_done_row": "✅ {label} - Completed on {date}",
        "ms_locked": "Complete the previous milestone first",
        "ms_undo": "Undo last check",
        "history_header": "Milestone log:",
        "history_line": "• {label} — {date}",
        "history_latest": "We have successfully completed your {label} for {program} on {date}.",
        "history_none": "No milestones logged yet.",
        "next_visit": "Next estimated slot",
        "note_prepaid": "No action needed if pre-paid!",
        "note_collect": "Please confirm payment at your earliest convenience.",
        "note_urgent": "Please reply TODAY.",
        "add_btn": "Add Client",
        "err_name": "Client / company name is required.",
        "err_total_ms": "Total milestones cannot be less than already completed ({done}).",
        "added": "Added {name}.",
        "manage": "Manage Clients",
        "no_trackers": "No clients yet.",
        "del": "Remove",
        "default_service": "Service plan",
        "empty_info": "Click **Add Client** above to get started.",
        "kpi_active": "Active Clients",
        "kpi_urgent": "Needs Attention",
        "kpi_milestone": "Sessions Logged",
        "kpi_ms_logged": "{done} of {total} sessions logged",
        "kpi_expired": "Overdue",
        "kpi_sub_urgent": "≤ {n} days",
        "section_priority": "Priority Tasks",
        "priority_empty": "Nothing urgent right now — you're all set.",
        "section_board": "Client Dashboard",
        "filter_all": "All",
        "filter_urgent": "Urgent",
        "filter_expired": "Overdue",
        "filter_milestone": "Milestones",
        "kpi_click_hint": "Click to filter",
        "btn_draft": "Generate Reminder",
        "days_left": "{n} Days Remaining",
        "days_over": "{n} Days Overdue",
        "card_end": "Ends",
        "next_service": "Next estimated slot",
        "next_payment": "Program end",
        "all_sessions_done": "All milestones completed",
        "progress": "{done} / {total} milestones",
        "section_compose": "Generate Reminder",
        "compose_cap": "Select a client, channel, and message type — then copy or send.",
        "select_client": "Client",
        "channel_lbl": "Channel",
        "channel_sms": "Short message",
        "channel_email": "Email",
        "payment_lbl": "Notice type",
        "payment_routine": "🟢 Pre-paid / Routine check",
        "payment_collection": "🔴 Need collection",
        "reminder_area": "Message draft",
        "copy_btn": "Copy to Clipboard",
        "email_open_btn": "Open in Email",
        "email_no_address": "Add a client email in **Manage Clients** to send mail.",
        "copy_one": "Copy — {name}",
        "copy_done": "✓ Copied!",
        "copy_fallback": "Or select the text and press Ctrl+C",
        "expander_table": "Spreadsheet view",
        "col_client": "Client / company",
        "col_mode": "Type",
        "col_detail": "Detail",
        "col_end": "End",
        "col_contact": "Contact",
        "col_email": "Email",
        "col_next": "Next date",
        "col_status": "Status",
        "detail_single": "Single expiration",
        "detail_ms": "{done}/{total} milestones",
        "status_expired": "Overdue · {n} days",
        "status_critical": "{n} Days Remaining · critical",
        "status_urgent": "{n} Days Remaining · act soon",
        "status_ok": "{n} Days Remaining",
        "badge_expired": "🔴 Overdue",
        "badge_urgent": "🔴 Urgent",
        "badge_warning": "🟠 Warning",
        "badge_healthy": "🟢 Active",
        "msg_default_label": "your service program",
        "msg_default_contact": "there",
        "msg_wa_friendly_single": (
            "Hi {contact}, quick update for {company}.\n"
            "{label} ends {next_date} ({days} days left).\n"
            "{payment_note}\n"
            "Please reply to confirm. Thanks!"
        ),
        "msg_wa_friendly_ms": (
            "Hi {contact}, quick update for {company}.\n"
            "{history_latest}\n"
            "Program: {label} · Progress: {done}/{total}.\n"
            "Next slot estimated: {next_date}.\n"
            "{payment_note}\n"
            "{history_block}\n"
            "Reply if you need to reschedule. Thanks!"
        ),
        "msg_wa_urgent_single": (
            "URGENT — {contact} / {company}\n"
            "{label}: {status}. Key date: {next_date}.\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_wa_urgent_ms": (
            "URGENT — {contact} / {company}\n"
            "{history_latest}\n"
            "{label}: {remain} milestone(s) left · ends {end}.\n"
            "Next slot was estimated: {next_date}.\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_email_friendly_single": (
            "Subject: Program reminder — {label}\n"
            "To: {email}\n\n"
            "Dear {contact},\n\n"
            "Quick update for {company}:\n\n"
            "Program: {label}\n"
            "End / renewal date: {next_date} ({days} days from today)\n\n"
            "{payment_note}\n\n"
            "Please reply to confirm.\n\n"
            "Best regards,\n{company}"
        ),
        "msg_email_friendly_ms": (
            "Subject: Session update — {label}\n"
            "To: {email}\n\n"
            "Dear {contact},\n\n"
            "Quick update for {company}:\n\n"
            "{history_latest}\n\n"
            "• Program: {label}\n"
            "• Progress: {done} / {total} milestones\n"
            "• Program end date: {end}\n"
            "• Next estimated slot: {next_date}\n\n"
            "{payment_note}\n\n"
            "{history_header}\n{history_block}\n\n"
            "Best regards,\n{company}"
        ),
        "msg_email_urgent_single": (
            "Subject: URGENT — Action required: {label}\n"
            "To: {email}\n\n"
            "Dear {contact},\n\n"
            "Immediate attention for {company}:\n\n"
            "Program: {label}\n"
            "Status: {status}\n"
            "Key date: {next_date}\n\n"
            "{payment_note}\n\n"
            "Please respond within 48 hours.\n\n"
            "{company}"
        ),
        "msg_email_urgent_ms": (
            "Subject: URGENT — {label} milestone action required\n"
            "To: {email}\n\n"
            "Dear {contact},\n\n"
            "Update for {company}:\n\n"
            "{history_latest}\n\n"
            "• Progress: {done} / {total}\n"
            "• Program ends: {end} ({days} days remaining)\n"
            "• Next estimated slot: {next_date}\n\n"
            "{payment_note}\n\n"
            "{history_header}\n{history_block}\n\n"
            "Please respond within 48 hours.\n\n"
            "{company}"
        ),
        "msg_line_friendly_single": (
            "Hi {contact}, quick update for {company} (LINE).\n"
            "{label} ends {next_date} ({days} days left).\n"
            "{payment_note}\n"
            "Please reply to confirm. Thanks!"
        ),
        "msg_line_friendly_ms": (
            "Hi {contact}, quick update for {company} (LINE).\n"
            "{history_latest}\n"
            "Program: {label} · Progress: {done}/{total}.\n"
            "Next slot estimated: {next_date}.\n"
            "{payment_note}\n"
            "{history_block}\n"
            "Reply if you need to reschedule. Thanks!"
        ),
        "msg_line_urgent_single": (
            "URGENT LINE — {contact} / {company}\n"
            "{label}: {status}. Key date: {next_date}.\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_line_urgent_ms": (
            "URGENT LINE — {contact} / {company}\n"
            "{history_latest}\n"
            "{label}: {remain} milestone(s) left · ends {end}.\n"
            "Next slot was estimated: {next_date}.\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_wechat_friendly_single": (
            "Hi {contact}, quick update for {company} (WeChat).\n"
            "{label} ends {next_date} ({days} days left).\n"
            "{payment_note}\n"
            "Please reply to confirm. Thanks!"
        ),
        "msg_wechat_friendly_ms": (
            "Hi {contact}, quick update for {company} (WeChat).\n"
            "{history_latest}\n"
            "Program: {label} · Progress: {done}/{total}.\n"
            "Next slot estimated: {next_date}.\n"
            "{payment_note}\n"
            "{history_block}\n"
            "Reply if you need to reschedule. Thanks!"
        ),
        "msg_wechat_urgent_single": (
            "URGENT WeChat — {contact} / {company}\n"
            "{label}: {status}. Key date: {next_date}.\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_wechat_urgent_ms": (
            "URGENT WeChat — {contact} / {company}\n"
            "{history_latest}\n"
            "{label}: {remain} milestone(s) left · ends {end}.\n"
            "Next slot was estimated: {next_date}.\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_wa_friendly_single_collect": (
            "Hi {contact}, update for {company}.\n"
            "🔴 Collection: {label} due {next_date} ({days} days).\n"
            "{payment_note}\n"
            "Please reply when payment is arranged. Thanks!"
        ),
        "msg_wa_friendly_ms_collect": (
            "Hi {contact}, update for {company}.\n"
            "{history_latest}\n"
            "Program: {label} · Progress: {done}/{total}.\n"
            "Next slot: {next_date}.\n"
            "{payment_note}"
        ),
        "msg_wa_urgent_single_collect": (
            "URGENT — {contact} / {company}\n"
            "🔴 Collection overdue: {label} · {status} · {next_date}.\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_wa_urgent_ms_collect": (
            "URGENT — {contact} / {company}\n"
            "🔴 Collection required before {next_date}.\n"
            "{history_latest}\n"
            "{remain} milestone(s) remaining.\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_line_friendly_single_collect": (
            "Hi {contact}, update for {company} (LINE).\n"
            "🔴 Collection: {label} due {next_date}.\n"
            "{payment_note}"
        ),
        "msg_line_friendly_ms_collect": (
            "Hi {contact}, update for {company} (LINE).\n"
            "{history_latest}\n"
            "Program: {label} · {done}/{total}.\n"
            "Next slot: {next_date}.\n"
            "{payment_note}"
        ),
        "msg_line_urgent_single_collect": (
            "URGENT LINE — {contact} / {company}\n"
            "🔴 Collection overdue · {label} · {next_date}.\n"
            "{urgent_note}"
        ),
        "msg_line_urgent_ms_collect": (
            "URGENT LINE — {contact} / {company}\n"
            "🔴 Collection due · next slot {next_date} · {remain} left.\n"
            "{urgent_note}"
        ),
        "msg_wechat_friendly_single_collect": (
            "Hi {contact}, update for {company} (WeChat).\n"
            "🔴 Collection: {label} due {next_date}.\n"
            "{payment_note}"
        ),
        "msg_wechat_friendly_ms_collect": (
            "Hi {contact}, update for {company} (WeChat).\n"
            "{history_latest}\n"
            "Program: {label} · Progress: {done}/{total}.\n"
            "Next slot: {next_date}.\n"
            "{payment_note}"
        ),
        "msg_wechat_urgent_single_collect": (
            "URGENT WeChat — {contact} / {company}\n"
            "🔴 Collection overdue · {label} · {next_date}.\n"
            "{urgent_note}"
        ),
        "msg_wechat_urgent_ms_collect": (
            "URGENT WeChat — {contact} / {company}\n"
            "🔴 Collection due before {next_date} · {remain} milestone(s) left.\n"
            "{urgent_note}"
        ),
        "msg_email_friendly_single_collect": (
            "Subject: Collection notice — {label}\n"
            "To: {email}\n\n"
            "Dear {contact},\n\n"
            "Program: {label}\n"
            "Due by: {next_date} ({days} days from today)\n\n"
            "{payment_note}\n\n"
            "{company}"
        ),
        "msg_email_friendly_ms_collect": (
            "Subject: Collection before next slot — {label}\n"
            "To: {email}\n\n"
            "Dear {contact},\n\n"
            "{history_latest}\n\n"
            "• Program: {label}\n"
            "• Progress: {done} / {total}\n"
            "• Next slot: {next_date}\n\n"
            "{payment_note}\n\n"
            "{company}"
        ),
        "msg_email_urgent_single_collect": (
            "Subject: URGENT — Collection overdue: {label}\n"
            "To: {email}\n\n"
            "Dear {contact},\n\n"
            "Program: {label} · Status: {status} · Due: {next_date}\n\n"
            "{payment_note}\n\n"
            "{company}"
        ),
        "msg_email_urgent_ms_collect": (
            "Subject: URGENT — Collection required: {label}\n"
            "To: {email}\n\n"
            "Dear {contact},\n\n"
            "Collection required before slot on {next_date}.\n"
            "• Progress: {done} / {total} · Remaining: {remain}\n\n"
            "{payment_note}\n\n"
            "{company}"
        ),
        "product_notice": (
            "**Web demo vs. production:** This page is your **interactive flight test** — "
            "nothing to install. When you hire us, you receive a **standalone Windows `.exe`** "
            "that runs **100% offline** on your PC. Client data stays on **your** machine only — "
            "no cloud DB, no subscription."
        ),
        "demo_banner": (
            "**Interactive Flight Test Demo Only** — fictional sample clients "
            "(Client A, Client B, …). Refresh the browser to reset. "
            "No `.exe` download on this page."
        ),
        "cta_lead": (
            "**Your own branded `.exe` — from $1,499 USD**\n\n"
            "Tell us your industry, reminder rules, and export needs. "
            "We deliver a plug-and-play desktop CRM, typically within **48 hours**.\n\n"
            "Email: **checkitnow123@gmail.com**"
        ),
        "footer_cta": (
            "**Enterprise custom CRM — quoted from $9,999 USD**\n\n"
            "Agencies charge five figures for offline client tracking, milestone schedules, "
            "and renewal reminders built from scratch. CheckItNow is already flight-tested.\n\n"
            "**Launch offer — demo to delivery from $1,499 USD**\n\n"
            "Email **checkitnow123@gmail.com** with your workflow. "
            "We reply within 24 hours with scope and timeline."
        ),
    },
    "zh": {
        "page_title": "CheckItNow 到期提醒",
        "title": "CheckItNow",
        "tagline": "自由工作者與服務 CRM",
        "subtitle": "管理客戶、課程與里程碑 — 家教、教練、技師、治療師皆適用。",
        "today": "今日",
        "mode_single": "單一到期",
        "mode_milestone": "里程碑週期",
        "badge_single": "到期",
        "badge_milestone": "里程碑",
        "sidebar_add": "新增追蹤",
        "sidebar_add_cap": "記錄合約結束日，或多次服務套裝進度。",
        "tracker_mode": "追蹤類型",
        "client_name": "客戶／公司名稱",
        "client_ph": "例：ABC 公司、學員 Mary、健身客戶 Alex",
        "contact_person": "聯絡人",
        "contact_ph": "WhatsApp、LINE、微信或 Email 上的名稱",
        "client_email": "客戶 Email",
        "email_ph": "contact@client.com",
        "edit_client": "編輯資料",
        "save_edit": "儲存變更",
        "close_btn": "關閉",
        "dialog_dismiss_hint": "提示：點擊視窗外或按 Esc 亦可關閉。",
        "saved_edit": "已儲存 {name}。",
        "service_label": "服務／方案名稱",
        "service_ph": "例：10 堂瑜伽、英文家教、CCTV 保養",
        "end_date": "方案結束日",
        "milestone_hdr": "Session 里程碑",
        "total_ms": "里程碑總數",
        "total_ms_help": "任意數字 — 課時、回訪、教練場次等。",
        "done_ms": "已完成",
        "progress_tracker": "進度追蹤",
        "progress_tracker_cap": "請依序勾選每次服務，系統會自動記錄今日日期。",
        "progress_empty": "此客戶尚未設定里程碑次數。",
        "ms_service": "第 {n} 次 Session／Milestone",
        "ms_done_row": "✅ {label} - 完成於 {date}",
        "ms_locked": "請先完成前一次",
        "ms_undo": "撤回上一筆",
        "history_header": "里程碑紀錄：",
        "history_line": "• {label} — {date}",
        "history_latest": "我們已於 {date} 順利完成您的{label}（{program}）。",
        "history_none": "尚無紀錄。",
        "next_visit": "下次預計時段",
        "add_btn": "加入追蹤",
        "err_name": "請填寫客戶／公司名稱。",
        "err_total_ms": "總里程碑數不可少於已完成數（{done}）。",
        "added": "已新增 {name}。",
        "manage": "追蹤清單",
        "no_trackers": "尚無項目。",
        "del": "移除",
        "sidebar_footer": "示範模式 — 完整重新整理瀏覽器後資料會重置。",
        "default_service": "服務合約",
        "empty_info": "按上方 **＋ 新增追蹤** 建立第一個項目。",
        "kpi_active": "追蹤中",
        "kpi_urgent": "待處理",
        "kpi_milestone": "已完成次數",
        "kpi_ms_logged": "里程碑合計 {done}/{total}",
        "kpi_expired": "已逾期",
        "kpi_sub_urgent": "≤ {n} 天",
        "section_priority": "優先處理",
        "priority_empty": "目前無緊急項目。",
        "section_board": "追蹤看板",
        "filter_all": "全部",
        "filter_urgent": "緊急",
        "filter_expired": "逾期",
        "filter_milestone": "里程碑",
        "kpi_click_hint": "點擊查看 →",
        "btn_draft": "撰寫提醒",
        "days_left": "剩 {n} 天",
        "days_over": "逾期 {n} 天",
        "card_end": "結束",
        "next_service": "下次服務／收款日",
        "next_payment": "合約結束日",
        "all_sessions_done": "所有里程碑已完成",
        "progress": "{done} / {total} 里程碑",
        "section_compose": "撰寫提醒",
        "compose_cap": "選擇客戶、頻道與通知類型，複製或發送。",
        "select_client": "客戶",
        "channel_lbl": "頻道",
        "channel_sms": "短訊",
        "channel_email": "Email",
        "payment_lbl": "通知類型",
        "payment_routine": "🟢 預付／例行通知",
        "payment_collection": "🔴 需要收款",
        "reminder_area": "訊息草稿",
        "copy_btn": "📋 複製到剪貼簿",
        "email_open_btn": "📧 以 Outlook 開啟／發送郵件",
        "email_no_address": "請在 **追蹤清單** 中填寫客戶 Email。",
        "copy_one": "複製 — {name}",
        "copy_done": "✓ 已複製！",
        "copy_fallback": "或選取文字後按 Ctrl+C",
        "expander_table": "表格檢視",
        "col_client": "客戶",
        "col_mode": "類型",
        "col_detail": "內容",
        "col_end": "結束日",
        "col_contact": "聯絡人",
        "col_email": "Email",
        "col_next": "下次日期",
        "col_status": "狀態",
        "detail_single": "單一到期",
        "detail_ms": "{done}/{total} 里程碑",
        "note_prepaid": "若已預付，無需額外操作！",
        "note_collect": "請儘早確認付款。",
        "note_urgent": "請今日內回覆。",
        "status_expired": "逾期 {n} 天",
        "status_critical": "剩 {n} 天 · 緊急",
        "status_urgent": "剩 {n} 天 · 請處理",
        "status_ok": "剩 {n} 天",
        "badge_expired": "🔴 逾期",
        "badge_urgent": "🔴 緊急",
        "badge_warning": "🟠 注意",
        "badge_healthy": "🟢 正常",
        "msg_default_label": "您的服務方案",
        "msg_default_contact": "您好",
        "msg_wa_friendly_single": (
            "Hi {contact}，{company} 進度更新。\n"
            "「{label}」將於 {next_date} 結束（剩 {days} 天）。\n"
            "{payment_note}\n"
            "請回覆確認，謝謝！"
        ),
        "msg_wa_friendly_ms": (
            "Hi {contact}，{company} 進度更新。\n"
            "{history_latest}\n"
            "方案：{label} · 進度 {done}/{total}。\n"
            "下次預計時段：{next_date}。\n"
            "{payment_note}\n"
            "{history_block}\n"
            "如需改期請回覆，謝謝！"
        ),
        "msg_wa_urgent_single": (
            "【緊急】{contact} / {company}\n"
            "「{label}」{status}，關鍵日期：{next_date}。\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_wa_urgent_ms": (
            "【緊急】{contact} / {company}\n"
            "{history_latest}\n"
            "「{label}」尚餘 {remain} 個里程碑；方案 {end} 結束。\n"
            "原預計時段：{next_date}。\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_email_friendly_single": (
            "Subject: 方案提醒 — {label}\n"
            "To: {email}\n\n"
            "{contact} 您好：\n\n"
            "為您更新 {company} 的進度：\n\n"
            "方案：{label}\n"
            "結束／續約日：{next_date}（距今 {days} 天）\n\n"
            "{payment_note}\n\n"
            "請回覆確認。\n\n"
            "敬祝 順心\n{company}"
        ),
        "msg_email_friendly_ms": (
            "Subject: Session 更新 — {label}\n"
            "To: {email}\n\n"
            "{contact} 您好：\n\n"
            "為您更新 {company} 的進度：\n\n"
            "{history_latest}\n\n"
            "• 方案：{label}\n"
            "• 進度：{done} / {total} 里程碑\n"
            "• 方案結束日：{end}\n"
            "• 下次預計時段：{next_date}\n\n"
            "{payment_note}\n\n"
            "{history_header}\n{history_block}\n\n"
            "敬祝 順心\n{company}"
        ),
        "msg_email_urgent_single": (
            "Subject: URGENT — 需立即處理：{label}\n"
            "To: {email}\n\n"
            "{contact} 您好：\n\n"
            "{company} 需您立即關注：\n\n"
            "方案：{label}\n"
            "狀態：{status}\n"
            "關鍵日期：{next_date}\n\n"
            "{payment_note}\n\n"
            "請於 48 小時內回覆。\n\n"
            "{company}"
        ),
        "msg_email_urgent_ms": (
            "Subject: URGENT — {label} 里程碑需處理\n"
            "To: {email}\n\n"
            "{contact} 您好：\n\n"
            "為您更新 {company} 的進度：\n\n"
            "{history_latest}\n\n"
            "• 進度：{done} / {total}\n"
            "• 方案結束：{end}（剩 {days} 天）\n"
            "• 下次預計時段：{next_date}\n\n"
            "{payment_note}\n\n"
            "{history_header}\n{history_block}\n\n"
            "請於 48 小時內回覆。\n\n"
            "{company}"
        ),
        "msg_line_friendly_single": (
            "Hi {contact}，{company} 進度更新（LINE）。\n"
            "「{label}」將於 {next_date} 結束（剩 {days} 天）。\n"
            "{payment_note}\n"
            "請回覆確認，謝謝！"
        ),
        "msg_line_friendly_ms": (
            "Hi {contact}，{company} 進度更新（LINE）。\n"
            "{history_latest}\n"
            "方案：{label} · 進度 {done}/{total}。\n"
            "下次預計時段：{next_date}。\n"
            "{payment_note}\n"
            "{history_block}\n"
            "如需改期請回覆，謝謝！"
        ),
        "msg_line_urgent_single": (
            "【緊急】LINE — {contact} / {company}\n"
            "「{label}」{status}，關鍵日期：{next_date}。\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_line_urgent_ms": (
            "【緊急】LINE — {contact} / {company}\n"
            "{history_latest}\n"
            "「{label}」尚餘 {remain} 個里程碑；方案 {end} 結束。\n"
            "原預計時段：{next_date}。\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_wechat_friendly_single": (
            "您好 {contact}，{company} 進度更新（微信）。\n"
            "「{label}」將於 {next_date} 結束（剩 {days} 天）。\n"
            "{payment_note}\n"
            "請回覆確認，謝謝！"
        ),
        "msg_wechat_friendly_ms": (
            "您好 {contact}，{company} 進度更新（微信）。\n"
            "{history_latest}\n"
            "方案：{label} · 進度 {done}/{total}。\n"
            "下次預計時段：{next_date}。\n"
            "{payment_note}\n"
            "{history_block}\n"
            "如需改期請回覆，謝謝！"
        ),
        "msg_wechat_urgent_single": (
            "【緊急】微信 — {contact} / {company}\n"
            "「{label}」{status}，關鍵日期：{next_date}。\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_wechat_urgent_ms": (
            "【緊急】微信 — {contact} / {company}\n"
            "{history_latest}\n"
            "「{label}」尚餘 {remain} 個里程碑；方案 {end} 結束。\n"
            "原預計時段：{next_date}。\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_wa_friendly_single_collect": (
            "Hi {contact}，{company} 進度更新。\n"
            "🔴 收款：「{label}」應於 {next_date} 付款（剩 {days} 天）。\n"
            "{payment_note}\n"
            "付款後請回覆確認，謝謝！"
        ),
        "msg_wa_friendly_ms_collect": (
            "Hi {contact}，{company} 進度更新。\n"
            "{history_latest}\n"
            "方案：{label} · 進度 {done}/{total}。\n"
            "下次時段：{next_date}。\n"
            "{payment_note}"
        ),
        "msg_wa_urgent_single_collect": (
            "【緊急】{contact} / {company}\n"
            "🔴 收款逾期：「{label}」· {status} · {next_date}。\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_wa_urgent_ms_collect": (
            "【緊急】{contact} / {company}\n"
            "🔴 {next_date} 前需收款。\n"
            "{history_latest}\n"
            "尚餘 {remain} 個里程碑。\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_line_friendly_single_collect": (
            "Hi {contact}，{company} 進度更新（LINE）。\n"
            "🔴 收款：「{label}」到期 {next_date}。\n"
            "{payment_note}"
        ),
        "msg_line_friendly_ms_collect": (
            "Hi {contact}，{company} 進度更新（LINE）。\n"
            "{history_latest}\n"
            "方案：{label} · {done}/{total}。\n"
            "下次時段：{next_date}。\n"
            "{payment_note}"
        ),
        "msg_line_urgent_single_collect": (
            "【緊急】LINE — {contact} / {company}\n"
            "🔴 收款逾期 · {label} · {next_date}。\n"
            "{urgent_note}"
        ),
        "msg_line_urgent_ms_collect": (
            "【緊急】LINE — {contact} / {company}\n"
            "🔴 收款 · 下次時段 {next_date} · 尚餘 {remain}。\n"
            "{urgent_note}"
        ),
        "msg_wechat_friendly_single_collect": (
            "您好 {contact}，{company} 進度更新（微信）。\n"
            "🔴 待收款：{label}，到期 {next_date}。\n"
            "{payment_note}"
        ),
        "msg_wechat_friendly_ms_collect": (
            "您好 {contact}，{company} 進度更新（微信）。\n"
            "{history_latest}\n"
            "方案：{label} · 進度 {done}/{total}。\n"
            "下次時段：{next_date}。\n"
            "{payment_note}"
        ),
        "msg_wechat_urgent_single_collect": (
            "【緊急】{contact} / {company}（微信）\n"
            "🔴 收款逾期 · {label} · {next_date}。\n"
            "{urgent_note}"
        ),
        "msg_wechat_urgent_ms_collect": (
            "【緊急】{contact} / {company}（微信）\n"
            "🔴 {next_date} 前需收款 · 尚餘 {remain} 個里程碑。\n"
            "{urgent_note}"
        ),
        "msg_email_friendly_single_collect": (
            "Subject: 收款通知 — {label}\n"
            "To: {email}\n\n"
            "{contact} 您好：\n\n"
            "方案：{label}\n"
            "應付日：{next_date}（距今 {days} 天）\n\n"
            "{payment_note}\n\n"
            "{company}"
        ),
        "msg_email_friendly_ms_collect": (
            "Subject: 下次時段前收款 — {label}\n"
            "To: {email}\n\n"
            "{contact} 您好：\n\n"
            "{history_latest}\n\n"
            "• 方案：{label}\n"
            "• 進度：{done} / {total}\n"
            "• 下次時段：{next_date}\n\n"
            "{payment_note}\n\n"
            "{company}"
        ),
        "msg_email_urgent_single_collect": (
            "Subject: URGENT — 收款逾期：{label}\n"
            "To: {email}\n\n"
            "{contact} 您好：\n\n"
            "方案：{label} · 狀態：{status} · 應付：{next_date}\n\n"
            "{payment_note}\n\n"
            "{company}"
        ),
        "msg_email_urgent_ms_collect": (
            "Subject: URGENT — 需收款：{label}\n"
            "To: {email}\n\n"
            "{contact} 您好：\n\n"
            "請於 {next_date} 時段前完成收款。\n"
            "• 進度：{done} / {total} · 尚餘：{remain}\n\n"
            "{payment_note}\n\n"
            "{company}"
        ),
    },
    "zh_cn": {
        "page_title": "CheckItNow 到期提醒",
        "title": "CheckItNow",
        "tagline": "自由职业者与服务 CRM",
        "subtitle": "管理客户、课程与里程碑 — 家教、教练、技师、治疗师皆适用。",
        "progress_tracker": "进度追踪",
        "progress_tracker_cap": "请按顺序勾选每次服务，系统自动记录今日日期。",
        "progress": "{done} / {total} 里程碑",
        "detail_ms": "{done}/{total} 里程碑",
        "kpi_milestone": "已记录里程碑",
        "ms_undo": "撤销上一步",
        "section_board": "追踪看板",
        "next_visit": "下次预计时段",
        "next_service": "下次预计时段",
        "contact_ph": "微信昵称或全名",
        "edit_client": "编辑资料",
        "save_edit": "保存变更",
        "close_btn": "关闭",
        "dialog_dismiss_hint": "提示：点击视窗外或按 Esc 亦可关闭。",
        "saved_edit": "已保存 {name}。",
        "sidebar_add": "新增追踪",
        "manage": "追踪清单",
        "add_btn": "加入追踪",
        "compose_cap": "选择客户、频道与通知类型，复制或发送。",
        "channel_lbl": "频道",
        "channel_sms": "短讯",
        "channel_email": "Email",
        "payment_lbl": "通知类型",
        "payment_routine": "🟢 预付/例行通知",
        "payment_collection": "🔴 需要收款",
        "copy_btn": "📋 复制到剪贴板",
        "email_open_btn": "📧 用 Outlook 打开/发送邮件",
        "email_no_address": "请在 **追踪清单** 中填写客户 Email。",
        "empty_info": "点击上方 **＋ 新增追踪** 建立第一个项目。",
        "client_name": "客户/公司名称",
        "client_ph": "例：Acme 公司、学员 Mary、健身客户 Alex",
        "service_label": "服务/方案名称",
        "service_ph": "例：10 节瑜伽、英语家教、监控维护",
        "ms_service": "第 {n} 次 Session/里程碑",
        "ms_done_row": "✅ {label} - 完成于 {date}",
        "note_prepaid": "如已预付，无需额外操作！",
        "note_collect": "请尽早确认付款。",
        "note_urgent": "请今日内回复。",
        "badge_expired": "🔴 逾期",
        "badge_urgent": "🔴 紧急",
        "badge_warning": "🟠 注意",
        "badge_healthy": "🟢 正常",
        "history_latest": "我们已于 {date} 顺利完成您的{label}（{program}）。",
        "history_none": "暂无记录。",
        "history_header": "里程碑记录：",
        "all_sessions_done": "所有里程碑已完成",
        "msg_default_contact": "您好",
        "msg_wa_friendly_single": (
            "您好 {contact}，{company} 进度更新。\n"
            "「{label}」将于 {next_date} 结束（剩 {days} 天）。\n"
            "{payment_note}\n"
            "请回复确认，谢谢！"
        ),
        "msg_wa_friendly_ms": (
            "您好 {contact}，{company} 进度更新。\n"
            "{history_latest}\n"
            "方案：{label} · 进度 {done}/{total}。\n"
            "下次预计时段：{next_date}。\n"
            "{payment_note}\n"
            "{history_block}\n"
            "如需改期请回复，谢谢！"
        ),
        "msg_wa_urgent_single": (
            "【紧急】{contact} / {company}\n"
            "「{label}」{status}，关键日期：{next_date}。\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_wa_urgent_ms": (
            "【紧急】{contact} / {company}\n"
            "{history_latest}\n"
            "「{label}」尚余 {remain} 个里程碑；方案 {end} 结束。\n"
            "原预计时段：{next_date}。\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_email_friendly_single": (
            "Subject: 方案提醒 — {label}\n"
            "To: {email}\n\n"
            "{contact} 您好：\n\n"
            "为您更新 {company} 的进度：\n\n"
            "方案：{label}\n"
            "结束/续约日：{next_date}（距今 {days} 天）\n\n"
            "{payment_note}\n\n"
            "请回复确认。\n\n"
            "此致\n{company}"
        ),
        "msg_email_friendly_ms": (
            "Subject: Session 更新 — {label}\n"
            "To: {email}\n\n"
            "{contact} 您好：\n\n"
            "为您更新 {company} 的进度：\n\n"
            "{history_latest}\n\n"
            "• 方案：{label}\n"
            "• 进度：{done} / {total} 里程碑\n"
            "• 方案结束日：{end}\n"
            "• 下次预计时段：{next_date}\n\n"
            "{payment_note}\n\n"
            "{history_header}\n{history_block}\n\n"
            "此致\n{company}"
        ),
        "msg_email_urgent_single": (
            "Subject: URGENT — 需立即处理：{label}\n"
            "To: {email}\n\n"
            "{contact} 您好：\n\n"
            "{company} 需您立即关注：\n\n"
            "方案：{label}\n"
            "状态：{status}\n"
            "关键日期：{next_date}\n\n"
            "{payment_note}\n\n"
            "请于 48 小时内回复。\n\n"
            "{company}"
        ),
        "msg_email_urgent_ms": (
            "Subject: URGENT — {label} 里程碑需处理\n"
            "To: {email}\n\n"
            "{contact} 您好：\n\n"
            "为您更新 {company} 的进度：\n\n"
            "{history_latest}\n\n"
            "• 进度：{done} / {total}\n"
            "• 方案结束：{end}（剩 {days} 天）\n"
            "• 下次预计时段：{next_date}\n\n"
            "{payment_note}\n\n"
            "{history_header}\n{history_block}\n\n"
            "请于 48 小时内回复。\n\n"
            "{company}"
        ),
        "msg_line_friendly_single": (
            "您好 {contact}，{company} 进度更新（LINE）。\n"
            "「{label}」将于 {next_date} 结束（剩 {days} 天）。\n"
            "{payment_note}\n"
            "请回复确认，谢谢！"
        ),
        "msg_line_friendly_ms": (
            "您好 {contact}，{company} 进度更新（LINE）。\n"
            "{history_latest}\n"
            "方案：{label} · 进度 {done}/{total}。\n"
            "下次预计时段：{next_date}。\n"
            "{payment_note}\n"
            "{history_block}\n"
            "如需改期请回复，谢谢！"
        ),
        "msg_line_urgent_single": (
            "【紧急】LINE — {contact} / {company}\n"
            "「{label}」{status}，关键日期：{next_date}。\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_line_urgent_ms": (
            "【紧急】LINE — {contact} / {company}\n"
            "{history_latest}\n"
            "「{label}」尚余 {remain} 个里程碑；方案 {end} 结束。\n"
            "原预计时段：{next_date}。\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_wechat_friendly_single": (
            "您好 {contact}，{company} 进度更新（微信）。\n"
            "「{label}」将于 {next_date} 结束（剩 {days} 天）。\n"
            "{payment_note}\n"
            "请回复确认，谢谢！"
        ),
        "msg_wechat_friendly_ms": (
            "您好 {contact}，{company} 进度更新（微信）。\n"
            "{history_latest}\n"
            "方案：{label} · 进度 {done}/{total}。\n"
            "下次预计时段：{next_date}。\n"
            "{payment_note}\n"
            "{history_block}\n"
            "如需改期请回复，谢谢！"
        ),
        "msg_wechat_urgent_single": (
            "【紧急】微信 — {contact} / {company}\n"
            "「{label}」{status}，关键日期：{next_date}。\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_wechat_urgent_ms": (
            "【紧急】微信 — {contact} / {company}\n"
            "{history_latest}\n"
            "「{label}」尚余 {remain} 个里程碑；方案 {end} 结束。\n"
            "原预计时段：{next_date}。\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_wa_friendly_single_collect": (
            "您好 {contact}，{company} 进度更新。\n"
            "🔴 收款：「{label}」应于 {next_date} 付款（剩 {days} 天）。\n"
            "{payment_note}\n"
            "付款后请回复确认，谢谢！"
        ),
        "msg_wa_friendly_ms_collect": (
            "您好 {contact}，{company} 进度更新。\n"
            "{history_latest}\n"
            "方案：{label} · 进度 {done}/{total}。\n"
            "下次时段：{next_date}。\n"
            "{payment_note}"
        ),
        "msg_wa_urgent_single_collect": (
            "【紧急】{contact} / {company}\n"
            "🔴 收款逾期：「{label}」· {status} · {next_date}。\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_wa_urgent_ms_collect": (
            "【紧急】{contact} / {company}\n"
            "🔴 {next_date} 前需收款。\n"
            "{history_latest}\n"
            "尚余 {remain} 个里程碑。\n"
            "{payment_note}\n"
            "{urgent_note}"
        ),
        "msg_line_friendly_single_collect": (
            "您好 {contact}，{company} 进度更新（LINE）。\n"
            "🔴 收款：「{label}」到期 {next_date}。\n"
            "{payment_note}"
        ),
        "msg_line_friendly_ms_collect": (
            "您好 {contact}，{company} 进度更新（LINE）。\n"
            "{history_latest}\n"
            "方案：{label} · {done}/{total}。\n"
            "下次时段：{next_date}。\n"
            "{payment_note}"
        ),
        "msg_line_urgent_single_collect": (
            "【紧急】LINE — {contact} / {company}\n"
            "🔴 收款逾期 · {label} · {next_date}。\n"
            "{urgent_note}"
        ),
        "msg_line_urgent_ms_collect": (
            "【紧急】LINE — {contact} / {company}\n"
            "🔴 收款 · 下次时段 {next_date} · 尚余 {remain}。\n"
            "{urgent_note}"
        ),
        "msg_wechat_friendly_single_collect": (
            "您好 {contact}，{company} 进度更新（微信）。\n"
            "🔴 待收款：{label}，到期 {next_date}。\n"
            "{payment_note}"
        ),
        "msg_wechat_friendly_ms_collect": (
            "您好 {contact}，{company} 进度更新（微信）。\n"
            "{history_latest}\n"
            "方案：{label} · 进度 {done}/{total}。\n"
            "下次时段：{next_date}。\n"
            "{payment_note}"
        ),
        "msg_wechat_urgent_single_collect": (
            "【紧急】{contact} / {company}（微信）\n"
            "🔴 收款逾期 · {label} · {next_date}。\n"
            "{urgent_note}"
        ),
        "msg_wechat_urgent_ms_collect": (
            "【紧急】{contact} / {company}（微信）\n"
            "🔴 {next_date} 前需收款 · 尚余 {remain} 个里程碑。\n"
            "{urgent_note}"
        ),
        "msg_email_friendly_single_collect": (
            "Subject: 收款通知 — {label}\n"
            "To: {email}\n\n"
            "{contact} 您好：\n\n"
            "方案：{label}\n"
            "应付日：{next_date}（距今 {days} 天）\n\n"
            "{payment_note}\n\n"
            "{company}"
        ),
        "msg_email_friendly_ms_collect": (
            "Subject: 下次时段前收款 — {label}\n"
            "To: {email}\n\n"
            "{contact} 您好：\n\n"
            "{history_latest}\n\n"
            "• 方案：{label}\n"
            "• 进度：{done} / {total}\n"
            "• 下次时段：{next_date}\n\n"
            "{payment_note}\n\n"
            "{company}"
        ),
        "msg_email_urgent_single_collect": (
            "Subject: URGENT — 收款逾期：{label}\n"
            "To: {email}\n\n"
            "{contact} 您好：\n\n"
            "方案：{label} · 状态：{status} · 应付：{next_date}\n\n"
            "{payment_note}\n\n"
            "{company}"
        ),
        "msg_email_urgent_ms_collect": (
            "Subject: URGENT — 需收款：{label}\n"
            "To: {email}\n\n"
            "{contact} 您好：\n\n"
            "请于 {next_date} 时段前完成收款。\n"
            "• 进度：{done} / {total} · 尚余：{remain}\n\n"
            "{payment_note}\n\n"
            "{company}"
        ),
    },
}


def _html_esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _qp_first(value: str | list[str] | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, list):
        return value[0] if value else None
    return str(value)


def apply_lang_query_param() -> bool:
    qp = getattr(st, "query_params", None)
    if qp is None:
        return False
    lang = _qp_first(qp.get("lang"))
    if lang not in LANG_CODES:
        return False
    st.session_state.lang_code = lang
    try:
        del qp["lang"]
    except Exception:
        pass
    return True


def apply_kpi_query_params() -> bool:
    """Apply KPI card navigation from URL query params (?kpi_filter=…&kpi_scroll=…)."""
    qp = getattr(st, "query_params", None)
    if qp is None:
        return False
    kpi_filter = _qp_first(qp.get("kpi_filter"))
    if not kpi_filter:
        return False
    kpi_navigate(kpi_filter, _qp_first(qp.get("kpi_scroll")) or "")
    try:
        qp.clear()
    except Exception:
        pass
    return True


def scroll_to_anchor(anchor_id: str) -> None:
    safe_id = re.sub(r"[^a-zA-Z0-9_-]", "", anchor_id)
    components.html(
        f"""
        <script>
        (function() {{
            var doc = window.parent.document;
            var el = doc.getElementById("{safe_id}");
            if (!el) return;
            setTimeout(function() {{
                el.scrollIntoView({{ behavior: "smooth", block: "start" }});
            }}, 280);
        }})();
        </script>
        """,
        height=0,
    )


def kpi_navigate(board_filter: str, scroll_target: str = "") -> None:
    st.session_state.board_filter = board_filter
    if scroll_target:
        st.session_state.cin_scroll_target = scroll_target


def board_columns(n: int) -> list:
    try:
        return st.columns(n, vertical_alignment="bottom")
    except TypeError:
        return st.columns(n)


def inject_styles() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        html, body, [class*="css"] {{
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Inter', sans-serif;
            line-height: 1.55;
            -webkit-font-smoothing: antialiased;
            color: {C_TEXT};
        }}
        [data-testid="stAppViewContainer"] {{
            background: {C_BG};
        }}
        [data-testid="stHeader"] {{
            background: {C_BG} !important;
        }}
        div[data-testid="column"]:has(.cin-lang-wrap) {{
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }}
        div[data-testid="stHorizontalBlock"]:has(.cin-lang-bar) {{
            display: inline-flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            align-items: center !important;
            gap: 0 !important;
            width: auto !important;
            max-width: 100%;
            padding: 2px !important;
            background: rgba(0, 0, 0, 0.04) !important;
            border-radius: 8px !important;
            border: 1px solid {C_BORDER} !important;
            box-shadow: none !important;
        }}
        div[data-testid="stHorizontalBlock"]:has(.cin-lang-bar) > div[data-testid="column"] {{
            width: auto !important;
            min-width: 1.55rem !important;
            flex: 0 0 auto !important;
            padding: 0 !important;
        }}
        div[data-testid="stHorizontalBlock"]:has(.cin-lang-bar) .cin-lang-bar {{
            display: none !important;
        }}
        div[data-testid="stHorizontalBlock"]:has(.cin-lang-bar) [data-testid="stButton"] {{
            margin: 0 !important;
            width: auto !important;
        }}
        div[data-testid="stHorizontalBlock"]:has(.cin-lang-bar) [data-testid="stButton"] > button {{
            min-height: 1.5rem !important;
            height: 1.5rem !important;
            width: 1.65rem !important;
            min-width: 1.65rem !important;
            padding: 0 !important;
            font-size: 0.68rem !important;
            font-weight: 600 !important;
            border-radius: 5px !important;
            box-shadow: none !important;
            border: none !important;
            background: transparent !important;
            color: {C_TEXT} !important;
        }}
        div[data-testid="stHorizontalBlock"]:has(.cin-lang-bar) [data-testid="stButton"] > button[kind="primary"] {{
            background: {C_PRIMARY} !important;
            color: #ffffff !important;
        }}
        div[data-testid="stHorizontalBlock"]:has(.cin-lang-bar) [data-testid="stButton"] > button[kind="secondary"]:hover {{
            background: rgba(0, 122, 255, 0.08) !important;
            color: {C_TEXT} !important;
            border: none !important;
        }}
        div[data-testid="stHorizontalBlock"]:has(.cin-lang-bar) [data-testid="stButton"] > button[kind="primary"]:hover {{
            background: {C_PRIMARY} !important;
            color: #ffffff !important;
        }}
        div[data-testid="stHorizontalBlock"]:has(.cin-lang-bar) [data-testid="stButton"] > button p,
        div[data-testid="stHorizontalBlock"]:has(.cin-lang-bar) [data-testid="stButton"] > button span,
        div[data-testid="stHorizontalBlock"]:has(.cin-lang-bar) [data-testid="stButton"] > button div {{
            font-size: 0.68rem !important;
            line-height: 1 !important;
            color: inherit !important;
        }}
        [data-testid="stSidebar"],
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="collapsedControl"] {{
            display: none !important;
        }}
        [data-testid="stAppViewBlockContainer"] {{
            margin-left: 0 !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100% !important;
        }}
        [data-testid="stMain"] {{
            padding-top: 1.5rem;
            background: {C_BG};
        }}
        [data-testid="stMain"] .block-container {{
            padding-top: 0.5rem;
            padding-bottom: 2.5rem;
            max-width: 1200px;
        }}
        [data-testid="stMain"] h3,
        [data-testid="stMain"] p,
        [data-testid="stMain"] .stCaption,
        [data-testid="stMain"] [data-testid="stCaptionContainer"] {{
            color: {C_MUTED};
        }}
        [data-testid="stSidebar"] {{
            background: {C_SIDEBAR} !important;
            border-right: 1px solid {C_BORDER} !important;
        }}
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {{
            color: {C_TEXT} !important;
        }}
        [data-testid="stSidebar"] .stCaption,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
            color: {C_MUTED} !important;
        }}
        [data-testid="stSidebar"] .stRadio label,
        [data-testid="stSidebar"] .stRadio label span,
        [data-testid="stSidebar"] .stRadio label p {{
            color: {C_TEXT} !important;
        }}
        [data-testid="stSidebar"] [data-testid="stForm"] {{
            background: {C_CARD} !important;
            border: 1px solid {C_BORDER} !important;
            border-radius: 12px;
            padding: 0.75rem 0.85rem 0.85rem;
            box-shadow: {C_SHADOW};
        }}
        [data-testid="stSidebar"] [data-testid="stForm"] label,
        [data-testid="stSidebar"] [data-testid="stForm"] label p,
        [data-testid="stSidebar"] [data-testid="stForm"] label span {{
            color: {C_TEXT} !important;
        }}
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] textarea,
        [data-testid="stSidebar"] [data-testid="stNumberInput"] input,
        [data-testid="stSidebar"] [data-testid="stDateInput"] input {{
            color: {C_TEXT} !important;
            background: {C_BG} !important;
            border-color: {C_BORDER} !important;
        }}
        [data-testid="stSidebar"] .stButton button,
        [data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button,
        [data-testid="stSidebar"] button[kind="primary"],
        [data-testid="stSidebar"] button[kind="secondaryFormSubmit"] {{
            background: {C_PRIMARY} !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
        }}
        [data-testid="stSidebar"] .stButton button p,
        [data-testid="stSidebar"] .stButton button span,
        [data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button p,
        [data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button span,
        [data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button div {{
            color: #ffffff !important;
        }}
        [data-testid="stSidebar"] [data-testid="stExpander"] {{
            background: transparent !important;
            border: none !important;
        }}
        [data-testid="stSidebar"] [data-testid="stExpander"] details {{
            background: {C_CARD} !important;
            border: 1px solid {C_BORDER} !important;
            border-radius: 12px;
            margin-bottom: 0.35rem;
        }}
        [data-testid="stSidebar"] [data-testid="stExpander"] details summary,
        [data-testid="stSidebar"] [data-testid="stExpander"] details summary span,
        [data-testid="stSidebar"] [data-testid="stExpander"] details summary p,
        [data-testid="stSidebar"] [data-testid="stExpander"] details summary div,
        [data-testid="stSidebar"] [data-testid="stExpander"] [role="button"],
        [data-testid="stSidebar"] [data-testid="stExpander"] [role="button"] p,
        [data-testid="stSidebar"] [data-testid="stExpander"] [role="button"] span,
        [data-testid="stSidebar"] [data-testid="stExpander"] [role="button"] div {{
            background: {C_CARD} !important;
            color: {C_TEXT} !important;
            -webkit-text-fill-color: {C_TEXT} !important;
        }}
        [data-testid="stSidebar"] [data-testid="stExpander"] details[open] summary {{
            border-bottom: 1px solid {C_BORDER} !important;
            border-radius: 12px 12px 0 0 !important;
        }}
        [data-testid="stSidebar"] [data-testid="stExpanderDetails"],
        [data-testid="stSidebar"] [data-testid="stExpander"] .streamlit-expanderContent {{
            background: {C_CARD} !important;
            border-radius: 0 0 12px 12px;
        }}
        [data-testid="stSidebar"] [data-testid="stExpander"] label,
        [data-testid="stSidebar"] [data-testid="stExpander"] label p,
        [data-testid="stSidebar"] [data-testid="stExpander"] label span,
        [data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stWidgetLabel"] p,
        [data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stMarkdown"] p {{
            color: {C_TEXT} !important;
        }}
        [data-testid="stSidebar"] [data-testid="stExpander"] input,
        [data-testid="stSidebar"] [data-testid="stExpander"] textarea,
        [data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stNumberInput"] input {{
            color: #1e1b4b !important;
            background: #ffffff !important;
            border-color: #c7d2fe !important;
        }}
        [data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stCaptionContainer"],
        [data-testid="stSidebar"] [data-testid="stExpander"] .stCaption {{
            color: #c7d2fe !important;
        }}
        [data-testid="stSidebar"] [data-testid="stExpander"] svg {{
            fill: #c7d2fe !important;
            color: #c7d2fe !important;
        }}
        [data-testid="stSidebar"] button[kind="secondary"]:not([data-testid="stFormSubmitButton"] button) {{
            background: {C_BG} !important;
            color: {C_RED} !important;
            border: 1px solid {C_BORDER} !important;
        }}
        [data-testid="stSidebar"] .stCheckbox label,
        [data-testid="stSidebar"] .stCheckbox label p,
        [data-testid="stSidebar"] .stCheckbox label span {{
            color: {C_TEXT} !important;
        }}
        .cin-sidebar-edit {{
            background: {C_CARD};
            border: 1px solid {C_BORDER};
            border-radius: 12px;
            padding: 0.65rem 0.75rem 0.75rem;
            margin: 0.15rem 0 0.55rem;
            box-shadow: {C_SHADOW};
        }}
        .cin-sidebar-edit label,
        .cin-sidebar-edit label p,
        .cin-sidebar-edit label span {{
            color: {C_TEXT} !important;
        }}
        .cin-hero-top {{
            background: linear-gradient(145deg, #ffffff 0%, #f8faff 42%, #eef3ff 100%);
            border: 1px solid rgba(0, 122, 255, 0.1);
            border-radius: 18px;
            padding: 1.1rem 1.25rem 0.95rem;
            margin-bottom: 0.65rem;
            box-shadow: 0 4px 24px rgba(0, 122, 255, 0.07), 0 1px 3px rgba(0, 0, 0, 0.04);
            position: relative;
            overflow: hidden;
        }}
        .cin-hero-top::before {{
            content: "";
            position: absolute;
            top: -55%;
            right: -8%;
            width: 320px;
            height: 320px;
            background: radial-gradient(circle, rgba(0, 122, 255, 0.09) 0%, transparent 68%);
            pointer-events: none;
        }}
        .cin-hero-brand {{
            display: flex;
            align-items: flex-start;
            gap: 0.9rem;
            position: relative;
            z-index: 1;
        }}
        .cin-hero-icon {{
            flex-shrink: 0;
            width: 40px;
            height: 40px;
            border-radius: 11px;
            background: linear-gradient(135deg, #007AFF 0%, #0051D5 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.15rem;
            line-height: 1;
            box-shadow: 0 3px 10px rgba(0, 122, 255, 0.28);
        }}
        .cin-hero-tag {{
            font-size: 0.62rem;
            font-weight: 600;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: {C_PRIMARY};
            margin-bottom: 0.15rem;
        }}
        .cin-hero-title {{
            margin: 0;
            font-size: 1.55rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            color: {C_TEXT};
            line-height: 1.15;
        }}
        .cin-hero-sub {{
            margin: 0.35rem 0 0;
            font-size: 0.82rem;
            color: {C_MUTED};
            max-width: 36rem;
            line-height: 1.45;
        }}
        .cin-hero-today {{
            margin: 0.4rem 0 0;
            font-size: 0.72rem;
            color: {C_MUTED};
            font-weight: 500;
        }}
        .cin-hero-toolbar {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 0.85rem;
            padding-top: 0.75rem;
            border-top: 1px solid rgba(0, 122, 255, 0.08);
            position: relative;
            z-index: 1;
        }}
        div[data-testid="column"]:has(.cin-hero-actions) [data-testid="stButton"] > button {{
            min-height: 2rem !important;
            padding: 0.3rem 0.75rem !important;
            font-size: 0.8rem !important;
            border-radius: 9px !important;
            font-weight: 600 !important;
        }}
        div[data-testid="column"]:has(.cin-hero-actions) [data-testid="stButton"]:first-child > button {{
            background: {C_PRIMARY} !important;
            color: #ffffff !important;
            border: none !important;
        }}
        div[data-testid="column"]:has(.cin-hero-actions) [data-testid="stButton"]:nth-child(2) > button,
        div[data-testid="column"]:has(.cin-hero-actions) + div [data-testid="stButton"] > button {{
            background: {C_CARD} !important;
            color: {C_TEXT} !important;
            border: 1px solid {C_BORDER} !important;
        }}
        .cin-hero-demo {{
            display: none !important;
        }}
        .cin-demo-banner {{
            margin: 0 0 0.85rem;
            padding: 0.65rem 1rem;
            border-radius: 12px;
            background: linear-gradient(90deg, rgba(255, 149, 0, 0.14) 0%, rgba(255, 59, 48, 0.08) 100%);
            border: 1px solid rgba(255, 149, 0, 0.35);
            font-size: 0.86rem;
            line-height: 1.5;
            color: {C_TEXT};
        }}
        .cin-demo-banner strong {{
            color: #b45309;
        }}
        .cin-product-notice {{
            margin: 0.5rem 0 1.25rem;
        }}
        .cin-product-notice [data-testid="stAlert"] {{
            border-radius: 12px;
            border: 1px solid rgba(0, 122, 255, 0.28);
            background: rgba(0, 122, 255, 0.06);
        }}
        .cin-cta-lead {{
            margin-top: 1.1rem;
            padding: 1rem 1.15rem;
            border-radius: 14px;
            background: linear-gradient(135deg, rgba(0, 122, 255, 0.12) 0%, rgba(0, 122, 255, 0.04) 100%);
            border: 2px solid {C_PRIMARY};
            box-shadow: {C_SHADOW};
        }}
        .cin-cta-lead p {{
            margin: 0.35rem 0;
            font-size: 0.88rem;
            line-height: 1.55;
            color: {C_TEXT};
        }}
        .cin-cta-lead strong {{
            color: {C_PRIMARY};
        }}
        .cin-cta-lead a {{
            color: {C_PRIMARY};
            font-weight: 600;
            text-decoration: none;
        }}
        .cin-cta-lead a:hover {{
            text-decoration: underline;
        }}
        .cin-footer-cta {{
            margin: 2rem 0 1.5rem;
            padding: 1.25rem 1.35rem;
            border-radius: 16px;
            background: {C_CARD};
            border: 1px solid {C_BORDER};
            box-shadow: {C_SHADOW};
        }}
        .cin-footer-cta p {{
            margin: 0.4rem 0;
            font-size: 0.9rem;
            line-height: 1.6;
            color: {C_TEXT};
        }}
        .cin-footer-cta strong {{
            color: {C_PRIMARY};
        }}
        .cin-footer-cta a {{
            color: {C_PRIMARY};
            font-weight: 600;
            text-decoration: none;
        }}
        .cin-section-title {{
            font-size: 0.95rem;
            font-weight: 600;
            color: {C_TEXT};
            letter-spacing: -0.02em;
            margin: 1.25rem 0 0.85rem;
        }}
        .cin-kpi-row-marker {{
            display: none !important;
        }}
        [data-testid="element-container"]:has(.cin-kpi-row-marker) {{
            margin: 0 !important;
            padding: 0 !important;
            min-height: 0 !important;
        }}
        div[data-testid="stHorizontalBlock"]:has(.cin-kpi-row-marker) {{
            padding: 6px 2px 18px;
            margin-bottom: 0.25rem;
        }}
        .cin-kpi-wrap {{
            display: none !important;
        }}
        [data-testid="element-container"]:has(.cin-kpi-wrap) {{
            margin: 0 !important;
            padding: 0 !important;
            min-height: 0 !important;
        }}
        div[data-testid="column"]:has(.cin-kpi-wrap) {{
            display: grid !important;
            grid-template: 1fr / 1fr !important;
            align-items: stretch !important;
        }}
        div[data-testid="column"]:has(.cin-kpi-wrap) > [data-testid="element-container"] {{
            grid-area: 1 / 1 !important;
            min-width: 0 !important;
        }}
        div[data-testid="column"]:has(.cin-kpi-wrap) [data-testid="element-container"]:has(.cin-kpi-card) {{
            z-index: 1 !important;
            pointer-events: none !important;
        }}
        div[data-testid="column"]:has(.cin-kpi-wrap) {{
            position: relative !important;
        }}
        div[data-testid="column"]:has(.cin-kpi-wrap) [data-testid="element-container"]:has([data-testid="stButton"]) {{
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            z-index: 2 !important;
            margin: 0 !important;
            padding: 0 !important;
            height: 132px !important;
            display: block !important;
        }}
        div[data-testid="column"]:has(.cin-kpi-wrap) [data-testid="stButton"] {{
            width: 100% !important;
            height: 100% !important;
            margin: 0 !important;
        }}
        div[data-testid="column"]:has(.cin-kpi-wrap) [data-testid="stButton"] > button {{
            min-height: 132px !important;
            height: 100% !important;
            width: 100% !important;
            opacity: 0 !important;
            background: transparent !important;
            color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
            cursor: pointer !important;
        }}
        div[data-testid="column"]:has(.cin-kpi-wrap) [data-testid="stButton"] > button p,
        div[data-testid="column"]:has(.cin-kpi-wrap) [data-testid="stButton"] > button span,
        div[data-testid="column"]:has(.cin-kpi-wrap) [data-testid="stButton"] > button div {{
            opacity: 0 !important;
            font-size: 0 !important;
            line-height: 0 !important;
            visibility: hidden !important;
        }}
        .cin-kpi-card {{
            background: {C_CARD};
            border: 1px solid {C_BORDER};
            border-radius: 12px;
            padding: 18px 14px;
            min-height: 132px;
            box-shadow: {C_SHADOW};
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            width: 100%;
            cursor: default;
            position: relative;
            z-index: 1;
            transition: box-shadow 0.25s ease, transform 0.25s ease;
        }}
        .cin-kpi-card:hover {{
            box-shadow: {C_SHADOW_HOVER};
            transform: translateY(-2px);
        }}
        div[data-testid="column"]:has(.cin-kpi-wrap):hover .cin-kpi-card {{
            box-shadow: {C_SHADOW_HOVER};
            transform: translateY(-2px);
        }}
        div[data-testid="column"]:has(.cin-kpi-wrap):active .cin-kpi-card {{
            transform: translateY(0);
            transition-duration: 0.1s;
        }}
        .cin-kpi-card:active {{
            transform: translateY(0);
            transition-duration: 0.1s;
        }}
        .cin-kpi-card--active {{
            box-shadow: 0 0 0 2px rgba(0, 122, 255, 0.18), {C_SHADOW};
        }}
        .cin-kpi-card--accent {{ border-top: 3px solid {C_PRIMARY}; }}
        .cin-kpi-card--warn {{ border-top: 3px solid {C_AMBER}; }}
        .cin-kpi-card--danger {{ border-top: 3px solid {C_RED}; }}
        .cin-kpi-card--ok {{ border-top: 3px solid {C_GREEN}; }}
        .cin-kpi-lbl {{
            font-size: 0.7rem;
            font-weight: 600;
            color: {C_MUTED};
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 8px;
            line-height: 1.4;
        }}
        .cin-kpi-val {{
            font-size: 2.15rem;
            font-weight: 700;
            color: {C_TEXT};
            letter-spacing: -0.04em;
            line-height: 1.05;
        }}
        .cin-kpi-sub {{
            font-size: 0.7rem;
            color: {C_MUTED};
            margin-top: 10px;
            font-weight: 500;
            line-height: 1.35;
        }}
        .cin-section-anchor {{
            scroll-margin-top: 1.25rem;
        }}
        @media (prefers-reduced-motion: reduce) {{
            .cin-kpi-card,
            .cin-kpi-card:hover,
            .cin-kpi-card:active {{
                transition: none;
                transform: none;
            }}
        }}
        .cin-status-pill {{
            display: inline-flex;
            align-items: center;
            padding: 4px 8px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            line-height: 1.2;
            white-space: nowrap;
            letter-spacing: 0.01em;
        }}
        .cin-status-pill--expired,
        .cin-status-pill--urgent {{
            background: rgba(255, 59, 48, 0.1);
            color: {C_RED};
        }}
        .cin-status-pill--warning {{
            background: rgba(255, 149, 0, 0.1);
            color: {C_AMBER};
        }}
        .cin-status-pill--healthy {{
            background: rgba(52, 199, 89, 0.1);
            color: {C_GREEN};
        }}
        .cin-panel {{
            background: transparent;
            border: none;
            border-radius: 0;
            padding: 0;
            margin-bottom: 1.25rem;
        }}
        .cin-panel h3 {{
            margin: 0 0 0.85rem;
            font-size: 0.875rem;
            font-weight: 600;
            color: {C_TEXT};
            letter-spacing: -0.01em;
        }}
        .cin-card {{
            background: {C_CARD};
            border: 1px solid {C_BORDER};
            border-radius: 12px;
            padding: 1.2rem 1.25rem;
            height: 100%;
            box-shadow: {C_SHADOW};
            transition: box-shadow 0.25s ease, transform 0.25s ease;
        }}
        .cin-card:hover {{
            box-shadow: {C_SHADOW_HOVER};
            transform: translateY(-2px);
        }}
        .cin-card-head {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 0.65rem;
        }}
        .cin-field {{
            margin-bottom: 0.7rem;
        }}
        .cin-field-lbl {{
            display: block;
            font-size: 0.65rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: {C_MUTED};
            margin-bottom: 0.2rem;
            line-height: 1.35;
        }}
        .cin-field-val {{
            display: block;
            font-size: 1rem;
            font-weight: 600;
            color: {C_TEXT};
            line-height: 1.4;
            word-break: break-word;
        }}
        .cin-field-val--muted {{
            font-weight: 500;
            color: {C_MUTED};
            font-size: 0.875rem;
        }}
        .cin-field--highlight .cin-field-val {{
            color: {C_PRIMARY};
            font-size: 0.9rem;
            font-weight: 600;
        }}
        .cin-card-stats {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.5rem;
            margin: 0.65rem 0 0.75rem;
            padding: 0.65rem 0;
            border-top: 1px solid {C_BORDER};
            border-bottom: 1px solid {C_BORDER};
        }}
        .cin-tracker-wrap {{
            display: block;
            margin-bottom: 0.35rem;
        }}
        .cin-card-unit {{
            margin-bottom: 0;
        }}
        .cin-card-unit .cin-card {{
            margin-bottom: 0;
        }}
        [data-testid="element-container"]:has(.cin-card-unit) {{
            margin-bottom: 0 !important;
        }}
        [data-testid="element-container"]:has(.cin-card-unit) + [data-testid="element-container"] {{
            margin-top: 0.4rem !important;
            margin-bottom: 1.1rem !important;
        }}
        [data-testid="element-container"]:has(.cin-card-unit) + [data-testid="element-container"] [data-testid="stButton"] > button {{
            width: 100% !important;
        }}
        .cin-prog-wrap {{
            min-height: 38px;
            margin: 0.5rem 0 0.35rem;
            padding: 0 0.15rem;
        }}
        .cin-prog-bar {{
            height: 6px;
            background: rgba(0, 0, 0, 0.06);
            border-radius: 999px;
            overflow: hidden;
        }}
        .cin-prog-fill {{
            height: 100%;
            background: linear-gradient(90deg, {C_PRIMARY} 0%, #5AC8FA 100%);
            border-radius: 999px;
            transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .cin-prog-meta {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 6px;
            gap: 0.5rem;
        }}
        .cin-prog-txt {{
            font-size: 0.75rem;
            color: {C_MUTED};
            line-height: 1.35;
            font-weight: 500;
        }}
        .cin-prog-pct {{
            font-size: 0.72rem;
            font-weight: 600;
            color: {C_PRIMARY};
            letter-spacing: 0.02em;
        }}
        .cin-badge {{
            display: inline-block;
            font-size: 0.62rem;
            font-weight: 700;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            padding: 3px 8px;
            border-radius: 20px;
        }}
        .cin-badge.expiry {{
            background: {C_PRIMARY_LIGHT};
            color: {C_PRIMARY};
        }}
        .cin-badge.milestone {{
            background: rgba(175, 82, 222, 0.1);
            color: #AF52DE;
        }}
        .cin-count {{
            font-size: 1.625rem;
            font-weight: 700;
            line-height: 1.1;
            letter-spacing: -0.02em;
        }}
        .cin-filter-pill-marker,
        .cin-filter-row-marker {{
            display: none;
        }}
        [data-testid="stHorizontalBlock"]:has(.cin-filter-pill-marker) {{
            margin-bottom: 1.25rem;
        }}
        [data-testid="stHorizontalBlock"]:has(.cin-filter-pill-marker) .stButton > button {{
            background: {C_BG} !important;
            color: {C_MUTED} !important;
            border: 1px solid {C_BORDER} !important;
            border-radius: 999px !important;
            font-size: 0.8rem !important;
            font-weight: 500 !important;
            padding: 0.45rem 0.75rem !important;
            min-height: 2.25rem !important;
            box-shadow: none !important;
            transition: all 0.2s ease !important;
        }}
        [data-testid="stHorizontalBlock"]:has(.cin-filter-pill-marker) .stButton > button:hover {{
            background: {C_CARD} !important;
            color: {C_TEXT} !important;
            border-color: rgba(0, 0, 0, 0.1) !important;
            transform: none !important;
        }}
        [data-testid="column"]:has(.cin-filter-pill-marker.is-active) .stButton > button {{
            background: {C_PRIMARY_LIGHT} !important;
            color: {C_PRIMARY} !important;
            border-color: rgba(0, 122, 255, 0.25) !important;
            box-shadow: none !important;
            font-weight: 600 !important;
        }}
        [data-testid="column"]:has(.cin-compose-anchor) {{
            background: {C_COMPOSE};
            border: 1px solid {C_BORDER};
            border-radius: 12px;
            padding: 20px;
            align-self: flex-start;
            position: sticky;
            top: 1rem;
            box-shadow: {C_SHADOW};
        }}
        .cin-compose-header h3 {{
            margin: 0 0 0.35rem;
            font-size: 0.95rem;
            font-weight: 600;
            color: {C_TEXT};
            letter-spacing: -0.02em;
        }}
        .cin-compose-header p {{
            margin: 0 0 1.15rem;
            font-size: 0.82rem;
            color: {C_MUTED};
            line-height: 1.5;
        }}
        .cin-compose-meta {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 0.5rem;
            margin: 0.25rem 0 0.85rem;
        }}
        .cin-compose-days {{
            font-size: 0.8rem;
            font-weight: 600;
            color: {C_MUTED};
        }}
        .cin-compose-next {{
            margin-bottom: 1rem !important;
        }}
        .cin-priority-list {{
            display: flex;
            flex-direction: column;
            gap: 0;
            width: 100%;
        }}
        .cin-priority-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.85rem;
            width: 100%;
            box-sizing: border-box;
            background-color: {C_CARD};
            border: 1px solid {C_BORDER};
            border-radius: 12px;
            padding: 12px 16px;
            margin-bottom: 8px;
            font-size: 0.875rem;
            line-height: 1.45;
            box-shadow: {C_SHADOW};
        }}
        .cin-priority-row:last-child {{
            margin-bottom: 0;
        }}
        .cin-priority-meta {{
            flex: 1;
            min-width: 0;
        }}
        .cin-priority-name {{
            font-weight: 600;
            color: {C_TEXT};
            display: block;
            font-size: 0.9rem;
        }}
        .cin-priority-svc {{
            font-size: 0.78rem;
            color: {C_MUTED};
            display: block;
            margin-top: 0.15rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        [data-testid="stMain"] .stButton button[kind="secondary"] {{
            background: {C_CARD} !important;
            color: {C_TEXT} !important;
            border: 1px solid {C_BORDER} !important;
            border-radius: 10px !important;
        }}
        [data-testid="stMain"] .stButton button[kind="primary"],
        [data-testid="stMain"] button[kind="primary"] {{
            background: {C_PRIMARY} !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }}
        [data-testid="stMain"] .stCheckbox label p,
        [data-testid="stMain"] .stCheckbox label span {{
            color: {C_TEXT} !important;
        }}
        [data-testid="stMain"] .stRadio label p,
        [data-testid="stMain"] .stRadio label span {{
            color: {C_MUTED} !important;
            font-size: 0.82rem !important;
        }}
        [data-testid="stMain"] .stSelectbox label,
        [data-testid="stMain"] [data-testid="stWidgetLabel"] p {{
            color: {C_MUTED} !important;
            font-size: 0.8rem !important;
        }}
        [data-testid="column"]:has(.cin-compose-anchor) [data-testid="stTextArea"] textarea {{
            background: {C_BG} !important;
            color: {C_TEXT} !important;
            border: 1px solid {C_BORDER} !important;
            border-radius: 10px !important;
            font-size: 0.82rem !important;
            line-height: 1.55 !important;
        }}
        [data-testid="column"]:has(.cin-compose-anchor) [data-baseweb="select"] > div {{
            background: {C_BG} !important;
            border-color: {C_BORDER} !important;
            border-radius: 10px !important;
        }}
        [data-testid="column"]:has(.cin-compose-anchor) [data-baseweb="select"] span {{
            color: {C_TEXT} !important;
        }}
        .cin-tracker-panel {{
            background: {C_BG};
            border: 1px solid {C_BORDER};
            border-radius: 12px;
            padding: 1rem 1.05rem;
            margin: 0.75rem 0 1rem;
        }}
        .cin-tracker-panel h4 {{
            margin: 0 0 0.35rem;
            font-size: 0.85rem;
            font-weight: 600;
            color: {C_TEXT};
        }}
        .cin-tracker-panel .cap {{
            font-size: 0.76rem;
            color: {C_MUTED};
            margin-bottom: 0.65rem;
            line-height: 1.45;
        }}
        .cin-ms-log {{
            max-height: 240px;
            overflow-y: auto;
        }}
        .cin-ms-row {{
            border-radius: 8px;
            padding: 0.4rem 0.55rem;
            margin: 0.28rem 0;
            font-size: 0.82rem;
            line-height: 1.35;
        }}
        .cin-ms-row--done {{
            background: rgba(52, 199, 89, 0.08);
            border: 1px solid rgba(52, 199, 89, 0.2);
            color: {C_GREEN};
            font-weight: 600;
        }}
        .cin-ms-row--locked {{
            color: {C_MUTED};
            padding-left: 0.65rem;
        }}
        .cin-ms-row--active {{
            background: {C_PRIMARY_LIGHT};
            border: 1px dashed rgba(0, 122, 255, 0.25);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_copy_button(
    label: str,
    text: str,
    key: str,
    *,
    L: str = "en",
    primary: bool = False,
) -> None:
    if hasattr(st, "copy_button"):
        kwargs: dict[str, Any] = {
            "label": label,
            "text": text,
            "use_container_width": True,
            "key": key,
        }
        if primary:
            kwargs["type"] = "primary"
        st.copy_button(**kwargs)
        return

    btn_id = re.sub(r"[^a-zA-Z0-9_]", "_", key)
    safe_label = json.dumps(label)
    safe_done = json.dumps(t(L, "copy_done"))
    safe_text = json.dumps(text)
    bg = C_PRIMARY if primary else "#f0f2f6"
    fg = "#ffffff" if primary else "#31333f"
    components.html(
        f"""
        <button id="{btn_id}" type="button" style="
            width:100%; margin-top:6px; padding:0.55rem 1rem; border:none;
            border-radius:0.5rem; background:{bg}; color:{fg};
            cursor:pointer; font-size:14px; font-weight:500;
        "></button>
        <script>
        (function() {{
            var btn = document.getElementById("{btn_id}");
            btn.textContent = {safe_label};
            btn.onclick = function() {{
                navigator.clipboard.writeText({safe_text}).then(function() {{
                    btn.textContent = {safe_done};
                    setTimeout(function() {{ btn.textContent = {safe_label}; }}, 1600);
                }});
            }};
        }})();
        </script>
        """,
        height=48,
    )
    st.caption(t(L, "copy_fallback"))


def render_compose_actions(
    L: str,
    message: str,
    client: dict,
    msg_key: str,
) -> None:
    channel = st.session_state.compose_channel
    if channel == CHANNEL_EMAIL:
        c1, c2 = st.columns(2)
        with c1:
            render_copy_button(
                t(L, "copy_btn"), message,
                key=f"copy_{msg_key}",
                L=L, primary=True,
            )
        with c2:
            subject, body = parse_email_message(message)
            mailto = build_mailto_link(client.get("client_email", ""), subject, body)
            if mailto:
                st.link_button(
                    t(L, "email_open_btn"),
                    mailto,
                    use_container_width=True,
                    type="primary",
                )
            else:
                st.button(
                    t(L, "email_open_btn"),
                    disabled=True,
                    use_container_width=True,
                )
                st.caption(t(L, "email_no_address"))
    else:
        render_copy_button(
            t(L, "copy_btn"), message,
            key=f"copy_{msg_key}",
            L=L, primary=True,
        )


_ZH_CN_SINGLE = (
    ("體", "体"), ("臺", "台"), ("灣", "湾"), ("訊", "信"), ("據", "据"), ("與", "与"),
    ("為", "为"), ("務", "务"), ("開", "开"), ("關", "关"), ("後", "后"), ("這", "这"),
    ("們", "们"), ("來", "来"), ("個", "个"), ("時", "时"), ("過", "过"), ("還", "还"),
    ("請", "请"), ("對", "对"), ("說", "说"), ("會", "会"), ("無", "无"), ("從", "从"),
    ("當", "当"), ("應", "应"), ("處", "处"), ("進", "进"), ("達", "达"), ("選", "选"),
    ("擇", "择"), ("復", "复"), ("製", "制"), ("複", "复"), ("擴", "扩"), ("條", "条"),
    ("記", "记"), ("錄", "录"), ("預", "预"), ("計", "计"), ("劃", "划"), ("標", "标"),
    ("準", "准"), ("確", "确"), ("認", "认"), ("證", "证"), ("擊", "击"), ("專", "专"),
    ("業", "业"), ("員", "员"), ("戶", "户"), ("聯", "联"), ("絡", "络"), ("電", "电"),
    ("郵", "邮"), ("編", "编"), ("輯", "辑"), ("儲", "储"), ("變", "变"), ("刪", "删"),
    ("項", "项"), ("單", "单"), ("週", "周"), ("裝", "装"), ("餘", "余"), ("僅", "仅"),
    ("強", "强"), ("溫", "温"), ("帳", "账"), ("滯", "滞"), ("納", "纳"), ("違", "违"),
    ("約", "约"), ("費", "费"), ("裡", "里"), ("發", "发"), ("順", "顺"), ("詢", "询"),
    ("問", "问"), ("題", "题"), ("質", "质"), ("檢", "检"), ("視", "视"), ("覽", "览"),
    ("蹤", "踪"), ("親", "亲"), ("愛", "爱"), ("國", "国"), ("學", "学"), ("習", "习"),
    ("產", "产"), ("經", "经"), ("濟", "济"), ("區", "区"), ("東", "东"), ("廣", "广"),
    ("場", "场"), ("園", "园"), ("號", "号"), ("樓", "楼"), ("層", "层"), ("價", "价"),
    ("買", "买"), ("賣", "卖"), ("購", "购"), ("貨", "货"), ("護", "护"), ("環", "环"),
    ("節", "节"), ("優", "优"), ("讓", "让"), ("議", "议"), ("談", "谈"), ("論", "论"),
    ("調", "调"), ("協", "协"), ("幫", "帮"), ("設", "设"), ("備", "备"), ("維", "维"),
    ("報", "报"), ("導", "导"), ("師", "师"), ("課", "课"), ("訓", "练"), ("練", "练"),
    ("續", "续"), ("麼", "么"), ("於", "于"), ("將", "将"), ("餘", "余"),
)


def to_zh_cn(text: str) -> str:
    for old, new in (
        ("追蹤看板", "追踪看板"), ("進度追蹤", "服务进度追踪"), ("撤回上一筆", "撤销上一步"),
        ("下一次預計上門日", "下一次预计上门日"), ("聯絡人", "联系人"), ("客戶", "客户"),
        ("儲存變更", "保存变更"), ("編輯資料", "编辑资料"), ("訊息草稿", "消息草稿"),
        ("側欄", "侧栏"), ("套裝", "套餐"), ("到府紀錄", "上门记录"), ("溫馨", "温馨"),
        ("敬祝 順心", "此致敬礼"), ("帳務", "账务"), ("尚無", "尚无"),
    ):
        text = text.replace(old, new)
    for old, new in _ZH_CN_SINGLE:
        text = text.replace(old, new)
    return text


def _lookup_lang(L: str, key: str) -> str:
    if L == "zh_cn":
        if key in LANG.get("zh_cn", {}):
            return LANG["zh_cn"][key]
        if key in LANG.get("zh", {}):
            return to_zh_cn(LANG["zh"][key])
    if key in LANG.get(L, {}):
        return LANG[L][key]
    if key in LANG.get("en", {}):
        return LANG["en"][key]
    if key.endswith("_collect"):
        return _lookup_lang(L, key[: -len("_collect")])
    return key


def t(L: str, key: str, **fmt) -> str:
    text = _lookup_lang(L, key)
    if fmt:
        try:
            return text.format(**fmt)
        except (KeyError, ValueError):
            return text
    return text


def mode_label(L: str, mode: str) -> str:
    return t(L, "mode_single" if mode == MODE_SINGLE else "mode_milestone")


def current_lang() -> str:
    """Production build: English-only UI for global B2B clients."""
    return "en"


def channel_label(L: str, channel: str) -> str:
    return t(L, f"channel_{channel}")


def parse_email_message(message: str) -> tuple[str, str]:
    lines = message.splitlines()
    subject = ""
    body_start = 0
    if lines and lines[0].startswith("Subject:"):
        subject = lines[0][len("Subject:") :].strip()
        body_start = 1
    if body_start < len(lines) and lines[body_start].startswith("To:"):
        body_start += 1
    while body_start < len(lines) and not lines[body_start].strip():
        body_start += 1
    body = "\n".join(lines[body_start:])
    return subject, body


def build_mailto_link(email: str, subject: str, body: str) -> str:
    addr = (email or "").strip()
    if not addr or addr == "—":
        return ""
    query = urlencode({"subject": subject, "body": body}, quote_via=quote)
    return f"mailto:{addr}?{query}"


def _today() -> date:
    return date.today()


def _new_id() -> str:
    return str(uuid.uuid4())[:8]


def _ordinal_suffix(n: int) -> str:
    if 10 <= (n % 100) <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def milestone_service_label(index_1based: int, L: str) -> str:
    if L in ("zh", "zh_cn"):
        return t(L, "ms_service", n=index_1based)
    return t(
        L, "ms_service",
        n=index_1based,
        suffix=_ordinal_suffix(index_1based),
    )


def _build_milestone_dates(total: int, done: int, base: date | None = None) -> list[str | None]:
    """Seed completion dates for demo / migration (sequential, one week apart)."""
    if total <= 0:
        return []
    base = base or _today()
    dates: list[str | None] = []
    for i in range(total):
        if i < done:
            dates.append(format_end_date(base - timedelta(days=7 * (done - 1 - i))))
        else:
            dates.append(None)
    return dates


def ensure_milestone_dates(client: dict[str, Any]) -> list[str | None]:
    total = int(client.get("total_milestones") or 0)
    if total <= 0:
        client["milestone_dates"] = []
        client["completed_milestones"] = 0
        return []

    raw = client.get("milestone_dates")
    if raw is None:
        done = int(client.get("completed_milestones") or 0)
        raw = _build_milestone_dates(total, min(done, total))
        client["milestone_dates"] = raw
    else:
        raw = list(raw)
        while len(raw) < total:
            raw.append(None)
        if len(raw) > total:
            raw = raw[:total]
        client["milestone_dates"] = raw

    sync_completed_from_dates(client)
    return client["milestone_dates"]


def sync_completed_from_dates(client: dict[str, Any]) -> None:
    dates = client.get("milestone_dates") or []
    client["completed_milestones"] = sum(1 for d in dates if d)


def milestone_done_count(client: dict) -> int:
    if client.get("mode") != MODE_MILESTONE:
        return 0
    return int(client.get("completed_milestones") or 0)


def set_milestone_checked(client: dict, index: int, checked: bool) -> None:
    dates = ensure_milestone_dates(client)
    if index < 0 or index >= len(dates):
        return
    done = milestone_done_count(client)
    if checked:
        if index != done:
            return
        dates[index] = format_end_date(_today())
    else:
        if index != done - 1:
            return
        dates[index] = None
    sync_completed_from_dates(client)


def milestone_history_text(client: dict, L: str) -> tuple[str, str, str]:
    """Returns (history_block, history_latest, latest_label)."""
    program = client.get("service_label") or t(L, "msg_default_label")
    dates = ensure_milestone_dates(client)
    lines: list[str] = []
    latest_label = ""
    latest_date = ""
    for i, d in enumerate(dates):
        if d:
            label = milestone_service_label(i + 1, L)
            lines.append(t(L, "history_line", label=label, date=d))
            latest_label = label
            latest_date = d
    block = "\n".join(lines) if lines else t(L, "history_none")
    latest = (
        t(L, "history_latest", label=latest_label, date=latest_date, program=program)
        if latest_label
        else ""
    )
    return block, latest, latest_label


def _default_clients() -> list[dict[str, Any]]:
    t0 = _today()
    return [
        {
            "id": _new_id(),
            "mode": MODE_SINGLE,
            "client_name": "Client A — Tutoring",
            "contact_name": "Contact A",
            "client_email": "client-a@example.com",
            "service_label": "English Tutoring Package",
            "end_date": t0 + timedelta(days=14),
            "start_date": t0,
            "total_milestones": None,
            "completed_milestones": None,
        },
        {
            "id": _new_id(),
            "mode": MODE_SINGLE,
            "client_name": "Client B — Gym",
            "contact_name": "Contact B",
            "client_email": "client-b@example.com",
            "service_label": "10-Session Personal Training",
            "end_date": t0 + timedelta(days=52),
            "start_date": t0,
            "total_milestones": None,
            "completed_milestones": None,
        },
        {
            "id": _new_id(),
            "mode": MODE_MILESTONE,
            "client_name": "Client C — Wellness Co.",
            "contact_name": "Contact C",
            "client_email": "client-c@example.com",
            "service_label": "10-Session Yoga Program",
            "end_date": t0 + timedelta(days=90),
            "start_date": t0,
            "total_milestones": 10,
            "completed_milestones": 3,
            "milestone_dates": _build_milestone_dates(10, 3, t0),
        },
        {
            "id": _new_id(),
            "mode": MODE_MILESTONE,
            "client_name": "Client D — Maintenance",
            "contact_name": "Contact D",
            "client_email": "client-d@example.com",
            "service_label": "CCTV Quarterly Maintenance",
            "end_date": t0 + timedelta(days=8),
            "start_date": t0,
            "total_milestones": 4,
            "completed_milestones": 2,
            "milestone_dates": _build_milestone_dates(4, 2, t0),
        },
    ]


def normalize_client(client: dict[str, Any]) -> dict[str, Any]:
    """Back-fill schema fields for older session data."""
    client.setdefault("contact_name", "")
    client.setdefault("client_email", "")
    client.setdefault("start_date", _today())
    if isinstance(client.get("start_date"), str):
        client["start_date"] = date.fromisoformat(client["start_date"])
    if client.get("mode") == MODE_MILESTONE:
        ensure_milestone_dates(client)
    return client


def init_state() -> None:
    if "clients" not in st.session_state:
        st.session_state.clients = _default_clients()
    else:
        st.session_state.clients = [
            normalize_client(dict(c)) for c in st.session_state.clients
        ]
    if "add_mode" not in st.session_state:
        st.session_state.add_mode = MODE_SINGLE
    if "lang_code" not in st.session_state:
        st.session_state.lang_code = "en"
    if "board_filter" not in st.session_state:
        st.session_state.board_filter = "all"
    if "cin_scroll_target" not in st.session_state:
        st.session_state.cin_scroll_target = None
    if "compose_channel" not in st.session_state:
        st.session_state.compose_channel = CHANNEL_SMS
    elif st.session_state.compose_channel in _LEGACY_IM_CHANNELS:
        st.session_state.compose_channel = CHANNEL_SMS
    elif st.session_state.compose_channel not in ALL_CHANNELS:
        st.session_state.compose_channel = CHANNEL_SMS
    if (
        "compose_payment" not in st.session_state
        or st.session_state.compose_payment
        not in (PAYMENT_ROUTINE, PAYMENT_COLLECTION)
    ):
        st.session_state.compose_payment = PAYMENT_ROUTINE
    if "compose_client_id" not in st.session_state and st.session_state.clients:
        st.session_state.compose_client_id = st.session_state.clients[0]["id"]


def days_remaining(end: date) -> int:
    return (end - _today()).days


def urgency_tier(days: int) -> str:
    if days < 0:
        return "expired"
    if days <= CRITICAL_DAYS:
        return "critical"
    if days <= URGENT_DAYS:
        return "urgent"
    return "ok"


def status_badge_tier(days: int) -> str:
    """Visual pill tier: urgent <15d · warning 15–30d · healthy >30d."""
    if days < 0:
        return "expired"
    if days < CRITICAL_DAYS + 1:
        return "urgent"
    if days <= URGENT_DAYS:
        return "warning"
    return "healthy"


def status_badge_html(days: int, L: str) -> str:
    tier = status_badge_tier(days)
    label = t(L, f"badge_{tier}")
    return (
        f'<span class="cin-status-pill cin-status-pill--{tier}" '
        f'role="status" aria-label="{label}">{label}</span>'
    )


def urgency_class(days: int) -> tuple[str, str]:
    tier = urgency_tier(days)
    colors = {
        "expired": C_RED,
        "critical": C_RED,
        "urgent": C_AMBER,
        "ok": C_GREEN,
    }
    return tier, colors[tier]


def urgency_label(days: int, L: str) -> str:
    tier = urgency_tier(days)
    if tier == "expired":
        return t(L, "status_expired", n=abs(days))
    if tier == "critical":
        return t(L, "status_critical", n=days)
    if tier == "urgent":
        return t(L, "status_urgent", n=days)
    return t(L, "status_ok", n=days)


def days_display(days: int, L: str) -> str:
    if days < 0:
        return t(L, "days_over", n=abs(days))
    return t(L, "days_left", n=days)


def milestone_progress(client: dict) -> float:
    total = int(client.get("total_milestones") or 1)
    if total <= 0:
        return 0.0
    done = milestone_done_count(client)
    return min(1.0, max(0.0, done / total))


def format_end_date(d: date) -> str:
    return d.strftime("%Y-%m-%d")


def next_date_info(client: dict, L: str) -> tuple[str, str, date | None]:
    """
    Returns (label_key, display_text, raw_date).
    label_key is 'next_payment' or 'next_service'.
    """
    if client["mode"] == MODE_SINGLE:
        d = client["end_date"]
        return "next_payment", format_end_date(d), d

    if client.get("mode") == MODE_MILESTONE:
        ensure_milestone_dates(client)
    done = milestone_done_count(client)
    total = int(client.get("total_milestones") or 0)
    if total <= 0:
        return "next_visit", "—", None
    if done >= total:
        return "next_visit", t(L, "all_sessions_done"), None

    today = _today()
    end = client["end_date"]
    start = client.get("start_date") or today
    if not isinstance(start, date):
        start = today

    total_days = (end - today).days
    if total_days < 0:
        total_days = 0

    interval_days = total_days / total
    offset_days = round(interval_days * (done + 1))
    next_d = start + timedelta(days=offset_days)
    if next_d > end:
        next_d = end
    return "next_visit", format_end_date(next_d), next_d


def reminder_template_key(
    client: dict,
    channel: str,
    payment: str,
) -> str:
    mode_suffix = "ms" if client["mode"] == MODE_MILESTONE else "single"
    ch = "email" if channel == CHANNEL_EMAIL else "wa"
    suffix = "_collect" if payment == PAYMENT_COLLECTION else ""
    return f"msg_{ch}_friendly_{mode_suffix}{suffix}"


def build_reminder_message(
    client: dict,
    L: str,
    channel: str,
    payment: str,
) -> str:
    contact = (client.get("contact_name") or "").strip() or t(L, "msg_default_contact")
    email = (client.get("client_email") or "").strip() or "—"
    company = client["client_name"]
    label = client.get("service_label") or t(L, "msg_default_label")
    days = days_remaining(client["end_date"])
    end_str = format_end_date(client["end_date"])
    _, next_str, _ = next_date_info(client, L)
    status = urgency_label(days, L)

    if client["mode"] == MODE_MILESTONE:
        ensure_milestone_dates(client)
    done = milestone_done_count(client)
    total = int(client.get("total_milestones") or 0)
    remain = max(0, total - done)
    overdue_days = abs(days) if days < 0 else days
    history_block, history_latest, _ = milestone_history_text(client, L)
    payment_note = (
        t(L, "note_prepaid")
        if payment == PAYMENT_ROUTINE
        else t(L, "note_collect")
    )
    urgent_note = t(L, "note_urgent")

    key = reminder_template_key(client, channel, payment)
    return t(
        L,
        key,
        contact=contact,
        email=email,
        company=company,
        label=label,
        end=end_str,
        next_date=next_str,
        days=overdue_days,
        done=done,
        total=total,
        remain=remain,
        status=status,
        history_block=history_block,
        history_latest=history_latest,
        history_header=t(L, "history_header"),
        payment_note=payment_note,
        urgent_note=urgent_note,
    )


def client_summary_row(client: dict, L: str) -> dict[str, str]:
    days = days_remaining(client["end_date"])
    if client["mode"] == MODE_MILESTONE:
        detail = t(
            L, "detail_ms",
            done=milestone_done_count(client),
            total=client["total_milestones"],
        )
    else:
        detail = client.get("service_label") or t(L, "detail_single")
    label_key, next_display, _ = next_date_info(client, L)
    return {
        t(L, "col_client"): client["client_name"],
        t(L, "col_contact"): client.get("contact_name") or "—",
        t(L, "col_email"): client.get("client_email") or "—",
        t(L, "col_mode"): mode_label(L, client["mode"]),
        t(L, "col_detail"): detail,
        t(L, "col_end"): format_end_date(client["end_date"]),
        t(L, "col_next"): f"{t(L, label_key)}: {next_display}",
        t(L, "col_status"): urgency_label(days, L),
    }


def filter_clients(clients: list[dict], flt: str) -> list[dict]:
    if flt == "urgent":
        return [c for c in clients if 0 <= days_remaining(c["end_date"]) <= URGENT_DAYS]
    if flt == "expired":
        return [c for c in clients if days_remaining(c["end_date"]) < 0]
    if flt == "milestone":
        return [c for c in clients if c.get("mode") == MODE_MILESTONE]
    return list(clients)


def add_client(
    L: str,
    mode: str,
    client_name: str,
    contact_name: str,
    client_email: str,
    service_label: str,
    end_date: date,
    total_milestones: int,
) -> None:
    entry: dict[str, Any] = {
        "id": _new_id(),
        "mode": mode,
        "client_name": client_name.strip(),
        "contact_name": contact_name.strip(),
        "client_email": client_email.strip(),
        "service_label": service_label.strip() or t(L, "default_service"),
        "end_date": end_date,
        "start_date": _today(),
        "total_milestones": None,
        "completed_milestones": 0,
        "milestone_dates": None,
    }
    if mode == MODE_MILESTONE:
        total = max(1, int(total_milestones))
        entry["total_milestones"] = total
        entry["milestone_dates"] = [None] * total
        entry["completed_milestones"] = 0
    st.session_state.clients.append(entry)
    st.session_state.compose_client_id = entry["id"]


def update_client(
    L: str,
    client_id: str,
    client_name: str,
    contact_name: str,
    client_email: str,
    service_label: str,
    end_date: date,
    total_milestones: int | None = None,
) -> str | None:
    name = client_name.strip()
    if not name:
        return t(L, "err_name")
    for c in st.session_state.clients:
        if c["id"] != client_id:
            continue
        if c.get("mode") == MODE_MILESTONE and total_milestones is not None:
            done = milestone_done_count(c)
            total = max(1, int(total_milestones))
            if total < done:
                return t(L, "err_total_ms", done=done)
            c["total_milestones"] = total
            ensure_milestone_dates(c)
        c["client_name"] = name
        c["contact_name"] = contact_name.strip()
        c["client_email"] = client_email.strip()
        c["service_label"] = service_label.strip() or t(L, "default_service")
        c["end_date"] = end_date
        return None
    return t(L, "err_name")


def render_progress_tracker(client: dict, L: str) -> None:
    """Clerk-facing sequential milestone checklist with auto timestamps."""
    if client.get("mode") != MODE_MILESTONE:
        return

    total = int(client.get("total_milestones") or 0)
    st.markdown(
        f'<div class="cin-tracker-panel">'
        f'<h4>📋 {t(L, "progress_tracker")}</h4>'
        f'<div class="cap">{t(L, "progress_tracker_cap")}</div>',
        unsafe_allow_html=True,
    )

    if total <= 0:
        st.caption(t(L, "progress_empty"))
        st.markdown("</div>", unsafe_allow_html=True)
        return

    dates = ensure_milestone_dates(client)
    done = milestone_done_count(client)
    st.markdown('<div class="cin-ms-log">', unsafe_allow_html=True)

    for i in range(total):
        label = milestone_service_label(i + 1, L)
        is_done = dates[i] is not None
        is_next = (not is_done) and (i == done)
        is_locked = (not is_done) and (i > done)

        if is_done:
            st.markdown(
                f'<div class="cin-ms-row cin-ms-row--done">'
                f'{t(L, "ms_done_row", label=label, date=dates[i])}</div>',
                unsafe_allow_html=True,
            )
            if i == done - 1 and st.button(
                t(L, "ms_undo"),
                key=f"ms_undo_{client['id']}_{i}_{done}",
                use_container_width=True,
            ):
                set_milestone_checked(client, i, False)
                st.rerun()
        elif is_next:
            st.markdown('<div class="cin-ms-row cin-ms-row--active">', unsafe_allow_html=True)
            if st.checkbox(
                label,
                value=False,
                key=f"ms_chk_{client['id']}_{i}_{done}",
            ):
                set_milestone_checked(client, i, True)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        elif is_locked:
            st.markdown(
                f'<div class="cin-ms-row cin-ms-row--locked">○ {label} — {t(L, "ms_locked")}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("</div></div>", unsafe_allow_html=True)


# Backward-compatible alias (older sessions / cached modules)
render_milestone_activity_log = render_progress_tracker


def delete_client(client_id: str) -> None:
    st.session_state.clients = [
        c for c in st.session_state.clients if c["id"] != client_id
    ]
    if st.session_state.clients:
        st.session_state.compose_client_id = st.session_state.clients[0]["id"]
    else:
        st.session_state.compose_client_id = None


def _cleanup_legacy_lang_picker() -> None:
    components.html(
        """
        <script>
        (function() {
            var doc = window.parent.document;
            var old = doc.getElementById("cin-lang-pills-root");
            if (old) old.remove();
            var style = doc.getElementById("cin-lang-styles");
            if (style) style.remove();
        })();
        </script>
        """,
        height=0,
    )


def _md_to_html(text: str) -> str:
    """Minimal markdown: **bold** and paragraphs."""
    parts = []
    for para in text.split("\n\n"):
        line = _html_esc(para)
        line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
        line = re.sub(
            r"checkitnow123@gmail\.com",
            r'<a href="mailto:checkitnow123@gmail.com">checkitnow123@gmail.com</a>',
            line,
        )
        parts.append(f"<p>{line}</p>")
    return "".join(parts)


def render_demo_banner(L: str) -> None:
    st.markdown(
        f'<div class="cin-demo-banner">{_md_to_html(t(L, "demo_banner"))}</div>',
        unsafe_allow_html=True,
    )


def render_product_notice(L: str) -> None:
    st.markdown('<div class="cin-product-notice">', unsafe_allow_html=True)
    st.info(t(L, "product_notice"))
    st.markdown("</div>", unsafe_allow_html=True)


def render_lead_cta(L: str) -> None:
    st.markdown(
        f'<div class="cin-cta-lead">{_md_to_html(t(L, "cta_lead"))}</div>',
        unsafe_allow_html=True,
    )


def render_footer_cta(L: str) -> None:
    st.markdown(
        f'<div class="cin-footer-cta">{_md_to_html(t(L, "footer_cta"))}</div>',
        unsafe_allow_html=True,
    )


def render_lang_picker() -> None:
    """English-only production UI — language picker hidden."""
    return


def render_add_tracker_form(L: str) -> None:
    st.session_state.add_mode = st.radio(
        t(L, "tracker_mode"),
        [MODE_SINGLE, MODE_MILESTONE],
        format_func=lambda m: mode_label(L, m),
        key="tracker_mode_radio",
        label_visibility="collapsed",
    )
    mode = st.session_state.add_mode

    with st.form("add_client_form", clear_on_submit=True):
        client_name = st.text_input(t(L, "client_name"), placeholder=t(L, "client_ph"))
        contact_name = st.text_input(
            t(L, "contact_person"), placeholder=t(L, "contact_ph"),
        )
        client_email = st.text_input(
            t(L, "client_email"), placeholder=t(L, "email_ph"),
        )
        service_label = st.text_input(t(L, "service_label"), placeholder=t(L, "service_ph"))
        end_date = st.date_input(
            t(L, "end_date"),
            value=_today() + timedelta(days=30),
            min_value=_today() - timedelta(days=365),
        )
        total_ms = 10
        if mode == MODE_MILESTONE:
            st.markdown(f"**{t(L, 'milestone_hdr')}**")
            total_ms = st.number_input(
                t(L, "total_ms"), 1, 999, 10, 1, help=t(L, "total_ms_help"),
            )
        submitted = st.form_submit_button(t(L, "add_btn"), use_container_width=True)

    if submitted:
        if not client_name.strip():
            st.error(t(L, "err_name"))
        else:
            add_client(
                L, mode, client_name, contact_name, client_email,
                service_label, end_date, total_ms,
            )
            st.success(t(L, "added", name=client_name.strip()))
            st.rerun()


def render_manage_panel(L: str) -> None:
    if not st.session_state.clients:
        st.caption(t(L, "no_trackers"))
        return
    for c in st.session_state.clients:
        c1, c2 = st.columns([3, 1])
        with c1:
            d = days_remaining(c["end_date"])
            st.caption(f"**{c['client_name']}** · {days_display(d, L)}")
        with c2:
            if st.button("×", key=f"del_{c['id']}", help=t(L, "del")):
                delete_client(c["id"])
                st.rerun()
        if st.checkbox(
            f"✎ {t(L, 'edit_client')} — {c['client_name']}",
            key=f"edit_open_{c['id']}",
        ):
            st.markdown('<div class="cin-sidebar-edit">', unsafe_allow_html=True)
            ec_name = st.text_input(
                t(L, "client_name"),
                value=c["client_name"],
                key=f"edit_name_{c['id']}",
            )
            ec_service = st.text_input(
                t(L, "service_label"),
                value=c.get("service_label", ""),
                key=f"edit_service_{c['id']}",
            )
            ec_contact = st.text_input(
                t(L, "contact_person"),
                value=c.get("contact_name", ""),
                key=f"edit_contact_{c['id']}",
            )
            ec_email = st.text_input(
                t(L, "client_email"),
                value=c.get("client_email", ""),
                key=f"edit_email_{c['id']}",
            )
            ec_end = st.date_input(
                t(L, "end_date"),
                value=c["end_date"],
                min_value=_today() - timedelta(days=365 * 3),
                key=f"edit_end_{c['id']}",
            )
            total_ms = None
            if c["mode"] == MODE_MILESTONE:
                done = milestone_done_count(c)
                st.caption(t(L, "progress", done=done, total=c.get("total_milestones", 0)))
                total_ms = st.number_input(
                    t(L, "total_ms"),
                    min_value=max(1, done),
                    max_value=999,
                    value=int(c.get("total_milestones") or 1),
                    step=1,
                    help=t(L, "total_ms_help"),
                    key=f"edit_total_ms_{c['id']}",
                )
            if st.button(
                t(L, "save_edit"),
                key=f"save_{c['id']}",
                use_container_width=True,
            ):
                err = update_client(
                    L,
                    c["id"],
                    ec_name,
                    ec_contact,
                    ec_email,
                    ec_service,
                    ec_end,
                    total_ms,
                )
                if err:
                    st.error(err)
                else:
                    st.success(t(L, "saved_edit", name=ec_name.strip()))
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)


@st.dialog("CheckItNow", width="large")
def add_tracker_dialog() -> None:
    L = current_lang()
    render_dialog_header(L, "sidebar_add", "sidebar_add_cap")
    render_add_tracker_form(L)
    render_dialog_footer(L, "add")


@st.dialog("CheckItNow", width="large")
def manage_clients_dialog() -> None:
    L = current_lang()
    render_dialog_header(L, "manage")
    render_manage_panel(L)
    render_dialog_footer(L, "manage")


def render_dialog_header(L: str, title_key: str, caption_key: str | None = None) -> None:
    title_col, close_col = st.columns([6, 1])
    with title_col:
        st.markdown(f"### {t(L, title_key)}")
        if caption_key:
            st.caption(t(L, caption_key))
    with close_col:
        if st.button(
            "✕",
            key=f"dlg_close_{title_key}",
            help=t(L, "close_btn"),
            use_container_width=True,
        ):
            st.rerun()


def render_dialog_footer(L: str, dialog_id: str) -> None:
    st.caption(t(L, "dialog_dismiss_hint"))
    if st.button(
        t(L, "close_btn"),
        key=f"dlg_close_footer_{dialog_id}",
        use_container_width=True,
    ):
        st.rerun()


def render_hero(L: str) -> None:
    today_str = _today().strftime("%Y-%m-%d")
    st.markdown('<div class="cin-hero-top">', unsafe_allow_html=True)
    brand_col, lang_col = st.columns([6.4, 1])
    with brand_col:
        st.markdown(
            f"""
            <div class="cin-hero-brand">
                <div class="cin-hero-icon">🔔</div>
                <div>
                    <div class="cin-hero-tag">{t(L, "tagline")}</div>
                    <h1 class="cin-hero-title">{t(L, "title")}</h1>
                    <p class="cin-hero-sub">{t(L, "subtitle")}</p>
                    <p class="cin-hero-today">{t(L, "today")}: {today_str}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with lang_col:
        st.markdown('<span class="cin-lang-wrap"></span>', unsafe_allow_html=True)
        render_lang_picker()

    st.markdown('<div class="cin-hero-toolbar">', unsafe_allow_html=True)
    st.markdown('<span class="cin-hero-actions"></span>', unsafe_allow_html=True)
    act_add, act_manage, _ = st.columns([1.05, 0.95, 5], gap="small")
    with act_add:
        if st.button(
            f"+ {t(L, 'sidebar_add')}",
            key="hero_add_btn",
            type="primary",
        ):
            add_tracker_dialog()
    with act_manage:
        if st.button(
            t(L, "manage"),
            key="hero_manage_btn",
        ):
            manage_clients_dialog()
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_kpi_row(L: str, clients: list[dict]) -> None:
    urgent = sum(1 for c in clients if 0 <= days_remaining(c["end_date"]) <= URGENT_DAYS)
    critical = sum(1 for c in clients if days_remaining(c["end_date"]) < 0)
    ms_logged = sum(milestone_done_count(c) for c in clients if c["mode"] == MODE_MILESTONE)
    ms_total = sum(
        int(c.get("total_milestones") or 0)
        for c in clients
        if c["mode"] == MODE_MILESTONE
    )
    specs = [
        ("accent", "all", "cin-section-board", t(L, "kpi_active"), str(len(clients)), ""),
        (
            "warn", "urgent", "cin-section-priority",
            t(L, "kpi_urgent"), str(urgent), t(L, "kpi_sub_urgent", n=URGENT_DAYS),
        ),
        (
            "ok", "milestone", "cin-section-board",
            t(L, "kpi_milestone"), str(ms_logged),
            t(L, "kpi_ms_logged", done=ms_logged, total=ms_total),
        ),
        ("danger", "expired", "cin-section-board", t(L, "kpi_expired"), str(critical), ""),
    ]
    hint = t(L, "kpi_click_hint")
    active_filter = st.session_state.board_filter
    cols = board_columns(4)
    for idx, (col, (css, nav_filter, scroll_id, lbl, val, sub)) in enumerate(
        zip(cols, specs)
    ):
        with col:
            if idx == 0:
                st.markdown(
                    '<span class="cin-kpi-row-marker"></span>',
                    unsafe_allow_html=True,
                )
            tail = sub if sub else hint
            active_cls = " cin-kpi-card--active" if active_filter == nav_filter else ""
            st.markdown('<span class="cin-kpi-wrap"></span>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="cin-kpi-card cin-kpi-card--{css}{active_cls}">'
                f'<span class="cin-kpi-lbl">{_html_esc(lbl)}</span>'
                f'<span class="cin-kpi-val">{_html_esc(val)}</span>'
                f'<span class="cin-kpi-sub">{_html_esc(tail)}</span>'
                f"</div>",
                unsafe_allow_html=True,
            )
            st.button(
                "\u200b",
                key=f"kpi_nav_{nav_filter}",
                on_click=kpi_navigate,
                args=(nav_filter, scroll_id),
                use_container_width=True,
                type="secondary",
                help=lbl,
            )


def render_priority_queue(L: str, clients: list[dict]) -> None:
    urgent_list = sorted(
        [c for c in clients if days_remaining(c["end_date"]) <= URGENT_DAYS],
        key=lambda c: days_remaining(c["end_date"]),
    )
    st.markdown(
        '<div id="cin-section-priority" class="cin-section-anchor"></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="cin-panel"><h3>⚡ {t(L, "section_priority")}</h3></div>',
        unsafe_allow_html=True,
    )
    if not urgent_list:
        st.caption(t(L, "priority_empty"))
    else:
        for c in urgent_list[:5]:
            days = days_remaining(c["end_date"])
            badge = status_badge_html(days, L)
            svc = c.get("service_label", "") or "—"
            st.markdown(
                '<div class="cin-priority-row">'
                f'<div class="cin-priority-meta">'
                f'<span class="cin-priority-name">{_html_esc(c["client_name"])}</span>'
                f'<span class="cin-priority-svc">{_html_esc(svc)}</span>'
                f'</div>{badge}</div>',
                unsafe_allow_html=True,
            )


def render_tracker_card(client: dict, L: str) -> None:
    days = days_remaining(client["end_date"])
    _, color = urgency_class(days)
    is_ms = client["mode"] == MODE_MILESTONE
    badge_cls = "milestone" if is_ms else "expiry"
    badge_txt = _html_esc(t(L, "badge_milestone" if is_ms else "badge_single"))
    next_lbl_key, next_display, _ = next_date_info(client, L)
    status_pill = status_badge_html(days, L)
    service = _html_esc(client.get("service_label", "") or "—")
    name = _html_esc(client["client_name"])
    end_str = _html_esc(format_end_date(client["end_date"]))
    next_lbl = _html_esc(t(L, next_lbl_key))
    next_val = _html_esc(next_display)
    col_client = _html_esc(t(L, "col_client"))
    svc_lbl = _html_esc(t(L, "service_label"))
    end_lbl = _html_esc(t(L, "card_end"))
    days_txt = _html_esc(days_display(days, L))

    ms_progress_txt = ""
    prog_html = '<div class="cin-prog-wrap" aria-hidden="true" style="min-height:34px;"></div>'
    if is_ms:
        ensure_milestone_dates(client)
        done = milestone_done_count(client)
        total = max(1, int(client.get("total_milestones") or 1))
        ms_progress_txt = _html_esc(t(L, "progress", done=done, total=total))
        pct = int(milestone_progress(client) * 100)
        prog_html = (
            f'<div class="cin-prog-wrap"><div class="cin-prog-bar">'
            f'<div class="cin-prog-fill" style="width:{pct}%;"></div></div>'
            f'<div class="cin-prog-meta"><div class="cin-prog-txt">{ms_progress_txt}</div>'
            f'<div class="cin-prog-pct">{pct}%</div></div></div>'
        )

    st.markdown(
        f"""
        <div class="cin-card-unit">
        <div class="cin-tracker-wrap">
            <div class="cin-card">
                <div class="cin-card-head">
                    <span class="cin-badge {badge_cls}">{badge_txt}</span>
                    {status_pill}
                </div>
                <div class="cin-field">
                    <span class="cin-field-lbl">{col_client}</span>
                    <span class="cin-field-val">{name}</span>
                </div>
                <div class="cin-field">
                    <span class="cin-field-lbl">{svc_lbl}</span>
                    <span class="cin-field-val cin-field-val--muted">{service}</span>
                </div>
                <div class="cin-card-stats">
                    <div class="cin-count" style="color:{color};">{days_txt}</div>
                </div>
                <div class="cin-field">
                    <span class="cin-field-lbl">{end_lbl}</span>
                    <span class="cin-field-val cin-field-val--muted">{end_str}</span>
                </div>
                <div class="cin-field cin-field--highlight">
                    <span class="cin-field-lbl">{next_lbl}</span>
                    <span class="cin-field-val">{next_val}</span>
                </div>
                {prog_html}
            </div>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        t(L, "btn_draft"),
        key=f"draft_{client['id']}",
        use_container_width=True,
    ):
        st.session_state.compose_client_id = client["id"]
        st.rerun()


def main() -> None:
    init_state()
    if apply_lang_query_param():
        st.rerun()
    if apply_kpi_query_params():
        st.rerun()
    L = current_lang()

    st.set_page_config(
        page_title=t(L, "page_title"),
        page_icon="🔔",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    inject_styles()
    _cleanup_legacy_lang_picker()

    render_demo_banner(L)
    render_hero(L)
    render_product_notice(L)

    clients = st.session_state.clients
    if not clients:
        st.info(t(L, "empty_info"))
        return

    render_kpi_row(L, clients)

    board_left, board_right = st.columns([1.55, 1], gap="large")

    with board_left:
        render_priority_queue(L, clients)

        st.markdown(
            '<div id="cin-section-board" class="cin-section-anchor"></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="cin-section-title">{t(L, "section_board")}</div>',
            unsafe_allow_html=True,
        )

        shown = sorted(
            filter_clients(clients, st.session_state.board_filter),
            key=lambda c: days_remaining(c["end_date"]),
        )
        if not shown:
            st.caption("—")
        else:
            for i in range(0, len(shown), 2):
                row = board_columns(2)
                for j, col in enumerate(row):
                    if i + j < len(shown):
                        with col:
                            render_tracker_card(shown[i + j], L)

        with st.expander(t(L, "expander_table")):
            st.dataframe(
                pd.DataFrame([client_summary_row(c, L) for c in clients]),
                use_container_width=True,
                hide_index=True,
            )

    with board_right:
        st.markdown('<span class="cin-compose-anchor"></span>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="cin-compose-header">'
            f'<h3>{t(L, "section_compose")}</h3>'
            f'<p>{t(L, "compose_cap")}</p></div>',
            unsafe_allow_html=True,
        )

        id_to_client = {c["id"]: c for c in clients}
        names = [c["client_name"] for c in clients]
        default_idx = 0
        if st.session_state.compose_client_id in id_to_client:
            cid = st.session_state.compose_client_id
            default_idx = next(
                i for i, c in enumerate(clients) if c["id"] == cid
            )

        picked_name = st.selectbox(
            t(L, "select_client"),
            names,
            index=default_idx,
            label_visibility="collapsed",
        )
        selected = next(c for c in clients if c["client_name"] == picked_name)
        st.session_state.compose_client_id = selected["id"]

        days = days_remaining(selected["end_date"])
        next_lbl_key, next_display, _ = next_date_info(selected, L)
        st.markdown(
            f'<div class="cin-compose-meta">'
            f'{status_badge_html(days, L)}'
            f'<span class="cin-compose-days">{days_display(days, L)}</span></div>'
            f'<div class="cin-field cin-field--highlight cin-compose-next">'
            f'<span class="cin-field-lbl">{t(L, next_lbl_key)}</span>'
            f'<span class="cin-field-val">{next_display}</span></div>',
            unsafe_allow_html=True,
        )

        render_progress_tracker(selected, L)

        st.radio(
            t(L, "channel_lbl"),
            list(ALL_CHANNELS),
            format_func=lambda c: channel_label(L, c),
            horizontal=True,
            key="compose_channel",
        )
        st.radio(
            t(L, "payment_lbl"),
            [PAYMENT_ROUTINE, PAYMENT_COLLECTION],
            format_func=lambda p: (
                t(L, "payment_routine")
                if p == PAYMENT_ROUTINE
                else t(L, "payment_collection")
            ),
            horizontal=True,
            key="compose_payment",
        )

        channel = st.session_state.compose_channel
        payment = st.session_state.compose_payment
        ms_sig = ""
        if selected["mode"] == MODE_MILESTONE:
            dlist = ensure_milestone_dates(selected)
            ms_sig = f"_{milestone_done_count(selected)}_{'-'.join(x or '-' for x in dlist)}"
        message = build_reminder_message(selected, L, channel, payment)
        msg_key = f"msg_{selected['id']}_{L}_{channel}_{payment}{ms_sig}"
        st.text_area(
            t(L, "reminder_area"),
            value=message,
            height=260,
            key=msg_key,
            label_visibility="collapsed",
        )
        render_compose_actions(L, message, selected, msg_key)
        render_lead_cta(L)

    scroll_target = st.session_state.get("cin_scroll_target")
    if scroll_target:
        scroll_to_anchor(scroll_target)
        st.session_state.cin_scroll_target = None

    render_footer_cta(L)


if __name__ == "__main__":
    main()
