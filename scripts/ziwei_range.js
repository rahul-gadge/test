// Zi Wei decadal + annual palace activation for a list of target dates.
// Usage: node scripts/ziwei_range.js <birthDate> <timeIndex> <gender> <date> [<date> ...]
const { astro } = require('iztro');
const [birth, ti, gender, ...dates] = process.argv.slice(2);
const en = astro.bySolar(birth, parseInt(ti), gender, true, 'en-US');
const zh = astro.bySolar(birth, parseInt(ti), gender, true, 'zh-CN');
const natal = zh.palaces.map((p, i) => ({
  index: i, name_zh: p.name, name_en: en.palaces[i].name,
  majorStars: p.majorStars.map(s => s.name),
}));
const out = { natal, targets: {} };
for (const d of dates) {
  const h = en.horoscope(d);
  out.targets[d] = {
    nominal_age: h.decadal.age ? h.decadal.age.nominalAge : null,
    decadal_index: h.decadal.index,
    decadal_natal_palace_zh: natal[h.decadal.index].name_zh,
    decadal_stem: h.decadal.heavenlyStem, decadal_branch: h.decadal.earthlyBranch,
    yearly_index: h.yearly.index,
    yearly_natal_palace_zh: natal[h.yearly.index].name_zh,
    yearly_stem: h.yearly.heavenlyStem, yearly_branch: h.yearly.earthlyBranch,
    yearly_mutagen: h.yearly.mutagen,
  };
}
console.log(JSON.stringify(out, null, 1));
