const { astro } = require('iztro');
const a = astro.bySolar(process.argv[2], parseInt(process.argv[3]), process.argv[4], true, 'en-US');
const z = astro.bySolar(process.argv[2], parseInt(process.argv[3]), process.argv[4], true, 'zh-CN');
const target = process.argv[5];
const h = a.horoscope(target); const hz = z.horoscope(target);
const mut = [];
a.palaces.forEach((p,i)=>{ [...p.majorStars,...p.minorStars].forEach((s,k)=>{ if(s.mutagen){
  const all=[...z.palaces[i].majorStars,...z.palaces[i].minorStars];
  mut.push({star:s.name, star_zh:all[k].name, mutagen:s.mutagen, mutagen_zh:hz? null:null,
            palace:p.name, palace_zh:z.palaces[i].name, branch:p.earthlyBranch});}});});
console.log(JSON.stringify({
  target, birth_year_stem: a.chineseDate.split(' ')[0],
  natal_mutagens: mut,
  decadal: {index:h.decadal.index, heavenlyStem:h.decadal.heavenlyStem, earthlyBranch:h.decadal.earthlyBranch,
            palaceNames:h.decadal.palaceNames, mutagen:h.decadal.mutagen, age:h.age},
  decadal_zh: {palaceNames: hz.decadal.palaceNames, mutagen: hz.decadal.mutagen},
  yearly: {index:h.yearly.index, heavenlyStem:h.yearly.heavenlyStem, earthlyBranch:h.yearly.earthlyBranch,
           palaceNames:h.yearly.palaceNames, mutagen:h.yearly.mutagen},
  yearly_zh: {palaceNames: hz.yearly.palaceNames, mutagen: hz.yearly.mutagen},
  natal_palace_at_decadal_index: {name: a.palaces[h.decadal.index].name, name_zh: z.palaces[h.decadal.index].name,
     majorStars: z.palaces[h.decadal.index].majorStars.map(s=>s.name)},
  natal_palace_at_yearly_index: {name: a.palaces[h.yearly.index].name, name_zh: z.palaces[h.yearly.index].name,
     majorStars: z.palaces[h.yearly.index].majorStars.map(s=>s.name)},
}, null, 2));
