/* eslint-disable no-undef, no-restricted-globals, no-case-declarations */
importScripts('./scripts/vendor/ok-metax-crypto.umd.js');
importScripts('./scripts/vendor/ok-metax-base.umd.js');
importScripts('./scripts/vendor/ok-metax-signlayer.umd.js');
importScripts('./scripts/vendor/ok-metax-bitcoin.umd.js');

self['ok-metax-signlayer'].register(
  0,
  new self['ok-metax-bitcoin'].BtcWallet()
);

// self['ok-metax-signlayer'].register(
//   1,
//   new self['ok-metax-bitcoin'].TBtcWallet()
// );

onmessage = async ({ data }) => {
  const { id, method, args } = data;
  const onResponse = (error, payload) => {
    postMessage({
      id,
      payload,
      error,
    });
  };

  try {
    switch (method) {
      case 'genRsaPair':
        const result = await self['ok-metax-signlayer'].GenRSAKeyForQRCode();
        onResponse(null, result);
        break;
      case 'signTransaction':
        try {
          const transactionSigned = await self[
            'ok-metax-signlayer'
          ].signTransaction(...args);
          onResponse(null, transactionSigned);
        } catch (_) {
          onResponse('signTransaction failed', null);
        }
        break;
      case 'inscribeForMPCUnsigned':
        try {
          const transactionSigned = await self[
            'ok-metax-bitcoin'
          ].inscribeForMPCUnsigned(...args);
          onResponse(null, transactionSigned);
        } catch (_) {
          onResponse('inscribeForMPCUnsigned failed', null);
        }
        break;
      case 'inscribeForMPCSigned':
        try {
          const transactionSigned = await self[
            'ok-metax-bitcoin'
          ].inscribeForMPCSigned(...args);
          onResponse(null, transactionSigned);
        } catch (_) {
          onResponse('inscribeForMPCSigned failed', null);
        }
        break;
      default:
        onResponse('mismatch action', null);
    }
  } catch (e) {
    onResponse(e, null);
  }
};
