// node examples/rate.mjs USD EUR [bank]
const [source = 'USD', target = 'EUR', bank = 'ecb'] = process.argv.slice(2);
const url = `https://allratestoday.com/api/open/central-bank/${bank}?source=${source}&target=${target}`;
const r = await fetch(url).then((r) => r.json());
if (r.error) throw new Error(r.error);
console.log(`1 ${r.source} = ${r.rate} ${r.target} (${r.bank.toUpperCase()}, ${r.rate_date}${r.derived ? ', derived' : ''})`);
