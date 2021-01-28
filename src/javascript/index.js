// Electron
const { ipcRenderer, Main, shell } = require('electron');
// Socket.io-client
const io = require('socket.io-client');
//----------Initialize----------//
// Global Variable
const AppData = {
    Clips: {},
    Nodes: {
        asd: (function () { return document.getElementById('info'); })(),
        info: (function () { return document.getElementById('info'); })(),
        next: (function () { return document.getElementById('next'); })(),
        previous: (function () { return document.getElementById('previous'); })(),
        ranking: (function () { return document.getElementById('ranking'); })(),
        progress: (function () { return document.getElementById("progress"); })(),
        form: (function () { return document.twitch; })(),
    },
    h: {
        frame: 0,
        rank: 0,
    },
};
// Getter and Setter for AppData.currentRanking
Object.defineProperty(AppData, 'currentRanking', {
    /**
     * Get currentRanking value
     * @returns {number} 0
     */
    get() { return this.h.rank; },
    /**
     * Set currentRanking value
     * @param {number} value 0 - ...
     */
    set(value) {
        // update value
        this.h.rank = value;
        // if data exist -> Render
        if (AppData.Clips[value]) { renderClipInfo(value); }
        // if data not exist -> Render after Request
        else { findByRank(value, function () { renderClipInfo(value); }); }
        // Preload nearby data
        for (let i = 1; i < 5; i++) {
            if (!AppData.Clips[value - i] && value > i) { findByRank(value - i); } // former
            if (!AppData.Clips[value + i]) { findByRank(value + i); } // latter
        }
    }
});
/**
 * Render AppData.currentRanking data
 * @param {number} rank 0
 */
function renderClipInfo(rank) {
    // if data exist -> Render
    if (AppData.Clips[rank]) {
        const BaseData = AppData.Clips[rank];
        const node = AppData.Nodes.info;
        // Pick up the data we need
        const MainData = {
            ranking: rank + 1,
            title: BaseData.title,
            name: BaseData.broadcaster.displayName,
            profile: BaseData.broadcaster.profileImageURL,
            url: BaseData.url,
            view_count: BaseData.viewCount,
            id: BaseData.id,
        }
        // prepare html
        const html = `
            <div class="clip" id="clip-${MainData.id}">
                <img class="info-profile-img" src="${MainData.profile}">
                <div class="info-detail">
                    <p class="info-clip">
                        <a href="javascript:shell.openExternal('${MainData.url}')">${MainData.title}</a>
                    </p>
                    <p class="info-profile-name">${MainData.name}</p>
                </div>
                <div class="right-side">
                    <p class="info-view_count">${MainData.view_count}回視聴</p>
                    <p class="info-ranking">${MainData.ranking}位</p>
                </div>
            </div>
        `;
        // Clear node
        node.innerHTML = "";
        // Render
        node.insertAdjacentHTML('beforeend', html);
    }
    // if data not exist -> Render after Request
    else {
        // Request
        findByRank(rank, function () {
            // callback this function
            renderClipInfo(rank);
        });
    }
}
/**
 * Initialize Shortcuts
 */
function initShortcut() {
    /**
     * Behavior when Shortcut or click-node
     * @param {string} key null ('ctrl-v')
     * @param {object} node null (html-node)
     * @param {function} action function(){}
     */
    function ButtonShortcut(key = null, node = null, action = function () { }) {
        if (key) { ipcRenderer.on(key, function (event, value) { action(node); }); }
        if (node) { node.addEventListener('click', function (event) { action(node); }); }
    }
    ButtonShortcut(
        key = 'ctrl+n',
        node = AppData.Nodes.next,
        action = function (node) {
            AppData.currentRanking += 1;
        }
    );
    ButtonShortcut(
        key = 'ctrl+p',
        node = AppData.Nodes.previous,
        action = function (node) {
            AppData.currentRanking -= AppData.currentRanking == 0 ? 0 : 1;
        }
    );
    ButtonShortcut(
        key = 'ctrl+enter',
        node = AppData.Nodes.ranking,
        action = function (node) {
            node.focus();
        }
    );
    ButtonShortcut(
        key = 'shift+enter',
        node = undefined,
        action = function (node) {
            p(2400);
        }
    );
}
/**
 * Initialize EventListeners
 */
function initEventListener() {
    AppData.Nodes.form.addEventListener('submit', function (event) {
        // <input> value
        const rank = document.twitch.ranking.value;
        AppData.currentRanking = Number(rank == '' ? 0 : rank);
    });
}
//------------------------------//
//----------TMP----------//
/**
 * Logger
 * @param {string} value Main Log
 * @param  {Array<string>} args ['arg', 'arg']
 * @returns {string} '[arg][arg] value'
 */
function logger(value) {
    ipcRenderer.invoke('chrome_logger', value);
}
function p(value = 6000) { ipcRenderer.invoke('python_StartEdit', value); }
//-----------------------//
//----------Main Function----------//
/**
 * Get data by specifying rank
 * @param {number} rank 0
 * @param {function} callback function(){}
 */
async function findByRank(rank, callback = function () { }) {
    AppData.Clips[rank] = await ipcRenderer.invoke('findByRank', rank);
    callback();
}
//---------------------------------//
//----------ipcRenderer----------//
ipcRenderer.on('nodejs_logger', function (event, value) { console.log(value); });
//-------------------------------//
//----------Socket.io----------//
// Connect to Server
const socket = io(`ws://localhost:8080`);
// Register client to Server
socket.emit('define_client', 'chrome');
socket.on('connect', function (value) { ipcRenderer.invoke('chrome_connected', 'chrome'); });
socket.on('python_Editing', function (value) { AppData.Nodes.progress.style.width = `${Number(value) / 10}px`; });
//-----------------------------//
//----------Main Process----------//
window.onload = function () {
    // initialize currentRanking
    AppData.currentRanking = 0;
    // initialize Shortcuts
    initShortcut();
    // Initialize EventListeners
    initEventListener();
};
//--------------------------------//