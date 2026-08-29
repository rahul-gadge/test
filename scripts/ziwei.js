const { astro } = require('iztro');
const [dateStr, timeIndex, gender] = [process.argv[2], parseInt(process.argv[3]), process.argv[4]];
const a = astro.bySolar(dateStr, timeIndex, gender, true, 'en-US');
const z = astro.bySolar(dateStr, timeIndex, gender, true, 'zh-CN');
const out = {
  implementation: 'iztro (canonical JavaScript)', version: require('iztro/package.json').version,
  input: { solarDate: dateStr, timeIndex, gender, fixLeap: true },
  meta: {
    solarDate: a.solarDate, lunarDate: a.lunarDate, chineseDate: a.chineseDate,
    time: a.time, timeRange: a.timeRange, sign: a.sign, zodiac: a.zodiac,
    earthlyBranchOfSoulPalace: a.earthlyBranchOfSoulPalace,
    earthlyBranchOfBodyPalace: a.earthlyBranchOfBodyPalace,
    soul: a.soul, body: a.body, fiveElementsClass: a.fiveElementsClass,
  },
  meta_zh: {
    lunarDate: z.lunarDate, chineseDate: z.chineseDate, soul: z.soul, body: z.body,
    fiveElementsClass: z.fiveElementsClass, sign: z.sign, zodiac: z.zodiac,
  },
  palaces: a.palaces.map((p, i) => ({
    index: i, name: p.name, name_zh: z.palaces[i].name,
    isBodyPalace: p.isBodyPalace, isOriginalPalace: p.isOriginalPalace,
    heavenlyStem: p.heavenlyStem, earthlyBranch: p.earthlyBranch,
    majorStars: p.majorStars.map((s, k) => ({ name: s.name, name_zh: z.palaces[i].majorStars[k].name,
      type: s.type, brightness: s.brightness, mutagen: s.mutagen || null })),
    minorStars: p.minorStars.map((s, k) => ({ name: s.name, name_zh: z.palaces[i].minorStars[k].name,
      type: s.type, brightness: s.brightness, mutagen: s.mutagen || null })),
    adjectiveStars: p.adjectiveStars.map(s => s.name),
    changsheng12: p.changsheng12, boshi12: p.boshi12, jiangqian12: p.jiangqian12, suiqian12: p.suiqian12,
    decadal: p.decadal, ages: p.ages,
  })),
};
console.log(JSON.stringify(out, null, 2));
