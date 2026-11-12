import { Link, useRouterState } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { useVisibleLinks } from "@/components/site-header";

// Primary destinations on a phone. Anything not listed stays in the account menu. Role filtering comes from useVisibleLinks.
const PRIORITY = ["/dashboard", "/my-research", "/reviews", "/admin", "/certificates", "/profile"];
// Pages with their own bottom action bar, or no signed-in chrome.
const HIDE_ON = ["/submit", "/auth"];

/** Bottom navigation for signed-in users below md. Hides while a field is focused so it never rides above the keyboard. */
export function MobileNav() {
  const path = useRouterState({ select: (s) => s.location.pathname });
  const all = useVisibleLinks();
  const [typing, setTyping] = useState(false);
  useEffect(() => {
    const isField = (t: EventTarget | null) => t instanceof HTMLElement && (t.isContentEditable || ["INPUT", "TEXTAREA", "SELECT"].includes(t.tagName));
    const on = (e: FocusEvent) => setTyping(isField(e.target));
    const off = () => setTyping(false);
    window.addEventListener("focusin", on);
    window.addEventListener("focusout", off);
    return () => { window.removeEventListener("focusin", on); window.removeEventListener("focusout", off); };
  }, []);

  const seen = new Set<string>();
  const items = PRIORITY.flatMap((to) => {
    const l = all.find((x) => x.to === to);
    if (!l || seen.has(to)) return [];
    seen.add(to);
    return [l];
  }).slice(0, 5);

  if (items.length < 2 || typing || HIDE_ON.some((h) => path === h || path.startsWith(h + "/"))) return null;
  return (
    <nav aria-label="Primary" className="fixed inset-x-0 bottom-0 z-40 border-t border-border bg-background/95 pb-[env(safe-area-inset-bottom)] md:hidden">
      <ul className="mx-auto grid max-w-md" style={{ gridTemplateColumns: `repeat(${items.length}, minmax(0, 1fr))` }}>
        {items.map(({ to, label, icon: Icon }) => {
          const active = path === to || path.startsWith(to + "/");
          return (
            <li key={to}>
              <Link to={to} aria-current={active ? "page" : undefined}
                className={`flex min-h-14 flex-col items-center justify-center gap-1 px-1 text-[11px] font-medium no-underline transition-colors duration-150 ${active ? "text-primary" : "text-muted-foreground hover:text-foreground"}`}>
                <Icon className="size-5 shrink-0" aria-hidden="true" />
                <span className="max-w-full break-words text-center leading-tight">{label.replace(/^My /, "")}</span>
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
