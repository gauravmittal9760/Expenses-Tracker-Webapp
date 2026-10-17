/*
 * SpendWise dark / light theme. Loaded in <head> of every page so the saved
 * choice applies before first paint. The round moon/sun button is drawn only
 * on pages whose <body> has data-theme-toggle (user + admin dashboards).
 * Light mode inverts the page colours, rotates the hue back (blues stay
 * blue) and re-inverts photos/videos. Choice is stored per browser.
 */
(function () {
  var KEY = "spendwise-theme", root = document.documentElement;
  function saved() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function save(m) { try { localStorage.setItem(KEY, m); } catch (e) {} }
  function apply(m) { if (m === "light") root.classList.add("light-mode"); else root.classList.remove("light-mode"); }
  apply(saved() === "light" ? "light" : "dark");

  var css =
    "html.light-mode{filter:invert(1) hue-rotate(180deg);background:#fff}" +
    "html.light-mode img,html.light-mode video,html.light-mode .no-invert{filter:invert(1) hue-rotate(180deg)}" +
    "#themeToggle{position:fixed;top:16px;right:20px;width:44px;height:44px;border-radius:50%;" +
    "border:1px solid rgba(255,255,255,.28);background:rgba(15,23,42,.92);color:#fde68a;cursor:pointer;" +
    "z-index:99999;display:flex;align-items:center;justify-content:center;padding:0;" +
    "box-shadow:0 4px 14px rgba(0,0,0,.45);transition:transform .2s,box-shadow .2s}" +
    "#themeToggle:hover{transform:scale(1.1);box-shadow:0 6px 18px rgba(0,0,0,.55)}#themeToggle svg{display:block}";
  var style = document.createElement("style"); style.textContent = css; (document.head || root).appendChild(style);

  var MOON = '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
  var SUN = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.5" fill="currentColor"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg>';

  document.addEventListener("DOMContentLoaded", function () {
    if (!document.body || !document.body.hasAttribute("data-theme-toggle")) return;
    var btn = document.createElement("button");
    btn.id = "themeToggle"; btn.type = "button"; btn.className = "no-invert";
    btn.setAttribute("aria-label", "Toggle dark / light mode");
    function render() { btn.innerHTML = root.classList.contains("light-mode") ? SUN : MOON; }
    btn.addEventListener("click", function () {
      var toLight = !root.classList.contains("light-mode");
      apply(toLight ? "light" : "dark"); save(toLight ? "light" : "dark"); render();
    });
    render(); document.body.appendChild(btn);
  });
})();