/** CheckItNow Demo — frontend */

if (document.documentElement.classList.contains("mobile-glance")) {
  document.addEventListener("gesturestart", (e) => e.preventDefault(), { passive: false });
}

const NAV_FALLBACK = {
  zh: { dashboard: "總覽", clients: "客戶", milestones: "里程碑" },
  zh_cn: { dashboard: "总览", clients: "客户", milestones: "里程碑" },
  en: { dashboard: "Overview", clients: "Clients", milestones: "Milestones" },
};

const EXTRA_FALLBACK = {
  zh: {
    filter_showing: "目前篩選",
    filter_clear: "清除篩選",
    priority_all_clear: "暫無須優先處理的事項",
    fab_compose: "撰寫提醒",
    compose_close: "關閉",
    last_reminder_none: "尚未發送提醒",
    banner_action: "查看優先事項",
    alert_settings_hint: "提醒設定：{urgent} / {critical} / {warning} 日",
    open_compose: "撰寫提醒",
    open_compose_short: "提醒",
    btn_renew_short: "續約",
    btn_dismiss_short: "稍後",
    schedule_title: "排期（課堂／預約／服務）",
    schedule_first: "第一次日期",
    schedule_every_1w: "每週 × 10 堂",
    schedule_every_2w: "每 2 週 × 8 次",
    schedule_every_3m: "每 3 個月 × 4 次",
    schedule_every_6m: "每 6 個月 × 2 次",
    schedule_add_row: "加一次",
    schedule_visit_n: "第 {n} 次",
    schedule_end_hint: "方案結束日會自動設為最後一次排期。",
    schedule_help: "教練排課、學生 booking、保養合約都適用。按快捷鍵自動填好，再點每行日曆改日期；或按 ＋ 加更多次。",
    err_schedule: "請至少設定一個排期日期。",
    err_schedule_incomplete: "請填寫每一行排期日期。",
    schedule_edit_btn: "查看排期",
    schedule_edit_btn_short: "排期",
    schedule_edit_title: "查看／修改排期",
    schedule_edit_help: "已完成的次數不可修改日期；未完成的可修改，或按 ＋ 新增更多次。",
    schedule_done_row: "已完成",
    schedule_saved: "排期已更新。",
    err_schedule_done: "不可刪除已完成的次數。",
    save_schedule: "儲存排期",
    edit_client_btn: "編輯",
    edit_client_title: "修改客戶資料",
    save_client: "儲存客戶",
    client_saved: "客戶資料已更新。",
    milestone_edit_hint: "里程碑客戶的日期請使用「查看排期」修改。",
    client_group: "群組",
    client_numbers: "客戶號碼",
    client_numbers_hint: "多個號碼用逗號分隔，例如：123, 456",
    clients_search: "搜尋客戶／號碼",
    clients_group_all: "全部群組",
    clients_group_none: "未分組",
    clients_pick: "選客戶",
    clients_pick_placeholder: "快速選客戶…",
    clients_detail_title: "客戶詳情",
    clients_detail_empty: "請從列表選取客戶，或在上方搜尋／快速選客戶。",
    clients_detail_hint: "點選客戶列，右側會滑出詳情；點選空白處可關閉",
    clients_filtered: "顯示 {n} / {total}",
    col_group: "群組",
    col_client_no: "客戶號碼",
    status_closed: "已結束",
    btn_close_client: "標記 Closed",
    btn_close_client_short: "關閉",
    btn_reopen_client: "重新開啟",
    close_client_confirm: "確定將此客戶標記為 Closed？到期後不續約的客戶將從 Dashboard 隱藏，但仍可在 Clients 中找到。",
    clients_account_all: "全部狀態",
    clients_account_active: "進行中",
    clients_account_closed: "Closed",
    export_excel_btn: "匯出 Excel",
    export_excel_done: "已匯出客戶清單",
    export_excel_cancelled: "已取消匯出",
    about_title: "關於",
    about_version: "版本 {version}",
    about_tagline: "{tagline}",
    notify_settings_title: "桌面通知",
    notify_settings_desc: "App 開啟時，Windows 會提示即將到期或已逾期的客戶（約每小時一次，有變化才通知）。",
    notify_settings_enable: "啟用到期桌面通知",
    sample_settings_title: "示範資料",
    sample_settings_desc: "首次啟動且資料庫為空時，可自動載入示範客戶。",
    sample_seed_enable: "空白時自動載入示範資料",
    sample_load_btn: "載入示範資料",
    sample_clear_btn: "清空所有客戶",
    sample_load_confirm: "載入示範資料？現有客戶會被取代。",
    sample_clear_confirm: "確定清空所有客戶？此操作無法復原。",
    sample_loaded: "已載入 {n} 個示範客戶。",
    sample_cleared: "已清空所有客戶。",
    sample_client_count: "目前 {n} 個客戶",
    activity_title: "操作紀錄",
    activity_empty: "尚無紀錄。",
    collab_login_title: "登入 CheckItNow",
    collab_login_desc: "Dropbox 共用資料庫測試：編輯者一次只得一人；監看模式不佔鎖，可長開。",
    collab_login_user: "使用者",
    collab_login_password: "密碼",
    collab_role_editor: "編輯（可改資料）",
    collab_role_viewer: "監看（只讀，不佔鎖）",
    collab_login_btn: "登入",
    collab_login_demo_hint: "示範帳號：admin/admin、user/user",
    collab_login_invalid: "帳號或密碼錯誤",
    collab_login_blocked: "「{user}」正在編輯（{machine}），已以監看模式登入。",
    collab_banner_viewer: "監看模式（只讀）— 不佔編輯鎖，可長開",
    collab_banner_readonly: "只讀 — 「{user}」正在編輯（{machine}），請聯絡關閉或稍後再試",
    collab_banner_editor: "編輯模式 — 你正在獨佔寫入",
    collab_promote_btn: "切換為編輯",
    collab_demote_btn: "切換為監看",
    collab_demote_ok: "已放開編輯鎖，現為監看模式",
    collab_promote_ok: "已取得編輯權",
    collab_promote_fail: "仍有人編輯中，無法切換",
    collab_logout_btn: "登出",
    collab_readonly_toast: "目前為只讀，無法儲存",
    collab_settings_title: "Dropbox 協作（測試）",
    collab_settings_desc: "啟用後需登入。編輯者獨佔寫入；監看者不佔鎖，適合 Admin 長開。",
    collab_settings_enable: "啟用登入與編輯鎖",
    collab_lock_status: "編輯中：{user}（{machine}）",
    collab_lock_free: "目前無人編輯，可登入為編輯者",
    collab_force_unlock_btn: "強制解除鎖定",
    collab_force_unlock_ok: "已解除編輯鎖",
    collab_test_hint: "測試：開第二個瀏覽器視窗（或無痕），一個選監看、一個選編輯。",
    collab_open_test_window: "開啟測試視窗",
    collab_banner_reclaimable: "上次未正常登出，編輯鎖仍留在本機 — 可按「切換為編輯」",
    collab_password_title: "帳號密碼",
    collab_password_desc: "可隨時更改自己的密碼，毋須首次登入強制修改。",
    password_current: "目前密碼",
    password_new: "新密碼",
    password_confirm: "確認新密碼",
    password_change_btn: "更改密碼",
    password_change_ok: "密碼已更新。",
    password_mismatch: "兩次輸入的新密碼不一致。",
    password_too_short: "密碼至少需要 4 個字元。",
    password_admin_reset_title: "Admin 重設使用者密碼",
    password_admin_reset_desc: "Admin 可重設其他帳號（例如 user）。",
    password_admin_confirm: "Admin 密碼（確認）",
    password_target_user: "使用者",
    password_reset_btn: "重設密碼",
    password_reset_ok: "已重設 {user} 的密碼。",
    password_not_admin: "只有 admin 可以重設其他使用者。",
    data_path_settings_title: "Dropbox 資料夾",
    data_path_settings_desc: "EXE 可放在桌面；請選擇 Dropbox 內共用的 data 資料夾，無需 mklink。變更後請重新啟動應用程式。",
    data_path_browse_btn: "選擇資料夾…",
    data_path_default_btn: "使用預設（EXE 旁邊）",
    data_path_apply_btn: "套用路徑",
    data_path_status_effective: "目前使用：{path}",
    data_path_status_configured: "已設定（重新啟動後生效）：{path}",
    data_path_restart_hint: "資料路徑已儲存，請關閉並重新開啟 CheckItNow。",
    data_path_saved: "資料夾路徑已儲存",
    data_path_cancelled: "已取消選擇",
    data_path_default_confirm: "改回 EXE 旁邊的 data 資料夾？儲存後請重新啟動應用程式。",
    data_path_browser_hint: "請貼上 Dropbox 資料夾完整路徑，再按「套用路徑」。使用 EXE 版可直接選擇資料夾。",
    backup_restore_selected_btn: "還原所選備份",
    backup_pick_label: "選擇備份",
    backup_kind_daily: "每日",
    backup_kind_recent: "快照",
    backup_restore_selected_confirm: "還原 {at} 的備份（{name}）？目前資料會被覆蓋。",
    import_settings_title: "Excel 匯入",
    import_settings_desc: "可先在 Excel 填寫客戶資料再匯入。建議使用「下載範本」。",
    import_template_btn: "下載匯入範本",
    import_template_done: "已下載匯入範本",
    import_excel_btn: "選擇 Excel 匯入…",
    import_replace_label: "匯入前清空現有客戶（慎用）",
    import_excel_confirm_replace: "匯入前會清空所有客戶，確定？",
    import_excel_done: "已匯入 {n} 個客戶（略過 {skipped} 行）。",
    import_excel_none: "沒有可匯入的資料列。",
    import_excel_errors: "部分資料未能匯入，請檢查 Excel。",
  },
  zh_cn: {
    filter_showing: "当前筛选",
    filter_clear: "清除筛选",
    priority_all_clear: "暂无须优先处理的事项",
    fab_compose: "撰写提醒",
    compose_close: "关闭",
    open_compose: "撰写提醒",
    open_compose_short: "提醒",
    btn_renew_short: "续约",
    btn_dismiss_short: "稍后",
    last_reminder_none: "尚未发送提醒",
    banner_action: "查看优先事项",
    alert_settings_hint: "提醒设置：{urgent} / {critical} / {warning} 日",
    schedule_title: "排期（课堂／预约／服务）",
    schedule_first: "第一次日期",
    schedule_every_1w: "每周 × 10 堂",
    schedule_every_2w: "每 2 周 × 8 次",
    schedule_every_3m: "每 3 个月 × 4 次",
    schedule_every_6m: "每 6 个月 × 2 次",
    schedule_add_row: "加一次",
    schedule_visit_n: "第 {n} 次",
    schedule_end_hint: "方案结束日会自动设为最后一次排期。",
    schedule_help: "教练排课、学生 booking、保养合约都适用。点快捷按钮自动填好，再点每行日历改日期；或按 ＋ 加更多次。",
    err_schedule: "请至少设定一个排期日期。",
    err_schedule_incomplete: "请填写每一行排期日期。",
    schedule_edit_btn: "查看排期",
    schedule_edit_btn_short: "排期",
    schedule_edit_title: "查看／修改排期",
    schedule_edit_help: "已完成的次数不可改日期；未做的可以改，或按 ＋ 加更多次。",
    schedule_done_row: "已完成",
    schedule_saved: "排期已更新。",
    err_schedule_done: "不可删除已完成的次数。",
    save_schedule: "保存排期",
    edit_client_btn: "编辑",
    edit_client_title: "修改客户资料",
    save_client: "保存客户",
    client_saved: "客户资料已更新。",
    milestone_edit_hint: "Milestone 客户的日期请用“查看排期”修改。",
    client_group: "群组",
    client_numbers: "客户号码",
    client_numbers_hint: "多个号码用逗号分隔，例如：123, 456",
    clients_search: "搜索客户／号码",
    clients_group_all: "全部群组",
    clients_group_none: "未分组",
    clients_pick: "选客户",
    clients_pick_placeholder: "快速选客户…",
    clients_detail_title: "客户详情",
    clients_detail_empty: "点选列表中的客户，或在上方搜索／选择。",
    clients_detail_hint: "点选客户列，右边会滑出详情；点空白处收起",
    clients_filtered: "显示 {n} / {total}",
    col_group: "群组",
    col_client_no: "客户号码",
    status_closed: "已结束",
    btn_close_client: "标记 Closed",
    btn_close_client_short: "关闭",
    btn_reopen_client: "重新开启",
    close_client_confirm: "确定将此客户标记为 Closed？",
    clients_account_all: "全部状态",
    clients_account_active: "进行中",
    clients_account_closed: "Closed",
    export_excel_btn: "导出 Excel",
    export_excel_done: "已导出客户清单",
    export_excel_cancelled: "已取消导出",
    about_title: "关于",
    about_version: "版本 {version}",
    about_tagline: "{tagline}",
    notify_settings_title: "桌面通知",
    notify_settings_desc: "App 开启时，Windows 会提示即将到期或已逾期的客户（约每小时一次，有变化才通知）。",
    notify_settings_enable: "启用到期桌面通知",
    sample_settings_title: "示范数据",
    sample_settings_desc: "首次启动且数据库为空时，可自动载入示范客户。",
    sample_seed_enable: "空白时自动载入示范数据",
    sample_load_btn: "载入示范数据",
    sample_clear_btn: "清空所有客户",
    sample_load_confirm: "载入示范数据？现有客户会被取代。",
    sample_clear_confirm: "确定清空所有客户？此操作无法复原。",
    sample_loaded: "已载入 {n} 个示范客户。",
    sample_cleared: "已清空所有客户。",
    sample_client_count: "目前 {n} 个客户",
    activity_title: "操作记录",
    activity_empty: "尚无记录。",
  },
  en: {
    filter_showing: "Showing",
    filter_clear: "Clear filter",
    priority_all_clear: "Nothing urgent — you're all set.",
    fab_compose: "Write reminder",
    compose_close: "Close",
    open_compose: "Write reminder",
    open_compose_short: "Remind",
    btn_renew_short: "Renew",
    btn_dismiss_short: "Later",
    banner_action: "View priority",
    last_reminder_none: "No reminder sent yet",
    alert_settings_hint: "Alert tiers: {urgent} / {critical} / {warning} days",
    schedule_title: "Schedule (sessions / bookings / visits)",
    schedule_first: "First date",
    schedule_every_1w: "Weekly × 10",
    schedule_every_2w: "Every 2 wk × 8",
    schedule_every_3m: "Every 3 mo × 4",
    schedule_every_6m: "Every 6 mo × 2",
    schedule_add_row: "Add session",
    schedule_visit_n: "Session {n}",
    schedule_end_hint: "Program end is set to the last scheduled date automatically.",
    schedule_help: "Works for coaching, student bookings, maintenance, and more. Quick-fill, then edit each date; or press + to add sessions.",
    err_schedule: "Add at least one scheduled date.",
    err_schedule_incomplete: "Fill in every schedule row.",
    schedule_edit_btn: "Schedule",
    schedule_edit_btn_short: "Dates",
    schedule_edit_title: "View / edit schedule",
    schedule_edit_help: "Completed sessions are locked. Edit upcoming dates or press + to add more.",
    schedule_done_row: "Done",
    schedule_saved: "Schedule updated.",
    err_schedule_done: "Cannot remove sessions already completed.",
    save_schedule: "Save schedule",
    edit_client_btn: "Edit",
    edit_client_title: "Edit client",
    save_client: "Save client",
    client_saved: "Client updated.",
    milestone_edit_hint: "For milestone plans, edit dates with Schedule.",
    client_group: "Group",
    client_numbers: "Client numbers",
    client_numbers_hint: "Separate multiple numbers with commas, e.g. 123, 456",
    clients_search: "Search client / number",
    clients_group_all: "All groups",
    clients_group_none: "Ungrouped",
    clients_pick: "Pick client",
    clients_pick_placeholder: "Quick pick…",
    clients_detail_title: "Client details",
    clients_detail_empty: "Select a client from the list, or search / pick above.",
    clients_detail_hint: "Click a client row — details slide in from the right; click outside to close",
    clients_filtered: "Showing {n} / {total}",
    col_group: "Group",
    col_client_no: "Client no.",
    status_closed: "Closed",
    btn_close_client: "Mark closed",
    btn_close_client_short: "Close",
    btn_reopen_client: "Reopen",
    close_client_confirm: "Mark this client as closed?",
    clients_account_all: "All statuses",
    clients_account_active: "Active",
    clients_account_closed: "Closed",
    export_excel_btn: "Export Excel",
    export_excel_done: "Client list exported",
    export_excel_cancelled: "Export cancelled",
    about_title: "About",
    about_version: "Version {version}",
    about_tagline: "{tagline}",
    notify_settings_title: "Desktop notifications",
    notify_settings_desc: "While the app is open, Windows toasts alert you when clients are due or overdue (about once per hour when counts change).",
    notify_settings_enable: "Enable expiry desktop notifications",
    sample_settings_title: "Sample data",
    sample_settings_desc: "On first launch with an empty database, demo clients can be loaded automatically.",
    sample_seed_enable: "Auto-load sample data when empty",
    sample_load_btn: "Load sample data",
    sample_clear_btn: "Clear all clients",
    sample_load_confirm: "Load sample data? This replaces current clients.",
    sample_clear_confirm: "Clear all clients? This cannot be undone.",
    sample_loaded: "Loaded {n} sample client(s).",
    sample_cleared: "All clients cleared.",
    sample_client_count: "{n} client(s) in database",
    activity_title: "Activity log",
    activity_empty: "No activity yet.",
    collab_login_title: "Sign in to CheckItNow",
    collab_login_desc: "Dropbox shared DB test: one editor at a time. Viewer mode does not hold the lock.",
    collab_login_user: "Username",
    collab_login_password: "Password",
    collab_role_editor: "Editor (can change data)",
    collab_role_viewer: "Viewer (read-only, no lock)",
    collab_login_btn: "Sign in",
    collab_login_demo_hint: "Demo: admin/admin, user/user",
    collab_login_invalid: "Invalid username or password",
    collab_login_blocked: "{user} is editing ({machine}). Signed in as viewer.",
    collab_banner_viewer: "Viewer mode (read-only)",
    collab_banner_readonly: "Read-only — {user} is editing ({machine})",
    collab_banner_editor: "Editor mode — you hold the write lock",
    collab_promote_btn: "Switch to editor",
    collab_demote_btn: "Switch to viewer",
    collab_demote_ok: "Edit lock released — viewer mode",
    collab_promote_ok: "You now have edit access",
    collab_promote_fail: "Someone else is still editing",
    collab_logout_btn: "Sign out",
    collab_readonly_toast: "Read-only — cannot save",
    collab_settings_title: "Dropbox collaboration (test)",
    collab_settings_desc: "Editors hold the write lock; viewers do not.",
    collab_settings_enable: "Enable sign-in and edit lock",
    collab_lock_status: "Editing: {user} ({machine})",
    collab_lock_free: "No one is editing",
    collab_force_unlock_btn: "Force release lock",
    collab_force_unlock_ok: "Edit lock released",
    collab_test_hint: "Test: open a second window — one viewer, one editor.",
    collab_open_test_window: "Open test window",
    collab_banner_reclaimable: "Previous session did not sign out — click Switch to editor.",
    collab_password_title: "Account password",
    collab_password_desc: "Change your password anytime — no forced change on first sign-in.",
    password_current: "Current password",
    password_new: "New password",
    password_confirm: "Confirm new password",
    password_change_btn: "Change password",
    password_change_ok: "Password updated.",
    password_mismatch: "New passwords do not match.",
    password_too_short: "Password must be at least 4 characters.",
    password_admin_reset_title: "Admin: reset user password",
    password_admin_reset_desc: "Admin can reset another account (e.g. user).",
    password_admin_confirm: "Admin password (confirm)",
    password_target_user: "User",
    password_reset_btn: "Reset password",
    password_reset_ok: "Password reset for {user}.",
    password_not_admin: "Only admin can reset other users.",
    data_path_settings_title: "Dropbox data folder",
    data_path_settings_desc: "Keep the EXE on Desktop and point data to a shared Dropbox folder — no mklink needed. Restart after changing.",
    data_path_browse_btn: "Choose folder…",
    data_path_default_btn: "Use default (next to EXE)",
    data_path_apply_btn: "Apply path",
    data_path_status_effective: "In use: {path}",
    data_path_status_configured: "Saved (after restart): {path}",
    data_path_restart_hint: "Data folder saved — close and reopen CheckItNow.",
    data_path_saved: "Data folder saved",
    data_path_cancelled: "Selection cancelled",
    data_path_default_confirm: "Use the default data folder next to the EXE? Restart the app after saving.",
    data_path_browser_hint: "Paste the full Dropbox folder path, then click Apply path. The EXE version can open a folder picker.",
    backup_restore_selected_btn: "Restore selected backup",
    backup_pick_label: "Choose backup",
    backup_kind_daily: "Daily",
    backup_kind_recent: "Snapshot",
    backup_restore_selected_confirm: "Restore backup from {at} ({name})? Current data will be overwritten.",
    import_settings_title: "Excel import",
    import_settings_desc: "Prepare clients in Excel, then import. Use the template for bulk entry.",
    import_template_btn: "Download import template",
    import_template_done: "Import template saved",
    import_excel_btn: "Choose Excel to import…",
    import_replace_label: "Clear existing clients before import (use with care)",
    import_excel_confirm_replace: "This clears all clients before import. Continue?",
    import_excel_done: "Imported {n} client(s) ({skipped} row(s) skipped).",
    import_excel_none: "No importable rows found.",
    import_excel_errors: "Some rows could not be imported — check your Excel file.",
  },
};

const state = {
  lang: "en",
  filter: "all",
  view: "dashboard",
  strings: {},
  meta: null,
  branding: null,
  dashboard: null,
  channel: "sms",
  payment: "routine",
  composeClientId: null,
  renewClientId: null,
  editClientId: null,
  scheduleEditClientId: null,
  scheduleEditLocked: [],
  scheduleEditDoneRows: [],
  clientsSearch: "",
  clientsGroupFilter: "all",
  clientsAccountFilter: "all",
  clientsSelectedId: null,
  clientsRows: [],
  clientsGroups: [],
  clientsTotal: 0,
  session: null,
};

const SESSION_KEY = "cin_session_token";
let heartbeatTimer = null;
let viewerPollTimer = null;

const $ = (sel) => document.querySelector(sel);

async function api(path, opts = {}) {
  const token = sessionStorage.getItem(SESSION_KEY);
  const headers = { "Content-Type": "application/json", ...(opts.headers || {}) };
  if (token) headers["X-Session-Token"] = token;
  const res = await fetch(path, { ...opts, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    if (res.status === 403 && err.detail === "read_only") {
      if (state.session) {
        state.session.can_write = false;
        state.session.role = err.role || "viewer";
        state.session.lock_holder = err.lock_holder || state.session.lock_holder;
      }
      applyReadOnlyUi();
      throw new Error(t("collab_readonly_toast"));
    }
    throw new Error(err.detail || res.statusText);
  }
  return res.json();
}

function applyLoginLabels() {
  $("#login-title").textContent = t("collab_login_title");
  $("#login-desc").textContent = t("collab_login_desc");
  $("#lbl-login-user").textContent = t("collab_login_user");
  $("#lbl-login-password").textContent = t("collab_login_password");
  $("#lbl-role-editor").textContent = t("collab_role_editor");
  $("#lbl-role-viewer").textContent = t("collab_role_viewer");
  $("#login-demo-hint").textContent = t("collab_login_demo_hint");
  $("#btn-login-submit").textContent = t("collab_login_btn");
  $("#btn-collab-promote").textContent = t("collab_promote_btn");
  $("#btn-collab-demote").textContent = t("collab_demote_btn");
  $("#btn-collab-logout").textContent = t("collab_logout_btn");
}

function applyReadOnlyUi() {
  const ro = !!(
    state.session?.collab_enabled
    && state.session?.authenticated
    && !state.session?.can_write
  );
  document.body.classList.toggle("read-only-mode", ro);
  const addBtn = $("#btn-add");
  const manageBtn = $("#btn-manage");
  if (addBtn) addBtn.disabled = ro;
  if (manageBtn) manageBtn.disabled = ro;
  renderCollabBanner();
}

function renderCollabBanner() {
  const bar = $("#collab-banner");
  if (!bar) return;
  if (!state.session?.collab_enabled || !state.session?.authenticated) {
    bar.classList.add("hidden");
    return;
  }
  bar.classList.remove("hidden");
  const holder = state.session.lock_holder;
  const canWrite = !!state.session.can_write;
  let text;
  let variant = "viewer";
  if (canWrite) {
    text = t("collab_banner_editor");
    variant = "editor";
  } else if (state.session.lock_reclaimable || holder?.reclaimable) {
    text = t("collab_banner_reclaimable");
    variant = "viewer";
  } else if (state.session.role === "viewer" && !holder) {
    text = t("collab_banner_viewer");
  } else if (holder?.username) {
    text = t("collab_banner_readonly", {
      user: holder.username,
      machine: holder.machine || "—",
    });
    variant = "readonly";
  } else {
    text = t("collab_banner_viewer");
  }
  bar.className = `collab-banner collab-banner--${variant}`;
  $("#collab-banner-text").textContent = text;
  const promoteBtn = $("#btn-collab-promote");
  const demoteBtn = $("#btn-collab-demote");
  const canPromote = !canWrite && (!holder || holder.reclaimable || state.session.lock_reclaimable);
  promoteBtn.classList.toggle("hidden", !canPromote);
  promoteBtn.textContent = t("collab_promote_btn");
  demoteBtn.classList.toggle("hidden", !canWrite);
  demoteBtn.textContent = t("collab_demote_btn");
  $("#btn-collab-logout").classList.remove("hidden");
  $("#btn-collab-logout").textContent = t("collab_logout_btn");
  updateCollabPolling();
}

function updateCollabPolling() {
  if (state.session?.collab_enabled && state.session?.authenticated && state.session?.can_write) {
    stopViewerPoll();
    startHeartbeat();
  } else if (state.session?.collab_enabled && state.session?.authenticated) {
    stopHeartbeat();
    startViewerPoll();
  } else {
    stopHeartbeat();
    stopViewerPoll();
  }
}

function stopViewerPoll() {
  if (viewerPollTimer) {
    clearInterval(viewerPollTimer);
    viewerPollTimer = null;
  }
}

function startViewerPoll() {
  stopViewerPoll();
  if (!state.session?.collab_enabled || state.session?.can_write) return;
  viewerPollTimer = setInterval(async () => {
    try {
      await refreshSessionStatus();
    } catch {
      /* ignore */
    }
  }, 5000);
}

async function refreshSessionStatus() {
  state.session = await api("/api/session/status");
  applyReadOnlyUi();
  return state.session;
}

function stopHeartbeat() {
  if (heartbeatTimer) {
    clearInterval(heartbeatTimer);
    heartbeatTimer = null;
  }
}

function startHeartbeat() {
  stopHeartbeat();
  if (!state.session?.collab_enabled || !state.session?.can_write) return;
  const seconds = state.session.heartbeat_interval_seconds || 120;
  heartbeatTimer = setInterval(async () => {
    try {
      state.session = await api("/api/session/heartbeat", { method: "POST", body: "{}" });
      applyReadOnlyUi();
    } catch {
      await refreshSessionStatus();
    }
  }, Math.max(30, seconds) * 1000);
}

function releaseSessionLock() {
  const token = sessionStorage.getItem(SESSION_KEY);
  if (!token || !state.session?.can_write) return;
  const blob = new Blob([JSON.stringify({ token })], { type: "application/json" });
  navigator.sendBeacon("/api/session/logout", blob);
  sessionStorage.removeItem(SESSION_KEY);
}

async function submitLogin(e) {
  e.preventDefault();
  const btn = $("#btn-login-submit");
  const role = document.querySelector('input[name="collab-role"]:checked')?.value || "viewer";
  if (btn) {
    btn.disabled = true;
    btn.textContent = "…";
  }
  try {
    const res = await fetch("/api/session/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: $("#login-user").value.trim(),
        password: $("#login-password").value,
        role,
      }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      const detail = typeof data.detail === "string" ? data.detail : "Error";
      showToast(detail === "invalid_credentials" ? t("collab_login_invalid") : detail);
      return;
    }
    sessionStorage.setItem(SESSION_KEY, data.token);
    state.session = data;
    $("#login-overlay").classList.add("hidden");
    $("#app").classList.remove("app--locked");
    if (data.editor_blocked && data.lock_holder) {
      showToast(t("collab_login_blocked", {
        user: data.lock_holder.username,
        machine: data.lock_holder.machine || "—",
      }));
    }
    applyReadOnlyUi();
    await loadMainApp();
  } catch (err) {
    showToast(err.message || "Server 未連接，請重新 run_dev.py");
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = t("collab_login_btn");
    }
  }
}

async function logoutSession() {
  try {
    await api("/api/session/logout", { method: "POST", body: "{}" });
  } catch {
    /* ignore */
  }
  sessionStorage.removeItem(SESSION_KEY);
  stopHeartbeat();
  stopViewerPoll();
  state.session = await api("/api/session/status");
  $("#login-password").value = "";
  applyReadOnlyUi();
  if (state.session?.collab_enabled) {
    applyLoginLabels();
    $("#login-overlay").classList.remove("hidden");
    $("#app").classList.add("app--locked");
  }
  renderCollabPasswordPanel({ enabled: state.session?.collab_enabled });
}

async function promoteToEditor() {
  const btn = $("#btn-collab-promote");
  if (btn?.disabled) return;
  const prev = btn?.textContent;
  if (btn) {
    btn.disabled = true;
    btn.textContent = "…";
  }
  try {
    state.session = await api("/api/session/promote", { method: "POST", body: "{}" });
    applyReadOnlyUi();
    showToast(t("collab_promote_ok"));
    await refreshAll();
  } catch (err) {
    state.session = await api("/api/session/status");
    applyReadOnlyUi();
    const msg = err.message === "lock_held" ? t("collab_promote_fail") : (err.message || t("collab_promote_fail"));
    showToast(msg);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = prev || t("collab_promote_btn");
    }
  }
}

async function demoteToViewer() {
  const btn = $("#btn-collab-demote");
  if (btn?.disabled) return;
  const prev = btn?.textContent;
  if (btn) {
    btn.disabled = true;
    btn.textContent = "…";
  }
  try {
    state.session = await api("/api/session/demote", { method: "POST", body: "{}" });
    applyReadOnlyUi();
    showToast(t("collab_demote_ok"));
    await refreshAll();
  } catch (err) {
    showToast(err.message || t("collab_readonly_toast"));
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = prev || t("collab_demote_btn");
    }
  }
}

async function renderCollabSettingsPanel(cfg, status) {
  $("#collab-settings-title").textContent = t("collab_settings_title");
  $("#collab-settings-desc").textContent = t("collab_settings_desc");
  $("#lbl-collab-enabled").textContent = t("collab_settings_enable");
  $("#collab-test-hint").textContent = t("collab_test_hint");
  $("#btn-collab-test-window").textContent = t("collab_open_test_window");
  $("#btn-collab-force-unlock").textContent = t("collab_force_unlock_btn");
  $("#collab-enabled").checked = !!cfg?.enabled;
  const holder = status?.lock_holder;
  $("#collab-lock-status").textContent = holder?.username
    ? t("collab_lock_status", { user: holder.username, machine: holder.machine || "—" })
    : t("collab_lock_free");
  renderCollabPasswordPanel(cfg);
}

function renderCollabPasswordLabels() {
  $("#collab-password-title").textContent = t("collab_password_title");
  $("#collab-password-desc").textContent = t("collab_password_desc");
  $("#lbl-pw-current").textContent = t("password_current");
  $("#lbl-pw-new").textContent = t("password_new");
  $("#lbl-pw-confirm").textContent = t("password_confirm");
  $("#btn-change-password").textContent = t("password_change_btn");
  $("#collab-admin-reset-title").textContent = t("password_admin_reset_title");
  $("#collab-admin-reset-desc").textContent = t("password_admin_reset_desc");
  $("#lbl-pw-target-user").textContent = t("password_target_user");
  $("#lbl-pw-admin-confirm").textContent = t("password_admin_confirm");
  $("#lbl-pw-reset-new").textContent = t("password_new");
  $("#lbl-pw-reset-confirm").textContent = t("password_confirm");
  $("#btn-admin-reset-password").textContent = t("password_reset_btn");
}

function renderCollabPasswordPanel(cfg) {
  const panel = $("#collab-password-panel");
  if (!panel) return;
  const show = !!cfg?.enabled && !!state.session?.authenticated;
  panel.classList.toggle("hidden", !show);
  if (!show) return;
  renderCollabPasswordLabels();
  const isAdmin = state.session?.username === "admin";
  const adminPanel = $("#collab-admin-reset-panel");
  adminPanel?.classList.toggle("hidden", !isAdmin);
  if (!isAdmin) return;
  const users = (cfg?.usernames || []).filter((u) => u !== "admin");
  const sel = $("#pw-target-user");
  if (!sel) return;
  const options = users.length ? users : ["user"];
  sel.innerHTML = options.map((u) => `<option value="${escapeHtml(u)}">${escapeHtml(u)}</option>`).join("");
}

function passwordErrorMessage(code) {
  const map = {
    invalid_credentials: t("collab_login_invalid"),
    password_too_short: t("password_too_short"),
    password_mismatch: t("password_mismatch"),
    password_empty: t("password_too_short"),
    not_authenticated: t("collab_login_invalid"),
    not_admin: t("password_not_admin"),
    user_not_found: t("collab_login_invalid"),
  };
  return map[code] || code;
}

async function submitChangePassword(e) {
  e.preventDefault();
  const current = $("#pw-current")?.value || "";
  const nw = $("#pw-new")?.value || "";
  const confirm = $("#pw-confirm")?.value || "";
  if (nw !== confirm) {
    showToast(t("password_mismatch"));
    return;
  }
  if (nw.trim().length < 4) {
    showToast(t("password_too_short"));
    return;
  }
  const btn = $("#btn-change-password");
  const prev = btn?.textContent;
  if (btn) {
    btn.disabled = true;
    btn.textContent = "…";
  }
  try {
    const res = await api(`/api/collab/change-password?lang=${state.lang}`, {
      method: "POST",
      body: JSON.stringify({ current_password: current, new_password: nw }),
    });
    showToast(res.message || t("password_change_ok"));
    $("#form-change-password")?.reset();
    const activity = await api(`/api/activity?limit=40&lang=${state.lang}`);
    renderActivityPanel(activity);
  } catch (err) {
    showToast(passwordErrorMessage(err.message));
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = prev || t("password_change_btn");
    }
  }
}

async function submitAdminResetPassword(e) {
  e.preventDefault();
  const target = $("#pw-target-user")?.value || "";
  const adminPass = $("#pw-admin-confirm")?.value || "";
  const nw = $("#pw-reset-new")?.value || "";
  const confirm = $("#pw-reset-confirm")?.value || "";
  if (nw !== confirm) {
    showToast(t("password_mismatch"));
    return;
  }
  if (nw.trim().length < 4) {
    showToast(t("password_too_short"));
    return;
  }
  const btn = $("#btn-admin-reset-password");
  const prev = btn?.textContent;
  if (btn) {
    btn.disabled = true;
    btn.textContent = "…";
  }
  try {
    const res = await api(`/api/collab/reset-password?lang=${state.lang}`, {
      method: "POST",
      body: JSON.stringify({
        admin_password: adminPass,
        target_username: target,
        new_password: nw,
      }),
    });
    showToast(res.message || t("password_reset_ok", { user: target }));
    $("#form-admin-reset-password")?.reset();
    renderCollabPasswordPanel(await api("/api/collab"));
    const activity = await api(`/api/activity?limit=40&lang=${state.lang}`);
    renderActivityPanel(activity);
  } catch (err) {
    showToast(passwordErrorMessage(err.message));
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = prev || t("password_reset_btn");
    }
  }
}

async function setCollabEnabled(enabled) {
  const cfg = await api("/api/collab", {
    method: "PATCH",
    body: JSON.stringify({ enabled }),
  });
  state.session = await refreshSessionStatus();
  if (enabled && !state.session?.authenticated) {
    applyLoginLabels();
    $("#login-overlay").classList.remove("hidden");
    $("#app").classList.add("app--locked");
  }
  renderCollabSettingsPanel(cfg, state.session);
}

async function forceUnlockCollab() {
  const user = window.prompt(`${t("collab_login_user")} (admin):`, "admin");
  if (!user) return;
  const pass = window.prompt(`${t("collab_login_password")}:`);
  if (pass === null) return;
  try {
    await api("/api/session/force-unlock", {
      method: "POST",
      body: JSON.stringify({ username: user.trim(), password: pass }),
    });
    state.session = await refreshSessionStatus();
    showToast(t("collab_force_unlock_ok"));
    renderCollabSettingsPanel(await api("/api/collab"), state.session);
  } catch (err) {
    showToast(err.message || t("collab_login_invalid"));
  }
}

function t(key, vars = {}) {
  const fb = (EXTRA_FALLBACK[state.lang] || EXTRA_FALLBACK.zh)[key];
  let s = state.strings[key] || fb || key;
  Object.entries(vars).forEach(([k, v]) => {
    s = s.replace(new RegExp(`\\{${k}\\}`, "g"), String(v));
  });
  return s;
}

function showToast(msg) {
  const el = $("#toast");
  el.textContent = msg;
  el.classList.remove("hidden");
  setTimeout(() => el.classList.add("hidden"), 2200);
}

function scrollToId(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function parseClientNumbers(text) {
  return [...new Set(String(text || "").split(/[\n,;]+/).map((s) => s.trim()).filter(Boolean))];
}

function formatClientNumbers(nums) {
  return (nums || []).join(", ");
}

function renderClientNumbersHtml(nums) {
  const list = nums || [];
  if (!list.length) return `<span class="field-val-muted">—</span>`;
  return `<div class="clients-number-list">${list.map((n) => `<span class="clients-number-pill">${escapeHtml(n)}</span>`).join("")}</div>`;
}

function statusClass(tier) {
  return `status-pill status-pill--${tier}`;
}

function progressRingHtml(done, total) {
  if (!total) return "";
  const pct = Math.min(100, Math.round((done / total) * 100));
  const r = 14;
  const circ = 2 * Math.PI * r;
  const offset = circ * (1 - pct / 100);
  return `<div class="ms-ring" title="${done}/${total}"><svg viewBox="0 0 36 36" width="32" height="32" aria-hidden="true">
    <circle class="ms-ring-bg" cx="18" cy="18" r="${r}"></circle>
    <circle class="ms-ring-fg" cx="18" cy="18" r="${r}" stroke-dasharray="${circ.toFixed(2)}" stroke-dashoffset="${offset.toFixed(2)}"></circle>
    <text x="18" y="19" class="ms-ring-text">${done}/${total}</text>
  </svg></div>`;
}

function trackerCardClass(c) {
  const tier = c.countdown_tier || c.status_tier;
  return `tracker-card tracker-card--${tier}`;
}

function daysCountHtml(c) {
  const tier = c.countdown_tier || "ok";
  return `<div class="days-count days-count--${tier}" style="color:${c.days_color}">${escapeHtml(c.days_display)}</div>`;
}

function lastReminderHtml(c) {
  const text = c.last_reminder_label || t("last_reminder_none");
  return `<div class="last-reminder-note">${escapeHtml(text)}</div>`;
}

function renderAlertBanner() {
  const el = $("#alert-banner");
  const hint = $("#alert-settings-hint");
  const cfg = state.dashboard?.alert_settings || state.meta?.alert_settings;
  if (hint && cfg) {
    hint.textContent = t("alert_settings_hint", {
      urgent: cfg.urgent_days,
      critical: cfg.critical_days,
      warning: cfg.warning_days,
    });
    hint.classList.toggle("hidden", state.view !== "dashboard");
  }
  if (!el) return;
  const banner = state.dashboard?.alert_banner;
  if (state.view !== "dashboard" || !banner?.show) {
    el.classList.add("hidden");
    return;
  }
  el.className = `alert-banner alert-banner--${banner.level}`;
  $("#alert-banner-text").textContent = banner.message;
  const action = $("#alert-banner-action");
  action.textContent = t("banner_action");
  action.onclick = async () => {
    state.filter = banner.expired > 0 ? "expired" : "urgent";
    switchView("dashboard");
    await loadDashboard();
    scrollToId("section-priority");
  };
  el.classList.remove("hidden");
}

async function logReminderSent() {
  if (!state.composeClientId) return;
  try {
    await api(`/api/clients/${state.composeClientId}/log-reminder?lang=${state.lang}`, {
      method: "POST",
      body: JSON.stringify({}),
    });
  } catch {
    /* non-blocking */
  }
}

function openComposeDrawer(clientId) {
  if (clientId) state.composeClientId = clientId;
  $("#compose-drawer").classList.add("open");
  $("#compose-drawer").setAttribute("aria-hidden", "false");
  $("#compose-backdrop").classList.remove("hidden");
  document.body.classList.add("compose-open");
  refreshComposeClients().then(async () => {
    await loadComposeDetail();
    await loadReminder();
  });
}

function closeComposeDrawer() {
  $("#compose-drawer").classList.remove("open");
  $("#compose-drawer").setAttribute("aria-hidden", "true");
  $("#compose-backdrop").classList.add("hidden");
  document.body.classList.remove("compose-open");
}

function scheduleEditBtnHtml(c) {
  if (c.mode !== "milestone") return "";
  return `<button type="button" class="btn btn-secondary btn-xs btn-schedule-edit" data-id="${c.id}">${escapeHtml(t("schedule_edit_btn"))}</button>`;
}

function useCompactActions() {
  return (
    document.documentElement.classList.contains("mobile-glance")
    || window.matchMedia("(max-width: 640px) and (orientation: portrait)").matches
  );
}

function actionLabel(fullKey, shortKey) {
  const key = useCompactActions() ? shortKey : fullKey;
  const label = t(key);
  if (label === key && useCompactActions()) return t(fullKey);
  return label;
}

function tableActionLabel(fullKey, shortKey) {
  const short = t(shortKey);
  if (short && short !== shortKey) return short;
  return t(fullKey);
}

function accountStatusBtnHtml(c, tableCompact = false) {
  if (c.is_closed) {
    return `<button type="button" class="btn btn-secondary btn-xs btn-reopen-client" data-id="${c.id}">${escapeHtml(t("btn_reopen_client"))}</button>`;
  }
  const label = tableCompact
    ? tableActionLabel("btn_close_client", "btn_close_client_short")
    : t("btn_close_client");
  return `<button type="button" class="btn btn-secondary btn-xs btn-close-client" data-id="${c.id}">${escapeHtml(label)}</button>`;
}

function milestoneQueueActionsHtml(c) {
  if (c.is_closed) return "";
  const parts = [];
  if (c.mode === "milestone") {
    parts.push(`<button type="button" class="btn btn-secondary btn-xs btn-schedule-edit" data-id="${c.id}">${escapeHtml(t("schedule_edit_btn"))}</button>`);
  }
  if (c.needs_alert || c.alert_snoozed) {
    parts.push(`<button type="button" class="btn btn-secondary btn-xs btn-renew" data-id="${c.id}">${escapeHtml(actionLabel("btn_renew", "btn_renew_short"))}</button>`);
    parts.push(`<button type="button" class="btn btn-secondary btn-xs btn-dismiss" data-id="${c.id}">${escapeHtml(actionLabel("btn_dismiss_alert", "btn_dismiss_short"))}</button>`);
    parts.push(`<button type="button" class="btn btn-secondary btn-xs btn-close-client" data-id="${c.id}">${escapeHtml(t("btn_close_client"))}</button>`);
  }
  parts.push(`<button type="button" class="btn btn-primary btn-xs btn-compose-open" data-id="${c.id}">${escapeHtml(actionLabel("open_compose", "open_compose_short"))}</button>`);
  const snooze = c.alert_snoozed
    ? `<div class="snooze-note">${escapeHtml(t("alert_snoozed"))}${c.alert_snoozed_until ? ` · ${escapeHtml(c.alert_snoozed_until)}` : ""}</div>`
    : "";
  return `${snooze}<div class="card-actions card-actions--compact">${parts.join("")}</div>`;
}

function cardActionsHtml(c) {
  if (c.is_closed) return "";
  if (!c.needs_alert && !c.alert_snoozed) return "";
  const snooze = c.alert_snoozed
    ? `<div class="snooze-note">${escapeHtml(t("alert_snoozed"))}${c.alert_snoozed_until ? ` · ${escapeHtml(c.alert_snoozed_until)}` : ""}</div>`
    : "";
  return `${snooze}<div class="card-actions card-actions--compact">
    <button type="button" class="btn btn-secondary btn-xs btn-renew" data-id="${c.id}">${escapeHtml(actionLabel("btn_renew", "btn_renew_short"))}</button>
    <button type="button" class="btn btn-secondary btn-xs btn-dismiss" data-id="${c.id}">${escapeHtml(actionLabel("btn_dismiss_alert", "btn_dismiss_short"))}</button>
    <button type="button" class="btn btn-secondary btn-xs btn-close-client" data-id="${c.id}">${escapeHtml(t("btn_close_client"))}</button>
    <button type="button" class="btn btn-primary btn-xs btn-compose-open" data-id="${c.id}">${escapeHtml(actionLabel("open_compose", "open_compose_short"))}</button>
  </div>`;
}

function priorityActionsHtml(c) {
  if (!c.needs_alert && !c.alert_snoozed) return "";
  const parts = [];
  if (c.needs_alert || c.alert_snoozed) {
    parts.push(`<button type="button" class="btn btn-secondary btn-xs btn-renew" data-id="${c.id}">${escapeHtml(actionLabel("btn_renew", "btn_renew_short"))}</button>`);
    parts.push(`<button type="button" class="btn btn-secondary btn-xs btn-dismiss" data-id="${c.id}">${escapeHtml(actionLabel("btn_dismiss_alert", "btn_dismiss_short"))}</button>`);
  }
  parts.push(`<button type="button" class="btn btn-primary btn-xs btn-compose-open" data-id="${c.id}">${escapeHtml(actionLabel("open_compose", "open_compose_short"))}</button>`);
  return `<div class="card-actions card-actions--compact">${parts.join("")}</div>`;
}

function bindCardActions(root) {
  root.querySelectorAll(".btn-client-edit").forEach((btn) => {
    btn.addEventListener("click", () => {
      closeClientDetailPanel();
      openClientEdit(btn.dataset.id);
    });
  });
  root.querySelectorAll(".btn-schedule-edit").forEach((btn) => {
    btn.addEventListener("click", () => {
      closeClientDetailPanel();
      openScheduleEdit(btn.dataset.id);
    });
  });
  root.querySelectorAll(".btn-renew").forEach((btn) => {
    btn.addEventListener("click", () => {
      closeClientDetailPanel();
      openRenew(btn.dataset.id);
    });
  });
  root.querySelectorAll(".btn-dismiss").forEach((btn) => {
    btn.addEventListener("click", () => dismissAlert(btn.dataset.id));
  });
  root.querySelectorAll(".btn-compose-open").forEach((btn) => {
    btn.addEventListener("click", () => {
      closeClientDetailPanel();
      openComposeDrawer(btn.dataset.id);
    });
  });
  root.querySelectorAll(".btn-close-client").forEach((btn) => {
    btn.addEventListener("click", () => closeClientAccount(btn.dataset.id));
  });
  root.querySelectorAll(".btn-reopen-client").forEach((btn) => {
    btn.addEventListener("click", () => reopenClientAccount(btn.dataset.id));
  });
}

function closeClientDetailPanel() {
  const drawer = $("#clients-detail-drawer");
  const backdrop = $("#clients-detail-backdrop");
  if (!drawer) return;
  drawer.classList.remove("open");
  drawer.setAttribute("aria-hidden", "true");
  backdrop?.classList.add("hidden");
  document.body.classList.remove("clients-detail-open");
  state.clientsSelectedId = null;
  const pickSel = $("#clients-quick-pick");
  if (pickSel) pickSel.value = "";
  $("#clients-tbody")?.querySelectorAll(".clients-row").forEach((tr) => {
    tr.classList.remove("selected");
  });
}

function openClientDetailPanelShell() {
  const drawer = $("#clients-detail-drawer");
  const backdrop = $("#clients-detail-backdrop");
  if (!drawer || !backdrop) return;
  drawer.classList.add("open");
  drawer.setAttribute("aria-hidden", "false");
  backdrop.classList.remove("hidden");
  document.body.classList.add("clients-detail-open");
}

async function dismissAlert(clientId) {
  const res = await api(`/api/clients/${clientId}/dismiss-alert?lang=${state.lang}`, {
    method: "POST",
    body: JSON.stringify({ snooze_days: 30 }),
  });
  showToast(res.message);
  await refreshAll();
}

async function closeClientAccount(clientId) {
  if (!clientId) return;
  if (!window.confirm(t("close_client_confirm"))) return;
  try {
    const res = await api(`/api/clients/${clientId}/close?lang=${state.lang}`, {
      method: "POST",
      body: JSON.stringify({}),
    });
    showToast(res.message);
    closeClientDetailPanel();
    $("#modal-renew").close();
    state.renewClientId = null;
    await refreshAll();
  } catch (err) {
    showToast(err.message);
  }
}

async function reopenClientAccount(clientId) {
  if (!clientId) return;
  try {
    const res = await api(`/api/clients/${clientId}/reopen?lang=${state.lang}`, {
      method: "POST",
      body: JSON.stringify({}),
    });
    showToast(res.message);
    await refreshAll();
  } catch (err) {
    showToast(err.message);
  }
}

function openRenew(clientId) {
  state.renewClientId = clientId;
  const c = [...(state.dashboard?.clients || []), ...(state.dashboard?.priority || [])].find(
    (x) => x.id === clientId
  );
  $("#renew-client-name").textContent = c ? c.client_name : "";
  $("#renew-date").value = state.meta.today;
  const isMs = c && c.mode === "milestone";
  $("#renew-reset-wrap").classList.toggle("hidden", !isMs);
  $("#renew-reset-ms").checked = false;
  $("#modal-renew").showModal();
}

async function submitRenew(e) {
  e.preventDefault();
  if (!state.renewClientId) return;
  try {
    const res = await api(`/api/clients/${state.renewClientId}/renew?lang=${state.lang}`, {
      method: "POST",
      body: JSON.stringify({
        new_end_date: $("#renew-date").value,
        reset_milestones: $("#renew-reset-ms").checked,
      }),
    });
    showToast(res.message);
    $("#modal-renew").close();
    state.renewClientId = null;
    await refreshAll();
  } catch (err) {
    showToast(err.message);
  }
}

function switchView(view) {
  state.view = view;
  if (view !== "clients") closeClientDetailPanel();
  document.querySelectorAll(".nav-tab").forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.view === view);
  });
  $("#view-dashboard").classList.toggle("hidden", view !== "dashboard");
  $("#view-clients").classList.toggle("hidden", view !== "clients");
  $("#view-milestones").classList.toggle("hidden", view !== "milestones");
  $("#kpi-row").classList.toggle("hidden", view !== "dashboard");
  $("#fab-compose").classList.toggle("hidden", view !== "dashboard" && view !== "milestones");
  $("#alert-banner").classList.toggle("hidden", view !== "dashboard");
  $("#alert-settings-hint").classList.toggle("hidden", view !== "dashboard");
  if (view === "dashboard" && state.dashboard) renderAlertBanner();
  if (view === "clients") loadClientsTable();
  if (view === "milestones") loadMilestoneQueue();
}

let clockTimer = null;

function formatLiveDatetime(lang) {
  const now = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  const time = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;
  if (lang === "en") {
    const date = now.toLocaleDateString("en-US", {
      weekday: "short",
      year: "numeric",
      month: "short",
      day: "numeric",
    });
    return `${date} ${time}`;
  }
  const locale = lang === "zh_cn" ? "zh-CN" : "zh-HK";
  const date = now.toLocaleDateString(locale, {
    weekday: "short",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
  return `${date} ${time}`;
}

function startLiveClock() {
  if (clockTimer) clearInterval(clockTimer);
  const tick = () => {
    const label = $("#hero-datetime-label");
    const value = $("#hero-datetime-value");
    if (!label || !value) return;
    label.textContent = t("today");
    value.textContent = formatLiveDatetime(state.lang);
  };
  tick();
  clockTimer = setInterval(tick, 1000);
}

function applyBranding() {
  const b = state.branding;
  const s = state.strings || {};
  document.title = b.appName;
  document.documentElement.style.setProperty("--primary", b.primaryColor || "#007AFF");
  $("#brand-logo").src = b.logo.includes("?") ? b.logo : `${b.logo}?v=3`;
  $("#brand-logo").alt = b.logoAlt || b.appName;
  $("#brand-tagline").textContent = s.tagline || b.tagline;
  $("#brand-title").textContent = b.appName;
  $("#brand-title").title = s.subtitle || b.subtitle || "";
  $("#footer-note").textContent = s.sidebar_footer || b.footerNote;
}

function applyScheduleQuickLabels() {
  $("#lbl-schedule-title").textContent = t("schedule_title");
  $("#lbl-schedule-end-hint").textContent = t("schedule_end_hint");
  $("#lbl-schedule-help").textContent = t("schedule_help");
  $("#lbl-schedule-first").textContent = t("schedule_first");
  $("#btn-schedule-10w1").textContent = t("schedule_every_1w");
  $("#btn-schedule-8w2").textContent = t("schedule_every_2w");
  $("#btn-schedule-4x3").textContent = t("schedule_every_3m");
  $("#btn-schedule-2x6").textContent = t("schedule_every_6m");
  $("#btn-schedule-add").textContent = `＋ ${t("schedule_add_row")}`;
}

function applyScheduleEditLabels() {
  $("#schedule-edit-title").textContent = t("schedule_edit_title");
  $("#lbl-schedule-edit-help").textContent = t("schedule_edit_help");
  $("#lbl-edit-schedule-first").textContent = t("schedule_first");
  $("#lbl-edit-schedule-end-hint").textContent = t("schedule_end_hint");
  $("#btn-edit-schedule-10w1").textContent = t("schedule_every_1w");
  $("#btn-edit-schedule-8w2").textContent = t("schedule_every_2w");
  $("#btn-edit-schedule-4x3").textContent = t("schedule_every_3m");
  $("#btn-edit-schedule-2x6").textContent = t("schedule_every_6m");
  $("#btn-edit-schedule-add").textContent = `＋ ${t("schedule_add_row")}`;
  $("#btn-schedule-save").textContent = t("save_schedule");
  $("#btn-schedule-cancel").textContent = state.strings?.close_btn || "Close";
}

function applyStaticLabels() {
  const s = state.strings;
  $("#btn-add").textContent = `＋ ${s.sidebar_add}`;
  $("#btn-manage").textContent = s.manage;
  $("#btn-settings").textContent = t("settings_btn");
  $("#modal-settings-title").textContent = t("settings_title");
  $("#data-path-settings-title").textContent = t("data_path_settings_title");
  $("#data-path-settings-desc").textContent = t("data_path_settings_desc");
  $("#btn-data-path-browse").textContent = t("data_path_browse_btn");
  $("#btn-data-path-apply").textContent = t("data_path_apply_btn");
  $("#btn-data-path-default").textContent = t("data_path_default_btn");
  $("#about-settings-title").textContent = t("about_title");
  $("#notify-settings-title").textContent = t("notify_settings_title");
  $("#notify-settings-desc").textContent = t("notify_settings_desc");
  $("#lbl-notify-enabled").textContent = t("notify_settings_enable");
  $("#sample-settings-title").textContent = t("sample_settings_title");
  $("#sample-settings-desc").textContent = t("sample_settings_desc");
  $("#lbl-sample-seed-enabled").textContent = t("sample_seed_enable");
  $("#btn-sample-load").textContent = t("sample_load_btn");
  $("#btn-sample-clear").textContent = t("sample_clear_btn");
  $("#activity-settings-title").textContent = t("activity_title");
  $("#lan-settings-title").textContent = t("lan_settings_title");
  $("#lan-settings-desc").textContent = t("lan_settings_desc");
  $("#lbl-lan-enabled").textContent = t("lan_settings_enable");
  $("#lan-settings-warn").textContent = t("lan_settings_warn");
  $("#lan-settings-hint").textContent = t("lan_settings_hint");
  $("#lan-glance-hint").textContent = t("lan_glance_hint");
  $("#lan-no-ip").textContent = t("lan_settings_no_ip");
  $("#btn-lan-copy").textContent = t("lan_copy_url");
  $("#backup-settings-title").textContent = t("backup_title");
  $("#lbl-backup-pick").textContent = t("backup_pick_label");
  $("#btn-backup-restore-selected").textContent = t("backup_restore_selected_btn");
  $("#btn-backup-restore").textContent = t("backup_restore_btn");
  $("#import-settings-title").textContent = t("import_settings_title");
  $("#import-settings-desc").textContent = t("import_settings_desc");
  $("#lbl-import-replace").textContent = t("import_replace_label");
  $("#btn-import-template").textContent = t("import_template_btn");
  $("#btn-import-excel").textContent = t("import_excel_btn");
  $("#btn-settings-close").textContent = s.close_btn;
  $("#collab-settings-title").textContent = t("collab_settings_title");
  $("#collab-settings-desc").textContent = t("collab_settings_desc");
  $("#lbl-collab-enabled").textContent = t("collab_settings_enable");
  $("#collab-test-hint").textContent = t("collab_test_hint");
  $("#btn-collab-test-window").textContent = t("collab_open_test_window");
  $("#btn-collab-force-unlock").textContent = t("collab_force_unlock_btn");
  renderCollabPasswordLabels();
  applyLoginLabels();
  $("#lbl-priority").textContent = `⚡ ${s.section_priority}`;
  $("#lbl-board").textContent = s.section_board;
  $("#lbl-compose").textContent = s.section_compose;
  $("#lbl-compose-cap").textContent = s.compose_cap;
  $("#lbl-select-client").textContent = s.select_client;
  $("#lbl-channel").textContent = s.channel_lbl;
  $("#lbl-payment").textContent = s.payment_lbl;
  $("#btn-copy").textContent = s.copy_btn;
  $("#btn-mailto").textContent = s.email_open_btn;
  $("#modal-add-title").textContent = s.sidebar_add;
  $("#modal-edit-title").textContent = t("edit_client_title");
  $("#modal-manage-title").textContent = s.manage;
  $("#btn-add-submit").textContent = s.add_btn;
  $("#btn-add-cancel").textContent = s.close_btn;
  $("#lbl-edit-client-name").textContent = s.client_name;
  $("#lbl-edit-group").textContent = t("client_group");
  $("#lbl-edit-client-numbers").textContent = t("client_numbers");
  $("#lbl-edit-client-numbers-hint").textContent = t("client_numbers_hint");
  $("#lbl-edit-contact").textContent = s.contact_person;
  $("#lbl-edit-email").textContent = s.client_email;
  $("#lbl-edit-service").textContent = s.service_label;
  $("#lbl-edit-end-date").textContent = s.end_date;
  $("#edit-ms-hint").textContent = t("milestone_edit_hint");
  $("#btn-edit-save").textContent = t("save_client");
  $("#btn-edit-cancel").textContent = s.close_btn;
  $("#btn-manage-close").textContent = s.close_btn;
  $("#lbl-mode").textContent = `${s.mode_single} / ${s.mode_milestone}`;
  $("#add-mode option[value=single]").textContent = s.mode_single;
  $("#add-mode option[value=milestone]").textContent = s.mode_milestone;
  $("#lbl-client-name").textContent = s.client_name;
  $("#lbl-add-group").textContent = t("client_group");
  $("#lbl-add-client-numbers").textContent = t("client_numbers");
  $("#lbl-add-client-numbers-hint").textContent = t("client_numbers_hint");
  $("#lbl-contact").textContent = s.contact_person;
  $("#lbl-email").textContent = s.client_email;
  $("#lbl-service").textContent = s.service_label;
  $("#lbl-end-date").textContent = s.end_date;
  $("#lbl-total-ms").textContent = s.total_ms;
  applyScheduleQuickLabels();
  applyScheduleEditLabels();
  document.querySelectorAll(".nav-tab").forEach((tab) => {
    const view = tab.dataset.view;
    const key = `nav_${view}`;
    const fb = (NAV_FALLBACK[state.lang] || NAV_FALLBACK.zh)[view];
    const label = s[key] || fb || view;
    tab.textContent = label;
    tab.title = label;
  });
  $("#lbl-clients-table").textContent = s.clients_table_title;
  $("#lbl-clients-detail").textContent = t("clients_detail_title");
  $("#clients-page-hint").textContent = t("clients_detail_hint");
  $("#clients-search").placeholder = t("clients_search");
  $("#clients-group-filter").title = t("client_group");
  $("#clients-quick-pick").title = t("clients_pick");
  const exportBtn = $("#btn-export-excel");
  if (exportBtn) exportBtn.textContent = t("export_excel_btn");
  $("#lbl-ms-pending").textContent = s.ms_pending_title;
  $("#lbl-ms-completed").textContent = s.ms_completed_title;
  $("#renew-title").textContent = s.renew_title;
  $("#lbl-renew-date").textContent = s.renew_new_date;
  $("#lbl-renew-reset").textContent = s.renew_reset_ms;
  $("#btn-renew-submit").textContent = s.btn_renew;
  $("#btn-renew-close-client").textContent = t("btn_close_client");
  $("#btn-renew-cancel").textContent = s.close_btn;
  $("#fab-compose-label").textContent = s.fab_compose || s.open_compose;
  $("#btn-compose-close").setAttribute("aria-label", s.compose_close || s.close_btn);
  if ($("#add-mode").value === "milestone") {
    const existing = collectScheduleDates();
    if (existing.length) renderScheduleRows(existing);
  }
  startLiveClock();
}

function renderLangBar() {
  const bar = $("#lang-bar");
  bar.innerHTML = "";
  state.meta.langs.forEach(({ code, short }) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = `lang-btn${code === state.lang ? " active" : ""}`;
    btn.textContent = short;
    btn.addEventListener("click", () => {
      state.lang = code;
      boot(false);
    });
    bar.appendChild(btn);
  });
}

function renderRadios(containerId, items, current, onChange) {
  const box = $(containerId);
  box.innerHTML = "";
  items.forEach((item) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = `pill${item.id === current ? " active" : ""}`;
    btn.textContent = item.label;
    btn.addEventListener("click", () => onChange(item.id));
    box.appendChild(btn);
  });
}

function addMonthsISO(iso, months) {
  const d = new Date(`${iso}T12:00:00`);
  d.setMonth(d.getMonth() + months);
  return d.toISOString().slice(0, 10);
}

function addDaysISO(iso, days) {
  const d = new Date(`${iso}T12:00:00`);
  d.setDate(d.getDate() + days);
  return d.toISOString().slice(0, 10);
}

function buildScheduleFromFirstDays(first, count, daysApart) {
  const out = [];
  for (let i = 0; i < count; i += 1) {
    out.push(addDaysISO(first, daysApart * i));
  }
  return out;
}

function buildScheduleFromFirst(first, count, monthsApart) {
  const out = [];
  for (let i = 0; i < count; i += 1) {
    out.push(addMonthsISO(first, monthsApart * i));
  }
  return out;
}

function renderScheduleRows(dates) {
  const box = $("#add-schedule-rows");
  if (!box) return;
  const list = dates.length ? dates : [""];
  box.innerHTML = list
    .map(
      (d, i) => `
    <div class="schedule-row">
      <label class="field-lbl">${escapeHtml(t("schedule_visit_n", { n: i + 1 }))}</label>
      <input type="date" class="input schedule-date" value="${escapeHtml(d)}" />
    </div>`
    )
    .join("");
}

function collectScheduleDates() {
  const dates = [...document.querySelectorAll("#add-schedule-rows .schedule-date")].map((inp) => inp.value);
  if (dates.length && dates.some((d) => !d)) return null;
  return dates.filter(Boolean);
}

function toDateInputValue(v) {
  if (!v) return "";
  const s = String(v).trim();
  if (/^\d{4}-\d{2}-\d{2}/.test(s)) return s.slice(0, 10);
  const dmY = s.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
  if (dmY) {
    const [, d, m, y] = dmY;
    return `${y}-${m.padStart(2, "0")}-${d.padStart(2, "0")}`;
  }
  return s;
}

function scheduleRowsFromClient(c) {
  const schedule = (c.milestone_schedule || []).map(toDateInputValue);
  const completions = c.milestone_dates || [];
  const apiRows = c.milestone_rows || [];
  const total = Math.max(schedule.length, completions.length, apiRows.length, c.milestone_total || 0);

  if (apiRows.length) {
    return apiRows.map((row, i) => ({
      ...row,
      planned: toDateInputValue(row.planned || schedule[i] || ""),
    }));
  }

  const rows = [];
  for (let i = 0; i < total; i += 1) {
    rows.push({
      index: i,
      label: t("schedule_visit_n", { n: i + 1 }),
      planned: schedule[i] || "",
      completed: completions[i] || null,
      done: Boolean(completions[i]),
    });
  }
  return rows;
}

function renderEditScheduleRows(rows) {
  const box = $("#edit-schedule-rows");
  if (!box) return;
  box.innerHTML = (rows || [])
    .map((row, i) => {
      if (row.done) {
        return `
    <div class="schedule-row schedule-row--done">
      <span class="field-lbl">${escapeHtml(row.label)} · ${escapeHtml(t("schedule_done_row"))}</span>
      <span class="schedule-done-date">${escapeHtml(row.planned)}${row.completed ? ` → ${escapeHtml(row.completed)}` : ""}</span>
    </div>`;
      }
      return `
    <div class="schedule-row">
      <label class="field-lbl">${escapeHtml(row.label || t("schedule_visit_n", { n: i + 1 }))}</label>
      <input type="date" class="input schedule-date" value="${escapeHtml(toDateInputValue(row.planned))}" />
    </div>`;
    })
    .join("");
}

function collectEditScheduleDates() {
  const locked = state.scheduleEditLocked || [];
  const pending = [...document.querySelectorAll("#edit-schedule-rows .schedule-date")]
    .map((inp) => inp.value)
    .filter(Boolean);
  return [...locked, ...pending];
}

function applyEditQuickFill(count, intervalDays, monthsApart) {
  const first = $("#edit-schedule-first").value;
  if (!first) return showToast(t("err_schedule"));
  const pending = monthsApart != null
    ? buildScheduleFromFirst(first, count, monthsApart)
    : buildScheduleFromFirstDays(first, count, intervalDays);
  renderEditScheduleRows([
    ...state.scheduleEditDoneRows,
    ...pending.map((planned, i) => ({
      done: false,
      label: t("schedule_visit_n", { n: state.scheduleEditLocked.length + i + 1 }),
      planned,
    })),
  ]);
}

async function openScheduleEdit(clientId) {
  state.scheduleEditClientId = clientId;
  try {
    const c = await api(`/api/clients/${clientId}?lang=${state.lang}`);
    if (c.mode !== "milestone") return;
    applyScheduleEditLabels();
    $("#schedule-edit-client-name").textContent = `${c.client_name} · ${c.service_label || ""}`;
    const rows = scheduleRowsFromClient(c);
    state.scheduleEditLocked = rows.filter((r) => r.done).map((r) => r.planned);
    state.scheduleEditDoneRows = rows.filter((r) => r.done);
    renderEditScheduleRows(rows);
    const firstPending = rows.find((r) => !r.done);
    $("#edit-schedule-first").value = firstPending?.planned || rows[0]?.planned || state.meta?.today || "";
    $("#modal-schedule").showModal();
  } catch (err) {
    showToast(err.message);
  }
}

async function submitScheduleEdit(e) {
  e.preventDefault();
  if (!state.scheduleEditClientId) return;
  const schedule = collectEditScheduleDates();
  if (!schedule.length) {
    showToast(t("err_schedule"));
    return;
  }
  try {
    const res = await api(`/api/clients/${state.scheduleEditClientId}/schedule?lang=${state.lang}`, {
      method: "PUT",
      body: JSON.stringify({ milestone_schedule: schedule }),
    });
    showToast(res.message || t("schedule_saved"));
    $("#modal-schedule").close();
    state.scheduleEditClientId = null;
    state.scheduleEditLocked = [];
    state.scheduleEditDoneRows = [];
    await refreshAll();
  } catch (err) {
    showToast(err.message);
  }
}

async function openClientEdit(clientId) {
  state.editClientId = clientId;
  try {
    const c = await api(`/api/clients/${clientId}?lang=${state.lang}`);
    $("#edit-client-name-caption").textContent = `${c.client_name} · ${c.mode_label || ""}`;
    $("#edit-name").value = c.client_name || "";
    $("#edit-group").value = c.group || "";
    $("#edit-client-numbers").value = formatClientNumbers(c.client_numbers);
    $("#edit-contact").value = c.contact_name || "";
    $("#edit-email").value = c.client_email || "";
    $("#edit-service").value = c.service_label || "";
    $("#edit-end").value = toDateInputValue(c.end_date);
    $("#edit-ms-hint").classList.toggle("hidden", c.mode !== "milestone");
    $("#modal-edit-client").showModal();
  } catch (err) {
    showToast(err.message);
  }
}

async function submitClientEdit(e) {
  e.preventDefault();
  if (!state.editClientId) return;
  try {
    const c = await api(`/api/clients/${state.editClientId}?lang=${state.lang}`);
    const total = c.mode === "milestone"
      ? (c.milestone_total || (c.milestone_schedule || []).length || 1)
      : (c.milestone_total || 0);
    const res = await api(`/api/clients/${state.editClientId}?lang=${state.lang}`, {
      method: "PUT",
      body: JSON.stringify({
        client_name: $("#edit-name").value,
        contact_name: $("#edit-contact").value,
        client_email: $("#edit-email").value,
        group: $("#edit-group").value,
        client_numbers: parseClientNumbers($("#edit-client-numbers").value),
        service_label: $("#edit-service").value,
        end_date: $("#edit-end").value,
        total_milestones: total,
      }),
    });
    showToast(res.message || t("client_saved"));
    $("#modal-edit-client").close();
    state.editClientId = null;
    await refreshAll();
  } catch (err) {
    showToast(err.message);
  }
}

function toggleAddModeUi() {
  const ms = $("#add-mode").value === "milestone";
  $("#add-schedule-panel").classList.toggle("hidden", !ms);
  $("#lbl-end-date").classList.toggle("hidden", ms);
  $("#add-end").classList.toggle("hidden", ms);
  $("#add-end").required = !ms;
  if (ms) {
    applyScheduleQuickLabels();
    if (!$("#add-schedule-first").value) {
      $("#add-schedule-first").value = state.meta?.today || "";
    }
    const existing = collectScheduleDates();
    renderScheduleRows(existing.length ? existing : [$("#add-schedule-first").value || ""]);
  }
}

function renderKpi() {
  const row = $("#kpi-row");
  row.innerHTML = "";
  const order = ["all", "urgent", "milestone", "expired"];
  order.forEach((key) => {
    const k = state.dashboard.kpi[key];
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = `kpi-card kpi-card--${k.css}${state.filter === k.filter ? " active" : ""}`;
    btn.innerHTML = `
      <span class="kpi-lbl">${escapeHtml(k.label)}</span>
      <span class="kpi-val">${escapeHtml(String(k.value))}</span>
      <span class="kpi-sub">${escapeHtml(k.sub)}</span>`;
    btn.addEventListener("click", async () => {
      state.filter = k.filter;
      if (k.filter === "milestone") {
        switchView("milestones");
        await loadMilestoneQueue();
      } else {
        switchView("dashboard");
        await loadDashboard();
        scrollToId(k.scroll);
      }
    });
    row.appendChild(btn);
  });
}

function updateSectionBadges() {
  if (!state.dashboard) return;
  const pCount = state.dashboard.priority.length;
  $("#badge-priority").textContent = pCount ? `· ${pCount}` : "";
  const filterKey = state.filter !== "all" ? state.filter : null;
  const kpiMatch = filterKey
    ? Object.values(state.dashboard.kpi).find((k) => k.filter === filterKey)
    : null;
  const bCount = state.dashboard.clients.length;
  if (kpiMatch) {
    $("#badge-board").textContent = `· ${kpiMatch.label}`;
  } else {
    $("#badge-board").textContent = bCount ? `· ${bCount}` : "";
  }
}

function renderFilterBar() {
  const bar = $("#filter-bar");
  if (!state.dashboard || state.filter === "all") {
    bar.innerHTML = "";
    bar.classList.add("hidden");
    return;
  }
  const k = Object.values(state.dashboard.kpi).find((x) => x.filter === state.filter);
  const label = k ? k.label : state.filter;
  bar.classList.remove("hidden");
  bar.innerHTML = `
    <span class="filter-bar-text">${escapeHtml(t("filter_showing"))} · ${escapeHtml(label)}</span>
    <button type="button" class="filter-clear btn btn-secondary btn-xs">${escapeHtml(t("filter_clear"))}</button>`;
  bar.querySelector(".filter-clear").addEventListener("click", async () => {
    state.filter = "all";
    await loadDashboard();
    scrollToId("section-board");
  });
}

function renderPriority() {
  const list = $("#priority-list");
  const items = state.dashboard.priority;
  updateSectionBadges();
  if (!items.length) {
    list.innerHTML = `<div class="empty-state empty-state--clear">
      <span class="empty-state-icon">✓</span>
      <p>${escapeHtml(t("priority_all_clear"))}</p>
    </div>`;
    return;
  }
  list.innerHTML = items
    .map(
      (c) => `
    <div class="priority-item priority-item--${c.countdown_tier || c.status_tier}">
      <div class="priority-item-body">
        <div class="priority-item-top">
          <strong>${escapeHtml(c.client_name)}</strong>
          <span class="${statusClass(c.status_tier)}">${escapeHtml(c.status_label)}</span>
        </div>
        <span class="priority-svc">${escapeHtml(c.service_label || "—")} · ${escapeHtml(c.days_display)}</span>
        ${lastReminderHtml(c)}
        ${c.alert_snoozed ? `<span class="snooze-note">${escapeHtml(t("alert_snoozed"))}${c.alert_snoozed_until ? ` · ${escapeHtml(c.alert_snoozed_until)}` : ""}</span>` : ""}
      </div>
      <div class="priority-item-actions">${priorityActionsHtml(c)}</div>
    </div>`
    )
    .join("");
  bindCardActions(list);
}

function renderBoard() {
  const grid = $("#board-grid");
  const items = state.dashboard.clients;
  renderFilterBar();
  if (!items.length) {
    grid.innerHTML = `<p class="empty-caption">—</p>`;
    return;
  }
  grid.innerHTML = items
    .map(
      (c) => {
        const ring =
          c.mode === "milestone" && c.milestone_total
            ? progressRingHtml(c.milestone_done, c.milestone_total)
            : "";
        return `
    <article class="${trackerCardClass(c)}">
      <div class="card-head">
        <div class="card-head-left">
          <span class="badge ${c.badge}">${escapeHtml(c.badge_text)}</span>
          ${ring}
        </div>
        <span class="${statusClass(c.status_tier)}">${escapeHtml(c.status_label)}</span>
      </div>
      ${c.milestone_all_complete ? `
      <div class="ms-complete-banner">
        <strong>${escapeHtml(t("ms_all_complete"))}</strong>
        <pre class="ms-history">${escapeHtml(c.milestone_history || "")}</pre>
      </div>` : ""}
      ${c.routine_next_month ? `<div class="routine-badge">${escapeHtml(c.routine_note)} · ${escapeHtml(c.next_planned_visit || "")}</div>` : ""}
      <div class="field-lbl">${escapeHtml(t("col_client"))}</div>
      <div class="field-val">${escapeHtml(c.client_name)}</div>
      <div class="field-lbl" style="margin-top:0.5rem">${escapeHtml(t("service_label"))}</div>
      <div class="field-val field-val-muted">${escapeHtml(c.service_label || "—")}</div>
      ${daysCountHtml(c)}
      ${lastReminderHtml(c)}
      <div class="field-lbl">${escapeHtml(t("card_end"))}</div>
      <div class="field-val field-val-muted">${escapeHtml(c.end_date)}</div>
      <div class="compose-next">
        <div class="field-lbl">${escapeHtml(c.next_label)}</div>
        <div class="field-val">${escapeHtml(c.next_display)}</div>
      </div>
      ${c.mode === "milestone" ? `<div class="card-schedule-bar">${scheduleEditBtnHtml(c)}</div>` : ""}
      ${cardActionsHtml(c)}
    </article>`;
      }
    )
    .join("");
  bindCardActions(grid);
}

async function blobToBase64(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result).split(",")[1] || "");
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

async function saveExportBlob(blob, filename) {
  const api = window.pywebview?.api;
  if (api?.save_excel_export) {
    const result = await api.save_excel_export(await blobToBase64(blob), filename);
    if (result?.cancelled) return "cancelled";
    if (!result?.ok) throw new Error(result?.error || "Save failed");
    return "saved";
  }
  if (typeof window.showSaveFilePicker === "function") {
    const handle = await window.showSaveFilePicker({
      suggestedName: filename,
      types: [{
        description: "Excel",
        accept: { "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"] },
      }],
    });
    const writable = await handle.createWritable();
    await writable.write(blob);
    await writable.close();
    return "saved";
  }
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
  return "downloaded";
}

async function exportClientsExcel() {
  try {
    const params = new URLSearchParams({ lang: state.lang });
    if (state.clientsSearch) params.set("q", state.clientsSearch);
    if (state.clientsGroupFilter && state.clientsGroupFilter !== "all") {
      params.set("group", state.clientsGroupFilter);
    }
    if (state.clientsAccountFilter && state.clientsAccountFilter !== "all") {
      params.set("account", state.clientsAccountFilter);
    }
    const res = await fetch(`/api/export/clients.xlsx?${params.toString()}`);
    if (!res.ok) throw new Error(await res.text());
    const blob = await res.blob();
    const disposition = res.headers.get("Content-Disposition") || "";
    const match = disposition.match(/filename="([^"]+)"/);
    const filename = match ? match[1] : `CheckItNow-clients-${new Date().toISOString().slice(0, 10)}.xlsx`;
    const outcome = await saveExportBlob(blob, filename);
    if (outcome === "cancelled") {
      showToast(t("export_excel_cancelled"));
      return;
    }
    showToast(t("export_excel_done"));
  } catch (err) {
    if (err?.name === "AbortError") {
      showToast(t("export_excel_cancelled"));
      return;
    }
    showToast(err.message || "Export failed");
  }
}

async function loadClientsTable() {
  try {
    const params = new URLSearchParams({ lang: state.lang });
    if (state.clientsSearch) params.set("q", state.clientsSearch);
    if (state.clientsGroupFilter && state.clientsGroupFilter !== "all") {
      params.set("group", state.clientsGroupFilter);
    }
    if (state.clientsAccountFilter && state.clientsAccountFilter !== "all") {
      params.set("account", state.clientsAccountFilter);
    }
    const data = await api(`/api/lists/clients?${params.toString()}`);
    state.clientsRows = data.rows || [];
    state.clientsGroups = data.groups || [];
    state.clientsTotal = data.total || state.clientsRows.length;
    renderClientsFilters(data);
    renderClientsTableRows();
    if (state.clientsSelectedId && !state.clientsRows.some((row) => row.id === state.clientsSelectedId)) {
      closeClientDetailPanel();
    }
  } catch (err) {
    showToast(err.message);
    $("#clients-tbody").innerHTML = `<tr><td colspan="11" class="empty-caption">${escapeHtml(err.message)}</td></tr>`;
  }
}

function renderClientsFilters(data) {
  const countEl = $("#clients-filter-count");
  if (countEl) {
    countEl.textContent = t("clients_filtered", {
      n: data.filtered ?? state.clientsRows.length,
      total: data.total ?? state.clientsTotal,
    });
  }

  const groupSel = $("#clients-group-filter");
  const groups = data.groups || state.clientsGroups || [];
  groupSel.innerHTML = [
    `<option value="all">${escapeHtml(t("clients_group_all"))}</option>`,
    `<option value="__none__">${escapeHtml(t("clients_group_none"))}</option>`,
    ...groups.map((g) => `<option value="${escapeHtml(g)}">${escapeHtml(g)}</option>`),
  ].join("");
  groupSel.value = state.clientsGroupFilter;

  const accountSel = $("#clients-account-filter");
  if (accountSel) {
    accountSel.innerHTML = [
      `<option value="all">${escapeHtml(t("clients_account_all"))}</option>`,
      `<option value="active">${escapeHtml(t("clients_account_active"))}</option>`,
      `<option value="closed">${escapeHtml(t("clients_account_closed"))}</option>`,
    ].join("");
    accountSel.value = state.clientsAccountFilter;
  }

  const pickSel = $("#clients-quick-pick");
  pickSel.innerHTML = [
    `<option value="">${escapeHtml(t("clients_pick_placeholder"))}</option>`,
    ...state.clientsRows.map((row) => {
      const nums = row.client_numbers && row.client_numbers !== "—" ? ` · ${row.client_numbers}` : "";
      const grp = row.group && row.group !== "—" ? ` [${row.group}]` : "";
      return `<option value="${row.id}">${escapeHtml(`${row.client_name}${grp}${nums}`)}</option>`;
    }),
  ].join("");
  if (state.clientsSelectedId) pickSel.value = state.clientsSelectedId;

  const datalist = $("#group-suggestions");
  if (datalist) {
    datalist.innerHTML = groups.map((g) => `<option value="${escapeHtml(g)}"></option>`).join("");
  }
}

function renderClientsTableRows() {
  const cols = ["group", "client_numbers", "client_name", "contact_name", "client_email", "mode_label", "detail", "end_date", "next", "status"];
  const headers = ["col_group", "col_client_no", "col_client", "col_contact", "col_email", "col_mode", "col_detail", "col_end", "col_next", "col_status", "col_actions"];
  $("#clients-thead").innerHTML = `<tr>${headers.map((h) => `<th>${escapeHtml(t(h))}</th>`).join("")}</tr>`;
  if (!state.clientsRows.length) {
    $("#clients-tbody").innerHTML = `<tr><td colspan="11" class="empty-caption">${escapeHtml(t("no_trackers"))}</td></tr>`;
    return;
  }
  $("#clients-tbody").innerHTML = state.clientsRows.map((row) => `
    <tr class="clients-row${row.id === state.clientsSelectedId ? " selected" : ""}${row.is_closed ? " clients-row--closed" : ""}" data-id="${row.id}">
      ${cols.map((k) => `<td>${escapeHtml(row[k] || "—")}</td>`).join("")}
      <td class="clients-row-actions">
        ${accountStatusBtnHtml(row, true)}
        <button type="button" class="btn btn-secondary btn-xs btn-client-edit" data-id="${row.id}">${escapeHtml(t("edit_client_btn"))}</button>
        ${!row.is_closed && row.mode === "milestone" ? `<button type="button" class="btn btn-secondary btn-xs btn-schedule-edit" data-id="${row.id}">${escapeHtml(tableActionLabel("schedule_edit_btn", "schedule_edit_btn_short"))}</button>` : ""}
        ${!row.is_closed ? `<button type="button" class="btn btn-primary btn-xs btn-compose-open" data-id="${row.id}">${escapeHtml(tableActionLabel("open_compose", "open_compose_short"))}</button>` : ""}
        ${!row.is_closed && row.needs_alert ? `<button type="button" class="btn btn-secondary btn-xs btn-renew" data-id="${row.id}">${escapeHtml(tableActionLabel("btn_renew", "btn_renew_short"))}</button>` : ""}
      </td>
    </tr>`).join("");
  $("#clients-tbody").querySelectorAll(".clients-row").forEach((tr) => {
    tr.addEventListener("click", (e) => {
      if (e.target.closest("button")) return;
      selectClientRow(tr.dataset.id);
    });
  });
  bindCardActions($("#clients-table"));
}

async function selectClientRow(clientId) {
  if (!clientId) return;
  state.clientsSelectedId = clientId;
  const pickSel = $("#clients-quick-pick");
  if (pickSel) pickSel.value = clientId;
  $("#clients-tbody").querySelectorAll(".clients-row").forEach((tr) => {
    tr.classList.toggle("selected", tr.dataset.id === clientId);
  });
  await openClientDetailPanel();
}

async function openClientDetailPanel() {
  const body = $("#clients-detail-body");
  if (!body || !state.clientsSelectedId) return;
  openClientDetailPanelShell();
  body.innerHTML = `<p class="clients-detail-empty">...</p>`;
  try {
    const c = await api(`/api/clients/${state.clientsSelectedId}?lang=${state.lang}`);
    body.innerHTML = `
      <div class="clients-detail-row"><span class="field-lbl">${escapeHtml(t("col_client"))}</span><strong>${escapeHtml(c.client_name)}</strong></div>
      <div class="clients-detail-row"><span class="field-lbl">${escapeHtml(t("client_group"))}</span><span>${escapeHtml(c.group || "—")}</span></div>
      <div class="clients-detail-row"><span class="field-lbl">${escapeHtml(t("client_numbers"))}</span>${renderClientNumbersHtml(c.client_numbers)}</div>
      <div class="clients-detail-row"><span class="field-lbl">${escapeHtml(t("col_contact"))}</span><span>${escapeHtml(c.contact_name || "—")}</span></div>
      <div class="clients-detail-row"><span class="field-lbl">${escapeHtml(t("col_email"))}</span><span>${escapeHtml(c.client_email || "—")}</span></div>
      <div class="clients-detail-row"><span class="field-lbl">${escapeHtml(t("service_label"))}</span><span>${escapeHtml(c.service_label || "—")}</span></div>
      <div class="clients-detail-row"><span class="field-lbl">${escapeHtml(t("col_mode"))}</span><span>${escapeHtml(c.mode_label || "—")}</span></div>
      <div class="clients-detail-row"><span class="field-lbl">${escapeHtml(t("col_end"))}</span><span>${escapeHtml(c.end_date || "—")}</span></div>
      <div class="clients-detail-row"><span class="field-lbl">${escapeHtml(c.next_label || t("col_next"))}</span><span>${escapeHtml(c.next_display || "—")}</span></div>
      <div class="clients-detail-row"><span class="field-lbl">${escapeHtml(t("col_status"))}</span><span class="${statusClass(c.status_tier)}">${escapeHtml(c.status_label || "—")}</span></div>
      ${c.is_closed && c.closed_at ? `<div class="clients-detail-row"><span class="field-lbl">${escapeHtml(t("status_closed"))}</span><span>${escapeHtml(c.closed_at)}</span></div>` : ""}
      <div class="clients-detail-actions">
        ${accountStatusBtnHtml(c)}
        ${!c.is_closed ? `<button type="button" class="btn btn-secondary btn-xs btn-client-edit" data-id="${c.id}">${escapeHtml(t("edit_client_btn"))}</button>` : ""}
        ${!c.is_closed && c.mode === "milestone" ? `<button type="button" class="btn btn-secondary btn-xs btn-schedule-edit" data-id="${c.id}">${escapeHtml(t("schedule_edit_btn"))}</button>` : ""}
        ${!c.is_closed ? `<button type="button" class="btn btn-primary btn-xs btn-compose-open" data-id="${c.id}">${escapeHtml(t("open_compose"))}</button>` : ""}
      </div>`;
    bindCardActions(body);
  } catch (err) {
    body.innerHTML = `<p class="clients-detail-empty">${escapeHtml(err.message)}</p>`;
  }
}

let clientsSearchTimer = null;

async function loadMilestoneQueue() {
  try {
    const data = await api(`/api/lists/milestones?lang=${state.lang}`);
  const pending = $("#ms-pending-list");
  const completed = $("#ms-completed-list");

  pending.innerHTML = data.pending.length
    ? data.pending.map((c) => `
      <div class="ms-queue-row">
        <div class="ms-queue-head">
          <div>
            <strong>${escapeHtml(c.client_name)}</strong>
            <div class="field-val-muted">${escapeHtml(c.service_label)}</div>
            <div class="snooze-note">${escapeHtml(t("ms_next"))}: ${escapeHtml(c.next_milestone_label)} · ${escapeHtml(c.milestone_progress)}</div>
          </div>
          <span class="${statusClass(c.status_tier)}">${escapeHtml(c.status_label)}</span>
        </div>
        ${milestoneQueueActionsHtml(c)}
      </div>`).join("")
    : `<p class="empty-caption">${escapeHtml(t("ms_queue_empty"))}</p>`;
  bindCardActions(pending);

  completed.innerHTML = data.completed.length
    ? data.completed.map((c) => `
      <div class="ms-completed-card">
        <div class="ms-queue-head">
          <div>
            <strong>${escapeHtml(c.client_name)}</strong>
            <div class="field-val-muted">${escapeHtml(c.service_label)}</div>
          </div>
          <span class="status-pill status-pill--healthy">${escapeHtml(t("ms_all_complete"))}</span>
        </div>
        <pre class="ms-history">${escapeHtml(c.milestone_history || "")}</pre>
        <div class="card-actions">
          <button type="button" class="btn btn-primary btn-xs btn-compose-open" data-id="${c.id}">${escapeHtml(t("open_compose"))}</button>
          <button type="button" class="btn btn-secondary btn-xs btn-renew" data-id="${c.id}">${escapeHtml(t("btn_renew"))}</button>
        </div>
      </div>`).join("")
    : `<p class="empty-caption">${escapeHtml(t("ms_completed_empty"))}</p>`;
    bindCardActions(completed);
  } catch (err) {
    showToast(err.message);
    $("#ms-pending-list").innerHTML = `<p class="empty-caption">${escapeHtml(err.message)}</p>`;
    $("#ms-completed-list").innerHTML = "";
  }
}

async function loadComposeDetail() {
  if (!state.composeClientId) return;
  const c = await api(`/api/clients/${state.composeClientId}?lang=${state.lang}`);
  let snoozeHtml = c.alert_snoozed
    ? `<div class="snooze-note">${escapeHtml(t("alert_snoozed"))}${c.alert_snoozed_until ? ` · ${escapeHtml(c.alert_snoozed_until)}` : ""}</div>`
    : "";
  let actionsHtml = c.needs_alert || c.alert_snoozed
    ? `<div class="card-actions">
        <button type="button" class="btn btn-secondary btn-xs btn-renew" data-id="${c.id}">${escapeHtml(t("btn_renew"))}</button>
        <button type="button" class="btn btn-secondary btn-xs btn-dismiss" data-id="${c.id}">${escapeHtml(t("btn_dismiss_alert"))}</button>
      </div>`
    : "";
  $("#compose-meta").innerHTML = `
    ${snoozeHtml}
    <span class="${statusClass(c.status_tier)}">${escapeHtml(c.status_label)}</span>
    <span class="field-val" style="margin-left:0.5rem">${escapeHtml(c.days_display)}</span>
    ${lastReminderHtml(c)}
    <div class="compose-next">
      <div class="field-lbl">${escapeHtml(c.next_label)}</div>
      <div class="field-val">${escapeHtml(c.next_display)}</div>
    </div>
    ${actionsHtml}`;
  bindCardActions($("#compose-meta"));

  const tracker = $("#milestone-tracker");
  if (c.mode === "milestone" && c.milestone_all_complete) {
    tracker.classList.remove("hidden");
    tracker.innerHTML = `
      <div class="ms-complete-banner">
        <strong>${escapeHtml(t("ms_all_complete"))}</strong>
        <div class="field-lbl">${escapeHtml(t("ms_complete_summary"))}</div>
        <pre class="ms-history">${escapeHtml(c.milestone_history || "")}</pre>
      </div>`;
    return;
  }
  if (c.mode === "milestone" && c.milestone_rows) {
    tracker.classList.remove("hidden");
    tracker.innerHTML = `<div class="field-lbl">${escapeHtml(t("progress_tracker"))}</div>` +
      c.milestone_rows.map((row) => {
        const planned = row.planned ? `<div class="ms-row-planned">${escapeHtml(row.planned)}</div>` : "";
        if (row.done) {
          return `<div class="ms-row ms-row--done">✅ ${escapeHtml(row.label)} — ${escapeHtml(row.completed || row.date || "")}${planned}</div>`;
        }
        if (row.is_locked) {
          return `<div class="ms-row ms-row--locked">○ ${escapeHtml(row.label)}${planned}</div>`;
        }
        if (row.is_next) {
          return `<label class="ms-row"><input type="checkbox" data-ms-index="${row.index}" /> ${escapeHtml(row.label)}${planned}</label>`;
        }
        return "";
      }).join("");
    tracker.querySelectorAll("input[type=checkbox]").forEach((chk) => {
      chk.addEventListener("change", async (e) => {
        const index = parseInt(e.target.dataset.msIndex, 10);
        await api(`/api/clients/${state.composeClientId}/milestone?lang=${state.lang}`, {
          method: "POST",
          body: JSON.stringify({ index, checked: e.target.checked }),
        });
        await refreshAll();
      });
    });
  } else {
    tracker.classList.add("hidden");
    tracker.innerHTML = "";
  }
}

async function loadReminder() {
  if (!state.composeClientId) return;
  const data = await api(
    `/api/reminder/${state.composeClientId}?lang=${state.lang}&channel=${state.channel}&payment=${state.payment}`
  );
  $("#compose-message").value = data.message;
  const mailBtn = $("#btn-mailto");
  if (state.channel === "email" && data.mailto) {
    mailBtn.href = data.mailto;
    mailBtn.classList.remove("hidden");
  } else {
    mailBtn.classList.add("hidden");
  }
}

async function loadDashboard() {
  state.dashboard = await api(`/api/dashboard?lang=${state.lang}&filter=${state.filter}`);
  state.filter = state.dashboard.filter;
  renderKpi();
  renderAlertBanner();
  renderPriority();
  renderBoard();
  if (!state.dashboard.alert_banner && state.dashboard.priority?.length) {
    console.warn("alert_banner missing — restart server for v1.3.0+");
  }
  await refreshComposeClients();
}

async function refreshComposeClients() {
  const all = await api(`/api/dashboard?lang=${state.lang}&filter=all`);
  const sel = $("#compose-client");
  sel.innerHTML = all.clients.map((c) =>
    `<option value="${c.id}">${escapeHtml(c.client_name)}</option>`
  ).join("");
  if (!state.composeClientId || !all.clients.some((c) => c.id === state.composeClientId)) {
    state.composeClientId = all.clients[0]?.id || null;
  }
  if (state.composeClientId) sel.value = state.composeClientId;
}

async function refreshAll() {
  await loadDashboard();
  if (state.view === "clients") await loadClientsTable();
  if (state.view === "milestones") await loadMilestoneQueue();
  await loadComposeDetail();
  await loadReminder();
}

async function openSettings() {
  const [lan, backup, about, appSettings, activity, notifyStatus, collabCfg] = await Promise.all([
    api("/api/lan-access"),
    api("/api/backup"),
    api("/api/about"),
    api("/api/app-settings"),
    api(`/api/activity?limit=40&lang=${state.lang}`),
    api(`/api/notifications/status?lang=${state.lang}`),
    api("/api/collab"),
  ]);
  state.lanAccess = lan;
  state.backup = backup;
  state.about = about;
  state.appSettings = appSettings;
  renderAboutPanel(about);
  renderDataPathPanel(appSettings);
  renderCollabSettingsPanel(collabCfg, state.session);
  renderNotifySettingsPanel(appSettings, notifyStatus);
  renderSampleSettingsPanel(appSettings);
  renderActivityPanel(activity);
  renderLanSettingsPanel(lan);
  renderBackupPanel(backup);
  $("#modal-settings").showModal();
}

function hasDesktopFolderPicker() {
  return !!window.pywebview?.api?.pick_data_folder;
}

function configureDataPathUi() {
  const desktop = hasDesktopFolderPicker();
  const input = $("#data-path-input");
  input.readOnly = desktop;
  $("#btn-data-path-apply").classList.toggle("hidden", desktop);
}

function renderDataPathPanel(settings) {
  const input = $("#data-path-input");
  const configured = settings?.data_path || "";
  const effective = settings?.data_path_effective || settings?.data_path_default || "";
  input.value = configured;
  input.placeholder = effective;
  configureDataPathUi();
  const statusEl = $("#data-path-status");
  const lines = [t("data_path_status_effective", { path: effective })];
  if (settings?.data_path_pending_restart && configured) {
    lines.push(t("data_path_status_configured", { path: configured }));
  }
  statusEl.textContent = lines.join(" · ");
  $("#data-path-restart-hint").classList.toggle(
    "hidden",
    !(settings?.data_path_pending_restart || settings?.data_path_changed),
  );
  if (!$("#data-path-restart-hint").classList.contains("hidden")) {
    $("#data-path-restart-hint").textContent = t("data_path_restart_hint");
  }
}

async function saveDataPath(rawPath) {
  const data = await patchAppSettings({ data_path: rawPath });
  renderDataPathPanel(data);
  showToast(t("data_path_saved"));
  if (data.data_path_pending_restart) {
    $("#data-path-restart-hint").textContent = t("data_path_restart_hint");
    $("#data-path-restart-hint").classList.remove("hidden");
  }
}

async function browseDataPathFolder() {
  const apiNative = window.pywebview?.api;
  if (apiNative?.pick_data_folder) {
    const initial = $("#data-path-input").value.trim()
      || state.appSettings?.data_path_effective
      || "";
    try {
      const result = await apiNative.pick_data_folder(initial);
      if (result?.cancelled) {
        showToast(t("data_path_cancelled"));
        return;
      }
      if (!result?.ok || !result.path) {
        throw new Error(result?.error || "Folder picker failed");
      }
      await saveDataPath(result.path);
    } catch (err) {
      showToast(err.message || "Error");
    }
    return;
  }
  showToast(t("data_path_browser_hint"));
  const input = $("#data-path-input");
  input.readOnly = false;
  $("#btn-data-path-apply").classList.remove("hidden");
  input.focus();
}

async function applyDataPathFromInput() {
  const raw = $("#data-path-input").value.trim();
  if (!raw) {
    showToast(t("data_path_status_effective", { path: state.appSettings?.data_path_default || "" }));
    return;
  }
  try {
    await saveDataPath(raw);
  } catch (err) {
    showToast(err.message || "Error");
  }
}

async function resetDataPathToDefault() {
  if (state.appSettings?.data_path && !window.confirm(t("data_path_default_confirm"))) {
    return;
  }
  try {
    await saveDataPath("");
  } catch (err) {
    showToast(err.message || "Error");
  }
}

function renderAboutPanel(data) {
  $("#about-version").textContent = t("about_version", { version: data?.version || "—" });
  const tagline = data?.tagline || "";
  const taglineEl = $("#about-tagline");
  taglineEl.textContent = tagline ? t("about_tagline", { tagline }) : "";
  taglineEl.classList.toggle("hidden", !tagline);
  const footer = data?.footer || "";
  const footerEl = $("#about-footer");
  footerEl.textContent = footer;
  footerEl.classList.toggle("hidden", !footer);
}

function renderNotifySettingsPanel(settings, status) {
  $("#notify-enabled").checked = !!settings?.desktop_notifications;
  const preview = $("#notify-preview");
  const counts = status?.counts || {};
  const hasAlerts = (counts.expired || 0) + (counts.urgent || 0) + (counts.priority || 0) > 0;
  if (hasAlerts && status?.preview_body) {
    preview.textContent = `${status.preview_title}: ${status.preview_body}`;
    preview.classList.remove("hidden");
  } else {
    preview.classList.add("hidden");
  }
}

function renderSampleSettingsPanel(settings) {
  $("#sample-seed-enabled").checked = !!settings?.seed_sample_data;
  $("#sample-client-count").textContent = t("sample_client_count", { n: settings?.client_count || 0 });
}

function formatActivityTime(iso) {
  if (!iso) return "";
  try {
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return iso;
    const locale = state.lang === "en" ? "en-GB" : state.lang === "zh_cn" ? "zh-CN" : "zh-TW";
    if (state.lang === "zh" || state.lang === "zh_cn") {
      const datePart = d.toLocaleDateString(locale, { month: "numeric", day: "numeric" });
      const timePart = d.toLocaleTimeString(locale, { hour: "2-digit", minute: "2-digit", hour12: false });
      return `${datePart} ${timePart}`;
    }
    return d.toLocaleString(locale, {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return iso;
  }
}

function renderActivityPanel(data) {
  const list = $("#activity-list");
  const items = data?.items || [];
  if (!items.length) {
    list.innerHTML = `<li class="activity-empty">${escapeHtml(t("activity_empty"))}</li>`;
    return;
  }
  list.innerHTML = items.map((entry) => `
    <li class="activity-item">
      <span class="activity-time">${escapeHtml(formatActivityTime(entry.at))}</span>
      <span class="activity-label">${escapeHtml(entry.label || entry.action || "")}</span>
    </li>`).join("");
}

async function patchAppSettings(patch) {
  const data = await api("/api/app-settings", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(patch),
  });
  state.appSettings = data;
  renderSampleSettingsPanel(data);
  renderDataPathPanel(data);
  return data;
}

async function loadSampleData() {
  if (!window.confirm(t("sample_load_confirm"))) return;
  try {
    const res = await api(`/api/sample-data/load?lang=${state.lang}`, { method: "POST" });
    showToast(res.message || t("sample_loaded", { n: res.count || 0 }));
    state.appSettings = await api("/api/app-settings");
    renderSampleSettingsPanel(state.appSettings);
    const activity = await api(`/api/activity?limit=40&lang=${state.lang}`);
    renderActivityPanel(activity);
    await refreshAll();
  } catch (err) {
    showToast(err.message || "Error");
  }
}

async function clearSampleData() {
  if (!window.confirm(t("sample_clear_confirm"))) return;
  try {
    const res = await api(`/api/sample-data/clear?lang=${state.lang}`, { method: "POST" });
    showToast(res.message || t("sample_cleared"));
    state.appSettings = await api("/api/app-settings");
    renderSampleSettingsPanel(state.appSettings);
    const activity = await api(`/api/activity?limit=40&lang=${state.lang}`);
    renderActivityPanel(activity);
    await refreshAll();
  } catch (err) {
    showToast(err.message || "Error");
  }
}

function renderBackupPanel(data) {
  const retention = data?.retention_days || 45;
  const recentKeep = data?.recent_keep || 8;
  $("#backup-settings-desc").textContent = t("backup_desc", { n: retention, r: recentKeep });
  const statusEl = $("#backup-settings-status");
  const restoreBtn = $("#btn-backup-restore");
  const restoreSelectedBtn = $("#btn-backup-restore-selected");
  const pickSel = $("#backup-pick");
  const backups = data?.backups || [];
  if (data?.latest_backup_at) {
    statusEl.textContent = t("backup_status_ok", {
      at: data.latest_backup_at,
      daily: data.daily_count || 0,
      recent: data.recent_count || 0,
    });
    restoreBtn.disabled = false;
  } else {
    statusEl.textContent = t("backup_status_empty");
    restoreBtn.disabled = true;
  }
  if (!backups.length) {
    pickSel.innerHTML = `<option value="">${escapeHtml(t("backup_status_empty"))}</option>`;
    pickSel.disabled = true;
    restoreSelectedBtn.disabled = true;
    return;
  }
  pickSel.disabled = false;
  pickSel.innerHTML = backups.map((item) => {
    const kind = item.kind === "daily" ? t("backup_kind_daily") : t("backup_kind_recent");
    const label = `${item.saved_at} · ${kind} · ${item.name}`;
    return `<option value="${escapeHtml(item.name)}">${escapeHtml(label)}</option>`;
  }).join("");
  restoreSelectedBtn.disabled = false;
}

async function restoreBackupByName(name, confirmKey, confirmArgs) {
  const args = confirmArgs || {};
  if (!window.confirm(t(confirmKey, args))) return;
  try {
    const res = await api(`/api/backup/restore?lang=${state.lang}`, {
      method: "POST",
      body: JSON.stringify({ name: name || "" }),
    });
    state.backup = res.backup;
    renderBackupPanel(res.backup);
    showToast(res.message || t("backup_restore_done", { name: name || res.backup?.latest_backup_name || "" }));
    const activity = await api(`/api/activity?limit=40&lang=${state.lang}`);
    renderActivityPanel(activity);
    await refreshAll();
  } catch (err) {
    showToast(err.message || t("backup_restore_none"));
  }
}

async function restoreLatestBackup() {
  await restoreBackupByName("", "backup_restore_confirm");
}

async function restoreSelectedBackup() {
  const name = $("#backup-pick")?.value || "";
  if (!name) {
    showToast(t("backup_restore_none"));
    return;
  }
  const backups = state.backup?.backups || [];
  const item = backups.find((row) => row.name === name);
  await restoreBackupByName(
    name,
    "backup_restore_selected_confirm",
    { at: item?.saved_at || name, name },
  );
}

async function downloadImportTemplate() {
  const res = await fetch(`/api/import/clients-template.xlsx?lang=${state.lang}`);
  if (!res.ok) throw new Error(await res.text());
  const blob = await res.blob();
  const disposition = res.headers.get("Content-Disposition") || "";
  const match = disposition.match(/filename="([^"]+)"/);
  const filename = match ? match[1] : "CheckItNow-import-template.xlsx";
  const outcome = await saveExportBlob(blob, filename);
  if (outcome === "cancelled") {
    showToast(t("export_excel_cancelled"));
    return;
  }
  showToast(t("import_template_done"));
}

async function importExcelFile(file) {
  if (!file) return;
  const replace = !!$("#import-replace-enabled")?.checked;
  if (replace && !window.confirm(t("import_excel_confirm_replace"))) return;
  const form = new FormData();
  form.append("file", file);
  const params = new URLSearchParams({
    lang: state.lang,
    mode: replace ? "replace" : "append",
  });
  const token = sessionStorage.getItem(SESSION_KEY);
  const headers = {};
  if (token) headers["X-Session-Token"] = token;
  const res = await fetch(`/api/import/clients?${params.toString()}`, {
    method: "POST",
    headers,
    body: form,
  });
  const payload = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(payload.detail || res.statusText);
  }
  const statusEl = $("#import-excel-status");
  statusEl.textContent = payload.message || t("import_excel_done", {
    n: payload.imported || 0,
    skipped: payload.skipped || 0,
  });
  statusEl.classList.remove("hidden");
  if ((payload.errors || []).length) {
    statusEl.textContent += ` ${t("import_excel_errors")}`;
  }
  showToast(payload.message || t("import_excel_done", {
    n: payload.imported || 0,
    skipped: payload.skipped || 0,
  }));
  state.appSettings = await api("/api/app-settings");
  renderSampleSettingsPanel(state.appSettings);
  const activity = await api(`/api/activity?limit=40&lang=${state.lang}`);
  renderActivityPanel(activity);
  await refreshAll();
}

function renderLanSettingsPanel(data) {
  const toggle = $("#lan-enabled");
  toggle.checked = !!data.enabled;
  toggle.disabled = !data.can_enable && !data.enabled;
  $("#lan-no-ip").classList.toggle("hidden", data.can_enable || data.enabled);
  const showQr = data.enabled && data.url;
  $("#lan-qr-panel").classList.toggle("hidden", !showQr);
  if (showQr) {
    $("#lan-url-text").textContent = data.url;
    $("#lan-qr-img").src = `${data.qr_path || "/api/lan-access/qr.svg"}?t=${Date.now()}`;
  }
}

async function setLanAccess(enabled) {
  const data = await api("/api/lan-access", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ enabled }),
  });
  state.lanAccess = data;
  renderLanSettingsPanel(data);
  showToast(t(enabled ? "lan_enabled_toast" : "lan_disabled_toast"));
}

async function openManage() {
  const all = await api(`/api/dashboard?lang=${state.lang}&filter=all`);
  const list = $("#manage-list");
  list.innerHTML = all.clients.map((c) => `
    <div class="manage-item">
      <div>
        <strong>${escapeHtml(c.client_name)}</strong>
        <div class="field-val-muted">${escapeHtml(c.service_label)}</div>
      </div>
      <div class="manage-item-actions">
        ${accountStatusBtnHtml(c)}
        <button type="button" class="btn btn-secondary btn-xs btn-client-edit" data-id="${c.id}">${escapeHtml(t("edit_client_btn"))}</button>
        ${!c.is_closed && c.mode === "milestone" ? `<button type="button" class="btn btn-secondary btn-xs btn-schedule-edit" data-id="${c.id}">${escapeHtml(t("schedule_edit_btn"))}</button>` : ""}
        <button type="button" class="btn btn-secondary btn-del" data-id="${c.id}">${escapeHtml(t("del"))}</button>
      </div>
    </div>`).join("") || `<p class="empty-caption">${escapeHtml(t("no_trackers"))}</p>`;
  list.querySelectorAll(".btn-del").forEach((btn) => {
    btn.addEventListener("click", async () => {
      await api(`/api/clients/${btn.dataset.id}`, { method: "DELETE" });
      await refreshAll();
      await openManage();
    });
  });
  bindCardActions(list);
  $("#modal-manage").showModal();
}

function bindEvents() {
  const bind = (sel, event, handler) => {
    const el = $(sel);
    if (el) el.addEventListener(event, handler);
  };
  bind("#form-login", "submit", submitLogin);
  bind("#btn-collab-demote", "click", demoteToViewer);
  bind("#btn-collab-promote", "click", promoteToEditor);
  bind("#btn-collab-logout", "click", logoutSession);
  bind("#collab-enabled", "change", async (e) => {
    try {
      await setCollabEnabled(e.target.checked);
    } catch (err) {
      e.target.checked = !e.target.checked;
      showToast(err.message || "Error");
    }
  });
  $("#btn-collab-test-window").addEventListener("click", () => {
    window.open(window.location.href, "_blank", "noopener,noreferrer");
  });
  $("#btn-collab-force-unlock").addEventListener("click", forceUnlockCollab);
  bind("#form-change-password", "submit", submitChangePassword);
  bind("#form-admin-reset-password", "submit", submitAdminResetPassword);
  $("#btn-add").addEventListener("click", () => {
    $("#add-end").value = state.meta.today;
    $("#add-schedule-first").value = state.meta.today;
    renderScheduleRows([state.meta.today]);
    toggleAddModeUi();
    $("#modal-add").showModal();
  });
  $("#btn-add-cancel").addEventListener("click", () => $("#modal-add").close());
  $("#btn-settings").addEventListener("click", openSettings);
  $("#btn-settings-close").addEventListener("click", () => $("#modal-settings").close());
  $("#btn-data-path-browse").addEventListener("click", browseDataPathFolder);
  $("#btn-data-path-apply").addEventListener("click", applyDataPathFromInput);
  $("#btn-data-path-default").addEventListener("click", resetDataPathToDefault);
  $("#btn-manage").addEventListener("click", openManage);
  $("#btn-manage-close").addEventListener("click", () => $("#modal-manage").close());
  $("#lan-enabled").addEventListener("change", async (e) => {
    try {
      await setLanAccess(e.target.checked);
    } catch (err) {
      e.target.checked = !e.target.checked;
      showToast(err.message || "Error");
    }
  });
  $("#btn-lan-copy").addEventListener("click", async () => {
    const url = state.lanAccess?.url || $("#lan-url-text").textContent;
    if (!url) return;
    try {
      await navigator.clipboard.writeText(url);
      showToast(t("lan_url_copied"));
    } catch {
      showToast(url);
    }
  });
  $("#btn-backup-restore").addEventListener("click", restoreLatestBackup);
  $("#btn-backup-restore-selected").addEventListener("click", restoreSelectedBackup);
  $("#btn-import-template").addEventListener("click", async () => {
    try {
      await downloadImportTemplate();
    } catch (err) {
      if (err?.name === "AbortError") {
        showToast(t("export_excel_cancelled"));
        return;
      }
      showToast(err.message || "Error");
    }
  });
  $("#btn-import-excel").addEventListener("click", () => $("#import-excel-file").click());
  $("#import-excel-file").addEventListener("change", async (e) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;
    try {
      await importExcelFile(file);
    } catch (err) {
      showToast(err.message || t("import_excel_none"));
    }
  });
  $("#notify-enabled").addEventListener("change", async (e) => {
    try {
      await patchAppSettings({ desktop_notifications: e.target.checked });
    } catch (err) {
      e.target.checked = !e.target.checked;
      showToast(err.message || "Error");
    }
  });
  $("#sample-seed-enabled").addEventListener("change", async (e) => {
    try {
      await patchAppSettings({ seed_sample_data: e.target.checked });
    } catch (err) {
      e.target.checked = !e.target.checked;
      showToast(err.message || "Error");
    }
  });
  $("#btn-sample-load").addEventListener("click", loadSampleData);
  $("#btn-sample-clear").addEventListener("click", clearSampleData);
  $("#btn-renew-cancel").addEventListener("click", () => $("#modal-renew").close());
  $("#btn-renew-close-client").addEventListener("click", async () => {
    if (!state.renewClientId) return;
    await closeClientAccount(state.renewClientId);
  });
  $("#form-renew").addEventListener("submit", submitRenew);
  $("#btn-edit-cancel").addEventListener("click", () => $("#modal-edit-client").close());
  $("#form-edit-client").addEventListener("submit", submitClientEdit);
  $("#clients-search").addEventListener("input", (e) => {
    clearTimeout(clientsSearchTimer);
    clientsSearchTimer = setTimeout(() => {
      state.clientsSearch = e.target.value.trim();
      loadClientsTable();
    }, 250);
  });
  $("#clients-group-filter").addEventListener("change", (e) => {
    state.clientsGroupFilter = e.target.value;
    loadClientsTable();
  });
  $("#clients-account-filter").addEventListener("change", (e) => {
    state.clientsAccountFilter = e.target.value;
    loadClientsTable();
  });
  $("#clients-quick-pick").addEventListener("change", (e) => {
    if (!e.target.value) return;
    selectClientRow(e.target.value);
  });
  $("#btn-export-excel").addEventListener("click", exportClientsExcel);
  $("#btn-client-detail-close").addEventListener("click", closeClientDetailPanel);
  $("#clients-detail-backdrop").addEventListener("click", closeClientDetailPanel);
  $("#btn-schedule-cancel").addEventListener("click", () => $("#modal-schedule").close());
  $("#form-schedule").addEventListener("submit", submitScheduleEdit);
  $("#btn-edit-schedule-10w1").addEventListener("click", () => applyEditQuickFill(10, 7, null));
  $("#btn-edit-schedule-8w2").addEventListener("click", () => applyEditQuickFill(8, 14, null));
  $("#btn-edit-schedule-4x3").addEventListener("click", () => applyEditQuickFill(4, null, 3));
  $("#btn-edit-schedule-2x6").addEventListener("click", () => applyEditQuickFill(2, null, 6));
  $("#btn-edit-schedule-add").addEventListener("click", () => {
    const pending = [...document.querySelectorAll("#edit-schedule-rows .schedule-date")].map((inp) => inp.value);
    pending.push("");
    renderEditScheduleRows([
      ...state.scheduleEditDoneRows,
      ...pending.map((planned, i) => ({
        done: false,
        label: t("schedule_visit_n", { n: state.scheduleEditLocked.length + i + 1 }),
        planned,
      })),
    ]);
  });

  document.querySelectorAll(".nav-tab").forEach((tab) => {
    tab.addEventListener("click", async () => {
      const view = tab.dataset.view;
      switchView(view);
      if (view === "clients") {
        closeClientDetailPanel();
        await loadClientsTable();
      }
      if (view === "milestones") await loadMilestoneQueue();
      if (view === "dashboard") await loadDashboard();
    });
  });

  $("#add-mode").addEventListener("change", toggleAddModeUi);

  $("#btn-schedule-10w1").addEventListener("click", () => {
    const first = $("#add-schedule-first").value;
    if (!first) return showToast(t("err_schedule"));
    renderScheduleRows(buildScheduleFromFirstDays(first, 10, 7));
  });
  $("#btn-schedule-8w2").addEventListener("click", () => {
    const first = $("#add-schedule-first").value;
    if (!first) return showToast(t("err_schedule"));
    renderScheduleRows(buildScheduleFromFirstDays(first, 8, 14));
  });
  $("#btn-schedule-4x3").addEventListener("click", () => {
    const first = $("#add-schedule-first").value;
    if (!first) return showToast(t("err_schedule"));
    renderScheduleRows(buildScheduleFromFirst(first, 4, 3));
  });
  $("#btn-schedule-2x6").addEventListener("click", () => {
    const first = $("#add-schedule-first").value;
    if (!first) return showToast(t("err_schedule"));
    renderScheduleRows(buildScheduleFromFirst(first, 2, 6));
  });
  $("#btn-schedule-add").addEventListener("click", () => {
    const dates = collectScheduleDates();
    dates.push("");
    renderScheduleRows(dates);
  });
  $("#add-schedule-first").addEventListener("change", () => {
    const first = $("#add-schedule-first").value;
    if (first && !collectScheduleDates().length) renderScheduleRows([first]);
  });

  $("#form-add").addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      const mode = $("#add-mode").value;
      const schedule = mode === "milestone" ? collectScheduleDates() : [];
      if (mode === "milestone") {
        if (!schedule?.length) {
          showToast(t("err_schedule_incomplete"));
          return;
        }
      }
      const body = {
        mode,
        client_name: $("#add-name").value,
        contact_name: $("#add-contact").value,
        client_email: $("#add-email").value,
        group: $("#add-group").value,
        client_numbers: parseClientNumbers($("#add-client-numbers").value),
        service_label: $("#add-service").value,
        end_date: mode === "milestone" ? schedule[schedule.length - 1] : $("#add-end").value,
        total_milestones: schedule.length || parseInt($("#add-total-ms").value, 10) || 4,
        milestone_schedule: schedule,
      };
      const res = await api(`/api/clients?lang=${state.lang}`, {
        method: "POST",
        body: JSON.stringify(body),
      });
      showToast(res.message);
      state.composeClientId = res.client.id;
      $("#modal-add").close();
      $("#form-add").reset();
      switchView("dashboard");
      await refreshAll();
    } catch (err) {
      showToast(err.message);
    }
  });

  $("#compose-client").addEventListener("change", async (e) => {
    state.composeClientId = e.target.value;
    await loadComposeDetail();
    await loadReminder();
  });

  $("#btn-copy").addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText($("#compose-message").value);
      await logReminderSent();
      showToast(t("copy_done"));
      await refreshAll();
    } catch {
      showToast(t("copy_fallback"));
    }
  });

  $("#btn-mailto").addEventListener("click", () => {
    logReminderSent().then(() => refreshAll());
  });

  $("#fab-compose").addEventListener("click", () => openComposeDrawer());
  $("#btn-compose-close").addEventListener("click", closeComposeDrawer);
  $("#compose-backdrop").addEventListener("click", closeComposeDrawer);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && $("#compose-drawer").classList.contains("open")) {
      closeComposeDrawer();
    }
  });
}

function renderChannelRadios() {
  renderRadios("#channel-radios", state.meta.channels, state.channel, async (id) => {
    state.channel = id;
    renderChannelRadios();
    await loadReminder();
  });
}

function renderPaymentRadios() {
  renderRadios("#payment-radios", state.meta.payments, state.payment, async (id) => {
    state.payment = id;
    renderPaymentRadios();
    await loadReminder();
  });
}

async function loadMainApp() {
  state.branding = await api("/api/branding");
  state.meta = await api(`/api/meta?lang=${state.lang}`);
  state.lang = state.meta.lang;
  state.strings = state.meta.strings;
  applyBranding();
  applyStaticLabels();
  renderLangBar();
  renderChannelRadios();
  renderPaymentRadios();
  switchView(state.view);
  await loadDashboard();
  if (state.view === "clients") await loadClientsTable();
  if (state.view === "milestones") await loadMilestoneQueue();
  await loadComposeDetail();
  await loadReminder();
}

async function boot(full = true) {
  if (full) {
    bindEvents();
    window.addEventListener("beforeunload", releaseSessionLock);
  }
  try {
    const health = await api("/api/health");
    if (!health.version || health.version < "1.3.0") {
      showToast("Please restart server (Ctrl+C then python run_dev.py)");
    }
  } catch {
    showToast("Server 未連接，請 run_dev.py");
    return;
  }
  try {
    state.meta = await api(`/api/meta?lang=${state.lang}`);
    state.lang = state.meta.lang;
    state.strings = state.meta.strings;
  } catch {
    /* fall back to EXTRA_FALLBACK for login screen */
  }
  applyLoginLabels();
  state.session = await api("/api/session/status");
  if (state.session?.collab_enabled && !state.session?.authenticated) {
    $("#login-overlay").classList.remove("hidden");
    $("#app").classList.add("app--locked");
    return;
  }
  $("#login-overlay").classList.add("hidden");
  $("#app").classList.remove("app--locked");
  applyReadOnlyUi();
  await loadMainApp();
}

boot();
