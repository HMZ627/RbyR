import streamlit as st
import streamlit.components.v1 as components

# 1. Configure Streamlit Page
st.set_page_config(
    page_title="Resins by R | Liquid Luxury",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Inject CSS to hide default Streamlit chrome for an immersive web experience
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

# 3. Complete Self-Contained Web Experience with Custom Intro & Animations
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resins by R</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    
    <!-- Icons & Tailwind CSS -->
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <script src="https://cdn.tailwindcss.com"></script>

    <style>
        :root {
            --bg-deep: #070709;
            --resin-gold: #e5b869;
            --resin-gold-bright: #ffd984;
            --resin-gold-glow: rgba(229, 184, 105, 0.45);
            --liquid-glass: rgba(255, 255, 255, 0.03);
            --liquid-glass-border: rgba(255, 255, 255, 0.12);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-deep);
            color: #f3f4f6;
            font-family: 'Plus Jakarta Sans', sans-serif;
            overflow-x: hidden;
            opacity: 0;
            transition: opacity 1.2s cubic-bezier(0.16, 1, 0.3, 1);
        }

        body.site-ready {
            opacity: 1;
        }

        .font-luxury {
            font-family: 'Cinzel', serif;
        }

        /* ================= INTRO ANIMATION SCREEN ================= */
        #intro-overlay {
            position: fixed;
            inset: 0;
            background: #000000;
            z-index: 99999;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transition: opacity 1s cubic-bezier(0.77, 0, 0.175, 1);
            pointer-events: all;
        }

        /* SVG Outline Drawing from top to bottom */
        .svg-r-path {
            stroke: #ffffff;
            stroke-width: 4;
            stroke-linecap: round;
            stroke-linejoin: round;
            fill: transparent;
            stroke-dasharray: 950;
            stroke-dashoffset: 950;
            animation: drawOutline 1.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.5));
        }

        @keyframes drawOutline {
            0% {
                stroke-dashoffset: 950;
            }
            100% {
                stroke-dashoffset: 0;
            }
        }

        /* Liquid White & Golden Dust Fill Animation */
        .svg-r-fill {
            opacity: 0;
            animation: fillGoldDust 1.3s cubic-bezier(0.25, 1, 0.5, 1) forwards 1.7s;
        }

        @keyframes fillGoldDust {
            0% {
                opacity: 0;
                transform: scale(0.97);
            }
            100% {
                opacity: 1;
                transform: scale(1);
                filter: drop-shadow(0 0 25px rgba(229, 184, 105, 0.8)) drop-shadow(0 0 45px rgba(255, 255, 255, 0.6));
            }
        }

        /* Floating Golden Sparkle Particles */
        .gold-dust-particles {
            position: absolute;
            inset: 0;
            pointer-events: none;
            overflow: hidden;
            opacity: 0;
            animation: particlesFadeIn 1s ease forwards 1.9s;
        }

        @keyframes particlesFadeIn {
            to { opacity: 1; }
        }

        .dust-particle {
            position: absolute;
            background: radial-gradient(circle, #fff, #e5b869, transparent);
            border-radius: 50%;
            animation: floatSparkle 2.2s infinite ease-in-out alternate;
        }

        @keyframes floatSparkle {
            0% { transform: translateY(0) scale(0.4); opacity: 0.3; }
            50% { opacity: 1; filter: drop-shadow(0 0 6px #ffd984); }
            100% { transform: translateY(-30px) scale(1.1); opacity: 0.2; }
        }

        /* ================= ONE-TIME FADE-IN-UPWARDS ANIMATIONS ================= */
        .fade-in-up {
            opacity: 0;
            transform: translateY(32px);
            transition: opacity 0.85s cubic-bezier(0.16, 1, 0.3, 1), transform 0.85s cubic-bezier(0.16, 1, 0.3, 1);
            will-change: opacity, transform;
        }

        .fade-in-up.appeared {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }

        /* Luxury Resin Glassmorphism */
        .resin-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.015));
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid var(--liquid-glass-border);
            box-shadow: 0 20px 45px -15px rgba(0, 0, 0, 0.85);
            transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.4s ease, box-shadow 0.4s ease;
        }

        .resin-card:hover {
            transform: translateY(-8px);
            border-color: rgba(229, 184, 105, 0.5);
            box-shadow: 0 25px 50px -15px var(--resin-gold-glow);
        }

        .btn-gold {
            background: linear-gradient(135deg, #e5b869, #bf8f3b);
            color: #08090b;
            font-weight: 700;
            position: relative;
            overflow: hidden;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .btn-gold::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -80%;
            width: 50%;
            height: 200%;
            background: rgba(255, 255, 255, 0.4);
            transform: rotate(30deg);
            transition: all 0.75s ease;
        }

        .btn-gold:hover::after {
            left: 140%;
        }

        .btn-gold:hover {
            box-shadow: 0 0 28px rgba(229, 184, 105, 0.6);
            transform: translateY(-2px);
        }

        .btn-glass {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.15);
            transition: all 0.3s ease;
        }

        .btn-glass:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: var(--resin-gold);
            color: var(--resin-gold);
        }

        /* Ambient floating fluid aura */
        .ambient-glow {
            position: fixed;
            width: 550px;
            height: 550px;
            background: radial-gradient(circle, rgba(229, 184, 105, 0.08) 0%, transparent 70%);
            border-radius: 50%;
            filter: blur(100px);
            pointer-events: none;
            z-index: 0;
        }
    </style>
</head>
<body class="relative min-h-screen">

    <!-- INTRO OVERLAY SCREEN -->
    <div id="intro-overlay">
        <div class="gold-dust-particles" id="dust-container"></div>
        <div class="relative flex flex-col items-center">
            <svg width="200" height="230" viewBox="0 0 200 230" fill="none" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <!-- Gold dust liquid gradient for the filled 'R' -->
                    <linearGradient id="goldDustGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#ffffff" />
                        <stop offset="35%" stop-color="#fff8db" />
                        <stop offset="65%" stop-color="#ffd984" />
                        <stop offset="100%" stop-color="#bf8f3b" />
                    </linearGradient>
                    <!-- Shimmering pattern overlay -->
                    <filter id="goldGlow" x="-20%" y="-20%" width="140%" height="140%">
                        <feGaussianBlur stdDeviation="3" result="blur" />
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                    </filter>
                </defs>

                <!-- Outline traced from top to bottom -->
                <path class="svg-r-path" d="M 55 200 L 55 35 L 125 35 C 165 35 165 110 125 110 L 55 110 M 110 110 L 160 200" />

                <!-- Filled body with white & liquid gold dust -->
                <path class="svg-r-fill" filter="url(#goldGlow)" fill="url(#goldDustGradient)" 
                      d="M 55 200 L 55 35 L 125 35 C 165 35 165 110 125 110 L 55 110 M 110 110 L 160 200" 
                      stroke="url(#goldDustGradient)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" />
            </svg>

            <span id="intro-subtitle" class="font-luxury text-xs tracking-[0.4em] uppercase text-amber-200 mt-6 opacity-0 transition-opacity duration-700">
                Resins By R
            </span>
        </div>
    </div>

    <!-- Ambient Glowing Lights -->
    <div class="ambient-glow top-0 left-[-100px]"></div>
    <div class="ambient-glow bottom-0 right-[-100px]"></div>

    <!-- Navigation Header -->
    <header class="sticky top-0 z-40 backdrop-blur-xl bg-black/50 border-b border-white/10">
        <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <a href="#" class="fade-in-up flex items-center space-x-3">
                <div class="w-10 h-10 rounded-full border border-amber-300/40 flex items-center justify-center bg-gradient-to-tr from-amber-600/30 to-amber-200/10">
                    <span class="font-luxury text-amber-200 text-xl font-bold">R</span>
                </div>
                <span class="font-luxury text-xl tracking-[0.22em] text-white">RESINS <span class="text-amber-300 font-light text-sm tracking-normal">BY R</span></span>
            </a>

            <button onclick="toggleCartDrawer(true)" class="fade-in-up relative flex items-center space-x-2 px-5 py-2 rounded-full border border-white/15 bg-white/5 hover:border-amber-300/40 transition">
                <i class="ph ph-handbag text-amber-300 text-lg"></i>
                <span class="text-xs uppercase tracking-widest text-gray-200 font-medium">Cart</span>
                <span id="nav-cart-count" class="ml-1 px-2 py-0.5 text-xs bg-amber-400 text-black font-bold rounded-full">0</span>
            </button>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="max-w-6xl mx-auto px-6 pt-20 pb-16 text-center relative z-10">
        <div class="fade-in-up inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-amber-400/20 bg-amber-400/5 mb-6">
            <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
            <span class="text-xs uppercase tracking-widest text-amber-300 font-semibold">Hand-Poured With Precision</span>
        </div>

        <h1 class="fade-in-up font-luxury text-4xl sm:text-6xl md:text-7xl font-semibold tracking-tight text-white mb-6 leading-tight">
            Immortalize Beauty.<br>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-200 via-amber-400 to-yellow-500">Liquid Luxury</span> In Resin.
        </h1>

        <p class="fade-in-up max-w-2xl mx-auto text-gray-400 text-sm md:text-base leading-relaxed mb-8">
            Bespoke epoxy creations encasing 24k gold leaf, mica pearls, botanical specimens, and personalized memories. Each piece is custom-cured and one-of-a-kind.
        </p>

        <div class="fade-in-up">
            <a href="#products-section" class="btn-gold px-8 py-3.5 rounded-full inline-flex items-center gap-3 text-xs tracking-widest uppercase">
                <span>View Products</span>
                <i class="ph ph-arrow-down text-sm"></i>
            </a>
        </div>
    </section>

    <!-- Product Grid -->
    <main id="products-section" class="max-w-7xl mx-auto px-6 py-12 relative z-10">
        <div class="flex flex-col md:flex-row md:items-end justify-between mb-12 border-b border-white/10 pb-6">
            <div>
                <h2 class="fade-in-up font-luxury text-3xl tracking-wide text-white">Signature Collection</h2>
                <p class="fade-in-up text-gray-400 text-sm mt-1">Select choices, customize your shades, or upload memories.</p>
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

                    <!-- Ring Size Selection -->
                    <div class="fade-in-up mb-6 bg-white/[0.02] p-4 rounded-xl border border-white/5">
                        <label class="block text-xs uppercase tracking-wider text-gray-300 font-semibold mb-2">Select Ring Size (US):</label>
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

                    <!-- Picture Options -->
                    <div class="fade-in-up mb-6 bg-white/[0.02] p-4 rounded-xl border border-white/5">
                        <div class="flex justify-between items-center mb-3">
                            <label class="text-xs uppercase tracking-wider text-gray-300 font-semibold">Embedded Pictures (Max 3):</label>
                            <span class="text-xs text-amber-300 font-mono">+PKR 100 / pic</span>
                        </div>
                        <div class="flex items-center gap-4">
                            <div class="flex items-center border border-white/20 rounded-lg overflow-hidden bg-black/40">
                                <button type="button" onclick="adjustPhotos(-1)" class="px-3.5 py-1.5 text-gray-300 hover:bg-white/10"><i class="ph ph-minus"></i></button>
                                <span id="shield-photo-count" class="px-4 py-1.5 text-sm font-semibold text-white">0</span>
                                <button type="button" onclick="adjustPhotos(1)" class="px-3.5 py-1.5 text-gray-300 hover:bg-white/10"><i class="ph ph-plus"></i></button>
                            </div>
                            <span id="shield-photo-status" class="text-xs text-gray-400">0 pictures (+PKR 0/-)</span>
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
                    <p class="fade-in-up text-gray-400 text-sm mb-6">Complete luxury set: 1 signature serving tray and 4 matching coasters hand-painted with gilded liquid leaf rims.</p>
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
            <!-- Rendered by JS -->
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

    <!-- ORDER NOW / CHECKOUT MODAL -->
    <div id="checkout-modal" class="fixed inset-0 bg-black/85 backdrop-blur-md z-50 hidden flex items-center justify-center p-4 overflow-y-auto">
        <div class="resin-card bg-[#0e0f14] w-full max-w-xl rounded-3xl border border-white/15 p-6 md:p-8 relative max-h-[92vh] overflow-y-auto my-auto shadow-2xl">
            <button onclick="toggleModal(false)" class="absolute top-5 right-5 text-gray-400 hover:text-amber-300 text-2xl">&times;</button>

            <div class="text-center mb-6">
                <span class="text-xs uppercase tracking-widest text-amber-300 font-semibold">Resins By R • Handcrafted Bespoke</span>
                <h3 class="font-luxury text-2xl text-white mt-1">Client Order Details</h3>
            </div>

            <!-- Real-time Cost Calculation Box -->
            <div class="p-4 rounded-2xl bg-white/[0.03] border border-white/10 mb-6 space-y-2">
                <div class="flex justify-between text-xs text-gray-300">
                    <span>Products Ordered:</span>
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
                    <span>Total Amount:</span>
                    <span id="modal-total" class="font-mono text-base">PKR 0/-</span>
                </div>
            </div>

            <!-- Form with 4 Mandatory Fields + Notes -->
            <form id="order-form" onsubmit="handleFormSubmission(event)" class="space-y-4 text-left">
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
                    <input type="tel" id="cust-phone" required placeholder="e.g. 0300 1234567" 
                           class="w-full px-4 py-3 bg-white/5 border border-white/15 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-amber-300">
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-300 font-semibold mb-1">
                        3. Full Address <span class="text-amber-400">*</span>
                    </label>
                    <textarea id="cust-address" required rows="2" placeholder="House/Apartment #, Street, City" 
                              class="w-full px-4 py-3 bg-white/5 border border-white/15 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-amber-300"></textarea>
                </div>

                <div>
                    <div class="flex justify-between items-center mb-1">
                        <label class="block text-xs uppercase tracking-wider text-gray-300 font-semibold">
                            4. TID (Transaction ID) For Payment Made <span class="text-amber-400">*</span>
                        </label>
                        <span class="text-[11px] text-amber-300">JazzCash / EasyPaisa / Raast / Bank</span>
                    </div>
                    <input type="text" id="cust-tid" required placeholder="Enter Payment TID reference" 
                           class="w-full px-4 py-3 bg-white/5 border border-white/15 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-amber-300 font-mono">
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-300 font-semibold mb-1">
                        Customization Notes (Colours, Design, or Picture Links)
                    </label>
                    <textarea id="cust-notes" rows="2" placeholder="Tell us your desired color themes, glitter types, flower inclusions, or attach photo upload links." 
                              class="w-full px-4 py-3 bg-white/5 border border-white/15 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-amber-300"></textarea>
                </div>

                <button type="submit" id="submit-btn" class="btn-gold w-full py-4 rounded-xl text-xs uppercase tracking-widest font-bold mt-2 shadow-xl">
                    Confirm & Place Custom Order
                </button>
            </form>
        </div>
    </div>

    <!-- Toast Notification -->
    <div id="toast" class="fixed bottom-6 left-1/2 -translate-x-1/2 bg-[#101115] border border-amber-300/50 text-white px-6 py-3 rounded-full text-xs uppercase tracking-widest shadow-2xl opacity-0 pointer-events-none transition-all duration-300 z-50 flex items-center gap-2">
        <i class="ph ph-sparkle text-amber-300 text-base"></i>
        <span id="toast-msg">Item added to cart</span>
    </div>

    <script>
        const DELIVERY_FEE = 500;
        let cart = [];
        let selectedRingSize = 'US 5';
        let shieldPhotosCount = 0;
        let directCheckoutItem = null;

        // 1. GENERATE GOLD DUST PARTICLES IN INTRO
        const dustContainer = document.getElementById('dust-container');
        for (let i = 0; i < 40; i++) {
            const p = document.createElement('div');
            p.className = 'dust-particle';
            const size = Math.random() * 5 + 2;
            p.style.width = size + 'px';
            p.style.height = size + 'px';
            p.style.left = Math.random() * 100 + '%';
            p.style.top = Math.random() * 100 + '%';
            p.style.animationDelay = (Math.random() * 2) + 's';
            dustContainer.appendChild(p);
        }

        // 2. TIMELINE: INTRO -> MAIN SITE FADE-IN & STAGGERED UPWARDS ANIMATION
        window.addEventListener('load', () => {
            setTimeout(() => {
                const sub = document.getElementById('intro-subtitle');
                if (sub) sub.style.opacity = '1';
            }, 2100);

            // Intro fade out at 3.3s
            setTimeout(() => {
                const intro = document.getElementById('intro-overlay');
                intro.style.opacity = '0';
                document.body.classList.add('site-ready');
                
                setTimeout(() => {
                    intro.style.display = 'none';
                    initScrollObserver();
                }, 1000);
            }, 3300);
        });

        // 3. ONE-TIME FADE-IN-UPWARDS INTERSECTION OBSERVER
        function initScrollObserver() {
            const elements = document.querySelectorAll('.fade-in-up');
            const observer = new IntersectionObserver((entries) => {
                entries.forEach((entry, idx) => {
                    if (entry.isIntersecting) {
                        setTimeout(() => {
                            entry.target.classList.add('appeared');
                        }, idx * 70); // Buttery stagger
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });

            elements.forEach(el => observer.observe(el));
        }

        // Ring selection
        function selectRingSize(btn, size) {
            document.querySelectorAll('#ring-sizes .size-btn').forEach(b => {
                b.className = 'size-btn px-3.5 py-1.5 rounded-lg border border-white/10 text-xs text-gray-300 hover:border-amber-300 transition';
            });
            btn.className = 'size-btn px-3.5 py-1.5 rounded-lg border border-amber-300 text-xs text-amber-300 bg-amber-300/10 transition';
            selectedRingSize = size;
        }

        // Shield photo counter
        function adjustPhotos(delta) {
            shieldPhotosCount = Math.max(0, Math.min(3, shieldPhotosCount + delta));
            document.getElementById('shield-photo-count').innerText = shieldPhotosCount;
            const total = 2000 + (shieldPhotosCount * 100);
            document.getElementById('shield-price-display').innerText = `PKR ${total.toLocaleString()}/-`;
            document.getElementById('shield-photo-status').innerText = `${shieldPhotosCount} picture(s) (+PKR ${shieldPhotosCount * 100}/-)`;
        }

        // Construct object
        function getProductData(id) {
            if (id === 'resin-ring') {
                return {
                    id: 'resin-ring',
                    name: `Resin Ring (${selectedRingSize})`,
                    spec: `Size: ${selectedRingSize}`,
                    price: 800,
                    qty: 1
                };
            } else if (id === 'resin-shield') {
                const total = 2000 + (shieldPhotosCount * 100);
                return {
                    id: 'resin-shield',
                    name: 'Resins Shield (6-Inch)',
                    spec: shieldPhotosCount > 0 ? `${shieldPhotosCount} picture(s) embedded` : 'No picture inclusion',
                    price: total,
                    qty: 1
                };
            } else if (id === 'chess-keychain') {
                return {
                    id: 'chess-keychain',
                    name: 'Resin 3D Chess Keychain',
                    spec: 'Sculpted Piece',
                    price: 500,
                    qty: 1
                };
            } else if (id === 'tray-coaster-set') {
                return {
                    id: 'tray-coaster-set',
                    name: 'Resin Tray & Coaster Set',
                    spec: '1 Tray + 4 Coasters',
                    price: 4000,
                    qty: 1
                };
            }
        }

        function handleAddToCart(id) {
            const item = getProductData(id);
            const found = cart.find(i => i.name === item.name && i.spec === item.spec);
            if (found) {
                found.qty += 1;
            } else {
                cart.push(item);
            }
            renderCart();
            showToast(`"${item.name}" added to cart`);
        }

        function handleQuickOrder(id) {
            directCheckoutItem = getProductData(id);
            openCheckout([directCheckoutItem]);
        }

        function renderCart() {
            const list = document.getElementById('cart-items-container');
            const badge = document.getElementById('nav-cart-count');
            const totalItems = cart.reduce((acc, c) => acc + c.qty, 0);
            badge.innerText = totalItems;

            if (cart.length === 0) {
                list.innerHTML = `<div class="h-64 flex flex-col items-center justify-center text-gray-500 text-sm">Your cart is currently empty.</div>`;
                document.getElementById('cart-subtotal').innerText = 'PKR 0/-';
                document.getElementById('cart-grandtotal').innerText = `PKR ${DELIVERY_FEE}/-`;
                return;
            }

            let subtotal = 0;
            let html = '';
            cart.forEach((item, idx) => {
                const itemTotal = item.price * item.qty;
                subtotal += itemTotal;
                html += `
                    <div class="p-4 rounded-xl bg-white/[0.03] border border-white/5 flex items-center justify-between">
                        <div>
                            <h4 class="text-sm font-semibold text-white">${item.name}</h4>
                            <p class="text-xs text-amber-300">${item.spec}</p>
                            <span class="text-xs font-mono text-gray-400 mt-1 block">Qty: ${item.qty} × PKR ${item.price}/-</span>
                        </div>
                        <div class="flex items-center gap-3">
                            <span class="font-mono text-sm font-bold text-white">PKR ${itemTotal}/-</span>
                            <button onclick="removeCartItem(${idx})" class="text-gray-500 hover:text-red-400 text-base">&times;</button>
                        </div>
                    </div>`;
            });

            list.innerHTML = html;
            document.getElementById('cart-subtotal').innerText = `PKR ${subtotal.toLocaleString()}/-`;
            document.getElementById('cart-grandtotal').innerText = `PKR ${(subtotal + DELIVERY_FEE).toLocaleString()}/-`;
        }

        function removeCartItem(idx) {
            cart.splice(idx, 1);
            renderCart();
        }

        function toggleCartDrawer(open) {
            const drawer = document.getElementById('cart-drawer');
            const backdrop = document.getElementById('cart-drawer-backdrop');
            if (open) {
                backdrop.classList.remove('hidden');
                setTimeout(() => drawer.classList.remove('translate-x-full'), 10);
            } else {
                drawer.classList.add('translate-x-full');
                setTimeout(() => backdrop.classList.add('hidden'), 300);
            }
        }

        function proceedToCheckoutFromCart() {
            if (cart.length === 0) {
                showToast("Your cart is empty");
                return;
            }
            toggleCartDrawer(false);
            directCheckoutItem = null;
            openCheckout(cart);
        }

        function openCheckout(items) {
            const subtotal = items.reduce((acc, c) => acc + (c.price * c.qty), 0);
            const grandTotal = subtotal + DELIVERY_FEE;

            document.getElementById('modal-item-summary').innerText = items.map(i => `${i.name} (x${i.qty})`).join(', ');
            document.getElementById('modal-subtotal').innerText = `PKR ${subtotal.toLocaleString()}/-`;
            document.getElementById('modal-total').innerText = `PKR ${grandTotal.toLocaleString()}/-`;

            toggleModal(true);
        }

        function toggleModal(open) {
            const modal = document.getElementById('checkout-modal');
            if (open) modal.classList.remove('hidden');
            else modal.classList.add('hidden');
        }

        function showToast(msg) {
            const toast = document.getElementById('toast');
            document.getElementById('toast-msg').innerText = msg;
            toast.classList.remove('opacity-0', 'pointer-events-none');
            setTimeout(() => toast.classList.add('opacity-0', 'pointer-events-none'), 3000);
        }

        function handleFormSubmission(e) {
            e.preventDefault();
            const name = document.getElementById('cust-name').value.trim();
            const phone = document.getElementById('cust-phone').value.trim();
            const address = document.getElementById('cust-address').value.trim();
            const tid = document.getElementById('cust-tid').value.trim();
            const notes = document.getElementById('cust-notes').value.trim() || 'No customization notes';

            const activeItems = directCheckoutItem ? [directCheckoutItem] : cart;
            const subtotal = activeItems.reduce((acc, c) => acc + (c.price * c.qty), 0);
            const total = subtotal + DELIVERY_FEE;

            alert(`✨ ORDER CONFIRMED! ✨\\n\\nDear ${name},\\nThank you for choosing Resins by R!\\n\\n• Items: ${activeItems.map(i => i.name).join(', ')}\\n• Total: PKR ${total}/- (Including PKR 500 delivery)\\n• TID: ${tid}\\n• Address: ${address}\\n• Custom Notes: ${notes}\\n\\nWe have received your custom order.`);

            // Reset
            cart = [];
            directCheckoutItem = null;
            renderCart();
            toggleModal(false);
            document.getElementById('order-form').reset();
        }

        renderCart();
    </script>
</body>
</html>
"""

# 4. Render directly through Streamlit Components
components.html(HTML_CODE, height=1000, scrolling=True)
