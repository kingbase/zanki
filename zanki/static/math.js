// Ugly and will overwrite existing text, just in case of the worst
if (window.MathJax == null) {
    document.write("MathJax not loaded, maybe we should try another way ...");
}

// solution from: https://niklaskorz.de/2017/06/studying-mathematics-with-anki-and-mathjax.html
MathJax.Hub.processSectionDelay = 0;
MathJax.Hub.Config({
  messageStyle: 'none',
  tex2jax: {
      // site-packages\notebook\static\notebook\js\mathjaxutils.js
      inlineMath: [ ['$','$'], ["\\(","\\)"] ],
      displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
      processEscapes: true
    }
});

