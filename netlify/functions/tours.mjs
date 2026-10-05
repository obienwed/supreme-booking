// Pulls the live tour lineup from supremeclubtours.com (Wix) and returns
// which tours are listed, their "Starts At" price, and their running days.
// Cached on Netlify's CDN for 6 hours, so the Wix site is hit ~4x a day.

const PAGES = {
  vegas: "https://www.supremeclubtours.com/lasvegas",
  miami: "https://www.supremeclubtours.com/miami",
};

// Each pattern matches the tour card heading on the city page.
const PATTERNS = {
  vegas: {
    "vegas-hiphop-club": /LAS\s+VEGAS\s+HIP\s*-?\s*HOP\s+CLUB\s+CRAWL/,
    "vegas-hiphop-pool": /LAS\s+VEGAS\s+HIP\s*-?\s*HOP\s+POOL\s+CRAWL/,
    "vegas-edm-club": /LAS\s+VEGAS\s+EDM\s+CLUB\s+CRAWL/,
    "vegas-edm-pool": /LAS\s+VEGAS\s+EDM\s+POOL\s+CRAWL/,
    "vegas-latin": /LAS\s+VEGAS\s+LATIN\s+CLUB\s+CRAWL/,
    "vegas-strip": /LAS\s+VEGAS\s+STRIP\s+CLUB\s+(?:TOURS?|CRAWL)/,
  },
  miami: {
    "miami-hiphop-club": /MIAMI\s+HIP\s*-?\s*HOP\s+CLUB\s+CRAWL/,
    "miami-yacht-club": /MIAMI\s+YACHT\s*\+\s*CLUB\s+CRAWL/,
    "miami-yacht": /MIAMI\s+YACHT\s+PARTY/,
    "miami-edm-club": /MIAMI\s+EDM\s+CLUB\s+CRAWL/,
    "miami-latin": /MIAMI\s+LATIN\s+CLUB\s+CRAWL/,
    "miami-strip": /MIAMI\s+STRIP\s*CLUB\s+CRAWL/,
  },
};

const DAY = {
  SUN: 0, SUNDAY: 0, MON: 1, MONDAY: 1, TUE: 2, TUES: 2, TUESDAY: 2,
  WED: 3, WEDNESDAY: 3, THU: 4, THUR: 4, THURS: 4, THURSDAY: 4,
  FRI: 5, FRIDAY: 5, SAT: 6, SATURDAY: 6,
};

function toText(html) {
  const body = html.split(/<body[^>]*>/i)[1] || html;
  return body
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;|&#160;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&#x27;|&#39;|&rsquo;/g, "'")
    .replace(/&[a-z#0-9]+;/gi, " ")
    .replace(/\s+/g, " ")
    .toUpperCase();
}

function parseDays(w) {
  if (/7\s*DAYS\s*A\s*WEEK|EVERY\s*NIGHT|DAILY/.test(w)) return [0, 1, 2, 3, 4, 5, 6];
  const m = w.match(/EVERY\s+([A-Z]+)\.?\s*(?:-|–|—|TO|THRU|THROUGH)\s*([A-Z]+)/);
  if (!m) return undefined;
  const a = DAY[m[1]], b = DAY[m[2]];
  if (a === undefined || b === undefined) return undefined;
  const out = [];
  for (let d = a; out.length < 7; d = (d + 1) % 7) {
    out.push(d);
    if (d === b) break;
  }
  return out;
}

function scan(text, re) {
  let best = null;
  for (const m of text.matchAll(new RegExp(re.source, "g"))) {
    const start = m.index + m[0].length;
    let w = text.slice(start, start + 220);
    const cut = w.search(/\b(LAS\s+VEGAS|MIAMI)\b/);
    if (cut > 0) w = w.slice(0, cut);
    const info = { active: true };
    const price = w.match(/STARTS?\s+AT\s+\$\s*(\d+)/);
    if (price) info.price = Number(price[1]);
    const days = parseDays(w);
    if (days) info.days = days;
    if (!best || (info.price != null && best.price == null)) best = info;
  }
  return best;
}

async function syncCity(city) {
  const res = await fetch(PAGES[city], {
    headers: { "user-agent": "Mozilla/5.0 (compatible; SupremeBookingSync/1.0)" },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const text = toText(await res.text());
  const ids = Object.keys(PATTERNS[city]);
  const tours = {};
  let found = 0;
  for (const id of ids) {
    const info = scan(text, PATTERNS[city][id]);
    if (info) { found++; tours[id] = info; } else tours[id] = { active: false };
  }
  // If most cards weren't found, Wix markup probably changed: don't hide anything.
  if (found < Math.ceil(ids.length / 2)) return { ok: false, reason: "layout-changed" };
  return { ok: true, tours };
}

export default async () => {
  const out = { syncedAt: new Date().toISOString(), cities: {} };
  await Promise.all(
    Object.keys(PAGES).map(async (city) => {
      try { out.cities[city] = await syncCity(city); }
      catch (e) { out.cities[city] = { ok: false, reason: String(e.message || e) }; }
    })
  );
  return new Response(JSON.stringify(out), {
    headers: {
      "content-type": "application/json",
      "cache-control": "public, max-age=300",
      "netlify-cdn-cache-control": "public, s-maxage=21600, stale-while-revalidate=86400",
    },
  });
};
