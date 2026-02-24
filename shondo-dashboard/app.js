/**
 * Shondo Admin Dashboard — App Logic
 * Mock data, Chart.js, channel filters, dark mode, sidebar
 */

// ============ MOCK DATA ============
const CHANNELS = {
  shopee:  { name: 'Shopee',      color: '#EE4D2D' },
  tiktok:  { name: 'TikTok Shop', color: '#010101' },
  lazada:  { name: 'Lazada',      color: '#0F1689' },
  website: { name: 'Website',     color: '#3B82F6' },
  store:   { name: 'Cửa hàng',   color: '#059669' },
};

const DAYS = ['19/02','20/02','21/02','22/02','23/02','24/02','25/02'];

const REVENUE_DATA = {
  shopee:  [58, 72, 65, 80, 75, 68, 82].map(v => v * 1000000),
  tiktok:  [42, 55, 48, 62, 58, 52, 65].map(v => v * 1000000),
  lazada:  [25, 30, 28, 35, 32, 27, 33].map(v => v * 1000000),
  website: [18, 22, 19, 25, 23, 20, 24].map(v => v * 1000000),
  store:   [10, 12, 11, 14, 13, 11, 15].map(v => v * 1000000),
};

const ORDERS_DATA = [
  { id: 'SH-2602-4821', customer: 'Nguyễn Minh Anh',    channel: 'shopee',  product: 'Son Thỏi Lì Velvet 3.5g',   amount: 289000,    status: 'completed',  time: '10 phút trước' },
  { id: 'TK-2602-1093', customer: 'Trần Thị Hương',     channel: 'tiktok',  product: 'Cushion Glow SPF50+ 15g',   amount: 435000,    status: 'processing', time: '25 phút trước' },
  { id: 'LZ-2602-7743', customer: 'Phạm Văn Đức',       channel: 'lazada',  product: 'Serum HA 30ml',              amount: 520000,    status: 'shipping',   time: '1 giờ trước' },
  { id: 'WB-2602-3312', customer: 'Lê Thị Mai',         channel: 'website', product: 'Set Chăm Sóc Da 5 Bước',    amount: 1250000,   status: 'completed',  time: '1.5 giờ trước' },
  { id: 'ST-2602-9981', customer: 'Hoàng Anh Tuấn',     channel: 'store',   product: 'Kem Chống Nắng UV 50ml',    amount: 345000,    status: 'completed',  time: '2 giờ trước' },
  { id: 'SH-2602-2255', customer: 'Vũ Ngọc Linh',       channel: 'shopee',  product: 'Bộ Cọ Trang Điểm 12 cây',  amount: 680000,    status: 'pending',    time: '2.5 giờ trước' },
  { id: 'TK-2602-8844', customer: 'Đỗ Quang Huy',       channel: 'tiktok',  product: 'Tẩy Trang Micellar 400ml',  amount: 185000,    status: 'processing', time: '3 giờ trước' },
  { id: 'SH-2602-6677', customer: 'Bùi Thị Thanh',      channel: 'shopee',  product: 'Phấn Nước Matte 15g',       amount: 395000,    status: 'shipping',   time: '3.5 giờ trước' },
  { id: 'LZ-2602-1122', customer: 'Ngô Hải Yến',        channel: 'lazada',  product: 'Mặt Nạ Collagen (Hộp 10)',  amount: 290000,    status: 'completed',  time: '4 giờ trước' },
  { id: 'WB-2602-5544', customer: 'Trịnh Đình Nam',     channel: 'website', product: 'Toner AHA/BHA 150ml',       amount: 425000,    status: 'cancelled',  time: '5 giờ trước' },
];

const TOP_PRODUCTS = [
  { name: 'Son Thỏi Lì Velvet 3.5g',       channel: 'Shopee, TikTok',  revenue: 128500000, qty: 445 },
  { name: 'Cushion Glow SPF50+ 15g',        channel: 'TikTok, Lazada',  revenue: 98200000,  qty: 226 },
  { name: 'Serum Hyaluronic Acid 30ml',      channel: 'All channels',    revenue: 87600000,  qty: 168 },
  { name: 'Set Chăm Sóc Da 5 Bước',         channel: 'Website',         revenue: 75000000,  qty: 60 },
  { name: 'Kem Chống Nắng UV Shield 50ml',  channel: 'Shopee, Cửa hàng', revenue: 62400000, qty: 181 },
  { name: 'Bộ Cọ Trang Điểm Premium 12 cây', channel: 'TikTok',         revenue: 54400000,  qty: 80 },
  { name: 'Tẩy Trang Micellar Water 400ml', channel: 'Lazada, Shopee',  revenue: 48100000,  qty: 260 },
];

// ============ UTILITIES ============
function formatCurrency(n) {
  return new Intl.NumberFormat('vi-VN').format(n) + '₫';
}

function formatShort(n) {
  if (n >= 1e9) return (n / 1e9).toFixed(1) + ' tỷ';
  if (n >= 1e6) return (n / 1e6).toFixed(0) + ' tr';
  return new Intl.NumberFormat('vi-VN').format(n);
}

// ============ STATUS MAP ============
const STATUS_MAP = {
  completed:  'Hoàn thành',
  processing: 'Đang xử lý',
  shipping:   'Đang giao',
  pending:    'Chờ xác nhận',
  cancelled:  'Đã hủy',
};

// ============ DARK MODE ============
const themeToggle = document.getElementById('themeToggle');
const iconSun = themeToggle.querySelector('.icon-sun');
const iconMoon = themeToggle.querySelector('.icon-moon');

function setTheme(dark) {
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
  iconSun.style.display = dark ? 'none' : 'block';
  iconMoon.style.display = dark ? 'block' : 'none';
  localStorage.setItem('shondo-theme', dark ? 'dark' : 'light');
  // Update charts
  updateChartsTheme();
}

themeToggle.addEventListener('click', () => {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  setTheme(!isDark);
});

// Init theme
const saved = localStorage.getItem('shondo-theme');
if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
  setTheme(true);
}

// ============ SIDEBAR (Mobile) ============
const sidebar = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebarOverlay');
const menuToggle = document.getElementById('menuToggle');

menuToggle.addEventListener('click', () => {
  const isOpen = sidebar.classList.contains('open');
  sidebar.classList.toggle('open');
  sidebarOverlay.classList.toggle('active');
  menuToggle.setAttribute('aria-expanded', !isOpen);
});

sidebarOverlay.addEventListener('click', () => {
  sidebar.classList.remove('open');
  sidebarOverlay.classList.remove('active');
  menuToggle.setAttribute('aria-expanded', 'false');
});

// ============ DATE RANGE BUTTONS ============
document.querySelectorAll('.date-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.date-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});

// ============ CHANNEL FILTERS ============
const channelPills = document.querySelectorAll('.channel-pill');
const allPill = document.querySelector('.channel-pill[data-channel="all"]');

channelPills.forEach(pill => {
  pill.addEventListener('click', () => {
    const ch = pill.dataset.channel;

    if (ch === 'all') {
      const allActive = pill.classList.contains('active');
      channelPills.forEach(p => {
        if (allActive) p.classList.remove('active');
        else p.classList.add('active');
      });
    } else {
      pill.classList.toggle('active');
      // Update "all" pill
      const channelSpecific = [...channelPills].filter(p => p.dataset.channel !== 'all');
      const allChecked = channelSpecific.every(p => p.classList.contains('active'));
      if (allChecked) allPill.classList.add('active');
      else allPill.classList.remove('active');
    }

    updateDashboard();
  });
});

function getActiveChannels() {
  const active = [];
  channelPills.forEach(p => {
    if (p.dataset.channel !== 'all' && p.classList.contains('active')) {
      active.push(p.dataset.channel);
    }
  });
  return active.length === 0 ? Object.keys(CHANNELS) : active;
}

// ============ RENDER ORDERS TABLE ============
function renderOrders(channels) {
  const tbody = document.getElementById('ordersBody');
  const filtered = ORDERS_DATA.filter(o => channels.includes(o.channel));
  
  tbody.innerHTML = filtered.map(order => `
    <tr>
      <td><span class="font-mono" style="font-size:13px;font-weight:500">${order.id}</span></td>
      <td>${order.customer}</td>
      <td><span class="channel-badge ${order.channel}">${CHANNELS[order.channel].name}</span></td>
      <td>${order.product}</td>
      <td class="font-mono text-right" style="font-weight:600">${formatCurrency(order.amount)}</td>
      <td><span class="status-badge ${order.status}">${STATUS_MAP[order.status]}</span></td>
      <td style="color:var(--text-secondary);font-size:13px">${order.time}</td>
    </tr>
  `).join('');
}

// ============ RENDER TOP PRODUCTS ============
function renderTopProducts() {
  const list = document.getElementById('topProductsList');
  list.innerHTML = TOP_PRODUCTS.map((p, i) => {
    const rankClass = i === 0 ? 'top-1' : i === 1 ? 'top-2' : i === 2 ? 'top-3' : 'rest';
    return `
      <li class="product-rank-item">
        <div class="product-rank-number ${rankClass}">${i + 1}</div>
        <div class="product-rank-info">
          <div class="product-rank-name">${p.name}</div>
          <div class="product-rank-channel">${p.channel}</div>
        </div>
        <div>
          <div class="product-rank-value">${formatShort(p.revenue)}</div>
          <div class="product-rank-count">${p.qty} đã bán</div>
        </div>
      </li>
    `;
  }).join('');
}

// ============ CHARTS ============
let revenueChart, channelChart, dailyChart;

function getChartTextColor() {
  return document.documentElement.getAttribute('data-theme') === 'dark' ? '#CBD5E1' : '#64748B';
}

function getChartGridColor() {
  return document.documentElement.getAttribute('data-theme') === 'dark' ? 'rgba(71,85,105,0.3)' : 'rgba(226,232,240,0.8)';
}

function buildRevenueChart(channels) {
  const ctx = document.getElementById('revenueChart').getContext('2d');
  
  if (revenueChart) revenueChart.destroy();

  const datasets = channels.map(ch => ({
    label: CHANNELS[ch].name,
    data: REVENUE_DATA[ch],
    borderColor: CHANNELS[ch].color,
    backgroundColor: CHANNELS[ch].color + '15',
    borderWidth: 2.5,
    pointRadius: 4,
    pointHoverRadius: 6,
    pointBackgroundColor: '#FFF',
    pointBorderColor: CHANNELS[ch].color,
    pointBorderWidth: 2,
    tension: 0.35,
    fill: false,
  }));

  revenueChart = new Chart(ctx, {
    type: 'line',
    data: { labels: DAYS, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            usePointStyle: true,
            pointStyle: 'circle',
            padding: 20,
            font: { family: "'Fira Sans', sans-serif", size: 12 },
            color: getChartTextColor(),
          }
        },
        tooltip: {
          backgroundColor: 'rgba(15,23,42,0.9)',
          titleFont: { family: "'Fira Sans', sans-serif" },
          bodyFont: { family: "'Fira Code', monospace", size: 13 },
          padding: 12,
          cornerRadius: 8,
          callbacks: {
            label: ctx => `${ctx.dataset.label}: ${formatShort(ctx.raw)}`,
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { family: "'Fira Sans', sans-serif", size: 12 }, color: getChartTextColor() },
        },
        y: {
          grid: { color: getChartGridColor() },
          ticks: {
            font: { family: "'Fira Code', monospace", size: 11 },
            color: getChartTextColor(),
            callback: v => formatShort(v),
          },
          border: { display: false },
        }
      }
    }
  });
}

function buildChannelChart(channels) {
  const ctx = document.getElementById('channelChart').getContext('2d');
  
  if (channelChart) channelChart.destroy();

  const totals = channels.map(ch => REVENUE_DATA[ch].reduce((a, b) => a + b, 0));
  const colors = channels.map(ch => CHANNELS[ch].color);
  const labels = channels.map(ch => CHANNELS[ch].name);

  channelChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data: totals,
        backgroundColor: colors.map(c => c + 'CC'),
        borderColor: colors,
        borderWidth: 2,
        hoverOffset: 8,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '65%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            usePointStyle: true,
            pointStyle: 'circle',
            padding: 16,
            font: { family: "'Fira Sans', sans-serif", size: 12 },
            color: getChartTextColor(),
          }
        },
        tooltip: {
          backgroundColor: 'rgba(15,23,42,0.9)',
          titleFont: { family: "'Fira Sans', sans-serif" },
          bodyFont: { family: "'Fira Code', monospace", size: 13 },
          padding: 12,
          cornerRadius: 8,
          callbacks: {
            label: ctx => {
              const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
              const pct = ((ctx.raw / total) * 100).toFixed(1);
              return `${ctx.label}: ${formatShort(ctx.raw)} (${pct}%)`;
            }
          }
        }
      }
    }
  });
}

function buildDailyChart(channels) {
  const ctx = document.getElementById('dailyChart').getContext('2d');
  
  if (dailyChart) dailyChart.destroy();

  // Stack totals per day
  const datasets = channels.map(ch => ({
    label: CHANNELS[ch].name,
    data: REVENUE_DATA[ch],
    backgroundColor: CHANNELS[ch].color + 'BB',
    borderColor: CHANNELS[ch].color,
    borderWidth: 1,
    borderRadius: 4,
  }));

  dailyChart = new Chart(ctx, {
    type: 'bar',
    data: { labels: DAYS, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(15,23,42,0.9)',
          titleFont: { family: "'Fira Sans', sans-serif" },
          bodyFont: { family: "'Fira Code', monospace", size: 12 },
          padding: 12,
          cornerRadius: 8,
          callbacks: {
            label: ctx => `${ctx.dataset.label}: ${formatShort(ctx.raw)}`,
          }
        }
      },
      scales: {
        x: {
          stacked: true,
          grid: { display: false },
          ticks: { font: { family: "'Fira Sans', sans-serif", size: 12 }, color: getChartTextColor() },
        },
        y: {
          stacked: true,
          grid: { color: getChartGridColor() },
          ticks: {
            font: { family: "'Fira Code', monospace", size: 11 },
            color: getChartTextColor(),
            callback: v => formatShort(v),
          },
          border: { display: false },
        }
      }
    }
  });
}

// ============ CHART TYPE TOGGLE ============
document.querySelectorAll('.card-action-btn[data-chart]').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.card-action-btn[data-chart]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const channels = getActiveChannels();
    if (btn.dataset.chart === 'bar') {
      buildBarRevenueChart(channels);
    } else {
      buildRevenueChart(channels);
    }
  });
});

function buildBarRevenueChart(channels) {
  const ctx = document.getElementById('revenueChart').getContext('2d');
  if (revenueChart) revenueChart.destroy();

  const datasets = channels.map(ch => ({
    label: CHANNELS[ch].name,
    data: REVENUE_DATA[ch],
    backgroundColor: CHANNELS[ch].color + 'BB',
    borderColor: CHANNELS[ch].color,
    borderWidth: 1,
    borderRadius: 4,
  }));

  revenueChart = new Chart(ctx, {
    type: 'bar',
    data: { labels: DAYS, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            usePointStyle: true,
            pointStyle: 'circle',
            padding: 20,
            font: { family: "'Fira Sans', sans-serif", size: 12 },
            color: getChartTextColor(),
          }
        },
        tooltip: {
          backgroundColor: 'rgba(15,23,42,0.9)',
          titleFont: { family: "'Fira Sans', sans-serif" },
          bodyFont: { family: "'Fira Code', monospace", size: 13 },
          padding: 12,
          cornerRadius: 8,
          callbacks: {
            label: ctx => `${ctx.dataset.label}: ${formatShort(ctx.raw)}`,
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { family: "'Fira Sans', sans-serif", size: 12 }, color: getChartTextColor() },
        },
        y: {
          grid: { color: getChartGridColor() },
          ticks: {
            font: { family: "'Fira Code', monospace", size: 11 },
            color: getChartTextColor(),
            callback: v => formatShort(v),
          },
          border: { display: false },
        }
      }
    }
  });
}

// ============ UPDATE THEME FOR CHARTS ============
function updateChartsTheme() {
  const channels = getActiveChannels();
  // Check which chart type is active
  const activeChartBtn = document.querySelector('.card-action-btn[data-chart].active');
  const chartType = activeChartBtn ? activeChartBtn.dataset.chart : 'line';
  
  if (chartType === 'bar') {
    buildBarRevenueChart(channels);
  } else {
    buildRevenueChart(channels);
  }
  buildChannelChart(channels);
  buildDailyChart(channels);
}

// ============ UPDATE DASHBOARD ============
function updateDashboard() {
  const channels = getActiveChannels();
  renderOrders(channels);

  // Update channel card visibility
  document.querySelectorAll('.channel-card').forEach(card => {
    const ch = card.dataset.channel;
    card.style.display = channels.includes(ch) ? '' : 'none';
  });

  // Rebuild charts
  const activeChartBtn = document.querySelector('.card-action-btn[data-chart].active');
  const chartType = activeChartBtn ? activeChartBtn.dataset.chart : 'line';

  if (chartType === 'bar') {
    buildBarRevenueChart(channels);
  } else {
    buildRevenueChart(channels);
  }
  buildChannelChart(channels);
  buildDailyChart(channels);
}

// ============ ACTIVE NAV HIGHLIGHT ============
document.querySelectorAll('.nav-item').forEach(item => {
  item.addEventListener('click', e => {
    e.preventDefault();
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    item.classList.add('active');
    // Close mobile sidebar
    sidebar.classList.remove('open');
    sidebarOverlay.classList.remove('active');
  });
});

// ============ INIT ============
function init() {
  const channels = getActiveChannels();
  renderOrders(channels);
  renderTopProducts();
  buildRevenueChart(channels);
  buildChannelChart(channels);
  buildDailyChart(channels);
}

init();
