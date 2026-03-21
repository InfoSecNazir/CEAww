/**
 * University Academic Results Bot – Main JS
 * Chart rendering, dynamic loading, tab navigation.
 */

/* ── Search form UX ─────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  // Auto-focus search input on home page
  const searchInput = document.querySelector('input[name="query"]');
  if (searchInput && !searchInput.value) {
    searchInput.focus();
  }

  // Press Enter submits search
  if (searchInput) {
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.target.form && e.target.form.submit();
      }
    });
  }

  // Bootstrap tab: persist active tab in localStorage
  const tabs = document.querySelectorAll('[data-bs-toggle="tab"]');
  const savedTab = localStorage.getItem('activeResultsTab');

  if (savedTab) {
    const target = document.querySelector(`[href="${savedTab}"]`);
    if (target) {
      const tab = new bootstrap.Tab(target);
      tab.show();
    }
  }

  tabs.forEach((tab) => {
    tab.addEventListener('shown.bs.tab', (e) => {
      localStorage.setItem('activeResultsTab', e.target.getAttribute('href'));
    });
  });

  // Trigger chart rendering after charts tab is shown
  const chartsTab = document.querySelector('[href="#tab-charts"]');
  if (chartsTab) {
    chartsTab.addEventListener('shown.bs.tab', () => {
      window.dispatchEvent(new Event('resize')); // force Chart.js reflow
    });
  }

  // Animate stat numbers on scroll into view
  animateNumbers();
});

/* ── Number animation ────────────────────────────────────────── */
function animateNumbers() {
  const statNums = document.querySelectorAll('.stat-number');
  if (!statNums.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const raw = el.textContent.trim();
        const num = parseFloat(raw);
        if (!isNaN(num)) {
          countUp(el, 0, num, raw.includes('%') ? '%' : '', 600);
        }
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.3 });

  statNums.forEach((el) => observer.observe(el));
}

function countUp(el, from, to, suffix, duration) {
  const start = performance.now();
  const isFloat = to % 1 !== 0;

  function step(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const val = from + (to - from) * easeOut(progress);
    el.textContent = (isFloat ? val.toFixed(2) : Math.round(val)) + suffix;
    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

function easeOut(t) { return 1 - Math.pow(1 - t, 3); }

/* ── Chart.js global defaults ────────────────────────────────── */
if (typeof Chart !== 'undefined') {
  Chart.defaults.font.family = "'Cairo', 'Segoe UI', sans-serif";
  Chart.defaults.font.size = 13;
  Chart.defaults.color = '#495057';
  Chart.defaults.plugins.tooltip.rtl = true;
  Chart.defaults.plugins.tooltip.textDirection = 'rtl';
}

/* ── Utility: format percentage tooltip ─────────────────────── */
function percentFormatter(value) {
  return value + '%';
}

/* ── Export PDF click feedback ───────────────────────────────── */
document.addEventListener('click', (e) => {
  const link = e.target.closest('a[href*="/export/pdf/"]');
  if (link) {
    const originalText = link.innerHTML;
    link.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>جار التصدير...';
    link.classList.add('disabled');
    setTimeout(() => {
      link.innerHTML = originalText;
      link.classList.remove('disabled');
    }, 3000);
  }
});
