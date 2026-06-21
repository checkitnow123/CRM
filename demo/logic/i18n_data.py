# Extracted from ../app.py

LANG = {
    "en": {
        "page_title": "CheckItNow",
        "title": "CheckItNow",
        "tagline": "Client & service CRM",
        "subtitle": "Track contracts, sessions, and renewals.",
        "today": "Today",
        "mode_single": "Single expiry",
        "mode_milestone": "Milestone plan",
        "badge_single": "EXPIRY",
        "badge_milestone": "MILESTONE",
        "sidebar_add": "New client",
        "sidebar_add_cap": "Add a contract end date or a multi-session plan (coaching, bookings, maintenance, etc.).",
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
        "progress_tracker_cap": "Check each session in order — today's date is saved automatically.",
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
        "add_btn": "Add",
        "err_name": "Client / company name is required.",
        "err_total_ms": "Total milestones cannot be less than already completed ({done}).",
        "added": "Added {name}.",
        "manage": "Manage clients",
        "no_trackers": "No clients yet.",
        "del": "Remove",
        "sidebar_footer": "Demo — data resets on full browser refresh.",
        "default_service": "Service plan",
        "empty_info": "Click **New client** above to get started.",
        "kpi_active": "Active",
        "kpi_urgent": "Action needed",
        "kpi_milestone": "Session progress",
        "kpi_ms_logged": "{done} of {total} logged",
        "kpi_expired": "Overdue",
        "kpi_sub_urgent": "≤ {n} days",
        "section_priority": "Priority",
        "priority_empty": "Nothing urgent right now.",
        "section_board": "Client status",
        "filter_all": "All",
        "filter_urgent": "Urgent",
        "filter_expired": "Overdue",
        "filter_milestone": "Milestones",
        "kpi_click_hint": "Click to filter",
        "btn_draft": "Write reminder",
        "days_left": "{n}d",
        "days_over": "+{n}d overdue",
        "card_end": "Ends",
        "next_service": "Next estimated slot",
        "next_payment": "Program end",
        "all_sessions_done": "All milestones completed",
        "progress": "{done} / {total} milestones",
        "section_compose": "Write reminder",
        "compose_cap": "Choose client, channel, and message type.",
        "select_client": "Client",
        "channel_lbl": "Channel",
        "channel_sms": "Text message",
        "channel_email": "Email",
        "payment_lbl": "Message type",
        "payment_routine": "Pre-paid / routine",
        "payment_collection": "Payment due",
        "reminder_area": "Message draft",
        "copy_btn": "Copy to clipboard",
        "email_open_btn": "Open in email",
        "email_no_address": "Add a client email in **Manage clients** to send mail.",
        "copy_one": "Copy — {name}",
        "copy_done": "Copied",
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
        "status_expired": "Overdue {n}d",
        "status_critical": "{n}d left · critical",
        "status_urgent": "{n}d left · act soon",
        "status_ok": "{n}d left",
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
    },
    "zh": {
        "page_title": "CheckItNow 到期提醒",
        "title": "CheckItNow",
        "tagline": "個人與服務業 CRM",
        "subtitle": "管理合約、課程與續約提醒。",
        "today": "今日",
        "mode_single": "單次到期",
        "mode_milestone": "里程碑方案",
        "badge_single": "到期",
        "badge_milestone": "里程碑",
        "sidebar_add": "新增客戶",
        "sidebar_add_cap": "加入合約到期日，或多次服務／課堂／預約方案。",
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
        "add_btn": "加入",
        "err_name": "請填寫客戶／公司名稱。",
        "err_total_ms": "總里程碑數不可少於已完成數（{done}）。",
        "added": "已新增 {name}。",
        "manage": "管理客戶",
        "no_trackers": "暫無客戶。",
        "del": "移除",
        "sidebar_footer": "示範模式 — 完整重新整理瀏覽器後資料會重置。",
        "default_service": "服務方案",
        "empty_info": "按上方「新增客戶」開始。",
        "kpi_active": "進行中",
        "kpi_urgent": "須跟進",
        "kpi_milestone": "服務進度",
        "kpi_ms_logged": "已記錄 {done}/{total} 次",
        "kpi_expired": "已逾期",
        "kpi_sub_urgent": "≤ {n} 天",
        "section_priority": "優先事項",
        "priority_empty": "暫無須優先處理的事項。",
        "section_board": "客戶狀態",
        "filter_all": "全部",
        "filter_urgent": "緊急",
        "filter_expired": "逾期",
        "filter_milestone": "里程碑",
        "kpi_click_hint": "點擊篩選",
        "btn_draft": "撰寫提醒",
        "days_left": "剩 {n} 天",
        "days_over": "逾期 {n} 天",
        "card_end": "結束",
        "next_service": "下次服務／收款日",
        "next_payment": "合約結束日",
        "all_sessions_done": "所有里程碑已完成",
        "progress": "{done} / {total} 里程碑",
        "section_compose": "撰寫提醒",
        "compose_cap": "選擇客戶、渠道與訊息類型，然後複製或發送。",
        "select_client": "客戶",
        "channel_lbl": "渠道",
        "channel_sms": "短訊",
        "channel_email": "電子郵件",
        "payment_lbl": "訊息類型",
        "payment_routine": "已預付／例行",
        "payment_collection": "須收款",
        "reminder_area": "訊息草稿",
        "copy_btn": "複製到剪貼簿",
        "email_open_btn": "以 Email 開啟",
        "email_no_address": "請在「管理客戶」填寫客戶 Email。",
        "copy_one": "複製 — {name}",
        "copy_done": "已複製",
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
        "tagline": "个人与服务 CRM",
        "subtitle": "管理合约、课程与续约提醒。",
        "today": "今天",
        "mode_single": "单次到期",
        "mode_milestone": "里程碑方案",
        "badge_single": "到期",
        "badge_milestone": "里程碑",
        "sidebar_add": "新增客户",
        "sidebar_add_cap": "加入合约到期日，或多次服务／课堂／预约方案。",
        "tracker_mode": "类型",
        "client_name": "客户/公司名称",
        "client_ph": "例：ABC 公司、学员 Mary",
        "contact_person": "联系人",
        "contact_ph": "微信昵称或姓名",
        "client_email": "客户邮箱",
        "email_ph": "contact@client.com",
        "edit_client": "编辑资料",
        "save_edit": "保存变更",
        "close_btn": "关闭",
        "saved_edit": "已保存 {name}。",
        "service_label": "服务/方案名称",
        "service_ph": "例：10 节瑜伽、英语家教",
        "end_date": "方案结束日",
        "total_ms": "里程碑总数",
        "done_ms": "已完成",
        "progress_tracker": "进度追踪",
        "progress_tracker_cap": "请按顺序勾选每次服务，系统自动记录日期。",
        "progress": "{done} / {total} 里程碑",
        "ms_locked": "请先完成上一项",
        "ms_undo": "撤销上一步",
        "add_btn": "加入",
        "added": "已新增 {name}。",
        "manage": "管理客户",
        "no_trackers": "暂无客户。",
        "del": "移除",
        "empty_info": "点击上方「新增客户」开始。",
        "kpi_active": "进行中",
        "kpi_urgent": "须跟进",
        "kpi_milestone": "服务进度",
        "kpi_ms_logged": "已记录 {done}/{total} 次",
        "kpi_expired": "已逾期",
        "kpi_sub_urgent": "≤ {n} 天",
        "kpi_click_hint": "点击筛选",
        "section_priority": "优先事项",
        "priority_empty": "暂无须优先处理的事项。",
        "section_board": "客户状态",
        "section_compose": "撰写提醒",
        "compose_cap": "选择客户、渠道与消息类型，然后复制或发送。",
        "select_client": "客户",
        "channel_lbl": "渠道",
        "channel_sms": "短信",
        "channel_email": "邮箱",
        "payment_lbl": "消息类型",
        "payment_routine": "已预付/例行",
        "payment_collection": "须收款",
        "copy_btn": "复制到剪贴板",
        "email_open_btn": "以邮箱打开",
        "email_no_address": "请在「管理客户」填写客户邮箱。",
        "copy_done": "已复制",
        "copy_fallback": "或选中文字后按 Ctrl+C",
        "card_end": "到期日",
        "col_client": "客户",
        "detail_ms": "{done}/{total} 里程碑",
        "next_visit": "下次预计时段",
        "next_service": "下次预计时段",
        "all_sessions_done": "所有里程碑已完成",
        "history_header": "里程碑记录：",
        "history_none": "暂无记录。",
        "note_prepaid": "如已预付，无需额外操作。",
        "note_collect": "请尽早确认付款。",
        "note_urgent": "请今日内回复。",
        "badge_expired": "🔴 逾期",
        "badge_urgent": "🔴 紧急",
        "badge_warning": "🟠 注意",
        "badge_healthy": "🟢 正常",
        "msg_default_contact": "您好",
        "msg_default_label": "您的服务方案",
        "dialog_dismiss_hint": "提示：点击窗口外或按 Esc 可关闭。",
        "milestone_hdr": "服务里程碑",
        "total_ms_help": "任意数字 — 课时、回访、教练场次等。",
        "progress_empty": "此客户尚未设置里程碑次数。",
        "ms_service": "第 {n} 次服务/里程碑",
        "ms_done_row": "✅ {label} - 完成于 {date}",
        "history_line": "• {label} — {date}",
        "history_latest": "我们已于 {date} 顺利完成您的{label}（{program}）。",
        "err_name": "请填写客户/公司名称。",
        "err_total_ms": "总里程碑数不可少于已完成数（{done}）。",
        "sidebar_footer": "演示模式 — 完整刷新浏览器后数据会重置。",
        "default_service": "服务方案",
        "filter_all": "全部",
        "filter_urgent": "紧急",
        "filter_expired": "逾期",
        "filter_milestone": "里程碑",
        "btn_draft": "撰写提醒",
        "days_left": "剩 {n} 天",
        "days_over": "逾期 {n} 天",
        "next_payment": "合约结束日",
        "reminder_area": "消息草稿",
        "copy_one": "复制 — {name}",
        "expander_table": "表格视图",
        "col_mode": "类型",
        "col_detail": "详情",
        "col_end": "结束日",
        "col_contact": "联系人",
        "col_email": "邮箱",
        "col_next": "下次日期",
        "col_status": "状态",
        "detail_single": "单次到期",
        "status_expired": "逾期 {n} 天",
        "status_critical": "剩 {n} 天 · 紧急",
        "status_urgent": "剩 {n} 天 · 请处理",
        "status_ok": "剩 {n} 天",
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
