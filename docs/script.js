// ── Scroll reveal (IntersectionObserver — no scroll event listeners) ──────────
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12, rootMargin: '0px 0px -48px 0px' }
);

document.querySelectorAll('.reveal').forEach((el, i) => {
  // Stagger siblings within the same parent slightly
  el.style.transitionDelay = `${(i % 4) * 60}ms`;
  revealObserver.observe(el);
});

// ── Copy buttons ──────────────────────────────────────────────────────────────
document.querySelectorAll('.copy-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    const text = btn.dataset.copy;
    if (!text) return;

    navigator.clipboard.writeText(text).then(() => {
      const original = btn.textContent;
      btn.textContent = 'Copied!';
      btn.classList.add('copied');
      setTimeout(() => {
        btn.textContent = original;
        btn.classList.remove('copied');
      }, 1500);
    }).catch(() => {
      // Fallback for environments without clipboard API
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.cssText = 'position:fixed;opacity:0;pointer-events:none';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      const original = btn.textContent;
      btn.textContent = 'Copied!';
      btn.classList.add('copied');
      setTimeout(() => {
        btn.textContent = original;
        btn.classList.remove('copied');
      }, 1500);
    });
  });
});

// ── Config tabs ───────────────────────────────────────────────────────────────
document.querySelectorAll('.tab-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.tab;

    // Update button states
    document.querySelectorAll('.tab-btn').forEach((b) => {
      b.classList.remove('active');
      b.setAttribute('aria-selected', 'false');
    });
    btn.classList.add('active');
    btn.setAttribute('aria-selected', 'true');

    // Update pane visibility
    document.querySelectorAll('.tab-pane').forEach((pane) => {
      pane.classList.remove('active');
    });
    const targetPane = document.getElementById(`tab-${target}`);
    if (targetPane) targetPane.classList.add('active');
  });
});

// ── File download helper (fetch + Blob, works cross-origin) ──────────────────
async function downloadFile(url, filename) {
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const blob = await res.blob();
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(a.href);
  } catch (err) {
    console.error('Download failed:', filename, err);
  }
}

// Kit definitions — each kit = array of { url, filename }
const KITS = {
  wired: [
    {
      url: 'https://raw.githubusercontent.com/Funnykid7/AirDeck-Linux/main/Wired/Arduino-Code/arduino_airdeck_wired.ino',
      filename: 'arduino_airdeck_wired.ino',
    },
    {
      url: 'https://raw.githubusercontent.com/Funnykid7/AirDeck-Linux/main/Wired/Host-Code/arduino_airdeck_wired.py',
      filename: 'arduino_airdeck_wired.py',
    },
    {
      url: 'https://raw.githubusercontent.com/Funnykid7/AirDeck-Linux/main/Wired/Host-Code/arduino_airdeck_wired_config.json',
      filename: 'arduino_airdeck_wired_config.json',
    },
  ],
  wireless: [
    {
      url: 'https://raw.githubusercontent.com/Funnykid7/AirDeck-Linux/main/Wireless/ESP8266-Code/esp8266_airdeck_wireless.ino',
      filename: 'esp8266_airdeck_wireless.ino',
    },
    {
      url: 'https://raw.githubusercontent.com/Funnykid7/AirDeck-Linux/main/Wireless/Host-Code/esp8266_airdeck_wireless_host.py',
      filename: 'esp8266_airdeck_wireless_host.py',
    },
    {
      url: 'https://raw.githubusercontent.com/Funnykid7/AirDeck-Linux/main/Wireless/Host-Code/esp8266_airdeck_wireless_config.json',
      filename: 'esp8266_airdeck_wireless_config.json',
    },
  ],
};

// "Download Kit" buttons — download all 3 files with staggered delay
document.querySelectorAll('.dl-kit-btn').forEach((btn) => {
  btn.addEventListener('click', async () => {
    const kit = KITS[btn.dataset.kit];
    if (!kit) return;

    const originalHTML = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="animation:spin .8s linear infinite"><path d="M21 12a9 9 0 11-6.219-8.56"/></svg> Downloading...`;

    for (let i = 0; i < kit.length; i++) {
      if (i > 0) await new Promise((r) => setTimeout(r, 300));
      await downloadFile(kit[i].url, kit[i].filename);
    }

    btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg> Done`;
    btn.disabled = false;
    setTimeout(() => { btn.innerHTML = originalHTML; }, 2000);
  });
});

// Individual file chips
document.querySelectorAll('.dl-file-chip').forEach((chip) => {
  chip.addEventListener('click', async () => {
    const { url, filename } = chip.dataset;
    if (!url || !filename) return;
    chip.style.opacity = '.5';
    await downloadFile(url, filename);
    chip.style.opacity = '1';
  });
});

// Spin keyframe for the loading icon
const spinStyle = document.createElement('style');
spinStyle.textContent = '@keyframes spin { to { transform: rotate(360deg); } }';
document.head.appendChild(spinStyle);

// ── Smooth anchor scroll with nav offset ─────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener('click', (e) => {
    const id = anchor.getAttribute('href').slice(1);
    if (!id) return;
    const target = document.getElementById(id);
    if (!target) return;
    e.preventDefault();
    const navHeight = 64;
    const top = target.getBoundingClientRect().top + window.scrollY - navHeight - 16;
    window.scrollTo({ top, behavior: 'smooth' });
  });
});
