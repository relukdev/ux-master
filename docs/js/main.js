/* ============================================
   UX Master — Main Scripts
   Scroll reveal, counters, sharing, mobile menu
   ============================================ */

// --- Scroll Reveal ---
const observer = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry, i) => {
            if (entry.isIntersecting) {
                setTimeout(() => entry.target.classList.add('visible'), i * 60);
                observer.unobserve(entry.target);
            }
        });
    },
    { threshold: 0.08, rootMargin: '0px 0px -30px 0px' }
);
document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

// --- Counter Animation ---
function animateCounters() {
    document.querySelectorAll('[data-target]').forEach((el) => {
        const target = parseInt(el.dataset.target);
        const suffix = el.dataset.suffix || '';
        const duration = 1400;
        const startTime = performance.now();

        function update(now) {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 4);
            el.textContent = Math.round(target * eased) + suffix;
            if (progress < 1) requestAnimationFrame(update);
        }

        requestAnimationFrame(update);
    });
}

const heroObserver = new IntersectionObserver(
    (entries) => {
        if (entries[0].isIntersecting) {
            animateCounters();
            heroObserver.disconnect();
        }
    },
    { threshold: 0.3 }
);

const statEl = document.querySelector('.stat-value');
if (statEl) heroObserver.observe(statEl.closest('div').parentElement);

// --- Share Functions ---
const shareText =
    'UX Master — turn any AI into a professional design studio. 838+ rules, 48 UX Laws. Free forever.';
const shareUrl = window.location.href;

function shareTwitter() {
    window.open(
        `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}&url=${encodeURIComponent(shareUrl)}`,
        '_blank'
    );
}

function shareLinkedIn() {
    window.open(
        `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(shareUrl)}`,
        '_blank'
    );
}

function copyLink() {
    navigator.clipboard.writeText(shareUrl).then(() => {
        const btn = document.getElementById('copyBtn');
        btn.textContent = 'Copied!';
        setTimeout(() => (btn.textContent = 'Copy Link'), 2000);
    });
}

// --- Mobile Menu ---
function toggleMobileMenu() {
    document.getElementById('mobileMenu').classList.toggle('open');
}

function closeMobileMenu() {
    document.getElementById('mobileMenu').classList.remove('open');
}

window.addEventListener('resize', () => {
    if (window.innerWidth >= 768) closeMobileMenu();
});

// Force dark mode
document.body.classList.remove('light-mode');
document.documentElement.classList.remove('light-mode');
localStorage.setItem('theme', 'dark');

// --- Magic Section Interaction ---
const chatBoard = document.getElementById('chatBoard');
const sidebarItems = document.querySelectorAll('.magic-sidebar-item');
let currentCase = 'generate';

function updateChat(caseKey) {
    currentCase = caseKey;
    const lang = localStorage.getItem('ux-master-lang') || 'en';
    const caseData = window.T[lang]?.magic_cases?.[caseKey];
    if (!caseData) return;

    // Remove active from others
    sidebarItems.forEach(item => item.classList.remove('active'));
    // Add active to current
    const activeItem = document.querySelector(`.magic-sidebar-item[data-case="${caseKey}"]`);
    if (activeItem) activeItem.classList.add('active');

    // Clear board and show user prompt first
    chatBoard.innerHTML = `
        <div class="tg-bubble user">
            <p>${caseData.prompt}</p>
            <div class="tg-bubble-meta">
                <span class="tg-time">${new Date().getHours()}:${String(new Date().getMinutes()).padStart(2, '0')}</span>
                <span class="tg-check">✓✓</span>
            </div>
        </div>
        <div class="typing-indicator" id="typing">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
    `;

    chatBoard.scrollTop = chatBoard.scrollHeight;

    // Simulate AI thinking
    setTimeout(() => {
        const typing = document.getElementById('typing');
        if (typing) typing.remove();

        const aiBubble = document.createElement('div');
        aiBubble.className = 'tg-bubble ai';

        // Custom inner content based on case
        let innerHTML = `<p>${caseData.response}</p>`;

        if (caseKey === 'generate') {
            innerHTML = `
                <p class="text-accent-light text-xs font-semibold mb-2">🐾 UX Master is analyzing...</p>
                <div class="ai-inner-card">
                    <div class="ai-inner-item"><span>🎨</span> <span>Glassmorphism + Soft UI</span></div>
                    <div class="ai-inner-item"><span>🎯</span> <span>Soft pink + Calming teal</span></div>
                    <div class="ai-inner-item"><span>⚖️</span> <span>Hick's Law applied</span></div>
                </div>
                <p class="mt-2">${caseData.response}</p>
            `;
        } else if (caseKey === 'audit') {
            innerHTML = `
                <p class="text-magic text-xs font-semibold mb-2">⚖️ UX Audit in progress...</p>
                <div class="ai-inner-card">
                    <div class="ai-inner-item"><span>⚠️</span> <span>Low contrast detected</span></div>
                    <div class="ai-inner-item"><span>📏</span> <span>Fitts' Law violation</span></div>
                    <div class="ai-inner-item"><span>📊</span> <span>Score: 85/100</span></div>
                </div>
                <p class="mt-2">${caseData.response}</p>
            `;
        }

        aiBubble.innerHTML = `
            ${innerHTML}
            <div class="tg-bubble-meta">
                <span class="tg-time">${new Date().getHours()}:${String(new Date().getMinutes()).padStart(2, '0')}</span>
            </div>
        `;
        chatBoard.appendChild(aiBubble);
        chatBoard.scrollTop = chatBoard.scrollHeight;
    }, 1500);
}

sidebarItems.forEach(item => {
    item.addEventListener('click', () => {
        const caseKey = item.getAttribute('data-case');
        updateChat(caseKey);
    });
});

window.addEventListener('langChanged', (e) => {
    // Silent update (no typing animation) when language changes
    const lang = e.detail.lang;
    const caseData = window.T[lang]?.magic_cases?.[currentCase];
    if (!caseData || !chatBoard) return;

    // Just update the text content of existing bubbles if possible, 
    // or just re-render immediately without delay
    updateChatSilent(currentCase, lang);
});

function updateChatSilent(caseKey, lang) {
    const caseData = window.T[lang]?.magic_cases?.[caseKey];
    if (!caseData) return;

    chatBoard.innerHTML = `
        <div class="tg-bubble user">
            <p>${caseData.prompt}</p>
            <div class="tg-bubble-meta">
                <span class="tg-time">${new Date().getHours()}:${String(new Date().getMinutes()).padStart(2, '0')}</span>
                <span class="tg-check">✓✓</span>
            </div>
        </div>
        <div class="tg-bubble ai">
            <div id="aiResponse">
                <p>${caseData.response}</p>
            </div>
            <div class="tg-bubble-meta">
                <span class="tg-time">${new Date().getHours()}:${String(new Date().getMinutes()).padStart(2, '0')}</span>
            </div>
        </div>
    `;
    chatBoard.scrollTop = chatBoard.scrollHeight;
}
