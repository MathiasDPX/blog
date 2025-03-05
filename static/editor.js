const codeArea = document.getElementById('code')
const previewFrame = document.getElementById('preview')
const previewSwitch = document.getElementById('previewSwitch')
let lastCode = ''
let previewMode = false

function forceUpdatePreview() {
    const currentCode = codeArea.value
    const encodedCode = btoa(currentCode)
    let url = `http://127.0.0.1:5000/preview/${encodedCode}`
    if (previewMode) {
        url += "?website=True"
    }
    previewFrame.src = url
}

function updatePreview() {
    const currentCode = codeArea.value
    if (currentCode !== lastCode) {
        forceUpdatePreview();
        lastCode = currentCode
    }
}

function saveCode() {
    const currentCode = codeArea.value
    const blob = new Blob([currentCode], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'code.html'
    a.style.display = 'none'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
}

setInterval(updatePreview, 1000)
updatePreview()

document.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.key === 's') {
        event.preventDefault()
        saveCode()
    }
})

previewSwitch.addEventListener('change', function(event) {
    previewMode = event.target.checked
    forceUpdatePreview()
})