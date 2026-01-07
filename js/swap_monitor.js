import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
    name: "Comfy.SwapMonitor",
    async setup() {
        // ID elementu pro snadnou manipulaci
        const ELEMENT_ID = "comfy-swap-monitor";
        
        // --- 1. Vytvoření HTML struktury ---
        const container = document.createElement("div");
        container.id = ELEMENT_ID;
        
        // Základní styl kontejneru
        Object.assign(container.style, {
            position: "fixed",
            bottom: "10px",
            right: "10px",
            width: "300px",
            height: "auto", // Výška se přizpůsobí obsahu
            backgroundColor: "rgba(0, 0, 0, 0.9)",
            border: "1px solid #444",
            borderRadius: "8px",
            zIndex: "9000",
            fontFamily: "monospace",
            color: "white",
            display: "flex",
            flexDirection: "column",
            overflow: "hidden",
            boxShadow: "0 4px 6px rgba(0,0,0,0.3)"
        });

        // HTML vnitřek: Header (pro drag) + Content (graf)
        container.innerHTML = `
            <div id="sm-header" style="
                background: #333; 
                padding: 5px 10px; 
                cursor: grab; 
                font-size: 12px; 
                font-weight: bold; 
                display: flex; 
                justify-content: space-between; 
                align-items: center;
                user-select: none;
            ">
                <span>💩 Swap Monitor</span>
                <div style="display: flex; gap: 8px;">
                    <span id="sm-btn-min" style="cursor: pointer; font-weight: bold;" title="Minimize">_</span>
                    <span id="sm-btn-close" style="cursor: pointer; font-weight: bold; color: #ff5555;" title="Close">×</span>
                </div>
            </div>
            <div id="sm-content" style="padding: 10px; display: flex; flex-direction: column; gap: 5px;">
                <div style="display: flex; justify-content: space-between; font-size: 10px;">
                    <span id="sm-swap-text">Swap: 0%</span>
                    <span id="sm-disk-text">Write: 0 MB/s</span>
                </div>
                <canvas id="sm-graph" width="280" height="100" style="width: 100%; height: 100%; margin-top: 5px; border: 1px solid #222; background: #111;"></canvas>
            </div>
        `;

        document.body.appendChild(container);

        // --- 2. Logika prvků ---
        const header = container.querySelector("#sm-header");
        const content = container.querySelector("#sm-content");
        const btnMin = container.querySelector("#sm-btn-min");
        const btnClose = container.querySelector("#sm-btn-close");
        const canvas = container.querySelector("#sm-graph");
        const ctx = canvas.getContext("2d");
        const swapText = container.querySelector("#sm-swap-text");
        const diskText = container.querySelector("#sm-disk-text");

        let isMinimized = false;

        // --- 3. Funkce: Minimalizace ---
        btnMin.onclick = () => {
            isMinimized = !isMinimized;
            if (isMinimized) {
                content.style.display = "none";
                btnMin.textContent = "□"; // Symbol pro obnovení
            } else {
                content.style.display = "flex";
                btnMin.textContent = "_";
            }
        };

        // --- 4. Funkce: Zavření (Skrytí) ---
        btnClose.onclick = () => {
            container.style.display = "none";
        };

        // --- 5. Funkce: Drag & Drop (Přesouvání) ---
        let isDragging = false;
        let dragOffsetX = 0;
        let dragOffsetY = 0;

        header.onmousedown = (e) => {
            isDragging = true;
            header.style.cursor = "grabbing";
            
            // Spočítáme posun myši oproti rohu okna
            const rect = container.getBoundingClientRect();
            dragOffsetX = e.clientX - rect.left;
            dragOffsetY = e.clientY - rect.top;
        };

        window.addEventListener("mousemove", (e) => {
            if (!isDragging) return;

            // Zrušíme bottom/right, abychom mohli volně hýbat pomocí top/left
            container.style.bottom = "auto";
            container.style.right = "auto";

            const newLeft = e.clientX - dragOffsetX;
            const newTop = e.clientY - dragOffsetY;

            container.style.left = `${newLeft}px`;
            container.style.top = `${newTop}px`;
        });

        window.addEventListener("mouseup", () => {
            if (isDragging) {
                isDragging = false;
                header.style.cursor = "grab";
            }
        });

        // --- 6. Registrace menu pro opětovné zobrazení ---
        // Přidáme možnost do kontextového menu ComfyUI (pravé tlačítko na plátno)
        const originalGetCanvasMenuOptions = app.canvas.getCanvasMenuOptions;
        app.canvas.getCanvasMenuOptions = function () {
            const options = originalGetCanvasMenuOptions.apply(this, arguments);
            options.push(null); // Separátor
            options.push({
                content: "Toggle Swap Monitor", // Název v menu
                callback: () => {
                    if (container.style.display === "none") {
                        container.style.display = "flex";
                        // Reset pozice pokud zmizel mimo obrazovku (volitelné)
                    } else {
                        container.style.display = "none";
                    }
                }
            });
            return options;
        };


        // --- 7. Vykreslování grafu (Stejné jako předtím) ---
        const maxDataPoints = 60;
        let historySwap = new Array(maxDataPoints).fill(0);
        let historyDisk = new Array(maxDataPoints).fill(0);

        function draw() {
            // Pokud je skryto nebo minimalizováno, nekreslíme (šetříme výkon)
            if (container.style.display === "none" || isMinimized) return;

            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            const w = canvas.width;
            const h = canvas.height;
            const step = w / (maxDataPoints - 1);

            // Mřížka
            ctx.strokeStyle = "#222";
            ctx.beginPath();
            ctx.moveTo(0, h/2); ctx.lineTo(w, h/2);
            ctx.stroke();

            // SWAP (Červená)
            ctx.beginPath();
            ctx.strokeStyle = "#ff4444";
            ctx.lineWidth = 2;
            for (let i = 0; i < maxDataPoints; i++) {
                const val = historySwap[i];
                const y = h - (val / 100) * h;
                if (i === 0) ctx.moveTo(0, y);
                else ctx.lineTo(i * step, y);
            }
            ctx.stroke();

            // DISK (Oranžová)
            ctx.beginPath();
            ctx.strokeStyle = "#ffaa00";
            ctx.lineWidth = 2;
            const maxDiskScale = 500; 
            for (let i = 0; i < maxDataPoints; i++) {
                const val = historyDisk[i];
                let normalized = val / maxDiskScale;
                if (normalized > 1) normalized = 1;
                const y = h - normalized * h;
                if (i === 0) ctx.moveTo(0, y);
                else ctx.lineTo(i * step, y);
            }
            ctx.stroke();
        }

        // Loop
        setInterval(async () => {
            try {
                const response = await api.fetchApi("/swap_monitor/stats");
                if (response.status !== 200) return;
                const data = await response.json();

                if (!isMinimized && container.style.display !== "none") {
                    swapText.innerText = `Swap: ${data.swap_percent}% (${data.swap_used_gb}/${data.swap_total_gb} GB)`;
                    diskText.innerText = `Write: ${data.disk_write_mb} MB/s`;
                }

                historySwap.shift(); historySwap.push(data.swap_percent);
                historyDisk.shift(); historyDisk.push(data.disk_write_mb);

                draw();
            } catch (e) { }
        }, 1000);
    }
});