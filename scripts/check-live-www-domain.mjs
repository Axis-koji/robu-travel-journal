const expectedOrigin = 'https://www.axis-jp.net';
const redirectCases = [
  ['https://axis-jp.net/', `${expectedOrigin}/`],
  ['http://axis-jp.net/', `${expectedOrigin}/`],
  ['http://www.axis-jp.net/', `${expectedOrigin}/`],
  ['https://axis-jp.net/articles/europe-ees-etias-guide/', `${expectedOrigin}/articles/europe-ees-etias-guide/`],
];

const errors = [];
for (const [url, expectedLocation] of redirectCases) {
  const response = await fetch(url, { method: 'HEAD', redirect: 'manual' });
  const location = response.headers.get('location');
  if (![301, 308].includes(response.status) || location !== expectedLocation) {
    errors.push(`${url} returned ${response.status} -> ${location || '(no location)'}; expected 301/308 -> ${expectedLocation}`);
  }
}

const canonicalResponse = await fetch(`${expectedOrigin}/`, { method: 'HEAD', redirect: 'manual' });
if (canonicalResponse.status !== 200) {
  errors.push(`${expectedOrigin}/ returned ${canonicalResponse.status}; expected 200`);
}

if (errors.length) {
  console.error('Live www redirect check failed:');
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log('Live www redirects and the canonical homepage are healthy.');
