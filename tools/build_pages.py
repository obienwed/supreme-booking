#!/usr/bin/env python3
"""Builds the SEO landing pages for lasvegaspartybuscrawl.com.

Run from the repo root:  python3 tools/build_pages.py
It writes one folder per page (e.g. las-vegas-club-crawl/index.html),
adds the "Plan your night" links to the two main pages, refreshes the
footer links everywhere, and rewrites sitemap.xml. Safe to run again.
"""
import html, json, re, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOMAIN = "https://lasvegaspartybuscrawl.com"
PHONE = "725-321-4517"
SMS = "sms:+17253214517"
TODAY = datetime.date.today().isoformat()

home = (ROOT / "index.html").read_text()
GA = re.search(r"(<!-- Google tag.*?</script>\n)", home, re.S).group(1)
DRESS = re.search(r"(  <section class=\"dress\".*?</section>)", home, re.S).group(1)
DIALOG = re.search(r"(<dialog id=\"sheet\".*?</dialog>)", home, re.S).group(1)

# ---------------------------------------------------------------- pages
# Paragraph text supports [link text](/path/) and **bold**.
PAGES = [
 dict(slug="las-vegas-club-crawl", city="vegas", tours="vegas-hiphop-club,vegas-edm-club,vegas-latin",
  nav="Club crawl",
  title="Las Vegas Club Crawl | $50, 2 Nightclubs, Free Drinks",
  desc="Las Vegas club crawl for $50, taxes and fees included: party bus with free drinks and skip-the-line entry into two nightclubs. Hip hop, EDM and Latin nights.",
  h1="Las Vegas Club Crawl",
  lead="Skip the lines, skip the cover and party on the bus between clubs. $50 a person, taxes and fees included. Pick a night and text us to book.",
  body=[
   ("What is a Las Vegas club crawl?", [
    "A club crawl is a hosted night out that takes your group to more than one nightclub in a single night. You check in, board a party bus with free drinks, and walk past the line into each club on the route with no cover charge. You don't have to plan anything, get on a guest list or argue with a door guy.",
    "It's the cheapest way to see more than one Las Vegas nightclub in a night. Paying cover at a single big Strip club on a Saturday can cost more than the whole crawl, before you've bought a drink."]),
   ("Why ours is $50", [
    "Shared club crawls in Las Vegas commonly list somewhere between about $65 and $110 a person, and many add booking fees on top at checkout. Ours is **$50 with taxes and fees already included**. The price you see is the price you pay.",
    "You get the party bus with free drinks, skip-the-line entry into two nightclubs and no cover charges. You're welcome to bring your own bottle on the bus."]),
   ("Pick your music", [
    "**[Hip Hop Club Crawl](/las-vegas-hip-hop-club-crawl/)**: our main crawl, every Thursday to Sunday.",
    "**EDM Club Crawl**: house and EDM clubs on the nights the big DJs are playing. We confirm dates by text.",
    "**Latin Club Crawl**: reggaeton, Latin and hip hop at venues like Drai's and Embassy.",
    "Want it during the day? Try the [Las Vegas pool party crawl](/las-vegas-pool-party-crawl/)."]),
   ("Who books it", [
    "Most of our groups are celebrating: [bachelorette parties](/las-vegas-bachelorette-party/), [bachelor parties](/las-vegas-bachelor-party/), [birthdays](/las-vegas-birthday-party-bus/), work trips and first-timers who want to see the clubs without the guesswork. Solo travelers and couples are welcome too."]),
  ],
  faq=[
   ("How much is a Las Vegas club crawl?", "Ours is $50 per person with taxes and fees included, and there's no cover at the clubs on the route."),
   ("How many clubs do we go to?", "Two nightclubs, plus the party bus ride with free drinks between them."),
   ("Which clubs does the crawl visit?", "The route rotates with the night and the event lineup. Past crawls have included clubs like Drai's, TAO and Marquee. We text you the night's check-in details when we confirm."),
   ("What nights does it run?", "The Hip Hop Club Crawl runs every Thursday through Sunday. EDM and Latin crawls run on select nights, and we confirm those dates by text."),
   ("Can I stay at the last club?", "Yes. Once you're in, you can stay as long as you like. Transportation back to the check-in spot isn't included."),
   ("Is a club crawl worth it?", "If you want to see more than one club in a night without paying a cover at each door or waiting in line, yes. It's also the easiest way for a big group to stay together."),
  ]),

 dict(slug="las-vegas-hip-hop-club-crawl", city="vegas", tours="vegas-hiphop-club",
  nav="Hip hop crawl",
  title="Las Vegas Hip Hop Club Crawl | $50 Party Bus, Thu–Sun",
  desc="Las Vegas hip hop club crawl: two hip hop nightclubs, a party bus with free drinks and no lines for $50, taxes and fees included. Every Thursday to Sunday.",
  h1="Las Vegas Hip Hop Club Crawl",
  lead="The only crawl built around hip hop from start to finish. Two clubs, one hour on the party bus with free drinks, and no lines. $50 a person, every Thursday to Sunday.",
  body=[
   ("Hip hop all night, not a mix", [
    "Plenty of Vegas crawls send you wherever has a table that night, so you end up at a house music club when you came for hip hop. Ours plays hip hop on the bus and takes you to clubs that play it too. Celebrity hosts and live sets happen often, and we post them on Instagram when they're booked.",
    "Supreme Club Tours has run hip hop crawls in Las Vegas for more than ten years."]),
   ("How the night goes", [
    "**Check in.** We text you the spot and time when we confirm your booking.",
    "**Party bus.** One hour on the bus with free drinks and hip hop playing. Bring your own bottle if you want; there's a quick liquor store stop early on.",
    "**Two clubs.** Skip-the-line entry into two hip hop nightclubs with no cover. Stay at the last one as long as you want."]),
   ("Every Thursday to Sunday", [
    "Thursday is the deal night. Friday and Saturday are the biggest crowds and the most likely to sell out, so book ahead on holiday weekends and fight nights. Sunday is the Vegas locals' night and usually has a big hip hop lineup."]),
  ],
  faq=[
   ("What hip hop clubs are on the crawl?", "The route depends on the night and who's performing. Drai's has been a regular stop. We text the night's details with your confirmation."),
   ("Is the hip hop crawl every night?", "It runs every Thursday, Friday, Saturday and Sunday."),
   ("Are drinks included?", "Yes, on the party bus. You can bring your own bottle too. Drinks inside the clubs are paid separately."),
   ("Can I wear Jordans?", "Yes, Jordans are fine. You still need to meet nightclub dress code: no shorts, tank tops, jerseys or athletic wear. See the [full dress code](/las-vegas-nightclub-dress-code/)."),
   ("How much is it?", "$50 per person with taxes and fees included."),
  ]),

 dict(slug="las-vegas-pool-party-crawl", city="vegas", tours="vegas-hiphop-pool,vegas-edm-pool",
  nav="Pool crawl",
  title="Las Vegas Pool Party Crawl | $50 Dayclub Crawl + Party Bus",
  desc="Las Vegas pool party crawl: two dayclubs, a party bus with free drinks and skip-the-line entry for $50, taxes and fees included. Friday to Sunday.",
  h1="Las Vegas Pool Party Crawl",
  lead="Two Vegas dayclubs in one afternoon, with the party bus and free drinks in between. $50 a person, taxes and fees included, Friday to Sunday.",
  body=[
   ("How the pool crawl works", [
    "You check in, board the party bus with free drinks, and get skip-the-line entry into two Las Vegas dayclubs and pool parties with no cover. It's the same idea as the night crawl, in the sun.",
    "Dayclubs like Ayu Dayclub have been on the route. Stops rotate with the weekend's DJ lineup and we text your check-in details when we confirm."]),
   ("Hip hop or EDM", [
    "**Hip Hop Pool Crawl**: Friday through Sunday, hip hop on the bus and at the pools.",
    "**EDM Pool Crawl**: built around the big EDM pool party lineups. Runs on select days; we confirm by text."]),
   ("Pool season", [
    "Las Vegas pool parties run in the warm months, generally spring through early fall. Holiday weekends like Memorial Day, the Fourth of July and Labor Day sell out first. Outside pool season, the [night club crawl](/las-vegas-club-crawl/) runs all year."]),
   ("What to bring", [
    "Swimwear with a cover-up, sunscreen, sunglasses, a valid ID and a small bag. Dayclubs are stricter about bags than nightclubs, so leave the big tote in the room. Swimwear is fine at the pool; on the bus and at the door, wear the cover-up."]),
  ],
  faq=[
   ("How much is the Las Vegas pool crawl?", "$50 per person with taxes and fees included. No cover at the dayclubs on the route."),
   ("What days does the pool crawl run?", "The Hip Hop Pool Crawl runs Friday through Sunday during pool season. The EDM Pool Crawl runs on select days."),
   ("How many pool parties do we go to?", "Two dayclubs, plus the party bus with free drinks."),
   ("Do I need to be 21?", "Yes. Every guest must be 21 or older with a valid government-issued ID."),
   ("Is there a pool crawl in winter?", "Las Vegas pools close for the cooler months. The night club crawl runs all year."),
  ]),

 dict(slug="las-vegas-bachelorette-party", city="vegas", tours="vegas-hiphop-club,vegas-hiphop-pool",
  nav="Bachelorette",
  title="Las Vegas Bachelorette Party Bus Club Crawl | $50 a Person",
  desc="Las Vegas bachelorette party bus: free drinks on the bus, skip-the-line entry into two nightclubs, no cover. $50 a person, taxes and fees included.",
  h1="Las Vegas Bachelorette Party Bus",
  lead="The whole group on one party bus, into two clubs with no lines and no cover. $50 a person, so nobody's paying bride-tax. Text us to book.",
  body=[
   ("Why bachelorettes book the crawl", [
    "Getting eight to fifteen women into a Strip nightclub on a Saturday usually means a long line, a guest list that may or may not work, or a table minimum someone has to cover. The crawl skips all of that. Everyone's on the bus, everyone gets in, and it's one simple price per person.",
    "At $50 each with taxes and fees included, it's easy to split, and no one gets stuck fronting a table."]),
   ("Plan the weekend", [
    "**Friday night:** [Hip Hop Club Crawl](/las-vegas-hip-hop-club-crawl/), two clubs and the party bus.",
    "**Saturday day:** [pool party crawl](/las-vegas-pool-party-crawl/), two dayclubs with free drinks on the bus (pool season).",
    "**Saturday night:** go again, or let us know if you'd like a table at a club on the route.",
    "Select **Bachelorette** as the occasion in the booking form and tell us your group size. We'll make sure the bride is taken care of."]),
   ("Tips from groups we've hosted", [
    "Book early for holiday weekends and big fight nights. Match outfits if you want, but follow the [dress code](/las-vegas-nightclub-dress-code/): heels or dressy flats, no flip flops and no big bags. Bring foldable flats for later in the night. Eat before check-in."]),
  ],
  faq=[
   ("How much is a bachelorette party bus in Las Vegas?", "Our shared party bus club crawl is $50 per person with taxes and fees included. Renting a private bus usually runs by the hour, so see our [party bus price guide](/las-vegas-party-bus-prices/) to compare."),
   ("Can the whole group ride together?", "Yes. Book under one name with the total number of ladies and guys, and your group rides and enters together."),
   ("Is there a minimum group size?", "No. Groups of every size book the crawl, from two people to large wedding parties."),
   ("Can you do something special for the bride?", "Pick Bachelorette as the occasion and add a note in the form. We'll text you about what we can set up."),
   ("Do guys get the same price?", "Yes. Every guest is $50 with taxes and fees included."),
  ]),

 dict(slug="las-vegas-bachelor-party", city="vegas", tours="vegas-hiphop-club,vegas-strip,vegas-hiphop-pool",
  nav="Bachelor",
  title="Las Vegas Bachelor Party Bus | Club Crawl & Strip Club Tour",
  desc="Las Vegas bachelor party on a party bus: club crawl, strip club tour or pool crawl with free drinks and no lines. $50 a person, taxes and fees included.",
  h1="Las Vegas Bachelor Party Bus",
  lead="Clubs, pools or strip clubs, with the party bus and free drinks between stops. $50 a guy, taxes and fees included. Text us to lock it in.",
  body=[
   ("Pick the night", [
    "**[Club crawl](/las-vegas-hip-hop-club-crawl/):** two nightclubs, skip-the-line entry, no cover. The easiest way to get a group of guys into a Vegas club, which is usually the hardest part of a bachelor weekend.",
    "**[Strip club tour](/las-vegas-strip-club-tour/):** VIP entry into top Las Vegas gentlemen's clubs with the party bus.",
    "**[Pool crawl](/las-vegas-pool-party-crawl/):** two dayclubs in the afternoon, during pool season."]),
   ("Why a crawl beats doing it yourself", [
    "All-guy groups have the hardest time at Vegas club doors. Without ladies in the group, you're usually looking at a long line, a high cover or a table minimum. On the crawl you walk in with the group, with no cover, for $50 each.",
    "Everyone pays the same, nobody has to front a deposit, and you don't need a sober planner tracking Ubers between clubs."]),
   ("Before you go", [
    "Nightclub [dress code](/las-vegas-nightclub-dress-code/) is enforced: collared or button-up shirt, dark jeans or dress pants, no shorts, jerseys or athletic wear. Jordans are fine. Everyone needs a valid ID and must be 21 or older."]),
  ],
  faq=[
   ("How much is a Las Vegas bachelor party bus?", "Our club crawl, strip club tour and pool crawl are each $50 per person, taxes and fees included."),
   ("Can an all-guy group get into the clubs?", "Yes. You walk in together with skip-the-line entry and no cover."),
   ("Can we do the club crawl and the strip club tour on the same trip?", "Yes. Many groups do the club crawl one night and the strip club tour another. Book each night separately."),
   ("Are drinks included?", "Drinks are free on the party bus, and you can bring your own bottle. Drinks inside the clubs are paid separately."),
  ]),

 dict(slug="las-vegas-birthday-party-bus", city="vegas", tours="vegas-hiphop-club,vegas-hiphop-pool",
  nav="Birthday",
  title="Las Vegas Birthday Party Bus | $50 Club Crawl, Free Drinks",
  desc="Celebrate your birthday in Las Vegas on a party bus: free drinks, two nightclubs, no lines, no cover. $50 a person, taxes and fees included.",
  h1="Las Vegas Birthday Party Bus",
  lead="Your birthday crew on the party bus, into two clubs with no lines. $50 a person, taxes and fees included. Text us and tell us whose birthday it is.",
  body=[
   ("A birthday night with no planning", [
    "Birthdays are the most common reason people book with us. Instead of picking one club, chasing a guest list and splitting Ubers, your group checks in once, rides the party bus with free drinks, and walks into two nightclubs together.",
    "Choose **Birthday** as the occasion in the booking form and put the birthday person's name in the notes."]),
   ("Night or day", [
    "**Night:** the [Hip Hop Club Crawl](/las-vegas-hip-hop-club-crawl/), Thursday to Sunday.",
    "**Day:** the [pool party crawl](/las-vegas-pool-party-crawl/), Friday to Sunday in pool season.",
    "Turning 21? The crawl is the classic first Vegas night out. Just bring a valid ID; everyone must be 21 or older."]),
   ("Group tips", [
    "Book under one name with the total count of ladies and guys. Friday and Saturday sell out first, especially on holiday weekends. Everyone needs to meet the [nightclub dress code](/las-vegas-nightclub-dress-code/), so check it before you pack."]),
  ],
  faq=[
   ("How much is a birthday party bus in Las Vegas?", "Our shared party bus club crawl is $50 per person, taxes and fees included."),
   ("Can I celebrate my 21st birthday on the crawl?", "Yes, as long as you're 21 on the night of the crawl and have a valid government-issued ID."),
   ("Do we need a minimum group size?", "No. Book any number of guests."),
   ("Can you do something for the birthday person?", "Choose Birthday as the occasion and add a note. We'll text you about what we can set up."),
  ]),

 dict(slug="las-vegas-strip-club-tour", city="vegas", tours="vegas-strip",
  nav="Strip club tour",
  title="Las Vegas Strip Club Tour | Party Bus & VIP Entry, $50",
  desc="Las Vegas strip club tour with party bus transportation and VIP entry into top gentlemen's clubs. $50 a person, taxes and fees included. 21+. Text us to book.",
  h1="Las Vegas Strip Club Tour",
  lead="VIP entry into top Las Vegas gentlemen's clubs with the party bus between stops. $50 a person, taxes and fees included. 21+ only.",
  body=[
   ("How the strip club tour works", [
    "Your group checks in, boards the party bus and gets VIP entry into Las Vegas gentlemen's clubs. Getting a group into the big clubs without paying cover and cab fare at each door is the whole point, and the bus keeps everyone together.",
    "The tour runs on select nights. Book your night and we'll confirm by text with check-in details."]),
   ("Who it's for", [
    "Mostly [bachelor parties](/las-vegas-bachelor-party/) and birthdays, plus plenty of mixed groups. Ladies are welcome."]),
   ("Rules to know", [
    "Every guest must be 21 or older with a valid government-issued ID. Dress code is smart casual: no athletic wear, jerseys or flip flops. Dances, drinks and tips inside the clubs are paid separately."]),
  ],
  faq=[
   ("How much is the Las Vegas strip club tour?", "$50 per person with taxes and fees included."),
   ("Can women go on the strip club tour?", "Yes. Mixed groups and ladies' groups book it too."),
   ("Which nights does it run?", "Select nights. Book the night you want and we confirm the date by text."),
   ("Are drinks inside the clubs included?", "No. The party bus and VIP entry are included; anything you buy inside the clubs is separate."),
  ]),

 dict(slug="las-vegas-party-bus-prices", city="vegas", tours="vegas-hiphop-club,vegas-hiphop-pool",
  nav="Party bus prices",
  title="How Much Is a Party Bus in Las Vegas? (2026 Price Guide)",
  desc="Las Vegas party bus prices: private rentals by the hour vs. shared party bus club crawls per person. What's included, what costs extra and how to save.",
  h1="How Much Is a Party Bus in Las Vegas?",
  lead="Short answer: a private party bus usually costs by the hour, while a shared party bus crawl costs per person. Here's how the two compare, and when each one makes sense.",
  body=[
   ("Private party bus rental", [
    "Renting a whole party bus in Las Vegas is usually priced by the hour. Smaller sprinter-style buses commonly run around $100 to $150 an hour, and larger party buses around $185 to $400 or more an hour, often with a two-hour minimum. Prices change with the date and the size of the bus, so always get a written quote.",
    "A rental gets you the bus and a driver. Nightclub entry, covers and drinks are usually extra. For a group of ten on a three-hour night, the bus alone often lands between about $40 and $120 a person before anyone gets into a club."]),
   ("Shared party bus crawl", [
    "A party bus crawl is priced per person and bundles the bus, drinks and club entry. Shared crawls in Las Vegas commonly list somewhere between about $65 and $110 a person. Ours is **$50 per person with taxes and fees included**, with free drinks on the bus and skip-the-line entry into two nightclubs with no cover."]),
   ("Which one should you book?", [
    "**Book a crawl** if your group wants to hit the clubs. You get the bus, drinks and entry for one flat price, and you don't have to sort out guest lists.",
    "**Rent a private bus** if you want the bus to yourselves for a set route, like a wedding, an airport pickup or a sightseeing tour of the Strip. Text us at " + PHONE + " if you'd like a quote for a private bus."]),
   ("Costs people forget", [
    "Cover charges at each club, which can be the biggest expense for all-guy groups. Driver gratuity on a private rental. Drinks inside the clubs. Fuel or cleaning surcharges on some rentals. Our crawl price already includes taxes and fees, so there's nothing added at checkout."]),
  ],
  faq=[
   ("How much does a party bus cost in Las Vegas?", "Private party bus rentals are usually priced by the hour, commonly around $100 to $400+ an hour depending on size, often with a two-hour minimum. A shared party bus club crawl is priced per person; ours is $50 with taxes and fees included."),
   ("Is a party bus cheaper than a limo in Vegas?", "Per person, usually yes, because a party bus carries more people. A shared crawl is cheaper still, since you split the bus with other groups and club entry is included."),
   ("Can you drink on a party bus in Las Vegas?", "Yes, adults 21 and over can drink on a party bus in Las Vegas. Our crawl includes free drinks on the bus, and you can bring your own bottle."),
   ("Does a party bus include club entry?", "A private rental usually doesn't. Our crawl includes skip-the-line entry into two nightclubs with no cover."),
   ("Should I tip the party bus driver?", "On a private rental, 15 to 20 percent is customary unless gratuity is already on the bill."),
  ]),

 dict(slug="las-vegas-nightclub-dress-code", city="vegas", tours="vegas-hiphop-club",
  nav="Dress code",
  title="Las Vegas Nightclub Dress Code 2026: What to Wear (Men & Women)",
  desc="What to wear to a Las Vegas nightclub: dress code for men and women, shoes, what gets you turned away at the door, and what to wear to Vegas pool parties.",
  h1="Las Vegas Nightclub Dress Code",
  lead="What gets you in and what gets you turned away at the door of a Vegas nightclub, for guys and ladies. We send groups into Strip clubs every weekend, so this is what actually works.",
  body=[
   ("Guys", [
    "**Wear:** a collared shirt, button-up or clean fitted top; dark jeans with no rips or dress pants; dress shoes, boots or clean sneakers. Jordans are fine at most hip hop clubs.",
    "**Don't wear:** shorts, tank tops, jerseys, athletic wear, sweatpants, baggy or ripped jeans, hats, or flip flops. All-guy groups get looked at harder at the door, so dress up a notch."]),
   ("Ladies", [
    "**Wear:** dresses, skirts, or a dressy going-out outfit; heels, dressy flats or sandals with straps. Bring foldable flats in a small bag for later.",
    "**Don't wear:** flip flops, athletic wear, jean shorts, or a large purse or tote. Big bags are often refused or have to be checked."]),
   ("Why people get turned away", [
    "Shoes are the number one reason. After that: athletic wear, hats, baggy clothes, and groups of guys who look underdressed. Door staff have the final call, and if you're turned away for dress code you usually don't get your money back, so it's worth getting right."]),
   ("Pool parties and dayclubs", [
    "Swimwear is expected at the pool, but you need a cover-up to walk in. Sandals are fine at dayclubs. Big bags are usually not allowed. See our [pool party crawl](/las-vegas-pool-party-crawl/) for more."]),
  ],
  faq=[
   ("Can you wear sneakers to Las Vegas nightclubs?", "At most clubs, clean fashion sneakers are fine. Athletic running shoes and dirty or beat-up sneakers usually aren't."),
   ("Can you wear Jordans to a Vegas club?", "Usually yes, especially at hip hop clubs. Pair them with dark jeans or dress pants and a collared or button-up shirt. They're fine on our crawl."),
   ("Can guys wear shorts to a Vegas nightclub?", "No. Shorts are one of the most common reasons guys are turned away."),
   ("Can I wear a hat to a Vegas club?", "Generally no. Most clubs don't allow hats."),
   ("What should I wear on a Las Vegas club crawl?", "The same as you'd wear to any Vegas nightclub, since the crawl takes you into them. For ours, Jordans are fine; shorts, jerseys and athletic wear aren't."),
  ]),

 dict(slug="miami/yacht-party", city="miami", tours="miami-yacht,miami-yacht-club",
  nav="Yacht party",
  title="Miami Yacht Party with Open Bar & Club Entry | $100",
  desc="Miami yacht party: three hours on the water with free drinks and a DJ, then the party bus to a nightclub. $100 a person, taxes and fees included. Fri–Sun.",
  h1="Miami Yacht Party",
  lead="Three hours on the water with free drinks and a DJ, and the option to keep going at a Miami nightclub after. $100 a person, taxes and fees included, Friday to Sunday.",
  body=[
   ("Two ways to do it", [
    "**Yacht Party:** three hours on the water with free drinks and a DJ.",
    "**Yacht + Club Crawl:** the same yacht party, then the party bus to a Miami nightclub with free entry. Same $100 price."]),
   ("How the night goes", [
    "Check-in starts around 9 PM. The yacht party runs about three hours, roughly 9:30 PM to 12:30 AM, then the Yacht + Club Crawl group boards the party bus to the club. We text you the exact meeting spot and times when we confirm."]),
   ("Why it's $100", [
    "Chartering a private party yacht in Miami usually costs well into the thousands for a few hours. A shared yacht party lets your group get on the water with drinks and a DJ for a fixed price per person, with taxes and fees included."]),
   ("Good for", [
    "[Bachelorette parties](/miami/bachelorette-party/), birthdays, spring break and anyone in Miami who wants one big night. Prefer the clubs? Try the [Miami hip hop club crawl](/miami/hip-hop-club-crawl/), $50 and seven nights a week."]),
  ],
  faq=[
   ("How much is a yacht party in Miami?", "Ours is $100 per person with taxes and fees included, for either the Yacht Party or the Yacht + Club Crawl."),
   ("What days are the yacht parties?", "Friday, Saturday and Sunday."),
   ("Are drinks included on the yacht?", "Yes, free drinks on the yacht."),
   ("What should I wear?", "Dress for the club, since the Yacht + Club Crawl ends at a nightclub: nightclub dress code for everyone. Ladies, bring flats for the boat."),
   ("Do I need to be 21?", "Yes. Every guest must be 21 or older with a valid government-issued ID."),
  ]),

 dict(slug="miami/hip-hop-club-crawl", city="miami", tours="miami-hiphop-club",
  nav="Hip hop crawl",
  title="Miami Hip Hop Club Crawl | $50 Party Bus, 7 Nights a Week",
  desc="Miami hip hop club crawl: check in on Ocean Drive, ride the party bus with free drinks and skip the line, no cover. $50 a person, seven nights a week.",
  h1="Miami Hip Hop Club Crawl",
  lead="Check in on Ocean Drive, ride the party bus with free drinks, and walk into Miami hip hop clubs with no line and no cover. $50 a person, seven nights a week.",
  body=[
   ("How the night goes", [
    "**Check in on Ocean Drive.** Our Miami crawl starts at Voodoo Lounge on Ocean Drive in South Beach, between about 8 and 10 PM, with drink specials at check-in.",
    "**Party bus.** Free drinks on the bus with hip hop playing.",
    "**The clubs.** Skip-the-line entry with no cover. The final club rotates by night, and we text it with your confirmation."]),
   ("Seven nights a week", [
    "Unlike most Miami crawls, ours runs every night of the week. Friday and Saturday are the biggest, and holiday weekends like Memorial Day and spring break fill up first."]),
   ("Make it a weekend", [
    "Pair the crawl with a [Miami yacht party](/miami/yacht-party/) on Friday, Saturday or Sunday. Planning for a bride? See [Miami bachelorette ideas](/miami/bachelorette-party/)."]),
  ],
  faq=[
   ("How much is the Miami club crawl?", "$50 per person with taxes and fees included."),
   ("Where does the Miami club crawl start?", "Voodoo Lounge on Ocean Drive in South Beach. We text you the exact time when we confirm."),
   ("What nights does it run?", "Every night of the week."),
   ("Is transportation back included?", "No. The party bus takes you to the club; getting back to your hotel is on your own."),
  ]),

 dict(slug="miami/bachelorette-party", city="miami", tours="miami-hiphop-club,miami-yacht-club,miami-yacht",
  nav="Bachelorette",
  title="Miami Bachelorette Party: Yacht Party & Club Crawl",
  desc="Plan a Miami bachelorette party with a yacht party, a South Beach club crawl, or both. Free drinks, no lines, no cover. From $50 a person, taxes and fees included.",
  h1="Miami Bachelorette Party",
  lead="A yacht party, a South Beach club crawl, or both in one night. Free drinks, no lines, and one simple price per person. Text us to plan the bride's weekend.",
  body=[
   ("The Miami bachelorette weekend", [
    "**Night one:** the [Miami hip hop club crawl](/miami/hip-hop-club-crawl/), $50, starting on Ocean Drive.",
    "**Night two:** the [Yacht + Club Crawl](/miami/yacht-party/), $100. Three hours on the water with free drinks and a DJ, then the party bus to a nightclub with free entry.",
    "Pick **Bachelorette** as the occasion in the booking form and tell us your group size."]),
   ("Why groups book with us", [
    "Getting a big group of women past a South Beach door, onto a boat and into a club in the same night usually takes a planner and a lot of texts. We handle the check-in, the bus and the entry, and everyone pays the same per-person price with taxes and fees included."]),
   ("Tips", [
    "Book the yacht night early since Friday to Sunday fills first. Bring flats for the boat and heels for the club. Everyone needs a valid ID and must be 21 or older."]),
  ],
  faq=[
   ("How much is a Miami bachelorette yacht party?", "Our shared yacht party is $100 per person with taxes and fees included, with free drinks and a DJ. The Yacht + Club Crawl adds club entry for the same price."),
   ("Can we do the yacht and the club in one night?", "Yes. That's the Yacht + Club Crawl, Friday through Sunday."),
   ("Is there a group minimum?", "No. Book any group size."),
   ("Do guys pay the same price?", "Yes. Prices are per person with taxes and fees included."),
  ]),
]

VEGAS_LINKS = [p for p in PAGES if p["city"] == "vegas"]
MIAMI_LINKS = [p for p in PAGES if p["city"] == "miami"]

# ---------------------------------------------------------------- helpers
def inline(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\[(.+?)\]\((/[^)]*)\)", r'<a href="\2">\1</a>', t)
    return t

def plain(text):
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    return re.sub(r"\[(.+?)\]\((/[^)]*)\)", r"\1", t)

def url_of(p):
    return f"{DOMAIN}/{p['slug']}/"

def link_grid(pages, heading, current=None):
    items = "".join(
        f'<li><a href="/{p["slug"]}/">{html.escape(p["h1"])}</a></li>'
        for p in pages if p["slug"] != current)
    return f'<nav class="links" aria-label="{html.escape(heading)}"><h2>{html.escape(heading)}</h2><ul>{items}</ul></nav>'

def footer_links():
    v = " · ".join(f'<a href="/{p["slug"]}/">{html.escape(p["nav"])}</a>' for p in VEGAS_LINKS)
    m = " · ".join(f'<a href="/{p["slug"]}/">{html.escape(p["nav"])}</a>' for p in MIAMI_LINKS)
    return (f'<!--footlinks--><p class="footlinks"><b>Las Vegas:</b> <a href="/">Party bus crawl</a> · {v}</p>'
            f'<p class="footlinks"><b>Miami:</b> <a href="/miami/">Club crawl</a> · {m}</p><!--/footlinks-->')

TOUR_PRICE = {"miami-yacht": 100, "miami-yacht-club": 100}

def page_html(p):
    city = p["city"]
    label = "Las Vegas" if city == "vegas" else "Miami"
    url = url_of(p)
    crumbs = [("Home", f"{DOMAIN}/")]
    if city == "miami":
        crumbs.append(("Miami", f"{DOMAIN}/miami/"))
    crumbs.append((p["h1"], url))
    ld = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in p["faq"]]},
        {"@context": "https://schema.org", "@type": "TouristTrip", "name": p["h1"], "description": p["desc"], "url": url,
         "touristType": "Nightlife",
         "provider": {"@type": "Organization", "name": "Supreme Club Tours", "url": "https://www.supremeclubtours.com", "telephone": "+1-" + PHONE},
         "offers": [{"@type": "Offer", "price": str(TOUR_PRICE.get(t, 50)), "priceCurrency": "USD", "url": url}
                    for t in p["tours"].split(",")][:1]},
    ]
    crumb_html = " / ".join(
        f'<a href="{u.replace(DOMAIN, "")}">{html.escape(n)}</a>' if i < len(crumbs) - 1 else f'<span>{html.escape(n)}</span>'
        for i, (n, u) in enumerate(crumbs))
    sections = ""
    for h, paras in p["body"]:
        sections += f"<h2>{html.escape(h)}</h2>" + "".join(f"<p>{inline(x)}</p>" for x in paras)
    faq = "".join(f"<details><summary>{html.escape(q)}</summary><p>{inline(a)}</p></details>" for q, a in p["faq"])
    related = link_grid(VEGAS_LINKS if city == "vegas" else MIAMI_LINKS,
                        "More Las Vegas nights" if city == "vegas" else "More Miami nights", p["slug"])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
{GA}<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(p["title"])}</title>
<meta name="description" content="{html.escape(p["desc"])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(p["title"])}">
<meta property="og:description" content="{html.escape(p["desc"])}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#1E1234">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bungee&family=Figtree:wght@400;500;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
''' + "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>\n' for x in ld) + f'''</head>
<body data-city="{city}" data-tours="{p["tours"]}">
<header>
  <div class="wrap bar">
    <a class="logo" href="/" aria-label="Supreme Club Tours, Las Vegas party bus crawl">SUPREME<small>Club Tours</small></a>
    <nav class="cities" aria-label="Choose city">
      <a href="/"{' aria-current="page"' if city == "vegas" else ""}>Las Vegas</a>
      <a href="/miami/"{' aria-current="page"' if city == "miami" else ""}>Miami</a>
    </nav>
  </div>
</header>

<main class="wrap">
  <p class="crumbs">{crumb_html}</p>
  <section class="hero">
    <h1 id="heroTitle">{html.escape(p["h1"])}</h1>
    <p id="heroSub">{inline(p["lead"])}</p>
  </section>

  <nav class="dates" id="dates" aria-label="Choose a night"></nav>
  <h2 class="day-head" id="dayHead"></h2>
  <section class="tickets" id="tickets" aria-live="polite">
    <noscript><div class="empty">Text {PHONE} to book your {label} night.</div></noscript>
  </section>

  <section class="content">
    {sections}
  </section>

{DRESS}

  <section class="content faq" aria-labelledby="faqTitle">
    <h2 id="faqTitle">FAQ</h2>
    {faq}
  </section>

  {related}

  <div class="cta-band">
    <p>Questions before you book? Text us.</p>
    <a href="{SMS}">Text {PHONE}</a>
  </div>
</main>

<footer>
  <div class="wrap">
    <p>Nightclub <a href="#dresscode">dress code</a> enforced. 21+ with valid ID. Venues are subject to change.</p>
    {footer_links()}
    <p>Questions? Text <a id="footPhone" href="#"></a>.</p>
    <p id="syncNote"></p>
  </div>
</footer>

{DIALOG}

<script src="/assets/app.js" defer></script>
</body>
</html>
'''

# ---------------------------------------------------------------- write pages
for p in PAGES:
    out = ROOT / p["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_html(p))

# ---------------------------------------------------------------- main pages: links + footer
def patch_main(path, pages, heading):
    s = path.read_text()
    block = f"<!--plan-->{link_grid(pages, heading)}<!--/plan-->"
    if "<!--plan-->" in s:
        s = re.sub(r"<!--plan-->.*?<!--/plan-->", block, s, flags=re.S)
    else:
        s = s.replace('  <section class="content faq"', f"  {block}\n\n  <section class=\"content faq\"", 1)
    if "<!--footlinks-->" in s:
        s = re.sub(r"<!--footlinks-->.*?<!--/footlinks-->", footer_links(), s, flags=re.S)
    else:
        s = s.replace('    <p id="syncNote"></p>', f"    {footer_links()}\n    <p id=\"syncNote\"></p>", 1)
    path.write_text(s)

patch_main(ROOT / "index.html", VEGAS_LINKS, "Plan your Las Vegas night")
patch_main(ROOT / "miami" / "index.html", MIAMI_LINKS, "Plan your Miami night")

# ---------------------------------------------------------------- sitemap
urls = [(f"{DOMAIN}/", "1.0"), (f"{DOMAIN}/miami/", "0.9")] + [(url_of(p), "0.8") for p in PAGES]
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for u, pr in urls)
    + "</urlset>\n")
print(f"built {len(PAGES)} pages")
