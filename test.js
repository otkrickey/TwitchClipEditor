
function log(value, ...args) {
    console.log((function (args) { let str = ''; args.forEach(function (e) { str += `[${e}]` }); return str })(args) + ' ' + String(value));
}

log('started', 'python', 'console');