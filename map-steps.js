  // 휴대폰에서는 경로를 층별 단계로 나누어 해당 구간을 확대합니다.
  const stepPanel=document.getElementById('step-panel'),stepStage=document.querySelector('.paper-stage');
  let routeSteps=[],stepIndex=0;
  function buildSteps(route,room) {
    const groups=[];let current=null;
    route.nodes.forEach((n,i)=>{
      const key=n.building+n.floor;
      if(!current||current.key!==key){current={key,building:n.building,floor:n.floor,nodes:[],exit:null};groups.push(current);}
      current.nodes.push(n);
      const next=route.nodes[i+1];
      if(next&&next.building+next.floor!==key)current.exit=route.edges[i];
    });
    const span=g=>g.nodes.reduce((sum,n,i)=>i?sum+Math.hypot(n.x-g.nodes[i-1].x,n.y-g.nodes[i-1].y):0,0);
    const kept=groups.filter((g,i)=>i===0||i===groups.length-1||span(g)>1||groups[i-1].exit?.kind==='bridge');
    const roomName=room.label.replaceAll('\n','');
    return kept.map((g,i)=>{
      const next=kept[i+1],e=g.exit;let text;
      if(!next)text=`복도를 따라 ${roomName}까지 가세요.`;
      else if(e.kind==='bridge')text=`연결통로를 지나 ${next.building} ${next.floor}층으로 가세요.`;
      else {
        const way=next.floor>g.floor?'올라가세요':'내려가세요',by=e.kind==='elevator'?'엘리베이터로':`${sideNames[e.side]} 계단으로`;
        text=`${by} ${next.floor}층까지 ${way}.`;
      }
      if(i===0)text=`${names.get(route.origin)}에서 출발합니다. ${text}`;
      const box=g.nodes.map(n=>({x:n.x,y:n.y}));
      if(!next)box.push({x:room.x,y:room.y},{x:room.x+room.w,y:room.y+room.h});
      return {title:`${g.building} ${g.floor}층`,text,box};
    });
  }
  function showStep(i) {
    stepIndex=i;const step=routeSteps[i],unit=paper.offsetWidth/model.width;
    document.getElementById('step-count').textContent=`${i+1} / ${routeSteps.length} 단계`;
    document.getElementById('step-title').textContent=step.title;
    document.getElementById('step-text').textContent=step.text;
    document.getElementById('step-prev').disabled=i===0;
    document.getElementById('step-next').disabled=i===routeSteps.length-1;
    document.getElementById('step-all').textContent='전체 지도 보기';
    const xs=step.box.map(p=>p.x),ys=step.box.map(p=>p.y),pad=26;
    const x0=Math.min(...xs)-pad,x1=Math.max(...xs)+pad,y0=Math.min(...ys)-pad,y1=Math.max(...ys)+pad;
    const height=Math.max(280,innerHeight-stepPanel.offsetHeight-90);
    stepStage.classList.add('zoomed');stepStage.style.setProperty('--step-h',height+'px');
    const width=stepStage.clientWidth,scale=Math.min(width/((x1-x0)*unit),height/((y1-y0)*unit),1.7);
    stepStage.style.setProperty('--s',scale);
    stepStage.style.setProperty('--tx',(width/2-(x0+x1)/2*unit*scale)+'px');
    stepStage.style.setProperty('--ty',(height/2-(y0+y1)/2*unit*scale)+'px');
  }
  function showSteps(route,room) {
    if(!matchMedia('(max-width:700px)').matches)return;
    routeSteps=buildSteps(route,room);
    stepPanel.hidden=false;document.body.classList.add('step-mobile');showStep(0);
    stepPanel.scrollIntoView({block:'start'});
  }
  function hideSteps() {
    routeSteps=[];stepPanel.hidden=true;document.body.classList.remove('step-mobile');stepStage.classList.remove('zoomed');
  }
  document.getElementById('step-prev').addEventListener('click',()=>showStep(stepIndex-1));
  document.getElementById('step-next').addEventListener('click',()=>showStep(stepIndex+1));
  document.getElementById('step-all').addEventListener('click',event=>{
    if(stepStage.classList.contains('zoomed')){stepStage.classList.remove('zoomed');event.target.textContent='단계별 보기';}
    else showStep(stepIndex);
  });
