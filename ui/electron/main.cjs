const { app, BrowserWindow, Menu, shell } = require('electron')
const { spawn } = require('node:child_process')
const fs = require('node:fs')
const http = require('node:http')
const path = require('node:path')

const repoRoot = path.resolve(__dirname, '..', '..')
const uiRoot = path.resolve(__dirname, '..')
const tmpDir = path.join(repoRoot, 'tmp')
const apiHealthUrl = 'http://127.0.0.1:8000/api/health'
const devUiUrl = 'http://127.0.0.1:5173'

let apiProcess = null
let mainWindow = null

function sendMenuAction(action) {
  const win = BrowserWindow.getFocusedWindow() || mainWindow
  if (!win || win.isDestroyed()) return

  const detail = JSON.stringify(action)
  void win.webContents.executeJavaScript(
    `window.dispatchEvent(new CustomEvent('formaltrust:native-menu', { detail: ${detail} }))`,
  )
}

function buildAppMenu() {
  const isMac = process.platform === 'darwin'
  const template = [
    ...(isMac
      ? [
          {
            label: app.name,
            submenu: [{ role: 'about' }, { type: 'separator' }, { role: 'hide' }, { role: 'quit' }],
          },
        ]
      : []),
    {
      label: '文件',
      submenu: [
        { label: '新建配置', accelerator: 'CmdOrCtrl+N', click: () => sendMenuAction('new-config') },
        { label: '保存配置', accelerator: 'CmdOrCtrl+S', click: () => sendMenuAction('save-config') },
        { type: 'separator' },
        { label: '运行实验', accelerator: 'CmdOrCtrl+Enter', click: () => sendMenuAction('run-experiment') },
        { label: '刷新全部', accelerator: 'CmdOrCtrl+R', click: () => sendMenuAction('refresh-all') },
        { type: 'separator' },
        isMac ? { role: 'close' } : { role: 'quit', label: '退出' },
      ],
    },
    {
      label: '编辑',
      submenu: [
        { label: '添加节点', accelerator: 'CmdOrCtrl+Shift+N', click: () => sendMenuAction('add-node') },
        { label: '重建线性流程', click: () => sendMenuAction('rebuild-edges') },
        { type: 'separator' },
        { role: 'undo', label: '撤销' },
        { role: 'redo', label: '重做' },
        { type: 'separator' },
        { role: 'cut', label: '剪切' },
        { role: 'copy', label: '复制' },
        { role: 'paste', label: '粘贴' },
        { role: 'selectAll', label: '全选' },
      ],
    },
    {
      label: '视图',
      submenu: [
        { label: '配置实验', accelerator: 'CmdOrCtrl+1', click: () => sendMenuAction('view-configure') },
        { label: '运行队列', accelerator: 'CmdOrCtrl+2', click: () => sendMenuAction('view-run') },
        { label: '结果查看', accelerator: 'CmdOrCtrl+3', click: () => sendMenuAction('view-results') },
        { type: 'separator' },
        { label: '切换资源栏', accelerator: 'CmdOrCtrl+B', click: () => sendMenuAction('toggle-left-sidebar') },
        { label: '切换状态栏', accelerator: 'CmdOrCtrl+Shift+B', click: () => sendMenuAction('toggle-right-sidebar') },
        { type: 'separator' },
        { label: '刷新运行状态', click: () => sendMenuAction('refresh-runtime') },
        { type: 'separator' },
        { role: 'toggleDevTools', label: '开发者工具' },
        { role: 'resetZoom', label: '实际大小' },
        { role: 'zoomIn', label: '放大' },
        { role: 'zoomOut', label: '缩小' },
      ],
    },
    {
      label: '帮助',
      submenu: [
        { label: '关于 FormalTrust', click: () => sendMenuAction('show-about') },
        {
          label: '打开项目目录',
          click: () => {
            void shell.openPath(repoRoot)
          },
        },
      ],
    },
  ]

  return Menu.buildFromTemplate(template)
}

function urlOk(url) {
  return new Promise((resolve) => {
    const request = http.get(url, (response) => {
      response.resume()
      resolve(response.statusCode >= 200 && response.statusCode < 400)
    })
    request.on('error', () => resolve(false))
    request.setTimeout(800, () => {
      request.destroy()
      resolve(false)
    })
  })
}

async function waitForUrl(url, timeoutMs = 15000) {
  const started = Date.now()
  while (Date.now() - started < timeoutMs) {
    if (await urlOk(url)) return true
    await new Promise((resolve) => setTimeout(resolve, 300))
  }
  return false
}

async function ensureApi() {
  if (await urlOk(apiHealthUrl)) return
  fs.mkdirSync(tmpDir, { recursive: true })
  const out = fs.openSync(path.join(tmpDir, 'formaltrust_desktop_api.out.log'), 'a')
  const err = fs.openSync(path.join(tmpDir, 'formaltrust_desktop_api.err.log'), 'a')
  apiProcess = spawn(
    'python',
    ['-m', 'uvicorn', 'formaltrust_platform.web_api:app', '--host', '127.0.0.1', '--port', '8000'],
    {
      cwd: repoRoot,
      detached: false,
      stdio: ['ignore', out, err],
      windowsHide: true,
    },
  )
  await waitForUrl(apiHealthUrl)
}

async function resolveUiUrl() {
  if (await urlOk(devUiUrl)) return devUiUrl
  return `file://${path.join(uiRoot, 'dist', 'index.html')}`
}

async function createWindow() {
  await ensureApi()
  const win = new BrowserWindow({
    width: 1440,
    height: 920,
    minWidth: 1100,
    minHeight: 720,
    title: 'FormalTrust 本地控制台',
    backgroundColor: '#f3f6f7',
    autoHideMenuBar: false,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
    },
  })
  mainWindow = win

  win.on('closed', () => {
    if (mainWindow === win) mainWindow = null
  })

  win.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url)
    return { action: 'deny' }
  })

  await win.loadURL(await resolveUiUrl())
}

app.whenReady().then(() => {
  Menu.setApplicationMenu(buildAppMenu())
  void createWindow()
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) void createWindow()
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})

app.on('before-quit', () => {
  if (apiProcess) {
    apiProcess.kill()
    apiProcess = null
  }
})
