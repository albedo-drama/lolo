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
    <title>ALBEDOLOLO-TV</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        [x-cloak] { display: none !important; }
        .hide-scroll::-webkit-scrollbar { display: none; }
        .glass { background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(255,255,255,0.05); }
        .card-gradient { background: linear-gradient(to top, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.6) 40%, transparent 100%); }
        .text-shadow { text-shadow: 0 2px 4px rgba(0,0,0,0.9); }
        video { outline: none; }
        .animate-enter { animation: enter 0.4s ease-out; }
        @keyframes enter { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        /* Transisi Smooth untuk Player Controls */
        .fade-transition { transition: opacity 0.3s ease-in-out, transform 0.3s ease-in-out; }
    </style>
</head>
<body class="bg-[#020617] text-slate-200 font-sans selection:bg-blue-600 selection:text-white" x-data="albedoApp()" x-init="init()">

    <nav class="fixed top-0 w-full z-50 glass transition-all duration-300">
        <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center gap-2">
            <div @click="view = 'home'; window.scrollTo(0,0)" class="flex items-center gap-2 cursor-pointer group flex-shrink-0">
                <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-600/20 group-hover:rotate-12 transition">
                    <span class="font-black text-white italic text-sm">A</span>
                </div>
                <h1 class="text-sm md:text-lg font-black tracking-tighter text-white">
                    ALBEDOLOLO<span class="text-blue-500">-TV</span>
                </h1>
            </div>
            
            <div class="flex items-center gap-3">
                <button @click="view = 'favorites'" class="relative p-2 text-slate-400 hover:text-pink-500 transition">
                    <i class="fa-solid fa-heart text-lg"></i>
                    <span x-show="favorites.length > 0" class="absolute top-0 right-0 w-2 h-2 bg-pink-500 rounded-full animate-pulse"></span>
                </button>

                <div class="relative w-32 md:w-64 transition-all focus-within:w-40 md:focus-within:w-72">
                    <input type="text" x-model="searchQuery" @keyup.enter="doSearch(true)" placeholder="Cari..." 
                           class="w-full bg-[#0f172a] text-xs py-2 pl-3 pr-8 rounded-full border border-white/10 focus:border-blue-500 outline-none text-white placeholder-slate-600 transition shadow-inner">
                    <i @click="doSearch(true)" class="fa-solid fa-magnifying-glass absolute right-3 top-2.5 text-slate-500 text-xs cursor-pointer hover:text-white"></i>
                </div>
            </div>
        </div>
    </nav>

    <div class="fixed bottom-5 right-5 z-[100] flex flex-col gap-2 pointer-events-none">
        <template x-for="toast in toasts" :key="toast.id">
            <div class="bg-slate-800 border border-slate-700 text-white px-4 py-3 rounded-lg shadow-2xl flex items-center gap-3 animate-enter pointer-events-auto">
                <i :class="toast.icon"></i>
                <span class="text-xs font-bold" x-text="toast.msg"></span>
            </div>
        </template>
    </div>

    <main class="max-w-7xl mx-auto px-4 pt-24 pb-24 min-h-screen">

        <div x-show="loading" class="fixed inset-0 bg-[#020617]/90 z-[9999] flex flex-col items-center justify-center">
            <div class="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-3"></div>
            <p class="text-[10px] font-bold text-blue-500 tracking-widest animate-pulse">MEMUAT...</p>
        </div>

        <template x-if="view === 'home'">
            <div class="space-y-12 animate-enter">
                
                <template x-if="trending.length > 0">
                    <div class="relative w-full aspect-[16/9] md:aspect-[21/9] rounded-2xl overflow-hidden shadow-2xl group cursor-pointer border border-white/5" @click="openDetail(trending[0].id)">
                        <img :src="trending[0].cover" class="absolute inset-0 w-full h-full object-cover opacity-60 group-hover:scale-105 transition duration-1000">
                        <div class="absolute inset-0 bg-gradient-to-t from-[#020617] via-[#020617]/40 to-transparent"></div>
                        <div class="absolute bottom-0 left-0 p-6 md:p-10 w-full md:w-2/3">
                            <span class="inline-flex items-center gap-1 bg-blue-600 text-white text-[10px] font-bold px-3 py-1 rounded-full shadow-lg mb-3">
                                <i class="fa-solid fa-fire"></i> #1 POPULER
                            </span>
                            <h2 class="text-2xl md:text-4xl font-black text-white mb-2 leading-tight text-shadow" x-text="trending[0].title"></h2>
                            <div class="flex items-center gap-3 text-xs font-bold text-slate-300 mb-4">
                                <span x-text="trending[0].genre"></span>
                                <span>•</span>
                                <span class="text-blue-400" x-text="trending[0].totalEps + ' Eps'"></span>
                            </div>
                            <button class="bg-white text-black hover:bg-blue-50 font-bold py-2 px-6 rounded-full text-xs transition flex items-center gap-2">
                                <i class="fa-solid fa-play"></i> NONTON
                            </button>
                        </div>
                    </div>
                </template>

                <section>
                    <div class="flex items-center justify-between mb-4 border-l-4 border-orange-500 pl-3">
                        <h2 class="text-lg font-black text-white tracking-wide">TRENDING HOT</h2>
                    </div>
                    <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3 md:gap-4">
                        <template x-for="(item, idx) in trending" :key="item.id">
                            <div x-show="idx > 0" class="group relative bg-[#0f172a] rounded-xl overflow-hidden cursor-pointer hover:-translate-y-1 transition duration-300 shadow-lg border border-white/5">
                                <div @click="openDetail(item.id)" class="relative aspect-[3/4.5]">
                                    <img :src="item.cover" class="w-full h-full object-cover">
                                    <div class="absolute inset-0 card-gradient"></div>
                                    
                                    <div class="absolute top-1.5 right-1.5 flex flex-col items-end gap-1">
                                        <template x-if="item.is18"><span class="bg-red-600/90 backdrop-blur text-[8px] font-black px-1.5 py-0.5 rounded text-white shadow-lg border border-red-500/30">18+</span></template>
                                    </div>
                                    <div class="absolute top-1.5 left-1.5">
                                        <span class="bg-black/60 backdrop-blur text-white text-[8px] font-bold px-1.5 py-0.5 rounded border border-white/10" x-text="item.totalEps + ' Eps'"></span>
                                    </div>

                                    <div class="absolute bottom-0 w-full p-3">
                                        <h3 class="text-[10px] font-bold text-white leading-tight line-clamp-2 mb-1" x-text="item.title"></h3>
                                        <p class="text-[8px] text-slate-400 truncate" x-text="item.genre"></p>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </div>
                    <div class="text-center mt-8" x-show="trendingHasMore">
                        <button @click="loadMoreTrending()" class="bg-slate-800 border border-slate-700 hover:bg-slate-700 text-white text-xs font-bold py-2.5 px-8 rounded-full transition">
                            MUAT LAGI
                        </button>
                    </div>
                </section>

                <section>
                    <div class="flex items-center justify-between mb-4 border-l-4 border-blue-500 pl-3">
                        <h2 class="text-lg font-black text-white tracking-wide">BARU DIRILIS</h2>
                    </div>
                    <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3 md:gap-4">
                        <template x-for="item in latest" :key="item.id">
                            <div class="group relative bg-[#0f172a] rounded-xl overflow-hidden cursor-pointer hover:-translate-y-1 transition duration-300 shadow-lg border border-white/5">
                                <div @click="openDetail(item.id)" class="relative aspect-[3/4.5]">
                                    <img :src="item.cover" class="w-full h-full object-cover">
                                    <div class="absolute inset-0 card-gradient"></div>
                                    
                                    <div class="absolute top-1.5 right-1.5 flex flex-col items-end gap-1">
                                        <template x-if="item.is18"><span class="bg-red-600 text-[8px] font-black px-1.5 py-0.5 rounded text-white shadow-md">18+</span></template>
                                    </div>
                                    <div class="absolute top-1.5 left-1.5">
                                        <span class="bg-black/60 backdrop-blur text-white text-[8px] font-bold px-1.5 py-0.5 rounded border border-white/10" x-text="item.totalEps + ' Eps'"></span>
                                    </div>

                                    <div class="absolute bottom-0 w-full p-3">
                                        <h3 class="text-[10px] font-bold text-white leading-tight line-clamp-2 mb-1" x-text="item.title"></h3>
                                        <p class="text-[8px] text-slate-400 truncate" x-text="item.genre"></p>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </div>
                    <div class="text-center mt-8" x-show="latestHasMore">
                        <button @click="loadMoreLatest()" class="bg-slate-800 border border-slate-700 hover:bg-slate-700 text-white text-xs font-bold py-2.5 px-8 rounded-full transition">
                            MUAT LAGI
                        </button>
                    </div>
                </section>
            </div>
        </template>

        <template x-if="view === 'search'">
            <div class="animate-enter">
                <button @click="view = 'home'" class="mb-6 text-xs font-bold text-slate-400 hover:text-white flex items-center gap-2 transition group">
                    <div class="w-6 h-6 rounded-full bg-slate-800 flex items-center justify-center group-hover:bg-blue-600"><i class="fa-solid fa-arrow-left"></i></div> KEMBALI
                </button>
                <h2 class="text-xl font-black mb-6 uppercase text-white flex items-center gap-2">
                    <i class="fa-solid fa-magnifying-glass text-blue-500"></i> HASIL: <span class="text-blue-400" x-text="searchQuery"></span>
                </h2>
                
                <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3 md:gap-4">
                    <template x-for="item in searchList" :key="item.id">
                        <div class="group relative bg-[#0f172a] rounded-xl overflow-hidden cursor-pointer hover:ring-1 hover:ring-blue-500 transition">
                            <div @click="openDetail(item.id)" class="relative aspect-[3/4.5]">
                                <img :src="item.cover" class="w-full h-full object-cover">
                                <div class="absolute inset-0 card-gradient"></div>
                                
                                <div class="absolute top-1.5 right-1.5 flex flex-col items-end gap-1">
                                    <template x-if="item.is18"><span class="bg-red-600 text-[8px] font-black px-1.5 py-0.5 rounded text-white shadow-md">18+</span></template>
                                </div>
                                <div class="absolute top-1.5 left-1.5">
                                    <span class="bg-black/60 backdrop-blur text-white text-[8px] font-bold px-1.5 py-0.5 rounded border border-white/10" x-text="item.totalEps + ' Eps'"></span>
                                </div>

                                <div class="absolute bottom-0 w-full p-3">
                                    <h3 class="text-[10px] font-bold text-white leading-tight line-clamp-2" x-text="item.title"></h3>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>
                <div class="text-center mt-8" x-show="searchHasMore">
                    <button @click="loadMoreSearch()" class="bg-slate-800 border border-slate-700 hover:bg-slate-700 text-white text-xs font-bold py-3 px-8 rounded-full transition">MUAT LEBIH BANYAK</button>
                </div>
            </div>
        </template>

        <template x-if="view === 'favorites'">
            <div class="animate-enter">
                <button @click="view = 'home'" class="mb-6 text-xs font-bold text-slate-400 hover:text-white flex items-center gap-2">
                    <i class="fa-solid fa-arrow-left"></i> KEMBALI
                </button>
                <h2 class="text-lg font-black text-pink-500 uppercase tracking-wide mb-6">FAVORIT SAYA</h2>
                <template x-if="favorites.length === 0">
                    <div class="text-center py-20 bg-slate-900/50 rounded-2xl border border-dashed border-slate-700">
                        <i class="fa-regular fa-heart text-4xl text-slate-600 mb-4"></i>
                        <p class="text-slate-500 text-sm">Belum ada drama favorit.</p>
                    </div>
                </template>
                <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3">
                    <template x-for="item in favorites" :key="item.id">
                        <div class="group relative bg-[#0f172a] rounded-xl overflow-hidden cursor-pointer hover:ring-1 hover:ring-pink-500 transition">
                            <div @click="openDetail(item.id)" class="relative aspect-[3/4.5]">
                                <img :src="item.cover" class="w-full h-full object-cover">
                                <div class="absolute inset-0 card-gradient"></div>
                                <div class="absolute top-1.5 right-1.5">
                                    <button @click.stop="toggleFavorite(item)" class="bg-black/50 text-pink-500 w-6 h-6 rounded-full flex items-center justify-center hover:bg-white transition">
                                        <i class="fa-solid fa-trash text-[10px]"></i>
                                    </button>
                                </div>
                                <div class="absolute bottom-0 w-full p-3">
                                    <h3 class="text-[10px] font-bold text-white leading-tight line-clamp-2" x-text="item.title"></h3>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>
            </div>
        </template>

        <template x-if="view === 'detail'">
            <div x-cloak class="animate-enter pb-10">
                <div class="flex justify-between items-center mb-4">
                    <button @click="view = 'home'" class="text-xs font-bold text-slate-400 hover:text-white flex items-center gap-2">
                        <i class="fa-solid fa-arrow-left"></i> KEMBALI
                    </button>
                    <button @click="toggleFavorite({id: activeDrama.series_id_str, title: activeDrama.series_title, cover: activeDrama.series_cover, totalEps: activeDrama.episode_cnt, is18: activeDrama.age_gate_info?.age_gate>=18, genre: 'Drama'})" 
                            class="bg-slate-800 px-3 py-1.5 rounded-full text-xs font-bold transition flex items-center gap-2 hover:bg-slate-700">
                        <i :class="isFavorite(activeDrama.series_id_str) ? 'fa-solid text-pink-500' : 'fa-regular text-slate-400'" class="fa-heart"></i>
                        <span x-text="isFavorite(activeDrama.series_id_str) ? 'Tersimpan' : 'Simpan'"></span>
                    </button>
                </div>

                <div class="relative bg-[#0f172a] rounded-2xl overflow-hidden shadow-2xl border border-white/5">
                    <div class="absolute inset-0">
                        <img :src="activeDrama.series_cover" class="w-full h-full object-cover opacity-20 blur-2xl">
                        <div class="absolute inset-0 bg-gradient-to-t from-[#0f172a] via-[#0f172a]/90 to-transparent"></div>
                    </div>

                    <div class="relative z-10 p-6 md:p-8 flex flex-col md:flex-row gap-8 items-start">
                        <div class="w-40 md:w-56 flex-shrink-0 mx-auto md:mx-0 shadow-2xl rounded-xl overflow-hidden border border-white/10">
                            <img :src="activeDrama.series_cover" class="w-full h-full object-cover">
                        </div>

                        <div class="flex-1 w-full text-center md:text-left">
                            <h1 class="text-2xl md:text-4xl font-black text-white mb-4 leading-tight drop-shadow-lg" x-text="activeDrama.series_title"></h1>
                            
                            <div class="flex flex-wrap justify-center md:justify-start gap-2 mb-6">
                                <span class="bg-blue-600/90 text-white text-[10px] font-bold px-3 py-1 rounded-full shadow-lg" x-text="activeDrama.episode_cnt + ' Episodes'"></span>
                                <span x-show="activeDrama.age_gate_info?.age_gate >= 18" class="bg-red-600 text-white text-[10px] font-bold px-3 py-1 rounded-full shadow-lg">18+</span>
                                <span class="bg-slate-800 text-slate-300 text-[10px] font-bold px-3 py-1 rounded-full border border-white/10" x-text="formatNumber(activeDrama.followed_cnt) + ' Pengikut'"></span>
                            </div>

                            <div class="flex flex-wrap justify-center md:justify-start gap-1.5 mb-6">
                                <template x-for="cat in parseTags(activeDrama.category_schema)" :key="cat.category_id">
                                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-800/50 text-slate-300 border border-slate-700" x-text="cat.name"></span>
                                </template>
                            </div>

                            <div class="bg-black/20 p-4 rounded-xl border border-white/5 mb-6 text-left backdrop-blur-sm">
                                <template x-if="activeDrama.disclaimer_info?.content">
                                    <div class="flex gap-2 mb-2 pb-2 border-b border-white/10">
                                        <i class="fa-solid fa-triangle-exclamation text-red-500 text-xs mt-0.5"></i>
                                        <p class="text-[10px] text-red-300 font-bold uppercase">Info Konten: <span class="font-normal capitalize text-slate-300" x-text="activeDrama.disclaimer_info.content"></span></p>
                                    </div>
                                </template>
                                <p class="text-slate-300 text-xs leading-relaxed" x-text="activeDrama.series_intro"></p>
                            </div>

                            <h3 class="text-xs font-black text-slate-500 uppercase mb-4 tracking-widest flex items-center justify-center md:justify-start gap-2">
                                <span class="w-6 h-[2px] bg-blue-600"></span> PILIH EPISODE
                            </h3>
                            <div class="grid grid-cols-5 sm:grid-cols-8 md:grid-cols-10 gap-2 max-h-80 overflow-y-auto pr-1">
                                <template x-for="(eps, index) in activeDrama.video_list" :key="eps.vid">
                                    <button @click="openPlayer(index)" 
                                        class="group bg-[#1e293b] hover:bg-blue-600 border border-slate-700 hover:border-blue-500 p-2 rounded transition flex flex-col items-center justify-center relative">
                                        <span class="text-xs font-bold text-white" x-text="eps.vid_index"></span>
                                        <span class="text-[8px] text-slate-500 group-hover:text-blue-100 mt-0.5" x-text="formatTime(eps.duration)"></span>
                                    </button>
                                </template>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </template>

        <template x-if="view === 'player'">
            <div class="fixed inset-0 bg-black z-[9999] flex flex-col justify-center items-center select-none"
                 x-data="{ 
                    showControls: true, 
                    timer: null,
                    toggleControls() {
                        this.showControls = !this.showControls;
                        if(this.showControls) this.resetTimer();
                    },
                    resetTimer() {
                        clearTimeout(this.timer);
                        this.timer = setTimeout(() => this.showControls = false, 4000);
                    }
                 }"
                 x-init="resetTimer()"
                 @click="toggleControls()">
                
                <div class="absolute top-0 w-full p-4 flex justify-between z-20 bg-gradient-to-b from-black/90 to-transparent fade-transition"
                     :class="showControls ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4 pointer-events-none'">
                    
                    <button @click.stop="view = 'detail'" class="bg-white/10 backdrop-blur px-5 py-2 rounded-full text-[10px] font-bold text-white border border-white/10 hover:bg-red-600 hover:border-red-500 transition shadow-lg flex items-center gap-2 pointer-events-auto">
                        <i class="fa-solid fa-xmark"></i> TUTUP
                    </button>
                    
                    <div class="text-right">
                        <p class="text-[9px] font-bold text-slate-400 uppercase tracking-widest max-w-[150px] truncate" x-text="activeDrama.series_title"></p>
                        <p class="text-sm font-black text-blue-500 shadow-black drop-shadow-md" x-text="'EPISODE ' + activeDrama.video_list[currentIdx].vid_index"></p>
                    </div>
                </div>
                
                <div class="w-full h-full bg-black relative flex items-center justify-center">
                    <video x-ref="vPlayer" :src="streamUrl" @ended="nextEps" @error="handleError" autoplay controls playsinline class="w-full h-full object-contain"></video>
                </div>

                <div class="absolute bottom-16 w-full p-6 flex gap-4 bg-gradient-to-t from-black via-black/90 to-transparent z-20 pb-10 fade-transition"
                     :class="showControls ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'">
                    
                    <button @click.stop="prevEps()" :disabled="currentIdx === 0" 
                            class="pointer-events-auto flex-1 bg-slate-800/80 backdrop-blur hover:bg-slate-700 py-4 rounded-2xl font-bold text-[10px] disabled:opacity-30 border border-slate-600 text-white transition flex items-center justify-center gap-2">
                        <i class="fa-solid fa-backward"></i> SEBELUMNYA
                    </button>
                    
                    <button @click.stop="nextEps()" :disabled="currentIdx === activeDrama.video_list.length-1" 
                            class="pointer-events-auto flex-[2] bg-blue-600/90 backdrop-blur hover:bg-blue-500 py-4 rounded-2xl font-bold text-[10px] disabled:opacity-30 text-white shadow-xl shadow-blue-600/20 transition flex items-center justify-center gap-2">
                        EPISODE LANJUT <i class="fa-solid fa-forward"></i>
                    </button>
                </div>
            </div>
        </template>

    </main>

    <script>
        function albedoApp() {
            return {
                view: 'home', loading: false, searchQuery: '', toasts: [],
                favorites: JSON.parse(localStorage.getItem('albedo_fav') || '[]'),
                
                trending: [], trendingOffset: 0, trendingHasMore: true,
                latest: [], latestOffset: 0, latestHasMore: true,
                searchList: [], searchOffset: 0, searchHasMore: true,
                
                trendingIds: new Set(), latestIds: new Set(), searchIds: new Set(),
                activeDrama: null, streamUrl: '', backupUrl: '', currentIdx: 0,

                async init() {
                    this.loading = true;
                    await Promise.all([this.loadTrend(), this.loadLatest()]);
                    this.loading = false;
                },

                showToast(msg, icon='fa-solid fa-circle-check', color='text-blue-500') {
                    const id = Date.now();
                    this.toasts.push({id, msg, icon: `${icon} ${color}`});
                    setTimeout(() => this.toasts = this.toasts.filter(t => t.id !== id), 3000);
                },

                isFavorite(id) { return this.favorites.some(f => f.id === id); },
                toggleFavorite(item) {
                    if (this.isFavorite(item.id)) {
                        this.favorites = this.favorites.filter(f => f.id !== item.id);
                        this.showToast('Dihapus dari Favorit', 'fa-solid fa-trash', 'text-red-500');
                    } else {
                        const favItem = {
                            id: item.id,
                            title: item.title || item.book_name,
                            cover: item.cover || item.thumb_url,
                            genre: item.genre || 'Drama',
                            totalEps: item.totalEps || '?',
                            is18: item.is18
                        };
                        this.favorites.unshift(favItem);
                        this.showToast('Disimpan ke Favorit');
                    }
                    localStorage.setItem('albedo_fav', JSON.stringify(this.favorites));
                },

                normalize(raw, type) {
                    let id, title, cover, totalEps, is18, genre;
                    if (type === 'search') {
                        const book = raw.books[0]; 
                        id = raw.id; title = book.book_name; cover = book.thumb_url;
                        totalEps = book.serial_count || '?';
                        is18 = book.visibility_age_gate === '18';
                        genre = book.stat_infos ? book.stat_infos[0] : 'Drama';
                    } else {
                        id = raw.book_id; title = raw.book_name; cover = raw.thumb_url;
                        totalEps = raw.serial_count;
                        is18 = raw.visibility_age_gate === '18';
                        genre = raw.stat_infos ? raw.stat_infos[0] : 'Drama';
                    }
                    return { id, title, cover, totalEps, is18, genre };
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
                
                async openDetail(id) {
                    this.loading = true;
                    try {
                        const res = await fetch(`/api/detail?id=${id}`);
                        const json = await res.json();
                        this.activeDrama = json.data.video_data;
                        this.view = 'detail';
                        window.scrollTo(0,0);
                    } catch(e) { this.showToast('Gagal memuat detail', 'fa-solid fa-triangle-exclamation', 'text-red-500'); }
                    this.loading = false;
                },

                async openPlayer(idx) {
                    this.currentIdx = idx;
                    this.loading = true;
                    try {
                        const res = await fetch(`/api/stream?vid=${this.activeDrama.video_list[idx].vid}`);
                        const json = await res.json();
                        this.streamUrl = json.data.main_url;
                        this.backupUrl = json.data.backup_url;
                        this.view = 'player';
                    } catch(e) { this.showToast('Video rusak', 'fa-solid fa-link-slash', 'text-red-500'); }
                    this.loading = false;
                },

                handleError() { 
                    if(this.streamUrl !== this.backupUrl && this.backupUrl) {
                        this.showToast('Pindah ke server cadangan...');
                        this.streamUrl = this.backupUrl; 
                    } else { this.showToast('Gagal memutar video', 'fa-solid fa-xmark', 'text-red-500'); }
                },
                nextEps() { if(this.currentIdx < this.activeDrama.video_list.length-1) this.openPlayer(this.currentIdx+1); },
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
