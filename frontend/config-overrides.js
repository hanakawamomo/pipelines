/**
 * Monkey patch webpack.config.js in react-scripts to manually inject bundles with nonce placeholder.
 */
module.exports = function override(config) {
    const indexHtmlPlugin = config.plugins.shift();
    indexHtmlPlugin.userOptions["inject"] = false;
    config.plugins.unshift(indexHtmlPlugin);
    return config;
};
