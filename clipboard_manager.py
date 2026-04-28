#!/usr/bin/env python3
import rumps
from AppKit import (
    NSPasteboard, NSPasteboardTypeString,
    NSPasteboardTypeTIFF, NSPasteboardTypePNG,
    NSImage,
)
from Foundation import NSData

MAX_ITEMS = 25
PREVIEW_LEN = 70
MAX_IMAGE_MB = 50  # skip images larger than this


def _fmt_bytes(n):
    if n < 1024:
        return f"{n} B"
    if n < 1024 ** 2:
        return f"{n // 1024} KB"
    return f"{n / 1024 ** 2:.1f} MB"


class ClipboardManager(rumps.App):
    def __init__(self):
        super().__init__("📋", quit_button=None)
        self.history = []       # list of dicts: {type, content, preview, pb_type}
        self.last_change = NSPasteboard.generalPasteboard().changeCount()
        self._rebuild_menu()

    @rumps.timer(0.5)
    def check_clipboard(self, _):
        pb = NSPasteboard.generalPasteboard()
        count = pb.changeCount()
        if count == self.last_change:
            return
        self.last_change = count

        types = pb.types()
        if not types:
            return

        item = None

        # --- Image ---
        for pb_type in (NSPasteboardTypePNG, NSPasteboardTypeTIFF):
            if pb_type in types:
                data = pb.dataForType_(pb_type)
                if data and data.length() <= MAX_IMAGE_MB * 1024 * 1024:
                    img = NSImage.alloc().initWithData_(data)
                    if img:
                        sz = img.size()
                        w, h = int(sz.width), int(sz.height)
                        kb = _fmt_bytes(data.length())
                        preview = f"🖼  {w}×{h}  ({kb})"
                        item = {"type": "image", "content": data,
                                "preview": preview, "pb_type": pb_type}
                        break

        # --- Text ---
        if item is None and NSPasteboardTypeString in types:
            text = pb.stringForType_(NSPasteboardTypeString)
            if text:
                short = text[:PREVIEW_LEN].replace("\n", "↵").replace("\r", "")
                suffix = "…" if len(text) > PREVIEW_LEN else ""
                preview = f"📝  {short}{suffix}"
                item = {"type": "text", "content": text,
                        "preview": preview, "pb_type": NSPasteboardTypeString}

        if item is None:
            return

        # Deduplicate by preview (good enough for text; images rarely exact-match)
        existing = next((i for i in self.history if i["preview"] == item["preview"]), None)
        if existing:
            self.history.remove(existing)
        self.history.insert(0, item)
        if len(self.history) > MAX_ITEMS:
            self.history.pop()

        self._rebuild_menu()

    def _rebuild_menu(self):
        self.menu.clear()
        count = len(self.history)
        self.title = f"📋 {count}" if count else "📋"

        if not self.history:
            self.menu.add(rumps.MenuItem("(clipboard is empty)"))
        else:
            for i, item in enumerate(self.history, 1):
                label = f"{i}.  {item['preview']}"
                mi = rumps.MenuItem(label, callback=self._select)
                mi.item_data = item
                self.menu.add(mi)

        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("Clear History", callback=self._clear))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("Quit", callback=rumps.quit_application))

    def _select(self, sender):
        item = sender.item_data
        pb = NSPasteboard.generalPasteboard()
        pb.clearContents()

        if item["type"] == "image":
            pb.setData_forType_(item["content"], item["pb_type"])
        else:
            pb.setString_forType_(item["content"], NSPasteboardTypeString)

        # Update change count so we don't re-ingest what we just wrote
        self.last_change = pb.changeCount()

        # Bubble to top
        if item in self.history:
            self.history.remove(item)
            self.history.insert(0, item)
            self._rebuild_menu()

    def _clear(self, _):
        self.history.clear()
        self.last_change = NSPasteboard.generalPasteboard().changeCount()
        self._rebuild_menu()


if __name__ == "__main__":
    ClipboardManager().run()
