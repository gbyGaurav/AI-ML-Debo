"""
LinkedIn Learning Publisher MCP Server

A simple, student-friendly MCP server for a college assignment:
- 1 Resource: learnings://today/raw
- 1 Prompt: format_linkedin_post
- 1 Tool: post_to_linkedin(content: str)
"""

import asyncio
import logging
from pathlib import Path
import re

from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

# Configure logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Initialize FastMCP Server
mcp = FastMCP("LinkedInLearningPublisher")

# Local paths
BASE_DIR = Path(__file__).parent.resolve()
DAILY_NOTES_FILE = BASE_DIR / "daily_notes.txt"
USER_DATA_DIR = BASE_DIR / "user_data"


# ==============================================================================
# 1. MCP RESOURCE: learnings://today/raw
# ==============================================================================
@mcp.resource("learnings://today/raw")
def get_today_learning() -> str:
    """
    Read-only resource that provides today's saved learning notes.
    Reads daily_notes.txt and returns plain text.
    """
    if not DAILY_NOTES_FILE.exists():
        return "No learning has been saved for today yet."

    try:
        content = DAILY_NOTES_FILE.read_text(encoding="utf-8").strip()
        if not content:
            return "No learning has been saved for today yet."
        return content
    except Exception as e:
        return f"Error reading daily notes: {str(e)}"


# ==============================================================================
# 2. MCP PROMPT: format_linkedin_post
# ==============================================================================
@mcp.prompt()
def format_linkedin_post() -> str:
    """
    Prompt template instructing Claude how to convert learning notes into
    a professional, student-friendly LinkedIn post without inventing facts.
    """
    return (
        "You are an assistant helping format today's learning into a LinkedIn post.\n\n"
        "Instructions:\n"
        "1. Use the user's actual learning from today (from the conversation or learnings://today/raw).\n"
        "2. Preserve the original meaning accurately.\n"
        "3. Do NOT invent achievements, projects, work experience, or facts not mentioned by the user.\n"
        "4. Make the post sound natural and professional, suitable for a student/developer.\n"
        "5. Include a short, engaging opening hook.\n"
        "6. Clearly explain what was learned in a clean, readable structure.\n"
        "7. Mention practical understanding or key takeaways if present.\n"
        "8. Add 2–3 relevant hashtags (e.g., #LearningInPublic #Python #MCP).\n"
        "9. Return ONLY the final LinkedIn post text so it is ready to publish."
    )


# ==============================================================================
# 3. MCP TOOL: post_to_linkedin
# ==============================================================================
@mcp.tool()
async def post_to_linkedin(content: str) -> str:
    """
    Publish an approved post to LinkedIn using Playwright browser automation.
    Reuses a local persistent Chromium profile (./user_data) to maintain login.
    """
    # 1. Validate content
    if not content or not content.strip():
        return "Error: Post content cannot be empty."

    post_text = content.strip()
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Launch persistent Playwright Chromium browser
    async with async_playwright() as p:
        try:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(USER_DATA_DIR),
                headless=False,
                viewport={"width": 1280, "height": 800},
            )
        except Exception as e:
            return f"Error launching browser: {str(e)}"

        try:
            page = context.pages[0] if context.pages else await context.new_page()

            # 3. Open LinkedIn feed directly
            try:
                await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded", timeout=60000)
            except PlaywrightTimeoutError:
                return "Error: Timed out opening LinkedIn feed. Please check your internet connection."

            # 4. Check if user is logged in
            async def check_logged_in() -> bool:
                if "/feed" in page.url:
                    return True
                try:
                    if await page.get_by_role("button", name=re.compile(r"start a post", re.I)).count() > 0:
                        return True
                except Exception:
                    pass
                try:
                    if await page.locator("nav.global-nav, #global-nav, div.global-nav__content").count() > 0:
                        return True
                except Exception:
                    pass
                return False

            if not await check_logged_in():
                # Allow user to log in manually using their LinkedIn email and password
                # (Avoid 'Sign in with Google' because Google blocks automated browsers)
                login_timeout = 300  # 5 minutes
                poll_interval = 2
                elapsed = 0
                while elapsed < login_timeout:
                    await asyncio.sleep(poll_interval)
                    elapsed += poll_interval
                    if await check_logged_in():
                        break
                else:
                    return (
                        "Error: LinkedIn login was not completed within 5 minutes. "
                        "Please run the tool again and sign in using your LinkedIn email and password "
                        "(avoid 'Sign in with Google' as Google blocks automated browsers)."
                    )

            # Ensure we are on the feed page after authentication
            if "/feed" not in page.url:
                try:
                    await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded", timeout=30000)
                except Exception:
                    pass

            await page.wait_for_timeout(3000)

            # 5. Dismiss non-essential popups/overlays that might block the composer
            for dismiss_sel in [
                "button[aria-label='Dismiss']",
                "button[aria-label='Got it']",
                "button.artdeco-modal__dismiss",
                "button:has-text('Got it')",
                "button:has-text('Dismiss')",
                "button:has-text('Not now')",
            ]:
                try:
                    dismiss_btns = page.locator(dismiss_sel)
                    if await dismiss_btns.count() > 0 and await dismiss_btns.first.is_visible():
                        await dismiss_btns.first.click()
                        await page.wait_for_timeout(500)
                except Exception:
                    pass

            # Collapse messaging overlay if it is expanded
            try:
                collapse_btn = page.locator(
                    "button[data-control-name='overlay.collapse_conversation'], "
                    "button[aria-label*='Collapse messaging'], "
                    ".msg-overlay-bubble-header__control--close"
                )
                if await collapse_btn.count() > 0 and await collapse_btn.first.is_visible():
                    await collapse_btn.first.click()
                    await page.wait_for_timeout(500)
            except Exception:
                pass

            # 6. Locate and click "Start a post" button
            start_post_button = None
            start_post_locators = [
                page.get_by_role("button", name=re.compile(r"start a post", re.I)),
                page.locator("button.share-box-feed-entry__trigger"),
                page.locator(".share-box-feed-entry button"),
                page.locator("div.share-box-feed-entry__wrapper button"),
                page.get_by_text("Start a post", exact=False),
            ]
            for loc in start_post_locators:
                try:
                    if await loc.count() > 0 and await loc.first.is_visible():
                        start_post_button = loc.first
                        break
                except Exception:
                    continue

            if not start_post_button:
                try:
                    primary = page.get_by_role("button", name=re.compile(r"start a post", re.I))
                    await primary.first.wait_for(state="visible", timeout=15000)
                    start_post_button = primary.first
                except PlaywrightTimeoutError:
                    return "Error: Could not locate 'Start a post' button on LinkedIn feed."

            await start_post_button.scroll_into_view_if_needed()
            await start_post_button.click()

            # 7. Wait for composer dialog to fully appear
            dialog_locators = [
                page.locator("[data-sdui-screen*='ShareCompose']"),
                page.locator(".share-creation-state"),
                page.locator(".share-box-modal"),
                page.locator("div.feed-shared-modal"),
                page.locator(".ProseMirror"),
                page.locator("div[role='dialog']").filter(has=page.locator("[contenteditable='true'], .ProseMirror, button:has-text('Post')")),
            ]
            dialog = None
            for d_loc in dialog_locators:
                try:
                    await d_loc.first.wait_for(state="visible", timeout=12000)
                    dialog = d_loc.first
                    break
                except Exception:
                    continue

            # Give rich editor time to initialize in DOM
            await page.wait_for_timeout(1500)

            # 8. Detect the visible and editable post editor inside the composer
            editor = None
            editor_selectors = [
                ".ProseMirror",
                "[contenteditable='true']",
                "[role='textbox']",
                ".ql-editor",
                "div.editor-content",
                "div[data-placeholder]",
                "div[aria-multiline='true']",
                "p",
            ]

            # Search within the active dialog first
            if dialog:
                for sel in editor_selectors:
                    try:
                        candidates = dialog.locator(sel)
                        count = await candidates.count()
                        for i in range(count):
                            el = candidates.nth(i)
                            if await el.is_visible():
                                is_editable = await el.is_editable()
                                is_content_editable = await el.evaluate("node => node.isContentEditable")
                                if is_editable or is_content_editable:
                                    editor = el
                                    break
                        if editor:
                            break
                    except Exception:
                        continue

            # Page-level fallback excluding messaging overlay
            if not editor:
                page_candidates = [
                    page.locator("[data-sdui-screen*='ShareCompose'] .ProseMirror"),
                    page.locator("[data-sdui-screen*='ShareCompose'] [contenteditable='true']"),
                    page.locator("div[role='dialog'] [contenteditable='true']"),
                    page.locator(".share-creation-state [contenteditable='true']"),
                    page.locator("div[role='dialog'] div[role='textbox']"),
                    page.locator("[contenteditable='true']:not(.msg-overlay-bubble-header):not(.msg-overlay-conversation-bubble [contenteditable='true'])"),
                    page.get_by_role("textbox", name=re.compile(r"what do you want to talk about", re.I)),
                ]
                for cand in page_candidates:
                    try:
                        if await cand.count() > 0 and await cand.first.is_visible():
                            is_editable = await cand.first.is_editable()
                            is_content_editable = await cand.first.evaluate("node => node.isContentEditable")
                            if is_editable or is_content_editable:
                                editor = cand.first
                                break
                    except Exception:
                        continue

            # If editor cannot be found, save diagnostic HTML & screenshot
            if not editor:
                diag_html = BASE_DIR / "composer_diagnostic.html"
                diag_png = BASE_DIR / "composer_diagnostic.png"
                try:
                    content_html = await page.content()
                    diag_html.write_text(content_html, encoding="utf-8")
                    await page.screenshot(path=str(diag_png))
                    diag_msg = f" (Saved diagnostics to {diag_html.name} and {diag_png.name})"
                except Exception:
                    diag_msg = ""
                return f"Error: Could not locate post editor in composer dialog.{diag_msg}"

            # 9. Insert post content and verify it appears in the composer
            await editor.click()
            await page.wait_for_timeout(500)
            await page.keyboard.press("Control+A")
            await page.keyboard.insert_text(post_text)

            # Trigger input/keyup events so LinkedIn's state updates and enables the Post button
            await page.keyboard.press("End")
            await page.keyboard.press("Space")
            await page.keyboard.press("Backspace")
            await page.wait_for_timeout(1000)

            # Verify that text registered in the DOM
            editor_text = (await editor.inner_text()).strip()
            if not editor_text or len(editor_text) < min(10, len(post_text)):
                try:
                    await editor.fill(post_text)
                except Exception:
                    await editor.click()
                    await page.keyboard.type(post_text, delay=15)
                await page.wait_for_timeout(1000)
                editor_text = (await editor.inner_text()).strip()

            if not editor_text:
                return "Error: Failed to enter post text into the LinkedIn editor. Text did not appear in composer."

            # Determine the active modal container that encloses our editor
            composer_container = None
            for container_sel in [
                "[data-sdui-screen*='ShareCompose']",
                "div.share-creation-state",
                "div.share-box-modal",
                "div.feed-shared-modal",
                "div.artdeco-modal",
                "div[role='dialog']",
            ]:
                try:
                    parent_modal = page.locator(container_sel).filter(has=editor).first
                    if await parent_modal.count() > 0:
                        composer_container = parent_modal
                        break
                except Exception:
                    pass

            if not composer_container:
                try:
                    sdui_modal = page.locator("[data-sdui-screen*='ShareCompose']").first
                    if await sdui_modal.count() > 0 and await sdui_modal.is_visible():
                        composer_container = sdui_modal
                except Exception:
                    pass

            container_scope = composer_container if composer_container else dialog

            # 10. Locate the final Post button using targeted selectors first, then fallback inspection
            post_button_info = None
            diagnostics_button_list = []

            # Direct targeted Post button candidate locators in order of specificity
            targeted_locators = []
            if composer_container:
                targeted_locators.extend([
                    composer_container.get_by_role("button", name="Post", exact=True),
                    composer_container.locator("button").filter(has_text=re.compile(r"^\s*Post\s*$", re.I)),
                    composer_container.locator("button.share-actions__primary-action"),
                ])

            targeted_locators.extend([
                page.get_by_role("button", name="Post", exact=True),
                page.locator("[data-sdui-screen*='ShareCompose'] button").filter(has_text=re.compile(r"^\s*Post\s*$", re.I)),
                page.locator("button.share-actions__primary-action"),
                page.locator("button").filter(has_text=re.compile(r"^\s*Post\s*$", re.I)),
            ])

            for target in targeted_locators:
                try:
                    if await target.count() > 0 and await target.first.is_visible():
                        btn = target.first
                        text = (await btn.inner_text()).strip()
                        aria_label = (await btn.get_attribute("aria-label")) or ""
                        cls = (await btn.get_attribute("class")) or ""
                        is_disabled = await btn.is_disabled()
                        aria_disabled = (await btn.get_attribute("aria-disabled")) == "true"
                        post_button_info = {
                            "text": text,
                            "aria_label": aria_label,
                            "class": cls,
                            "disabled": is_disabled or aria_disabled,
                            "locator": btn,
                        }
                        logger.info(f"Targeted match found for Post button: text='{text}', disabled={is_disabled or aria_disabled}")
                        break
                except Exception:
                    continue

            # Fallback: inspect buttons in scope if targeted locators did not yield a candidate
            if not post_button_info and container_scope:
                buttons_locator = container_scope.locator("button, [role='button']")
                btn_count = await buttons_locator.count()
                logger.info(f"Inspecting {btn_count} buttons inside container scope...")
                candidate_buttons = []

                for i in range(btn_count):
                    btn = buttons_locator.nth(i)
                    try:
                        if not await btn.is_visible():
                            continue
                        text = (await btn.inner_text()).strip()
                        aria_label = (await btn.get_attribute("aria-label")) or ""
                        cls = (await btn.get_attribute("class")) or ""
                        data_ctl = (await btn.get_attribute("data-control-name")) or ""
                        is_disabled = await btn.is_disabled()
                        aria_disabled = (await btn.get_attribute("aria-disabled")) == "true"
                        disabled = is_disabled or aria_disabled

                        btn_info = {
                            "index": i,
                            "text": text,
                            "aria_label": aria_label,
                            "class": cls,
                            "data_control": data_ctl,
                            "disabled": disabled,
                            "locator": btn,
                        }
                        diagnostics_button_list.append(
                            f"Button #{i}: text='{text}', aria-label='{aria_label}', disabled={disabled}, class='{cls[:50]}'"
                        )

                        text_lower = text.lower()
                        aria_lower = aria_label.lower()
                        is_post = False
                        if text_lower == "post" or aria_lower == "post":
                            is_post = True
                        elif "share-actions__primary-action" in cls or "primary-action" in cls:
                            is_post = True
                        elif "post" in text_lower and not any(w in text_lower for w in ["start", "who can see", "schedule", "visibility"]):
                            is_post = True
                        elif "post" in aria_lower and not any(w in aria_lower for w in ["start", "who can see", "schedule", "visibility"]):
                            is_post = True

                        if is_post:
                            candidate_buttons.append(btn_info)
                    except Exception:
                        continue

                if candidate_buttons:
                    for c in candidate_buttons:
                        if not c["disabled"]:
                            post_button_info = c
                            break
                    if not post_button_info:
                        post_button_info = candidate_buttons[-1]

            # If Post button still cannot be found, save full diagnostic files
            if not post_button_info:
                diag_html = BASE_DIR / "composer_diagnostic.html"
                diag_png = BASE_DIR / "composer_diagnostic.png"
                diag_btns = BASE_DIR / "composer_buttons_diagnostic.txt"
                try:
                    all_page_btns = page.locator("button, [role='button']")
                    all_count = await all_page_btns.count()
                    for idx in range(min(all_count, 30)):
                        b_cand = all_page_btns.nth(idx)
                        if await b_cand.is_visible():
                            t = (await b_cand.inner_text()).strip()
                            al = (await b_cand.get_attribute("aria-label")) or ""
                            diagnostics_button_list.append(f"Button #{idx}: text='{t}', aria-label='{al}'")
                    content_html = await page.content()
                    diag_html.write_text(content_html, encoding="utf-8")
                    await page.screenshot(path=str(diag_png))
                    diag_btns.write_text("\n".join(diagnostics_button_list), encoding="utf-8")
                    diag_msg = f" (Saved diagnostics to {diag_html.name}, {diag_png.name}, and {diag_btns.name})"
                except Exception:
                    diag_msg = ""
                buttons_summary = "; ".join(diagnostics_button_list[:5])
                return f"Error: Could not locate the 'Post' button inside the active composer dialog. Visible buttons: [{buttons_summary}].{diag_msg}"

            post_button = post_button_info["locator"]

            # Log selected button attributes for debugging
            logger.info(
                f"Selected Post button: text='{post_button_info.get('text')}', "
                f"aria-label='{post_button_info.get('aria-label')}', "
                f"disabled={post_button_info.get('disabled')}, "
                f"class='{post_button_info.get('class', '')[:60]}'"
            )

            # Scroll into view
            await post_button.scroll_into_view_if_needed()

            # Verify button is enabled before clicking
            is_disabled = await post_button.is_disabled()
            aria_disabled = (await post_button.get_attribute("aria-disabled")) == "true"
            if is_disabled or aria_disabled:
                logger.info("Post button currently disabled, waiting for enablement...")
                try:
                    await page.wait_for_function(
                        "b => b && !b.disabled && b.getAttribute('aria-disabled') !== 'true'",
                        arg=await post_button.element_handle(),
                        timeout=8000,
                    )
                    is_disabled = await post_button.is_disabled()
                    aria_disabled = (await post_button.get_attribute("aria-disabled")) == "true"
                except Exception:
                    pass

            if is_disabled or aria_disabled:
                return "Error: The 'Post' button remained disabled. Content may not have been accepted by LinkedIn."

            # 11. Click the verified Post button
            logger.info("Clicking the Post button...")
            await post_button.click()

            # 12. Verify actual publishing success
            dialog_closed = False
            try:
                if composer_container:
                    await composer_container.wait_for(state="hidden", timeout=25000)
                    dialog_closed = True
                elif editor:
                    await editor.wait_for(state="hidden", timeout=25000)
                    dialog_closed = True
                else:
                    await page.locator("[data-sdui-screen*='ShareCompose'], div.share-creation-state, .share-box-modal").first.wait_for(state="hidden", timeout=25000)
                    dialog_closed = True
            except PlaywrightTimeoutError:
                try:
                    if editor and not await editor.is_visible():
                        dialog_closed = True
                    elif post_button and not await post_button.is_visible():
                        dialog_closed = True
                except Exception:
                    pass

            if not dialog_closed:
                # Check for LinkedIn error banner
                error_banner = page.locator("div.artdeco-inline-feedback--error, .feed-shared-error")
                if await error_banner.count() > 0 and await error_banner.first.is_visible():
                    err_msg = await error_banner.first.inner_text()
                    return f"Error from LinkedIn: {err_msg.strip()}"
                return "Error: Composer dialog did not close after clicking Post. The post may not have been published."

            # Wait briefly and log toast if visible
            await page.wait_for_timeout(2000)
            toast = page.locator("div.artdeco-toast-item, .feed-shared-toast")
            if await toast.count() > 0 and await toast.first.is_visible():
                toast_text = await toast.first.inner_text()
                logger.info(f"LinkedIn confirmation toast: {toast_text.strip()}")

            return "LinkedIn post published successfully."

        except Exception as e:
            return f"Error publishing post: {str(e)}"
        finally:
            await context.close()


# ==============================================================================
# SERVER STARTUP (stdio)
# ==============================================================================
if __name__ == "__main__":
    mcp.run()
