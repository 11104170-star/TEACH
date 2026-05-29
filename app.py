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

    def hand_points(angle: float, length: float, base_width: float) -> str:
        tip_x, tip_y = point(angle, length)
        back_x, back_y = point(angle + 180, base_width * 0.85)
        left_x, left_y = point(angle - 90, base_width)
        right_x, right_y = point(angle + 90, base_width)
        return (
            f"{tip_x:.1f},{tip_y:.1f} "
            f"{left_x:.1f},{left_y:.1f} "
            f"{back_x:.1f},{back_y:.1f} "
            f"{right_x:.1f},{right_y:.1f}"
        )

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

    hour_hand = hand_points(hour_angle, radius * 0.5, 9)
    minute_hand = hand_points(minute_angle, radius * 0.76, 6)

    return f"""
    <svg viewBox="0 0 {size} {size}" width="100%" height="100%" role="img" aria-label="時鐘">
        <circle cx="{center}" cy="{center}" r="{radius + 14}" fill="#fffdf8" stroke="#2f5f72" stroke-width="7" />
        <circle cx="{center}" cy="{center}" r="{radius + 4}" fill="#ffffff" stroke="#d5e3e8" stroke-width="2" />
        {''.join(ticks)}
        {''.join(numbers)}
        <polygon points="{hour_hand}" fill="#24495a" />
        <polygon points="{minute_hand}" fill="#d85c3a" />
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
    rad = math.radians(180 - angle)
    arm_x = cx + math.cos(rad) * radius
    arm_y = cy - math.sin(rad) * radius
    arc_x = cx + math.cos(rad) * (radius * 0.38)
    arc_y = cy - math.sin(rad) * (radius * 0.38)

    ticks = []
    labels = []
    for value in range(0, 181, 5):
        tick_rad = math.radians(180 - value)
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
        <path d="M {cx:.1f} {cy:.1f} L {cx - radius * 0.38:.1f} {cy:.1f}
                 A {radius * 0.38:.1f} {radius * 0.38:.1f} 0 0 1 {arc_x:.1f} {arc_y:.1f} Z"
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
        .period-status {
            font-size: 22px;
            font-weight: 800;
            color: #24495a;
        }
        .hint {
            color: #607882;
            font-size: 14px;
            line-height: 1.45;
        }
        .button-row {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            justify-content: flex-end;
        }
        .drag-target {
            cursor: grab;
            touch-action: none;
        }
        .drag-target:active {
            cursor: grabbing;
        }
        .clock-hand {
            filter: drop-shadow(0 1px 1px rgba(35, 63, 74, 0.22));
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
                <div class="period-status" id="periodStatus" aria-live="polite">時段：AM 上午</div>
                <div class="hint">拖拉紅色長針改分鐘；分針跨過 12 時，短針會自動進位或退位。</div>
            </div>
            <div class="button-row">
                <button id="togglePeriod" type="button">切換 AM/PM</button>
                <button id="randomClock" type="button">隨機時間</button>
                <button id="resetClock" type="button">回到 3:20 AM</button>
            </div>
        </div>
        <svg id="clockSvg" viewBox="0 0 360 360" aria-label="可拖拉時鐘">
            <circle cx="180" cy="180" r="162" fill="#fffdf8" stroke="#2f5f72" stroke-width="8"></circle>
            <circle cx="180" cy="180" r="150" fill="#ffffff" stroke="#d5e3e8" stroke-width="2"></circle>
            <g id="clockTicks"></g>
            <g id="clockNumbers"></g>
            <polygon id="hourHand" class="drag-target clock-hand" points="" fill="#24495a"></polygon>
            <polygon id="minuteHand" class="drag-target clock-hand" points="" fill="#d85c3a"></polygon>
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
        let period = "AM";
        let dragging = null;
        let lastMinute = minute;

        function point(angle, length) {
            const rad = (angle - 90) * Math.PI / 180;
            return {
                x: cx + Math.cos(rad) * length,
                y: cy + Math.sin(rad) * length
            };
        }

        function handPoints(angle, length, baseWidth) {
            const tip = point(angle, length);
            const back = point(angle + 180, baseWidth * 0.85);
            const left = point(angle - 90, baseWidth);
            const right = point(angle + 90, baseWidth);
            return `${tip.x},${tip.y} ${left.x},${left.y} ${back.x},${back.y} ${right.x},${right.y}`;
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

        function periodText() {
            return period === "AM" ? "上午" : "下午";
        }

        function updateClock() {
            const hourAngle = (hour + minute / 60) * 30;
            const minuteAngle = minute * 6;
            const hp = point(hourAngle, 78);
            const mp = point(minuteAngle, 118);
            document.getElementById("hourHand").setAttribute("points", handPoints(hourAngle, 82, 12));
            document.getElementById("minuteHand").setAttribute("points", handPoints(minuteAngle, 122, 7));
            document.getElementById("hourHandle").setAttribute("cx", hp.x);
            document.getElementById("hourHandle").setAttribute("cy", hp.y);
            document.getElementById("minuteHandle").setAttribute("cx", mp.x);
            document.getElementById("minuteHandle").setAttribute("cy", mp.y);
            document.getElementById("periodStatus").textContent =
                `時段：${period} ${periodText()}`;
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
            if (kind === "minute") {
                lastMinute = minute;
            }
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
                const nextMinute = Math.round(angle / 6) % 60;
                const diff = nextMinute - lastMinute;
                if (diff < -30) {
                    hour = (hour + 1) % 12;
                } else if (diff > 30) {
                    hour = (hour + 11) % 12;
                }
                minute = nextMinute;
                lastMinute = nextMinute;
            } else {
                hour = Math.round(angle / 30) % 12;
            }
            updateClock();
            event.preventDefault();
        });
        svg.addEventListener("pointerup", () => {
            dragging = null;
            lastMinute = minute;
        });
        svg.addEventListener("pointercancel", () => {
            dragging = null;
            lastMinute = minute;
        });
        document.getElementById("togglePeriod").addEventListener("click", () => {
            period = period === "AM" ? "PM" : "AM";
            updateClock();
        });
        document.getElementById("randomClock").addEventListener("click", () => {
            hour = Math.floor(Math.random() * 12);
            minute = Math.floor(Math.random() * 12) * 5;
            period = Math.random() < 0.5 ? "AM" : "PM";
            lastMinute = minute;
            updateClock();
        });
        document.getElementById("resetClock").addEventListener("click", () => {
            hour = 3;
            minute = 20;
            period = "AM";
            lastMinute = minute;
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
                <div class="hint">0° 在左邊。拖拉紅色圓點或紅色邊，角度會即時改變。</div>
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
            const rad = (180 - angle) * Math.PI / 180;
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
            angle = 180 - angle;
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
                `M ${cx} ${cy} L ${cx - arcRadius} ${cy} A ${arcRadius} ${arcRadius} 0 ${largeArc} 1 ${arc.x} ${arc.y} Z`
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


def interactive_full_circle_html() -> str:
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
        .preset-buttons {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            justify-content: flex-end;
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
                <div class="readout"><span id="fullReadout">120</span>°，<span id="fullType">鈍角</span></div>
                <div class="hint">0° 在左邊，順著上方、右邊、下方拖一圈就是 360°。</div>
            </div>
            <div class="preset-buttons">
                <button data-angle="0" type="button">0°</button>
                <button data-angle="90" type="button">90°</button>
                <button data-angle="180" type="button">180°</button>
                <button data-angle="270" type="button">270°</button>
                <button data-angle="360" type="button">360°</button>
            </div>
        </div>
        <svg id="fullSvg" viewBox="0 0 420 420" aria-label="可拖拉 360 度角">
            <circle cx="210" cy="210" r="166" fill="#f7fbfc" stroke="#2f5f72" stroke-width="6"></circle>
            <circle cx="210" cy="210" r="138" fill="#ffffff" stroke="#d7e4ea" stroke-width="2"></circle>
            <g id="fullTicks"></g>
            <path id="fullWedge" fill="#f2a65a" opacity="0.35"></path>
            <line x1="210" y1="210" x2="44" y2="210" stroke="#24495a" stroke-width="5" stroke-linecap="round"></line>
            <line id="fullArm" class="drag-target" x1="210" y1="210" x2="127" y2="66" stroke="#d85c3a" stroke-width="8" stroke-linecap="round"></line>
            <circle cx="210" cy="210" r="9" fill="#24495a"></circle>
            <circle id="fullHandle" class="drag-target" cx="127" cy="66" r="13" fill="#d85c3a"></circle>
        </svg>
    </div>
    <script>
        const svg = document.getElementById("fullSvg");
        const cx = 210;
        const cy = 210;
        const radius = 166;
        const armLength = 150;
        const wedgeRadius = 100;
        let degrees = 120;
        let dragging = false;

        function point(angle, length) {
            const rad = (180 - angle) * Math.PI / 180;
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
            let raw = Math.atan2(cy - local.y, local.x - cx) * 180 / Math.PI;
            if (raw < 0) raw += 360;
            return Math.round((180 - raw + 360) % 360);
        }

        function angleType(angle) {
            if (angle === 0) return "零角";
            if (angle < 90) return "銳角";
            if (angle === 90) return "直角";
            if (angle < 180) return "鈍角";
            if (angle === 180) return "平角";
            if (angle < 360) return "優角";
            return "周角";
        }

        function wedgePath(angle) {
            const startX = cx - wedgeRadius;
            const startY = cy;
            if (angle >= 360) {
                return `M ${cx} ${cy} m ${-wedgeRadius} 0 ` +
                    `a ${wedgeRadius} ${wedgeRadius} 0 1 1 ${wedgeRadius * 2} 0 ` +
                    `a ${wedgeRadius} ${wedgeRadius} 0 1 1 ${-wedgeRadius * 2} 0`;
            }
            if (angle <= 0) {
                return `M ${cx} ${cy} L ${startX} ${startY} Z`;
            }
            const end = point(angle, wedgeRadius);
            const largeArc = angle > 180 ? 1 : 0;
            return `M ${cx} ${cy} L ${startX} ${startY} A ${wedgeRadius} ${wedgeRadius} 0 ${largeArc} 1 ${end.x} ${end.y} Z`;
        }

        function updateFullCircle() {
            const visibleAngle = degrees >= 360 ? 360 : degrees;
            const arm = point(visibleAngle, armLength);
            document.getElementById("fullArm").setAttribute("x2", arm.x);
            document.getElementById("fullArm").setAttribute("y2", arm.y);
            document.getElementById("fullHandle").setAttribute("cx", arm.x);
            document.getElementById("fullHandle").setAttribute("cy", arm.y);
            document.getElementById("fullWedge").setAttribute("d", wedgePath(visibleAngle));
            document.getElementById("fullReadout").textContent = visibleAngle;
            document.getElementById("fullType").textContent = angleType(visibleAngle);
        }

        function makeCircleFace() {
            const ticks = document.getElementById("fullTicks");
            for (let value = 0; value < 360; value += 5) {
                const outer = point(value, radius);
                const inner = point(value, value % 30 === 0 ? radius - 22 : radius - 11);
                const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                line.setAttribute("x1", inner.x);
                line.setAttribute("y1", inner.y);
                line.setAttribute("x2", outer.x);
                line.setAttribute("y2", outer.y);
                line.setAttribute("stroke", value % 30 === 0 ? "#294a56" : "#8aa0a8");
                line.setAttribute("stroke-width", value % 30 === 0 ? "2" : "1");
                line.setAttribute("stroke-linecap", "round");
                ticks.appendChild(line);
            }

            const labels = [
                [0, "0/360"],
                [90, "90"],
                [180, "180"],
                [270, "270"]
            ];
            for (const [angle, label] of labels) {
                const labelPoint = point(angle, radius - 48);
                const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
                text.setAttribute("x", labelPoint.x);
                text.setAttribute("y", labelPoint.y + 5);
                text.setAttribute("text-anchor", "middle");
                text.setAttribute("font-size", "15");
                text.setAttribute("font-family", "Arial");
                text.setAttribute("font-weight", "800");
                text.setAttribute("fill", "#294a56");
                text.textContent = label;
                ticks.appendChild(text);
            }
        }

        function startDrag(event) {
            dragging = true;
            svg.setPointerCapture(event.pointerId);
            event.preventDefault();
        }

        document.getElementById("fullArm").addEventListener("pointerdown", startDrag);
        document.getElementById("fullHandle").addEventListener("pointerdown", startDrag);
        svg.addEventListener("pointermove", (event) => {
            if (!dragging) return;
            const next = angleFromEvent(event);
            if (degrees > 300 && next < 20) {
                degrees = 360;
            } else if (degrees < 60 && next > 340) {
                degrees = 0;
            } else {
                degrees = next;
            }
            updateFullCircle();
            event.preventDefault();
        });
        svg.addEventListener("pointerup", () => dragging = false);
        svg.addEventListener("pointercancel", () => dragging = false);

        for (const button of document.querySelectorAll("[data-angle]")) {
            button.addEventListener("click", () => {
                degrees = Number(button.dataset.angle);
                updateFullCircle();
            });
        }

        makeCircleFace();
        updateFullCircle();
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
            st.write("按「隨機時間」可以抽一個時間，讓學生練習看指針讀出時間與 AM/PM。")
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

    st.subheader("AM / PM 教學")
    ampm_col, example_col = st.columns([1, 1])
    with ampm_col:
        with st.container(border=True):
            st.markdown("#### AM 是上午")
            st.write("AM 從午夜 12:00 到中午 11:59。")
            st.markdown(
                """
                <div class="formula">
                    <span class="chip">12:00 AM = 00:00</span>
                    <span class="chip">7:30 AM = 07:30</span>
                    <span class="chip">11:59 AM = 11:59</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with example_col:
        with st.container(border=True):
            st.markdown("#### PM 是下午和晚上")
            st.write("PM 從中午 12:00 到晚上 11:59。")
            st.markdown(
                """
                <div class="formula">
                    <span class="chip">12:00 PM = 12:00</span>
                    <span class="chip">3:20 PM = 15:20</span>
                    <span class="chip">11:45 PM = 23:45</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

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
            st.write("這個半圓量角器的 0° 在左邊，往上方拖會慢慢變大。")
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

    st.subheader("360° 圓形角度")
    full_col, full_lesson_col = st.columns([1.1, 1])
    with full_col:
        st.iframe(interactive_full_circle_html(), height=540)

    with full_lesson_col:
        with st.container(border=True):
            st.markdown("#### 超過 180° 的角")
            st.write("這個圓形角度教具可以從 0° 拖到 360°。")
            st.markdown(
                """
                <div class="formula">
                    <span class="chip">180°：平角</span>
                    <span class="chip">大於 180°：優角</span>
                    <span class="chip">360°：周角</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.info("如果拖到 360°，代表剛好轉完整一圈。")

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
