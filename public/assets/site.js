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
  var modes=['auto','light','dark'],names={auto:'auto',light:'světlý',dark:'tmavý'};
  var cur='auto';try{cur=localStorage.getItem('theme')||'auto'}catch(e){}
  var apply=function(m){if(m==='auto')root.removeAttribute('data-theme');else root.setAttribute('data-theme',m);if(btn)btn.textContent='Motiv: '+names[m]};
  apply(cur);
  if(btn)btn.addEventListener('click',function(){cur=modes[(modes.indexOf(cur)+1)%3];try{localStorage.setItem('theme',cur)}catch(e){}apply(cur)});
})();
