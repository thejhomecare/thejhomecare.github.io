const yearEl=document.getElementById('year');if(yearEl)yearEl.textContent=new Date().getFullYear();

(()=>{
  const path=location.pathname.endsWith('/')?location.pathname:location.pathname+'/';
  if(!path.startsWith('/cases/'))return;

  const TOTAL=28;
  const BLACK=12;

  const setCount=(selector,value)=>{const el=document.querySelector(selector);if(el)el.textContent=String(value)};
  setCount('.board-switch a span',TOTAL);
  setCount('.board-filters a[href="/cases/"] span',TOTAL);
  setCount('.board-filters a[href="/cases/category/black-stainless/"] span',BLACK);

  if(path==='/cases/'){
    const strong=document.querySelector('.board-count strong');if(strong)strong.textContent=`${TOTAL}건`;
    const list=document.querySelector('.board-list');
    if(list&&!list.querySelector('[data-case-id="S02"]')){
      list.insertAdjacentHTML('afterbegin',`<article class="board-row" data-case-id="S02"><a class="board-post" href="/cases/samgye-guji-village3-prugio-black-stainless/"><span class="post-number" aria-hidden="true">28</span><div class="post-copy"><p class="post-meta"><span class="post-category">블랙스텐망</span><span>김해 삼계동 · 구지마을3단지 푸르지오 · 부식된 망·롤러</span></p><h2>김해 삼계동 구지마을3단지 푸르지오 블랙스텐망 교체</h2><p class="post-summary">여러 곳이 찢어지고 부식된 기존 방충망을 0.14/28메쉬 블랙스텐망으로 교체하고 롤러·모헤어까지 함께 정비.</p><span class="post-read">시공사례 보기 ↗</span></div><img class="board-photo" src="/images/cases/screens/gimhae/samgye-guji-village3-prugio-black-stainless/gimhae-samgye-guji-village3-prugio-black-stainless-hero.webp" alt="김해 삼계동 구지마을3단지 푸르지오 블랙스텐망 교체 후 시야" width="1200" height="1600" loading="lazy"></a></article>`);
    }
  }

  if(path==='/cases/category/black-stainless/'){
    const strong=document.querySelector('.board-count strong');if(strong)strong.textContent=`${BLACK}건`;
    const list=document.querySelector('.board-list');
    if(list&&!list.querySelector('[data-case-id="S02"]')){
      list.insertAdjacentHTML('afterbegin',`<article class="board-row" data-case-id="S02"><a class="board-post" href="/cases/samgye-guji-village3-prugio-black-stainless/"><span class="post-number" aria-hidden="true">12</span><div class="post-copy"><p class="post-meta"><span class="post-category">블랙스텐망</span><span>김해 삼계동 · 구지마을3단지 푸르지오 · 부식된 망·롤러</span></p><h2>김해 삼계동 구지마을3단지 푸르지오 블랙스텐망 교체</h2><p class="post-summary">찢어지고 부식된 기존 망을 0.14/28메쉬 블랙스텐망으로 교체하고 녹슨 롤러와 노후 모헤어까지 정비.</p><span class="post-read">시공사례 보기 ↗</span></div><img class="board-photo" src="/images/cases/screens/gimhae/samgye-guji-village3-prugio-black-stainless/gimhae-samgye-guji-village3-prugio-black-stainless-hero.webp" alt="김해 삼계동 구지마을3단지 푸르지오 블랙스텐망 교체 완료" width="1200" height="1600" loading="lazy"></a></article>`);
    }
  }
})();