String.prototype.format = function (o) {
    return this.replace(/{([^{}]*)}/g,
        function (a, b) {
            var r = o[b];
            return typeof r === 'string' || typeof r === 'number' ? r : a;
        }
    );
};

// // Usage:
// alert("I'm {age} years old!".format({ age: 29 }));
// alert("The {a} says {n}, {n}, {n}!".format({ a: 'cow', n: 'moo' }));
