var DARK = 'dark';
var LIGHT = 'light';

function getActualTheme() {
  const darkMode = window.matchMedia('(prefers-color-scheme: dark)');
  if (darkMode.matches) {
    return DARK;
  }
  return LIGHT;
}

var theme = window.localStorage.getItem('theme');
if (!theme || theme === 'auto') {
  window.localStorage.setItem('theme', 'auto');
  theme = getActualTheme();
}

document.body.setAttribute('class', `theme-${theme}`);

var logo = document.getElementById('logo');
var logoMap = {
  DARK: `./static/images/logo-dark.svg`,
  LIGHT: `./static/images/logo-light.svg`
}
var logoSrc = logoMap[theme];
if (logo && logoSrc) {
  // @ts-ignore
  logo.src = logoSrc;
}
