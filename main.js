// Electron
const { app, BrowserWindow, Menu, ipcMain, globalShortcut } = require('electron');
// FileSystem
const fs = require('fs');
// PythonShell
const { PythonShell } = require('python-shell');
// Socket.io Client
const io = require('socket.io-client');


//----------Electron----------//
// Electron Window
let window;
/**
 *Create Electron Window (if Electron-App is ready)
 */
function createWindow() {
    window = new BrowserWindow({
        // frame: false,
        // fullscreen: true,
        width: 1824,
        height: 1216,
        titleBarStyle: 'hiddenInset',
        maximizable: true,
        minWidth: 960,
        minHeight: 540,
        webPreferences: {
            nodeIntegration: true
        }
    });
    window.loadFile('src/html/index.html');
    window.webContents.openDevTools();
}
/**
 * Initialize Window Menu (if Electron-App is ready)
 */
function initWindowMenu() {
    const template = [
        // { role: 'fileMenu' }
        { label: 'File', submenu: [{ role: 'quit' }] },
        // { role: 'editMenu' }
        { label: 'Edit', submenu: [{ role: 'undo' }, { role: 'redo' }, { type: 'separator' }, { role: 'cut' }, { role: 'copy' }, { role: 'paste' }, { role: 'delete' }, { type: 'separator' }, { role: 'selectAll' }] },
        // { role: 'viewMenu' }
        { label: 'View', submenu: [{ role: 'reload' }, { role: 'forceReload' }, { role: 'toggleDevTools' }, { type: 'separator' }, { role: 'resetZoom' }, { role: 'zoomIn' }, { role: 'zoomOut' }, { type: 'separator' }, { role: 'togglefullscreen' }] },
        // { role: 'windowMenu' }
        { label: 'Window', submenu: [{ role: 'minimize' }, { role: 'maximize' }, { role: 'zoom' }, { role: 'close' }] }
    ];
    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
}
/**
 * Define Shortcut (if executed, send its data to Window.)
 * @param {string} key 
 */
function shortcut(key) {
    globalShortcut.register(key, function () {
        window.webContents.send(key, true);
    });
}
//----------Electron----------//


//----------TMP----------//
function log(value, ...args) {
    const _ = (function (args) { let str = ''; args.forEach(function (e) { str += `[${e}]` }); return str })(args) + ' ' + String(value);
    console.log(_);
    return _
}
/**
 * tem function for test
 * @param {object} event
 * @param {string} file 'xxx.py'
 * @returns {string} 'started'
 */
function python_ctrl(event, file) {
    socket.emit('first', 'hello', function () { });
    return 'started'
}
//----------TMP----------//

//----------  ----------//
/**
 * Find data by ranking
 * @param {object} event 
 * @param {number} id 
 */
function findByRank(event = {}, id = 0) {
    const baseData = JSON.parse(fs.readFileSync('src/json/twitch.json', 'utf8'));
    const mainData = baseData['edges'][id]['node'];
    return mainData
}
//----------  ----------//

//----------MAIN PROCESS----------//
// Create Server
const server = new PythonShell('src/python/socket.io.py');
// Connect to Server
const socket = io.connect('ws://localhost:8256');
// Register client to Server
socket.emit('define_client', 'nodejs');

// start
app.on('ready', function () {
    createWindow();
    initWindowMenu();

    shortcut('ctrl+n');
    shortcut('ctrl+p');
    shortcut('ctrl+enter');
    shortcut('shift+enter');

    ipcMain.handle('findByRank', findByRank);
    ipcMain.handle('python_start', python_ctrl);
    // Socket.io
    socket.on('connect', function (data) { console.log('[Socket.io] Connected to Python Server'); });
    ipcMain.handle('python_start_request', function (event, value) { socket.emit('python_start_request', value); return log('Request accepted', 'nodejs') });
    socket.on('python_start_request', function (value) { window.webContents.send('python_start_request', value); });
});

// finish
app.on('window-all-closed', function () { if (process.platform !== 'darwin') { app.quit(); } });