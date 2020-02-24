var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    }
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
/**
 * The unique id is used for unique hashes.
 */
var uniqueId = 0;
/**
 * Tag styles with this string to get unique hashes.
 */
export var IS_UNIQUE = '__DO_NOT_DEDUPE_STYLE__';
var upperCasePattern = /[A-Z]/g;
var msPattern = /^ms-/;
var interpolatePattern = /&/g;
var escapePattern = /[ !#$%&()*+,./;<=>?@[\]^`{|}~"'\\]/g;
var propLower = function (m) { return "-" + m.toLowerCase(); };
/**
 * CSS properties that are valid unit-less numbers.
 *
 * Ref: https://github.com/facebook/react/blob/master/packages/react-dom/src/shared/CSSProperty.js
 */
var CSS_NUMBER = {
    'animation-iteration-count': true,
    'border-image-outset': true,
    'border-image-slice': true,
    'border-image-width': true,
    'box-flex': true,
    'box-flex-group': true,
    'box-ordinal-group': true,
    'column-count': true,
    'columns': true,
    'counter-increment': true,
    'counter-reset': true,
    'flex': true,
    'flex-grow': true,
    'flex-positive': true,
    'flex-shrink': true,
    'flex-negative': true,
    'flex-order': true,
    'font-weight': true,
    'grid-area': true,
    'grid-column': true,
    'grid-column-end': true,
    'grid-column-span': true,
    'grid-column-start': true,
    'grid-row': true,
    'grid-row-end': true,
    'grid-row-span': true,
    'grid-row-start': true,
    'line-clamp': true,
    'line-height': true,
    'opacity': true,
    'order': true,
    'orphans': true,
    'tab-size': true,
    'widows': true,
    'z-index': true,
    'zoom': true,
    // SVG properties.
    'fill-opacity': true,
    'flood-opacity': true,
    'stop-opacity': true,
    'stroke-dasharray': true,
    'stroke-dashoffset': true,
    'stroke-miterlimit': true,
    'stroke-opacity': true,
    'stroke-width': true
};
// Add vendor prefixes to all unit-less properties.
for (var _i = 0, _a = Object.keys(CSS_NUMBER); _i < _a.length; _i++) {
    var property = _a[_i];
    for (var _b = 0, _c = ['-webkit-', '-ms-', '-moz-', '-o-', '']; _b < _c.length; _b++) {
        var prefix = _c[_b];
        CSS_NUMBER[prefix + property] = true;
    }
}
/**
 * Escape a CSS class name.
 */
export var escape = function (str) { return str.replace(escapePattern, '\\$&'); };
/**
 * Transform a JavaScript property into a CSS property.
 */
export function hyphenate(propertyName) {
    return propertyName
        .replace(upperCasePattern, propLower)
        .replace(msPattern, '-ms-'); // Internet Explorer vendor prefix.
}
/**
 * Generate a hash value from a string.
 */
export function stringHash(str) {
    var value = 5381;
    var len = str.length;
    while (len--)
        value = (value * 33) ^ str.charCodeAt(len);
    return (value >>> 0).toString(36);
}
/**
 * Transform a style string to a CSS string.
 */
function styleToString(key, value) {
    if (typeof value === 'number' && value !== 0 && !CSS_NUMBER.hasOwnProperty(key)) {
        return key + ":" + value + "px";
    }
    return key + ":" + value;
}
/**
 * Sort an array of tuples by first value.
 */
function sortTuples(value) {
    return value.sort(function (a, b) { return a[0] > b[0] ? 1 : -1; });
}
/**
 * Categorize user styles.
 */
function parseStyles(styles, hasNestedStyles) {
    var properties = [];
    var nestedStyles = [];
    var isUnique = false;
    // Sort keys before adding to styles.
    for (var _i = 0, _a = Object.keys(styles); _i < _a.length; _i++) {
        var key = _a[_i];
        var value = styles[key];
        if (value !== null && value !== undefined) {
            if (key === IS_UNIQUE) {
                isUnique = true;
            }
            else if (typeof value === 'object' && !Array.isArray(value)) {
                nestedStyles.push([key.trim(), value]);
            }
            else {
                properties.push([hyphenate(key.trim()), value]);
            }
        }
    }
    return {
        style: stringifyProperties(sortTuples(properties)),
        nested: hasNestedStyles ? nestedStyles : sortTuples(nestedStyles),
        isUnique: isUnique
    };
}
/**
 * Stringify an array of property tuples.
 */
function stringifyProperties(properties) {
    return properties.map(function (_a) {
        var name = _a[0], value = _a[1];
        if (!Array.isArray(value))
            return styleToString(name, value);
        return value.map(function (x) { return styleToString(name, x); }).join(';');
    }).join(';');
}
/**
 * Interpolate CSS selectors.
 */
function interpolate(selector, parent) {
    if (selector.indexOf('&') === -1)
        return parent + " " + selector;
    return selector.replace(interpolatePattern, parent);
}
/**
 * Recursive loop building styles with deferred selectors.
 */
function stylize(selector, styles, rulesList, stylesList, parent) {
    var _a = parseStyles(styles, selector !== ''), style = _a.style, nested = _a.nested, isUnique = _a.isUnique;
    var pid = style;
    if (selector.charCodeAt(0) === 64 /* @ */) {
        var child = { selector: selector, styles: [], rules: [], style: parent ? '' : style };
        rulesList.push(child);
        // Nested styles support (e.g. `.foo > @media > .bar`).
        if (style && parent)
            child.styles.push({ selector: parent, style: style, isUnique: isUnique });
        for (var _i = 0, nested_1 = nested; _i < nested_1.length; _i++) {
            var _b = nested_1[_i], name = _b[0], value = _b[1];
            pid += name + stylize(name, value, child.rules, child.styles, parent);
        }
    }
    else {
        var key = parent ? interpolate(selector, parent) : selector;
        if (style)
            stylesList.push({ selector: key, style: style, isUnique: isUnique });
        for (var _c = 0, nested_2 = nested; _c < nested_2.length; _c++) {
            var _d = nested_2[_c], name = _d[0], value = _d[1];
            pid += name + stylize(name, value, rulesList, stylesList, key);
        }
    }
    return pid;
}
/**
 * Transform `stylize` tree into style objects.
 */
function composeStylize(cache, pid, rulesList, stylesList, className, isStyle) {
    for (var _i = 0, stylesList_1 = stylesList; _i < stylesList_1.length; _i++) {
        var _a = stylesList_1[_i], selector = _a.selector, style = _a.style, isUnique = _a.isUnique;
        var key = isStyle ? interpolate(selector, className) : selector;
        var id = isUnique ? "u\0" + (++uniqueId).toString(36) : "s\0" + pid + "\0" + style;
        var item = new Style(style, id);
        item.add(new Selector(key, "k\0" + pid + "\0" + key));
        cache.add(item);
    }
    for (var _b = 0, rulesList_1 = rulesList; _b < rulesList_1.length; _b++) {
        var _c = rulesList_1[_b], selector = _c.selector, style = _c.style, rules = _c.rules, styles = _c.styles;
        var item = new Rule(selector, style, "r\0" + pid + "\0" + selector + "\0" + style);
        composeStylize(item, pid, rules, styles, className, isStyle);
        cache.add(item);
    }
}
/**
 * Cache to list to styles.
 */
function join(arr) {
    var res = '';
    for (var i = 0; i < arr.length; i++)
        res += arr[i];
    return res;
}
/**
 * Noop changes.
 */
var noopChanges = {
    add: function () { return undefined; },
    change: function () { return undefined; },
    remove: function () { return undefined; }
};
/**
 * Implement a cache/event emitter.
 */
var Cache = /** @class */ (function () {
    function Cache(changes) {
        if (changes === void 0) { changes = noopChanges; }
        this.changes = changes;
        this.sheet = [];
        this.changeId = 0;
        this._keys = [];
        this._children = Object.create(null);
        this._counters = Object.create(null);
    }
    Cache.prototype.add = function (style) {
        var count = this._counters[style.id] || 0;
        var item = this._children[style.id] || style.clone();
        this._counters[style.id] = count + 1;
        if (count === 0) {
            this._children[item.id] = item;
            this._keys.push(item.id);
            this.sheet.push(item.getStyles());
            this.changeId++;
            this.changes.add(item, this._keys.length - 1);
        }
        else if (item instanceof Cache && style instanceof Cache) {
            var curIndex = this._keys.indexOf(style.id);
            var prevItemChangeId = item.changeId;
            item.merge(style);
            if (item.changeId !== prevItemChangeId) {
                this.sheet.splice(curIndex, 1, item.getStyles());
                this.changeId++;
                this.changes.change(item, curIndex, curIndex);
            }
        }
        return item;
    };
    Cache.prototype.remove = function (style) {
        var count = this._counters[style.id];
        if (count !== undefined && count > 0) {
            this._counters[style.id] = count - 1;
            var item = this._children[style.id];
            var index = this._keys.indexOf(item.id);
            if (count === 1) {
                delete this._counters[style.id];
                delete this._children[style.id];
                this._keys.splice(index, 1);
                this.sheet.splice(index, 1);
                this.changeId++;
                this.changes.remove(item, index);
            }
            else if (item instanceof Cache && style instanceof Cache) {
                var prevChangeId = item.changeId;
                item.unmerge(style);
                if (item.changeId !== prevChangeId) {
                    this.sheet.splice(index, 1, item.getStyles());
                    this.changeId++;
                    this.changes.change(item, index, index);
                }
            }
        }
    };
    Cache.prototype.values = function () {
        var _this = this;
        return this._keys.map(function (key) { return _this._children[key]; });
    };
    Cache.prototype.merge = function (cache) {
        for (var _i = 0, _a = cache.values(); _i < _a.length; _i++) {
            var item = _a[_i];
            this.add(item);
        }
        return this;
    };
    Cache.prototype.unmerge = function (cache) {
        for (var _i = 0, _a = cache.values(); _i < _a.length; _i++) {
            var item = _a[_i];
            this.remove(item);
        }
        return this;
    };
    Cache.prototype.clone = function () {
        return new Cache().merge(this);
    };
    return Cache;
}());
export { Cache };
/**
 * Selector is a dumb class made to represent nested CSS selectors.
 */
var Selector = /** @class */ (function () {
    function Selector(selector, id) {
        this.selector = selector;
        this.id = id;
    }
    Selector.prototype.getStyles = function () {
        return this.selector;
    };
    Selector.prototype.clone = function () {
        return new Selector(this.selector, this.id);
    };
    return Selector;
}());
export { Selector };
/**
 * The style container registers a style string with selectors.
 */
var Style = /** @class */ (function (_super) {
    __extends(Style, _super);
    function Style(style, id) {
        var _this = _super.call(this) || this;
        _this.style = style;
        _this.id = id;
        return _this;
    }
    Style.prototype.getStyles = function () {
        return this.sheet.join(',') + "{" + this.style + "}";
    };
    Style.prototype.clone = function () {
        return new Style(this.style, this.id).merge(this);
    };
    return Style;
}(Cache));
export { Style };
/**
 * Implement rule logic for style output.
 */
var Rule = /** @class */ (function (_super) {
    __extends(Rule, _super);
    function Rule(rule, style, id) {
        var _this = _super.call(this) || this;
        _this.rule = rule;
        _this.style = style;
        _this.id = id;
        return _this;
    }
    Rule.prototype.getStyles = function () {
        return this.rule + "{" + this.style + join(this.sheet) + "}";
    };
    Rule.prototype.clone = function () {
        return new Rule(this.rule, this.style, this.id).merge(this);
    };
    return Rule;
}(Cache));
export { Rule };
/**
 * The FreeStyle class implements the API for everything else.
 */
var FreeStyle = /** @class */ (function (_super) {
    __extends(FreeStyle, _super);
    function FreeStyle(hash, debug, id, changes) {
        var _this = _super.call(this, changes) || this;
        _this.hash = hash;
        _this.debug = debug;
        _this.id = id;
        return _this;
    }
    FreeStyle.prototype.registerStyle = function (styles, displayName) {
        var rulesList = [];
        var stylesList = [];
        var pid = stylize('&', styles, rulesList, stylesList);
        var hash = "f" + this.hash(pid);
        var id = this.debug && displayName ? displayName + "_" + hash : hash;
        composeStylize(this, pid, rulesList, stylesList, "." + escape(id), true);
        return id;
    };
    FreeStyle.prototype.registerKeyframes = function (keyframes, displayName) {
        return this.registerHashRule('@keyframes', keyframes, displayName);
    };
    FreeStyle.prototype.registerHashRule = function (prefix, styles, displayName) {
        var rulesList = [];
        var stylesList = [];
        var pid = stylize('', styles, rulesList, stylesList);
        var hash = "f" + this.hash(pid);
        var id = this.debug && displayName ? displayName + "_" + hash : hash;
        var rule = new Rule(prefix + " " + escape(id), '', "h\0" + pid + "\0" + prefix);
        composeStylize(rule, pid, rulesList, stylesList, '', false);
        this.add(rule);
        return id;
    };
    FreeStyle.prototype.registerRule = function (rule, styles) {
        var rulesList = [];
        var stylesList = [];
        var pid = stylize(rule, styles, rulesList, stylesList);
        composeStylize(this, pid, rulesList, stylesList, '', false);
    };
    FreeStyle.prototype.registerCss = function (styles) {
        return this.registerRule('', styles);
    };
    FreeStyle.prototype.getStyles = function () {
        return join(this.sheet);
    };
    FreeStyle.prototype.clone = function () {
        return new FreeStyle(this.hash, this.debug, this.id, this.changes).merge(this);
    };
    return FreeStyle;
}(Cache));
export { FreeStyle };
/**
 * Exports a simple function to create a new instance.
 */
export function create(hash, debug, changes) {
    if (hash === void 0) { hash = stringHash; }
    if (debug === void 0) { debug = typeof process !== 'undefined' && process.env.NODE_ENV !== 'production'; }
    if (changes === void 0) { changes = noopChanges; }
    return new FreeStyle(hash, debug, "f" + (++uniqueId).toString(36), changes);
}
//# sourceMappingURL=free-style.js.map