"""CheckItNow Demo — FastAPI server."""

from __future__ import annotations

from datetime import date
from io import BytesIO

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from starlette.responses import Response as StarletteResponse

from logic.branding import load_branding
from logic.alert_banner import compute_alert_banner
from logic.alert_settings import load_alert_settings
from logic.lan_access import (
    DEFAULT_PORT,
    build_lan_url,
    get_lan_ip,
    is_loopback,
    lan_access_allowed,
    lan_status,
    load_lan_settings,
    save_lan_settings,
)
from logic.backup import (
    backup_status,
    ensure_startup_backup,
    list_backups,
    restore_from_backup,
)
from logic.clients import (
    add_client,
    active_clients,
    clear_all_clients,
    client_matches_query,
    client_summary_row,
    client_to_view,
    compute_kpi,
    delete_client_by_id,
    dismiss_alert,
    ensure_sample_on_startup,
    filter_clients,
    is_client_closed,
    list_client_groups,
    load_clients,
    log_reminder_sent,
    milestone_queue,
    normalize_client_numbers,
    renew_client,
    save_clients,
    seed_sample_clients,
    set_client_closed,
    toggle_milestone,
    update_client,
    update_client_schedule,
)
from logic.app_settings import get_data_path_info, load_app_settings, save_app_settings
from logic.activity_log import list_activity, log_activity
from logic.notifications import expiry_counts, maybe_send_desktop_notification
from logic.extra_i18n import EXTRA, extra_t
from logic.constants import (
    ALL_CHANNELS,
    CHANNEL_EMAIL,
    CHANNEL_SMS,
    KPI_SCROLL_TARGETS,
    LANG_CODES,
    LANG_SHORT,
    MODE_MILESTONE,
    MODE_SINGLE,
    PAYMENT_COLLECTION,
    PAYMENT_ROUTINE,
)
from logic.alerts import needs_priority_alert
from logic.dates import days_remaining, today
from logic.i18n import channel_label, mode_label, strip_emoji, t
from logic.milestones import milestone_service_label, schedule_rows
from logic.reminders import build_mailto_link, build_reminder_message, parse_email_message
from logic.export import export_clients_xlsx
from logic.import_excel import import_clients_from_rows, import_template_xlsx, parse_import_workbook
from logic.collab import (
    admin_reset_password,
    change_password,
    collab_enabled,
    force_release_lock,
    get_session,
    list_usernames,
    load_collab_config,
    login as collab_login,
    logout as collab_logout,
    promote_to_editor,
    demote_to_viewer,
    refresh_lock,
    save_collab_config,
    session_can_write,
    session_status,
)

from logic.paths import web_dir

WEB = web_dir()

app = FastAPI(title="CheckItNow Demo", version="1.7.0")
app.mount("/assets", StaticFiles(directory=WEB / "assets"), name="assets")
app.mount("/css", StaticFiles(directory=WEB / "css"), name="css")
app.mount("/js", StaticFiles(directory=WEB / "js"), name="js")


class ClientCreate(BaseModel):
    mode: str = MODE_SINGLE
    client_name: str
    contact_name: str = ""
    client_email: str = ""
    group: str = ""
    client_numbers: list[str] = Field(default_factory=list)
    service_label: str = ""
    end_date: str = ""
    total_milestones: int = 4
    milestone_schedule: list[str] = Field(default_factory=list)


class ClientUpdate(BaseModel):
    client_name: str
    contact_name: str = ""
    client_email: str = ""
    group: str = ""
    client_numbers: list[str] = Field(default_factory=list)
    service_label: str = ""
    end_date: str
    total_milestones: int | None = None


class MilestoneToggle(BaseModel):
    index: int
    checked: bool


class RenewBody(BaseModel):
    new_end_date: str
    reset_milestones: bool = False


class ScheduleUpdate(BaseModel):
    milestone_schedule: list[str] = Field(default_factory=list)


class DismissBody(BaseModel):
    snooze_days: int = 30


class LanAccessUpdate(BaseModel):
    enabled: bool


class AppSettingsUpdate(BaseModel):
    seed_sample_data: bool | None = None
    desktop_notifications: bool | None = None
    notification_interval_minutes: int | None = None
    data_path: str | None = None


class BackupRestoreBody(BaseModel):
    name: str = ""


class SessionLoginBody(BaseModel):
    username: str
    password: str
    role: str = "viewer"


class ForceUnlockBody(BaseModel):
    username: str
    password: str


class CollabConfigUpdate(BaseModel):
    enabled: bool | None = None


class ChangePasswordBody(BaseModel):
    current_password: str
    new_password: str


class AdminResetPasswordBody(BaseModel):
    admin_password: str
    target_username: str
    new_password: str


def _client_host(request: Request) -> str:
    client = request.client
    return client.host if client else "127.0.0.1"


def _server_port(request: Request) -> int:
    port = request.url.port
    return port if port else DEFAULT_PORT


def _session_token(request: Request) -> str:
    header = (request.headers.get("X-Session-Token") or "").strip()
    if header:
        return header
    return ""


_WRITE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})
_COLLAB_WRITE_EXEMPT = frozenset({
    "/api/collab/change-password",
    "/api/collab/reset-password",
})


@app.middleware("http")
async def lan_access_guard(request: Request, call_next):
    host = _client_host(request)
    if lan_access_allowed(host):
        return await call_next(request)
    return JSONResponse(
        {"detail": "LAN access is disabled. Enable it in Settings on your PC."},
        status_code=403,
    )


@app.middleware("http")
async def collab_write_guard(request: Request, call_next):
    if request.method in _WRITE_METHODS and collab_enabled():
        path = request.url.path
        if not path.startswith("/api/session/") and path not in _COLLAB_WRITE_EXEMPT:
            token = _session_token(request)
            if not session_can_write(token):
                status = session_status(token)
                holder = status.get("lock_holder") or {}
                return JSONResponse(
                    {
                        "detail": "read_only",
                        "lock_holder": holder,
                        "authenticated": status.get("authenticated"),
                        "role": status.get("role"),
                    },
                    status_code=403,
                )
    return await call_next(request)


def _lang(lang: str) -> str:
    return lang if lang in LANG_CODES else "en"


def _strings(lang: str) -> dict[str, str]:
    L = _lang(lang)
    keys = [
        "today", "sidebar_add", "manage", "kpi_active", "kpi_urgent", "kpi_milestone",
        "kpi_expired", "kpi_sub_urgent", "kpi_ms_logged", "kpi_click_hint",
        "section_priority", "priority_empty", "section_board", "section_compose",
        "compose_cap", "select_client", "channel_lbl", "payment_lbl", "payment_routine",
        "payment_collection", "reminder_area", "copy_btn", "email_open_btn",
        "email_no_address", "copy_done", "sidebar_footer", "empty_info", "card_end",
        "col_client", "service_label", "mode_single", "mode_milestone", "add_btn",
        "err_name", "added", "del", "close_btn", "client_name", "contact_person",
        "client_email", "end_date", "total_ms", "service_label", "progress_tracker",
        "ms_undo", "ms_locked", "no_trackers", "tagline", "subtitle",
        "badge_single", "badge_milestone", "next_payment", "next_service",
    ]
    strings = {k: t(L, k) for k in keys}
    strings.update(EXTRA.get(L, EXTRA["zh"]))
    return strings


APP_VERSION = "1.7.0"


@app.on_event("startup")
def startup_tasks() -> None:
    try:
        ensure_startup_backup()
        if ensure_sample_on_startup():
            log_activity("sample_loaded", detail="auto")
    except Exception:
        import traceback
        from logic.paths import data_dir

        log_path = data_dir() / "startup.log"
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write("Startup task failed:\n" + traceback.format_exc() + "\n")


@app.get("/api/health")
def api_health() -> dict:
    return {"ok": True, "version": APP_VERSION}


@app.get("/api/collab")
def api_collab_config() -> dict:
    cfg = load_collab_config()
    return {
        "enabled": cfg.get("enabled"),
        "lock_stale_minutes": cfg.get("lock_stale_minutes"),
        "heartbeat_interval_seconds": cfg.get("heartbeat_interval_seconds"),
        "demo_users_hint": ", ".join(sorted((cfg.get("users") or {}).keys())),
        "usernames": list_usernames(),
    }


@app.patch("/api/collab")
def api_collab_update(body: CollabConfigUpdate, request: Request) -> dict:
    if not is_loopback(_client_host(request)):
        raise HTTPException(403, "Change collaboration settings from the desktop app only.")
    patch = body.model_dump(exclude_none=True)
    return save_collab_config(patch)


@app.post("/api/collab/change-password")
def api_collab_change_password(body: ChangePasswordBody, request: Request, lang: str = "en") -> dict:
    if not is_loopback(_client_host(request)):
        raise HTTPException(403, "Change passwords from the desktop app only.")
    token = _session_token(request)
    sess = get_session(token)
    if not sess:
        raise HTTPException(401, "not_authenticated")
    if not body.new_password.strip():
        raise HTTPException(400, "password_empty")
    ok, err = change_password(sess.get("username", ""), body.current_password, body.new_password.strip())
    if not ok:
        raise HTTPException(401 if err == "invalid_credentials" else 400, err or "change_failed")
    L = _lang(lang)
    log_activity("password_changed", detail=sess.get("username", ""))
    return {"ok": True, "message": extra_t(L, "password_change_ok")}


@app.post("/api/collab/reset-password")
def api_collab_reset_password(body: AdminResetPasswordBody, request: Request, lang: str = "en") -> dict:
    if not is_loopback(_client_host(request)):
        raise HTTPException(403, "Reset passwords from the desktop app only.")
    token = _session_token(request)
    sess = get_session(token)
    if not sess or sess.get("username") != "admin":
        raise HTTPException(403, "not_admin")
    target = body.target_username.strip()
    new_pw = body.new_password.strip()
    if not new_pw:
        raise HTTPException(400, "password_empty")
    ok, err = admin_reset_password("admin", body.admin_password, target, new_pw)
    if not ok:
        code = 401 if err == "invalid_credentials" else 403 if err == "not_admin" else 400
        raise HTTPException(code, err or "reset_failed")
    L = _lang(lang)
    log_activity("password_reset", detail=target)
    return {
        "ok": True,
        "message": extra_t(L, "password_reset_ok", user=target),
    }


@app.get("/api/session/status")
def api_session_status(request: Request) -> dict:
    return session_status(_session_token(request))


@app.post("/api/session/login")
def api_session_login(body: SessionLoginBody) -> dict:
    payload, err = collab_login(body.username, body.password, body.role)
    if err == "invalid_credentials":
        raise HTTPException(401, "invalid_credentials")
    if payload is None:
        raise HTTPException(400, "login_failed")
    return payload


@app.post("/api/session/logout")
async def api_session_logout(request: Request) -> dict:
    token = _session_token(request)
    if not token:
        try:
            body = await request.json()
            if isinstance(body, dict):
                token = str(body.get("token") or "").strip()
        except Exception:
            token = ""
    if token:
        collab_logout(token)
    return {"ok": True}


@app.post("/api/session/heartbeat")
def api_session_heartbeat(request: Request) -> dict:
    token = _session_token(request)
    if not token:
        raise HTTPException(401, "not_authenticated")
    if not refresh_lock(token):
        status = session_status(token)
        if status.get("authenticated"):
            return status
        raise HTTPException(409, "lock_lost")
    return session_status(token)


@app.post("/api/session/promote")
def api_session_promote(request: Request) -> dict:
    token = _session_token(request)
    if not token:
        raise HTTPException(401, "not_authenticated")
    payload, err = promote_to_editor(token)
    if err == "lock_held":
        raise HTTPException(409, "lock_held")
    if err or payload is None:
        raise HTTPException(400, err or "promote_failed")
    return payload


@app.post("/api/session/demote")
def api_session_demote(request: Request) -> dict:
    token = _session_token(request)
    if not token:
        raise HTTPException(401, "not_authenticated")
    payload, err = demote_to_viewer(token)
    if err or payload is None:
        raise HTTPException(400, err or "demote_failed")
    return payload


@app.post("/api/session/force-unlock")
def api_session_force_unlock(body: ForceUnlockBody, request: Request) -> dict:
    if not is_loopback(_client_host(request)):
        raise HTTPException(403, "Force unlock from the desktop app only.")
    ok, reason = force_release_lock(body.username, body.password)
    if not ok:
        raise HTTPException(401, reason)
    return {"ok": True, "message": "released"}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(WEB / "index.html")


@app.get("/api/branding")
def api_branding() -> dict:
    return load_branding()


@app.get("/api/meta")
def api_meta(lang: str = "en") -> dict:
    L = _lang(lang)
    alert_cfg = load_alert_settings()
    return {
        "lang": L,
        "langs": [{"code": c, "short": LANG_SHORT[c]} for c in LANG_CODES],
        "strings": _strings(L),
        "alert_settings": alert_cfg,
        "urgent_days": alert_cfg["priority_days"],
        "channels": [
            {"id": CHANNEL_SMS, "label": channel_label(L, CHANNEL_SMS)},
            {"id": CHANNEL_EMAIL, "label": channel_label(L, CHANNEL_EMAIL)},
        ],
        "payments": [
            {"id": PAYMENT_ROUTINE, "label": strip_emoji(t(L, "payment_routine"))},
            {"id": PAYMENT_COLLECTION, "label": strip_emoji(t(L, "payment_collection"))},
        ],
        "kpi_scroll_targets": KPI_SCROLL_TARGETS,
        "today": today().strftime("%Y-%m-%d"),
        "app_version": APP_VERSION,
    }


@app.get("/api/dashboard")
def api_dashboard(lang: str = "en", filter: str = "all") -> dict:
    L = _lang(lang)
    all_clients = load_clients()
    active = active_clients(all_clients)
    kpi = compute_kpi(all_clients)
    alert_cfg = load_alert_settings()
    filtered = filter_clients(all_clients, filter)
    filtered.sort(key=lambda c: days_remaining(c["end_date"]))
    priority = sorted(
        [c for c in active if needs_priority_alert(c)],
        key=lambda c: days_remaining(c["end_date"]),
    )
    return {
        "kpi": {
            "all": {
                "value": kpi["all"],
                "label": t(L, "kpi_active"),
                "sub": t(L, "kpi_click_hint"),
                "css": "accent",
                "filter": "all",
                "scroll": KPI_SCROLL_TARGETS["all"],
            },
            "urgent": {
                "value": kpi["urgent"],
                "label": t(L, "kpi_urgent"),
                "sub": t(L, "kpi_sub_urgent", n=alert_cfg["priority_days"]),
                "css": "warn",
                "filter": "urgent",
                "scroll": KPI_SCROLL_TARGETS["urgent"],
            },
            "milestone": {
                "value": kpi["milestone"],
                "label": extra_t(L, "nav_milestones"),
                "sub": t(
                    L, "kpi_ms_logged",
                    done=kpi["milestone_logged"],
                    total=kpi["milestone_total"],
                ),
                "css": "ok",
                "filter": "milestone",
                "scroll": KPI_SCROLL_TARGETS["milestone"],
            },
            "expired": {
                "value": kpi["expired"],
                "label": t(L, "kpi_expired"),
                "sub": t(L, "kpi_click_hint"),
                "css": "danger",
                "filter": "expired",
                "scroll": KPI_SCROLL_TARGETS["expired"],
            },
        },
        "filter": filter,
        "clients": [client_to_view(c, L) for c in filtered],
        "priority": [client_to_view(c, L) for c in priority[:5]],
        "alert_banner": compute_alert_banner(active, L),
        "alert_settings": alert_cfg,
    }


@app.get("/api/lists/clients")
@app.get("/api/clients-list")  # legacy alias
def api_clients_list(lang: str = "en", q: str = "", group: str = "", account: str = "all") -> dict:
    L = _lang(lang)
    all_clients = load_clients()
    clients = sorted(all_clients, key=lambda c: c["client_name"].lower())
    if account == "active":
        clients = [c for c in clients if not is_client_closed(c)]
    elif account == "closed":
        clients = [c for c in clients if is_client_closed(c)]
    if group:
        if group == "__none__":
            clients = [c for c in clients if not (c.get("group") or "").strip()]
        else:
            clients = [c for c in clients if (c.get("group") or "").strip() == group]
    if q.strip():
        clients = [c for c in clients if client_matches_query(c, q)]
    return {
        "rows": [client_summary_row(c, L) for c in clients],
        "groups": list_client_groups(all_clients),
        "total": len(all_clients),
        "filtered": len(clients),
    }


@app.get("/api/export/clients.xlsx")
def api_export_clients(
    lang: str = "en",
    q: str = "",
    group: str = "",
    account: str = "all",
) -> Response:
    L = _lang(lang)
    buf, filename = export_clients_xlsx(L=L, q=q, group=group, account=account)
    log_activity("export_excel")
    return Response(
        content=buf.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.get("/api/import/clients-template.xlsx")
def api_import_template(lang: str = "en") -> Response:
    L = _lang(lang)
    buf, filename = import_template_xlsx(L)
    return Response(
        content=buf.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.post("/api/import/clients")
async def api_import_clients(
    request: Request,
    file: UploadFile = File(...),
    lang: str = "en",
    mode: str = "append",
) -> dict:
    if not is_loopback(_client_host(request)):
        raise HTTPException(403, "Import from the desktop app only.")
    L = _lang(lang)
    if mode not in {"append", "replace"}:
        raise HTTPException(400, "mode must be append or replace")
    raw = await file.read()
    if not raw:
        raise HTTPException(400, "Empty file")
    rows, parse_errors = parse_import_workbook(raw)
    if not rows and parse_errors:
        raise HTTPException(400, parse_errors[0])
    try:
        result = import_clients_from_rows(L, rows, mode=mode)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    all_errors = parse_errors + result.get("errors", [])
    if result["imported"] <= 0:
        detail = all_errors[0] if all_errors else extra_t(L, "import_excel_none")
        raise HTTPException(400, detail)
    log_activity("import_excel", detail=f"{result['imported']} rows")
    message = extra_t(
        L,
        "import_excel_done",
        n=result["imported"],
        skipped=result.get("skipped") or 0,
    )
    return {
        "ok": True,
        "message": message,
        "imported": result["imported"],
        "skipped": result.get("skipped") or 0,
        "errors": all_errors[:20],
        "total_clients": result.get("total_clients") or 0,
    }


@app.get("/api/lists/milestones")
@app.get("/api/milestone-queue")  # legacy alias
def api_milestone_queue(lang: str = "en") -> dict:
    L = _lang(lang)
    return milestone_queue(L)


@app.get("/api/clients/{client_id}")
def api_client(client_id: str, lang: str = "en") -> dict:
    L = _lang(lang)
    for c in load_clients():
        if c["id"] == client_id:
            view = client_to_view(c, L)
            if c["mode"] == MODE_MILESTONE:
                view["milestone_rows"] = schedule_rows(c, L)
            return view
    raise HTTPException(404, "Client not found")


@app.post("/api/clients")
def api_create_client(body: ClientCreate, lang: str = "en") -> dict:
    L = _lang(lang)
    if not body.client_name.strip():
        raise HTTPException(400, t(L, "err_name"))
    schedule = [s.strip() for s in (body.milestone_schedule or []) if s and s.strip()]
    if body.mode == MODE_MILESTONE:
        if not schedule:
            raise HTTPException(400, extra_t(L, "err_schedule"))
        try:
            end = date.fromisoformat(schedule[-1][:10])
        except ValueError as exc:
            raise HTTPException(400, "Invalid milestone_schedule") from exc
    else:
        if not body.end_date.strip():
            raise HTTPException(400, "Invalid end_date")
        try:
            end = date.fromisoformat(body.end_date[:10])
        except ValueError as exc:
            raise HTTPException(400, "Invalid end_date") from exc
    clients = load_clients()
    entry = add_client(
        L, body.mode, body.client_name, body.contact_name,
        body.client_email, body.service_label, end, body.total_milestones,
        milestone_schedule=schedule if body.mode == MODE_MILESTONE else None,
        group=body.group,
        client_numbers=normalize_client_numbers(body.client_numbers),
    )
    clients.append(entry)
    save_clients(clients)
    log_activity("client_added", client_id=entry["id"], client_name=entry["client_name"])
    return {"ok": True, "client": client_to_view(entry, L), "message": t(L, "added", name=entry["client_name"])}


@app.put("/api/clients/{client_id}")
def api_update_client(client_id: str, body: ClientUpdate, lang: str = "en") -> dict:
    L = _lang(lang)
    try:
        end = date.fromisoformat(body.end_date[:10])
    except ValueError as exc:
        raise HTTPException(400, "Invalid end_date") from exc
    err = update_client(
        L, client_id, body.client_name, body.contact_name,
        body.client_email, body.service_label, end, body.total_milestones,
        group=body.group,
        client_numbers=normalize_client_numbers(body.client_numbers),
    )
    if err:
        raise HTTPException(400, err)
    for c in load_clients():
        if c["id"] == client_id:
            log_activity("client_updated", client_id=client_id, client_name=c["client_name"])
            return {"ok": True, "client": client_to_view(c, L), "message": extra_t(L, "client_saved")}
    raise HTTPException(404, "Client not found")


@app.put("/api/clients/{client_id}/schedule")
def api_update_schedule(client_id: str, body: ScheduleUpdate, lang: str = "en") -> dict:
    L = _lang(lang)
    schedule = [s.strip() for s in (body.milestone_schedule or []) if s and s.strip()]
    if not schedule:
        raise HTTPException(400, extra_t(L, "err_schedule"))
    updated, err = update_client_schedule(L, client_id, schedule)
    if err:
        raise HTTPException(400, err)
    if not updated:
        raise HTTPException(404, "Client not found")
    log_activity("schedule_updated", client_id=client_id, client_name=updated["client_name"])
    return {
        "ok": True,
        "client": client_to_view(updated, L),
        "message": extra_t(L, "schedule_saved"),
    }


@app.delete("/api/clients/{client_id}")
def api_delete_client(client_id: str, lang: str = "en") -> dict:
    L = _lang(lang)
    name = ""
    for c in load_clients():
        if c["id"] == client_id:
            name = c["client_name"]
            break
    delete_client_by_id(client_id)
    if name:
        log_activity("client_deleted", client_id=client_id, client_name=name)
    return {"ok": True, "message": t(L, "del") if name else ""}


@app.post("/api/clients/{client_id}/milestone")
def api_milestone(client_id: str, body: MilestoneToggle, lang: str = "en") -> dict:
    L = _lang(lang)
    updated = toggle_milestone(client_id, body.index, body.checked)
    if not updated:
        raise HTTPException(404, "Client not found")
    log_activity("milestone_toggled", client_id=client_id, client_name=updated["client_name"],
                 detail=f"{body.index}:{body.checked}")
    return {"ok": True, "client": client_to_view(updated, L)}


@app.get("/api/reminder/{client_id}")
def api_reminder(
    client_id: str,
    lang: str = "en",
    channel: str = CHANNEL_SMS,
    payment: str = PAYMENT_ROUTINE,
) -> dict:
    L = _lang(lang)
    for c in load_clients():
        if c["id"] == client_id:
            msg = build_reminder_message(c, L, channel, payment)
            mailto = ""
            if channel == CHANNEL_EMAIL:
                subject, body = parse_email_message(msg)
                mailto = build_mailto_link(c.get("client_email", ""), subject, body)
            return {"message": msg, "mailto": mailto}
    raise HTTPException(404, "Client not found")


@app.post("/api/clients/{client_id}/log-reminder")
def api_log_reminder(client_id: str, lang: str = "en") -> dict:
    L = _lang(lang)
    updated = log_reminder_sent(client_id)
    if not updated:
        raise HTTPException(404, "Client not found")
    log_activity("reminder_sent", client_id=client_id, client_name=updated["client_name"])
    return {
        "ok": True,
        "client": client_to_view(updated, L),
        "message": extra_t(L, "last_reminder", date=updated.get("last_reminder_at", "")),
    }


@app.post("/api/clients/{client_id}/renew")
def api_renew(client_id: str, body: RenewBody, lang: str = "en") -> dict:
    L = _lang(lang)
    try:
        new_end = date.fromisoformat(body.new_end_date[:10])
    except ValueError as exc:
        raise HTTPException(400, "Invalid new_end_date") from exc
    updated = renew_client(client_id, new_end, body.reset_milestones)
    if not updated:
        raise HTTPException(404, "Client not found")
    log_activity("client_renewed", client_id=client_id, client_name=updated["client_name"],
                 detail=body.new_end_date[:10])
    return {
        "ok": True,
        "client": client_to_view(updated, L),
        "message": extra_t(L, "renew_saved", name=updated["client_name"]),
    }


@app.post("/api/clients/{client_id}/close")
def api_close_client(client_id: str, lang: str = "en") -> dict:
    L = _lang(lang)
    updated = set_client_closed(client_id, True)
    if not updated:
        raise HTTPException(404, "Client not found")
    log_activity("client_closed", client_id=client_id, client_name=updated["client_name"])
    return {
        "ok": True,
        "client": client_to_view(updated, L),
        "message": extra_t(L, "client_closed", name=updated["client_name"]),
    }


@app.post("/api/clients/{client_id}/reopen")
def api_reopen_client(client_id: str, lang: str = "en") -> dict:
    L = _lang(lang)
    updated = set_client_closed(client_id, False)
    if not updated:
        raise HTTPException(404, "Client not found")
    log_activity("client_reopened", client_id=client_id, client_name=updated["client_name"])
    return {
        "ok": True,
        "client": client_to_view(updated, L),
        "message": extra_t(L, "client_reopened", name=updated["client_name"]),
    }


@app.get("/api/lan-access")
def api_lan_access(request: Request) -> dict:
    port = _server_port(request)
    status = lan_status(port)
    status["qr_path"] = "/api/lan-access/qr.svg" if status.get("url") else None
    return status


@app.patch("/api/lan-access")
def api_lan_access_update(body: LanAccessUpdate, request: Request) -> dict:
    if not is_loopback(_client_host(request)):
        raise HTTPException(403, "Change LAN settings from the desktop app only.")
    if body.enabled and not get_lan_ip():
        raise HTTPException(400, "No WiFi / LAN IP found. Connect to a network first.")
    save_lan_settings(body.enabled)
    port = _server_port(request)
    status = lan_status(port)
    status["qr_path"] = "/api/lan-access/qr.svg" if status.get("url") else None
    return status


@app.get("/api/lan-access/qr.svg")
def api_lan_qr_svg(request: Request) -> StarletteResponse:
    if not load_lan_settings().get("enabled"):
        raise HTTPException(404, "LAN access disabled")
    host = _client_host(request)
    if not lan_access_allowed(host):
        raise HTTPException(403, "Forbidden")
    port = _server_port(request)
    url = build_lan_url(get_lan_ip(), port)
    if not url:
        raise HTTPException(404, "No LAN URL")
    try:
        import qrcode
        import qrcode.image.svg
    except ImportError as exc:
        raise HTTPException(501, "QR library not installed") from exc
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    stream = BytesIO()
    img.save(stream)
    return Response(content=stream.getvalue(), media_type="image/svg+xml")


@app.get("/api/backup")
def api_backup_status() -> dict:
    status = backup_status()
    status["backups"] = list_backups(50)
    return status


@app.post("/api/backup/restore")
def api_backup_restore(body: BackupRestoreBody, request: Request, lang: str = "en") -> dict:
    if not is_loopback(_client_host(request)):
        raise HTTPException(403, "Restore backups from the desktop app only.")
    L = _lang(lang)
    target = None
    if body.name.strip():
        from logic.backup import DAILY_DIR, RECENT_DIR

        for folder in (DAILY_DIR, RECENT_DIR):
            candidate = folder / body.name.strip()
            if candidate.exists() and candidate.is_file():
                target = candidate
                break
        if target is None:
            raise HTTPException(404, "Backup not found")
    restored = restore_from_backup(target)
    if restored is None:
        raise HTTPException(404, "No valid backup available")
    log_activity("backup_restored", detail=body.name.strip() or "latest")
    latest = backup_status()
    return {
        "ok": True,
        "message": extra_t(
            L,
            "backup_restore_done",
            name=body.name.strip() or latest.get("latest_backup_name") or "backup",
        ),
        "count": len(restored),
        "backup": latest,
    }


@app.post("/api/clients/{client_id}/dismiss-alert")
def api_dismiss(client_id: str, body: DismissBody, lang: str = "en") -> dict:
    L = _lang(lang)
    updated = dismiss_alert(client_id, body.snooze_days)
    if not updated:
        raise HTTPException(404, "Client not found")
    log_activity("alert_dismissed", client_id=client_id, client_name=updated["client_name"])
    return {
        "ok": True,
        "client": client_to_view(updated, L),
        "message": extra_t(L, "dismiss_saved"),
    }


@app.get("/api/about")
def api_about() -> dict:
    branding = load_branding()
    return {
        "app_name": branding.get("appName", "CheckItNow"),
        "tagline": branding.get("tagline", ""),
        "version": APP_VERSION,
        "footer": branding.get("footerNote", ""),
    }


@app.get("/api/app-settings")
def api_app_settings() -> dict:
    settings = load_app_settings()
    settings["client_count"] = len(load_clients())
    settings.update(get_data_path_info())
    return settings


@app.patch("/api/app-settings")
def api_app_settings_update(body: AppSettingsUpdate, request: Request) -> dict:
    if not is_loopback(_client_host(request)):
        raise HTTPException(403, "Change settings from the desktop app only.")
    patch = body.model_dump(exclude_none=True)
    try:
        settings = save_app_settings(patch)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    settings["client_count"] = len(load_clients())
    settings.update(get_data_path_info())
    if "data_path" in patch:
        settings["data_path_changed"] = True
    return settings


@app.get("/api/activity")
def api_activity(limit: int = 40, lang: str = "en") -> dict:
    L = _lang(lang)
    rows = []
    for entry in list_activity(limit):
        action = entry.get("action", "")
        key = f"activity_{action}"
        text = extra_t(
            L,
            key,
            name=entry.get("client_name") or "",
            detail=entry.get("detail") or "",
        )
        rows.append({**entry, "label": text})
    return {"items": rows}


@app.post("/api/sample-data/load")
def api_sample_load(request: Request, lang: str = "en") -> dict:
    if not is_loopback(_client_host(request)):
        raise HTTPException(403, "Load sample data from the desktop app only.")
    L = _lang(lang)
    clients = seed_sample_clients()
    log_activity("sample_loaded", detail="manual")
    return {"ok": True, "count": len(clients), "message": extra_t(L, "sample_loaded", n=len(clients))}


@app.post("/api/sample-data/clear")
def api_sample_clear(request: Request, lang: str = "en") -> dict:
    if not is_loopback(_client_host(request)):
        raise HTTPException(403, "Clear data from the desktop app only.")
    L = _lang(lang)
    clear_all_clients()
    log_activity("sample_cleared")
    return {"ok": True, "message": extra_t(L, "sample_cleared")}


@app.post("/api/notifications/check")
def api_notifications_check(lang: str = "en") -> dict:
    L = _lang(lang)
    return maybe_send_desktop_notification(L)


@app.get("/api/notifications/status")
def api_notifications_status(lang: str = "en") -> dict:
    L = _lang(lang)
    from logic.notifications import notification_message

    counts = expiry_counts()
    title, body = notification_message(L, counts)
    settings = load_app_settings()
    return {
        "counts": counts,
        "preview_title": title,
        "preview_body": body,
        "desktop_notifications": settings.get("desktop_notifications", True),
    }
