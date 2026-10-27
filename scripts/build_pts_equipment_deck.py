#!/usr/bin/env python3
"""Build PTS-oborudovanie.html with embedded photos from assets/equipment."""

from __future__ import annotations

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "equipment"
OUT = ROOT / "PTS-oborudovanie.html"


def img(name: str) -> str:
    path = ASSETS / name
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{data}"


def photo(name: str, alt: str, credit: str = "", *, contain: bool = False) -> str:
    cap = f'<div class="photo-credit">{credit}</div>' if credit else ""
    cls = "photo-panel contain" if contain else "photo-panel"
    return f'''<div class="{cls}">
        <img src="{img(name)}" alt="{alt}" />
        {cap}
      </div>'''


CSS = r"""
:root {
  --bg:#12081c; --bg-2:#1a0f2e; --panel:rgba(36,18,58,.72);
  --text:#f7eef5; --muted:#c4a8bc; --accent:#cc0c5e;
  --accent-soft:#ff4d8d; --accent-2:#3b1a69; --line:rgba(255,255,255,.12);
  --safe:clamp(1.6rem,4vw,3.5rem);
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:var(--bg);color:var(--text);font-family:Manrope,sans-serif;overflow:hidden}
body{background:
  radial-gradient(1100px 700px at 8% -8%,rgba(204,12,94,.28),transparent 55%),
  radial-gradient(900px 640px at 100% 0%,rgba(59,26,105,.55),transparent 52%),
  linear-gradient(160deg,#0e0616 0%,#1a0f2e 45%,#12081c 100%)}
.orb{position:fixed;border-radius:50%;filter:blur(60px);pointer-events:none;z-index:0;opacity:.4;animation:drift 18s ease-in-out infinite alternate}
.orb.a{width:420px;height:420px;background:#cc0c5e;top:-120px;left:-80px}
.orb.b{width:360px;height:360px;background:#3b1a69;bottom:-140px;right:-60px;animation-duration:22s}
@keyframes drift{from{transform:translate(0,0) scale(1)}to{transform:translate(40px,-30px) scale(1.1)}}
body::before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.14;z-index:0;
  background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);
  background-size:48px 48px;mask-image:radial-gradient(ellipse at center,black 35%,transparent 80%)}
.deck{height:100%;width:100%;position:relative;z-index:2}
.slide{position:absolute;inset:0;padding:var(--safe);padding-bottom:calc(var(--safe) + 1.4rem);
  display:flex;flex-direction:column;justify-content:center;opacity:0;visibility:hidden;pointer-events:none;
  transform:translateX(28px) scale(.985);transition:opacity .4s ease,transform .4s ease,visibility .4s}
.slide.active{opacity:1;visibility:visible;pointer-events:auto;transform:none}
.slide.split{display:grid;grid-template-columns:1.15fr .95fr;gap:clamp(1rem,2.5vw,2rem);align-items:center}
.slide.split .copy{display:flex;flex-direction:column;justify-content:center;min-width:0}
.eyebrow{color:var(--accent-soft);font-size:.78rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;margin-bottom:.7rem}
.eyebrow::before{content:"";display:inline-block;width:1.2rem;height:2px;margin-right:.55rem;vertical-align:middle;background:var(--accent)}
h1,h2,h3{font-family:Unbounded,sans-serif;font-weight:600;line-height:1.15}
h1{font-size:clamp(2rem,5vw,3.6rem);max-width:14ch}
h2{font-size:clamp(1.45rem,3.2vw,2.4rem);margin-bottom:.45rem}
h3{font-size:1rem;margin-bottom:.3rem}
.sub{color:var(--muted);font-size:clamp(.95rem,1.35vw,1.12rem);line-height:1.45;max-width:42rem;margin-bottom:1.1rem}
.hero-meta{margin-top:1.3rem;color:var(--muted);font-size:1.02rem}
.reveal{opacity:0;transform:translateY(14px);transition:opacity .5s ease,transform .5s ease;transition-delay:var(--d,0ms)}
.slide.active .reveal{opacity:1;transform:none}
.reveal-scale{opacity:0;transform:scale(.95);transition:opacity .45s ease,transform .45s ease;transition-delay:var(--d,0ms)}
.slide.active .reveal-scale{opacity:1;transform:none}
.photo-panel{position:relative;border-radius:16px;overflow:hidden;border:1px solid var(--line);
  background:#0a0410;min-height:min(58vh,520px);height:100%;max-height:70vh;box-shadow:0 20px 50px rgba(0,0,0,.35)}
.photo-panel img{width:100%;height:100%;object-fit:cover;display:block}
.photo-panel.contain{background:#1a1028;display:flex;align-items:center;justify-content:center;padding:1rem}
.photo-panel.contain img{width:100%;height:auto;max-height:100%;object-fit:contain}
.photo-credit{position:absolute;left:0;right:0;bottom:0;padding:.35rem .7rem;font-size:.65rem;color:rgba(255,255,255,.7);
  background:linear-gradient(transparent,rgba(0,0,0,.75))}
.grid{display:grid;gap:.85rem}
.grid-2{grid-template-columns:repeat(2,minmax(0,1fr))}
.grid-3{grid-template-columns:repeat(3,minmax(0,1fr))}
.grid-4{grid-template-columns:repeat(4,minmax(0,1fr))}
.tile{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:1rem 1.05rem;backdrop-filter:blur(8px);min-height:0}
.tile .num{font-family:Unbounded,sans-serif;color:var(--accent);font-size:.72rem;letter-spacing:.08em;margin-bottom:.4rem}
.tile p,.list-plain li{color:var(--muted);font-size:.92rem;line-height:1.4}
.tile img{width:100%;height:110px;object-fit:cover;border-radius:10px;margin-bottom:.65rem;border:1px solid var(--line)}
.big-list{display:flex;flex-direction:column;gap:.55rem}
.big-list .item{display:grid;grid-template-columns:auto 1fr;gap:.85rem;align-items:start;padding:.75rem .9rem;
  border:1px solid var(--line);border-radius:12px;background:rgba(36,18,58,.45)}
.big-list .n{font-family:Unbounded,sans-serif;color:var(--accent);font-size:.9rem;min-width:2.2rem;padding-top:.15rem}
.big-list h3{margin:0;font-size:1.02rem}
.big-list p{color:var(--muted);font-size:.88rem;margin-top:.15rem}
.pipeline{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.65rem;margin-top:.3rem}
.pipe{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:.95rem .85rem;position:relative;min-height:7rem}
.pipe::after{content:"→";position:absolute;right:-.5rem;top:50%;transform:translateY(-50%);color:var(--accent-soft);opacity:.75}
.pipe:last-child::after{content:none}
.list-plain{list-style:none;display:flex;flex-direction:column;gap:.45rem}
.list-plain li{position:relative;padding-left:1rem}
.list-plain li::before{content:"—";position:absolute;left:0;color:var(--accent)}
.list-plain strong{color:var(--text);font-weight:600}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:1rem 1.1rem}
.panel h3{color:var(--accent-soft);font-size:.85rem;letter-spacing:.04em;text-transform:uppercase;margin-bottom:.55rem}
.tag-row{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.7rem}
.tag{border:1px solid var(--line);border-radius:999px;padding:.22rem .65rem;font-size:.78rem;color:var(--muted)}
.tag.on{color:var(--accent-soft);border-color:rgba(204,12,94,.4);background:rgba(204,12,94,.12)}
.note{margin-top:.9rem;padding:.75rem .9rem;border-left:3px solid var(--accent);background:rgba(204,12,94,.08);
  color:var(--muted);font-size:.92rem;line-height:1.4;max-width:52rem}
.note strong{color:var(--text)}
.scheme{display:flex;flex-wrap:wrap;gap:.45rem;align-items:center;margin-top:.6rem}
.scheme .box{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:.55rem .75rem;font-size:.88rem}
.scheme .box strong{color:var(--accent-soft);display:block;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.15rem}
.scheme .arrow{color:var(--accent-soft);font-size:1.1rem}
.fragment{opacity:0;transform:translateY(8px);transition:opacity .3s ease,transform .3s ease,border-color .3s}
.fragment.visible{opacity:1;transform:none}
.fragment.hl{border-color:rgba(204,12,94,.55);box-shadow:0 0 0 1px rgba(204,12,94,.22)}
.footer-bar{position:fixed;left:var(--safe);right:var(--safe);bottom:.75rem;z-index:5;display:flex;justify-content:space-between;
  align-items:center;color:var(--muted);font-size:.78rem;pointer-events:none}
.hint{display:flex;align-items:center;gap:.45rem}
.key{display:inline-flex;align-items:center;justify-content:center;min-width:1.4rem;height:1.4rem;padding:0 .3rem;
  border:1px solid var(--line);border-radius:6px;color:var(--text);font-size:.7rem}
.progress-track{position:fixed;left:0;right:0;bottom:0;height:3px;background:rgba(255,255,255,.06);z-index:6}
.progress{height:100%;width:0;background:linear-gradient(90deg,var(--accent),var(--accent-soft));transition:width .3s ease}
.thumb-grid{display:grid;grid-template-columns:1fr 1fr;gap:.55rem}
.thumb-grid img{width:100%;height:120px;object-fit:cover;border-radius:10px;border:1px solid var(--line)}
@media (max-width:980px){
  .slide.split{grid-template-columns:1fr;overflow:auto;justify-content:flex-start;padding-top:1.2rem}
  .photo-panel{min-height:220px;max-height:34vh}
  .pipeline,.grid-4{grid-template-columns:1fr 1fr}
  .pipe::after{display:none}
}
@media (max-width:640px){
  .grid-2,.grid-3,.grid-4,.pipeline{grid-template-columns:1fr}
}

.slide.solo{max-width:56rem}
.dual-photo{display:grid;grid-template-rows:1fr 1fr;gap:.55rem;height:100%;min-height:min(58vh,520px)}
.dual-photo .photo-panel{min-height:0;max-height:none;height:100%}
.flow{display:flex;flex-wrap:wrap;gap:.55rem;align-items:stretch;margin-top:.55rem}
.flow-node{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:.7rem .85rem;min-width:7.2rem;text-align:center}
.flow-node .role{display:block;font-family:Unbounded,sans-serif;font-size:.68rem;letter-spacing:.06em;text-transform:uppercase;color:var(--accent-soft);margin-bottom:.25rem}
.flow-node .name{font-size:.92rem;font-weight:600}
.flow-edge{display:flex;flex-direction:column;align-items:center;justify-content:center;min-width:3.2rem;color:var(--accent-soft);font-size:.78rem;gap:.12rem}
.flow-edge .wire{font-family:Unbounded,sans-serif;font-size:.7rem;letter-spacing:.04em;padding:.12rem .4rem;border:1px solid rgba(204,12,94,.45);border-radius:999px;color:var(--accent-soft)}
.flow-edge.bad .wire{border-color:rgba(255,120,80,.75);color:#ffb090;background:rgba(255,100,60,.12)}
.answer-box{margin-top:.85rem;padding:1rem 1.1rem;border:1px solid rgba(204,12,94,.35);border-radius:12px;background:rgba(204,12,94,.1)}
.answer-box h3{margin-bottom:.45rem}
.tile .cap{font-family:Unbounded,sans-serif;font-size:.72rem;color:var(--accent-soft);letter-spacing:.05em;text-transform:uppercase;margin:.15rem 0 .45rem}
.tile img.fit{object-fit:contain;background:#12081c;height:130px}
"""

JS = r"""
const slides=[...document.querySelectorAll('.slide')];
const counter=document.getElementById('counter');
const progress=document.getElementById('progress');
let i=0, frag=-1;
function frags(s){return [...s.querySelectorAll('.fragment')]}
function setFrag(s,index){const items=frags(s);items.forEach((el,n)=>{el.classList.toggle('visible',n<=index);el.classList.toggle('hl',n===index&&index>=0)});frag=index}
function resetFrags(s){setFrag(s,-1)}
function showSlide(n){const next=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,idx)=>{const on=idx===next;s.classList.toggle('active',on);if(!on)resetFrags(s)});i=next;frag=-1;updateChrome()}
function updateChrome(){counter.textContent=`${i+1} / ${slides.length}`;progress.style.width=`${((i+1)/slides.length)*100}%`}
function next(){const s=slides[i],items=frags(s);if(items.length&&frag<items.length-1){setFrag(s,frag+1);return}if(i<slides.length-1)showSlide(i+1)}
function prev(){const s=slides[i],items=frags(s);if(items.length&&frag>=0){setFrag(s,frag-1);return}if(i>0){showSlide(i-1);const ps=slides[i],pi=frags(ps);if(pi.length)setFrag(ps,pi.length-1)}}
window.addEventListener('keydown',e=>{
  if(['ArrowRight','ArrowDown','PageDown',' ','Enter'].includes(e.key)){e.preventDefault();next()}
  if(['ArrowLeft','ArrowUp','PageUp','Backspace'].includes(e.key)){e.preventDefault();prev()}
  if(e.key==='Home')showSlide(0); if(e.key==='End')showSlide(slides.length-1);
  if(e.key==='f'||e.key==='F'){document.fullscreenElement?document.exitFullscreen?.():document.documentElement.requestFullscreen?.()}
});
let touchX=null;
window.addEventListener('touchstart',e=>{touchX=e.changedTouches[0].screenX},{passive:true});
window.addEventListener('touchend',e=>{if(touchX===null)return;const dx=e.changedTouches[0].screenX-touchX;if(Math.abs(dx)>40)dx<0?next():prev();touchX=null},{passive:true});
document.body.addEventListener('click',e=>{if(e.target.closest('a,button'))return;e.clientX>window.innerWidth*.55?next():prev()});
showSlide(0);
"""


def node(role: str, name: str) -> str:
    return (
        f'<div class="flow-node"><span class="role">{role}</span>'
        f'<span class="name">{name}</span></div>'
    )


def edge(label: str, *, bad: bool = False) -> str:
    cls = "flow-edge bad" if bad else "flow-edge"
    return (
        f'<div class="{cls}"><span>→</span>'
        f'<span class="wire">{label}</span></div>'
    )


def dual_photo(a: str, alt_a: str, b: str, alt_b: str, credit: str = "") -> str:
    cap = f'<div class="photo-credit">{credit}</div>' if credit else ""
    return (
        '<div class="dual-photo">'
        f'<div class="photo-panel"><img src="{img(a)}" alt="{alt_a}" /></div>'
        f'<div class="photo-panel"><img src="{img(b)}" alt="{alt_b}" />{cap}</div>'
        "</div>"
    )


def build() -> None:
    slides: list[str] = []

    slides.append(
        """
    <section class="slide active solo" data-title="Титул">
      <div class="eyebrow reveal">ТЕХ ГУАП · направление ПТС</div>
      <h1 class="reveal" style="--d:80ms">Оборудование<br>для трансляций</h1>
      <p class="sub reveal" style="--d:160ms">Какая задача → какое соединение → какое оборудование</p>
      <div class="hero-meta reveal" style="--d:240ms">Не спецификации наизусть — логика тракта</div>
    </section>"""
    )

    slides.append(
        """
    <section class="slide" data-title="Карта мира" data-fragments="1">
      <div class="eyebrow">Вступление</div>
      <h2>Карта мира эфира</h2>
      <p class="sub">Трансляция — это путь сигнала от источника к зрителю. Четыре блока, через которые проходит картинка и звук.</p>
      <div class="pipeline">
        <div class="pipe fragment"><h3>Источник</h3><p>Камеры, ПК, внешний сигнал</p></div>
        <div class="pipe fragment"><h3>Путь</h3><p>Кабели, сеть, преобразователи</p></div>
        <div class="pipe fragment"><h3>Обработка</h3><p>Микшер, скейлер, матрица, ПК</p></div>
        <div class="pipe fragment"><h3>Вывод</h3><p>Стрим, запись, экраны зала</p></div>
      </div>
      <div class="note fragment"><strong>Мысль занятия:</strong> сначала задача, потом тип соединения, потом железо — а не наоборот.</div>
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide split" data-title="Камеры">
      <div class="copy">
        <div class="eyebrow reveal">Источник · 01</div>
        <h2 class="reveal" style="--d:60ms">Камеры</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Источник сигнала</strong> — устройство, которое впервые формирует видео. Камера отдаёт кадр и параметры формата в кабель или сеть.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li><strong>Выход:</strong> SDI (BNC), HDMI, иногда NDI</li>
          <li><strong>Параметры:</strong> разрешение, частота кадров, progressive / interlace</li>
        </ul>
        <div class="note reveal" style="--d:220ms"><strong>В первую очередь проверяем здесь:</strong> формат, выход и другие параметры источника.</div>
      </div>
      {photo("cam-tripod.jpg", "Камера на штативе", "Wikimedia Commons · Blackmagic URSA")}
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide split" data-title="ПК">
      <div class="copy">
        <div class="eyebrow reveal">Источник · 02</div>
        <h2 class="reveal" style="--d:60ms">ПК и ноутбуки</h2>
        <p class="sub reveal" style="--d:100ms">Компьютер — источник <strong>компьютерной графики</strong>: презентации, браузер, окна приложений, графика микшера.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li><strong>Выход:</strong> HDMI / DisplayPort / USB-C → адаптер</li>
          <li><strong>Сетевые протоколы:</strong> NDI, SRT, RTMP и другие пути «по IP»</li>
          <li><strong>EDID</strong> — данные о возможностях дисплея; без них ПК может отдать неверный режим</li>
          <li><strong>Важно:</strong> HDMI на ноутбуке/ПК — <em>всегда</em> только выход, не вход</li>
        </ul>
        <div class="tag-row reveal" style="--d:220ms">
          <span class="tag on">презентация</span><span class="tag on">браузер</span><span class="tag on">сетевые протоколы</span>
        </div>
      </div>
      {photo("laptop.jpg", "Ноутбук с презентацией", "Wikimedia Commons")}
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide split" data-title="Внешний сигнал">
      <div class="copy">
        <div class="eyebrow reveal">Источник · 03</div>
        <h2 class="reveal" style="--d:60ms">Другие устройства</h2>
        <p class="sub reveal" style="--d:100ms">Внешний сигнал — уже собранная программа с другого микшера, плеера, медиасервера, телемоста.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li><strong>PGM с другого пульта</strong> — готовая программа в наш тракт</li>
          <li><strong>Плеер / медиасервер</strong> — ролики, заставки</li>
          <li><strong>ВКС / телемост</strong> — удалённый участник как отдельный вход</li>
        </ul>
        <div class="note reveal" style="--d:220ms"><strong>Запомните:</strong> внешний сигнал тоже источник. У него есть формат и интерфейс — согласуйте их так же, как у камеры.</div>
      </div>
      {photo("bmd-atem.jpg", "Видеомикшер как источник", "Wikimedia Commons · Blackmagic ATEM")}
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide split" data-title="Тракт сигнала">
      <div class="copy">
        <div class="eyebrow reveal">Путь</div>
        <h2 class="reveal" style="--d:60ms">Тракт сигнала</h2>
        <p class="sub reveal" style="--d:100ms">Между источником и обработкой сигнал проходит по кабелю, по сети или через преобразователи — из‑за разных разъёмов, длин линий и форматов.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li><strong>Кабель</strong> — HDMI, SDI, XLR, Ethernet</li>
          <li><strong>Сеть</strong> — NDI, SRT, RTMP (передача по IP)</li>
          <li><strong>Устройства на пути</strong> — конвертер, сплиттер, матрица</li>
        </ul>
        <div class="note reveal" style="--d:220ms"><strong>Тракт</strong> — упорядоченная последовательность звеньев, по которой сигнал проходит от источника к конечному приёмнику.</div>
      </div>
      {photo("path-setup.jpg", "Кабели и стойка", "Wikimedia Commons")}
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide" data-title="Кабели">
      <div class="eyebrow reveal">Путь · кабели</div>
      <h2 class="reveal" style="--d:40ms">Кабели и интерфейсы</h2>
      <p class="sub reveal" style="--d:80ms">Кабель — не «просто провод», а стандарт: разъём + электрический/цифровой протокол + ограничения по длине.</p>
      <div class="grid grid-4">
        <div class="tile reveal-scale" style="--d:120ms"><img src="{img('cable-hdmi-plug.jpg')}" alt="HDMI"/><div class="num">HDMI</div><h3>HDMI</h3><p>Бытовой/компьютерный видео+звук. Короткие линии, чувствителен к качеству кабеля.</p></div>
        <div class="tile reveal-scale" style="--d:160ms"><img src="{img('bnc.jpg')}" alt="BNC"/><div class="num">SDI</div><h3>SDI (BNC)</h3><p>Профессиональное видео. Level A / Level B — разные упаковки 3G-SDI. Длиннее HDMI, надёжнее на площадке.</p></div>
        <div class="tile reveal-scale" style="--d:200ms"><img src="{img('cable-xlr.jpg')}" alt="XLR"/><div class="num">XLR</div><h3>XLR</h3><p>Балансный звуковой интерфейс для микрофонов и линейных сигналов.</p></div>
        <div class="tile reveal-scale" style="--d:240ms"><img src="{img('rj45-plug.jpg')}" alt="RJ45"/><div class="num">ETH</div><h3>Ethernet</h3><p>Сеть, управление, стрим и другие средства передачи по IP.</p></div>
      </div>
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide split" data-title="Преобразователи">
      <div class="copy">
        <div class="eyebrow reveal">Путь</div>
        <h2 class="reveal" style="--d:60ms">Преобразователи сигнала</h2>
        <p class="sub reveal" style="--d:100ms">На пути сигнала часто устанавливают устройства этой группы. «Преобразование» здесь — общее обозначение: речь не только о смене типа интерфейса, но и о разветвлении, согласовании разъёмов и соединении линий.</p>
        <div class="big-list reveal" style="--d:160ms">
          <div class="item"><div class="n">01</div><div><h3>Конверторы</h3><p>Меняют стандарт сигнала (HDMI↔SDI)</p></div></div>
          <div class="item"><div class="n">02</div><div><h3>Адаптеры</h3><p>Меняют только разъём / форм-фактор</p></div></div>
          <div class="item"><div class="n">03</div><div><h3>Сплиттеры</h3><p>Раздают один сигнал на N выходов</p></div></div>
          <div class="item"><div class="n">04</div><div><h3>Соединители</h3><p>«Бочонки», удлинители, пассивные разветвители</p></div></div>
        </div>
      </div>
      {photo("bmd-converters.jpg", "Mini-конвертеры", "Wikimedia Commons · Blackmagic Mini Converters")}
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide split" data-title="Конверторы">
      <div class="copy">
        <div class="eyebrow reveal">Конверторы</div>
        <h2 class="reveal" style="--d:60ms">Конвертер ≠ адаптер</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Конвертер</strong> переводит один <em>стандарт сигнала</em> в другой: перепаковывает данные, как правило с питанием и специализированным чипом.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li><strong>Пример:</strong> HDMI и SDI — разные стандарты → нужен именно конвертер</li>
          <li>Может выполнять up/down/cross conversion (разрешение, частота кадров)</li>
          <li>Часто умеет встраивать и извлекать звук (embed / de-embed)</li>
        </ul>
        <div class="note reveal" style="--d:220ms"><strong>Правило:</strong> если разъёмы разные <em>и</em> протоколы разные — это конвертер, а не простой переходник.</div>
      </div>
      {photo("bmd-converters.jpg", "HDMI/SDI конвертеры", "Wikimedia Commons")}
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide split" data-title="Адаптеры">
      <div class="copy">
        <div class="eyebrow reveal">Адаптеры</div>
        <h2 class="reveal" style="--d:60ms">Только разъём</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Адаптер</strong> изменяет форм-фактор разъёма, не перекодируя сигнал. Типичный пример — HDMI ↔ DVI.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li>Не превращает HDMI в SDI</li>
          <li>Не устраняет несовместимость форматов кадра</li>
          <li>Активный USB-C‑хаб не следует путать с пассивным переходником</li>
        </ul>
        <div class="note reveal" style="--d:220ms"><strong>Ошибка новичка:</strong> ожидать от адаптера работу конвертера стандартов.</div>
      </div>
      {photo("adapter-hdmi-dvi.jpg", "Адаптер HDMI–DVI", "Wikimedia Commons", contain=True)}
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide split" data-title="Сплиттеры">
      <div class="copy">
        <div class="eyebrow reveal">Сплиттеры</div>
        <h2 class="reveal" style="--d:60ms">1 → N</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Сплиттер (distribution amplifier)</strong> формирует несколько копий одного входного сигнала для параллельных потребителей: микшер, рекордер, превью.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li>Активный сплиттер — с питанием и стабилизацией сигнала</li>
          <li>Пассивный разветвитель повышает риск потери уровня и срыва приёма</li>
        </ul>
      </div>
      {photo("hdmi-splitter.jpg", "HDMI splitter", "", contain=True)}
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide split" data-title="Соединители">
      <div class="copy">
        <div class="eyebrow reveal">Соединители</div>
        <h2 class="reveal" style="--d:60ms">Бочонки и удлинение</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Соединитель («бочонок»)</strong> — элемент механического стыкования двух однотипных кабелей (например, BNC–BNC) для удлинения линии или смены пола разъёма.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li>Позволяет нарастить линию без замены всего кабеля</li>
          <li>Каждое дополнительное соединение увеличивает число потенциальных точек отказа</li>
          <li><strong>Пассивные разветвители</strong> делят энергию сигнала между несколькими выходами и поэтому менее предпочтительны в эфирном тракте, чем активные устройства распределения</li>
        </ul>
      </div>
      {photo("bnc-barrel.jpg", "BNC barrel", "", contain=True)}
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide" data-title="Схема HDMI→SDI">
      <div class="eyebrow reveal">Связка</div>
      <h2 class="reveal" style="--d:40ms">Камера HDMI → SDI-сплиттер</h2>
      <p class="sub reveal" style="--d:80ms">Типовая задача: камера отдаёт HDMI, а тракт площадки построен на SDI. Требуется конвертер, затем раздача.</p>
      <div class="scheme reveal" style="--d:140ms">
        <div class="box"><strong>Источник</strong>Камера HDMI</div>
        <div class="arrow">→</div>
        <div class="box"><strong>Конвертер</strong>HDMI → SDI</div>
        <div class="arrow">→</div>
        <div class="box"><strong>Сплиттер SDI</strong>1→N</div>
        <div class="arrow">→</div>
        <div class="box"><strong>Потребители</strong>микшер / запись / превью</div>
      </div>
      <div class="grid grid-2" style="margin-top:1rem">
        <div class="tile reveal-scale" style="--d:200ms"><img src="{img('cam-bmd.jpg')}" alt="камера"/><h3>Почему так</h3><p>Длинные HDMI-линии на площадке менее стабильны. SDI обеспечивает большую дальность и удобные разъёмы BNC.</p></div>
        <div class="tile reveal-scale" style="--d:260ms"><img src="{img('bmd-converters.jpg')}" alt="конвертер"/><h3>Где ошибаются</h3><p>Ставят адаптер вместо конвертера; забывают питание конвертера; путают параметры сигнала.</p></div>
      </div>
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide split" data-title="Обработка">
      <div class="copy">
        <div class="eyebrow reveal">Обработка</div>
        <h2 class="reveal" style="--d:60ms">Микшеры, скейлеры, матрицы</h2>
        <p class="sub reveal" style="--d:100ms">На этом этапе из входных сигналов формируют программу: переключают, масштабируют и маршрутизируют.</p>
        <div class="big-list reveal" style="--d:160ms">
          <div class="item"><div class="n">01</div><div><h3>Микшер</h3><p>Определяет, что сейчас в программе</p></div></div>
          <div class="item"><div class="n">02</div><div><h3>Скейлер</h3><p>Согласует формат кадра с целевым экраном</p></div></div>
          <div class="item"><div class="n">03</div><div><h3>Матрица</h3><p>Назначает маршруты «любой вход → любой выход»</p></div></div>
        </div>
      </div>
      {photo("atem-panel.jpg", "Панель микшера", "Wikimedia Commons · ATEM panel")}
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide split" data-title="Микшеры">
      <div class="copy">
        <div class="eyebrow reveal">Микшеры</div>
        <h2 class="reveal" style="--d:60ms">Roland V-60HD</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Видеомикшер (switcher)</strong> — устройство или программа, которое в реальном времени выбирает PGM и PVW, выполняет переходы, PinP и ключи.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li>4× SDI + 2× HDMI (со скейлом на HDMI)</li>
          <li>Выходы PGM / AUX / Multi-View</li>
          <li>Встроенный аудимикшер, XLR, автомикс</li>
        </ul>
        <div class="tag-row reveal" style="--d:220ms">
          <span class="tag on">PGM</span><span class="tag on">PVW</span><span class="tag on">AUX</span>
        </div>
      </div>
      {photo("roland-v60hd-main.jpg", "Roland V-60HD", "Roland Pro A/V · V-60HD", contain=True)}
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide split" data-title="Скейлеры">
      <div class="copy">
        <div class="eyebrow reveal">Скейлеры</div>
        <h2 class="reveal" style="--d:60ms">Согласование формата</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Скейлер</strong> приводит входной кадр к требуемому формату отображения: разрешению, соотношению сторон и ориентации — без искажения пропорций.</p>
        <div class="panel reveal" style="--d:160ms">
          <h3>Кейс</h3>
          <ul class="list-plain">
            <li><strong>Вход:</strong> Full HD 1920×1080</li>
            <li><strong>Экран:</strong> 768×1280 (вертикальный)</li>
            <li><strong>Решение:</strong> масштабирование и подгонка (fit / crop)</li>
            <li><strong>Ошибка:</strong> принудительное растягивание — нарушение пропорций</li>
          </ul>
        </div>
      </div>
      {photo("video-scaler.jpg", "Video scaler", "", contain=True)}
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide split" data-title="Матрицы">
      <div class="copy">
        <div class="eyebrow reveal">Матрицы / видеохабы</div>
        <h2 class="reveal" style="--d:60ms">Несколько × несколько</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Матрица (router / Videohub)</strong> — коммутатор M входов на N выходов с независимым назначением маршрутов.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li>Сплиттер: один вход → одинаковые копии на все выходы</li>
          <li>Матрица: входы и выходы назначаются независимо</li>
          <li>Пресеты снижают необходимость перекоммутации в эфире</li>
        </ul>
      </div>
      {dual_photo("bmd-videohub.jpg", "Videohub спереди", "videohub-rear.jpg", "Videohub сзади", "Спереди — управление; сзади — разъёмы")}
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide" data-title="Карты захвата">
      <div class="eyebrow reveal">Карты ввода</div>
      <h2 class="reveal" style="--d:40ms">USB и PCIe</h2>
      <p class="sub reveal" style="--d:80ms"><strong>Карта захвата (capture)</strong> принимает SDI/HDMI и передаёт кадры в компьютер / микшерное ПО.</p>
      <div class="grid grid-2">
        <div class="tile reveal-scale" style="--d:120ms">
          <div class="cap">USB capture — внешний бокс</div>
          <img class="fit" src="{img('capture-usb2.jpg')}" alt="USB capture"/>
          <div class="num">USB</div>
          <h3>Внешняя карта / бокс USB</h3>
          <p>Подключается к порту USB. Удобна для ноутбука. Полоса делится с другими устройствами; стабильность зависит от чипа и драйвера.</p>
        </div>
        <div class="tile reveal-scale" style="--d:180ms">
          <div class="cap">PCIe capture — плата внутрь ПК</div>
          <img class="fit" src="{img('capture-datapath.jpg')}" alt="PCIe capture"/>
          <div class="num">PCIe</div>
          <h3>Внутренняя плата PCIe</h3>
          <p>Устанавливается в слот системной платы (линии x4/x8/x16). Выше запас по полосе, удобнее многоканальные входы.</p>
        </div>
      </div>
      <div class="note reveal" style="--d:240ms"><strong>Как отличить:</strong> USB — отдельный корпус к порту компьютера; PCIe — плата с контактной «гребёнкой» внутрь корпуса ПК.</div>
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide" data-title="Вывод">
      <div class="eyebrow reveal">Вывод программы</div>
      <h2 class="reveal" style="--d:40ms">Карты и боксы вывода</h2>
      <p class="sub reveal" style="--d:80ms">После обработки программу возвращают в тракт устройствами вывода — это не мониторный выход игровой видеокарты.</p>
      <div class="grid grid-2">
        <div class="tile reveal-scale" style="--d:120ms">
          <div class="cap">Внешний бокс вывода</div>
          <img class="fit" src="{img('bmd-monitor-out.jpg')}" alt="UltraStudio Monitor"/>
          <h3>Blackmagic UltraStudio Monitor (пример)</h3>
          <p>Внешнее устройство: принимает программу со станции и отдаёт её в SDI/HDMI эфирного тракта или на контрольный монитор.</p>
        </div>
        <div class="tile reveal-scale" style="--d:180ms">
          <div class="cap">Внутренняя PCIe-плата вывода</div>
          <img class="fit" src="{img('pcie-output-card.jpg')}" alt="PCIe SDI HDMI out"/>
          <h3>PCIe SDI + HDMI playback</h3>
          <p>Плата в слот ПК с выходами SDI и HDMI. Типовая роль — playback / program out в профессиональный тракт.</p>
        </div>
      </div>
      <div class="note reveal" style="--d:240ms"><strong>Связка:</strong> захват → обработка на станции → вывод. HDMI ноутбука/ПК — всегда только выход и не заменяет вход захвата.</div>
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide split" data-title="Видеокарты">
      <div class="copy">
        <div class="eyebrow reveal">Рабочая станция</div>
        <h2 class="reveal" style="--d:60ms">Видеокарты (GPU)</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Видеокарта</strong> на эфирной станции — не «для игр», а ускоритель композиции, кодирования стрима и вывода на мониторы оператора. Её не следует путать с картой захвата или платой профессионального вывода в тракт.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li><strong>Композиция:</strong> слои, переходы, ключи, NDI, превью в микшерном ПО</li>
          <li><strong>Кодирование:</strong> аппаратный энкодер (например NVENC) снижает нагрузку на CPU при стриме</li>
          <li><strong>Мониторинг:</strong> несколько выходов на экраны инженера и режиссёра</li>
          <li><strong>Запас:</strong> чем больше входов и эффектов, тем выше требования к GPU и памяти</li>
        </ul>
        <div class="note reveal" style="--d:220ms"><strong>Зачем нужна:</strong> без достаточного GPU станция «плывёт» по кадрам при сложной программе. При этом мониторный HDMI с видеокарты не заменяет SDI/HDMI‑вывод через карту playback в эфирный тракт.</div>
      </div>
      {photo("rtx-5090.jpg", "GeForce RTX 5090", "Wikimedia Commons · Palit GeForce RTX 5090", contain=True)}
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide split" data-title="Стрим / запись">
      <div class="copy">
        <div class="eyebrow reveal">Вывод</div>
        <h2 class="reveal" style="--d:60ms">Стриммеры и рекордеры</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Железный стриммер/рекордер</strong> кодирует и/или записывает программу отдельно от рабочей станции — снижая риск потери архива при сбое ОС.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li>Рекордер — файл на SSD (Program / ISO)</li>
          <li>Стриммер — RTMP/SRT на платформу</li>
          <li>Запись только на тот же ПК уязвима к зависанию станции</li>
        </ul>
      </div>
      {photo("bmd-hyperdeck.jpg", "HyperDeck рекордер", "Wikimedia Commons · HyperDeck Studio")}
    </section>"""
    )

    slides.append(
        f"""
    <section class="slide split" data-title="Звук">
      <div class="copy">
        <div class="eyebrow reveal">Звук</div>
        <h2 class="reveal" style="--d:60ms">Карты и синхрон</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Звуковая карта / аудиоинтерфейс</strong> обеспечивает качественный ввод-вывод и контроль уровней, когда звук идёт отдельным трактом.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li><strong>«Звук отстаёт»</strong> — разные пути: видео по сети, звук по XLR/USB</li>
          <li>Коррекция — <strong>delay / lip-sync</strong> в микшере или ПО</li>
          <li>Согласование семплрейта (обычно 48 kHz) с видеорядом</li>
        </ul>
      </div>
      {photo("audio-iface.jpg", "Аудиоинтерфейсы", "Wikimedia Commons · Focusrite")}
    </section>"""
    )

    slides.append(
        """
    <section class="slide solo" data-title="Практика">
      <div class="eyebrow reveal">Мини-практика · 10 мин</div>
      <h2 class="reveal" style="--d:60ms">Четыре схемы</h2>
      <p class="sub reveal" style="--d:100ms">На каждом следующем слайде — схема из узлов занятия. Задача: определить типы соединений (SDI / HDMI / NDI) на связях и найти <strong>ровно одну ошибку</strong>.</p>
    </section>"""
    )


    def blank_edge() -> str:
        return '<div class="flow-edge"><span>→</span><span class="wire">?</span></div>'

    practices = [
        (
            "Схема A",
            "Камера SDI должна попасть в ноутбук и далее в стрим. Подпишите соединения и найдите одну ошибку.",
            "".join([
                '<div class="flow">',
                node("источник", "Камера SDI"),
                blank_edge(),
                node("путь", "Кабель"),
                blank_edge(),
                node("захват", "Ноутбук"),
                blank_edge(),
                node("вывод", "Стриммер"),
                "</div>",
            ]),
            "Правильные типы: SDI (или NDI после энкодера) до станции; RTMP/SRT до платформы. На ошибочной версии между камерой и ноутбуком указан HDMI.",
            "HDMI нельзя использовать как вход ноутбука/ПК. Нужна карта захвата или сетевой протокол.",
        ),
        (
            "Схема B",
            "Камера HDMI, микшер V-60HD и рекордер на длинной дистанции. Подпишите соединения и найдите одну ошибку.",
            "".join([
                '<div class="flow">',
                node("источник", "Камера HDMI"),
                blank_edge(),
                node("путь", "Линия 40 м"),
                blank_edge(),
                node("обработка", "V-60HD"),
                blank_edge(),
                node("запись", "Рекордер"),
                "</div>",
            ]),
            "Правильные типы: HDMI→конвертер→SDI до микшера; SDI до рекордера.",
            "Длинный HDMI без конвертации в SDI (или без сетевого тракта).",
        ),
        (
            "Схема C",
            "Один SDI-источник нужен и микшеру, и рекордеру. Подпишите соединения и найдите одну ошибку.",
            "".join([
                '<div class="flow">',
                node("источник", "Камера SDI"),
                blank_edge(),
                node("путь", "Разветвитель"),
                blank_edge(),
                node("обработка", "Микшер"),
                blank_edge(),
                node("запись", "Рекордер"),
                "</div>",
            ]),
            "Правильные типы: SDI до активного сплиттера; SDI до микшера и SDI до рекордера (либо матрица).",
            "Пассивный тройник вместо активного сплиттера или выходов матрицы.",
        ),
        (
            "Схема D",
            "ПК 1920×1080 выводят на экран 768×1280. Подпишите соединения и найдите одну ошибку.",
            "".join([
                '<div class="flow">',
                node("источник", "ПК 1080p"),
                blank_edge(),
                node("обработка", "Микшер"),
                blank_edge(),
                node("формат", "Обработка кадра"),
                blank_edge(),
                node("экран", "768×1280"),
                "</div>",
            ]),
            "Правильные типы: HDMI до микшера; далее через скейлер (не stretch) на экран.",
            "Принудительное растягивание без скейлера — искажение пропорций.",
        ),
    ]


    for title, lead, diagram, wires, err in practices:
        slides.append(
            f"""
    <section class="slide" data-title="{title}" data-fragments="1">
      <div class="eyebrow">Практика</div>
      <h2>{title}</h2>
      <p class="sub">{lead}</p>
      {diagram}
      <div class="answer-box fragment">
        <h3>Ответ</h3>
        <p style="color:var(--muted);margin-bottom:.45rem">{wires}</p>
        <p style="color:var(--text)"><strong>Ошибка:</strong> {err}</p>
      </div>
    </section>"""
        )

    slides.append(
        """
    <section class="slide solo" data-title="Итог">
      <div class="eyebrow reveal">Итог</div>
      <h2 class="reveal" style="--d:60ms">Сначала задача, потом тип соединения, потом железо — а не наоборот.</h2>
      <p class="sub reveal" style="--d:120ms">Источник → путь → обработка → вывод. Оборудование выбираем под задачу.</p>
      <ul class="list-plain reveal" style="--d:180ms">
        <li>Конвертер ≠ адаптер; сплиттер ≠ матрица</li>
        <li>HDMI персонального компьютера — всегда только выход</li>
      </ul>
      <div class="note reveal" style="--d:260ms"><strong>Диагностика:</strong> исследование неисправности ведут от источника к конечному приёмнику; устранение начинают на участке сразу после последнего звена, где сигнал ещё присутствовал в штатном виде.</div>
    </section>"""
    )

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ПТС · Оборудование для трансляций · ТЕХ ГУАП</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@400;600;700&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <style>{CSS}</style>
</head>
<body>
  <div class="orb a"></div><div class="orb b"></div>
  <div class="deck" id="deck">
{''.join(slides)}
  </div>
  <div class="footer-bar">
    <div>ТЕХ ГУАП · ПТС</div>
    <div class="hint"><span class="key">←</span><span class="key">→</span><span>шаг / слайд</span><span id="counter">1 / {len(slides)}</span></div>
  </div>
  <div class="progress-track"><div class="progress" id="progress"></div></div>
  <script>{JS}</script>
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size / 1024 / 1024:.1f} MiB), slides={len(slides)}")


if __name__ == "__main__":
    build()
