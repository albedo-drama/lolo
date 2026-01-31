from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx

app = FastAPI()

# API Base URL
API_BASE = "https://api.sansekai.my.id/api/melolo"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
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
        /* Hilangkan kontrol bawaan video player biar bersih */
        video::-webkit-media-controls { display:none !important; }
    </style>
</head>
<body class="bg-[#050505] text-gray-200 font-sans selection:bg-blue-500 selection:text-white" x-data="albedoApp()" x-init="init()">

    <nav class="sticky top-0 z-50 bg-[#0f1014]/95 backdrop-blur border-b border-gray-800 shadow-lg">
        <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
            <div @click="resetHome()" class="flex items-center gap-2 cursor-pointer group">
                <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center group-hover:rotate-12 transition">
                    <i class="fa-solid fa-play text-white text-xs"></i>
                </div>
                <h1 class="text-xl font-black italic tracking-tighter text-white">
                    ALBEDOLOLO<span class="text-blue-500">-TV</span>
                </h1>
            </div>
            
            <div class="relative w-1/2 md:w-1/3">
                <input type="text" x-model="searchQuery" @keyup.enter="doSearch(true)" placeholder="Cari Drama / CEO..." 
                       class="w-full bg-[#1c1f26] border border-gray-700 rounded-full py-2 px-4 text-xs focus:border-blue-500 outline-none transition text-white placeholder-gray-500">
                <i @click="doSearch(true)" class="fa-solid fa-magnifying-glass absolute right-4 top-2.5 text-gray-500 text-xs cursor-pointer hover:text-white"></i>
            </div>
        </div>
    </nav>

    <div x-show="loading" class="fixed inset-0 bg-black/90 z-[9999] flex flex-col gap-3 items-center justify-center">
        <div class="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
        <p class="text-xs font-bold text-blue-500 animate-pulse">MEMUAT DATA...</p>
    </div>

    <main class="max-w-7xl mx-auto p-4 pb-24 min-h-screen">

        <template x-if="view === 'home'">
            <div class="space-y-12 animate-fade-in">
                
                <section>
                    <div class="flex items-center justify-between mb-4 border-l-4 border-orange-500 pl-3">
                        <h2 class="text-lg font-black text-white italic tracking-wider">SEDANG TRENDING</h2>
                    </div>
                    
                    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3 md:gap-4">
                        <template x-for="item in trendingList" :key="item.id + '_trend'">
                            <div @click="openDetail(item.id)" class="group cursor-pointer relative bg-[#15171c] rounded-xl overflow-hidden shadow-lg hover:shadow-orange-500/20 transition duration-300">
                                <div class="relative aspect-[3/4.5] overflow-hidden">
                                    <img :src="item.cover" class="w-full h-full object-cover group-hover:scale-110 transition duration-500">
                                    <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-transparent to-transparent"></div>
                                    <div class="absolute top-2 right-2 flex flex-col items-end gap-1">
                                        <template x-if="item.is18"><span class="bg-red-600 text-white text-[9px] font-bold px-1.5 py-0.5 rounded shadow">18+</span></template>
                                        <template x-if="item.isFinished"><span class="bg-green-600 text-white text-[9px] font-bold px-1.5 py-0.5 rounded shadow">TAMAT</span></template>
                                    </div>
                                    <div class="absolute top-2 left-2">
                                        <span class="bg-black/60 backdrop-blur text-orange-400 text-[9px] font-bold px-1.5 py-0.5 rounded border border-orange-500/30">
                                            <i class="fa-solid fa-fire mr-1"></i>HOT
                                        </span>
                                    </div>
                                </div>
                                <div class="p-3 absolute bottom-0 w-full">
                                    <h3 class="text-[11px] font-bold text-white leading-tight line-clamp-2 mb-1 group-hover:text-orange-400 transition" x-text="item.title"></h3>
                                    <p class="text-[9px] text-gray-400 truncate" x-text="item.genre"></p>
                                </div>
                            </div>
                        </template>
                    </div>

                    <div class="text-center mt-6" x-show="trendingHasMore">
                        <button @click="loadMoreTrending()" class="bg-[#1c1f26] hover:bg-orange-600 hover:text-white border border-gray-700 text-gray-300 text-xs font-bold py-2.5 px-8 rounded-full transition shadow-lg flex items-center gap-2 mx-auto">
                            <span>MUAT LAGI</span> <i class="fa-solid fa-chevron-down"></i>
                        </button>
                    </div>
                </section>

                <section>
                    <div class="flex items-center justify-between mb-4 border-l-4 border-blue-500 pl-3">
                        <h2 class="text-lg font-black text-white italic tracking-wider">RILIS TERBARU</h2>
                    </div>

                    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3 md:gap-4">
                        <template x-for="item in latestList" :key="item.id + '_latest'">
                            <div @click="openDetail(item.id)" class="group cursor-pointer relative bg-[#15171c] rounded-xl overflow-hidden shadow-lg hover:shadow-blue-500/20 transition duration-300">
                                <div class="relative aspect-[3/4.5] overflow-hidden">
                                    <img :src="item.cover" class="w-full h-full object-cover group-hover:scale-110 transition duration-500">
                                    <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-transparent to-transparent"></div>
                                    <div class="absolute top-2 right-2 flex flex-col items-end gap-1">
                                        <template x-if="item.is18"><span class="bg-red-600 text-white text-[9px] font-bold px-1.5 py-0.5 rounded shadow">18+</span></template>
                                        <template x-if="item.isFinished"><span class="bg-green-600 text-white text-[9px] font-bold px-1.5 py-0.5 rounded shadow">TAMAT</span></template>
                                    </div>
                                </div>
                                <div class="p-3 absolute bottom-0 w-full">
                                    <h3 class="text-[11px] font-bold text-white leading-tight line-clamp-2 mb-1 group-hover:text-blue-400 transition" x-text="item.title"></h3>
                                    <p class="text-[9px] text-gray-400 truncate" x-text="item.genre"></p>
                                </div>
                            </div>
                        </template>
                    </div>

                    <div class="text-center mt-6" x-show="latestHasMore">
                        <button @click="loadMoreLatest()" class="bg-[#1c1f26] hover:bg-blue-600 hover:text-white border border-gray-700 text-gray-300 text-xs font-bold py-2.5 px-8 rounded-full transition shadow-lg flex items-center gap-2 mx-auto">
                            <span>MUAT LAGI</span> <i class="fa-solid fa-chevron-down"></i>
                        </button>
                    </div>
                </section>

            </div>
        </template>

        <template x-if="view === 'search'">
            <div class="animate-fade-in">
                <button @click="resetHome()" class="mb-6 text-xs font-bold text-gray-500 hover:text-white flex items-center gap-2">
                    <i class="fa-solid fa-arrow-left"></i> KEMBALI KE BERANDA
                </button>
                <div class="border-b border-gray-800 pb-4 mb-6">
                    <h2 class="text-xl font-black uppercase text-white">HASIL: <span class="text-blue-500" x-text="searchQuery"></span></h2>
                </div>
                
                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3 md:gap-4">
                    <template x-for="item in searchList" :key="item.id">
                        <div @click="openDetail(item.id)" class="group cursor-pointer relative bg-[#15171c] rounded-xl overflow-hidden border border-gray-800 hover:border-blue-500 transition">
                            <div class="relative aspect-[3/4.5]">
                                <img :src="item.cover" class="w-full h-full object-cover">
                                <div class="absolute bottom-0 w-full bg-black/80 p-2 text-center">
                                    <h3 class="text-[10px] font-bold text-white truncate" x-text="item.title"></h3>
                                </div>
                                <div class="absolute top-2 right-2">
                                     <template x-if="item.isFinished"><span class="bg-green-600 text-white text-[8px] font-bold px-1.5 py-0.5 rounded">TAMAT</span></template>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>

                <div class="text-center mt-8" x-show="searchHasMore">
                    <button @click="loadMoreSearch()" class="bg-[#1c1f26] hover:bg-blue-600 border border-gray-700 text-xs font-bold py-3 px-8 rounded-full transition">
                        MUAT LEBIH BANYAK
                    </button>
                </div>
            </div>
        </template>

        <template x-if="view === 'detail'">
            <div x-cloak class="animate-fade-in pb-20">
                <button @click="view = 'home'" class="mb-4 text-xs font-bold text-gray-400 hover:text-white flex items-center gap-2">
                    <i class="fa-solid fa-arrow-left"></i> KEMBALI
                </button>

                <div class="relative bg-[#15171c] rounded-2xl border border-gray-800 overflow-hidden shadow-2xl p-6 flex flex-col md:flex-row gap-8">
                    <div class="absolute top-0 right-0 w-full h-full bg-gradient-to-bl from-blue-900/10 to-transparent pointer-events-none"></div>

                    <div class="w-48 md:w-60 flex-shrink-0 mx-auto md:mx-0 relative z-10">
                        <img :src="activeDrama.series_cover" class="w-full rounded-xl shadow-2xl border border-gray-700">
                    </div>

                    <div class="flex-1 relative z-10 text-center md:text-left">
                        <h1 class="text-3xl font-black text-white mb-3 leading-tight" x-text="activeDrama.series_title"></h1>
                        
                        <div class="flex flex-wrap justify-center md:justify-start gap-2 mb-5">
                            <span class="bg-blue-600 text-[10px] font-bold px-2 py-1 rounded text-white"><i class="fa-solid fa-list mr-1"></i> <span x-text="activeDrama.episode_cnt"></span> EPS</span>
                            <span x-show="activeDrama.age_gate_info?.age_gate >= 18" class="bg-red-600 text-[10px] font-bold px-2 py-1 rounded text-white">18+</span>
                            <span class="bg-gray-800 text-gray-300 text-[10px] font-bold px-2 py-1 rounded border border-gray-700"><i class="fa-solid fa-thumbs-up mr-1"></i> <span x-text="formatNumber(activeDrama.followed_cnt)"></span></span>
                        </div>

                        <div class="bg-[#0f1014] p-4 rounded-xl border border-gray-800 mb-6 text-left">
                             <p class="text-gray-400 text-xs leading-relaxed" x-text="activeDrama.series_intro"></p>
                        </div>

                        <h3 class="text-xs font-bold text-gray-500 uppercase mb-3 tracking-widest text-left">Pilih Episode</h3>
                        <div class="grid grid-cols-5 sm:grid-cols-8 md:grid-cols-10 gap-2">
                            <template x-for="(eps, index) in activeDrama.video_list" :key="eps.vid">
                                <button @click="openPlayer(index)" 
                                    class="group bg-[#1c1f26] hover:bg-blue-600 border border-gray-800 p-2 rounded transition flex flex-col items-center justify-center">
                                    <span class="text-xs font-bold text-white" x-text="eps.vid_index"></span>
                                    <span class="text-[8px] text-gray-500 group-hover:text-blue-100 mt-0.5" x-text="formatTime(eps.duration)"></span>
                                </button>
                            </template>
                        </div>
                    </div>
                </div>
            </div>
        </template>

        <template x-if="view === 'player'">
            <div class="fixed inset-0 bg-black z-[9999] flex flex-col items-center justify-center">
                <div class="absolute top-0 w-full p-4 flex justify-between items-center bg-gradient-to-b from-black via-black/80 to-transparent z-20">
                    <button @click="view = 'detail'" class="text-white bg-white/10 px-4 py-1.5 rounded-full text-xs font-bold backdrop-blur border border-white/10 hover:bg-white/20 transition">
                        ✕ TUTUP
                    </button>
                    <div class="text-right">
                        <p class="text-[10px] text-gray-400 font-bold uppercase tracking-wider" x-text="activeDrama.series_title"></p>
                        <p class="text-sm font-black text-blue-500" x-text="'EPISODE ' + activeDrama.video_list[currentIdx].vid_index"></p>
                    </div>
                </div>

                <div class="w-full max-w-lg aspect-[9/16] relative bg-black shadow-2xl">
                    <video x-ref="videoPlayer" :src="streamUrl" @error="handleError" @ended="nextEps" controls autoplay playsinline class="w-full h-full object-contain"></video>
                </div>

                <div class="absolute bottom-0 w-full max-w-lg p-6 bg-gradient-to-t from-black via-black/90 to-transparent z-20 pb-10">
                    <div class="flex gap-4">
                        <button @click="prevEps()" :disabled="currentIdx === 0" 
                            class="flex-1 bg-[#1c1f26] hover:bg-gray-700 py-3 rounded-xl font-bold text-xs disabled:opacity-30 border border-gray-700 transition">
                            <i class="fa-solid fa-backward mr-2"></i> PREV
                        </button>
                        <button @click="nextEps()" :disabled="currentIdx === activeDrama.video_list.length - 1" 
                            class="flex-[2] bg-blue-600 hover:bg-blue-500 py-3 rounded-xl font-bold text-xs disabled:opacity-30 shadow-lg shadow-blue-600/20 transition">
                            NEXT EPISODE <i class="fa-solid fa-forward ml-2"></i>
                        </button>
                    </div>
                </div>
            </div>
        </template>

    </main>

    <script>
        function albedoApp() {
            return {
                view: 'home',
                loading: false,
                searchQuery: '',
                
                // Data Containers
                trendingList: [],
                trendingOffset: 0,
                trendingHasMore: true,

                latestList: [],
                latestOffset: 0,
                latestHasMore: true,

                searchList: [],
                searchOffset: 0,
                searchHasMore: true,

                activeDrama: null,
                streamUrl: '',
                backupUrl: '',
                currentIdx: 0,
                
                async init() {
                    await this.loadInitialData();
                    
                    // Auto-Next Listener
                    this.$watch('view', value => {
                        if (value === 'player') {
                            this.$nextTick(() => {
                                const vid = this.$refs.videoPlayer;
                                vid.onended = () => this.nextEps();
                                vid.onerror = () => this.handleError();
                            });
                        }
                    });
                },

                async loadInitialData() {
                    this.loading = true;
                    try {
                        const [t, l] = await Promise.all([
                            fetch('/api/trending?offset=0').then(r => r.json()),
                            fetch('/api/latest?offset=0').then(r => r.json())
                        ]);
                        
                        this.trendingList = t.books.map(b => this.normalize(b, 'home'));
                        this.trendingOffset = t.next_offset || 10;
                        this.trendingHasMore = t.has_more;

                        this.latestList = l.books.map(b => this.normalize(b, 'home'));
                        this.latestOffset = l.next_offset || 10;
                        this.latestHasMore = l.has_more;

                    } catch(e) { console.error(e); }
                    this.loading = false;
                },

                // LOAD MORE FUNCTION (TRENDING)
                async loadMoreTrending() {
                    this.loading = true;
                    try {
                        const res = await fetch(`/api/trending?offset=${this.trendingOffset}`);
                        const json = await res.json();
                        const newItems = json.books.map(b => this.normalize(b, 'home'));
                        this.trendingList = [...this.trendingList, ...newItems];
                        this.trendingOffset = json.next_offset;
                        this.trendingHasMore = json.has_more;
                    } catch(e) { console.error(e); }
                    this.loading = false;
                },

                // LOAD MORE FUNCTION (LATEST)
                async loadMoreLatest() {
                    this.loading = true;
                    try {
                        const res = await fetch(`/api/latest?offset=${this.latestOffset}`);
                        const json = await res.json();
                        const newItems = json.books.map(b => this.normalize(b, 'home'));
                        this.latestList = [...this.latestList, ...newItems];
                        this.latestOffset = json.next_offset;
                        this.latestHasMore = json.has_more;
                    } catch(e) { console.error(e); }
                    this.loading = false;
                },

                // SEARCH FUNCTION
                async doSearch(isNew = false) {
                    if (!this.searchQuery) return;
                    if (isNew) {
                        this.searchOffset = 0;
                        this.searchList = [];
                        this.searchHasMore = true;
                    }
                    this.view = 'search';
                    this.loading = true;

                    try {
                        const res = await fetch(`/api/search?q=${this.searchQuery}&offset=${this.searchOffset}`);
                        const json = await res.json();
                        
                        if (json.data && json.data.search_data) {
                            const newItems = json.data.search_data.map(b => this.normalize(b, 'search'));
                            this.searchList = [...this.searchList, ...newItems];
                            this.searchOffset = json.next_offset || (this.searchOffset + 10);
                            this.searchHasMore = json.has_more;
                        } else {
                            this.searchHasMore = false;
                        }
                    } catch(e) { console.error(e); }
                    this.loading = false;
                },

                async loadMoreSearch() {
                    this.doSearch(false);
                },

                resetHome() {
                    this.searchQuery = '';
                    this.view = 'home';
                },

                // NORMALISASI DATA (PENTING BIAR SERAGAM)
                normalize(raw, type) {
                    let id, title, cover, genre, totalEps, isFinished, is18;

                    if (type === 'search') {
                        const book = raw.books[0]; 
                        id = raw.id;
                        title = book.book_name;
                        cover = book.thumb_url;
                        genre = book.stat_infos ? book.stat_infos[0] : 'Drama';
                        isFinished = book.stat_infos && book.stat_infos.includes('Selesai');
                        totalEps = book.serial_count || '?';
                        is18 = false; 
                    } else {
                        id = raw.book_id;
                        title = raw.book_name;
                        cover = raw.thumb_url;
                        genre = raw.stat_infos ? raw.stat_infos[0] : 'Drama';
                        totalEps = raw.serial_count;
                        isFinished = raw.show_creation_status === 'Selesai';
                        is18 = raw.visibility_age_gate === '18';
                    }
                    return { id, title, cover, genre, totalEps, isFinished, is18 };
                },

                async openDetail(id) {
                    this.loading = true;
                    try {
                        const res = await fetch(`/api/detail?id=${id}`);
                        const json = await res.json();
                        this.activeDrama = json.data.video_data;
                        this.view = 'detail';
                        window.scrollTo(0,0);
                    } catch(e) { console.error(e); }
                    this.loading = false;
                },

                async openPlayer(idx) {
                    this.currentIdx = idx;
                    this.loading = true;
                    const vid = this.activeDrama.video_list[idx].vid;
                    try {
                        const res = await fetch(`/api/stream?vid=${vid}`);
                        const json = await res.json();
                        this.streamUrl = json.data.main_url;
                        this.backupUrl = json.data.backup_url;
                        this.view = 'player';
                    } catch(e) { alert('Stream error'); }
                    this.loading = false;
                },

                handleError() {
                    if (this.streamUrl !== this.backupUrl && this.backupUrl) {
                        console.log("Switching to backup...");
                        this.streamUrl = this.backupUrl;
                    }
                },

                nextEps() {
                    if (this.currentIdx < this.activeDrama.video_list.length - 1) this.openPlayer(this.currentIdx + 1);
                },
                prevEps() {
                    if (this.currentIdx > 0) this.openPlayer(this.currentIdx - 1);
                },
                formatNumber(num) { return new Intl.NumberFormat('id-ID', { notation: "compact" }).format(num); },
                formatTime(s) { return `${Math.floor(s/60)}:${(s%60).toString().padStart(2,'0')}`; },
                parseTags(str) { try { return JSON.parse(str); } catch { return []; } }
            }
        }
    </script>
</body>
</html>
"""

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
