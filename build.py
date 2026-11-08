# 학기초 안내자료의 교실배치도 → 수능판 길찾기 반영 + 휴대폰용 확대/이동 → index.html
import sys
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8', newline='').read()
crlf = chr(13)+chr(10) in s
s = s.replace(chr(13)+chr(10), chr(10))
def rep(old, new, n=1):
    global s
    c = s.count(old); assert c == n, (c, old[:70]); s = s.replace(old, new)

# 1) 수능판 길찾기 경로 (11/2)
rep("        const score=best+edge.weight;",
    "        // 중앙 입구에서는 좌우 계단을 피해 가운데 계단으로 올라갑니다.\n"
    "        const sideStairs=origin==='entrance-2'&&edge.kind==='stairs'&&edge.side!=='center'&&graph.nodes.get(current).building==='본관';\n"
    "        const score=best+edge.weight+(sideStairs?1000:0);")
rep("if(drawWalk(walk,segment))segment++;walk=[b];transfers.push(edge);",
    "if(drawWalk(walk,segment))segment++;walk=[b];transfers.push(edge);drawTransferLine(a,b,edge.kind);")
rep("note.textContent='빨간 화살표: 복도 이동 · 원 안의 숫자",
    "note.textContent='빨간 선: 이동 경로 · 원 안의 숫자")
# drawTransferLine: drawWalk 함수 앞에 넣음
i = s.index("  function drawWalk(")
s = s[:i] + ("  function drawTransferLine(a,b,kind) {\n"
"    // 층간 이동과 연결통로 구간도 복도 선과 이어지게 그립니다.\n"
"    const points=kind==='bridge'?[a,{x:a.x,y:b.y},b]:[a,b];\n"
"    const coords=points.map(p=>`${p.x.toFixed(2)},${p.y.toFixed(2)}`).join(' ');\n"
"    paths.append(svg('polyline',{points:coords,fill:'none',stroke:'white','stroke-width':4.7,'stroke-linejoin':'round','stroke-linecap':'round'}));\n"
"    paths.append(svg('polyline',{points:coords,fill:'none',stroke:'#bd272e','stroke-width':2,'stroke-linejoin':'round','stroke-linecap':'round'}));\n"
"  }\n") + s[i:]

# 2) 휴대폰용: 확대 배율(zoom)과 손가락 확대
rep("  function fitMap(){frame.style.setProperty('--paper-scale',Math.min(1,(scroll.clientWidth-2)/paper.offsetWidth));}",
"""  let zoom=1;const ZOOM_MAX=4;
  function fitScale(){return Math.min(1,(scroll.clientWidth-2)/paper.offsetWidth);}
  function fitMap(){frame.style.setProperty('--paper-scale',fitScale()*zoom);document.getElementById('zoom-value').textContent=Math.round(zoom*100)+'%';document.getElementById('zoom-out').disabled=zoom<=1;document.getElementById('zoom-in').disabled=zoom>=ZOOM_MAX;}
  // 확대할 때 손가락(또는 화면 가운데) 아래 지점이 제자리에 있도록 스크롤을 맞춥니다.
  function setZoom(value,cx,cy){
    value=Math.max(1,Math.min(ZOOM_MAX,value));if(Math.abs(value-zoom)<.001)return;
    const area=scroll.getBoundingClientRect();
    cx??=area.left+scroll.clientWidth/2;cy??=Math.max(area.top,0)+(Math.min(area.bottom,innerHeight)-Math.max(area.top,0))/2;
    const before=frame.getBoundingClientRect(),old=fitScale()*zoom,px=(cx-before.left)/old,py=(cy-before.top)/old;
    if(typeof closePop==='function')closePop();
    zoom=value;fitMap();
    const after=frame.getBoundingClientRect(),now=fitScale()*zoom;
    scroll.scrollLeft+=after.left+px*now-cx;window.scrollBy(0,after.top+py*now-cy);
  }
  function resetZoom(){if(zoom!==1){zoom=1;fitMap();}}
  document.getElementById('zoom-in').addEventListener('click',()=>setZoom(zoom*1.5));
  document.getElementById('zoom-out').addEventListener('click',()=>setZoom(zoom/1.5));
  document.getElementById('zoom-fit').addEventListener('click',()=>{resetZoom();scroll.scrollIntoView({block:'start',behavior:'smooth'});});
  {
    let pinch=null;const gap=t=>Math.hypot(t[0].clientX-t[1].clientX,t[0].clientY-t[1].clientY);
    scroll.addEventListener('touchstart',e=>{if(e.touches.length===2)pinch={d:gap(e.touches),z:zoom};},{passive:true});
    scroll.addEventListener('touchmove',e=>{if(!pinch||e.touches.length!==2)return;e.preventDefault();const t=e.touches;setZoom(pinch.z*gap(t)/pinch.d,(t[0].clientX+t[1].clientX)/2,(t[0].clientY+t[1].clientY)/2);},{passive:false});
    scroll.addEventListener('touchend',e=>{if(e.touches.length<2)pinch=null;});
  }""")
# 길 안내가 나오면 전체가 보이게 되돌리고, 경로 설명을 펼침
rep("  function showRoute() {\n    setStage('route');renderRoute();",
    "  function showRoute() {\n    resetZoom();setStage('route');renderRoute();routeDetails.open=true;")
rep("  function showEntrances() {\n    requestAnimationFrame(",
    "  function showEntrances() {\n    resetZoom();requestAnimationFrame(")
# 편집·버전은 주소 끝에 ?edit=1 을 붙였을 때만
rep("  new ResizeObserver(fitMap).observe(scroll);fitMap();",
    "  document.documentElement.classList.toggle('public-view',!new URLSearchParams(location.search).has('edit'));\n  new ResizeObserver(fitMap).observe(scroll);fitMap();")

# 3) 화면 요소
rep('<div class="paper-scroll" role="region"',
    '<p class="map-hint">교실을 누르면 <b>길찾기</b>를 할 수 있어요. 두 손가락으로 벌리거나 아래 <b>+</b> 단추로 크게 볼 수 있어요.</p>\n'
    '<div class="zoom-bar" role="group" aria-label="배치도 확대"><button id="zoom-out" type="button" aria-label="작게">−</button><button id="zoom-fit" type="button" aria-label="화면에 맞추기"><span id="zoom-value">100%</span></button><button id="zoom-in" type="button" aria-label="크게">+</button></div>\n'
    '<div class="paper-scroll" role="region"')
css = """
/* 2026-11-07 휴대폰용 */
.paper-scroll { touch-action:pan-x pan-y; -webkit-overflow-scrolling:touch; }
.map-hint { margin:0 0 8px; color:#4b5d70; font-size:13px; line-height:1.5; }
.zoom-bar { position:fixed; z-index:70; right:max(14px,env(safe-area-inset-right)); bottom:max(16px,env(safe-area-inset-bottom)); display:flex; align-items:center; gap:2px; padding:4px; border-radius:30px; background:#fff; box-shadow:0 4px 18px #162c4240; }
.zoom-bar button { min-width:46px; height:46px; border:0; border-radius:23px; background:#edf4fa; color:#0f3d6e; font-size:24px; font-weight:700; line-height:1; }
.zoom-bar #zoom-fit { min-width:64px; background:transparent; font-size:13px; }
.zoom-bar button:disabled { opacity:.35; }
.public-view #edit-start,.public-view #version-select { display:none!important; }
@media(max-width:500px) { .public-view .sheet-tools .room-text-controls { display:none; } }
.room-pop { min-width:170px; padding:11px 12px; }
#pop-go { padding:11px; font-size:15px; }
#pop-close { font-size:22px; padding:2px 4px; }
.route-details { padding-bottom:78px; }
.route-details>summary { font-size:14px; font-weight:700; color:#0f3d6e; }
.route-result { font-size:14px; line-height:1.75; }
.route-result h3 { font-size:16px; }
.route-result p { font-size:12.5px; }
@media(max-width:500px) { .workspace { padding-top:8px; } .guidance { position:sticky; top:6px; z-index:65; } .guidance p { font-size:13px; } .guidance button { font-size:13px; padding:6px 8px; } .sheet-tools .room-text-controls button { width:28px; height:26px; } .elevator-choices button { min-height:52px; font-size:15px; } }
@media print { .map-hint,.zoom-bar { display:none!important; } }
"""
rep("</style></head>", css + "</style></head>")
rep("<title>구월중학교 교실배치도</title>",
    '<title>구월중학교 교실배치도</title><meta name="theme-color" content="#0f3d6e"><meta name="description" content="구월중학교 교실배치도와 교실 길찾기">')
# 4) 휴대폰 길찾기: 층별 단계로 나누어 확대 (수능 앱 map-steps.js·css 그대로, 11/8)
import os
here = os.path.dirname(os.path.abspath(__file__))
steps_js = open(os.path.join(here, 'map-steps.js'), encoding='utf-8').read().replace(chr(13)+chr(10), chr(10))
steps_css = open(os.path.join(here, 'map-steps.css'), encoding='utf-8').read().replace(chr(13)+chr(10), chr(10))
panel = ('<section id="step-panel" class="step-panel" hidden aria-live="polite"><p id="step-count"></p><h3 id="step-title"></h3><p id="step-text"></p>'
         '<div class="step-nav"><button id="step-prev" type="button">이전</button><button id="step-next" type="button">다음</button></div>'
         '<div class="step-sub"><button id="step-all" type="button">전체 지도 보기</button><button id="step-share" class="share-route" type="button">길찾기 주소 공유</button></div></section>\n')
rep('<div class="paper-scroll" role="region"', panel + '<div class="paper-scroll" role="region"')
rep("paper.classList.remove('has-route');", "paper.classList.remove('has-route');hideSteps();")
rep("    state.stage=stage;paper.dataset.routeStage=stage;", "    state.stage=stage;paper.dataset.routeStage=stage;setRouteUrl();")
rep("paper.classList.add('has-route');routeDetails.hidden=false;",
    "paper.classList.add('has-route');routeDetails.hidden=false;"
    "result.append(shareBox());setRouteUrl();showSteps(route,room);")
i = s.index('  function renderRoute() {')
s = s[:i] + steps_js + s[i:]
# 단계 보기 중에는 지도 위치를 단계가 정하므로 지도로 스크롤하지 않고, 확대 단추·손가락 확대도 쉰다.
rep("routeDetails.open=true;\n    document.querySelector('.paper-scroll').scrollIntoView({block:'start',behavior:'smooth'});",
    "routeDetails.open=true;\n    if(!document.body.classList.contains('step-mobile'))document.querySelector('.paper-scroll').scrollIntoView({block:'start',behavior:'smooth'});")
rep("    value=Math.max(1,Math.min(ZOOM_MAX,value));",
    "    if(frame.classList.contains('zoomed'))return;\n    value=Math.max(1,Math.min(ZOOM_MAX,value));")

# 5) 길찾기 주소 공유: ?to=교실&lift=1(엘리베이터)|0(계단)&from=입구번호  (11/8)
#    to 는 교실 id(room-55) 또는 이름(3-5). 주소로 열면 같은 조건의 길찾기가 바로 나온다.
i = s.index('  function renderRoute() {')
s = s[:i] + """  // 길찾기 조건(목적지·엘리베이터·입구)을 주소에 담아 공유합니다.
  const initialQuery=location.search;
  function routeQuery(route) {
    const q=new URLSearchParams(location.search);['to','lift','from'].forEach(k=>q.delete(k));
    if(route){q.set('to',route.destination);q.set('lift',route.useElevator?'1':'0');if(!route.useElevator)q.set('from',route.origin.replace('entrance-',''));}
    return q.toString();
  }
  // 주소는 한 동작이 끝난 뒤 한 번만 바꿉니다(브라우저가 잦은 주소 변경을 막기 때문).
  // 엘리베이터 질문·입구 고르기 중에도 지금까지 정한 조건(목적지, 계단)을 주소에 남깁니다.
  let urlQueued=false;
  function setRouteUrl() {
    if(urlQueued)return;urlQueued=true;
    queueMicrotask(()=>{
      urlQueued=false;const q=new URLSearchParams(location.search);['to','lift','from'].forEach(k=>q.delete(k));
      const route=window.currentSchoolRoute;
      if(state.destination&&['elevator','entrance','route'].includes(state.stage)) {
        q.set('to',state.destination);
        if(state.useElevator!==null)q.set('lift',state.useElevator?'1':'0');
        if(state.useElevator===false&&route&&state.stage==='route')q.set('from',route.origin.replace('entrance-',''));
      }
      const text=q.toString(),url=location.pathname+(text?'?'+text:'')+location.hash;
      if(url!==location.pathname+location.search+location.hash)window.history.replaceState(null,'',url);
    });
  }
  function shareBox() {
    const box=document.createElement('div');box.className='share-box';
    const button=document.createElement('button');button.type='button';button.className='share-route';button.textContent='길찾기 주소 공유';
    const p=document.createElement('p');p.textContent='이 주소를 받은 사람은 같은 목적지·엘리베이터·입구 조건의 길찾기를 바로 볼 수 있어요.';
    box.append(button,p);return box;
  }
  async function shareRoute(button) {
    const route=window.currentSchoolRoute;if(!route)return;
    const url=location.origin+location.pathname+'?'+routeQuery(route),room=roomMap.get(route.destination).label.replaceAll('\\n','');
    const done=text=>{const old=button.dataset.label||button.textContent;button.dataset.label=old;button.textContent=text;clearTimeout(button._t);button._t=setTimeout(()=>button.textContent=old,2200);};
    if(navigator.share&&matchMedia('(pointer:coarse)').matches) {
      try{await navigator.share({title:'구월중학교 '+room+' 가는 길',text:'구월중학교 '+room+' 가는 길',url});return;}catch(e){if(e.name==='AbortError')return;}
    }
    try{await navigator.clipboard.writeText(url);done('주소를 복사했어요');}
    catch(e){
      const input=document.createElement('input');input.value=url;input.readOnly=true;input.className='share-url';
      button.parentElement.querySelector('.share-url')?.remove();button.after(input);input.select();done('주소를 길게 눌러 복사하세요');
    }
  }
  document.addEventListener('click',event=>{const b=event.target.closest('.share-route');if(b)shareRoute(b);});
  function openFromUrl() {
    const q=new URLSearchParams(initialQuery),to=q.get('to');if(!to)return;
    const room=roomMap.get(to)||model.rooms.find(r=>r.label.replaceAll('\\n','')===to);
    if(!room||!graph.roomNodes.has(room.id)){setRouteUrl();return;}
    state.destination=room.id;const lift=q.get('lift');let from=q.get('from');
    if(lift==='1'){state.useElevator=true;state.origin='entrance-2';setStage('elevator');showRoute();}
    else if(lift==='0'){
      state.useElevator=false;
      if(room.building==='신관'&&from==='3')from='4';
      if(/^[1-4]$/.test(from||'')){state.origin='entrance-'+from;setStage('entrance');showRoute();}
      else{setStage('entrance');showEntrances();}
    }
    else askElevator();
  }
""" + s[i:]
rep("fitMap();measureTextLimits();setTextSize(textSize);setStage('idle');",
    "fitMap();measureTextLimits();setTextSize(textSize);setStage('idle');openFromUrl();")
css2 = steps_css + """
.step-sub { display:flex; gap:6px; margin-top:6px; }
.step-sub #step-all { flex:1; margin:0; }
.step-sub .share-route { flex:1; min-height:38px; border:1.5px solid #1668b8; border-radius:9px; background:#fff; color:#1668b8; font-size:14px; font-weight:700; }
.share-box { margin-top:10px; padding-top:10px; border-top:1px solid #e6ebf0; }
.share-box .share-route { padding:9px 14px; border:1.5px solid #1668b8; border-radius:9px; background:#fff; color:#1668b8; font-size:14px; font-weight:700; }
.share-box p { margin:6px 0 0; color:#62707f; font-size:12px; }
.share-url { display:block; width:100%; margin-top:6px; padding:8px; border:1px solid #bac8d5; border-radius:7px; font-size:13px; }
body:has(.paper-stage.zoomed) .zoom-bar { display:none; }
@media print { .share-box { display:none!important; } }
"""
rep("</style></head>", css2 + "</style></head>")

open(out, 'w', encoding='utf-8', newline='').write(s.replace(chr(10), chr(13)+chr(10)) if crlf else s)
print('ok', len(s))
