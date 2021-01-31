// Electron
const { app, BrowserWindow, Menu, ipcMain, globalShortcut, ipcRenderer } = require('electron');
// FileSystem
const fs = require('fs');
// PythonShell
const { PythonShell } = require('python-shell');
// socket.io-Server
var fs = require('fs');
var http = require('http');
var server = http.createServer();
// Socket.io-Client
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
 * Initialize Shortcut Event Handler
 * @param {Array[string]} keys ['ctrl-v', 'ctrl-s']
 */
function initShortcut(keys) {
    /**
     * Create Shortcut Event Handler
     * @param {string} key 'ctrl-v'
     */
    function shortcut(key) {
        globalShortcut.register(key, function () {
            logger(`'${key}'`, ['nodejs', 'shortcut']);
            window.webContents.send(key, key);
        });
    }
    keys.forEach(function (key) { shortcut(key); });
}
//----------------------------//

//----------TMP----------//
/**
 * Logger
 * @param {string} value Main Log
 * @param  {Array<string>} args ['arg', 'arg']
 * @returns {string} '[arg][arg] value'
 */
function logger(value, args) {
    const _ = (function (args) { let str = ''; args.forEach(function (e) { str += `[${e}]` }); return str })(args) + ' ' + String(value);
    console.log(_);
    window.webContents.send('nodejs_logger', _);
    return _
}
//-----------------------//

//----------Main Function----------//
/**
 * Find data by ranking
 * @param {object} event default value : { }
 * @param {number} id default value : 0
 * @returns {object} { ... }
 */
function findByRank(event = {}, id = 0) {
    const baseData = JSON.parse(fs.readFileSync('src/json/twitch.json', 'utf8'));
    const mainData = baseData['edges'][id]['node'];
    return mainData
}
//---------------------------------//

//----------ipcMain----------//
ipcMain.handle('findByRank', findByRank);
ipcMain.handle('chrome_connected', function (event, value) { logger('Connected.', ['chrome', 'socket.io-client']); });
ipcMain.handle('chrome_logger', function (event, value) { logger(value, ['chrome']); });
ipcMain.handle('python_StartEdit', function (event, value) { socket.emit('StartEdit', value); });
ipcMain.handle('python_server_port', function (event, value) { return port });
//---------------------------//

//----------Socket.io----------//
// Create Server
// const server = new PythonShell('src/python/socket.io.py', { args: ['-p', 8080] });
// Connect to Server
const socket = io.connect(`ws://localhost:8080`);
// Register client to Server
socket.emit('define_client', 'nodejs');
socket.on('python_logger', function (value) { logger(value, ['python', 'socket.io-server']); });
socket.on('connect', function (value) { logger('Connected.', ['nodejs', 'socket.io-client']); });
socket.on('python_StartEdit', function (value) { logger(value, ['python', 'socket.io-server']); });
//-----------------------------//

//----------MAIN PROCESS----------//
// start
app.on('ready', function () {
    createWindow();
    initWindowMenu();
    initShortcut(['ctrl+n', 'ctrl+p', 'ctrl+enter', 'shift+enter']);
});

// finish
app.on('window-all-closed', function () { if (process.platform !== 'darwin') { app.quit(); } });
//--------------------------------//
