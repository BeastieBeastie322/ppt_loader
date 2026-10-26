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


def build() -> None:
    slides: list[str] = []

    # 1 Title
    slides.append(f'''
    <section class="slide active split" data-title="Титул">
      <div class="copy">
        <div class="eyebrow reveal">ТЕХ ГУАП · направление ПТС</div>
        <h1 class="reveal" style="--d:80ms">Оборудование<br>для трансляций</h1>
        <p class="sub reveal" style="--d:160ms">Какая задача → какое соединение → какое оборудование</p>
        <div class="hero-meta reveal" style="--d:240ms">Не спецификации наизусть — логика тракта</div>
      </div>
      {photo("live-setup.jpg", "Стойка трансляции", "Wikimedia Commons")}
    </section>''')

    # 2 Map
    slides.append(f'''
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
    </section>''')

    # 3 Cameras
    slides.append(f'''
    <section class="slide split" data-title="Камеры">
      <div class="copy">
        <div class="eyebrow reveal">Источник · 01</div>
        <h2 class="reveal" style="--d:60ms">Камеры</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Источник сигнала</strong> — устройство, которое впервые формирует видео. Камера отдаёт кадр + метаданные формата в кабель или сеть.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li><strong>PTZ</strong> — pan/tilt/zoom, управление по сети (VISCA/IP)</li>
          <li><strong>Камкордер / cinema</strong> — ручная работа оператора</li>
          <li><strong>Выход:</strong> SDI (BNC), HDMI, иногда NDI</li>
          <li><strong>Параметры:</strong> разрешение, fps, progressive/interlace</li>
        </ul>
        <div class="note reveal" style="--d:220ms"><strong>Термин:</strong> «лок» сигнала — приёмник видит стабильный вход. Нет лока — дальше чинить бессмысленно.</div>
      </div>
      {photo("cam-tripod.jpg", "Камера на штативе", "Wikimedia Commons · Blackmagic URSA")}
    </section>''')

    # 4 PC
    slides.append(f'''
    <section class="slide split" data-title="ПК">
      <div class="copy">
        <div class="eyebrow reveal">Источник · 02</div>
        <h2 class="reveal" style="--d:60ms">ПК и ноутбуки</h2>
        <p class="sub reveal" style="--d:100ms">Компьютер — источник <strong>компьютерной графики</strong>: презентации, браузер, vMix/графика, Zoom-окно.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li><strong>Выход:</strong> HDMI / DisplayPort / USB-C → адаптер</li>
          <li><strong>EDID</strong> — «паспорт» монитора; без него ПК может отдать «не тот» режим</li>
          <li><strong>Важно:</strong> HDMI на ноутбуке/ПК — почти всегда <em>только выход</em>, не вход</li>
        </ul>
        <div class="tag-row reveal" style="--d:220ms">
          <span class="tag on">презентация</span><span class="tag on">браузер</span><span class="tag">NDI Screen Capture</span>
        </div>
      </div>
      {photo("laptop.jpg", "Ноутбук с презентацией", "Wikimedia Commons")}
    </section>''')

    # 5 Other sources
    slides.append(f'''
    <section class="slide split" data-title="Внешний сигнал">
      <div class="copy">
        <div class="eyebrow reveal">Источник · 03</div>
        <h2 class="reveal" style="--d:60ms">Другие устройства</h2>
        <p class="sub reveal" style="--d:100ms">Внешний сигнал — уже собранная программа с другого микшера, плеера, медиасервера, телемоста.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li><strong>PGM с другого пульта</strong> — «чистая» программа в наш тракт</li>
          <li><strong>Плеер / медиасервер</strong> — ролики, заставки, таймкод</li>
          <li><strong>ВКС / телемост</strong> — удалённый спикер как отдельный вход</li>
        </ul>
        <div class="note reveal" style="--d:220ms"><strong>Практика:</strong> внешний сигнал тоже источник. У него есть формат и интерфейс — согласуйте так же, как камеру.</div>
      </div>
      {photo("bmd-atem.jpg", "Видеомикшер как источник", "Wikimedia Commons · Blackmagic ATEM")}
    </section>''')

    # 6 Path overview
    slides.append(f'''
    <section class="slide split" data-title="Путь сигнала">
      <div class="copy">
        <div class="eyebrow reveal">Путь</div>
        <h2 class="reveal" style="--d:60ms">Как сигнал доезжает</h2>
        <p class="sub reveal" style="--d:100ms">Между источником и обработкой сигнал идёт по кабелю, по сети или через «коробочки»-преобразователи — из‑за разных разъёмов, длин линий и форматов.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li><strong>Кабель</strong> — HDMI, SDI, XLR, Ethernet</li>
          <li><strong>Сеть</strong> — NDI, SRT, RTMP (сигнал «по IP»)</li>
          <li><strong>Устройства на пути</strong> — конвертер, сплиттер, матрица</li>
        </ul>
      </div>
      {photo("path-setup.jpg", "Кабели и стойка", "Wikimedia Commons")}
    </section>''')

    # 7 Cables
    slides.append(f'''
    <section class="slide" data-title="Кабели">
      <div class="eyebrow reveal">Путь · кабели</div>
      <h2 class="reveal" style="--d:40ms">Кабели и интерфейсы</h2>
      <p class="sub reveal" style="--d:80ms">Кабель — не «просто провод», а стандарт: разъём + электрический/цифровой протокол + ограничения по длине.</p>
      <div class="grid grid-4">
        <div class="tile reveal-scale" style="--d:120ms"><img src="{img('cable-hdmi-plug.jpg')}" alt="HDMI"/><div class="num">HDMI</div><h3>HDMI</h3><p>Бытовой/компьютерный видео+звук. Короткие линии, чувствителен к качеству кабеля.</p></div>
        <div class="tile reveal-scale" style="--d:160ms"><img src="{img('bnc.jpg')}" alt="BNC"/><div class="num">SDI</div><h3>SDI (BNC)</h3><p>Проф. видео. Level A / Level B — разные упаковки 3G-SDI. Длиннее HDMI, надёжнее на площадке.</p></div>
        <div class="tile reveal-scale" style="--d:200ms"><img src="{img('cable-xlr.jpg')}" alt="XLR"/><div class="num">XLR</div><h3>XLR</h3><p>Балансный звук, фантомное питание +48V для конденсаторных микрофонов.</p></div>
        <div class="tile reveal-scale" style="--d:240ms"><img src="{img('cable-eth.jpg')}" alt="Ethernet"/><div class="num">ETH</div><h3>Ethernet</h3><p>Сеть: NDI, управление PTZ, стрим, Dante. Качество линка = качество эфира.</p></div>
      </div>
      <div class="note reveal" style="--d:300ms"><strong>SDI Level A / Level B:</strong> оба могут нести 1080p50/60 по 3G, но упаковка разная — устройства должны договориться о режиме.</div>
    </section>''')

    # 8 Transformers map
    slides.append(f'''
    <section class="slide split" data-title="Преобразователи">
      <div class="copy">
        <div class="eyebrow reveal">Путь · преобразователи</div>
        <h2 class="reveal" style="--d:60ms">Четыре семейства «коробочек»</h2>
        <p class="sub reveal" style="--d:100ms">На пути сигнала почти всегда стоит что‑то из этого списка. Путать их нельзя — чините разное.</p>
        <div class="big-list reveal" style="--d:160ms">
          <div class="item"><div class="n">01</div><div><h3>Конверторы</h3><p>Меняют стандарт сигнала (HDMI↔SDI)</p></div></div>
          <div class="item"><div class="n">02</div><div><h3>Адаптеры</h3><p>Меняют только разъём/форм-фактор</p></div></div>
          <div class="item"><div class="n">03</div><div><h3>Сплиттеры</h3><p>Раздают один сигнал на N выходов</p></div></div>
          <div class="item"><div class="n">04</div><div><h3>Соединители</h3><p>«Бочонки», удлинители, пассивные тройники</p></div></div>
        </div>
      </div>
      {photo("bmd-converters.jpg", "Mini-конвертеры", "Wikimedia Commons · Blackmagic Mini Converters")}
    </section>''')

    # 9 Converters
    slides.append(f'''
    <section class="slide split" data-title="Конверторы">
      <div class="copy">
        <div class="eyebrow reveal">Конверторы</div>
        <h2 class="reveal" style="--d:60ms">Конвертер ≠ адаптер</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Конвертер</strong> переводит один <em>стандарт сигнала</em> в другой: перепаковывает данные, часто с питанием и чипом.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li><strong>Пример:</strong> HDMI и SDI — разные стандарты → нужен именно конвертер</li>
          <li>Может делать up/down/cross conversion (разрешение, fps)</li>
          <li>Часто умеет встраивать/доставать звук (embed/de-embed)</li>
        </ul>
        <div class="note reveal" style="--d:220ms"><strong>Правило:</strong> если разъёмы разные <em>и</em> протоколы разные — это конвертер, не «переходник за 200 ₽».</div>
      </div>
      {photo("bmd-converters.jpg", "HDMI/SDI конвертеры", "Wikimedia Commons")}
    </section>''')

    # 10 Adapters
    slides.append(f'''
    <section class="slide split" data-title="Адаптеры">
      <div class="copy">
        <div class="eyebrow reveal">Адаптеры</div>
        <h2 class="reveal" style="--d:60ms">Только разъём</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Адаптер</strong> меняет форм-фактор разъёма, не перекодируя сигнал: USB-C→HDMI (иногда с активной электроникой DisplayPort Alt Mode), HDMI-A→HDMI-C и т.п.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li>Не превратит HDMI в SDI</li>
          <li>Не «починит» несовместимый формат 1080i↔1080p</li>
          <li>Активный USB-C хаб ≠ пассивный кусок металла</li>
        </ul>
        <div class="note reveal" style="--d:220ms"><strong>Ошибка новичка:</strong> купить «HDMI→SDI переходник» без чипа — и ждать чуда. Чуда не будет.</div>
      </div>
      {photo("connectors-panel.jpg", "Разъёмы и кабели", "Wikimedia Commons")}
    </section>''')

    # 11 Splitters
    slides.append(f'''
    <section class="slide split" data-title="Сплиттеры">
      <div class="copy">
        <div class="eyebrow reveal">Сплиттеры</div>
        <h2 class="reveal" style="--d:60ms">1 → N</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Сплиттер (distribution amplifier)</strong> копирует один вход на несколько одинаковых выходов: микшер + рекордер + превью.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li>Активный сплиттер — с питанием и реклокингом</li>
          <li>Пассивный «тройник» — риск потерять уровень/лок</li>
          <li>Не путать с матрицей: сплиттер <em>раздаёт</em>, матрица <em>переключает</em></li>
        </ul>
      </div>
      {photo("sdi-gear.jpg", "Видеокоммутация", "Wikimedia Commons")}
    </section>''')

    # 12 Connectors
    slides.append(f'''
    <section class="slide split" data-title="Соединители">
      <div class="copy">
        <div class="eyebrow reveal">Соединители</div>
        <h2 class="reveal" style="--d:60ms">Бочонки и удлинение</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Соединитель («бочонок»)</strong> — механическое стыкование двух кабелей одного типа (BNC–BNC, HDMI coupler). Пассивные сплиттеры рядом по полке, но по роли опаснее.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li>Удлинить линию без нового длинного кабеля</li>
          <li>Сменить пол разъёма (папа/мама)</li>
          <li>Каждое пассивное соединение — точка отказа</li>
        </ul>
      </div>
      {photo("bnc.jpg", "BNC-разъём", "Wikimedia Commons")}
    </section>''')

    # 13 Scheme
    slides.append(f'''
    <section class="slide" data-title="Схема HDMI→SDI">
      <div class="eyebrow reveal">Связка</div>
      <h2 class="reveal" style="--d:40ms">Камера HDMI → SDI-сплиттер</h2>
      <p class="sub reveal" style="--d:80ms">Типовая задача: камера отдаёт HDMI, а тракт площадки — SDI. Нужен конвертер, потом раздача.</p>
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
        <div class="tile reveal-scale" style="--d:200ms"><img src="{img('cam-bmd.jpg')}" alt="камера"/><h3>Почему так</h3><p>Не тащим длинный HDMI по залу. SDI держит дистанцию и разъёмы BNC надёжнее на ногах публики.</p></div>
        <div class="tile reveal-scale" style="--d:260ms"><img src="{img('bmd-converters.jpg')}" alt="конвертер"/><h3>Где ошибаются</h3><p>Ставят адаптер вместо конвертера; забывают питание конвертера; путают Level A/B на 3G.</p></div>
      </div>
    </section>''')

    # 14 Processing overview
    slides.append(f'''
    <section class="slide split" data-title="Обработка">
      <div class="copy">
        <div class="eyebrow reveal">Обработка</div>
        <h2 class="reveal" style="--d:60ms">Микшеры, скейлеры, матрицы</h2>
        <p class="sub reveal" style="--d:100ms">Здесь из входов собирают программу: переключают, масштабируют, маршрутизируют.</p>
        <div class="big-list reveal" style="--d:160ms">
          <div class="item"><div class="n">01</div><div><h3>Микшер</h3><p>Выбирает, что в PGM прямо сейчас</p></div></div>
          <div class="item"><div class="n">02</div><div><h3>Скейлер</h3><p>Подгоняет разрешение/геометрию под экран</p></div></div>
          <div class="item"><div class="n">03</div><div><h3>Матрица</h3><p>Любой вход → любой выход (M×N)</p></div></div>
        </div>
      </div>
      {photo("atem-panel.jpg", "Панель микшера", "Wikimedia Commons · ATEM panel")}
    </section>''')

    # 15 Mixers Roland V-60HD
    slides.append(f'''
    <section class="slide split" data-title="Микшеры">
      <div class="copy">
        <div class="eyebrow reveal">Микшеры</div>
        <h2 class="reveal" style="--d:60ms">Roland V-60HD</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Видеомикшер (switcher)</strong> — устройство/софт, которое в реальном времени выбирает PGM (программа) и PVW (превью), делает переходы, PinP, ключи.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li>4× SDI + 2× HDMI (со скейлом на HDMI)</li>
          <li>Выходы PGM / AUX / Multi-View</li>
          <li>Встроенный аудимикшер, XLR, автомикс</li>
        </ul>
        <div class="tag-row reveal" style="--d:220ms">
          <span class="tag on">PGM</span><span class="tag on">PVW</span><span class="tag on">AUX</span><span class="tag">T-bar</span>
        </div>
      </div>
      {photo("roland-v60hd-main.jpg", "Roland V-60HD", "Roland Pro A/V · V-60HD", contain=True)}
    </section>''')

    # 16 Scalers
    slides.append(f'''
    <section class="slide split" data-title="Скейлеры">
      <div class="copy">
        <div class="eyebrow reveal">Скейлеры</div>
        <h2 class="reveal" style="--d:60ms">Подгон под экран</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Скейлер</strong> меняет геометрию кадра: разрешение, соотношение сторон, ориентацию — без «тупого растягивания».</p>
        <div class="panel reveal" style="--d:160ms">
          <h3>Кейс</h3>
          <ul class="list-plain">
            <li><strong>Вход:</strong> Full HD 1920×1080</li>
            <li><strong>Экран:</strong> 768×1280 (вертикальный)</li>
            <li><strong>Решение:</strong> ресайз и fit по высоте без чёрных полос / с осмысленным crop</li>
            <li><strong>Ошибка:</strong> «растянуть» в плеере — пропорции поедут</li>
          </ul>
        </div>
      </div>
      {photo("scaler-box.jpg", "Устройство обработки видео", "Wikimedia Commons")}
    </section>''')

    # 17 Matrices
    slides.append(f'''
    <section class="slide split" data-title="Матрицы">
      <div class="copy">
        <div class="eyebrow reveal">Матрицы / видеохабы</div>
        <h2 class="reveal" style="--d:60ms">Несколько × несколько</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Матрица (router / Videohub)</strong> — коммутатор M входов на N выходов. Любой источник можно послать на любой выход.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li>Сплиттер: один вход → все выходы одинаковые</li>
          <li>Матрица: входы и выходы независимо назначаются</li>
          <li>Пресеты сцен = меньше перетыкания кабелей в эфире</li>
        </ul>
      </div>
      {photo("bmd-videohub.jpg", "Blackmagic Videohub", "Wikimedia Commons · Videohub")}
    </section>''')

    # 18 Capture cards
    slides.append(f'''
    <section class="slide" data-title="Карты захвата">
      <div class="eyebrow reveal">Карты ввода</div>
      <h2 class="reveal" style="--d:40ms">USB и PCIe</h2>
      <p class="sub reveal" style="--d:80ms"><strong>Карта захвата (capture)</strong> — мост SDI/HDMI → компьютер. Без неё «провода» в vMix не попадут.</p>
      <div class="grid grid-2">
        <div class="tile reveal-scale" style="--d:120ms">
          <img src="{img('capture-usb2.jpg')}" alt="USB capture"/>
          <div class="num">USB</div>
          <h3>USB capture</h3>
          <p>Удобно, портативно. USB 3.x ≈ 5–10 Гбит/с на контроллер; делите полосу с дисками и другими устройствами. Latency и стабильность зависят от чипсета/драйвера.</p>
        </div>
        <div class="tile reveal-scale" style="--d:180ms">
          <img src="{img('capture-datapath.jpg')}" alt="PCIe capture"/>
          <div class="num">PCIe</div>
          <h3>PCIe (DeckLink и др.)</h3>
          <p>Слоты x4/x8/x16 — отдельные линии PCI Express. Выше запас по полосе, ниже сюрпризы на длинном эфире, несколько входов на одной карте.</p>
        </div>
      </div>
      <div class="note reveal" style="--d:240ms"><strong>Линии PCIe:</strong> карта x4 в слоте x4 получает свою полосу; «электрически x16, механически x4» читайте в мануале платы.</div>
    </section>''')

    # 19 Output vs GPU
    slides.append(f'''
    <section class="slide split" data-title="Вывод и GPU">
      <div class="copy">
        <div class="eyebrow reveal">Вывод · видеокарта</div>
        <h2 class="reveal" style="--d:60ms">Захват → обработка → вывод</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Карта вывода</strong> отдаёт программу обратно в SDI/HDMI. <strong>Видеокарта (GPU)</strong> — ускоритель композиции и кодирования (NVENC), плюс мониторы.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li>Capture (SDI/HDMI) → рабочая станция</li>
          <li>GPU: слои, NDI, энкод стрима, несколько дисплеев</li>
          <li class=""><strong>HDMI в ноутбуке/ПК не работает на вход</strong></li>
        </ul>
        <div class="note reveal" style="--d:220ms"><strong>Вывод ≠ GPU:</strong> мониторный HDMI с видеокарты — не профессиональный PGM-выход в тракт. Для эфирного SDI нужна карта вывода / конвертер.</div>
      </div>
      {photo("gpu.jpg", "Видеокарта", "Wikimedia Commons · NVIDIA GeForce")}
    </section>''')

    # 20 Streamers recorders
    slides.append(f'''
    <section class="slide split" data-title="Стрим / запись">
      <div class="copy">
        <div class="eyebrow reveal">Вывод</div>
        <h2 class="reveal" style="--d:60ms">Стриммеры и рекордеры</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Железный стриммер/рекордер</strong> пишет и/или отдаёт эфир отдельно от рабочей станции — меньше шансов потерять архив из‑за зависания ОС.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li>Рекордер (HyperDeck и др.) — файл на SSD, ISO/Program</li>
          <li>Стриммер — RTMP/SRT на платформу</li>
          <li>Почему не «только на комп»: синий экран = нет ни эфира, ни файла</li>
        </ul>
      </div>
      {photo("bmd-hyperdeck.jpg", "HyperDeck рекордер", "Wikimedia Commons · HyperDeck Studio")}
    </section>''')

    # 21 Audio
    slides.append(f'''
    <section class="slide split" data-title="Звук">
      <div class="copy">
        <div class="eyebrow reveal">Звук</div>
        <h2 class="reveal" style="--d:60ms">Карты и синхрон</h2>
        <p class="sub reveal" style="--d:100ms"><strong>Звуковая карта / аудиоинтерфейс</strong> — качественный ввод-вывод и контроль уровней. Нужна, когда звук идёт отдельным трактом и его надо свести с видео.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li><strong>«Звук отстаёт»</strong> — разные пути: видео по NDI, звук по XLR/USB</li>
          <li>Лечится <strong>delay / lip-sync</strong> в микшере или софте</li>
          <li>Сверяйте семплрейт 48 kHz с видеорядом</li>
        </ul>
      </div>
      {photo("audio-iface.jpg", "Аудиоинтерфейсы", "Wikimedia Commons · Focusrite")}
    </section>''')

    # 22 Practice intro
    slides.append(f'''
    <section class="slide split" data-title="Практика">
      <div class="copy">
        <div class="eyebrow reveal">Мини-практика · 10 мин</div>
        <h2 class="reveal" style="--d:60ms">Четыре схемы</h2>
        <p class="sub reveal" style="--d:100ms">На каждом слайде — схема. Задача: подписать стрелки типом соединения (SDI / HDMI / NDI) и найти <strong>одну ошибку</strong>.</p>
        <div class="note reveal" style="--d:180ms"><strong>Критерий:</strong> не «угадать бренд», а объяснить, почему такой интерфейс и где разрыв логики.</div>
      </div>
      {photo("roland-v60hd.jpg", "Roland V-60HD", "Roland Pro A/V")}
    </section>''')

    # 23-26 practice schemes
    practices = [
        ("Схема A", "Камера SDI → ноутбук по HDMI без карты захвата",
         "Камера SDI → ? → Ноутбук → Стрим",
         "Ошибка: HDMI ноутбука не принимает вход. Нужна capture-карта (USB/PCIe) или NDI-энкодер.",
         "cam-ptz.jpg"),
        ("Схема B", "Камера HDMI → длинный HDMI 40 м → микшер",
         "Камера HDMI → HDMI 40 м → V-60HD",
         "Ошибка: длинный HDMI нестабилен. Конвертер HDMI→SDI + SDI-кабель (или оптика/NDI).",
         "cable-hdmi.jpg"),
        ("Схема C", "Один источник на микшер и рекордер через пассивный тройник",
         "Камера → пассивный BNC-тройник → микшер + рекордер",
         "Ошибка: пассивный сплит. Нужен активный SDI DA / выход матрицы.",
         "bmd-hyperdeck.jpg"),
        ("Схема D", "Вертикальный экран без скейлера",
         "ПК 1920×1080 → микшер → экран 768×1280 «stretch»",
         "Ошибка: растягивание. Нужен скейлер (fit/crop), не distort.",
         "laptop.jpg"),
    ]
    for title, lead, scheme, err, pic in practices:
        slides.append(f'''
    <section class="slide split" data-title="{title}">
      <div class="copy">
        <div class="eyebrow reveal">Практика</div>
        <h2 class="reveal" style="--d:60ms">{title}</h2>
        <p class="sub reveal" style="--d:100ms">{lead}</p>
        <div class="panel reveal" style="--d:160ms"><h3>Цепочка</h3><p style="color:var(--muted);font-size:1rem;line-height:1.45">{scheme}</p></div>
        <div class="note reveal" style="--d:220ms"><strong>Ошибка:</strong> {err}</div>
      </div>
      {photo(pic, title, "")}
    </section>''')

    # 27 Summary
    slides.append(f'''
    <section class="slide split" data-title="Итог">
      <div class="copy">
        <div class="eyebrow reveal">Итог</div>
        <h2 class="reveal" style="--d:60ms">Думать трактом</h2>
        <p class="sub reveal" style="--d:100ms">Источник → путь → обработка → вывод. Оборудование выбираем под задачу и соединение.</p>
        <ul class="list-plain reveal" style="--d:160ms">
          <li>Конвертер ≠ адаптер; сплиттер ≠ матрица</li>
          <li>HDMI ПК — не вход; длинные линии — зона SDI/сети</li>
          <li>Железная запись страхует софт; звук синхронизируют delay</li>
        </ul>
      </div>
      {photo("bmd-atem.jpg", "Эфирный комплект", "Wikimedia Commons")}
    </section>''')

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
