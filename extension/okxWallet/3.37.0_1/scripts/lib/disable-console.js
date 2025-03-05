function noop() {
  return undefined;
}

if (
  !(
    typeof process !== 'undefined' &&
    (process.env.ASSETS_BUILD_TYPE === 'dev' ||
      process.env.ASSETS_BUILD_TYPE === 'daily')
  ) &&
  typeof console !== 'undefined'
) {
  console.log = noop;
  console.info = noop;
}
