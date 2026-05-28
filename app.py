import math
import random

import streamlit as st


st.set_page_config(
    page_title="國小時間與角度教學",
    page_icon="⏰",
    layout="wide",
)


st.markdown(
    """
    <style>
        .main .block-container {
            max-width: 1180px;
            padding-top: 2rem;
        }
        .hero {
            padding: 22px 24px;
            border: 1px solid #d6e1e7;
            border-radius: 8px;
            background: linear-gradient(135deg, #f8fcff 0%, #fff8f0 100%);
        }
        .hero h1 {
            margin: 0 0 8px 0;
            color: #233f4a;
        }
        .hero p {
            margin: 0;
            color: #4d6670;
            font-size: 1.05rem;
        }
        .chip {
            display: inline-block;
            margin: 6px 8px 0 0;
            padding: 6px 10px;
            border: 1px solid #c7d7df;
            border-radius: 8px;
            background: #ffffff;
            color: #233f4a;
            font-weight: 700;
        }
        .svg-wrap {
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }
        .formula {
            font-size: 1.05rem;
            line-height: 1.8;
        }
        .good {
            padding: 10px 12px;
            border-left: 5px solid #20875a;
            border-radius: 6px;
            background: #effaf4;
        }
        .warm {
            padding: 10px 12px;
            border-left: 5px solid #c76528;
            border-radius: 6px;
            background: #fff6ec;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def time_label(hour: int, minute: int) -> str:
    return f"{hour % 24:02d}:{minute:02d}"


def twelve_hour_label(hour: int, minute: int) -> str:
    display_hour = hour % 12 or 12
    return f"{display_hour}:{minute:02d}"


def add_minutes(hour: int, minute: int, delta: int) -> tuple[int, int]:
    total = (hour * 60 + minute + delta) % (24 * 60)
    return total // 60, total % 60


def angle_name(degrees: int) -> str:
    if degrees < 90:
        return "銳角"
    if degrees == 90:
        return "直角"
    if degrees < 180:
        return "鈍角"
    return "平角"


def render_svg(svg: str, height: int) -> None:
    st.markdown(
        f'<div class="svg-wrap" style="height:{height}px">{svg}</div>',
        unsafe_allow_html=True,
    )


def clock_svg(hour: int, minute: int, size: int = 320) -> str:
    center = size / 2
    radius = size * 0.42
    hour_angle = ((hour % 12) + minute / 60) * 30
    minute_angle = minute * 6

    def point(angle: float, length: float) -> tuple[float, float]:
        rad = math.radians(angle - 90)
        return center + math.cos(rad) * length, center + math.sin(rad) * length

    ticks = []
    for value in range(60):
        angle = value * 6
        outer_x, outer_y = point(angle, radius)
        inner = radius - (16 if value % 5 == 0 else 7)
        inner_x, inner_y = point(angle, inner)
        stroke = "#263238" if value % 5 == 0 else "#94a8b1"
        width = 3 if value % 5 == 0 else 1
        ticks.append(
            f'<line x1="{inner_x:.1f}" y1="{inner_y:.1f}" '
            f'x2="{outer_x:.1f}" y2="{outer_y:.1f}" stroke="{stroke}" '
            f'stroke-width="{width}" stroke-linecap="round" />'
        )

    numbers = []
    for number in range(1, 13):
        x, y = point(number * 30, radius - 34)
        numbers.append(
            f'<text x="{x:.1f}" y="{y + 6:.1f}" text-anchor="middle" '
            f'font-size="18" font-family="Arial" fill="#263238" '
            f'font-weight="700">{number}</text>'
        )

    hour_x, hour_y = point(hour_angle, radius * 0.48)
    minute_x, minute_y = point(minute_angle, radius * 0.72)

    return f"""
    <svg viewBox="0 0 {size} {size}" width="100%" height="100%" role="img" aria-label="時鐘">
        <circle cx="{center}" cy="{center}" r="{radius + 14}" fill="#fffdf8" stroke="#2f5f72" stroke-width="7" />
        <circle cx="{center}" cy="{center}" r="{radius + 4}" fill="#ffffff" stroke="#d5e3e8" stroke-width="2" />
        {''.join(ticks)}
        {''.join(numbers)}
        <line x1="{center}" y1="{center}" x2="{hour_x:.1f}" y2="{hour_y:.1f}" stroke="#24495a" stroke-width="9" stroke-linecap="round" />
        <line x1="{center}" y1="{center}" x2="{minute_x:.1f}" y2="{minute_y:.1f}" stroke="#d85c3a" stroke-width="5" stroke-linecap="round" />
        <circle cx="{center}" cy="{center}" r="9" fill="#24495a" />
        <text x="{center}" y="{size - 18}" text-anchor="middle" font-size="17" font-family="Arial" fill="#47606b" font-weight="700">
            {twelve_hour_label(hour, minute)}
        </text>
    </svg>
    """


def protractor_svg(degrees: int, size: int = 360) -> str:
    width = size
    height = int(size * 0.64)
    cx = width / 2
    cy = height * 0.82
    radius = width * 0.39
    angle = max(0, min(180, degrees))
    rad = math.radians(angle)
    arm_x = cx + math.cos(rad) * radius
    arm_y = cy - math.sin(rad) * radius
    arc_x = cx + math.cos(rad) * (radius * 0.38)
    arc_y = cy - math.sin(rad) * (radius * 0.38)

    ticks = []
    labels = []
    for value in range(0, 181, 5):
        tick_rad = math.radians(value)
        outer_x = cx + math.cos(tick_rad) * radius
        outer_y = cy - math.sin(tick_rad) * radius
        inner_length = radius - (17 if value % 10 == 0 else 9)
        inner_x = cx + math.cos(tick_rad) * inner_length
        inner_y = cy - math.sin(tick_rad) * inner_length
        stroke = "#294a56" if value % 10 == 0 else "#8aa0a8"
        width_tick = 2 if value % 10 == 0 else 1
        ticks.append(
            f'<line x1="{inner_x:.1f}" y1="{inner_y:.1f}" '
            f'x2="{outer_x:.1f}" y2="{outer_y:.1f}" stroke="{stroke}" '
            f'stroke-width="{width_tick}" stroke-linecap="round" />'
        )
        if value % 30 == 0:
            label_x = cx + math.cos(tick_rad) * (radius - 36)
            label_y = cy - math.sin(tick_rad) * (radius - 36)
            labels.append(
                f'<text x="{label_x:.1f}" y="{label_y + 5:.1f}" '
                f'text-anchor="middle" font-size="13" font-family="Arial" '
                f'fill="#294a56" font-weight="700">{value}</text>'
            )

    return f"""
    <svg viewBox="0 0 {width} {height}" width="100%" height="100%" role="img" aria-label="量角器">
        <path d="M {cx - radius:.1f} {cy:.1f} A {radius:.1f} {radius:.1f} 0 0 1 {cx + radius:.1f} {cy:.1f}"
              fill="#f7fbfc" stroke="#2f5f72" stroke-width="5" />
        <path d="M {cx - radius + 18:.1f} {cy:.1f} A {radius - 18:.1f} {radius - 18:.1f} 0 0 1 {cx + radius - 18:.1f} {cy:.1f}"
              fill="none" stroke="#d7e4ea" stroke-width="2" />
        {''.join(ticks)}
        {''.join(labels)}
        <line x1="{cx - radius - 10:.1f}" y1="{cy:.1f}" x2="{cx + radius + 10:.1f}" y2="{cy:.1f}"
              stroke="#273f49" stroke-width="4" stroke-linecap="round" />
        <path d="M {cx:.1f} {cy:.1f} L {cx + radius * 0.38:.1f} {cy:.1f}
                 A {radius * 0.38:.1f} {radius * 0.38:.1f} 0 0 0 {arc_x:.1f} {arc_y:.1f} Z"
              fill="#f2a65a" opacity="0.35" />
        <line x1="{cx:.1f}" y1="{cy:.1f}" x2="{arm_x:.1f}" y2="{arm_y:.1f}"
              stroke="#d85c3a" stroke-width="6" stroke-linecap="round" />
        <circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="#24495a" />
        <text x="{cx:.1f}" y="{cy - 32:.1f}" text-anchor="middle" font-size="22"
              font-family="Arial" fill="#24495a" font-weight="800">{angle}°</text>
    </svg>
    """


def interactive_clock_html() -> str:
    return """
    <style>
        body {
            margin: 0;
            font-family: "Noto Sans TC", "Microsoft JhengHei", Arial, sans-serif;
            color: #233f4a;
            background: transparent;
        }
        .panel {
            border: 1px solid #d6e1e7;
            border-radius: 8px;
            background: #ffffff;
            padding: 14px;
        }
        .toolbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 8px;
        }
        .readout {
            font-size: 32px;
            font-weight: 800;
            color: #24495a;
        }
        .hint {
            color: #607882;
            font-size: 14px;
            line-height: 1.45;
        }
        .drag-target {
            cursor: grab;
            touch-action: none;
        }
        .drag-target:active {
            cursor: grabbing;
        }
        svg {
            width: 100%;
            max-width: 390px;
            display: block;
            margin: 0 auto;
            user-select: none;
        }
        button {
            border: 1px solid #b9ccd5;
            border-radius: 8px;
            background: #f7fbfc;
            color: #233f4a;
            padding: 8px 10px;
            font-weight: 700;
            cursor: pointer;
        }
    </style>
    <div class="panel">
        <div class="toolbar">
            <div>
                <div class="readout" id="clockReadout">3:20</div>
                <div class="hint">拖拉紅色長針改分鐘，拖拉藍色短針改小時。</div>
            </div>
            <button id="resetClock" type="button">回到 3:20</button>
        </div>
        <svg id="clockSvg" viewBox="0 0 360 360" aria-label="可拖拉時鐘">
            <circle cx="180" cy="180" r="162" fill="#fffdf8" stroke="#2f5f72" stroke-width="8"></circle>
            <circle cx="180" cy="180" r="150" fill="#ffffff" stroke="#d5e3e8" stroke-width="2"></circle>
            <g id="clockTicks"></g>
            <g id="clockNumbers"></g>
            <line id="hourHand" class="drag-target" x1="180" y1="180" x2="180" y2="104" stroke="#24495a" stroke-width="12" stroke-linecap="round"></line>
            <line id="minuteHand" class="drag-target" x1="180" y1="180" x2="180" y2="66" stroke="#d85c3a" stroke-width="7" stroke-linecap="round"></line>
            <circle cx="180" cy="180" r="10" fill="#24495a"></circle>
            <circle id="hourHandle" class="drag-target" cx="180" cy="104" r="14" fill="#24495a" opacity="0.92"></circle>
            <circle id="minuteHandle" class="drag-target" cx="180" cy="66" r="12" fill="#d85c3a" opacity="0.94"></circle>
        </svg>
    </div>
    <script>
        const svg = document.getElementById("clockSvg");
        const cx = 180;
        const cy = 180;
        let hour = 3;
        let minute = 20;
        let dragging = null;

        function point(angle, length) {
            const rad = (angle - 90) * Math.PI / 180;
            return {
                x: cx + Math.cos(rad) * length,
                y: cy + Math.sin(rad) * length
            };
        }

        function angleFromEvent(event) {
            const pt = svg.createSVGPoint();
            pt.x = event.clientX;
            pt.y = event.clientY;
            const local = pt.matrixTransform(svg.getScreenCTM().inverse());
            let deg = Math.atan2(local.y - cy, local.x - cx) * 180 / Math.PI + 90;
            if (deg < 0) deg += 360;
            return deg;
        }

        function displayHour() {
            return hour === 0 ? 12 : hour;
        }

        function updateClock() {
            const hourAngle = (hour + minute / 60) * 30;
            const minuteAngle = minute * 6;
            const hp = point(hourAngle, 78);
            const mp = point(minuteAngle, 118);
            document.getElementById("hourHand").setAttribute("x2", hp.x);
            document.getElementById("hourHand").setAttribute("y2", hp.y);
            document.getElementById("minuteHand").setAttribute("x2", mp.x);
            document.getElementById("minuteHand").setAttribute("y2", mp.y);
            document.getElementById("hourHandle").setAttribute("cx", hp.x);
            document.getElementById("hourHandle").setAttribute("cy", hp.y);
            document.getElementById("minuteHandle").setAttribute("cx", mp.x);
            document.getElementById("minuteHandle").setAttribute("cy", mp.y);
            document.getElementById("clockReadout").textContent =
                `${displayHour()}:${String(minute).padStart(2, "0")}`;
        }

        function makeClockFace() {
            const ticks = document.getElementById("clockTicks");
            const numbers = document.getElementById("clockNumbers");
            for (let value = 0; value < 60; value += 1) {
                const angle = value * 6;
                const outer = point(angle, 138);
                const inner = point(angle, value % 5 === 0 ? 120 : 130);
                const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                line.setAttribute("x1", inner.x);
                line.setAttribute("y1", inner.y);
                line.setAttribute("x2", outer.x);
                line.setAttribute("y2", outer.y);
                line.setAttribute("stroke", value % 5 === 0 ? "#263238" : "#94a8b1");
                line.setAttribute("stroke-width", value % 5 === 0 ? "3" : "1");
                line.setAttribute("stroke-linecap", "round");
                ticks.appendChild(line);
            }
            for (let number = 1; number <= 12; number += 1) {
                const p = point(number * 30, 102);
                const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
                text.setAttribute("x", p.x);
                text.setAttribute("y", p.y + 7);
                text.setAttribute("text-anchor", "middle");
                text.setAttribute("font-size", "20");
                text.setAttribute("font-family", "Arial");
                text.setAttribute("font-weight", "800");
                text.setAttribute("fill", "#263238");
                text.textContent = number;
                numbers.appendChild(text);
            }
        }

        function startDrag(kind, event) {
            dragging = kind;
            svg.setPointerCapture(event.pointerId);
            event.preventDefault();
        }

        document.getElementById("minuteHand").addEventListener("pointerdown", (event) => startDrag("minute", event));
        document.getElementById("minuteHandle").addEventListener("pointerdown", (event) => startDrag("minute", event));
        document.getElementById("hourHand").addEventListener("pointerdown", (event) => startDrag("hour", event));
        document.getElementById("hourHandle").addEventListener("pointerdown", (event) => startDrag("hour", event));
        svg.addEventListener("pointermove", (event) => {
            if (!dragging) return;
            const angle = angleFromEvent(event);
            if (dragging === "minute") {
                minute = Math.round(angle / 6) % 60;
            } else {
                hour = Math.round(angle / 30) % 12;
            }
            updateClock();
            event.preventDefault();
        });
        svg.addEventListener("pointerup", () => dragging = null);
        svg.addEventListener("pointercancel", () => dragging = null);
        document.getElementById("resetClock").addEventListener("click", () => {
            hour = 3;
            minute = 20;
            updateClock();
        });

        makeClockFace();
        updateClock();
    </script>
    """


def interactive_protractor_html() -> str:
    return """
    <style>
        body {
            margin: 0;
            font-family: "Noto Sans TC", "Microsoft JhengHei", Arial, sans-serif;
            color: #233f4a;
            background: transparent;
        }
        .panel {
            border: 1px solid #d6e1e7;
            border-radius: 8px;
            background: #ffffff;
            padding: 14px;
        }
        .toolbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 8px;
        }
        .readout {
            font-size: 32px;
            font-weight: 800;
            color: #24495a;
        }
        .hint {
            color: #607882;
            font-size: 14px;
            line-height: 1.45;
        }
        .drag-target {
            cursor: grab;
            touch-action: none;
        }
        .drag-target:active {
            cursor: grabbing;
        }
        svg {
            width: 100%;
            max-width: 430px;
            display: block;
            margin: 0 auto;
            user-select: none;
        }
        button {
            border: 1px solid #b9ccd5;
            border-radius: 8px;
            background: #f7fbfc;
            color: #233f4a;
            padding: 8px 10px;
            font-weight: 700;
            cursor: pointer;
        }
    </style>
    <div class="panel">
        <div class="toolbar">
            <div>
                <div class="readout"><span id="angleReadout">65</span>°，<span id="angleType">銳角</span></div>
                <div class="hint">拖拉紅色圓點或紅色邊，角度會即時改變。</div>
            </div>
            <button id="resetAngle" type="button">回到 65°</button>
        </div>
        <svg id="angleSvg" viewBox="0 0 420 270" aria-label="可拖拉量角器">
            <path d="M 45 225 A 165 165 0 0 1 375 225" fill="#f7fbfc" stroke="#2f5f72" stroke-width="6"></path>
            <path d="M 65 225 A 145 145 0 0 1 355 225" fill="none" stroke="#d7e4ea" stroke-width="2"></path>
            <g id="angleTicks"></g>
            <line x1="35" y1="225" x2="385" y2="225" stroke="#273f49" stroke-width="5" stroke-linecap="round"></line>
            <path id="angleWedge" fill="#f2a65a" opacity="0.35"></path>
            <line id="angleArm" class="drag-target" x1="210" y1="225" x2="280" y2="75" stroke="#d85c3a" stroke-width="8" stroke-linecap="round"></line>
            <circle cx="210" cy="225" r="9" fill="#24495a"></circle>
            <circle id="angleHandle" class="drag-target" cx="280" cy="75" r="13" fill="#d85c3a"></circle>
        </svg>
    </div>
    <script>
        const svg = document.getElementById("angleSvg");
        const cx = 210;
        const cy = 225;
        const radius = 165;
        const armLength = 154;
        const arcRadius = 70;
        let degrees = 65;
        let dragging = false;

        function point(angle, length) {
            const rad = angle * Math.PI / 180;
            return {
                x: cx + Math.cos(rad) * length,
                y: cy - Math.sin(rad) * length
            };
        }

        function angleFromEvent(event) {
            const pt = svg.createSVGPoint();
            pt.x = event.clientX;
            pt.y = event.clientY;
            const local = pt.matrixTransform(svg.getScreenCTM().inverse());
            let angle = Math.atan2(cy - local.y, local.x - cx) * 180 / Math.PI;
            return Math.max(0, Math.min(180, Math.round(angle)));
        }

        function angleType(angle) {
            if (angle < 90) return "銳角";
            if (angle === 90) return "直角";
            if (angle < 180) return "鈍角";
            return "平角";
        }

        function updateAngle() {
            const arm = point(degrees, armLength);
            const arc = point(degrees, arcRadius);
            const largeArc = degrees > 180 ? 1 : 0;
            document.getElementById("angleArm").setAttribute("x2", arm.x);
            document.getElementById("angleArm").setAttribute("y2", arm.y);
            document.getElementById("angleHandle").setAttribute("cx", arm.x);
            document.getElementById("angleHandle").setAttribute("cy", arm.y);
            document.getElementById("angleWedge").setAttribute(
                "d",
                `M ${cx} ${cy} L ${cx + arcRadius} ${cy} A ${arcRadius} ${arcRadius} 0 ${largeArc} 0 ${arc.x} ${arc.y} Z`
            );
            document.getElementById("angleReadout").textContent = degrees;
            document.getElementById("angleType").textContent = angleType(degrees);
        }

        function makeProtractor() {
            const ticks = document.getElementById("angleTicks");
            for (let value = 0; value <= 180; value += 5) {
                const outer = point(value, radius);
                const inner = point(value, value % 10 === 0 ? radius - 20 : radius - 10);
                const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                line.setAttribute("x1", inner.x);
                line.setAttribute("y1", inner.y);
                line.setAttribute("x2", outer.x);
                line.setAttribute("y2", outer.y);
                line.setAttribute("stroke", value % 10 === 0 ? "#294a56" : "#8aa0a8");
                line.setAttribute("stroke-width", value % 10 === 0 ? "2" : "1");
                line.setAttribute("stroke-linecap", "round");
                ticks.appendChild(line);

                if (value % 30 === 0) {
                    const labelPoint = point(value, radius - 45);
                    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
                    text.setAttribute("x", labelPoint.x);
                    text.setAttribute("y", labelPoint.y + 5);
                    text.setAttribute("text-anchor", "middle");
                    text.setAttribute("font-size", "14");
                    text.setAttribute("font-family", "Arial");
                    text.setAttribute("font-weight", "800");
                    text.setAttribute("fill", "#294a56");
                    text.textContent = value;
                    ticks.appendChild(text);
                }
            }
        }

        function startDrag(event) {
            dragging = true;
            svg.setPointerCapture(event.pointerId);
            event.preventDefault();
        }

        document.getElementById("angleArm").addEventListener("pointerdown", startDrag);
        document.getElementById("angleHandle").addEventListener("pointerdown", startDrag);
        svg.addEventListener("pointermove", (event) => {
            if (!dragging) return;
            degrees = angleFromEvent(event);
            updateAngle();
            event.preventDefault();
        });
        svg.addEventListener("pointerup", () => dragging = false);
        svg.addEventListener("pointercancel", () => dragging = false);
        document.getElementById("resetAngle").addEventListener("click", () => {
            degrees = 65;
            updateAngle();
        });

        makeProtractor();
        updateAngle();
    </script>
    """


def make_quiz() -> dict[str, int]:
    start_hour = random.randint(7, 15)
    start_minute = random.choice(list(range(0, 60, 5)))
    elapsed = random.choice([15, 20, 30, 35, 45, 50, 60, 75, 90, 105, 120])
    end_hour, end_minute = add_minutes(start_hour, start_minute, elapsed)
    return {
        "clock_hour": random.randint(1, 12),
        "clock_minute": random.choice(list(range(0, 60, 5))),
        "start_hour": start_hour,
        "start_minute": start_minute,
        "elapsed": elapsed,
        "end_hour": end_hour,
        "end_minute": end_minute,
        "angle": random.choice([25, 45, 60, 90, 110, 135, 150, 180]),
    }


if "quiz" not in st.session_state:
    st.session_state["quiz"] = make_quiz()
    st.session_state["checked"] = False


st.markdown(
    """
    <div class="hero">
        <h1>國小時間與角度教學</h1>
        <p>用可以拖拉的時鐘、量角器和小測驗練習「讀時間、算經過時間、認識角度」。</p>
        <span class="chip">1 小時 = 60 分鐘</span>
        <span class="chip">1 分鐘 = 60 秒</span>
        <span class="chip">直角 = 90°</span>
        <span class="chip">平角 = 180°</span>
    </div>
    """,
    unsafe_allow_html=True,
)

time_tab, angle_tab, quiz_tab = st.tabs(["時間教室", "角度教室", "小測驗"])

with time_tab:
    st.subheader("拖拉時鐘")
    clock_col, lesson_col = st.columns([1.08, 1])
    with clock_col:
        st.iframe(interactive_clock_html(), height=500)

    with lesson_col:
        with st.container(border=True):
            st.markdown("#### 指針怎麼看")
            st.write("直接拖拉紅色長針，可以改變分鐘。")
            st.write("直接拖拉藍色短針，可以改變小時。")
            st.markdown(
                """
                <div class="formula">
                    長針走一小格是 <strong>1 分鐘</strong>。<br>
                    長針走一大格是 <strong>5 分鐘</strong>。<br>
                    短針走一大格是 <strong>1 小時</strong>。
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.info("拖一拖，再請學生說出現在是幾點幾分。")

    st.subheader("經過時間")
    start_col, result_col = st.columns([1.05, 1])
    with start_col:
        with st.container(border=True):
            start_hour = st.number_input("開始：時", 0, 23, 8, 1)
            start_minute = st.selectbox("開始：分", list(range(0, 60, 5)), index=6)
            elapsed = st.slider("經過幾分鐘", 5, 180, 45, 5)
            end_hour, end_minute = add_minutes(start_hour, start_minute, elapsed)

    with result_col:
        with st.container(border=True):
            st.metric("結束時間", time_label(end_hour, end_minute))
            st.write(f"從 {time_label(start_hour, start_minute)} 開始，經過 {elapsed} 分鐘。")
            st.markdown(
                f"""
                <div class="formula">
                    {start_hour:02d}:{start_minute:02d}
                    ＋ {elapsed} 分鐘
                    ＝ <strong>{end_hour:02d}:{end_minute:02d}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )

with angle_tab:
    st.subheader("拖拉量角器")
    angle_col, lesson_col = st.columns([1.1, 1])
    with angle_col:
        st.iframe(interactive_protractor_html(), height=420)

    with lesson_col:
        with st.container(border=True):
            st.markdown("#### 角度怎麼看")
            st.write("直接拖拉紅色邊或紅色圓點，角度會即時改變。")
            st.markdown(
                """
                <div class="formula">
                    <span class="chip">小於 90°：銳角</span>
                    <span class="chip">等於 90°：直角</span>
                    <span class="chip">90° 到 180°：鈍角</span>
                    <span class="chip">等於 180°：平角</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.info("拖到 90° 時是直角；拖到 180° 時是平角。")

    st.subheader("角度加減")
    add_col, result_col = st.columns([1.05, 1])
    with add_col:
        with st.container(border=True):
            first = st.slider("第一個角", 0, 180, 40, 5)
            second = st.slider("第二個角", 0, 180, 50, 5)
            total = first + second

    with result_col:
        with st.container(border=True):
            st.metric("合起來", f"{total}°")
            if total < 90:
                st.info("合起來還是銳角。")
            elif total == 90:
                st.success("合起來剛好是直角。")
            elif total < 180:
                st.info("合起來是鈍角。")
            elif total == 180:
                st.success("合起來剛好是平角。")
            else:
                st.warning("超過平角，可以先拆成 180° 再多一些來想。")
            st.markdown(
                f'<div class="formula">{first}° ＋ {second}° ＝ <strong>{total}°</strong></div>',
                unsafe_allow_html=True,
            )

with quiz_tab:
    quiz = st.session_state["quiz"]
    action_col, hint_col = st.columns([1, 3])
    with action_col:
        if st.button("換一組題目"):
            st.session_state["quiz"] = make_quiz()
            st.session_state["checked"] = False
            st.rerun()
    with hint_col:
        st.caption("完成三題後按下檢查答案。")

    q1_col, q2_col, q3_col = st.columns(3)
    with q1_col:
        with st.container(border=True):
            st.markdown("#### 1. 讀出鐘面時間")
            render_svg(clock_svg(quiz["clock_hour"], quiz["clock_minute"], 260), 235)
            answer_hour = st.selectbox("答案：時", list(range(1, 13)), key="quiz_hour")
            answer_minute = st.selectbox("答案：分", list(range(0, 60, 5)), key="quiz_minute")

    with q2_col:
        with st.container(border=True):
            st.markdown("#### 2. 算出結束時間")
            st.write(
                f"{time_label(quiz['start_hour'], quiz['start_minute'])} 開始，"
                f"經過 {quiz['elapsed']} 分鐘。"
            )
            answer_end_hour = st.number_input("答案：時", 0, 23, quiz["start_hour"], key="end_hour")
            answer_end_minute = st.selectbox("答案：分", list(range(0, 60, 5)), key="end_minute")

    with q3_col:
        with st.container(border=True):
            st.markdown("#### 3. 判斷角的種類")
            render_svg(protractor_svg(quiz["angle"], 300), 220)
            answer_angle = st.radio("答案", ["銳角", "直角", "鈍角", "平角"], horizontal=True)

    if st.button("檢查答案", type="primary"):
        st.session_state["checked"] = True

    if st.session_state["checked"]:
        correct_clock = answer_hour == quiz["clock_hour"] and answer_minute == quiz["clock_minute"]
        correct_elapsed = answer_end_hour == quiz["end_hour"] and answer_end_minute == quiz["end_minute"]
        correct_angle = answer_angle == angle_name(quiz["angle"])
        score = sum([correct_clock, correct_elapsed, correct_angle])

        st.subheader(f"得分：{score} / 3")
        if correct_clock:
            st.markdown('<div class="good">第 1 題正確。</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="warm">第 1 題答案是 {twelve_hour_label(quiz["clock_hour"], quiz["clock_minute"])}。</div>',
                unsafe_allow_html=True,
            )

        if correct_elapsed:
            st.markdown('<div class="good">第 2 題正確。</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="warm">第 2 題答案是 {time_label(quiz["end_hour"], quiz["end_minute"])}。</div>',
                unsafe_allow_html=True,
            )

        if correct_angle:
            st.markdown('<div class="good">第 3 題正確。</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="warm">第 3 題答案是 {angle_name(quiz["angle"])}。</div>',
                unsafe_allow_html=True,
            )
