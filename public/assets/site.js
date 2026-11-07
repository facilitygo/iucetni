(function(){
  var h=document.querySelector('header');
  if(h){
    var onScroll=function(){h.classList.toggle('scrolled',window.scrollY>8)};
    onScroll();window.addEventListener('scroll',onScroll,{passive:true});
    var mb=h.querySelector('.menu-btn');
    if(mb){
      mb.addEventListener('click',function(){var o=h.classList.toggle('open');mb.setAttribute('aria-expanded',o?'true':'false')});
      h.querySelectorAll('.nav ul a').forEach(function(a){a.addEventListener('click',function(){h.classList.remove('open');mb.setAttribute('aria-expanded','false')})});
    }
  }

  var els=document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    els.forEach(function(el){io.observe(el)});
  }else{els.forEach(function(el){el.classList.add('in')})}

  var root=document.documentElement,btn=document.getElementById('theme');
  var en=root.lang==='en',modes=['auto','light','dark'],names=en?{auto:'auto',light:'light',dark:'dark'}:{auto:'auto',light:'světlý',dark:'tmavý'},label=en?'Theme: ':'Motiv: ';
  var cur='auto';try{cur=localStorage.getItem('theme')||'auto'}catch(e){}
  var apply=function(m){if(m==='auto')root.removeAttribute('data-theme');else root.setAttribute('data-theme',m);if(btn)btn.textContent=label+names[m]};
  apply(cur);
  if(btn)btn.addEventListener('click',function(){cur=modes[(modes.indexOf(cur)+1)%3];try{localStorage.setItem('theme',cur)}catch(e){}apply(cur)});

  // příběhy – záložky
  var tabs=document.querySelectorAll('.case-tab');
  var show=function(t){tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on?'true':'false');x.tabIndex=on?0:-1;var p=document.getElementById(x.getAttribute('aria-controls'));if(p)p.hidden=!on})};
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){show(t)});
    t.addEventListener('keydown',function(e){var d=e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0;if(d){var n=tabs[(i+d+tabs.length)%tabs.length];show(n);n.focus();e.preventDefault()}});
  });

  // kopírování adresy
  document.querySelectorAll('.copy-btn').forEach(function(b){
    b.addEventListener('click',function(){var t=b.getAttribute('data-copy'),o=b.textContent;
      var done=function(){b.textContent=b.getAttribute('data-done')||'OK';setTimeout(function(){b.textContent=o},1500)};
      if(navigator.clipboard)navigator.clipboard.writeText(t).then(done,function(){});});
  });
})();
