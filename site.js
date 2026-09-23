const yearEl=document.getElementById('year');if(yearEl)yearEl.textContent=new Date().getFullYear();

(()=>{
  const path=location.pathname.endsWith('/')?location.pathname:location.pathname+'/';
  if(!path.startsWith('/cases/'))return;

  const counts={total:31,fine:9,black:13,entrance:5,pj:3,louver:1};
  const setCount=(selector,value)=>{const el=document.querySelector(selector);if(el)el.textContent=String(value)};

  setCount('.board-switch a span',counts.total);
  setCount('.board-filters a[href="/cases/"] span',counts.total);
  setCount('.board-filters a[href="/cases/category/fine/"] span',counts.fine);
  setCount('.board-filters a[href="/cases/category/black-stainless/"] span',counts.black);
  setCount('.board-filters a[href="/cases/category/entrance/"] span',counts.entrance);
  setCount('.board-filters a[href="/cases/category/pj-roll/"] span',counts.pj);
  setCount('.board-filters a[href="/cases/category/louver/"] span',counts.louver);

  const caseMarkup=`<article class="board-row" data-case-id="N09"><a class="board-post" href="/cases/buwon-store-entrance-roll-screen/"><span class="post-number" aria-hidden="true">${path==='/cases/category/entrance/'?'05':'31'}</span><div class="post-copy"><p class="post-meta"><span class="post-category">현관방충망</span><span>김해 부원동 · 상가 · 실버 현관롤방충망</span></p><h2>김해 부원동 상가 현관롤방충망 시공</h2><p class="post-summary">상가 출입구를 실측하고 문고리·도어클로저 등 주변 구조의 간섭 여부를 확인한 뒤 실버 프레임 현관롤방충망을 맞춤 설치.</p><span class="post-read">시공사례 보기 ↗</span></div><img class="board-photo" src="/images/cases/screens/gimhae/buwon-store-entrance-roll-screen/gimhae-buwon-store-entrance-roll-screen-hero.webp" alt="김해 부원동 상가 현관롤방충망 설치 완료" width="1200" height="1600" loading="lazy"></a></article>`;
  if(path==='/cases/'||path==='/cases/category/entrance/'){
    const list=document.querySelector('.board-list');
    if(list&&!list.querySelector('[data-case-id="N09"]'))list.insertAdjacentHTML('afterbegin',caseMarkup);
  }

  const strong=document.querySelector('.board-count strong');
  if(!strong)return;
  if(path==='/cases/'||path==='/cases/page/2/')strong.textContent=`${counts.total}건`;
  else if(path==='/cases/category/fine/')strong.textContent=`${counts.fine}건`;
  else if(path==='/cases/category/black-stainless/')strong.textContent=`${counts.black}건`;
  else if(path==='/cases/category/entrance/')strong.textContent=`${counts.entrance}건`;
  else if(path==='/cases/category/pj-roll/')strong.textContent=`${counts.pj}건`;
  else if(path==='/cases/category/louver/')strong.textContent=`${counts.louver}건`;
})();