const yearEl=document.getElementById('year');if(yearEl)yearEl.textContent=new Date().getFullYear();

(()=>{
  const path=location.pathname.endsWith('/')?location.pathname:location.pathname+'/';
  if(!path.startsWith('/cases/'))return;

  const counts={total:30,fine:9,black:13,entrance:4,pj:3,louver:1};
  const setCount=(selector,value)=>{const el=document.querySelector(selector);if(el)el.textContent=String(value)};

  setCount('.board-switch a span',counts.total);
  setCount('.board-filters a[href="/cases/"] span',counts.total);
  setCount('.board-filters a[href="/cases/category/fine/"] span',counts.fine);
  setCount('.board-filters a[href="/cases/category/black-stainless/"] span',counts.black);
  setCount('.board-filters a[href="/cases/category/entrance/"] span',counts.entrance);
  setCount('.board-filters a[href="/cases/category/pj-roll/"] span',counts.pj);
  setCount('.board-filters a[href="/cases/category/louver/"] span',counts.louver);

  const strong=document.querySelector('.board-count strong');
  if(!strong)return;
  if(path==='/cases/'||path==='/cases/page/2/')strong.textContent=`${counts.total}건`;
  else if(path==='/cases/category/fine/')strong.textContent=`${counts.fine}건`;
  else if(path==='/cases/category/black-stainless/')strong.textContent=`${counts.black}건`;
  else if(path==='/cases/category/entrance/')strong.textContent=`${counts.entrance}건`;
  else if(path==='/cases/category/pj-roll/')strong.textContent=`${counts.pj}건`;
  else if(path==='/cases/category/louver/')strong.textContent=`${counts.louver}건`;
})();