import os
import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(
    page_title="Resins by R | Bespoke Handcrafted Resin",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Retrieve Discord Webhook from Streamlit Secrets or Environment
DISCORD_WEBHOOK_URL = st.secrets.get("DISCORD_WEBHOOK_URL", os.environ.get("DISCORD_WEBHOOK_URL", ""))

# 3. Streamlit Frame Layout Override
st.markdown("""
    <style>
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        div[data-testid="stToolbar"] {visibility: hidden !important;}
        div[data-testid="stDecoration"] {visibility: hidden !important;}
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100vw !important;
        }
        iframe {
            border: none !important;
            width: 100vw !important;
            height: 100vh !important;
            display: block;
        }
    </style>
""", unsafe_allow_html=True)

# 4. Master Frontend Template
HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resins by R</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Icons & Tailwind CSS -->
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <script src="https://cdn.tailwindcss.com"></script>

    <style>
        :root {{
            --bg-deep: #070709;
            --resin-gold: #e5b869;
            --resin-gold-bright: #ffd984;
            --resin-gold-glow: rgba(229, 184, 105, 0.45);
            --liquid-glass-border: rgba(255, 255, 255, 0.12);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-deep);
            color: #f3f4f6;
            font-family: 'Plus Jakarta Sans', sans-serif;
            overflow-x: hidden;
            opacity: 0;
            transition: opacity 1.2s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        body.site-ready {{
            opacity: 1;
        }}

        .font-luxury {{
            font-family: 'Cinzel', serif;
        }}

        /* ================= ELEVATED INTRO ANIMATION ================= */
        #intro-overlay {{
            position: fixed;
            inset: 0;
            background: radial-gradient(circle at center, #111218 0%, #000000 100%);
            z-index: 999999;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transition: opacity 1.2s cubic-bezier(0.77, 0, 0.175, 1);
            pointer-events: all;
        }}

        .etching-path {{
            stroke: #ffffff;
            stroke-width: 4.5;
            stroke-linecap: round;
            stroke-linejoin: round;
            fill: transparent;
            stroke-dasharray: 1000;
            stroke-dashoffset: 1000;
            animation: etchStroke 2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            filter: drop-shadow(0 0 12px rgba(255, 255, 255, 0.9));
        }}

        @keyframes etchStroke {{
            0% {{ stroke-dashoffset: 1000; }}
            100% {{ stroke-dashoffset: 0; }}
        }}

        .gold-fill-layer {{
            opacity: 0;
            animation: fillResin 1.4s cubic-bezier(0.16, 1, 0.3, 1) forwards 1.8s;
        }}

        @keyframes fillResin {{
            0% {{
                opacity: 0;
                transform: scale(0.96);
                filter: blur(8px);
            }}
            100% {{
                opacity: 1;
                transform: scale(1);
                filter: blur(0px) drop-shadow(0 0 35px rgba(229, 184, 105, 0.9)) drop-shadow(0 0 60px rgba(255, 217, 132, 0.6));
            }}
        }}

        .dust-canvas {{
            position: absolute;
            inset: 0;
            pointer-events: none;
        }}

        /* ================= ONE-TIME FADE-IN-UPWARDS ================= */
        .fade-in-up {{
            opacity: 0;
            transform: translateY(32px);
            transition: opacity 0.85s cubic-bezier(0.16, 1, 0.3, 1), transform 0.85s cubic-bezier(0.16, 1, 0.3, 1);
            will-change: opacity, transform;
        }}

        .fade-in-up.appeared {{
            opacity: 1 !important;
            transform: translateY(0) !important;
        }}

        /* Luxury Glassmorphism */
        .resin-card {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.015));
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid var(--liquid-glass-border);
            box-shadow: 0 20px 45px -15px rgba(0, 0, 0, 0.85);
            transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.4s ease, box-shadow 0.4s ease;
        }}

        .resin-card:hover {{
            transform: translateY(-8px);
            border-color: rgba(229, 184, 105, 0.5);
            box-shadow: 0 25px 50px -15px var(--resin-gold-glow);
        }}

        .btn-gold {{
            background: linear-gradient(135deg, #e5b869, #bf8f3b);
            color: #08090b;
            font-weight: 700;
            position: relative;
            overflow: hidden;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .btn-gold:hover {{
            box-shadow: 0 0 25px rgba(229, 184, 105, 0.6);
            transform: translateY(-2px);
        }}

        .btn-glass {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.15);
            transition: all 0.3s ease;
        }}

        .btn-glass:hover {{
            background: rgba(255, 255, 255, 0.1);
            border-color: var(--resin-gold);
            color: var(--resin-gold);
        }}

        /* Ambient floating fluid aura */
        .ambient-glow {{
            position: fixed;
            width: 550px;
            height: 550px;
            background: radial-gradient(circle, rgba(229, 184, 105, 0.07) 0%, transparent 70%);
            border-radius: 50%;
            filter: blur(100px);
            pointer-events: none;
            z-index: 0;
        }}
    </style>
</head>
<body class="relative min-h-screen">

    <!-- INTRO ANIMATION SCREEN -->
    <div id="intro-overlay">
        <canvas id="dust-canvas" class="dust-canvas"></canvas>
        <div class="relative flex flex-col items-center">
            <svg width="220" height="250" viewBox="0 0 200 230" fill="none" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="goldDustLiquid" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#ffffff" />
                        <stop offset="30%" stop-color="#fff6d1" />
                        <stop offset="65%" stop-color="#ffd984" />
                        <stop offset="100%" stop-color="#b68428" />
                    </linearGradient>
                    <filter id="liquidGlow" x="-20%" y="-20%" width="140%" height="140%">
                        <feGaussianBlur stdDeviation="4" result="blur" />
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                    </filter>
                </defs>

                <!-- 1. The White Outline (Traced Top to Bottom) -->
                <path class="etching-path" d="M 55 200 L 55 35 L 125 35 C 165 35 165 110 125 110 L 55 110 M 110 110 L 160 200" />

                <!-- 2. The Liquid White & Gold Dust Fill -->
                <path class="gold-fill-layer" filter="url(#liquidGlow)" fill="url(#goldDustLiquid)" 
                      d="M 55 200 L 55 35 L 125 35 C 165 35 165 110 125 110 L 55 110 M 110 110 L 160 200" 
                      stroke="url(#goldDustLiquid)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" />
            </svg>

            <span id="intro-caption" class="font-luxury text-xs tracking-[0.45em] uppercase text-amber-200 mt-6 opacity-0 transition-opacity duration-700">
                Resins By R • Bespoke
            </span>
        </div>
    </div>

    <!-- Ambient Lights -->
    <div class="ambient-glow top-0 left-[-100px]"></div>
    <div class="ambient-glow bottom-0 right-[-100px]"></div>

    <!-- MAIN PAGE CONTAINER -->
    <div id="page-main">
        <!-- Navigation Header -->
        <header class="sticky top-0 z-40 backdrop-blur-xl bg-black/50 border-b border-white/10">
            <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
                <a href="javascript:showPage('main')" class="fade-in-up flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-full border border-amber-300/40 flex items-center justify-center bg-gradient-to-tr from-amber-600/30 to-amber-200/10">
                        <span class="font-luxury text-amber-200 text-xl font-bold">R</span>
                    </div>
                    <span class="font-luxury text-xl tracking-[0.22em] text-white">RESINS <span class="text-amber-300 font-light text-sm tracking-normal">BY R</span></span>
                </a>

                <div class="flex items-center space-x-4">
                    <button onclick="showPage('policy')" class="fade-in-up text-xs uppercase tracking-widest text-gray-300 hover:text-amber-300 transition hidden sm:inline-block">
                        Policies
                    </button>
                    <button onclick="toggleCartDrawer(true)" class="fade-in-up relative flex items-center space-x-2 px-5 py-2 rounded-full border border-white/15 bg-white/5 hover:border-amber-300/40 transition">
                        <i class="ph ph-handbag text-amber-300 text-lg"></i>
                        <span class="text-xs uppercase tracking-widest text-gray-200 font-medium">Cart</span>
                        <span id="nav-cart-count" class="ml-1 px-2 py-0.5 text-xs bg-amber-400 text-black font-bold rounded-full">0</span>
                    </button>
                </div>
            </div>
        </header>

        <!-- Hero Section -->
        <section class="max-w-6xl mx-auto px-6 pt-20 pb-16 text-center relative z-10">
            <div class="fade-in-up inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-amber-400/20 bg-amber-400/5 mb-6">
                <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
                <span class="text-xs uppercase tracking-widest text-amber-300 font-semibold">100% Handcrafted • Liquid Elegance</span>
            </div>

            <h1 class="fade-in-up font-luxury text-4xl sm:text-6xl md:text-7xl font-semibold tracking-tight text-white mb-6 leading-tight">
                Frozen In Time.<br>
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-200 via-amber-400 to-yellow-500">Liquid Luxury</span> Preserved.
            </h1>

            <p class="fade-in-up max-w-2xl mx-auto text-gray-400 text-sm md:text-base leading-relaxed mb-8">
                Cured with botanical elements, 24k gold leaf, and high-clarity epoxy. Custom-made heirlooms designed to outlast memories.
            </p>

            <div class="fade-in-up flex items-center justify-center gap-4">
                <a href="#products-section" class="btn-gold px-8 py-3.5 rounded-full inline-flex items-center gap-3 text-xs tracking-widest uppercase">
                    <span>Explore Products</span>
                    <i class="ph ph-arrow-down text-sm"></i>
                </a>
                <button onclick="showPage('policy')" class="btn-glass px-7 py-3.5 rounded-full text-xs tracking-widest uppercase text-gray-300">
                    Studio Policies
                </button>
            </div>
        </section>

        <!-- Product Grid -->
        <main id="products-section" class="max-w-7xl mx-auto px-6 py-12 relative z-10">
            <div class="flex flex-col md:flex-row md:items-end justify-between mb-12 border-b border-white/10 pb-6">
                <div>
                    <h2 class="fade-in-up font-luxury text-3xl tracking-wide text-white">Signature Collection</h2>
                    <p class="fade-in-up text-gray-400 text-sm mt-1">Every artifact is poured individually upon order.</p>
                </div>
                <div class="fade-in-up mt-4 md:mt-0 text-amber-300 font-mono text-xs tracking-widest uppercase">
                    Flat Delivery: PKR 500/- Nationwide
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 lg:gap-10">
                
                <!-- 1. RESIN RING -->
                <div class="resin-card rounded-3xl p-6 flex flex-col justify-between">
                    <div>
                        <div class="fade-in-up relative h-64 sm:h-72 w-full rounded-2xl overflow-hidden mb-6 group">
                            <img src="https://images.unsplash.com/photo-1605100804763-247f67b3557e?q=80&w=800&auto=format&fit=crop" 
                                 alt="Resin Ring" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105">
                            <span class="absolute top-4 left-4 px-3 py-1 bg-black/60 backdrop-blur-md border border-white/10 rounded-full text-xs uppercase tracking-wider text-amber-300">
                                Jewelry
                            </span>
                        </div>

                        <div class="flex justify-between items-baseline mb-2">
                            <h3 class="fade-in-up font-luxury text-2xl text-white">Resin Ring</h3>
                            <span class="fade-in-up text-xl font-bold text-amber-300">PKR 800/-</span>
                        </div>
                        <p class="fade-in-up text-gray-400 text-sm mb-6">Polished glass-like epoxy ring infused with golden flakes and crystalline botanicals.</p>

                        <!-- Ring Size Selector -->
                        <div class="fade-in-up mb-6 bg-white/[0.02] p-4 rounded-xl border border-white/5">
                            <label class="block text-xs uppercase tracking-wider text-gray-300 font-semibold mb-2">Select Size (US):</label>
                            <div class="flex flex-wrap gap-2" id="ring-sizes">
                                <button type="button" onclick="selectRingSize(this, 'US 5')" class="size-btn px-3.5 py-1.5 rounded-lg border border-amber-300 text-xs text-amber-300 bg-amber-300/10 transition">US 5</button>
                                <button type="button" onclick="selectRingSize(this, 'US 6')" class="size-btn px-3.5 py-1.5 rounded-lg border border-white/10 text-xs text-gray-300 hover:border-amber-300 transition">US 6</button>
                                <button type="button" onclick="selectRingSize(this, 'US 7')" class="size-btn px-3.5 py-1.5 rounded-lg border border-white/10 text-xs text-gray-300 hover:border-amber-300 transition">US 7</button>
                                <button type="button" onclick="selectRingSize(this, 'US 8')" class="size-btn px-3.5 py-1.5 rounded-lg border border-white/10 text-xs text-gray-300 hover:border-amber-300 transition">US 8</button>
                                <button type="button" onclick="selectRingSize(this, 'US 9')" class="size-btn px-3.5 py-1.5 rounded-lg border border-white/10 text-xs text-gray-300 hover:border-amber-300 transition">US 9</button>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-3 pt-4 border-t border-white/5">
                        <button onclick="handleAddToCart('resin-ring')" class="fade-in-up btn-glass py-3 rounded-xl text-xs uppercase tracking-widest font-semibold flex items-center justify-center gap-2">
                            <i class="ph ph-shopping-bag"></i> Add To Cart
                        </button>
                        <button onclick="handleQuickOrder('resin-ring')" class="fade-in-up btn-gold py-3 rounded-xl text-xs uppercase tracking-widest font-bold">
                            Order Now
                        </button>
                    </div>
                </div>

                <!-- 2. RESIN SHIELD 6-INCH -->
                <div class="resin-card rounded-3xl p-6 flex flex-col justify-between">
                    <div>
                        <div class="fade-in-up relative h-64 sm:h-72 w-full rounded-2xl overflow-hidden mb-6 group">
                            <img src="https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?q=80&w=800&auto=format&fit=crop" 
                                 alt="Resin Shield" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105">
                            <span class="absolute top-4 left-4 px-3 py-1 bg-black/60 backdrop-blur-md border border-white/10 rounded-full text-xs uppercase tracking-wider text-amber-300">
                                Keepsake
                            </span>
                        </div>

                        <div class="flex justify-between items-baseline mb-2">
                            <h3 class="fade-in-up font-luxury text-2xl text-white">Resins Shield (6-Inch)</h3>
                            <span id="shield-price-display" class="fade-in-up text-xl font-bold text-amber-300">PKR 2,000/-</span>
                        </div>
                        <p class="fade-in-up text-gray-400 text-sm mb-4">6-inch solid resin plaque. Base price PKR 2,000/- with an option to embed up to 3 pictures (+PKR 100/- each).</p>

                        <!-- Picture Configurator -->
                        <div class="fade-in-up mb-6 bg-white/[0.02] p-4 rounded-xl border border-white/5">
                            <div class="flex justify-between items-center mb-3">
                                <label class="text-xs uppercase tracking-wider text-gray-300 font-semibold">Embedded Pictures (Max 3):</label>
                                <span class="text-xs text-amber-300 font-mono">+PKR 100 / pic</span>
                            </div>
                            <div class="flex items-center gap-4 mb-3">
                                <div class="flex items-center border border-white/20 rounded-lg overflow-hidden bg-black/40">
                                    <button type="button" onclick="adjustPhotos(-1)" class="px-3.5 py-1.5 text-gray-300 hover:bg-white/10"><i class="ph ph-minus"></i></button>
                                    <span id="shield-photo-count" class="px-4 py-1.5 text-sm font-semibold text-white">0</span>
                                    <button type="button" onclick="adjustPhotos(1)" class="px-3.5 py-1.5 text-gray-300 hover:bg-white/10"><i class="ph ph-plus"></i></button>
                                </div>
                                <span id="shield-photo-status" class="text-xs text-gray-400">0 pictures (+PKR 0/-)</span>
                            </div>

                            <!-- Upload Pictures Section (Shown when pictures count > 0) -->
                            <div id="shield-uploader-box" class="hidden pt-3 border-t border-white/10">
                                <label class="block text-xs uppercase tracking-wider text-amber-300 font-semibold mb-1">
                                    Upload Client Pictures:
                                </label>
                                <input type="file" id="shield-file-input" multiple accept="image/*" onchange="handleShieldFiles(this)" 
                                       class="w-full text-xs text-gray-400 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-amber-300/10 file:text-amber-300 hover:file:bg-amber-300/20 cursor-pointer">
                                <p id="shield-files-status" class="text-[11px] text-gray-400 mt-1">Please upload up to 3 photos.</p>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-3 pt-4 border-t border-white/5">
                        <button onclick="handleAddToCart('resin-shield')" class="fade-in-up btn-glass py-3 rounded-xl text-xs uppercase tracking-widest font-semibold flex items-center justify-center gap-2">
                            <i class="ph ph-shopping-bag"></i> Add To Cart
                        </button>
                        <button onclick="handleQuickOrder('resin-shield')" class="fade-in-up btn-gold py-3 rounded-xl text-xs uppercase tracking-widest font-bold">
                            Order Now
                        </button>
                    </div>
                </div>

                <!-- 3. RESIN 3D CHESS KEYCHAINS -->
                <div class="resin-card rounded-3xl p-6 flex flex-col justify-between">
                    <div>
                        <div class="fade-in-up relative h-64 sm:h-72 w-full rounded-2xl overflow-hidden mb-6 group">
                            <img src="https://images.unsplash.com/photo-1529699211952-734e80c4d42b?q=80&w=800&auto=format&fit=crop" 
                                 alt="3D Chess Keychains" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105">
                            <span class="absolute top-4 left-4 px-3 py-1 bg-black/60 backdrop-blur-md border border-white/10 rounded-full text-xs uppercase tracking-wider text-amber-300">
                                Collectibles
                            </span>
                        </div>

                        <div class="flex justify-between items-baseline mb-2">
                            <h3 class="fade-in-up font-luxury text-2xl text-white">Resin 3D Chess Keychains</h3>
                            <span class="fade-in-up text-xl font-bold text-amber-300">PKR 500/-</span>
                        </div>
                        <p class="fade-in-up text-gray-400 text-sm mb-6">Hand-poured 3D Chess pieces (Knight, Queen, King) with heavy shimmer mica and durable gold keyrings.</p>
                    </div>

                    <div class="grid grid-cols-2 gap-3 pt-4 border-t border-white/5">
                        <button onclick="handleAddToCart('chess-keychain')" class="fade-in-up btn-glass py-3 rounded-xl text-xs uppercase tracking-widest font-semibold flex items-center justify-center gap-2">
                            <i class="ph ph-shopping-bag"></i> Add To Cart
                        </button>
                        <button onclick="handleQuickOrder('chess-keychain')" class="fade-in-up btn-gold py-3 rounded-xl text-xs uppercase tracking-widest font-bold">
                            Order Now
                        </button>
                    </div>
                </div>

                <!-- 4. RESIN TRAY AND COASTER SET -->
                <div class="resin-card rounded-3xl p-6 flex flex-col justify-between">
                    <div>
                        <div class="fade-in-up relative h-64 sm:h-72 w-full rounded-2xl overflow-hidden mb-6 group">
                            <img src="https://images.unsplash.com/photo-1615529182904-14819c35db37?q=80&w=800&auto=format&fit=crop" 
                                 alt="Tray & Coaster Set" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105">
                            <span class="absolute top-4 left-4 px-3 py-1 bg-black/60 backdrop-blur-md border border-white/10 rounded-full text-xs uppercase tracking-wider text-amber-300">
                                Home Decor
                            </span>
                        </div>

                        <div class="flex justify-between items-baseline mb-2">
                            <h3 class="fade-in-up font-luxury text-2xl text-white">Resin Tray & Coaster Set</h3>
                            <span class="fade-in-up text-xl font-bold text-amber-300">PKR 4,000/-</span>
                        </div>
                        <p class="fade-in-up text-gray-400 text-sm mb-6">Complete luxury set: 1 signature serving tray and 4 matching coasters hand-embellished with gilded raw edges.</p>
                    </div>

                    <div class="grid grid-cols-2 gap-3 pt-4 border-t border-white/5">
                        <button onclick="handleAddToCart('tray-coaster-set')" class="fade-in-up btn-glass py-3 rounded-xl text-xs uppercase tracking-widest font-semibold flex items-center justify-center gap-2">
                            <i class="ph ph-shopping-bag"></i> Add To Cart
                        </button>
                        <button onclick="handleQuickOrder('tray-coaster-set')" class="fade-in-up btn-gold py-3 rounded-xl text-xs uppercase tracking-widest font-bold">
                            Order Now
                        </button>
                    </div>
                </div>

            </div>
        </main>

        <!-- Studio Footer -->
        <footer class="border-t border-white/10 bg-black/60 py-12 px-6 mt-20 relative z-10">
            <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6 text-center md:text-left">
                <div>
                    <h3 class="font-luxury text-lg text-white">RESINS BY R</h3>
                    <p class="text-xs text-gray-400 mt-1">Direct inquiries & instant support:</p>
                    <a href="https://wa.me/923058866692?text=Assalamo-alaikum%20Resins%20by%20R%2C%20I%20have%20an%20inquiry%20regarding%20bespoke%20orders." 
                       target="_blank" 
                       class="text-amber-300 hover:text-amber-200 text-sm font-semibold flex items-center justify-center md:justify-start gap-2 mt-2">
                        <i class="ph ph-whatsapp-logo text-lg"></i>
                        <span>0305-8866692 (Ramsha Fatima)</span>
                    </a>
                </div>

                <div class="flex items-center gap-6 text-xs text-gray-400">
                    <button onclick="showPage('policy')" class="hover:text-amber-300 transition">Studio Policies</button>
                    <button onclick="showPage('404')" class="hover:text-amber-300 transition">Error 404 Preview</button>
                </div>
            </div>
        </footer>
    </div>

    <!-- POLICY VIEW PAGE -->
    <div id="page-policy" class="hidden min-h-screen pt-12 pb-24 px-6 max-w-4xl mx-auto relative z-10">
        <button onclick="showPage('main')" class="mb-8 btn-glass px-5 py-2.5 rounded-full text-xs uppercase tracking-widest text-amber-300 flex items-center gap-2">
            <i class="ph ph-arrow-left"></i> Return to Store
        </button>

        <div class="resin-card p-8 md:p-12 rounded-3xl border border-white/10">
            <h1 class="font-luxury text-3xl md:text-4xl text-white mb-2">Studio Policies</h1>
            <p class="text-xs uppercase tracking-widest text-amber-300 mb-8 font-semibold">Terms of Artistry, Crafting & Deliveries</p>

            <div class="space-y-6 text-sm text-gray-300 leading-relaxed">
                <div>
                    <h2 class="text-base font-semibold text-white flex items-center gap-2">
                        <span class="text-amber-300">1.</span> Bespoke No-Return Policy
                    </h2>
                    <p class="mt-1 text-gray-400">Every single product is custom-poured and personalized according to your selected dimensions, color palette, and design notes. As these are irreversible bespoke commissions, we do not accept returns or refunds.</p>
                </div>

                <div>
                    <h2 class="text-base font-semibold text-white flex items-center gap-2">
                        <span class="text-amber-300">2.</span> Organic Micro-Bubbles & Human Touch
                    </h2>
                    <p class="mt-1 text-gray-400">Resin curing is an organic thermodynamic chemical process. While we vacuum-degas and torch our pours to maintain museum-grade glass clarity, minor micro-bubbles or microscopic variations may occur. These are natural characteristics of hand-poured epoxy craftsmanship.</p>
                </div>

                <div>
                    <h2 class="text-base font-semibold text-white flex items-center gap-2">
                        <span class="text-amber-300">3.</span> Order Finality After Confirmation
                    </h2>
                    <p class="mt-1 text-gray-400">Once your order and specifications have been confirmed by our seller via WhatsApp, the casting and pigment curation begins immediately. Orders cannot be canceled or modified after this confirmation point.</p>
                </div>

                <div>
                    <h2 class="text-base font-semibold text-white flex items-center gap-2">
                        <span class="text-amber-300">4.</span> 100% Advance Payment Solemnity
                    </h2>
                    <p class="mt-1 text-gray-400">Because every artifact is customized, 100% advance payment via JazzCash or Raast ID (0305-8866692 - Ramsha Fatima) is required to validate your commitment and initiate pouring.</p>
                </div>

                <div>
                    <h2 class="text-base font-semibold text-white flex items-center gap-2">
                        <span class="text-amber-300">5.</span> 3–7 Days Curing & Hardening Protocol
                    </h2>
                    <p class="mt-1 text-gray-400">High-grade bio-resin requires between 72 to 168 hours to fully cross-link and cure to rock-solid barcol hardness. Dispatching resin before full chemical cure causes heat warping and transit distortion. Please allow 3–7 business days before dispatch.</p>
                </div>

                <div>
                    <h2 class="text-base font-semibold text-white flex items-center gap-2">
                        <span class="text-amber-300">6.</span> Heirloom Resin Care
                    </h2>
                    <p class="mt-1 text-gray-400">Keep out of direct, prolonged outdoor sunlight. Clean only with a gentle microfiber towel and mild soapy water. Never use harsh abrasive chemicals or high-heat dishwashers.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- ERROR 404 PAGE -->
    <div id="page-404" class="hidden min-h-screen flex items-center justify-center px-6 relative z-10 text-center">
        <div class="resin-card p-10 md:p-14 rounded-3xl max-w-lg border border-white/10">
            <span class="font-luxury text-7xl font-bold text-amber-300/80 block mb-2">404</span>
            <h2 class="font-luxury text-2xl text-white mb-3">Resin Void: Piece Unfound</h2>
            <p class="text-xs text-gray-400 leading-relaxed mb-6">
                The artifact or chamber you are looking for has not materialized or was wiped from our casting inventory.
            </p>
            <button onclick="showPage('main')" class="btn-gold px-8 py-3 rounded-full text-xs uppercase tracking-widest font-bold">
                Return to Studio Catalog
            </button>
        </div>
    </div>

    <!-- SLIDE-OVER CART DRAWER -->
    <div id="cart-drawer-backdrop" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden" onclick="toggleCartDrawer(false)"></div>
    <aside id="cart-drawer" class="fixed top-0 right-0 h-full w-full max-w-md bg-[#0a0b0e] border-l border-white/10 z-50 translate-x-full transition-transform duration-500 ease-in-out flex flex-col justify-between shadow-2xl">
        <div class="p-6 border-b border-white/10 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <i class="ph ph-handbag text-amber-300 text-2xl"></i>
                <h3 class="font-luxury text-xl text-white tracking-wide">Your Resin Bag</h3>
            </div>
            <button onclick="toggleCartDrawer(false)" class="text-gray-400 hover:text-white text-2xl p-1">&times;</button>
        </div>

        <div id="cart-items-container" class="p-6 overflow-y-auto space-y-4 flex-grow">
            <!-- Populated via JS -->
        </div>

        <div class="p-6 border-t border-white/10 bg-black/50 space-y-3">
            <div class="flex justify-between text-sm text-gray-400">
                <span>Sub-Total</span>
                <span id="cart-subtotal" class="font-mono text-white">PKR 0/-</span>
            </div>
            <div class="flex justify-between text-sm text-gray-400">
                <span>Delivery Charges</span>
                <span class="font-mono text-white">PKR 500/-</span>
            </div>
            <div class="flex justify-between text-base font-bold text-white pt-2 border-t border-white/10">
                <span>Total Amount</span>
                <span id="cart-grandtotal" class="font-mono text-amber-300 text-lg">PKR 500/-</span>
            </div>
            <button onclick="proceedToCheckoutFromCart()" class="btn-gold w-full py-3.5 rounded-xl text-xs uppercase tracking-widest font-bold mt-2">
                Order Now
            </button>
        </div>
    </aside>

    <!-- CHECKOUT MODAL -->
    <div id="checkout-modal" class="fixed inset-0 bg-black/85 backdrop-blur-md z-50 hidden flex items-center justify-center p-4 overflow-y-auto">
        <div class="resin-card bg-[#0e0f14] w-full max-w-xl rounded-3xl border border-white/15 p-6 md:p-8 relative max-h-[92vh] overflow-y-auto my-auto shadow-2xl">
            <button onclick="toggleCheckoutModal(false)" class="absolute top-5 right-5 text-gray-400 hover:text-amber-300 text-2xl">&times;</button>

            <div class="text-center mb-6">
                <span class="text-xs uppercase tracking-widest text-amber-300 font-semibold">Resins By R • Commission Form</span>
                <h3 class="font-luxury text-2xl text-white mt-1">Client Order Details</h3>
            </div>

            <!-- Cost Summary -->
            <div class="p-4 rounded-2xl bg-white/[0.03] border border-white/10 mb-6 space-y-2">
                <div class="flex justify-between text-xs text-gray-300">
                    <span>Selected Artifacts:</span>
                    <span id="modal-item-summary" class="font-medium text-right text-white"></span>
                </div>
                <div class="flex justify-between text-xs text-gray-400">
                    <span>Sub-Total:</span>
                    <span id="modal-subtotal" class="font-mono text-white">PKR 0/-</span>
                </div>
                <div class="flex justify-between text-xs text-gray-400">
                    <span>Delivery Charges:</span>
                    <span class="font-mono text-white">PKR 500/-</span>
                </div>
                <div class="flex justify-between text-sm font-bold text-amber-300 pt-2 border-t border-white/5">
                    <span>Total Amount Payable:</span>
                    <span id="modal-total" class="font-mono text-base">PKR 0/-</span>
                </div>
            </div>

            <!-- Bank / JazzCash Notice -->
            <div class="p-3.5 rounded-xl bg-amber-400/10 border border-amber-300/30 mb-5 text-xs text-amber-200">
                <div class="font-bold flex items-center gap-1.5 mb-0.5">
                    <i class="ph ph-wallet text-sm"></i> JazzCash / Raast Payment Details:
                </div>
                <div>Account Number: <strong class="text-white font-mono">0305-8866692</strong></div>
                <div>Account Title: <strong class="text-white">Ramsha Fatima</strong></div>
            </div>

            <!-- Form -->
            <form id="order-form" onsubmit="submitClientOrder(event)" class="space-y-4 text-left">
                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-300 font-semibold mb-1">
                        1. Full Name <span class="text-amber-400">*</span>
                    </label>
                    <input type="text" id="cust-name" required placeholder="Your full name" 
                           class="w-full px-4 py-3 bg-white/5 border border-white/15 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-amber-300">
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-300 font-semibold mb-1">
                        2. Phone Number <span class="text-amber-400">*</span>
                    </label>
                    <input type="tel" id="cust-phone" required placeholder="0300 1234567" 
                           class="w-full px-4 py-3 bg-white/5 border border-white/15 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-amber-300">
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-300 font-semibold mb-1">
                        3. Full Address <span class="text-amber-400">*</span>
                    </label>
                    <textarea id="cust-address" required rows="2" placeholder="House/Flat #, Street address, Area, City" 
                              class="w-full px-4 py-3 bg-white/5 border border-white/15 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-amber-300"></textarea>
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-300 font-semibold mb-1">
                        4. TID (Transaction ID) For Payment Made <span class="text-amber-400">*</span>
                    </label>
                    <input type="text" id="cust-tid" required placeholder="Transaction ID (JazzCash / Raast)" 
                           class="w-full px-4 py-3 bg-white/5 border border-white/15 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-amber-300 font-mono">
                </div>

                <!-- MANDATORY PAYMENT SCREENSHOT -->
                <div>
                    <label class="block text-xs uppercase tracking-wider text-amber-300 font-semibold mb-1">
                        5. Upload Screenshot of Payment Made <span class="text-amber-400">*</span>
                    </label>
                    <input type="file" id="cust-payment-screenshot" required accept="image/*" 
                           class="w-full text-xs text-gray-400 file:mr-3 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-amber-300 file:text-black hover:file:bg-amber-400 cursor-pointer">
                    <p class="text-[11px] text-gray-400 mt-1">Please attach receipt confirmation from JazzCash / Raast.</p>
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-300 font-semibold mb-1">
                        Customization Notes (Colours, Foil, or Styling)
                    </label>
                    <textarea id="cust-notes" rows="2" placeholder="Describe chosen color tones, glitter, or custom details." 
                              class="w-full px-4 py-3 bg-white/5 border border-white/15 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-amber-300"></textarea>
                </div>

                <button type="submit" id="submit-btn" class="btn-gold w-full py-4 rounded-xl text-xs uppercase tracking-widest font-bold mt-2 shadow-xl flex items-center justify-center gap-2">
                    <span>Submit & Generate Order ID</span>
                </button>
            </form>
        </div>
    </div>

    <!-- ORDER SUCCESS CONFIRMATION MODAL WITH WHATSAPP LINK -->
    <div id="success-modal" class="fixed inset-0 bg-black/90 backdrop-blur-md z-50 hidden flex items-center justify-center p-4">
        <div class="resin-card bg-[#0e0f14] w-full max-w-lg rounded-3xl border border-amber-300/40 p-8 text-center shadow-2xl relative">
            <div class="w-16 h-16 mx-auto mb-4 rounded-full border border-amber-300/60 bg-amber-300/10 flex items-center justify-center">
                <i class="ph ph-check text-amber-300 text-3xl"></i>
            </div>

            <span class="text-xs uppercase tracking-widest text-amber-300 font-semibold">Commission Received</span>
            <h3 class="font-luxury text-2xl text-white mt-1 mb-2">Order Confirmed!</h3>
            
            <p class="text-xs text-gray-400 mb-6">
                Your order has been registered in our studio queue. Please use your unique Order ID below for reference:
            </p>

            <div class="p-4 rounded-2xl bg-white/[0.04] border border-amber-300/30 mb-6">
                <span class="text-xs text-gray-400 block mb-1">Unique Order ID</span>
                <span id="confirmed-order-id" class="font-mono text-2xl font-bold text-amber-300 tracking-wider">RBR-00000</span>
            </div>

            <!-- Pre-filled WhatsApp button -->
            <a id="whatsapp-order-link" href="#" target="_blank" class="btn-gold w-full py-4 rounded-xl text-xs uppercase tracking-widest font-bold flex items-center justify-center gap-2 mb-3">
                <i class="ph ph-whatsapp-logo text-lg"></i>
                <span>Confirm on WhatsApp (0305-8866692)</span>
            </a>

            <button onclick="closeSuccessModal()" class="text-xs text-gray-400 hover:text-white uppercase tracking-wider py-2">
                Close & Return to Studio
            </button>
        </div>
    </div>

    <!-- Toast Notification -->
    <div id="toast" class="fixed bottom-6 left-1/2 -translate-x-1/2 bg-[#101115] border border-amber-300/50 text-white px-6 py-3 rounded-full text-xs uppercase tracking-widest shadow-2xl opacity-0 pointer-events-none transition-all duration-300 z-50 flex items-center gap-2">
        <i class="ph ph-sparkle text-amber-300 text-base"></i>
        <span id="toast-msg">Item added to cart</span>
    </div>

    <script>
        const DISCORD_WEBHOOK_URL = "{DISCORD_WEBHOOK_URL}".trim();
        const SELLER_WHATSAPP = "923058866692";
        const DELIVERY_FEE = 500;

        let cart = [];
        let selectedRingSize = 'US 5';
        let shieldPhotosCount = 0;
        let shieldUploadedFiles = [];
        let quickOrderItem = null;

        // 1. DUST CANVAS FOR INTRO
        const canvas = document.getElementById('dust-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];

        function resizeCanvas() {{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }}
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        for(let i=0; i<60; i++) {{
            particles.push({{
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                radius: Math.random() * 2.5 + 0.5,
                color: Math.random() > 0.4 ? '#e5b869' : '#ffffff',
                vy: -Math.random() * 0.8 - 0.2,
                vx: (Math.random() - 0.5) * 0.5,
                alpha: Math.random() * 0.8 + 0.2
            }});
        }}

        function animateDust() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => {{
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.globalAlpha = p.alpha;
                ctx.shadowBlur = 6;
                ctx.shadowColor = p.color;
                ctx.fill();

                p.y += p.vy;
                p.x += p.vx;
                if(p.y < 0) p.y = canvas.height;
                if(p.x < 0) p.x = canvas.width;
                if(p.x > canvas.width) p.x = 0;
            }});
            requestAnimationFrame(animateDust);
        }}
        animateDust();

        // 2. TIMELINE: INTRO -> MAIN SITE FADE-IN
        window.addEventListener('load', () => {{
            setTimeout(() => {{
                const cap = document.getElementById('intro-caption');
                if (cap) cap.style.opacity = '1';
            }}, 2100);

            // Intro fade out
            setTimeout(() => {{
                const intro = document.getElementById('intro-overlay');
                intro.style.opacity = '0';
                document.body.classList.add('site-ready');
                
                setTimeout(() => {{
                    intro.style.display = 'none';
                    initScrollObserver();
                }}, 1100);
            }}, 3400);
        }});

        // 3. ONE-TIME FADE-IN-UPWARDS OBSERVER
        function initScrollObserver() {{
            const elements = document.querySelectorAll('.fade-in-up');
            const observer = new IntersectionObserver((entries) => {{
                entries.forEach((entry, idx) => {{
                    if (entry.isIntersecting) {{
                        setTimeout(() => {{
                            entry.target.classList.add('appeared');
                        }}, idx * 60);
                        observer.unobserve(entry.target);
                    }}
                }});
            }}, {{ threshold: 0.1 }});

            elements.forEach(el => observer.observe(el));
        }}

        // Page Navigation
        function showPage(page) {{
            document.getElementById('page-main').classList.add('hidden');
            document.getElementById('page-policy').classList.add('hidden');
            document.getElementById('page-404').classList.add('hidden');

            if (page === 'main') {{
                document.getElementById('page-main').classList.remove('hidden');
                initScrollObserver();
            }} else if (page === 'policy') {{
                document.getElementById('page-policy').classList.remove('hidden');
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }} else if (page === '404') {{
                document.getElementById('page-404').classList.remove('hidden');
            }}
        }}

        // Ring size selection
        function selectRingSize(btn, size) {{
            document.querySelectorAll('#ring-sizes .size-btn').forEach(b => {{
                b.className = 'size-btn px-3.5 py-1.5 rounded-lg border border-white/10 text-xs text-gray-300 hover:border-amber-300 transition';
            }});
            btn.className = 'size-btn px-3.5 py-1.5 rounded-lg border border-amber-300 text-xs text-amber-300 bg-amber-300/10 transition';
            selectedRingSize = size;
        }}

        // Shield photo counter
        function adjustPhotos(delta) {{
            shieldPhotosCount = Math.max(0, Math.min(3, shieldPhotosCount + delta));
            document.getElementById('shield-photo-count').innerText = shieldPhotosCount;
            const total = 2000 + (shieldPhotosCount * 100);
            document.getElementById('shield-price-display').innerText = `PKR ${{total.toLocaleString()}}/-`;
            document.getElementById('shield-photo-status').innerText = `${{shieldPhotosCount}} picture(s) (+PKR ${{shieldPhotosCount * 100}}/-)`;

            const uploader = document.getElementById('shield-uploader-box');
            if (shieldPhotosCount > 0) {{
                uploader.classList.remove('hidden');
            }} else {{
                uploader.classList.add('hidden');
                shieldUploadedFiles = [];
            }}
        }}

        function handleShieldFiles(input) {{
            const files = Array.from(input.files);
            if (files.length > 3) {{
                alert("You can upload a maximum of 3 pictures.");
                input.value = "";
                shieldUploadedFiles = [];
                document.getElementById('shield-files-status').innerText = "Please upload up to 3 photos.";
                return;
            }}
            shieldUploadedFiles = files;
            document.getElementById('shield-files-status').innerText = `${{files.length}} file(s) selected for shield embedding.`;
        }}

        function generateUniqueOrderId() {{
            const randomDigits = Math.floor(10000 + Math.random() * 90000);
            return `RBR-${{randomDigits}}`;
        }}

        function getProductSpecs(id) {{
            if (id === 'resin-ring') {{
                return {{
                    id: 'resin-ring',
                    name: `Resin Ring (${{selectedRingSize}})`,
                    spec: `Size: ${{selectedRingSize}}`,
                    price: 800,
                    qty: 1
                }};
            }} else if (id === 'resin-shield') {{
                const total = 2000 + (shieldPhotosCount * 100);
                return {{
                    id: 'resin-shield',
                    name: 'Resins Shield (6-Inch)',
                    spec: shieldPhotosCount > 0 ? `${{shieldPhotosCount}} custom picture(s)` : 'No pictures',
                    price: total,
                    qty: 1
                }};
            }} else if (id === 'chess-keychain') {{
                return {{
                    id: 'chess-keychain',
                    name: 'Resin 3D Chess Keychain',
                    spec: 'Sculpted Piece',
                    price: 500,
                    qty: 1
                }};
            }} else if (id === 'tray-coaster-set') {{
                return {{
                    id: 'tray-coaster-set',
                    name: 'Resin Tray & Coaster Set',
                    spec: '1 Tray + 4 Coasters',
                    price: 4000,
                    qty: 1
                }};
            }}
        }}

        function handleAddToCart(id) {{
            const item = getProductSpecs(id);
            const exists = cart.find(i => i.name === item.name && i.spec === item.spec);
            if (exists) {{
                exists.qty += 1;
            }} else {{
                cart.push(item);
            }}
            renderCart();
            showToast(`"${{item.name}}" added to cart`);
        }}

        function handleQuickOrder(id) {{
            quickOrderItem = getProductSpecs(id);
            openCheckoutModal([quickOrderItem]);
        }}

        function renderCart() {{
            const list = document.getElementById('cart-items-container');
            const totalCount = cart.reduce((acc, c) => acc + c.qty, 0);
            document.getElementById('nav-cart-count').innerText = totalCount;

            if (cart.length === 0) {{
                list.innerHTML = `<div class="h-64 flex flex-col items-center justify-center text-gray-500 text-sm">Your bag is empty.</div>`;
                document.getElementById('cart-subtotal').innerText = 'PKR 0/-';
                document.getElementById('cart-grandtotal').innerText = `PKR ${{DELIVERY_FEE}}/-`;
                return;
            }}

            let subtotal = 0;
            let html = '';
            cart.forEach((item, idx) => {{
                const cost = item.price * item.qty;
                subtotal += cost;
                html += `
                    <div class="p-4 rounded-xl bg-white/[0.03] border border-white/5 flex items-center justify-between">
                        <div>
                            <h4 class="text-sm font-semibold text-white">${{item.name}}</h4>
                            <p class="text-xs text-amber-300">${{item.spec}}</p>
                            <span class="text-xs font-mono text-gray-400 mt-1 block">Qty: ${{item.qty}} × PKR ${{item.price}}/-</span>
                        </div>
                        <div class="flex items-center gap-3">
                            <span class="font-mono text-sm font-bold text-white">PKR ${{cost}}/-</span>
                            <button onclick="removeCartItem(${{idx}})" class="text-gray-500 hover:text-red-400 text-base">&times;</button>
                        </div>
                    </div>`;
            }});

            list.innerHTML = html;
            document.getElementById('cart-subtotal').innerText = `PKR ${{subtotal.toLocaleString()}}/-`;
            document.getElementById('cart-grandtotal').innerText = `PKR ${{(subtotal + DELIVERY_FEE).toLocaleString()}}/-`;
        }}

        function removeCartItem(idx) {{
            cart.splice(idx, 1);
            renderCart();
        }}

        function toggleCartDrawer(open) {{
            const drawer = document.getElementById('cart-drawer');
            const backdrop = document.getElementById('cart-drawer-backdrop');
            if (open) {{
                backdrop.classList.remove('hidden');
                setTimeout(() => drawer.classList.remove('translate-x-full'), 10);
            }} else {{
                drawer.classList.add('translate-x-full');
                setTimeout(() => backdrop.classList.add('hidden'), 300);
            }}
        }}

        function proceedToCheckoutFromCart() {{
            if (cart.length === 0) {{
                showToast("Your cart is empty");
                return;
            }}
            toggleCartDrawer(false);
            quickOrderItem = null;
            openCheckoutModal(cart);
        }}

        function openCheckoutModal(items) {{
            const subtotal = items.reduce((acc, c) => acc + (c.price * c.qty), 0);
            const total = subtotal + DELIVERY_FEE;

            document.getElementById('modal-item-summary').innerText = items.map(i => `${{i.name}} (x${{i.qty}})`).join(', ');
            document.getElementById('modal-subtotal').innerText = `PKR ${{subtotal.toLocaleString()}}/-`;
            document.getElementById('modal-total').innerText = `PKR ${{total.toLocaleString()}}/-`;

            toggleCheckoutModal(true);
        }}

        function toggleCheckoutModal(open) {{
            const modal = document.getElementById('checkout-modal');
            if (open) modal.classList.remove('hidden');
            else modal.classList.add('hidden');
        }}

        function showToast(msg) {{
            const toast = document.getElementById('toast');
            document.getElementById('toast-msg').innerText = msg;
            toast.classList.remove('opacity-0', 'pointer-events-none');
            setTimeout(() => toast.classList.add('opacity-0', 'pointer-events-none'), 3000);
        }}

        // 4. DISPATCH ORDER TO DISCORD WEBHOOK & ALLOT UNIQUE ORDER ID
        async function submitClientOrder(e) {{
            e.preventDefault();

            const screenshotInput = document.getElementById('cust-payment-screenshot');
            if (!screenshotInput.files || screenshotInput.files.length === 0) {{
                alert("Please attach screenshot of payment made.");
                return;
            }}

            const btn = document.getElementById('submit-btn');
            btn.disabled = true;
            btn.innerHTML = `<span class="animate-pulse">Registering Order & Generating ID...</span>`;

            const orderId = generateUniqueOrderId();
            const fullName = document.getElementById('cust-name').value.trim();
            const phone = document.getElementById('cust-phone').value.trim();
            const address = document.getElementById('cust-address').value.trim();
            const tid = document.getElementById('cust-tid').value.trim();
            const notes = document.getElementById('cust-notes').value.trim() || 'No customization notes';

            const activeItems = quickOrderItem ? [quickOrderItem] : cart;
            const subtotal = activeItems.reduce((acc, c) => acc + (c.price * c.qty), 0);
            const grandTotal = subtotal + DELIVERY_FEE;
            const productsListString = activeItems.map(i => `${{i.name}} (x${{i.qty}})`).join(', ');

            // Construct Multipart Form-Data for Discord
            const formData = new FormData();
            
            // Build rich embed
            const embedPayload = {{
                title: `✨ New Bespoke Order: ${{orderId}}`,
                color: 15054953, // Resin Gold #E5B869
                fields: [
                    {{ name: "Order ID", value: orderId, inline: true }},
                    {{ name: "Client Name", value: fullName, inline: true }},
                    {{ name: "Phone Number", value: phone, inline: true }},
                    {{ name: "Delivery Address", value: address, inline: false }},
                    {{ name: "Payment TID", value: tid, inline: true }},
                    {{ name: "Payment Account", value: "0305-8866692 (Ramsha Fatima)", inline: true }},
                    {{ name: "Items Ordered", value: productsListString, inline: false }},
                    {{ name: "Sub-Total", value: `PKR ${{subtotal}}/-`, inline: true }},
                    {{ name: "Delivery Fee", value: `PKR ${{DELIVERY_FEE}}/-`, inline: true }},
                    {{ name: "Grand Total", value: `PKR ${{grandTotal}}/-`, inline: true }},
                    {{ name: "Custom Notes", value: notes, inline: false }}
                ],
                footer: {{ text: "Resins by R • Automation Queue" }},
                timestamp: new Date().toISOString()
            }};

            formData.append("payload_json", JSON.stringify({{
                content: `🚨 **New Order Received from ${{fullName}}** | Order ID: \`${{orderId}}\``,
                embeds: [embedPayload]
            }}));

            // Attach payment screenshot
            formData.append("files[0]", screenshotInput.files[0], `Payment_TID_${{tid}}_${{screenshotInput.files[0].name}}`);

            // Attach shield images if any
            let fileIndex = 1;
            shieldUploadedFiles.forEach((file) => {{
                formData.append(`files[${{fileIndex}}]`, file, `Shield_Inclusion_${{fileIndex}}_${{file.name}}`);
                fileIndex++;
            }});

            // Send to Discord Webhook
            if (DISCORD_WEBHOOK_URL && DISCORD_WEBHOOK_URL.startsWith('http')) {{
                try {{
                    await fetch(DISCORD_WEBHOOK_URL, {{
                        method: 'POST',
                        body: formData
                    }});
                }} catch (err) {{
                    console.warn("Discord Webhook dispatch failed:", err);
                }}
            }} else {{
                console.info("No valid DISCORD_WEBHOOK_URL set. Order logged locally.");
            }}

            // Pre-fill WhatsApp Confirmation Link
            const prewrittenMsg = `Assalamo-alaikum, I had ordered ${{productsListString}} under the order ID ${{orderId}}, can I get a confirmation on it?`;
            const waUrl = `https://wa.me/${{SELLER_WHATSAPP}}?text=${{encodeURIComponent(prewrittenMsg)}}`;

            document.getElementById('confirmed-order-id').innerText = orderId;
            document.getElementById('whatsapp-order-link').href = waUrl;

            // Reset and show success modal
            toggleCheckoutModal(false);
            document.getElementById('success-modal').classList.remove('hidden');
            cart = [];
            quickOrderItem = null;
            renderCart();
            document.getElementById('order-form').reset();
            shieldUploadedFiles = [];
            document.getElementById('shield-uploader-box').classList.add('hidden');
            document.getElementById('shield-photo-count').innerText = "0";

            btn.disabled = false;
            btn.innerHTML = `<span>Submit & Generate Order ID</span>`;
        }}

        function closeSuccessModal() {{
            document.getElementById('success-modal').classList.add('hidden');
        }}

        renderCart();
    </script>
</body>
</html>
"""

# 5. Render App
components.html(HTML_TEMPLATE, height=1000, scrolling=True)
