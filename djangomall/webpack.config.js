var path = require('path'),
    webpack = require('webpack'),
    BundleTracker = require('webpack-bundle-tracker'),
    MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  context: __dirname,
  entry: ['./static/js/index', './static/css/base.css'],
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        resolve: {
          extensions: ['.js', '.jsx']
        },
        exclude: /node_modules/,
        use: ['babel-loader']
      },
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, "css-loader"]
      },
      {
        test: /\.(jpg|png|svg|ttf|woff|woff2|eot)\??.*$/,
        use: [{
          loader: "url-loader",
          options: {
            limit: 8192,
            name: '[name].[ext]'
          }
        }]
      },
    ]
  },
  output: {
        path: path.resolve('./static/webpack_bundles/'),
        publicPath: '/static/webpack_bundles/',
        filename: "[name].js"
    },
    plugins: [
        new MiniCssExtractPlugin(),
        new BundleTracker({filename: './webpack-stats.json'})
    ],
};