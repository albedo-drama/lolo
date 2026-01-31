from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import httpx
import json

app = FastAPI()

# Konfigurasi API Target
API_BASE = "https://api.sansekai.my.id/api/melolo"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# --- HTML TEMPLATE (Frontend) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ALBEDOLOLO-TV | Premium Stream</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        [x-cloak] { display: none !important; }
        .hide-scroll::-webkit-scrollbar { display: none; }
        .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); }
        .line-clamp-2 { overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
    </style>
</head>
<body class="bg-[#0b0c15] text-gray-200 font-sans selection:bg-blue-500 selection:text-white" x-data="albedoApp()" x-init="init()">

    <nav class="sticky top-0 z-50 glass border-b border-gray-800/50 shadow-2xl">
        <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center gap-4">
            <div @click="view = 'home'; window.scrollTo(0,0)" class="flex items-center gap-2 cursor-pointer group">
                <i class="fa-solid fa-play-circle text-blue-500 text-2xl group-hover:scale-110 transition"></i>
                <h1 class="text-xl font-black tracking-tighter bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">ALBEDOLOLO-TV</h1>
            </div>
            
            <div class="relative w-full max-w-md hidden md:block">
                <input type="text" x-model="searchQuery" @keyup.enter="search()" placeholder="Cari Drama, CEO, Genre..." 
                       class="w-full bg-[#151921] border border-gray-700 rounded-full py-2 px-5 text-sm focus:outline-none focus:border-blue-500 transition shadow-inner">
                <i @click="search()" class="fa-solid fa-magnifying-glass absolute right-4 top-2.5 text-gray-500 cursor-pointer hover:text-white"></i>
            </div>
            
            <button @click="searchModal = true" class="md:hidden text-gray-300"><i class="fa-solid fa-magnifying-glass text-xl"></i></button>
        </div>
    </nav>

    <div x-show="searchModal" x-cloak class="fixed inset-0 z-[60] bg-black/90 p-4 flex flex-col pt-20" x-transition>
        <button @click="searchModal = false" class="absolute top-5 right-5 text-white text-2xl">✕</button>
        <input type="text" x-model="searchQuery" @keyup.enter="search(); searchModal = false" placeholder="Cari judul..." 
               class="w-full bg-gray-800 text-white text-xl p-4 rounded-xl border border-gray-700 mb-4 outline-none">
        <button @click="search(); searchModal = false" class="bg-blue-600 text-white font-bold py-3 rounded-xl">CARI SEKARANG</button>
    </div>

    <main class="max-w-7xl mx-auto p-4 min-h-screen">
        
        <div x-show="loading" class="fixed inset-0 bg-black/80 flex items-center justify-center z-[100]" x-transition>
            <div class="flex flex-col items-center gap-4">
                <div class="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                <p class="text-xs font-bold tracking-widest animate-pulse">MEMUAT DATA...</p>
            </div>
        </div>

        <template x-if="view === 'home'">
            <div class="space-y-12 animate-fade-in">
                <section>
                    <div class="flex items-center gap-2 mb-6">
                        <i class="fa-solid fa-fire text-orange-500"></i>
                        <h2 class="text-xl font-bold text-white tracking-wide">SEDANG TRENDING</h2>
                    </div>
                    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                        <template x-for="item in trending" :key="item.book_id">
                            <div @click="openDetail(item.book_id)" class="group cursor-pointer relative">
                                <div class="relative overflow-hidden rounded-xl aspect-[2/3] shadow-lg border border-gray-800 group-hover:border-blue-500 transition">
                                    <img :src="item.thumb_url" class="w-full h-full object-cover transform group-hover:scale-110 transition duration-500">
                                    <div class="absolute top-2 right-2 flex flex-col gap-1 items-end">
                                        <template x-if="item.status_finish">
                                            <span class="bg-green-600 text-[9px] font-bold px-2 py-0.5 rounded shadow">TAMAT</span>
                                        </template>
                                        <template x-if="item.is_adult">
                                            <span class="bg-red-600 text-[9px] font-bold px-2 py-0.5 rounded shadow">18+</span>
                                        </template>
                                    </div>
                                    <div class="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black via-black/70 to-transparent p-3 pt-10">
                                        <p class="text-xs font-bold text-white line-clamp-2 leading-tight" x-text="item.book_name"></p>
                                        <p class="text-[10px] text-gray-400 mt-1 truncate" x-text="item.tags"></p>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </div>
                </section>

                <section>
                    <div class="flex items-center gap-2 mb-6">
                        <i class="fa-solid fa-clock text-blue-500"></i>
                        <h2 class="text-xl font-bold text-white tracking-wide">RILIS TERBARU</h2>
                    </div>
                    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                        <template x-for="item in latest" :key="item.book_id">
                            <div @click="openDetail(item.book_id)" class="group cursor-pointer">
                                <div class="relative overflow-hidden rounded-xl aspect-[2/3] shadow-lg border border-gray-800">
                                    <img :src="item.thumb_url" class="w-full h-full object-cover group-hover:opacity-80 transition">
                                    <div class="absolute bottom-2 left-2 right-2">
                                        <p class="text-xs font-bold text-white drop-shadow-md truncate" x-text="item.book_name"></p>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </div>
                </section>
            </div>
        </template>

        <template x-if="view === 'search'">
            <div>
                <button @click="view = 'home'" class="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition">
                    <i class="fa-solid fa-arrow-left"></i> KEMBALI
                </button>
                <h2 class="text-xl font-bold mb-6">HASIL: <span class="text-blue-500" x-text="searchQuery"></span></h2>
                
                <template x-if="searchResults.length === 0">
                    <div class="text-center py-20 text-gray-500">
                        <i class="fa-regular fa-folder-open text-4xl mb-4"></i>
                        <p>Tidak ada drama ditemukan.</p>
                    </div>
                </template>

                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
                    <template x-for="item in searchResults" :key="item.id">
                        <div @click="openDetail(item.id)" class="group cursor-pointer">
                            <div class="relative overflow-hidden rounded-xl aspect-[2/3] border border-gray-800">
                                <img :src="item.books[0].thumb_url" class="w-full h-full object-cover">
                                <div class="absolute bottom-0 w-full bg-black/60 p-2">
                                    <p class="text-xs font-bold truncate" x-text="item.books[0].book_name"></p>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>
            </div>
        </template>

        <template x-if="view === 'detail'">
            <div class="animate-fade-in pb-20">
                <button @click="view = 'home'" class="mb-6 flex items-center gap-2 text-sm font-bold text-gray-500 hover:text-white">
                    <i class="fa-solid fa-chevron-left"></i> KEMBALI KE BERANDA
                </button>

                <div class="flex flex-col md:flex-row gap-8 bg-[#151921] p-6 rounded-2xl border border-gray-800 shadow-2xl relative overflow-hidden">
                    <div class="absolute top-0 right-0 w-full h-full bg-gradient-to-bl from-blue-900/10 to-transparent pointer-events-none"></div>

                    <div class="w-full md:w-64 flex-shrink-0 relative z-10">
                        <img :src="activeDrama.series_cover" class="w-full rounded-xl shadow-2xl border border-gray-700">
                        <div class="absolute top-3 left-3 flex flex-col gap-2">
                            <span x-show="activeDrama.series_status === 1" class="bg-blue-600 text-white text-[10px] font-bold px-3 py-1 rounded-full shadow-lg">ONGOING</span>
                            <span x-show="activeDrama.age_gate_info.age_gate >= 18" class="bg-red-600 text-white text-[10px] font-bold px-3 py-1 rounded-full shadow-lg">18+</span>
                        </div>
                    </div>

                    <div class="flex-1 relative z-10">
                        <h1 class="text-3xl md:text-4xl font-black mb-4 text-white leading-tight" x-text="activeDrama.series_title"></h1>
                        
                        <div class="flex flex-wrap gap-2 mb-6">
                            <template x-for="cat in parseTags(activeDrama.category_schema)" :key="cat.category_id">
                                <span class="bg-gray-800 text-blue-400 border border-gray-700 px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider hover:bg-gray-700 transition" x-text="cat.name"></span>
                            </template>
                        </div>

                        <template x-if="activeDrama.disclaimer_info">
                            <div class="bg-red-900/20 border border-red-900/50 p-3 rounded-lg mb-6 flex gap-3 items-start">
                                <i class="fa-solid fa-triangle-exclamation text-red-500 mt-1"></i>
                                <div>
                                    <p class="text-red-400 text-xs font-bold uppercase">Peringatan Konten</p>
                                    <p class="text-gray-400 text-xs" x-text="activeDrama.disclaimer_info.content"></p>
                                </div>
                            </div>
                        </template>

                        <p class="text-gray-400 text-sm leading-7 mb-6" x-text="activeDrama.series_intro"></p>
                        
                        <div class="flex items-center gap-6 text-sm text-gray-500 font-bold border-t border-gray-800 pt-4">
                            <span><i class="fa-solid fa-layer-group mr-2"></i> <span x-text="activeDrama.episode_cnt"></span> Eps</span>
                            <span><i class="fa-solid fa-thumbs-up mr-2"></i> <span x-text="formatNumber(activeDrama.followed_cnt)"></span> Pengikut</span>
                        </div>
                    </div>
                </div>

                <div class="mt-8">
                    <h3 class="text-lg font-bold mb-4 flex items-center gap-2"><i class="fa-solid fa-list-ul text-blue-500"></i> DAFTAR EPISODE</h3>
                    <div class="grid grid-cols-3 sm:grid-cols-5 md:grid-cols-8 lg:grid-cols-10 gap-3">
                        <template x-for="(eps, index) in activeDrama.video_list" :key="eps.vid">
                            <button @click="stream(index)" class="group relative bg-[#151921] hover:bg-blue-600 border border-gray-800 hover:border-blue-500 p-3 rounded-lg text-center transition-all duration-300">
                                <div class="text-xs font-black text-white mb-1">EPS <span x-text="eps.vid_index"></span></div>
                                <div class="flex justify-center items-center gap-2 text-[9px] text-gray-400 group-hover:text-blue-200">
                                    <span><i class="fa-regular fa-clock"></i> <span x-text="formatDuration(eps.duration)"></span></span>
                                </div>
                                <div class="text-[9px] text-gray-500 group-hover:text-white mt-1">
                                    <i class="fa-solid fa-heart text-red-500"></i> <span x-text="formatNumber(eps.digged_count)"></span>
                                </div>
                            </button>
                        </template>
                    </div>
                </div>
            </div>
        </template>

        <template x-if="view === 'stream'">
            <div class="fixed inset-0 bg-black z-[200] flex flex-col items-center justify-center">
                <div class="absolute top-0 w-full bg-gradient-to-b from-black/90 to-transparent p-4 z-10 flex justify-between items-center">
                    <button @click="view = 'detail'" class="bg-white/10 hover:bg-white/20 backdrop-blur text-white px-4 py-2 rounded-full text-xs font-bold transition">
                        ✕ TUTUP PLAYER
                    </button>
                    <div class="text-right">
                        <p class="text-[10px] text-gray-400 uppercase font-bold tracking-widest" x-text="activeDrama.series_title"></p>
                        <p class="text-sm font-black text-blue-400" x-text="'EPISODE ' + activeDrama.video_list[currentIdx].vid_index"></p>
                    </div>
                </div>

                <div class="w-full max-w-lg aspect-[9/16] relative bg-black shadow-2xl">
                    <video x-ref="player" :src="streamUrl" 
                           @error="handleError" 
                           @ended="nextEps"
                           controls autoplay 
                           class="w-full h-full object-contain">
                    </video>
                    
                    <div x-show="buffering" class="absolute inset-0 flex items-center justify-center pointer-events-none">
                        <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
                    </div>
                </div>

                <div class="absolute bottom-10 w-full max-w-lg px-4 flex justify-between gap-4">
                    <button @click="prevEps()" :disabled="currentIdx === 0" 
                            class="flex-1 bg-gray-800/80 hover:bg-gray-700 backdrop-blur py-3 rounded-xl font-bold text-xs disabled:opacity-30 transition">
                        <i class="fa-solid fa-backward-step mr-2"></i> SEBELUMNYA
                    </button>
                    <button @click="nextEps()" :disabled="currentIdx === activeDrama.video_list.length - 1" 
                            class="flex-1 bg-blue-600/90 hover:bg-blue-600 backdrop-blur py-3 rounded-xl font-bold text-xs disabled:opacity-30 transition shadow-lg shadow-blue-500/30">
                        SELANJUTNYA <i class="fa-solid fa-forward-step ml-2"></i>
                    </button>
                </div>
            </div>
        </template>

    </main>

    <footer class="text-center py-8 text-gray-600 text-xs border-t border-gray-800 mt-10">
        <p>&copy; 2024 ALBEDOLOLO-TV. Stream Drama Premium.</p>
    </footer>

    <script>
        function albedoApp() {
            return {
                view: 'home',
                loading: false,
                buffering: false,
                searchModal: false,
                latest: [],
                trending: [],
                searchResults: [],
                searchQuery: '',
                activeDrama: null,
                streamUrl: '',
                backupUrl: '',
                currentIdx: 0,
                
                async init() {
                    this.loading = true;
                    try {
                        const [l, t] = await Promise.all([
                            fetch('/api/latest').then(r => r.json()),
                            fetch('/api/trending').then(r => r.json())
                        ]);
                        this.latest = l.books.map(this.processBook);
                        this.trending = t.books.map(this.processBook);
                    } catch (e) { console.error(e); }
                    this.loading = false;
                },

                // Helper memproses data buku (Hidden Gems extraction)
                processBook(book) {
                    let tags = "Drama";
                    if (book.stat_infos && book.stat_infos.length > 0) tags = book.stat_infos[0];
                    return {
                        ...book,
                        tags: tags,
                        is_adult: book.visibility_age_gate === "18",
                        status_finish: book.show_creation_status === "Selesai"
                    };
                },

                async search() {
                    if(!this.searchQuery) return;
                    this.loading = true;
                    this.view = 'search';
                    try {
                        const res = await fetch(`/api/search?q=${this.searchQuery}`);
                        const data = await res.json();
                        this.searchResults = data.data.search_data;
                    } catch (e) { alert('Gagal mencari data'); }
                    this.loading = false;
                },

                async openDetail(id) {
                    this.loading = true;
                    try {
                        const res = await fetch(`/api/detail?id=${id}`);
                        const data = await res.json();
                        this.activeDrama = data.data.video_data;
                        this.view = 'detail';
                        window.scrollTo(0,0);
                    } catch (e) { alert('Gagal memuat detail'); }
                    this.loading = false;
                },

                async stream(idx) {
                    this.currentIdx = idx;
                    this.buffering = true;
                    const vid = this.activeDrama.video_list[idx].vid;
                    try {
                        const res = await fetch(`/api/stream?vid=${vid}`);
                        const data = await res.json();
                        this.streamUrl = data.data.main_url;
                        this.backupUrl = data.data.backup_url; // Simpan backup URL
                        this.view = 'stream';
                    } catch (e) { alert('Gagal memuat video'); }
                    this.buffering = false;
                },

                handleError() {
                    // Fitur Anti-Mati: Switch ke Backup URL jika Main error
                    if (this.streamUrl !== this.backupUrl && this.backupUrl) {
                        console.log("Switching to backup URL...");
                        this.streamUrl = this.backupUrl;
                    } else {
                        console.error("Video failed to load.");
                    }
                },

                nextEps() {
                    if (this.currentIdx < this.activeDrama.video_list.length - 1) {
                        this.stream(this.currentIdx + 1);
                    }
                },

                prevEps() {
                    if (this.currentIdx > 0) {
                        this.stream(this.currentIdx - 1);
                    }
                },

                // Utilities
                formatNumber(num) {
                    return new Intl.NumberFormat('id-ID', { notation: "compact" }).format(num);
                },
                formatDuration(seconds) {
                    const m = Math.floor(seconds / 60);
                    const s = seconds % 60;
                    return `${m}:${s.toString().padStart(2, '0')}`;
                },
                parseTags(schemaString) {
                    try {
                        return JSON.parse(schemaString);
                    } catch (e) { return []; }
                }
            }
        }
    </script>
</body>
</html>
"""

# --- BACKEND PROXY (FastAPI) ---

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_TEMPLATE

@app.get("/api/latest")
async def proxy_latest():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_BASE}/latest", headers=HEADERS)
        return r.json()

@app.get("/api/trending")
async def proxy_trending():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_BASE}/trending", headers=HEADERS)
        return r.json()

@app.get("/api/search")
async def proxy_search(q: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_BASE}/search?query={q}&limit=20&offset=0", headers=HEADERS)
        return r.json()

@app.get("/api/detail")
async def proxy_detail(id: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_BASE}/detail?bookId={id}", headers=HEADERS)
        return r.json()

@app.get("/api/stream")
async def proxy_stream(vid: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_BASE}/stream?videoId={vid}", headers=HEADERS)
        return r.json()
