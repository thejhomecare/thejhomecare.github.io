const yearEl=document.getElementById('year');if(yearEl)yearEl.textContent=new Date().getFullYear();

(()=>{
  const path=location.pathname.endsWith('/')?location.pathname:location.pathname+'/';
  if(!path.startsWith('/cases/'))return;

  const counts={total:34,fine:10,black:14,entrance:6,pj:3,louver:1};
  const setCount=(selector,value)=>{const el=document.querySelector(selector);if(el)el.textContent=String(value)};

  setCount('.board-switch a span',counts.total);
  setCount('.board-filters a[href="/cases/"] span',counts.total);
  setCount('.board-filters a[href="/cases/category/fine/"] span',counts.fine);
  setCount('.board-filters a[href="/cases/category/black-stainless/"] span',counts.black);
  setCount('.board-filters a[href="/cases/category/entrance/"] span',counts.entrance);
  setCount('.board-filters a[href="/cases/category/pj-roll/"] span',counts.pj);
  setCount('.board-filters a[href="/cases/category/louver/"] span',counts.louver);

  const buwonMarkup=`<article class="board-row" data-case-id="N09"><a class="board-post" href="/cases/buwon-store-entrance-roll-screen/"><span class="post-number" aria-hidden="true">${path==='/cases/category/entrance/'?'05':'31'}</span><div class="post-copy"><p class="post-meta"><span class="post-category">현관방충망</span><span>김해 부원동 · 상가 · 실버 현관롤방충망</span></p><h2>김해 부원동 상가 현관롤방충망 시공</h2><p class="post-summary">상가 출입구를 실측하고 문고리·도어클로저 등 주변 구조의 간섭 여부를 확인한 뒤 실버 프레임 현관롤방충망을 맞춤 설치.</p><span class="post-read">시공사례 보기 ↗</span></div><img class="board-photo" src="/images/cases/screens/gimhae/buwon-store-entrance-roll-screen/gimhae-buwon-store-entrance-roll-screen-hero.webp" alt="김해 부원동 상가 현관롤방충망 설치 완료" width="1200" height="1600" loading="lazy"></a></article>`;
  if(path==='/cases/'||path==='/cases/category/entrance/'){
    const list=document.querySelector('.board-list');
    if(list&&!list.querySelector('[data-case-id="N09"]'))list.insertAdjacentHTML('afterbegin',buwonMarkup);
  }

  const n12Markup=`<article class="board-row" data-case-id="N12"><a class="board-post" href="/cases/gusan-ijin-castle2-black-stainless/"><span class="post-number" aria-hidden="true">${path==='/cases/category/black-stainless/'?'14':'32'}</span><div class="post-copy"><p class="post-meta"><span class="post-category">블랙스텐망</span><span>김해 구산동 · 이진캐스빌2단지 · 망 찢어짐·노후 모헤어</span></p><h2>김해 구산동 이진캐스빌2단지 블랙스텐망 교체</h2><p class="post-summary">찢어지고 보수 흔적이 있던 기존 방충망을 0.14/28메쉬 블랙스텐망으로 교체하고 노후 모헤어와 코너 부분까지 함께 정비.</p><span class="post-read">시공사례 보기 ↗</span></div><img class="board-photo" src="/images/cases/screens/gimhae/gusan-ijin-castle2-black-stainless/gimhae-gusan-ijin-castle2-black-stainless-hero.webp" alt="김해 구산동 이진캐스빌2단지 블랙스텐망 교체 완료" width="1200" height="1600" loading="lazy"></a></article>`;
  if(path==='/cases/'||path==='/cases/category/black-stainless/'){
    const list=document.querySelector('.board-list');
    if(list&&!list.querySelector('[data-case-id="N12"]'))list.insertAdjacentHTML('afterbegin',n12Markup);
  }

  const n13Markup=`<article class="board-row" data-case-id="N13"><a class="board-post" href="/cases/naedong-entrance-roll-replacement/"><span class="post-number" aria-hidden="true">${path==='/cases/category/entrance/'?'06':'33'}</span><div class="post-copy"><p class="post-meta"><span class="post-category">현관방충망</span><span>김해 내동 · 주택 · 망 찢어짐·레일 이탈</span></p><h2>김해 내동 주택 현관롤방충망 교체</h2><p class="post-summary">망이 찢어지고 레일이 이탈한 무턱형 제품을 철거하고 화이트 프레임·미세촘촘망 현관롤방충망으로 교체, 주변 틈새까지 마감.</p><span class="post-read">시공사례 보기 ↗</span></div><img class="board-photo" src="/images/cases/screens/gimhae/naedong-entrance-roll-replacement/gimhae-naedong-entrance-roll-replacement-hero.webp" alt="김해 내동 주택 화이트 현관롤방충망 교체 완료" width="1200" height="1600" loading="lazy"></a></article>`;
  if(path==='/cases/'||path==='/cases/category/entrance/'){
    const list=document.querySelector('.board-list');
    if(list&&!list.querySelector('[data-case-id="N13"]'))list.insertAdjacentHTML('afterbegin',n13Markup);
  }

  const n14Markup=`<article class="board-row" data-case-id="N14"><a class="board-post" href="/cases/yulha-seohui-starhills-fine-screen/"><span class="post-number" aria-hidden="true">${path==='/cases/category/fine/'?'10':'34'}</span><div class="post-copy"><p class="post-meta"><span class="post-category">미세방충망</span><span>김해 율하 · 서희스타힐스 · 망 찢어짐·모헤어·롤러 정비</span></p><h2>김해 율하 서희스타힐스 미세방충망 교체</h2><p class="post-summary">찢어진 기존 알루미늄망을 미세방충망으로 교체하고, 눌리고 해진 모헤어와 작동이 좋지 않은 롤러까지 함께 정비.</p><span class="post-read">시공사례 보기 ↗</span></div><img class="board-photo" src="/images/cases/screens/gimhae/yulha-seohui-starhills-fine-screen/gimhae-yulha-seohui-starhills-fine-screen-hero.webp" alt="김해 율하 서희스타힐스 미세방충망 교체 완료" width="1200" height="1600" loading="lazy"></a></article>`;
  if(path==='/cases/'||path==='/cases/category/fine/'){
    const list=document.querySelector('.board-list');
    if(list&&!list.querySelector('[data-case-id="N14"]'))list.insertAdjacentHTML('afterbegin',n14Markup);
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