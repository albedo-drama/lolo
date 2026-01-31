from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx

app = FastAPI()

# API Target
API_BASE = "https://api.sansekai.my.id/api/melolo"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "Referer": "https://sansekai.my.id/"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ALBEDOLOLO-TV | Premium Stream</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        [x-cloak] { display: none !important; }
        .hide-scroll::-webkit-scrollbar { display: none; }
        .glass { background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(16px); border-bottom: 1px solid rgba(255,255,255,0.05); }
        .card-gradient { background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, transparent 100%); }
        .text-shadow { text-shadow: 0 2px 4px rgba(0,0,0,0.8); }
        video::-webkit-media-controls { display:none !important; }
        .animate-enter { animation: enter 0.3s ease-out; }
        @keyframes enter { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body class="bg-[#020617] text-slate-200 font-sans selection:bg-blue-600 selection:text-white" x-data="albedoApp()" x-init="init()">

    <nav class="fixed top-0 w-full z-50 glass transition-all duration-300" :class="{'py-2': scrollY > 10, 'py-4': scrollY <= 10}">
        <div class="max-w-7xl mx-auto px-4 flex justify-between items-center">
            <div @click="resetHome()" class="flex items-center gap-2 cursor-pointer group">
                <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-600 to-violet-600 flex items-center justify-center shadow-lg shadow-blue-900/50 group-hover:rotate-12 transition">
                    <i class="fa-solid fa-play text-white text-xs"></i>
                </div>
                <h1 class="text-xl font-black tracking-tighter bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
                    ALBEDO<span class="text-blue-500 italic">TV</span>
                </h1>
            </div>
            
            <div class="relative w-1/2 md:w-1/3 group">
                <div class="absolute -inset-0.5 bg-gradient-to-r from-blue-600 to-violet-600 rounded-full opacity-20 group-hover:opacity-100 transition duration-500 blur"></div>
                <div class="relative flex items-center">
                    <input type="text" x-model="searchQuery" @keyup.enter="doSearch(true)" placeholder="Cari Drama..." 
                           class="w-full bg-[#0f172a] text-xs py-2.5 pl-4 pr-10 rounded-full border border-white/10 focus:border-transparent outline-none text-white placeholder-slate-500 transition">
                    <i @click="doSearch(true)" class="fa-solid fa-magnifying-glass absolute right-4 text-slate-400 cursor-pointer hover:text-white transition"></i>
                </div>
            </div>
        </div>
    </nav>

    <div class="fixed bottom-5 right-5 z-[100] flex flex-col gap-2 pointer-events-none">
        <template x-for="toast in toasts" :key="toast.id">
            <div class="bg-slate-800 border border-slate-700 text-white px-4 py-3 rounded-lg shadow-2xl flex items-center gap-3 animate-enter pointer-events-auto">
                <i :class="toast.icon" class="text-blue-500"></i>
                <span class="text-xs font-bold" x-text="toast.msg"></span>
            </div>
        </template>
    </div>

    <div x-show="loading" class="fixed inset-0 bg-[#020617]/90 backdrop-blur-sm z-[9999] flex flex-col items-center justify-center gap-4 transition-opacity duration-300">
        <div class="relative w-16 h-16">
            <div class="absolute inset-0 border-4 border-blue-500/20 rounded-full"></div>
            <div class="absolute inset-0 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            <i class="fa-solid fa-video absolute inset-0 flex items-center justify-center text-blue-500 text-xl animate-pulse"></i>
        </div>
        <p class="text-[10px] font-bold tracking-[0.2em] text-blue-500 animate-pulse">MEMUAT KONTEN...</p>
    </div>

    <main class="max-w-7xl mx-auto px-4 pt-24 pb-24 min-h-screen">

        <template x-if="view === 'home'">
            <div class="space-y-12 animate-enter">
                
                <template x-if="trending.length > 0">
                    <div class="relative w-full aspect-[16/9] md:aspect-[21/9] rounded-2xl overflow-hidden shadow-2xl group cursor-pointer border border-white/5" @click="openDetail(trending[0].id)">
                        <img :src="trending[0].cover" class="absolute inset-0 w-full h-full object-cover opacity-60 group-hover:scale-105 transition duration-1000">
                        <div class="absolute inset-0 bg-gradient-to-t from-[#020617] via-[#020617]/40 to-transparent"></div>
                        <div class="absolute bottom-0 left-0 p-6 md:p-12 w-full md:w-2/3">
                            <span class="inline-flex items-center gap-1 bg-blue-600/90 backdrop-blur text-white text-[10px] font-bold px-3 py-1 rounded-full shadow-lg mb-3 border border-blue-400/30">
                                <i class="fa-solid fa-fire"></i> TRENDING #1
                            </span>
                            <h2 class="text-2xl md:text-5xl font-black text-white mb-3 leading-tight text-shadow drop-shadow-lg" x-text="trending[0].title"></h2>
                            <div class="flex items-center gap-3 text-xs font-bold text-slate-300 mb-6">
                                <span class="bg-white/10 px-2 py-0.5 rounded border border-white/10" x-text="trending[0].genre"></span>
                                <span>•</span>
                                <span class="text-blue-400" x-text="trending[0].totalEps + ' Episode'"></span>
                            </div>
                            <button class="bg-white text-black hover:bg-blue-50 font-bold py-2.5 px-8 rounded-full text-xs transition shadow-[0_0_20px_rgba(255,255,255,0.3)] flex items-center gap-2">
                                <i class="fa-solid fa-play"></i> NONTON SEKARANG
                            </button>
                        </div>
                    </div>
                </template>

                <template x-if="history.length > 0">
                    <section>
                        <div class="flex items-center gap-2 mb-4 px-1">
                            <div class="w-1 h-5 bg-violet-500 rounded-full"></div>
                            <h2 class="text-lg font-bold text-white tracking-wide">LANJUTKAN MENONTON</h2>
                        </div>
                        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                            <template x-for="h in history" :key="h.id">
                                <div @click="openDetail(h.id)" class="group relative bg-slate-900 rounded-xl overflow-hidden border border-white/5 hover:border-violet-500/50 transition cursor-pointer">
                                    <div class="relative aspect-[16/9]">
                                        <img :src="h.cover" class="w-full h-full object-cover opacity-60 group-hover:opacity-100 transition">
                                        <div class="absolute inset-0 flex items-center justify-center">
                                            <div class="w-8 h-8 bg-white/20 backdrop-blur rounded-full flex items-center justify-center group-hover:bg-violet-600 transition">
                                                <i class="fa-solid fa-play text-white text-[10px]"></i>
                                            </div>
                                        </div>
                                        <div class="absolute bottom-2 right-2 bg-black/80 px-2 py-0.5 rounded text-[9px] font-bold text-violet-400 border border-violet-500/30">
                                            EPS <span x-text="h.eps"></span>
                                        </div>
                                    </div>
                                    <div class="p-3">
                                        <h3 class="text-[10px] font-bold text-slate-200 truncate" x-text="h.title"></h3>
                                        <p class="text-[9px] text-slate-500">Terakhir ditonton</p>
                                    </div>
                                </div>
                            </template>
                        </div>
                    </section>
                </template>

                <section>
                    <div class="flex items-center justify-between mb-4 px-1">
                        <div class="flex items-center gap-2">
                            <div class="w-1 h-5 bg-blue-500 rounded-full"></div>
                            <h2 class="text-lg font-bold text-white tracking-wide">POPULER SAAT INI</h2>
                        </div>
                    </div>
                    <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3 md:gap-4">
                        <template x-for="(item, idx) in trending" :key="item.id">
                            <div x-show="idx > 0" @click="openDetail(item.id)" class="group relative bg-[#0f172a] rounded-xl overflow-hidden cursor-pointer hover:-translate-y-1 transition duration-300 shadow-lg border border-white/5">
                                <div class="relative aspect-[3/4.5]">
                                    <img :src="item.cover" class="w-full h-full object-cover loading-bg">
                                    <div class="absolute inset-0 card-gradient"></div>
                                    <div class="absolute top-1.5 right-1.5 flex flex-col items-end gap-1.5">
                                        <template x-if="item.is18"><span class="bg-red-600/90 backdrop-blur text-[8px] font-black px-1.5 py-0.5 rounded text-white shadow-lg border border-red-500/30">18+</span></template>
                                        <template x-if="item.isFinished"><span class="bg-emerald-600/90 backdrop-blur text-[8px] font-black px-1.5 py-0.5 rounded text-white shadow-lg border border-emerald-500/30">TAMAT</span></template>
                                    </div>
                                    <div class="absolute bottom-0 w-full p-3">
                                        <h3 class="text-[10px] md:text-xs font-bold text-white leading-tight line-clamp-2 mb-1 group-hover:text-blue-400 transition" x-text="item.title"></h3>
                                        <div class="flex items-center gap-1 text-[9px] text-slate-400">
                                            <i class="fa-solid fa-layer-group text-blue-500"></i> <span x-text="item.totalEps"></span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </div>
                    <div class="text-center mt-8" x-show="trendingHasMore">
                        <button @click="loadMoreTrending()" class="bg-slate-800 hover:bg-blue-600 border border-slate-700 hover:border-blue-500 text-white text-xs font-bold py-3 px-8 rounded-full transition flex items-center gap-2 mx-auto shadow-lg">
                            <span>MUAT LEBIH BANYAK</span> <i class="fa-solid fa-arrow-down"></i>
                        </button>
                    </div>
                </section>

                <section>
                    <div class="flex items-center gap-2 mb-4 px-1">
                        <div class="w-1 h-5 bg-pink-500 rounded-full"></div>
                        <h2 class="text-lg font-bold text-white tracking-wide">BARU DIRILIS</h2>
                    </div>
                    <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3 md:gap-4">
                        <template x-for="item in latest" :key="item.id">
                            <div @click="openDetail(item.id)" class="group relative bg-[#0f172a] rounded-xl overflow-hidden cursor-pointer hover:-translate-y-1 transition duration-300 shadow-lg border border-white/5">
                                <div class="relative aspect-[3/4.5]">
                                    <img :src="item.cover" class="w-full h-full object-cover loading-bg">
                                    <div class="absolute inset-0 card-gradient"></div>
                                    <div class="absolute top-1.5 right-1.5 flex flex-col items-end gap-1.5">
                                        <template x-if="!item.isFinished"><span class="bg-blue-600/90 backdrop-blur text-[8px] font-black px-1.5 py-0.5 rounded text-white shadow-lg border border-blue-500/30">ONGOING</span></template>
                                    </div>
                                    <div class="absolute bottom-0 w-full p-3">
                                        <h3 class="text-[10px] md:text-xs font-bold text-white leading-tight line-clamp-2 mb-1 group-hover:text-pink-400 transition" x-text="item.title"></h3>
                                        <p class="text-[9px] text-slate-400 truncate" x-text="item.genre"></p>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </div>
                    <div class="text-center mt-8" x-show="latestHasMore">
                        <button @click="loadMoreLatest()" class="bg-slate-800 hover:bg-pink-600 border border-slate-700 hover:border-pink-500 text-white text-xs font-bold py-3 px-8 rounded-full transition flex items-center gap-2 mx-auto shadow-lg">
                            <span>MUAT LEBIH BANYAK</span> <i class="fa-solid fa-arrow-down"></i>
                        </button>
                    </div>
                </section>
            </div>
        </template>

        <template x-if="view === 'search'">
            <div class="animate-enter">
                <button @click="resetHome()" class="mb-6 text-xs font-bold text-slate-400 hover:text-white flex items-center gap-2 transition group">
                    <div class="w-6 h-6 rounded-full bg-slate-800 flex items-center justify-center group-hover:bg-blue-600"><i class="fa-solid fa-arrow-left"></i></div> KEMBALI
                </button>
                <h2 class="text-xl font-black mb-6 uppercase text-white flex items-center gap-2">
                    <i class="fa-solid fa-magnifying-glass text-blue-500"></i> HASIL: <span class="text-blue-400" x-text="searchQuery"></span>
                </h2>
                
                <template x-if="searchList.length === 0 && !loading">
                    <div class="text-center py-20 bg-slate-900/50 rounded-2xl border border-dashed border-slate-700">
                        <i class="fa-regular fa-folder-open text-4xl text-slate-600 mb-4"></i>
                        <p class="text-slate-500 text-sm">Tidak ada drama yang ditemukan.</p>
                    </div>
                </template>

                <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3 md:gap-4">
                    <template x-for="item in searchList" :key="item.id">
                        <div @click="openDetail(item.id)" class="group relative bg-[#0f172a] rounded-xl overflow-hidden cursor-pointer hover:ring-1 hover:ring-blue-500 transition">
                            <div class="relative aspect-[3/4.5]">
                                <img :src="item.cover" class="w-full h-full object-cover">
                                <div class="absolute inset-0 card-gradient"></div>
                                <div class="absolute top-1.5 right-1.5">
                                    <template x-if="item.isFinished"><span class="bg-emerald-600 text-[8px] font-black px-1.5 py-0.5 rounded text-white shadow-lg">TAMAT</span></template>
                                </div>
                                <div class="absolute bottom-0 w-full p-3">
                                    <h3 class="text-[10px] md:text-xs font-bold text-white leading-tight line-clamp-2" x-text="item.title"></h3>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>
                <div class="text-center mt-8" x-show="searchHasMore">
                    <button @click="loadMoreSearch()" class="bg-slate-800 hover:bg-blue-600 border border-slate-700 text-xs font-bold py-3 px-8 rounded-full transition">MUAT LEBIH BANYAK</button>
                </div>
            </div>
        </template>

        <template x-if="view === 'detail'">
            <div x-cloak class="animate-enter pb-10">
                <button @click="view = 'home'" class="mb-4 text-xs font-bold text-slate-400 hover:text-white flex items-center gap-2 group">
                    <i class="fa-solid fa-chevron-left group-hover:-translate-x-1 transition"></i> KEMBALI
                </button>

                <div class="relative bg-[#0f172a] rounded-3xl overflow-hidden shadow-2xl border border-white/5">
                    <div class="absolute inset-0">
                        <img :src="activeDrama.series_cover" class="w-full h-full object-cover opacity-20 blur-3xl scale-125">
                        <div class="absolute inset-0 bg-gradient-to-t from-[#0f172a] via-[#0f172a]/80 to-transparent"></div>
                    </div>

                    <div class="relative z-10 p-6 md:p-10 flex flex-col md:flex-row gap-8 items-start">
                        <div class="w-48 md:w-64 flex-shrink-0 mx-auto md:mx-0 shadow-[0_20px_50px_rgba(0,0,0,0.5)] rounded-xl overflow-hidden border border-white/10 rotate-1 hover:rotate-0 transition duration-500">
                            <img :src="activeDrama.series_cover" class="w-full h-full object-cover">
                        </div>

                        <div class="flex-1 text-center md:text-left w-full">
                            <h1 class="text-3xl md:text-5xl font-black text-white mb-4 leading-tight drop-shadow-xl" x-text="activeDrama.series_title"></h1>
                            
                            <div class="flex flex-wrap justify-center md:justify-start gap-2 mb-6">
                                <span class="bg-white/10 backdrop-blur text-white text-[10px] font-bold px-3 py-1.5 rounded-full border border-white/10">
                                    <i class="fa-solid fa-list-ol mr-1 text-blue-400"></i> <span x-text="activeDrama.episode_cnt"></span> EPISODE
                                </span>
                                <span class="bg-white/10 backdrop-blur text-white text-[10px] font-bold px-3 py-1.5 rounded-full border border-white/10">
                                    <i class="fa-solid fa-heart mr-1 text-pink-500"></i> <span x-text="formatNumber(activeDrama.followed_cnt)"></span> LIKES
                                </span>
                                <template x-if="activeDrama.age_gate_info?.age_gate >= 18">
                                    <span class="bg-red-600 text-white text-[10px] font-bold px-3 py-1.5 rounded-full shadow-lg shadow-red-600/20">18+ DEWASA</span>
                                </template>
                            </div>

                            <div class="flex flex-wrap justify-center md:justify-start gap-1.5 mb-6">
                                <template x-for="cat in parseTags(activeDrama.category_schema)" :key="cat.category_id">
                                    <span class="text-[10px] font-bold px-3 py-1 rounded-lg bg-slate-800 text-slate-300 border border-slate-700 hover:bg-slate-700 transition cursor-default" x-text="cat.name"></span>
                                </template>
                            </div>

                            <div class="bg-black/20 p-5 rounded-2xl border border-white/5 mb-8 backdrop-blur-md">
                                 <template x-if="activeDrama.disclaimer_info?.content">
                                    <div class="flex gap-3 mb-3 pb-3 border-b border-white/10">
                                        <i class="fa-solid fa-circle-exclamation text-red-500 text-sm mt-0.5"></i>
                                        <p class="text-[10px] text-red-300 font-bold leading-relaxed" x-text="activeDrama.disclaimer_info.content"></p>
                                    </div>
                                </template>
                                <p class="text-slate-300 text-xs md:text-sm leading-relaxed" x-text="activeDrama.series_intro"></p>
                            </div>

                            <h3 class="text-xs font-black text-slate-400 uppercase mb-4 tracking-[0.2em] flex items-center gap-2 justify-center md:justify-start">
                                <span class="w-8 h-[2px] bg-blue-500"></span> PILIH EPISODE
                            </h3>
                            <div class="grid grid-cols-5 sm:grid-cols-8 md:grid-cols-10 gap-2 max-h-96 overflow-y-auto pr-2 custom-scroll">
                                <template x-for="(eps, index) in activeDrama.video_list" :key="eps.vid">
                                    <button @click="openPlayer(index)" 
                                        class="group relative p-2 rounded-lg transition-all duration-300 flex flex-col items-center justify-center border"
                                        :class="index === currentIdx && view === 'player' ? 'bg-blue-600 border-blue-500 shadow-lg shadow-blue-600/30 scale-105' : 'bg-slate-800 border-slate-700 hover:bg-slate-700 hover:border-slate-500'">
                                        <span class="text-xs font-black" :class="index === currentIdx && view === 'player' ? 'text-white' : 'text-slate-300'" x-text="eps.vid_index"></span>
                                        <span class="text-[7px] mt-1 opacity-60" :class="index === currentIdx && view === 'player' ? 'text-blue-100' : 'text-slate-500'" x-text="formatTime(eps.duration)"></span>
                                        
                                        <div class="absolute inset-0 bg-black/50 rounded-lg flex items-center justify-center opacity-0 group-hover:opacity-100 transition">
                                            <i class="fa-solid fa-play text-white text-[8px]"></i>
                                        </div>
                                    </button>
                                </template>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </template>

        <template x-if="view === 'player'">
            <div class="fixed inset-0 bg-black z-[9999] flex flex-col justify-center items-center group" x-data="{ showControls: true }" @mousemove="showControls = true; setTimeout(() => showControls = false, 3000)">
                
                <div class="absolute top-0 w-full p-4 flex justify-between z-20 bg-gradient-to-b from-black/90 to-transparent transition duration-500" :class="showControls ? 'opacity-100' : 'opacity-0'">
                    <button @click="view = 'detail'" class="bg-white/10 backdrop-blur px-5 py-2 rounded-full text-[10px] font-bold text-white border border-white/10 hover:bg-red-600 hover:border-red-500 transition shadow-lg flex items-center gap-2">
                        <i class="fa-solid fa-xmark"></i> TUTUP
                    </button>
                    <div class="text-right">
                        <p class="text-[9px] font-bold text-slate-400 uppercase tracking-widest max-w-[200px] truncate" x-text="activeDrama.series_title"></p>
                        <p class="text-sm font-black text-blue-500 shadow-black drop-shadow-md" x-text="'EPISODE ' + activeDrama.video_list[currentIdx].vid_index"></p>
                    </div>
                </div>
                
                <div class="w-full h-full bg-black relative flex items-center justify-center">
                    <video x-ref="vPlayer" :src="streamUrl" @ended="nextEps" @error="handleError" autoplay controls playsinline class="w-full h-full object-contain"></video>
                </div>

                <div class="absolute bottom-0 w-full p-6 flex gap-4 bg-gradient-to-t from-black via-black/90 to-transparent z-20 pb-10 transition duration-500" :class="showControls ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'">
                    <button @click="prevEps()" :disabled="currentIdx === 0" class="flex-1 bg-slate-800/80 backdrop-blur hover:bg-slate-700 py-4 rounded-2xl font-bold text-[10px] disabled:opacity-30 border border-slate-600 text-white transition flex items-center justify-center gap-2 group/btn">
                        <i class="fa-solid fa-backward group-hover/btn:-translate-x-1 transition"></i> SEBELUMNYA
                    </button>
                    <button @click="nextEps()" :disabled="currentIdx === activeDrama.video_list.length-1" class="flex-[2] bg-blue-600/90 backdrop-blur hover:bg-blue-500 py-4 rounded-2xl font-bold text-[10px] disabled:opacity-30 text-white shadow-xl shadow-blue-600/20 transition flex items-center justify-center gap-2 group/btn">
                        EPISODE LANJUT <i class="fa-solid fa-forward group-hover/btn:translate-x-1 transition"></i>
                    </button>
                </div>
            </div>
        </template>

    </main>

    <footer class="text-center py-8 text-slate-700 text-[10px] font-bold tracking-widest border-t border-slate-900 mt-10">
        <p>ALBEDOLOLO-TV &copy; 2026 • MIMPI JADI CEO</p>
    </footer>

    <script>
        function albedoApp() {
            return {
                view: 'home', loading: false, searchQuery: '', scrollY: 0,
                toasts: [],
                
                trending: [], trendingOffset: 0, trendingHasMore: true,
                latest: [], latestOffset: 0, latestHasMore: true,
                searchList: [], searchOffset: 0, searchHasMore: true,
                
                trendingIds: new Set(), latestIds: new Set(), searchIds: new Set(),
                
                activeDrama: null, streamUrl: '', backupUrl: '', currentIdx: 0,
                history: [], // History Storage

                async init() {
                    window.addEventListener('scroll', () => this.scrollY = window.scrollY);
                    this.loadHistory(); // Load history from local storage
                    this.loading = true;
                    await Promise.all([this.loadTrend(), this.loadLatest()]);
                    this.loading = false;
                },

                // TOAST SYSTEM
                showToast(msg, icon='fa-solid fa-check') {
                    const id = Date.now();
                    this.toasts.push({id, msg, icon});
                    setTimeout(() => this.toasts = this.toasts.filter(t => t.id !== id), 3000);
                },

                // DATA NORMALIZATION & LOGIC
                normalize(raw, type) {
                    let id, title, cover, totalEps, isFinished, is18;
                    if (type === 'search') {
                        const book = raw.books[0]; 
                        id = raw.id; title = book.book_name; cover = book.thumb_url;
                        totalEps = book.serial_count || '?';
                        isFinished = book.show_creation_status === 'Selesai' || (book.stat_infos && book.stat_infos.includes('Selesai'));
                        is18 = book.visibility_age_gate === '18';
                    } else {
                        id = raw.book_id; title = raw.book_name; cover = raw.thumb_url;
                        totalEps = raw.serial_count;
                        isFinished = raw.show_creation_status === 'Selesai';
                        is18 = raw.visibility_age_gate === '18';
                        // Clean Genre for Banner
                        if(raw.stat_infos && raw.stat_infos.length > 0) raw.genre = raw.stat_infos[0];
                        else raw.genre = "Drama Seru";
                    }
                    return { id, title, cover, totalEps, isFinished, is18, genre: raw.genre };
                },

                appendData(targetList, newItems) {
                    const existingIds = new Set(targetList.map(i => i.id));
                    const uniqueItems = newItems.filter(i => !existingIds.has(i.id));
                    return [...targetList, ...uniqueItems];
                },

                async loadTrend() {
                    const res = await fetch(`/api/trending?offset=${this.trendingOffset}`);
                    const json = await res.json();
                    const newItems = json.books.map(b => this.normalize(b, 'home'));
                    const unique = newItems.filter(i => !this.trendingIds.has(i.id));
                    
                    if(unique.length === 0 && this.trending.length > 0) this.trendingHasMore = false;
                    else {
                        unique.forEach(i => this.trendingIds.add(i.id));
                        this.trending = [...this.trending, ...unique];
                        this.trendingOffset = json.next_offset; this.trendingHasMore = json.has_more;
                    }
                },
                async loadMoreTrending() { this.loading=true; await this.loadTrend(); this.loading=false; },

                async loadLatest() {
                    const res = await fetch(`/api/latest?offset=${this.latestOffset}`);
                    const json = await res.json();
                    const newItems = json.books.map(b => this.normalize(b, 'home'));
                    const unique = newItems.filter(i => !this.latestIds.has(i.id));
                    
                    if(unique.length === 0 && this.latest.length > 0) this.latestHasMore = false;
                    else {
                        unique.forEach(i => this.latestIds.add(i.id));
                        this.latest = [...this.latest, ...unique];
                        this.latestOffset = json.next_offset; this.latestHasMore = json.has_more;
                    }
                },
                async loadMoreLatest() { this.loading=true; await this.loadLatest(); this.loading=false; },

                async doSearch(isNew = false) {
                    if(!this.searchQuery) return;
                    if(isNew) { this.searchList=[]; this.searchIds=new Set(); this.searchOffset=0; this.searchHasMore=true; }
                    this.view = 'search'; this.loading = true;
                    try {
                        const res = await fetch(`/api/search?q=${this.searchQuery}&offset=${this.searchOffset}`);
                        const json = await res.json();
                        if(json.data && json.data.search_data) {
                            const newItems = json.data.search_data.map(b => this.normalize(b, 'search'));
                            const unique = newItems.filter(i => !this.searchIds.has(i.id));
                            if(unique.length === 0 && this.searchList.length > 0) this.searchHasMore = false;
                            else {
                                unique.forEach(i => this.searchIds.add(i.id));
                                this.searchList = [...this.searchList, ...unique];
                                this.searchOffset = json.data.next_offset; this.searchHasMore = json.data.has_more;
                            }
                        } else { this.searchHasMore = false; }
                    } catch(e) { this.searchHasMore = false; }
                    this.loading = false;
                },
                async loadMoreSearch() { await this.doSearch(false); },

                resetHome() { this.searchQuery = ''; this.view = 'home'; window.scrollTo(0,0); },
                
                // DETAIL & PLAYER & HISTORY
                async openDetail(id) {
                    this.loading = true;
                    try {
                        const res = await fetch(`/api/detail?id=${id}`);
                        const json = await res.json();
                        this.activeDrama = json.data.video_data;
                        this.view = 'detail';
                        window.scrollTo(0,0);
                    } catch(e) { this.showToast('Gagal memuat detail', 'fa-solid fa-triangle-exclamation'); }
                    this.loading = false;
                },

                async openPlayer(idx) {
                    this.currentIdx = idx;
                    this.loading = true;
                    try {
                        const vid = this.activeDrama.video_list[idx].vid;
                        const res = await fetch(`/api/stream?vid=${vid}`);
                        const json = await res.json();
                        this.streamUrl = json.data.main_url;
                        this.backupUrl = json.data.backup_url;
                        
                        // Save History
                        this.saveHistory({
                            id: this.activeDrama.series_id_str,
                            title: this.activeDrama.series_title,
                            cover: this.activeDrama.series_cover,
                            eps: this.activeDrama.video_list[idx].vid_index
                        });

                        this.view = 'player';
                    } catch(e) { this.showToast('Link video rusak', 'fa-solid fa-link-slash'); }
                    this.loading = false;
                },

                // HISTORY LOGIC
                saveHistory(item) {
                    let h = JSON.parse(localStorage.getItem('albedo_history') || '[]');
                    h = h.filter(i => i.id !== item.id); // Remove if exists
                    h.unshift(item); // Add to top
                    if(h.length > 6) h.pop(); // Limit 6 items
                    localStorage.setItem('albedo_history', JSON.stringify(h));
                    this.history = h;
                },
                loadHistory() {
                    this.history = JSON.parse(localStorage.getItem('albedo_history') || '[]');
                },

                handleError() { 
                    if(this.streamUrl !== this.backupUrl && this.backupUrl) {
                        this.showToast('Mengalihkan ke server cadangan...', 'fa-solid fa-server');
                        this.streamUrl = this.backupUrl; 
                    } else {
                        this.showToast('Video tidak dapat diputar', 'fa-solid fa-circle-xmark');
                    }
                },
                nextEps() { 
                    if(this.currentIdx < this.activeDrama.video_list.length-1) {
                        this.showToast('Memutar episode selanjutnya...', 'fa-solid fa-forward');
                        this.openPlayer(this.currentIdx+1); 
                    }
                },
                prevEps() { if(this.currentIdx > 0) this.openPlayer(this.currentIdx-1); },
                
                formatNumber(num) { return new Intl.NumberFormat('id-ID', { notation: "compact" }).format(num); },
                formatTime(s) { return `${Math.floor(s/60)}:${(s%60).toString().padStart(2,'0')}`; },
                parseTags(str) { try { return JSON.parse(str); } catch { return []; } }
            }
        }
    </script>
</body>
</html>
"""

# --- BACKEND ---
@app.get("/", response_class=HTMLResponse)
async def root(): return HTML_TEMPLATE

@app.get("/api/latest")
async def latest(offset: int = 0):
    async with httpx.AsyncClient() as client:
        return (await client.get(f"{API_BASE}/latest?offset={offset}", headers=HEADERS)).json()

@app.get("/api/trending")
async def trending(offset: int = 0):
    async with httpx.AsyncClient() as client:
        return (await client.get(f"{API_BASE}/trending?offset={offset}", headers=HEADERS)).json()

@app.get("/api/search")
async def search(q: str, offset: int = 0):
    async with httpx.AsyncClient() as client:
        return (await client.get(f"{API_BASE}/search?query={q}&limit=10&offset={offset}", headers=HEADERS)).json()

@app.get("/api/detail")
async def detail(id: str):
    async with httpx.AsyncClient() as client:
        return (await client.get(f"{API_BASE}/detail?bookId={id}", headers=HEADERS)).json()

@app.get("/api/stream")
async def stream(vid: str):
    async with httpx.AsyncClient() as client:
        return (await client.get(f"{API_BASE}/stream?videoId={vid}", headers=HEADERS)).json()
