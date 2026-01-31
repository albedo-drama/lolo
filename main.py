from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx

app = FastAPI()

# API Base URL
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
        .line-clamp-2 { overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
        video::-webkit-media-controls { display:none !important; }
        /* Animasi Loading Player */
        .loader { border: 4px solid rgba(255,255,255,0.1); border-left-color: #3b82f6; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body class="bg-[#050505] text-gray-200 font-sans" x-data="albedoApp()" x-init="init()">

    <nav class="fixed top-0 w-full z-50 bg-[#0f1014]/95 backdrop-blur border-b border-gray-800 shadow-lg">
        <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
            <h1 @click="resetHome()" class="text-xl font-black italic text-blue-600 cursor-pointer tracking-tighter">ALBEDO<span class="text-white">LOLO</span></h1>
            <div class="relative w-2/3 md:w-1/3">
                <input type="text" x-model="searchQuery" @keyup.enter="doSearch(true)" placeholder="Cari Judul..." 
                       class="w-full bg-[#1c1f26] border border-gray-700 rounded-full py-2 px-4 text-xs focus:border-blue-500 outline-none text-white transition">
                <i @click="doSearch(true)" class="fa-solid fa-magnifying-glass absolute right-4 top-2.5 text-gray-500 text-xs"></i>
            </div>
        </div>
    </nav>

    <div x-show="loading" class="fixed inset-0 bg-black/90 z-[9999] flex flex-col items-center justify-center gap-3">
        <div class="loader"></div>
        <p class="text-[10px] text-blue-500 font-bold animate-pulse tracking-widest">MEMUAT...</p>
    </div>

    <main class="max-w-7xl mx-auto p-4 pt-20 pb-24 min-h-screen">

        <template x-if="view === 'home'">
            <div class="space-y-10 animate-fade-in">
                <section>
                    <div class="flex items-center justify-between mb-4 border-l-4 border-orange-500 pl-3">
                        <h2 class="text-lg font-black text-white italic tracking-wider">TRENDING HOT</h2>
                    </div>
                    <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3">
                        <template x-for="item in trending" :key="item.id">
                            <div @click="openDetail(item.id)" class="group relative bg-[#15171c] rounded-lg overflow-hidden cursor-pointer hover:ring-1 hover:ring-orange-500 transition">
                                <div class="relative aspect-[3/4.5]">
                                    <img :src="item.cover" class="w-full h-full object-cover">
                                    <div class="absolute top-1 right-1 flex flex-col items-end gap-1">
                                        <template x-if="item.is18"><span class="bg-red-600 text-[8px] font-black px-1.5 py-0.5 rounded text-white shadow-md">18+</span></template>
                                        <template x-if="item.isFinished"><span class="bg-green-600 text-[8px] font-black px-1.5 py-0.5 rounded text-white shadow-md">TAMAT</span></template>
                                        <template x-if="!item.isFinished"><span class="bg-blue-600 text-[8px] font-black px-1.5 py-0.5 rounded text-white shadow-md">ONGOING</span></template>
                                    </div>
                                    <div class="absolute top-1 left-1"><span class="bg-black/60 text-white text-[8px] font-bold px-1.5 py-0.5 rounded backdrop-blur border border-white/10" x-text="item.totalEps + ' Eps'"></span></div>
                                    <div class="absolute bottom-0 w-full bg-gradient-to-t from-black to-transparent p-2 pt-8">
                                        <p class="text-[10px] font-bold text-white line-clamp-2 leading-tight" x-text="item.title"></p>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </div>
                    <div class="text-center mt-6" x-show="trendingHasMore">
                        <button @click="loadMoreTrending()" class="bg-[#1c1f26] border border-gray-700 text-[10px] font-bold py-2 px-6 rounded-full hover:bg-white hover:text-black transition">MUAT LAGI</button>
                    </div>
                </section>

                <section>
                    <div class="flex items-center justify-between mb-4 border-l-4 border-blue-500 pl-3">
                        <h2 class="text-lg font-black text-white italic tracking-wider">RILIS TERBARU</h2>
                    </div>
                    <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3">
                        <template x-for="item in latest" :key="item.id">
                            <div @click="openDetail(item.id)" class="group relative bg-[#15171c] rounded-lg overflow-hidden cursor-pointer hover:ring-1 hover:ring-blue-500 transition">
                                <div class="relative aspect-[3/4.5]">
                                    <img :src="item.cover" class="w-full h-full object-cover">
                                    <div class="absolute top-1 right-1 flex flex-col items-end gap-1">
                                        <template x-if="item.is18"><span class="bg-red-600 text-[8px] font-black px-1.5 py-0.5 rounded text-white shadow-md">18+</span></template>
                                        <template x-if="item.isFinished"><span class="bg-green-600 text-[8px] font-black px-1.5 py-0.5 rounded text-white shadow-md">TAMAT</span></template>
                                        <template x-if="!item.isFinished"><span class="bg-blue-600 text-[8px] font-black px-1.5 py-0.5 rounded text-white shadow-md">ONGOING</span></template>
                                    </div>
                                    <div class="absolute top-1 left-1"><span class="bg-black/60 text-white text-[8px] font-bold px-1.5 py-0.5 rounded backdrop-blur border border-white/10" x-text="item.totalEps + ' Eps'"></span></div>
                                    <div class="absolute bottom-0 w-full bg-gradient-to-t from-black to-transparent p-2 pt-8">
                                        <p class="text-[10px] font-bold text-white line-clamp-2 leading-tight" x-text="item.title"></p>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </div>
                    <div class="text-center mt-6" x-show="latestHasMore">
                        <button @click="loadMoreLatest()" class="bg-[#1c1f26] border border-gray-700 text-[10px] font-bold py-2 px-6 rounded-full hover:bg-white hover:text-black transition">MUAT LAGI</button>
                    </div>
                </section>
            </div>
        </template>

        <template x-if="view === 'search'">
            <div>
                <button @click="resetHome()" class="mb-4 text-[10px] font-bold text-gray-500 hover:text-white flex items-center gap-2 transition"><i class="fa-solid fa-arrow-left"></i> KEMBALI</button>
                <h2 class="text-lg font-black mb-4 uppercase italic">HASIL: <span class="text-blue-500" x-text="searchQuery"></span></h2>
                <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3">
                    <template x-for="item in searchList" :key="item.id">
                        <div @click="openDetail(item.id)" class="group relative bg-[#15171c] rounded-lg overflow-hidden cursor-pointer hover:ring-1 hover:ring-blue-500 transition">
                            <div class="relative aspect-[3/4.5]">
                                <img :src="item.cover" class="w-full h-full object-cover">
                                <div class="absolute top-1 right-1 flex flex-col items-end gap-1">
                                    <template x-if="item.is18"><span class="bg-red-600 text-[8px] font-black px-1.5 py-0.5 rounded text-white shadow-md">18+</span></template>
                                    <template x-if="item.isFinished"><span class="bg-green-600 text-[8px] font-black px-1.5 py-0.5 rounded text-white shadow-md">TAMAT</span></template>
                                    <template x-if="!item.isFinished"><span class="bg-blue-600 text-[8px] font-black px-1.5 py-0.5 rounded text-white shadow-md">ONGOING</span></template>
                                </div>
                                <div class="absolute top-1 left-1"><span class="bg-black/60 text-white text-[8px] font-bold px-1.5 py-0.5 rounded backdrop-blur border border-white/10" x-text="item.totalEps + ' Eps'"></span></div>
                                <div class="absolute bottom-0 w-full bg-gradient-to-t from-black to-transparent p-2 pt-8">
                                    <p class="text-[10px] font-bold text-white line-clamp-2 leading-tight" x-text="item.title"></p>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>
                <div class="text-center mt-6" x-show="searchHasMore">
                    <button @click="loadMoreSearch()" class="bg-[#1c1f26] border border-gray-700 text-[10px] font-bold py-2 px-6 rounded-full hover:bg-white hover:text-black transition">MUAT LEBIH BANYAK</button>
                </div>
            </div>
        </template>

        <template x-if="view === 'detail'">
            <div x-cloak class="animate-fade-in">
                <button @click="view = 'home'" class="mb-4 text-[10px] font-bold text-gray-500 hover:text-white flex items-center gap-2"><i class="fa-solid fa-arrow-left"></i> KEMBALI</button>
                <div class="bg-[#151515] rounded-xl p-5 border border-gray-800 shadow-2xl flex flex-col md:flex-row gap-6 relative overflow-hidden">
                    <div class="absolute top-0 right-0 w-full h-full bg-gradient-to-bl from-blue-900/10 to-transparent pointer-events-none"></div>
                    <div class="w-40 md:w-56 flex-shrink-0 mx-auto md:mx-0 relative z-10">
                        <img :src="activeDrama.series_cover" class="w-full rounded-lg shadow-2xl border border-gray-700">
                    </div>
                    <div class="flex-1 relative z-10 text-center md:text-left">
                        <h1 class="text-2xl font-black text-white mb-2 leading-tight" x-text="activeDrama.series_title"></h1>
                        <div class="flex flex-wrap justify-center md:justify-start gap-2 mb-4">
                            <span class="bg-blue-600 text-white text-[10px] font-bold px-2 py-1 rounded shadow" x-text="activeDrama.episode_cnt + ' EPS'"></span>
                            <span x-show="activeDrama.age_gate_info.age_gate >= 18" class="bg-red-600 text-white text-[10px] font-bold px-2 py-1 rounded shadow">18+</span>
                            <span class="bg-gray-800 text-gray-400 text-[10px] font-bold px-2 py-1 rounded border border-gray-700" x-text="formatNumber(activeDrama.followed_cnt) + ' Likes'"></span>
                        </div>
                        <div class="bg-black/30 p-3 rounded-lg border border-white/5 mb-5 text-left">
                             <p class="text-gray-400 text-xs leading-relaxed" x-text="activeDrama.series_intro"></p>
                        </div>
                        <h3 class="text-[10px] font-bold text-gray-500 uppercase mb-3 text-left tracking-widest">Pilih Episode</h3>
                        <div class="grid grid-cols-5 sm:grid-cols-8 md:grid-cols-10 gap-2">
                            <template x-for="(eps, index) in activeDrama.video_list" :key="eps.vid">
                                <button @click="openPlayer(index)" class="bg-[#202020] hover:bg-blue-600 p-2 rounded text-[10px] font-bold text-white transition border border-gray-700 hover:border-blue-500"><span x-text="eps.vid_index"></span></button>
                            </template>
                        </div>
                    </div>
                </div>
            </div>
        </template>

        <template x-if="view === 'player'">
            <div class="fixed inset-0 bg-black z-[9999] flex flex-col">
                
                <div class="flex-1 relative w-full h-full flex items-center justify-center bg-black">
                    <div class="absolute top-0 w-full p-4 flex justify-between z-20 bg-gradient-to-b from-black/90 to-transparent">
                        <button @click="view = 'detail'" class="bg-white/10 backdrop-blur px-4 py-2 rounded-full text-[10px] font-bold text-white border border-white/10 hover:bg-red-600 transition">✕ TUTUP</button>
                        <div class="text-right">
                            <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest truncate max-w-[150px]" x-text="activeDrama.series_title"></p>
                            <p class="text-xs font-black text-blue-500" x-text="'EPS ' + activeDrama.video_list[currentIdx].vid_index"></p>
                        </div>
                    </div>

                    <video x-ref="vPlayer" :src="streamUrl" @ended="nextEps" @error="handleError" autoplay controls playsinline class="w-full h-full object-contain focus:outline-none"></video>
                </div>

                <div class="absolute bottom-0 w-full p-6 flex gap-3 bg-gradient-to-t from-black via-black/80 to-transparent z-20 pb-8">
                    <button @click="prevEps()" :disabled="currentIdx === 0" class="flex-1 bg-[#202020]/90 backdrop-blur hover:bg-gray-700 py-3 rounded-xl font-bold text-[10px] disabled:opacity-30 border border-gray-700 text-white transition">
                        <i class="fa-solid fa-backward mr-2"></i> PREV
                    </button>
                    <button @click="nextEps()" :disabled="currentIdx === activeDrama.video_list.length-1" class="flex-[2] bg-blue-600/90 backdrop-blur hover:bg-blue-500 py-3 rounded-xl font-bold text-[10px] disabled:opacity-30 text-white shadow-lg shadow-blue-500/30 transition">
                        NEXT EPISODE <i class="fa-solid fa-forward ml-2"></i>
                    </button>
                </div>
            </div>
        </template>

    </main>

    <script>
        function albedoApp() {
            return {
                view: 'home', loading: false, searchQuery: '',
                trending: [], trendingOffset: 0, trendingHasMore: true,
                latest: [], latestOffset: 0, latestHasMore: true,
                searchList: [], searchOffset: 0, searchHasMore: true,
                activeDrama: null, streamUrl: '', backupUrl: '', currentIdx: 0,

                async init() {
                    this.loading = true;
                    await Promise.all([this.loadTrend(), this.loadLatest()]);
                    this.loading = false;
                },

                // NORMALISASI DATA (Search & Home jadi SATU format)
                normalize(raw, type) {
                    let id, title, cover, totalEps, isFinished, is18;
                    if (type === 'search') {
                        const book = raw.books[0]; 
                        id = raw.id; title = book.book_name; cover = book.thumb_url;
                        totalEps = book.serial_count || '?';
                        // Fix deteksi TAMAT/18+ di search result
                        isFinished = book.show_creation_status === 'Selesai' || (book.stat_infos && book.stat_infos.includes('Selesai'));
                        is18 = book.visibility_age_gate === '18';
                    } else {
                        id = raw.book_id; title = raw.book_name; cover = raw.thumb_url;
                        totalEps = raw.serial_count;
                        isFinished = raw.show_creation_status === 'Selesai';
                        is18 = raw.visibility_age_gate === '18';
                    }
                    return { id, title, cover, totalEps, isFinished, is18 };
                },

                async loadTrend() {
                    const res = await fetch(`/api/trending?offset=${this.trendingOffset}`);
                    const json = await res.json();
                    const newItems = json.books.map(b => this.normalize(b, 'home'));
                    this.trending = [...this.trending, ...newItems];
                    this.trendingOffset = json.next_offset; this.trendingHasMore = json.has_more;
                },
                async loadMoreTrending() { this.loading=true; await this.loadTrend(); this.loading=false; },

                async loadLatest() {
                    const res = await fetch(`/api/latest?offset=${this.latestOffset}`);
                    const json = await res.json();
                    const newItems = json.books.map(b => this.normalize(b, 'home'));
                    this.latest = [...this.latest, ...newItems];
                    this.latestOffset = json.next_offset; this.latestHasMore = json.has_more;
                },
                async loadMoreLatest() { this.loading=true; await this.loadLatest(); this.loading=false; },

                async doSearch(isNew = false) {
                    if(!this.searchQuery) return;
                    if(isNew) { this.searchList = []; this.searchOffset = 0; this.searchHasMore = true; }
                    this.view = 'search'; this.loading = true;
                    try {
                        const res = await fetch(`/api/search?q=${this.searchQuery}&offset=${this.searchOffset}`);
                        const json = await res.json();
                        if(json.data && json.data.search_data) {
                            const newItems = json.data.search_data.map(b => this.normalize(b, 'search'));
                            this.searchList = [...this.searchList, ...newItems];
                            this.searchOffset = json.data.next_offset;
                            this.searchHasMore = json.data.has_more;
                        } else { this.searchHasMore = false; }
                    } catch(e) { console.error(e); }
                    this.loading = false;
                },
                async loadMoreSearch() { await this.doSearch(false); },

                resetHome() { this.searchQuery = ''; this.view = 'home'; },
                
                async openDetail(id) {
                    this.loading = true;
                    try {
                        const res = await fetch(`/api/detail?id=${id}`);
                        const json = await res.json();
                        this.activeDrama = json.data.video_data;
                        this.view = 'detail';
                        window.scrollTo(0,0);
                    } catch(e) { alert('Gagal memuat detail'); }
                    this.loading = false;
                },

                async openPlayer(idx) {
                    this.currentIdx = idx; this.loading = true;
                    try {
                        const res = await fetch(`/api/stream?vid=${this.activeDrama.video_list[idx].vid}`);
                        const json = await res.json();
                        this.streamUrl = json.data.main_url;
                        this.backupUrl = json.data.backup_url;
                        this.view = 'player';
                    } catch(e) { alert('Video error'); }
                    this.loading = false;
                },

                handleError() { if(this.streamUrl !== this.backupUrl && this.backupUrl) this.streamUrl = this.backupUrl; },
                nextEps() { if(this.currentIdx < this.activeDrama.video_list.length-1) this.openPlayer(this.currentIdx+1); },
                prevEps() { if(this.currentIdx > 0) this.openPlayer(this.currentIdx-1); },
                formatNumber(num) { return new Intl.NumberFormat('id-ID', { notation: "compact" }).format(num); }
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
        return (await client.get(f"{API_BASE}/latest?offset={offset}&limit=10&gender=1", headers=HEADERS)).json()

@app.get("/api/trending")
async def trending(offset: int = 0):
    async with httpx.AsyncClient() as client:
        return (await client.get(f"{API_BASE}/trending?offset={offset}&limit=10&gender=1", headers=HEADERS)).json()

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
