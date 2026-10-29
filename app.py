import os
import json
import time
import hmac
import html
import re
import base64
import requests
import streamlit as st
import streamlit.components.v1 as components

# ================= SECRETS & ENVIRONMENT CONFIGURATION =================
GSHEET_URL = st.secrets.get("GSHEET_URL", os.environ.get("GSHEET_URL", "")).strip()
ADMIN_NAME = st.secrets.get("ADMIN_NAME", os.environ.get("ADMIN_NAME", "admin")).strip()
ADMIN_PASS = st.secrets.get("ADMIN_PASS", os.environ.get("ADMIN_PASS", "resin123")).strip()
DISCORD_WEBHOOK_URL = st.secrets.get("DISCORD_WEBHOOK_URL", os.environ.get("DISCORD_WEBHOOK_URL", "")).strip()

st.set_page_config(
    page_title="Resins by R | Bespoke Handcrafted Resin",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Session Security State Initialization
if "orders_db" not in st.session_state:
    st.session_state["orders_db"] = []
if "admin_authenticated" not in st.session_state:
    st.session_state["admin_authenticated"] = False
if "dispatch_target" not in st.session_state:
    st.session_state["dispatch_target"] = None
if "admin_failed_attempts" not in st.session_state:
    st.session_state["admin_failed_attempts"] = 0
if "admin_locked_until" not in st.session_state:
    st.session_state["admin_locked_until"] = 0.0
if "last_admin_fetch" not in st.session_state:
    st.session_state["last_admin_fetch"] = 0.0

# ================= SECURE BASE64 IMAGE LOADER =================
def get_image_src(filename, fallback_url):
    """
    Safely reads local product images, sanitizes path to prevent traversal,
    and encodes them into Base64 for zero-CORS iframe rendering.
    """
    safe_name = os.path.basename(filename)
    base_name = os.path.splitext(safe_name)[0]
    for ext in ["jpg", "jpeg", "png", "webp"]:
        candidate_path = os.path.join("images", f"{base_name}.{ext}")
        if os.path.exists(candidate_path) and os.path.isfile(candidate_path):
            try:
                # 5MB local safety check
                if os.path.getsize(candidate_path) <= 5 * 1024 * 1024:
                    with open(candidate_path, "rb") as img_file:
                        encoded = base64.b64encode(img_file.read()).decode()
                    mime = "image/png" if ext == "png" else f"image/{ext}"
                    return f"data:{mime};base64,{encoded}"
            except Exception:
                pass
    return fallback_url

IMG_PRODUCT_1 = get_image_src("Product1.jpg", "https://images.unsplash.com/photo-1605100804763-247f67b3557e?q=80&w=800&auto=format&fit=crop")
IMG_PRODUCT_2 = get_image_src("Product2.jpg", "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?q=80&w=800&auto=format&fit=crop")
IMG_PRODUCT_3 = get_image_src("Product3.jpg", "https://images.unsplash.com/photo-1529699211952-734e80c4d42b?q=80&w=800&auto=format&fit=crop")
IMG_PRODUCT_4 = get_image_src("Product4.jpg", "https://images.unsplash.com/photo-1615529182904-14819c35db37?q=80&w=800&auto=format&fit=crop")

# ================= SECURE BACKEND GOOGLE SHEET API =================
@st.cache_data(ttl=25, show_spinner=False)
def fetch_pending_orders_cached(url):
    """Protected fetcher to respect Google Apps Script rate limits."""
    if url and url.startswith("http"):
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                if isinstance(data, list):
                    return [o for o in data if str(o.get("status", "")).strip().lower() == "pending"]
        except Exception:
            pass
    return []

def fetch_pending_orders():
    if GSHEET_URL:
        orders = fetch_pending_orders_cached(GSHEET_URL)
        if orders:
            return orders
    return [o for o in st.session_state["orders_db"] if str(o.get("status", "")).lower() == "pending"]

def mark_order_dispatched(order_id):
    """Updates order status to Dispatched with strict alphanumeric sanitization."""
    safe_order_id = "".join(c for c in str(order_id) if c.isalnum() or c == "-")
    success = False
    if GSHEET_URL and GSHEET_URL.startswith("http"):
        try:
            res = requests.get(f"{GSHEET_URL}?action=dispatch_order&order_id={safe_order_id}", timeout=10)
            if res.status_code == 200:
                success = True
                st.cache_data.clear()
        except Exception as e:
            st.error(f"Error updating Google Sheet dispatch: {e}")
    
    for item in st.session_state["orders_db"]:
        if str(item.get("order_id")) == safe_order_id:
            item["status"] = "Dispatched"
            success = True
            break

    return success

# ================= STOREFRONT CLIENT VIEW =================
def storefront_view():
    HTML_TEMPLATE = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Resins by R</title>
        
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
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

            * {{ box-sizing: border-box; margin: 0; padding: 0; }}

            body {{
                background-color: var(--bg-deep);
                color: #f3f4f6;
                font-family: 'Plus Jakarta Sans', sans-serif;
                overflow-x: hidden;
            }}

            .font-luxury {{ font-family: 'Cinzel', serif; }}

            /* ================= REGAL MONOGRAM INTRO OVERLAY ================= */
            #intro-overlay {{
                position: fixed;
                inset: 0;
                background: radial-gradient(circle at center, #13141b 0%, #000000 100%);
                z-index: 999999;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                pointer-events: all;
                will-change: opacity;
            }}

            .regal-r-path {{
                stroke: #ffffff;
                stroke-width: 4;
                stroke-linecap: round;
                stroke-linejoin: round;
                fill: transparent;
                animation: etchRoyalStroke 2.2s cubic-bezier(0.42, 0, 0.2, 1) forwards;
                filter: drop-shadow(0 0 12px rgba(255, 255, 255, 0.95)) drop-shadow(0 0 25px rgba(229, 184, 105, 0.6));
            }}

            @keyframes etchRoyalStroke {{
                0% {{ stroke-dashoffset: var(--r-length, 750); }}
                100% {{ stroke-dashoffset: 0; }}
            }}

            .regal-r-fill {{
                opacity: 0;
                animation: fillRoyalGold 1.6s cubic-bezier(0.16, 1, 0.3, 1) forwards 2.0s;
            }}

            @keyframes fillRoyalGold {{
                0% {{
                    opacity: 0;
                    transform: scale(0.97);
                    filter: blur(8px);
                }}
                100% {{
                    opacity: 1;
                    transform: scale(1);
                    filter: blur(0px) drop-shadow(0 0 35px rgba(229, 184, 105, 0.95)) drop-shadow(0 0 70px rgba(255, 217, 132, 0.7));
                }}
            }}

            .dust-canvas {{
                position: absolute;
                inset: 0;
                pointer-events: none;
            }}

            .skip-intro-btn {{
                position: absolute;
                top: 24px;
                right: 28px;
                padding: 6px 16px;
                font-size: 11px;
                letter-spacing: 0.15em;
                text-transform: uppercase;
                color: rgba(255, 255, 255, 0.6);
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 9999px;
                cursor: pointer;
                transition: all 0.3s ease;
                z-index: 1000000;
            }}
            .skip-intro-btn:hover {{
                color: #e5b869;
                border-color: #e5b869;
                background: rgba(229, 184, 105, 0.1);
            }}

            .fade-in-up {{
                opacity: 0;
                transform: translateY(28px);
                transition: opacity 0.85s cubic-bezier(0.16, 1, 0.3, 1), transform 0.85s cubic-bezier(0.16, 1, 0.3, 1);
                will-change: opacity, transform;
            }}

            .fade-in-up.appeared {{
                opacity: 1 !important;
                transform: translateY(0) !important;
            }}

            .resin-card {{
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.015));
                backdrop-filter: blur(25px);
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

            .btn-gold:disabled {{
                opacity: 0.5;
                cursor: not-allowed;
                transform: none !important;
                box-shadow: none !important;
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
            <button class="skip-intro-btn" onclick="dismissIntro()">Skip ✕</button>
            <canvas id="dust-canvas" class="dust-canvas"></canvas>
            
            <div class="relative flex flex-col items-center">
                <svg width="240" height="260" viewBox="0 0 220 240" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="goldDustLiquid" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#ffffff" />
                            <stop offset="25%" stop-color="#fff8db" />
                            <stop offset="60%" stop-color="#ffd984" />
                            <stop offset="100%" stop-color="#b88328" />
                        </linearGradient>
                        <filter id="royalGlow" x="-20%" y="-20%" width="140%" height="140%">
                            <feGaussianBlur stdDeviation="3.5" result="blur" />
                            <feComposite in="SourceGraphic" in2="blur" operator="over" />
                        </filter>
                    </defs>

                    <path id="regal-r-path" class="regal-r-path" 
                          d="M 52 205 L 52 42 C 52 38 56 34 68 34 C 118 34 158 46 158 88 C 158 122 128 135 78 135 L 52 135 M 108 135 C 122 152 144 186 166 205 C 176 205 184 198 188 190" />
                    
                    <path class="regal-r-fill" filter="url(#royalGlow)" fill="url(#goldDustLiquid)" 
                          d="M 52 205 L 52 42 C 52 38 56 34 68 34 C 118 34 158 46 158 88 C 158 122 128 135 78 135 L 52 135 M 108 135 C 122 152 144 186 166 205 C 176 205 184 198 188 190" 
                          stroke="url(#goldDustLiquid)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" />
                </svg>

                <span id="intro-caption" class="font-luxury text-xs tracking-[0.45em] uppercase text-amber-200 mt-6 opacity-0 transition-opacity duration-1000">
                    Resins By R • Bespoke
                </span>
            </div>
        </div>

        <div class="ambient-glow top-0 left-[-100px]"></div>
        <div class="ambient-glow bottom-0 right-[-100px]"></div>

        <!-- MAIN STORE VIEW -->
        <div id="page-main">
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
                    Museum-grade bio-resin, metallic mica, botanical inclusions, and real 24k gold leaf foil. Every piece is an unrepeatable bespoke keepsake.
                </p>

                <div class="fade-in-up flex items-center justify-center gap-4">
                    <a href="#products-section" class="btn-gold px-8 py-3.5 rounded-full inline-flex items-center gap-3 text-xs tracking-widest uppercase">
                        <span>Explore Catalog</span>
                        <i class="ph ph-arrow-down text-sm"></i>
                    </a>
                    <button onclick="showPage('policy')" class="btn-glass px-7 py-3.5 rounded-full text-xs tracking-widest uppercase text-gray-300">
                        Policies
                    </button>
                </div>
            </section>

            <!-- Product Grid -->
            <main id="products-section" class="max-w-7xl mx-auto px-6 py-12 relative z-10">
                <div class="flex flex-col md:flex-row md:items-end justify-between mb-12 border-b border-white/10 pb-6">
                    <div>
                        <h2 class="fade-in-up font-luxury text-3xl tracking-wide text-white">Signature Collection</h2>
                        <p class="fade-in-up text-gray-400 text-sm mt-1">Select choices, personalize colors, and upload cherished memories.</p>
                    </div>
                    <div class="fade-in-up mt-4 md:mt-0 text-amber-300 font-mono text-xs tracking-widest uppercase">
                        Flat Delivery: PKR 500/- Nationwide
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-8 lg:gap-10">
                    
                    <!-- 1. Resin Ring -->
                    <div class="resin-card rounded-3xl p-6 flex flex-col justify-between">
                        <div>
                            <div class="fade-in-up relative h-64 sm:h-72 w-full rounded-2xl overflow-hidden mb-6 group">
                                <img src="{IMG_PRODUCT_1}" 
                                     alt="Resin Ring" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105">
                                <span class="absolute top-4 left-4 px-3 py-1 bg-black/60 backdrop-blur-md border border-white/10 rounded-full text-xs uppercase tracking-wider text-amber-300">Jewelry</span>
                            </div>
                            <div class="flex justify-between items-baseline mb-2">
                                <h3 class="fade-in-up font-luxury text-2xl text-white">Resin Ring</h3>
                                <span class="fade-in-up text-xl font-bold text-amber-300">PKR 800/-</span>
                            </div>
                            <p class="fade-in-up text-gray-400 text-sm mb-6">Polished glass-like epoxy ring infused with golden flakes and crystalline botanicals.</p>
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

                    <!-- 2. Resin Shield 6-Inch -->
                    <div class="resin-card rounded-3xl p-6 flex flex-col justify-between">
                        <div>
                            <div class="fade-in-up relative h-64 sm:h-72 w-full rounded-2xl overflow-hidden mb-6 group">
                                <img src="{IMG_PRODUCT_2}" 
                                     alt="Resin Shield" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105">
                                <span class="absolute top-4 left-4 px-3 py-1 bg-black/60 backdrop-blur-md border border-white/10 rounded-full text-xs uppercase tracking-wider text-amber-300">Keepsake</span>
                            </div>
                            <div class="flex justify-between items-baseline mb-2">
                                <h3 class="fade-in-up font-luxury text-2xl text-white">Resins Shield (6-Inch)</h3>
                                <span id="shield-price-display" class="fade-in-up text-xl font-bold text-amber-300">PKR 2,000/-</span>
                            </div>
                            <p class="fade-in-up text-gray-400 text-sm mb-4">6-inch solid resin plaque. Base price PKR 2,000/- with an option to embed up to 3 pictures (+PKR 100/- each).</p>
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
                                <div id="shield-uploader-box" class="hidden pt-3 border-t border-white/10">
                                    <label class="block text-xs uppercase tracking-wider text-amber-300 font-semibold mb-1">Upload Shield Pictures (Max 5MB each):</label>
                                    <input type="file" id="shield-file-input" multiple accept="image/jpeg,image/png,image/webp" onchange="handleSecureShieldFiles(this)" 
                                           class="w-full text-xs text-gray-400 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-amber-300/10 file:text-amber-300 hover:file:bg-amber-300/20 cursor-pointer">
                                    <p id="shield-files-status" class="text-[11px] text-gray-400 mt-1">Accepts verified JPEG, PNG, or WebP.</p>
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

                    <!-- 3. Resin 3D Chess Keychains -->
                    <div class="resin-card rounded-3xl p-6 flex flex-col justify-between">
                        <div>
                            <div class="fade-in-up relative h-64 sm:h-72 w-full rounded-2xl overflow-hidden mb-6 group">
                                <img src="{IMG_PRODUCT_3}" 
                                     alt="3D Chess Keychains" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105">
                                <span class="absolute top-4 left-4 px-3 py-1 bg-black/60 backdrop-blur-md border border-white/10 rounded-full text-xs uppercase tracking-wider text-amber-300">Collectibles</span>
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

                    <!-- 4. Resin Tray and Coaster Set -->
                    <div class="resin-card rounded-3xl p-6 flex flex-col justify-between">
                        <div>
                            <div class="fade-in-up relative h-64 sm:h-72 w-full rounded-2xl overflow-hidden mb-6 group">
                                <img src="{IMG_PRODUCT_4}" 
                                     alt="Tray & Coaster Set" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105">
                                <span class="absolute top-4 left-4 px-3 py-1 bg-black/60 backdrop-blur-md border border-white/10 rounded-full text-xs uppercase tracking-wider text-amber-300">Home Decor</span>
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

            <!-- Footer -->
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

        <!-- POLICY PAGE -->
        <div id="page-policy" class="hidden min-h-screen pt-12 pb-24 px-6 max-w-4xl mx-auto relative z-10">
            <button onclick="showPage('main')" class="mb-8 btn-glass px-5 py-2.5 rounded-full text-xs uppercase tracking-widest text-amber-300 flex items-center gap-2">
                <i class="ph ph-arrow-left"></i> Return to Store
            </button>
            <div class="resin-card p-8 md:p-12 rounded-3xl border border-white/10">
                <h1 class="font-luxury text-3xl md:text-4xl text-white mb-2">Studio Policies</h1>
                <p class="text-xs uppercase tracking-widest text-amber-300 mb-8 font-semibold">Terms of Artistry, Crafting & Deliveries</p>
                <div class="space-y-6 text-sm text-gray-300 leading-relaxed">
                    <div>
                        <h2 class="text-base font-semibold text-white flex items-center gap-2"><span class="text-amber-300">1.</span> Bespoke No-Return Policy</h2>
                        <p class="mt-1 text-gray-400">Every single product is custom-poured and personalized according to your selected dimensions, color palette, and design notes. As these are irreversible bespoke commissions, we do not accept returns or refunds.</p>
                    </div>
                    <div>
                        <h2 class="text-base font-semibold text-white flex items-center gap-2"><span class="text-amber-300">2.</span> Organic Micro-Bubbles & Human Touch</h2>
                        <p class="mt-1 text-gray-400">Resin curing is an organic thermodynamic chemical process. While we vacuum-degas and torch our pours to maintain museum-grade clarity, minor micro-bubbles or microscopic variations may occur. These are natural characteristics of hand-poured epoxy craftsmanship.</p>
                    </div>
                    <div>
                        <h2 class="text-base font-semibold text-white flex items-center gap-2"><span class="text-amber-300">3.</span> Order Finality After Confirmation</h2>
                        <p class="mt-1 text-gray-400">Once your order and specifications have been confirmed by our seller via WhatsApp, the casting and pigment curation begins immediately. Orders cannot be canceled or modified after this confirmation point.</p>
                    </div>
                    <div>
                        <h2 class="text-base font-semibold text-white flex items-center gap-2"><span class="text-amber-300">4.</span> 100% Advance Payment Solemnity</h2>
                        <p class="mt-1 text-gray-400">Because every artifact is customized, 100% advance payment via JazzCash or Raast ID (0305-8866692 - Ramsha Fatima) is required to validate your commitment and initiate pouring.</p>
                    </div>
                    <div>
                        <h2 class="text-base font-semibold text-white flex items-center gap-2"><span class="text-amber-300">5.</span> 3–7 Days Curing & Hardening Protocol</h2>
                        <p class="mt-1 text-gray-400">High-grade bio-resin requires between 72 to 168 hours to fully cross-link and cure to rock-solid barcol hardness. Dispatching resin before full chemical cure causes heat warping and transit distortion. Please allow 3–7 business days before dispatch.</p>
                    </div>
                    <div>
                        <h2 class="text-base font-semibold text-white flex items-center gap-2"><span class="text-amber-300">6.</span> Heirloom Resin Care</h2>
                        <p class="mt-1 text-gray-400">Keep out of direct, prolonged outdoor sunlight. Clean only with a gentle microfiber towel and mild soapy water. Never use harsh abrasive chemicals or high-heat dishwashers.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- 404 PAGE -->
        <div id="page-404" class="hidden min-h-screen flex items-center justify-center px-6 relative z-10 text-center">
            <div class="resin-card p-10 md:p-14 rounded-3xl max-w-lg border border-white/10">
                <span class="font-luxury text-7xl font-bold text-amber-300/80 block mb-2">404</span>
                <h2 class="font-luxury text-2xl text-white mb-3">Resin Void: Piece Unfound</h2>
                <p class="text-xs text-gray-400 leading-relaxed mb-6">The artifact or chamber you are looking for has not materialized or was wiped from our casting inventory.</p>
                <button onclick="showPage('main')" class="btn-gold px-8 py-3 rounded-full text-xs uppercase tracking-widest font-bold">
                    Return to Studio Catalog
                </button>
            </div>
        </div>

        <!-- CART DRAWER -->
        <div id="cart-drawer-backdrop" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden" onclick="toggleCartDrawer(false)"></div>
        <aside id="cart-drawer" class="fixed top-0 right-0 h-full w-full max-w-md bg-[#0a0b0e] border-l border-white/10 z-50 translate-x-full transition-transform duration-500 ease-in-out flex flex-col justify-between shadow-2xl">
            <div class="p-6 border-b border-white/10 flex items-center justify-between">
                <div class="flex items-center gap-3">
                    <i class="ph ph-handbag text-amber-300 text-2xl"></i>
                    <h3 class="font-luxury text-xl text-white tracking-wide">Your Resin Bag</h3>
                </div>
                <button onclick="toggleCartDrawer(false)" class="text-gray-400 hover:text-white text-2xl p-1">&times;</button>
            </div>
            <div id="cart-items-container" class="p-6 overflow-y-auto space-y-4 flex-grow"></div>
            <div class="p-6 border-t border-white/10 bg-black/50 space-y-3">
                <div class="flex justify-between text-sm text-gray-400"><span>Sub-Total</span><span id="cart-subtotal" class="font-mono text-white">PKR 0/-</span></div>
                <div class="flex justify-between text-sm text-gray-400"><span>Delivery Charges</span><span class="font-mono text-white">PKR 500/-</span></div>
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

                <div class="p-4 rounded-2xl bg-white/[0.03] border border-white/10 mb-6 space-y-2">
                    <div class="flex justify-between text-xs text-gray-300"><span>Selected Artifacts:</span><span id="modal-item-summary" class="font-medium text-right text-white"></span></div>
                    <div class="flex justify-between text-xs text-gray-400"><span>Sub-Total:</span><span id="modal-subtotal" class="font-mono text-white">PKR 0/-</span></div>
                    <div class="flex justify-between text-xs text-gray-400"><span>Delivery Charges:</span><span class="font-mono text-white">PKR 500/-</span></div>
                    <div class="flex justify-between text-sm font-bold text-amber-300 pt-2 border-t border-white/5">
                        <span>Total Amount Payable:</span><span id="modal-total" class="font-mono text-base">PKR 0/-</span>
                    </div>
                </div>

                <div class="p-3.5 rounded-xl bg-amber-400/10 border border-amber-300/30 mb-5 text-xs text-amber-200">
                    <div class="font-bold flex items-center gap-1.5 mb-0.5"><i class="ph ph-wallet text-sm"></i> JazzCash / Raast Payment Details:</div>
                    <div>Account Number: <strong class="text-white font-mono">0305-8866692</strong></div>
                    <div>Account Title: <strong class="text-white">Ramsha Fatima</strong></div>
                </div>

                <form id="order-form" onsubmit="submitClientOrder(event)" class="space-y-4 text-left">
                    <div>
                        <label class="block text-xs uppercase tracking-wider text-gray-300 font-semibold mb-1">1. Full Name <span class="text-amber-400">*</span></label>
                        <input type="text" id="cust-name" required maxlength="80" placeholder="Your full name" class="w-full px-4 py-3 bg-white/5 border border-white/15 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-amber-300">
                    </div>
                    <div>
                        <label class="block text-xs uppercase tracking-wider text-gray-300 font-semibold mb-1">2. Email Address <span class="text-amber-400">*</span></label>
                        <input type="email" id="cust-email" required maxlength="100" placeholder="name@example.com" class="w-full px-4 py-3 bg-white/5 border border-white/15 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-amber-300">
                    </div>
                    <div>
                        <label class="block text-xs uppercase tracking-wider text-gray-300 font-semibold mb-1">3. Phone Number <span class="text-amber-400">*</span></label>
                        <input type="tel" id="cust-phone" required maxlength="25" placeholder="0300 1234567" class="w-full px-4 py-3 bg-white/5 border border-white/15 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-amber-300">
                    </div>
                    <div>
                        <label class="block text-xs uppercase tracking-wider text-gray-300 font-semibold mb-1">4. Full Address <span class="text-amber-400">*</span></label>
                        <textarea id="cust-address" required maxlength="300" rows="2" placeholder="House/Flat #, Street address, Area, City" class="w-full px-4 py-3 bg-white/5 border border-white/15 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-amber-300"></textarea>
                    </div>
                    <div>
                        <label class="block text-xs uppercase tracking-wider text-gray-300 font-semibold mb-1">5. TID (Transaction ID) For Payment Made <span class="text-amber-400">*</span></label>
                        <input type="text" id="cust-tid" required maxlength="40" placeholder="Transaction ID (JazzCash / Raast)" class="w-full px-4 py-3 bg-white/5 border border-white/15 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-amber-300 font-mono">
                    </div>
                    <div>
                        <label class="block text-xs uppercase tracking-wider text-amber-300 font-semibold mb-1">6. Upload Screenshot of Payment Made (Max 5MB) <span class="text-amber-400">*</span></label>
                        <input type="file" id="cust-payment-screenshot" required accept="image/jpeg,image/png,image/webp" 
                               class="w-full text-xs text-gray-400 file:mr-3 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-amber-300 file:text-black hover:file:bg-amber-400 cursor-pointer">
                    </div>
                    <div>
                        <label class="block text-xs uppercase tracking-wider text-gray-300 font-semibold mb-1">Customization Notes (Colours, Foil, or Styling)</label>
                        <textarea id="cust-notes" maxlength="400" rows="2" placeholder="Describe chosen color tones, glitter, or custom details." class="w-full px-4 py-3 bg-white/5 border border-white/15 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-amber-300"></textarea>
                    </div>
                    <button type="submit" id="submit-btn" class="btn-gold w-full py-4 rounded-xl text-xs uppercase tracking-widest font-bold mt-2 shadow-xl flex items-center justify-center gap-2">
                        <span>Submit & Generate Order ID</span>
                    </button>
                </form>
            </div>
        </div>

        <!-- SUCCESS CONFIRMATION MODAL -->
        <div id="success-modal" class="fixed inset-0 bg-black/90 backdrop-blur-md z-50 hidden flex items-center justify-center p-4">
            <div class="resin-card bg-[#0e0f14] w-full max-w-lg rounded-3xl border border-amber-300/40 p-8 text-center shadow-2xl relative">
                <div class="w-16 h-16 mx-auto mb-4 rounded-full border border-amber-300/60 bg-amber-300/10 flex items-center justify-center">
                    <i class="ph ph-check text-amber-300 text-3xl"></i>
                </div>
                <span class="text-xs uppercase tracking-widest text-amber-300 font-semibold">Commission Received</span>
                <h3 class="font-luxury text-2xl text-white mt-1 mb-2">Order Confirmed!</h3>
                <p class="text-xs text-gray-400 mb-6">Your order has been saved to our studio database. Quote your Order ID below:</p>
                <div class="p-4 rounded-2xl bg-white/[0.04] border border-amber-300/30 mb-6">
                    <span class="text-xs text-gray-400 block mb-1">Unique Order ID</span>
                    <span id="confirmed-order-id" class="font-mono text-2xl font-bold text-amber-300 tracking-wider">RBR-00000</span>
                </div>
                <a id="whatsapp-order-link" href="#" target="_blank" class="btn-gold w-full py-4 rounded-xl text-xs uppercase tracking-widest font-bold flex items-center justify-center gap-2 mb-3">
                    <i class="ph ph-whatsapp-logo text-lg"></i>
                    <span>Confirm on WhatsApp (0305-8866692)</span>
                </a>
                <button onclick="closeSuccessModal()" class="text-xs text-gray-400 hover:text-white uppercase tracking-wider py-2">
                    Close & Return to Studio
                </button>
            </div>
        </div>

        <div id="toast" class="fixed bottom-6 left-1/2 -translate-x-1/2 bg-[#101115] border border-amber-300/50 text-white px-6 py-3 rounded-full text-xs uppercase tracking-widest shadow-2xl opacity-0 pointer-events-none transition-all duration-300 z-50 flex items-center gap-2">
            <i class="ph ph-sparkle text-amber-300 text-base"></i>
            <span id="toast-msg">Item added to cart</span>
        </div>

        <script>
            const DISCORD_WEBHOOK_URL = "{DISCORD_WEBHOOK_URL}".trim();
            const GSHEET_URL = "{GSHEET_URL}".trim();
            const SELLER_WHATSAPP = "923058866692";
            const DELIVERY_FEE = 500;
            const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB hard limit
            const SUBMIT_COOLDOWN_SECONDS = 60;

            let cart = [];
            let selectedRingSize = 'US 5';
            let shieldPhotosCount = 0;
            let shieldUploadedBlobs = [];
            let quickOrderItem = null;
            let introDismissed = false;

            // ================= PRECISE INTRO ANIMATION TIMELINE =================
            function setupExactIntroAnimation() {{
                const path = document.getElementById('regal-r-path');
                if (path) {{
                    const totalLength = path.getTotalLength();
                    path.style.setProperty('--r-length', totalLength);
                    path.style.strokeDasharray = totalLength;
                    path.style.strokeDashoffset = totalLength;
                }}

                setTimeout(() => {{
                    if (!introDismissed) {{
                        const cap = document.getElementById('intro-caption');
                        if (cap) cap.style.opacity = '1';
                    }}
                }}, 4200);

                setTimeout(() => {{
                    if (!introDismissed) {{
                        dismissIntro();
                    }}
                }}, 5800);
            }}

            function dismissIntro() {{
                if (introDismissed) return;
                introDismissed = true;
                const intro = document.getElementById('intro-overlay');
                if (intro) {{
                    intro.style.transition = 'opacity 1.4s cubic-bezier(0.4, 0, 0.2, 1)';
                    intro.style.opacity = '0';
                    intro.addEventListener('transitionend', () => {{
                        intro.style.display = 'none';
                        initScrollObserver();
                    }}, {{ once: true }});
                }}
            }}

            // Dust canvas
            const canvas = document.getElementById('dust-canvas');
            const ctx = canvas.getContext('2d');
            let particles = [];
            function resizeCanvas() {{ canvas.width = window.innerWidth; canvas.height = window.innerHeight; }}
            resizeCanvas();
            window.addEventListener('resize', resizeCanvas);

            for(let i=0; i<60; i++) {{
                particles.push({{
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    radius: Math.random() * 2.2 + 0.6,
                    color: Math.random() > 0.4 ? '#e5b869' : '#ffffff',
                    vy: -Math.random() * 0.8 - 0.2,
                    vx: (Math.random() - 0.5) * 0.5,
                    alpha: Math.random() * 0.8 + 0.2
                }});
            }}

            function animateDust() {{
                if (introDismissed) return;
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                particles.forEach(p => {{
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                    ctx.fillStyle = p.color;
                    ctx.globalAlpha = p.alpha;
                    ctx.shadowBlur = 6;
                    ctx.shadowColor = p.color;
                    ctx.fill();
                    p.y += p.vy; p.x += p.vx;
                    if(p.y < 0) p.y = canvas.height;
                    if(p.x < 0) p.x = canvas.width;
                    if(p.x > canvas.width) p.x = 0;
                }});
                requestAnimationFrame(animateDust);
            }}

            setupExactIntroAnimation();
            animateDust();

            // ================= FILE INTEGRITY & ANTI-MALWARE VERIFICATION =================
            function verifyMagicBytes(file) {{
                return new Promise((resolve) => {{
                    const reader = new FileReader();
                    reader.onloadend = function(e) {{
                        const arr = (new Uint8Array(e.target.result)).subarray(0, 4);
                        let header = "";
                        for (let i = 0; i < arr.length; i++) {{
                            header += arr[i].toString(16).toUpperCase();
                        }}
                        const isJPEG = header.startsWith("FFD8FF");
                        const isPNG = header.startsWith("89504E47");
                        const isWEBP = header.startsWith("52494646");
                        resolve(isJPEG || isPNG || isWEBP);
                    }};
                    reader.readAsArrayBuffer(file.slice(0, 4));
                }});
            }}

            function sanitizeAndCompressImage(file) {{
                return new Promise((resolve, reject) => {{
                    const img = new Image();
                    const objectUrl = URL.createObjectURL(file);
                    img.onload = () => {{
                        URL.revokeObjectURL(objectUrl);
                        // Pixel-bomb guard: reject absurd dimension bombs
                        if (img.naturalWidth > 5000 || img.naturalHeight > 5000) {{
                            reject(new Error("Image dimensions exceed 5000px safety limit"));
                            return;
                        }}
                        const cvs = document.createElement('canvas');
                        const maxDim = 1800;
                        let w = img.width;
                        let h = img.height;
                        if (w > maxDim || h > maxDim) {{
                            if (w > h) {{ h = Math.round((h * maxDim) / w); w = maxDim; }}
                            else {{ w = Math.round((w * maxDim) / h); h = maxDim; }}
                        }}
                        cvs.width = w;
                        cvs.height = h;
                        const c2d = cvs.getContext('2d');
                        c2d.drawImage(img, 0, 0, w, h);
                        cvs.toBlob((blob) => {{
                            resolve(blob);
                        }}, 'image/jpeg', 0.88);
                    }};
                    img.onerror = () => {{
                        URL.revokeObjectURL(objectUrl);
                        reject(new Error("Image stream decode failure"));
                    }};
                    img.src = objectUrl;
                }});
            }}

            async function handleSecureShieldFiles(input) {{
                const files = Array.from(input.files);
                if (files.length > 3) {{
                    alert("Max 3 pictures allowed.");
                    input.value = ""; shieldUploadedBlobs = [];
                    return;
                }}
                shieldUploadedBlobs = [];
                for (const f of files) {{
                    if (f.size > MAX_FILE_SIZE) {{
                        alert(`File "${{f.name}}" exceeds 5MB limit.`);
                        input.value = ""; shieldUploadedBlobs = [];
                        return;
                    }}
                    const isValidFormat = await verifyMagicBytes(f);
                    if (!isValidFormat) {{
                        alert(`File "${{f.name}}" failed binary validation. Only verified JPEG, PNG, or WebP images are permitted.`);
                        input.value = ""; shieldUploadedBlobs = [];
                        return;
                    }}
                    try {{
                        const cleanBlob = await sanitizeAndCompressImage(f);
                        shieldUploadedBlobs.push({{ name: f.name, blob: cleanBlob }});
                    }} catch(e) {{
                        alert(`Error validating ${{f.name}}: ${{e.message}}`);
                        input.value = ""; shieldUploadedBlobs = [];
                        return;
                    }}
                }}
                document.getElementById('shield-files-status').textContent = `${{shieldUploadedBlobs.length}} verified file(s) attached.`;
            }}

            function initScrollObserver() {{
                const elements = document.querySelectorAll('.fade-in-up');
                const observer = new IntersectionObserver((entries) => {{
                    entries.forEach((entry, idx) => {{
                        if (entry.isIntersecting) {{
                            setTimeout(() => {{ entry.target.classList.add('appeared'); }}, idx * 55);
                            observer.unobserve(entry.target);
                        }}
                    }});
                }}, {{ threshold: 0.1 }});
                elements.forEach(el => observer.observe(el));
            }}

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

            function selectRingSize(btn, size) {{
                document.querySelectorAll('#ring-sizes .size-btn').forEach(b => {{
                    b.className = 'size-btn px-3.5 py-1.5 rounded-lg border border-white/10 text-xs text-gray-300 hover:border-amber-300 transition';
                }});
                btn.className = 'size-btn px-3.5 py-1.5 rounded-lg border border-amber-300 text-xs text-amber-300 bg-amber-300/10 transition';
                selectedRingSize = size;
            }}

            function adjustPhotos(delta) {{
                shieldPhotosCount = Math.max(0, Math.min(3, shieldPhotosCount + delta));
                document.getElementById('shield-photo-count').textContent = shieldPhotosCount;
                const total = 2000 + (shieldPhotosCount * 100);
                document.getElementById('shield-price-display').textContent = `PKR ${{total.toLocaleString()}}/-`;
                document.getElementById('shield-photo-status').textContent = `${{shieldPhotosCount}} picture(s) (+PKR ${{shieldPhotosCount * 100}}/-)`;
                const uploader = document.getElementById('shield-uploader-box');
                if (shieldPhotosCount > 0) {{ uploader.classList.remove('hidden'); }}
                else {{ uploader.classList.add('hidden'); shieldUploadedBlobs = []; }}
            }}

            function generateUniqueOrderId() {{
                return `RBR-${{Math.floor(10000 + Math.random() * 90000)}}`;
            }}

            // Neutralize Google Sheets Formula Injection (=, +, -, @)
            function sanitizeForSheet(str) {{
                const s = String(str || '').trim();
                if (s.startsWith('=') || s.startsWith('+') || s.startsWith('-') || s.startsWith('@')) {{
                    return "'" + s;
                }}
                return s;
            }}

            function getProductSpecs(id) {{
                if (id === 'resin-ring') return {{ id, name: `Resin Ring (${{selectedRingSize}})`, spec: `Size: ${{selectedRingSize}}`, price: 800, qty: 1 }};
                if (id === 'resin-shield') {{
                    const total = 2000 + (shieldPhotosCount * 100);
                    return {{ id, name: 'Resins Shield (6-Inch)', spec: shieldPhotosCount > 0 ? `${{shieldPhotosCount}} custom picture(s)` : 'No pictures', price: total, qty: 1 }};
                }}
                if (id === 'chess-keychain') return {{ id, name: 'Resin 3D Chess Keychain', spec: 'Sculpted Piece', price: 500, qty: 1 }};
                if (id === 'tray-coaster-set') return {{ id, name: 'Resin Tray & Coaster Set', spec: '1 Tray + 4 Coasters', price: 4000, qty: 1 }};
            }}

            function handleAddToCart(id) {{
                const item = getProductSpecs(id);
                const exists = cart.find(i => i.name === item.name && i.spec === item.spec);
                if (exists) exists.qty += 1; else cart.push(item);
                renderCart();
                showToast(`"${{item.name}}" added to cart`);
            }}

            function handleQuickOrder(id) {{
                quickOrderItem = getProductSpecs(id);
                openCheckoutModal([quickOrderItem]);
            }}

            function renderCart() {{
                const list = document.getElementById('cart-items-container');
                document.getElementById('nav-cart-count').textContent = cart.reduce((a, c) => a + c.qty, 0);
                if (cart.length === 0) {{
                    list.innerHTML = `<div class="h-64 flex flex-col items-center justify-center text-gray-500 text-sm">Your bag is empty.</div>`;
                    document.getElementById('cart-subtotal').textContent = 'PKR 0/-';
                    document.getElementById('cart-grandtotal').textContent = `PKR ${{DELIVERY_FEE}}/-`;
                    return;
                }}
                let sub = 0; let html = '';
                cart.forEach((item, idx) => {{
                    const cost = item.price * item.qty; sub += cost;
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
                document.getElementById('cart-subtotal').textContent = `PKR ${{sub.toLocaleString()}}/-`;
                document.getElementById('cart-grandtotal').textContent = `PKR ${{(sub + DELIVERY_FEE).toLocaleString()}}/-`;
            }}

            function removeCartItem(idx) {{ cart.splice(idx, 1); renderCart(); }}

            function toggleCartDrawer(open) {{
                const drawer = document.getElementById('cart-drawer');
                const backdrop = document.getElementById('cart-drawer-backdrop');
                if (open) {{ backdrop.classList.remove('hidden'); setTimeout(() => drawer.classList.remove('translate-x-full'), 10); }}
                else {{ drawer.classList.add('translate-x-full'); setTimeout(() => backdrop.classList.add('hidden'), 300); }}
            }}

            function proceedToCheckoutFromCart() {{
                if (cart.length === 0) {{ showToast("Your cart is empty"); return; }}
                toggleCartDrawer(false); quickOrderItem = null; openCheckoutModal(cart);
            }}

            function openCheckoutModal(items) {{
                const sub = items.reduce((a, c) => a + (c.price * c.qty), 0);
                document.getElementById('modal-item-summary').textContent = items.map(i => `${{i.name}} (x${{i.qty}})`).join(', ');
                document.getElementById('modal-subtotal').textContent = `PKR ${{sub.toLocaleString()}}/-`;
                document.getElementById('modal-total').textContent = `PKR ${{(sub + DELIVERY_FEE).toLocaleString()}}/-`;
                toggleCheckoutModal(true);
            }}

            function toggleCheckoutModal(open) {{
                const m = document.getElementById('checkout-modal');
                if (open) m.classList.remove('hidden'); else m.classList.add('hidden');
            }}

            function showToast(msg) {{
                const t = document.getElementById('toast');
                document.getElementById('toast-msg').textContent = msg;
                t.classList.remove('opacity-0', 'pointer-events-none');
                setTimeout(() => t.classList.add('opacity-0', 'pointer-events-none'), 3000);
            }}

            // ================= ZERO-TRUST SUBMISSION WORKFLOW =================
            async function submitClientOrder(e) {{
                e.preventDefault();

                // 1. Client-Side Rate Limiter
                const lastOrderTime = localStorage.getItem('rbr_last_order_ts');
                const now = Math.floor(Date.now() / 1000);
                if (lastOrderTime && (now - parseInt(lastOrderTime)) < SUBMIT_COOLDOWN_SECONDS) {{
                    const remaining = SUBMIT_COOLDOWN_SECONDS - (now - parseInt(lastOrderTime));
                    alert(`Studio Queue Cooldown:\\nPlease wait ${{remaining}}s before submitting another order.`);
                    return;
                }}

                const fullName = document.getElementById('cust-name').value.trim();
                const email = document.getElementById('cust-email').value.trim();
                const phone = document.getElementById('cust-phone').value.trim();
                const address = document.getElementById('cust-address').value.trim();
                const tid = document.getElementById('cust-tid').value.trim();
                const notes = document.getElementById('cust-notes').value.trim() || 'No customization notes';

                // Strict Regex Validations
                const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{{2,}}$/;
                if (!emailRegex.test(email)) {{
                    alert("Please enter a valid email address."); return;
                }}
                const phoneRegex = /^[0-9+\-\s()]{{10,20}}$/;
                if (!phoneRegex.test(phone)) {{
                    alert("Please enter a valid phone number (digits and standard formatting only)."); return;
                }}
                const tidRegex = /^[a-zA-Z0-9\-_]{{4,40}}$/;
                if (!tidRegex.test(tid)) {{
                    alert("Please enter a valid Payment TID (alphanumeric characters, dashes, or underscores only)."); return;
                }}

                const screenshotInput = document.getElementById('cust-payment-screenshot');
                if (!screenshotInput.files || screenshotInput.files.length === 0) {{
                    alert("Please attach screenshot of payment made."); return;
                }}
                const rawScreenshot = screenshotInput.files[0];
                if (rawScreenshot.size > MAX_FILE_SIZE) {{
                    alert("Screenshot exceeds 5MB size limit."); return;
                }}

                const isValidScreenshot = await verifyMagicBytes(rawScreenshot);
                if (!isValidScreenshot) {{
                    alert("Suspicious or invalid payment screenshot file detected. Upload rejected.");
                    screenshotInput.value = "";
                    return;
                }}

                const btn = document.getElementById('submit-btn');
                btn.disabled = true;
                btn.innerHTML = `<span class="animate-pulse">Verifying & Curating...</span>`;

                let cleanScreenshotBlob;
                try {{
                    cleanScreenshotBlob = await sanitizeAndCompressImage(rawScreenshot);
                }} catch(err) {{
                    alert(`Payment screenshot validation failure: ${{err.message}}`);
                    btn.disabled = false;
                    btn.innerHTML = `<span>Submit & Generate Order ID</span>`;
                    return;
                }}

                const orderId = generateUniqueOrderId();
                const activeItems = quickOrderItem ? [quickOrderItem] : cart;
                const subtotal = activeItems.reduce((a, c) => a + (c.price * c.qty), 0);
                const grandTotal = subtotal + DELIVERY_FEE;
                const productsListString = activeItems.map(i => `${{i.name}} (x${{i.qty}})`).join(', ');

                // 2. Dispatch to Google Sheet with Formula Injection Shields
                if (GSHEET_URL && GSHEET_URL.startsWith('http')) {{
                    try {{
                        const gsheetPayload = JSON.stringify({{
                            action: "add_order",
                            name: sanitizeForSheet(fullName),
                            address: sanitizeForSheet(address),
                            products: sanitizeForSheet(productsListString),
                            customization: sanitizeForSheet(notes),
                            email: sanitizeForSheet(email),
                            order_id: sanitizeForSheet(orderId)
                        }});

                        await fetch(GSHEET_URL, {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'text/plain;charset=utf-8' }},
                            body: gsheetPayload
                        }});
                    }} catch (err) {{
                        console.warn("Direct Sheet push note:", err);
                    }}
                }}

                // 3. Dispatch to Discord Webhook with @everyone Exploit Shield
                if (DISCORD_WEBHOOK_URL && DISCORD_WEBHOOK_URL.startsWith('http')) {{
                    const formData = new FormData();
                    const embedPayload = {{
                        title: `New Order: ${{orderId}}`,
                        color: 15054953,
                        fields: [
                            {{ name: "Order ID", value: orderId, inline: true }},
                            {{ name: "Client Name", value: fullName, inline: true }},
                            {{ name: "Email", value: email, inline: true }},
                            {{ name: "Phone", value: phone, inline: true }},
                            {{ name: "Delivery Address", value: address, inline: false }},
                            {{ name: "Payment TID", value: tid, inline: true }},
                            {{ name: "Payment Account", value: "0305-8866692 (Ramsha Fatima)", inline: true }},
                            {{ name: "Products Ordered", value: productsListString, inline: false }},
                            {{ name: "Total Amount", value: `PKR ${{grandTotal}}/-`, inline: true }},
                            {{ name: "Custom Notes", value: notes, inline: false }}
                        ],
                        footer: {{ text: "Resins by R • Zero-Trust Pipeline" }},
                        timestamp: new Date().toISOString()
                    }};

                    // allowed_mentions: { parse: [] } prevents @everyone / @here / mass pings
                    formData.append("payload_json", JSON.stringify({{
                        content: `**New Order Received from ${{fullName.replace(/@/g, '')}}** | Order ID: \`${{orderId}}\``,
                        embeds: [embedPayload],
                        allowed_mentions: {{ parse: [] }}
                    }}));
                    formData.append("files[0]", cleanScreenshotBlob, `Sanitized_Payment_TID_${{tid}}.jpg`);
                    
                    let fIdx = 1;
                    shieldUploadedBlobs.forEach(item => {{
                        formData.append(`files[${{fIdx}}]`, item.blob, `Sanitized_Shield_${{fIdx}}.jpg`);
                        fIdx++;
                    }});

                    try {{
                        await fetch(DISCORD_WEBHOOK_URL, {{ method: 'POST', body: formData }});
                    }} catch (err) {{
                        console.warn("Discord Webhook dispatch note:", err);
                    }}
                }}

                localStorage.setItem('rbr_last_order_ts', Math.floor(Date.now() / 1000).toString());

                const prewrittenMsg = `Assalamo-alaikum, I had ordered ${{productsListString}} under the order ID ${{orderId}}, can I get a confirmation on it?`;
                const waUrl = `https://wa.me/${{SELLER_WHATSAPP}}?text=${{encodeURIComponent(prewrittenMsg)}}`;
                document.getElementById('confirmed-order-id').textContent = orderId;
                document.getElementById('whatsapp-order-link').href = waUrl;

                toggleCheckoutModal(false);
                document.getElementById('success-modal').classList.remove('hidden');
                cart = []; quickOrderItem = null; renderCart();
                document.getElementById('order-form').reset();
                shieldUploadedBlobs = [];
                document.getElementById('shield-uploader-box').classList.add('hidden');
                document.getElementById('shield-photo-count').textContent = "0";

                btn.disabled = false;
                btn.innerHTML = `<span>Submit & Generate Order ID</span>`;
            }}

            function closeSuccessModal() {{ document.getElementById('success-modal').classList.add('hidden'); }}
            renderCart();
        </script>
    </body>
    </html>
    """
    components.html(HTML_TEMPLATE, height=1000, scrolling=True)

# ================= SECURED OWNER ADMIN DASHBOARD =================
def admin_view():
    st.title("Resins by R • Owner Admin Portal")
    st.caption("PENDING ORDERS FULFILLMENT & DISPATCH QUEUE")

    now = time.time()

    # 1. Brute-Force Lockout Guard
    if now < st.session_state["admin_locked_until"]:
        lock_remaining = int(st.session_state["admin_locked_until"] - now)
        st.error(f"Security Alert: Maximum login attempts exceeded. Portal locked for {lock_remaining} seconds.")
        return

    # 2. Timing-Attack Proof Authentication (Zero unsafe_allow_html)
    if not st.session_state["admin_authenticated"]:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.container(border=True):
                st.subheader("Owner Authentication")
                user_input = st.text_input("Admin Username", key="login_user")
                pass_input = st.text_input("Admin Password", type="password", key="login_pass")
                if st.button("Unlock Admin Dashboard", use_container_width=True):
                    valid_user = hmac.compare_digest(user_input.strip(), ADMIN_NAME)
                    valid_pass = hmac.compare_digest(pass_input.strip(), ADMIN_PASS)
                    if valid_user and valid_pass:
                        st.session_state["admin_authenticated"] = True
                        st.session_state["admin_failed_attempts"] = 0
                        st.rerun()
                    else:
                        st.session_state["admin_failed_attempts"] += 1
                        if st.session_state["admin_failed_attempts"] >= 5:
                            st.session_state["admin_locked_until"] = now + 900  # 15-minute lockout
                            st.error("Too many failed attempts. Admin locked for 15 minutes.")
                        else:
                            st.error(f"Invalid credentials. Attempt {st.session_state['admin_failed_attempts']} of 5.")
        return

    # 3. Authenticated Dashboard Header
    col_l, col_m, col_r = st.columns([4, 2, 1])
    with col_l:
        st.write(f"Logged in as: **{html.escape(ADMIN_NAME)}**")
    with col_m:
        if st.button("Sync with Google Sheet"):
            if now - st.session_state["last_admin_fetch"] < 5.0:
                st.warning("Please wait 5 seconds before refreshing Google Sheets.")
            else:
                st.session_state["last_admin_fetch"] = now
                st.cache_data.clear()
                st.rerun()
    with col_r:
        if st.button("Logout"):
            st.session_state["admin_authenticated"] = False
            st.rerun()

    pending_orders = fetch_pending_orders()

    # 4. Confirmation Dialog for Dispatching
    if st.session_state["dispatch_target"]:
        target = st.session_state["dispatch_target"]
        order_id_safe = html.escape(str(target.get('order_id', '')))
        st.warning(f"**Confirm Dispatch For Order #{order_id_safe}?**")
        st.markdown(f"""
            - **Client Name:** {html.escape(str(target.get('name', '')))}
            - **Products:** {html.escape(str(target.get('products', '')))}
            - **Address:** {html.escape(str(target.get('address', '')))}
            - **Email:** {html.escape(str(target.get('email', '')))}
        """)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Yes, Confirm & Update Google Sheets", use_container_width=True):
                success = mark_order_dispatched(target.get("order_id"))
                if success:
                    st.success(f"Order #{order_id_safe} successfully marked as Dispatched in Google Sheets!")
                st.session_state["dispatch_target"] = None
                st.rerun()
        with c2:
            if st.button("Cancel", use_container_width=True):
                st.session_state["dispatch_target"] = None
                st.rerun()
        st.divider()

    st.subheader(f"Pending Orders ({len(pending_orders)})")

    if not pending_orders:
        st.info("No pending orders to dispatch at this time. All orders are fulfilled!")
        return

    # Table Header
    header_cols = st.columns([1, 2, 3, 3, 2, 2, 2, 2, 2])
    headers = ["Sr no.", "Name", "Address", "Products ordered", "Customization", "Email", "Order ID", "Status", "Action"]
    for col, h in zip(header_cols, headers):
        col.markdown(f"**{h}**")

    st.divider()

    # Render Order Rows with 100% Native Safe Streamlit Syntax (Zero unsafe_allow_html)
    for idx, order in enumerate(pending_orders):
        cols = st.columns([1, 2, 3, 3, 2, 2, 2, 2, 2])
        cols[0].write(html.escape(str(order.get("sr_no", idx + 1))))
        cols[1].write(html.escape(str(order.get("name", "N/A"))))
        cols[2].write(html.escape(str(order.get("address", "N/A"))))
        cols[3].write(html.escape(str(order.get("products", "N/A"))))
        cols[4].write(html.escape(str(order.get("customization", "None"))))
        cols[5].write(html.escape(str(order.get("email", "N/A"))))
        cols[6].markdown(f"`{html.escape(str(order.get('order_id', '')))}`")
        
        # Pure native colored markdown without unsafe_allow_html
        cols[7].markdown(":orange[**Pending**]")

        safe_btn_key = f"disp_{order.get('order_id', idx)}_{idx}"
        if cols[8].button("Dispatch", key=safe_btn_key):
            st.session_state["dispatch_target"] = order
            st.rerun()

# ================= MULTI-ROUTE DISPATCHER =================
main_page = st.Page(storefront_view, title="Resins by R", default=True)
admin_page = st.Page(admin_view, title="Admin Portal", url_path="admin")

pg = st.navigation([main_page, admin_page], position="hidden")
pg.run()
