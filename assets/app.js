/* ====== SETTINGS ====== */
const BOOKING_PHONE = "+17253214517";      // guests text this number
const PRICE = 50;                           // default price per person, all-in (tours can override with price:)
const DAYS_AHEAD = 21;                      // how many nights to show
const SYNC_URL = "/.netlify/functions/tours";

/* ====== TOUR CATALOG (defaults; live site overrides price/days/listed) ====== */
const CATALOG = {
  vegas: {
    label: "Las Vegas",
    sub: "Hip hop, EDM, Latin and pool crawls on the Strip. Pick your night, choose a crawl, and text us your reservation.",
    tours: [
      { id:"vegas-hiphop-club", name:"Hip Hop Club Crawl", kind:"night", price:50, days:[4,5,6,0], time:"Night",
        perks:["2 nightclubs","1 hr party bus","Free drinks on the bus","Skip the line"] },
      { id:"vegas-hiphop-pool", name:"Hip Hop Pool Crawl", kind:"day", price:50, days:[5,6,0], time:"Day",
        perks:["2 dayclubs","Party bus","Free drinks","Skip the line"] },
      { id:"vegas-edm-club", name:"EDM Club Crawl", kind:"night", price:50, days:null, time:"Night",
        perks:["Top EDM clubs","Party bus","Free drinks"] },
      { id:"vegas-edm-pool", name:"EDM Pool Crawl", kind:"day", price:50, days:null, time:"Day",
        perks:["EDM dayclubs","Party bus","Free drinks"] },
      { id:"vegas-latin", name:"Latin Club Crawl", kind:"night", price:50, days:null, time:"Night",
        perks:["Latin nightclubs","Party bus","Champagne on the bus"] },
      { id:"vegas-strip", name:"Strip Club Tour", kind:"night", price:50, days:null, time:"Night",
        perks:["VIP entry","Party bus"] }
    ]
  },
  miami: {
    label: "Miami",
    sub: "Yacht parties, hip hop crawls and South Beach nightlife. Pick your night, choose a crawl, and text us your reservation.",
    tours: [
      { id:"miami-hiphop-club", name:"Hip Hop Club Crawl", kind:"night", price:50, days:[0,1,2,3,4,5,6], time:"Night",
        perks:["2 clubs","Party bus","Free drinks","Skip the line"] },
      { id:"miami-yacht-club", name:"Yacht + Club Crawl", kind:"yacht", price:100, days:[5,6,0], time:"Night",
        perks:["3 hr yacht party","Free drinks","Free club entry"] },
      { id:"miami-yacht", name:"Yacht Party", kind:"yacht", price:100, days:[5,6,0], time:"Night",
        perks:["3 hr yacht party","Free drinks"] },
      { id:"miami-edm-club", name:"EDM Club Crawl", kind:"night", price:50, days:null, time:"Night",
        perks:["EDM clubs","Party bus","Free drinks"] },
      { id:"miami-latin", name:"Latin Club Crawl", kind:"night", price:50, days:null, time:"Night",
        perks:["Latin clubs","Party bus","Free drinks"] },
      { id:"miami-strip", name:"Strip Club Crawl", kind:"night", price:50, days:null, time:"Night",
        perks:["VIP entry","1 hr party bus","Free drinks"] }
    ]
  }
};

/* ====== STATE ====== */
const DOW = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
const DOW_LONG = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
const MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
let city = document.body.dataset.city === "miami" ? "miami" : "vegas";
let picked = null;          // Date
let activeTour = null;
let lastMessage = "";

const $ = s => document.querySelector(s);
const prettyPhone = p => p.replace(/^\+1(\d{3})(\d{3})(\d{4})$/, "$1-$2-$3");
const keyOf = d => d.toISOString().slice(0,10);

function nights() {
  const out = [], t = new Date(); t.setHours(12,0,0,0);
  for (let i = 0; i < DAYS_AHEAD; i++) { const d = new Date(t); d.setDate(t.getDate()+i); out.push(d); }
  return out;
}
const ONLY = (document.body.dataset.tours || "").split(",").filter(Boolean);
const tours = () => CATALOG[city].tours.filter(t => t.active !== false && (!ONLY.length || ONLY.includes(t.id)));
const runsOn = (t, d) => !t.days || t.days.includes(d.getDay());
const toursOn = d => tours().filter(t => runsOn(t, d))
  .sort((a,b) => (b.days ? 1 : 0) - (a.days ? 1 : 0));
const fullDate = d => `${DOW_LONG[d.getDay()]}, ${MON[d.getMonth()]} ${d.getDate()}`;

/* ====== RENDER ====== */

function renderDates() {
  const list = nights();
  if (!picked || !list.some(d => keyOf(d) === keyOf(picked))) {
    picked = list.find(d => toursOn(d).some(t => t.days)) || list[0];
  }
  const today = keyOf(list[0]);
  $("#dates").innerHTML = list.map(d => {
    const k = keyOf(d), on = k === keyOf(picked);
    const label = k === today ? "Tonight" : "";
    return `<button type="button" class="date" data-key="${k}" aria-pressed="${on}" aria-label="${fullDate(d)}">
      <span>${DOW[d.getDay()]}</span><b>${d.getDate()}</b><em>${label}</em></button>`;
  }).join("");
  const sel = $(`.date[aria-pressed="true"]`);
  if (sel) sel.scrollIntoView({ block:"nearest", inline:"center" });
}

function priceHTML(t) {
  return `<span class="price">$${t.price ?? PRICE} <small>per person, taxes &amp; fees included</small></span>`;
}

function renderTickets() {
  const d = picked;
  $("#dayHead").textContent = `${CATALOG[city].label}: ${fullDate(d)}`;
  const list = toursOn(d);
  if (!list.length) {
    $("#tickets").innerHTML = `<div class="empty">No crawls are scheduled this night. Pick another date above, or text ${prettyPhone(BOOKING_PHONE)} for a private party bus.</div>`;
    return;
  }
  $("#tickets").innerHTML = list.map(t => `
    <article class="ticket ${t.kind}">
      <div class="stub" aria-hidden="true">
        <span class="dow">${DOW[d.getDay()]}</span><span class="num">${d.getDate()}</span><span class="mon">${MON[d.getMonth()]}</span>
      </div>
      <div class="body">
        <h3>${t.name}</h3>
        <p class="when">${CATALOG[city].label}, ${t.time.toLowerCase()} crawl</p>
        <ul class="perks">${t.perks.map(p => `<li>${p}</li>`).join("")}</ul>
        <div class="row">${priceHTML(t)}
          <button type="button" class="btn" data-book="${t.id}">Book ${DOW[d.getDay()]} ${MON[d.getMonth()]} ${d.getDate()}</button>
        </div>
        ${t.days ? "" : `<p class="flag">Runs on select nights. We'll confirm this date by text.</p>`}
      </div>
    </article>`).join("");
}

function render() { renderDates(); renderTickets(); }

/* ====== ANALYTICS ====== */
function track(name, params) {
  try { if (typeof gtag === "function") gtag("event", name, params); } catch {}
}

/* ====== BOOKING ====== */
function openSheet(id) {
  activeTour = tours().find(t => t.id === id);
  if (!activeTour) return;
  $("#form").hidden = false; $("#done").hidden = true; $("#err").textContent = "";
  $("#sheetTitle").textContent = `${CATALOG[city].label} ${activeTour.name}`;
  $("#sheetSub").textContent = `$${activeTour.price ?? PRICE} per person, taxes & fees included`;
  $("#fDate").innerHTML = nights().filter(d => runsOn(activeTour, d))
    .map(d => `<option value="${keyOf(d)}"${keyOf(d) === keyOf(picked) ? " selected" : ""}>${fullDate(d)}</option>`).join("");
  track("begin_booking", { city: CATALOG[city].label, tour: activeTour.name });
  $("#sheet").showModal();
  setTimeout(() => $("#fName").focus(), 50);
}

function smsHref(body) {
  const sep = /iPhone|iPad|iPod|Macintosh/.test(navigator.userAgent) ? "&" : "?";
  return `sms:${BOOKING_PHONE}${sep}body=${encodeURIComponent(body)}`;
}

$("#form").addEventListener("submit", e => {
  e.preventDefault();
  const name = $("#fName").value.trim();
  const ladies = Math.max(0, parseInt($("#fLadies").value, 10) || 0);
  const guys = Math.max(0, parseInt($("#fGuys").value, 10) || 0);
  if (!name) { $("#err").textContent = "Enter the name the reservation is under."; $("#fName").focus(); return; }
  if (ladies + guys < 1) { $("#err").textContent = "Add at least one guest in Ladies or Guys."; $("#fLadies").focus(); return; }
  if (!$("#fDress").checked) { $("#err").textContent = "Confirm your group will follow the nightclub dress code."; $("#fDress").focus(); return; }
  const [y,m,dd] = $("#fDate").value.split("-").map(Number);
  const date = new Date(y, m-1, dd, 12);
  const group = [ladies && `${ladies} ${ladies === 1 ? "lady" : "ladies"}`, guys && `${guys} ${guys === 1 ? "guy" : "guys"}`]
    .filter(Boolean).join(", ");
  const lines = [
    "SUPREME CLUB TOURS RESERVATION",
    `Tour: ${CATALOG[city].label} ${activeTour.name}`,
    `Date: ${fullDate(date)}`,
    `Name: ${name}`,
    `Group: ${group} (${ladies + guys} total)`,
    `Total: $${(ladies + guys) * (activeTour.price ?? PRICE)} ($${activeTour.price ?? PRICE} x ${ladies + guys}, taxes & fees included)`,
    `Occasion: ${$("#fOccasion").value}`,
    $("#fHotel").value.trim() && `Hotel: ${$("#fHotel").value.trim()}`,
    $("#fPromo").value.trim() && `Promo: ${$("#fPromo").value.trim().toUpperCase()}`,
    $("#fNotes").value.trim() && `Notes: ${$("#fNotes").value.trim()}`,
    "Dress code: confirmed"
  ].filter(Boolean);
  lastMessage = lines.join("\n") + "\n\nPlease confirm my reservation!";
  const href = smsHref(lastMessage);
  $("#msgPreview").textContent = lastMessage;
  $("#reopen").href = href;
  $("#donePhone").textContent = prettyPhone(BOOKING_PHONE);
  $("#form").hidden = true; $("#done").hidden = false;
  const guests = ladies + guys, price = activeTour.price ?? PRICE;
  track("generate_lead", { city: CATALOG[city].label, tour: activeTour.name, guests,
    value: guests * price, currency: "USD", occasion: $("#fOccasion").value });
  setTimeout(() => { window.location.href = href; }, 300);
});

$("#copy").addEventListener("click", async () => {
  try { await navigator.clipboard.writeText(lastMessage); $("#copy").textContent = "Copied"; }
  catch { $("#copy").textContent = "Select and copy above"; }
  setTimeout(() => $("#copy").textContent = "Copy message", 2500);
});

/* ====== EVENTS ====== */
document.addEventListener("click", e => {
  const d = e.target.closest(".date");
  if (d) { picked = nights().find(n => keyOf(n) === d.dataset.key); renderDates(); renderTickets(); return; }
  const b = e.target.closest("[data-book]");
  if (b) { openSheet(b.dataset.book); return; }
  if (e.target.closest("[data-close]")) $("#sheet").close();
});
$("#sheet").addEventListener("click", e => { if (e.target === $("#sheet")) $("#sheet").close(); });

/* ====== LIVE SYNC FROM SUPREMECLUBTOURS.COM ====== */
async function sync() {
  try {
    const r = await fetch(SYNC_URL, { headers: { accept: "application/json" } });
    if (!r.ok) throw 0;
    const data = await r.json();
    let synced = false;
    for (const [c, info] of Object.entries(data.cities || {})) {
      if (!info.ok || !CATALOG[c]) continue;
      synced = true;
      for (const t of CATALOG[c].tours) {
        const live = info.tours[t.id];
        if (!live) continue;
        t.active = live.active;
        if (live.days) t.days = live.days;
      }
    }
    if (synced && data.syncedAt) {
      const s = new Date(data.syncedAt);
      $("#syncNote").textContent = `Tour lineup synced from supremeclubtours.com on ${MON[s.getMonth()]} ${s.getDate()}.`;
    }
    render();
  } catch { /* offline or local preview: catalog defaults stay */ }
}

$("#footPhone").textContent = prettyPhone(BOOKING_PHONE);
$("#footPhone").href = `sms:${BOOKING_PHONE}`;
render();
sync();
