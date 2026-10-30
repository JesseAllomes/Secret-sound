// Bendigo only: print the text of Triple M Bendigo's Secret Sound page (clues, wrong guesses, jackpot). No audio.
// The site asks for a station first: pick Triple M Bendigo, then open the competition page.
//   node tools/bendigo_page.js
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://triplem.listnr.com/stations/', { waitUntil: 'networkidle', timeout: 90000 });
  await page.getByText('Triple M Bendigo 93.5', { exact: true }).first().click();
  await page.waitForLoadState('networkidle');
  await page.goto('https://triplem.listnr.com/w/bendigo/secret-sound-2026', { waitUntil: 'networkidle', timeout: 90000 });
  await page.waitForTimeout(4000);
  console.log(page.url());
  console.log(await page.evaluate(() => document.body.innerText));
  await browser.close();
})();
