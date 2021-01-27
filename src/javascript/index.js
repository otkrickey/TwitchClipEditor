const { ipcRenderer, Main, shell } = require('electron');
const io = require('socket.io-client');
const socket = io('ws://localhost:8256');
// define client to server
socket.emit('define_client', 'web_client');

// グローバル変数の定義
// 変数の変更イベントの管理
const AppData = {
    Clips: {},
    Nodes: {
        info: document.getElementById('info'),
        next: document.getElementById('next'),
        previous: document.getElementById('previous'),
        ranking: document.getElementById('ranking'),
        progress: document.getElementById("progress"),
        form: document.twitch,
    },
    h: {
        frame: 0,
        rank: 0,
    },
};
// AppData.currentRanking のゲッター・セッター定義
Object.defineProperty(AppData, 'currentRanking', {
    get() { return this.h.rank; },
    set(value) {
        this.h.rank = value;
        // データがある場合 -> レンダリング
        if (AppData.Clips[value]) { renderClipInfo(value); }
        // データがない場合 -> リクエストした後にレンダリング
        else { findByRank(value, function () { renderClipInfo(value); }); }
        // 周辺データのプリロード
        for (let i = 1; i < 5; i++) {
            // 前のデータ
            if (!AppData.Clips[value - i] && value > i) { findByRank(value - i); }
            // 後のデータ
            if (!AppData.Clips[value + i]) { findByRank(value + i); }
        }
    }
});
// AppData.python のゲッター・セッター定義
Object.defineProperty(AppData, 'python', {
    get() { return this.h.frame },
    set(value) {
        this.h.frame = value;
        this.Nodes.asd.innerHTML = value;
    }
});


// ボタンとショートカットキーのアクションを指定（どちらもイベント時にアクション）
function ButtonShortcut(key = undefined, node = undefined, action = () => { }) { if (key) { ipcRenderer.on(key, function (event, value) { action(node); }); } if (node) { node.addEventListener('click', action); } }
// ランクを指定して検索・取得
// コールバックでは情報取得直後の動作を指定（デフォルトでは処理なし）
async function findByRank(rank, callback = () => { }) { AppData.Clips[rank] = await ipcRenderer.invoke('findByRank', rank); callback(); }
// クリップのレンダリング
function renderClipInfo(rank) {
    // クリップデータが読み込まれていなかった場合、データを取得し、再帰的にこの関数を実行
    // 余りよろしくはないが、この関数を実行するだけでレンダリングはできる。
    if (!AppData.Clips[rank]) { findByRank(rank, function () { renderClipInfo(rank); }); }
    // クリップデータが読み込まれている場合、レンダリングを実行
    else {
        const BaseData = AppData.Clips[rank];
        const node = AppData.Nodes.info;
        MainData = { ranking: rank + 1, title: BaseData.title, name: BaseData.broadcaster.displayName, profile: BaseData.broadcaster.profileImageURL, url: BaseData.url, view_count: BaseData.viewCount, id: BaseData.id, }
        node.innerHTML = "";
        node.insertAdjacentHTML('beforeend', `<div class="clip" id="clip-${MainData.id}"><img class="info-profile-img" src="${MainData.profile}"><div class="info-detail"><p class="info-clip"><a href="javascript:shell.openExternal('${MainData.url}')">${MainData.title}</a></p><p class="info-profile-name">${MainData.name}</p></div><div class="right-side"><p class="info-view_count">${MainData.view_count}回視聴</p><p class="info-ranking">${MainData.ranking}位</p></div></div>`);
    }
}






// ウィンドウ読み込み時
window.onload = function () {
    // ウィンドウのロード時に最初のデータを取得・レンダリング
    AppData.currentRanking = 0;
    // イベントリスナーの設定
    ButtonShortcut('ctrl+n', AppData.Nodes.next, function (node) { AppData.currentRanking += 1; });
    ButtonShortcut('ctrl+p', AppData.Nodes.previous, function (node) { AppData.currentRanking -= AppData.currentRanking == 0 ? 0 : 1; });
    ButtonShortcut('ctrl+enter', AppData.Nodes.ranking, function (node) { node.focus(); });
    ButtonShortcut('shift+enter', undefined, function (node = undefined) { p(); });
    // 指定されたランキングで検索・取得・レンダリング
    AppData.Nodes.form.addEventListener('submit', function () {
        // フォームに入力されたランキングデータ
        const rank = document.twitch.ranking.value;
        AppData.currentRanking = Number(rank == '' ? 0 : rank);
    });
    ipcRenderer.on('python_start_request', function (event, value) { console.log(value); });
};

// テスト中
async function pydo() {
    AppData.Nodes.progress = document.getElementById("progress");
    ipcRenderer.on('python', function (event, value) {
        AppData.Nodes.progress.style.width = `${Number(value) / 10}px`;
    });
    const message = await ipcRenderer.invoke('python_start', 'test/test.py')
    console.log(message);
}

async function p(value = 6000) {
    AppData.Nodes.progress = document.getElementById("progress");
    const message = await ipcRenderer.invoke('python_start_request', value);
    console.log(message);
}

socket.on('python_executing', function (value) { AppData.Nodes.progress.style.width = `${Number(value) / 10}px`; });